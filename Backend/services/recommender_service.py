"""Recommendation service – calls external ML service for ranking; Backend enriches from DB."""

import logging
import os
from pathlib import Path
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)

# Requirement keywords: request_text -> mentor attribute checks
_REQ_VISA = ("visa",)
_REQ_HOUSING = ("housing", "accommodation", "accommodations")
_REQ_CULTURAL = ("cultural", "culture", "adaptation")
_REQ_CAREER = ("career", "job", "employment")
# Field-of-study: phrases that imply user wants CS/tech
_REQ_FIELD_CS = (
    "computer science", "computing", "data science", "software", "programming",
    " cs ", "cs ", " it ", "information technology", "tech",
)
# Language names we detect in request text (lowercase); mentor languages_spoken can be "English;Mandarin" etc.
_LANGUAGE_KEYWORDS = (
    "mandarin", "chinese", "english", "spanish", "french", "hindi", "arabic",
    "italian", "german", "japanese", "korean", "vietnamese", "thai", "indonesian",
    "malay", "portuguese", "russian", "bengali", "tamil", "telugu", "turkish",
)

_BACKEND_ROOT = Path(__file__).resolve().parent.parent

# Known universities (for matching from request_text or user profile)
_KNOWN_UNIVERSITIES = (
    "Monash University", "University of Melbourne", "University of Sydney", "University of Queensland",
    "University of Western Australia", "University of Adelaide", "Australian National University",
    "Queensland University of Technology", "Deakin University", "University of Technology Sydney",
    "RMIT University", "University of New South Wales", "Macquarie University", "Swinburne University",
    "La Trobe University", "University of Wollongong", "Griffith University", "Curtin University",
    "University of Newcastle", "Flinders University", "James Cook University", "University of Tasmania",
)


def _get_ml_service_url() -> str:
    url = os.environ.get("ML_SERVICE_URL", "").strip()
    if not url:
        raise ValueError(
            "ML_SERVICE_URL is not set. Start the ML service (e.g. from repo root: cd ML && uvicorn api:app --port 8001) "
            "and set ML_SERVICE_URL to its base URL (e.g. http://127.0.0.1:8001)."
        )
    return url.rstrip("/")


def _call_ml_recommend(
    request_text: Optional[str] = None,
    user_profile: Optional[dict[str, Any]] = None,
    top_k: int = 5,
    candidate_university: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Call ML service POST /recommend; returns list of { mentor_id, final_score }."""
    base = _get_ml_service_url()
    payload = {
        "request_text": request_text or None,
        "user_profile": user_profile,
        "top_k": top_k,
        "candidate_university": candidate_university,
    }
    try:
        r = requests.post(f"{base}/recommend", json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []
    except requests.RequestException as e:
        logger.warning("ML service call failed: %s", e)
        return []


def _call_ml_evaluate(
    sample_size: int = 200,
    top_k: int = 5,
    seed: int = 42,
) -> dict[str, Any]:
    """Call ML service GET /evaluate; returns hit_rate_at_k, mrr, n_eval, top_k."""
    base = _get_ml_service_url()
    try:
        r = requests.get(
            f"{base}/evaluate",
            params={"sample_size": sample_size, "top_k": top_k, "seed": seed},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logger.warning("ML service evaluate call failed: %s", e)
        return {"hit_rate_at_k": 0.0, "mrr": 0.0, "n_eval": 0, "top_k": top_k}


def _normalize_university(name: Optional[str]) -> Optional[str]:
    """Return trimmed, non-empty university name or None."""
    if not name or not str(name).strip():
        return None
    return str(name).strip()


def _extract_university(user_profile: Optional[dict[str, Any]], request_text: str) -> Optional[str]:
    """
    Get university filter: from request_text if non-empty (priority), else from user profile (target_university).
    Used to filter mentors to that university.
    """
    text = (request_text or "").strip().lower()
    if text:
        for uni in _KNOWN_UNIVERSITIES:
            if uni.lower() in text:
                return _normalize_university(uni)
    if user_profile:
        target = user_profile.get("target_university")
        if target:
            return _normalize_university(target)
    return None


def _filter_results_by_university(
    results: list[dict[str, Any]], university_filter: Optional[str]
) -> list[dict[str, Any]]:
    """Keep only results whose mentor is from the given university (case-insensitive)."""
    if not university_filter or not results:
        return results
    u_lower = university_filter.strip().lower()
    out = []
    for item in results:
        mentor = item.get("mentor")
        if not isinstance(mentor, dict):
            uni = getattr(mentor, "university", None) if mentor else None
        else:
            uni = mentor.get("university")
        if uni and str(uni).strip().lower() == u_lower:
            out.append(item)
    return out


def _mentor_to_recommendation_item(mentor: Any, scores: dict[str, Any]) -> dict[str, Any]:
    """Build response item: mentor data nested, recommendation scores at top level."""
    mentor_data = {
        "mentor_id": mentor.id,
        "first_name": getattr(mentor, "first_name", None),
        "last_name": getattr(mentor, "last_name", None),
        "mentor_type": getattr(mentor, "mentor_type", None),
        "university": getattr(mentor, "university", None),
        "field_of_study": getattr(mentor, "field_of_study", None),
        "degree_level": getattr(mentor, "degree_level", None),
        "years_in_country": getattr(mentor, "years_in_country", None),
        "visa_experience": getattr(mentor, "visa_experience", None),
        "housing_experience": getattr(mentor, "housing_experience", None),
        "cultural_adaptation_experience": getattr(mentor, "cultural_adaptation_experience", None),
        "career_guidance_experience": getattr(mentor, "career_guidance_experience", None),
        "languages_spoken": getattr(mentor, "languages_spoken", None),
        "bio": getattr(mentor, "bio", None),
        "availability_hours_per_week": getattr(mentor, "availability_hours_per_week", None),
        "sessions_completed": getattr(mentor, "sessions_completed", None),
        "response_time_hours": getattr(mentor, "response_time_hours", None),
        "graduation_year": getattr(mentor, "graduation_year", None),
        "mentor_rating": getattr(mentor, "mentor_rating", None),
        "mentoring_topics": getattr(mentor, "mentoring_topics", None),
    }
    return {
        "mentor": mentor_data,
        "similarity": scores.get("similarity"),
        "quality_score": scores.get("quality_score"),
        "final_score": scores.get("final_score"),
        "interaction_count": scores.get("interaction_count"),
        "success_rate": scores.get("success_rate"),
    }


def _detect_requested_languages(request_text: Optional[str]) -> list[str]:
    """Detect which languages are mentioned in request text (e.g. 'speak Mandarin', 'English and Spanish')."""
    if not request_text or not request_text.strip():
        return []
    t = request_text.lower().strip()
    return [lang for lang in _LANGUAGE_KEYWORDS if lang in t]


def _mentor_speaks_any(mentor: dict[str, Any], languages: list[str]) -> bool:
    """True if mentor's languages_spoken contains any of the requested languages (case-insensitive)."""
    if not languages:
        return True
    spoken = (mentor.get("languages_spoken") or "").strip()
    if not spoken:
        return False
    parts = [p.strip().lower() for p in spoken.replace(";", ",").split(",") if p.strip()]
    for req in languages:
        for part in parts:
            if req in part or part in req:
                return True
    return False


def _detect_requirements(request_text: str) -> list[str]:
    """Detect which explicit requirements are mentioned in request text. Returns list of requirement keys."""
    if not request_text or not request_text.strip():
        return []
    t = request_text.lower().strip()
    reqs = []
    if any(k in t for k in _REQ_VISA):
        reqs.append("visa")
    if any(k in t for k in _REQ_HOUSING):
        reqs.append("housing")
    if any(k in t for k in _REQ_CULTURAL):
        reqs.append("cultural")
    if any(k in t for k in _REQ_CAREER):
        reqs.append("career")
    if any(k in t for k in _REQ_FIELD_CS):
        reqs.append("field_cs")
    return reqs


def _mentor_satisfies_requirement(mentor: dict[str, Any], req: str) -> bool:
    """Return True if mentor satisfies the given requirement."""
    if req == "visa":
        return (mentor.get("visa_experience") or 0) == 1
    if req == "housing":
        return (mentor.get("housing_experience") or 0) == 1
    if req == "cultural":
        return (mentor.get("cultural_adaptation_experience") or 0) == 1
    if req == "career":
        return (mentor.get("career_guidance_experience") or 0) == 1
    if req == "field_cs":
        field = (mentor.get("field_of_study") or "").lower()
        return any(
            x in field for x in ("computer", "computing", "data science", "software", "programming", "information technology", "it ", "cs")
        )
    return False


def _requirement_match_score(
    mentor: dict[str, Any],
    requirements: list[str],
    request_text: Optional[str] = None,
) -> float:
    """Return fraction of requirements satisfied by mentor (0 to 1). If no requirements, return 1.
    When request_text mentions languages, language counts as 2 requirement units so that
    mentors who speak the requested language rank clearly above those who don't.
    """
    total = len(requirements)
    satisfied = sum(1 for r in requirements if _mentor_satisfies_requirement(mentor, r))
    requested_languages = _detect_requested_languages(request_text or "") if request_text else []
    if requested_languages:
        total += 2
        if _mentor_speaks_any(mentor, requested_languages):
            satisfied += 2
    if total == 0:
        return 1.0
    return satisfied / total


def _rerank_by_requirements(
    results: list[dict[str, Any]],
    request_text: Optional[str],
    w_similarity: float = 0.65,
    w_quality: float = 0.15,
    w_requirement: float = 0.2,
) -> list[dict[str, Any]]:
    """
    Re-score and re-sort results using explicit requirement match when request_text is present.
    Puts mentors who satisfy visa/housing/field etc. higher when the user asked for them.
    When results come from the ML service we only have final_score (no similarity/quality_score);
    in that case we blend ML final_score with requirement_match instead of replacing it.
    """
    if not request_text or not results:
        return results
    requirements = _detect_requirements(request_text)
    if not requirements:
        return results

    for item in results:
        mentor = item.get("mentor") or {}
        sim = float(item.get("similarity") or 0)
        qual = float(item.get("quality_score") or 0)
        req_score = _requirement_match_score(mentor, requirements, request_text)
        item["requirement_match"] = req_score
        ml_score = item.get("final_score")
        # If we have ML final_score (from external ML service) but no similarity/quality, blend it with req_score
        if ml_score is not None and (sim == 0 and qual == 0):
            item["final_score"] = (1.0 - w_requirement) * float(ml_score) + w_requirement * req_score
        else:
            item["final_score"] = w_similarity * sim + w_quality * qual + w_requirement * req_score

    results.sort(key=lambda x: (float(x.get("final_score") or 0), float(x.get("similarity") or 0)), reverse=True)
    return results


def mentee_to_user_profile(mentee: Any, user: Any) -> dict[str, Any]:
    """
    Build a user_profile dict (users.csv shape) from DB User + Mentee.
    Used when recommending by mentee_id. Missing fields left as None/0 for recommender.
    """
    return {
        "user_id": getattr(user, "user_id", None),
        "first_name": getattr(user, "first_name", None),
        "last_name": getattr(user, "last_name", None),
        "user_type": getattr(mentee, "user_type", None),
        "home_country": getattr(mentee, "home_country", None),
        "preferred_city_type": None,
        "target_university": getattr(mentee, "university", None),
        "field_of_study": getattr(mentee, "field_of_study", None),
        "degree_level": getattr(mentee, "degree_level", None),
        "intended_start_year": None,
        "budget_range_aud": getattr(mentee, "budget_range", None),
        "scholarship_interest": None,
        "concern_visa": None,
        "concern_accommodation": None,
        "concern_safety": None,
        "concern_academics": None,
        "concern_career": None,
        "concern_culture": None,
        "preferred_language": getattr(mentee, "preferred_language", None),
        "accommodation_type": None,
        "work_while_studying_interest": None,
    }


def recommend(
    *,
    user_id: Optional[int] = None,
    request_text: str = "",
    top_k: int = 5,
    db_session: Optional[Any] = None,
) -> tuple[list[dict[str, Any]], Optional[dict[str, Any]]]:
    """
    Get ranked mentor recommendations. At least one of user_id or request_text (non-empty) required.
    - Both given: use only request_text (user profile ignored).
    - Only request_text: rank by free-text; if university in text, filter mentors by that university.
    - Only user_id: rank by user's mentee profile; filter by user's target university if set.
    Returns (list of mentor dicts with mentor + final_score, profile_used).
    """
    req_text = (request_text or "").strip()
    if user_id is None and not req_text:
        raise ValueError("Provide at least one of: request_text, user_id")

    user_profile: Optional[dict[str, Any]] = None
    profile_used: Optional[dict[str, Any]] = None
    # When request_text is given (including when both request_text and user_id are sent): ignore user_id.
    # All recommendation is done from request_text only. Load user profile only when request_text is empty.
    if not req_text and user_id is not None and db_session is not None:
        from models.user_model import User
        from sqlalchemy.orm import joinedload
        user = (
            db_session.query(User)
            .options(joinedload(User.mentee))
            .filter(User.user_id == user_id)
            .first()
        )
        if user is None:
            raise ValueError(f"user_id {user_id} not found")
        if user.mentee is not None:
            profile_used = mentee_to_user_profile(user.mentee, user)
            user_profile = profile_used

    # If request_text mentions a university (e.g. "Monash University"), filter mentors to that university.
    university_filter = _extract_university(user_profile, req_text)

    # Call ML service for ranking (returns list of { mentor_id, final_score }).
    ml_results = _call_ml_recommend(
        request_text=req_text or None,
        user_profile=user_profile,
        top_k=top_k,
        candidate_university=university_filter,
    )

    # Enrich from DB: fetch full mentor rows and build response with final_score from ML.
    if db_session is not None and ml_results:
        from models.mentor_model import Mentor

        ordered_mentor_ids = [r["mentor_id"] for r in ml_results]
        scores_by_id = {r["mentor_id"]: {"final_score": r["final_score"]} for r in ml_results}
        db_mentors = (
            db_session.query(Mentor)
            .filter(Mentor.id.in_(ordered_mentor_ids))
            .all()
        )
        if university_filter:
            u_lower = university_filter.strip().lower()
            db_mentors = [m for m in db_mentors if (getattr(m, "university", None) or "").strip().lower() == u_lower]
        db_by_id = {m.id: m for m in db_mentors}
        results = []
        for mid in ordered_mentor_ids:
            mentor = db_by_id.get(mid)
            if mentor is None:
                continue
            scores = scores_by_id.get(mid) or {}
            results.append(_mentor_to_recommendation_item(mentor, scores))
        results = _rerank_by_requirements(results, req_text)
        results = _filter_results_by_university(results, university_filter)
        return results, profile_used

    # When ML returns no results but we have DB: return mentors from DB (no ranking).
    if db_session is not None and not ml_results:
        from models.mentor_model import Mentor

        limit = (top_k * 3) if university_filter else top_k
        db_mentors = db_session.query(Mentor).order_by(Mentor.id).limit(limit).all()
        if university_filter:
            u_lower = university_filter.strip().lower()
            db_mentors = [m for m in db_mentors if (getattr(m, "university", None) or "").strip().lower() == u_lower][:top_k]
        else:
            db_mentors = db_mentors[:top_k]
        empty_scores: dict[str, Any] = {}
        results = [_mentor_to_recommendation_item(m, empty_scores) for m in db_mentors]
        results = _rerank_by_requirements(results, req_text)
        results = _filter_results_by_university(results, university_filter)
        return results, profile_used

    # ML returned results but no db_session: cannot enrich; return empty (API always passes db_session).
    return [], profile_used


def evaluate(sample_size: Optional[int] = 200, top_k: int = 5, seed: int = 42) -> dict[str, Any]:
    """Run offline evaluation via ML service; returns hit_rate_at_k, mrr, n_eval, top_k."""
    return _call_ml_evaluate(sample_size=sample_size, top_k=top_k, seed=seed)
