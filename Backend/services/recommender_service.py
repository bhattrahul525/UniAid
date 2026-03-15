"""Recommendation service – bridges Backend (mentee_id, DB) with ML recommender (users.csv, mentors.csv)."""

from pathlib import Path
from typing import Any, Optional

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

# Resolve paths: Backend/services -> Backend -> UniAid
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _BACKEND_ROOT.parent / "Dataset"  # Dataset/ (mentors_dataset, mentees_dataset, interactions_dataset)
_ML_DIR = _BACKEND_ROOT / "ML"
_MODELS_DIR = _ML_DIR / "models"

# Known universities (for matching from request_text or user profile)
_KNOWN_UNIVERSITIES = (
    "Monash University", "University of Melbourne", "University of Sydney", "University of Queensland",
    "University of Western Australia", "University of Adelaide", "Australian National University",
    "Queensland University of Technology", "Deakin University", "University of Technology Sydney",
    "RMIT University", "University of New South Wales", "Macquarie University", "Swinburne University",
    "La Trobe University", "University of Wollongong", "Griffith University", "Curtin University",
    "University of Newcastle", "Flinders University", "James Cook University", "University of Tasmania",
)

_recommender_instance: Optional[Any] = None


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


def _get_ml_recommender():
    """Lazy-load the ML MentorRecommender (uses Dataset/ and ML/models)."""
    global _recommender_instance
    if _recommender_instance is not None:
        return _recommender_instance
    import sys
    if str(_ML_DIR) not in sys.path:
        sys.path.insert(0, str(_ML_DIR))
    from recommender import MentorRecommender, RecommenderPaths
    paths = RecommenderPaths(
        data_dir=_DATA_DIR,
        models_dir=_MODELS_DIR,
        mentors_csv_name="mentors_dataset.csv",
        users_csv_name="mentees_dataset.csv",
        interactions_csv_name="interactions_dataset.csv",
    )
    _recommender_instance = MentorRecommender(paths=paths, model_name="all-MiniLM-L6-v2")
    return _recommender_instance


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
        # Recompute final_score so requirement match has weight
        item["final_score"] = w_similarity * sim + w_quality * qual + w_requirement * req_score

    results.sort(key=lambda x: (float(x.get("final_score") or 0), float(x.get("similarity") or 0)), reverse=True)
    return results


def _ml_result_to_recommendation_item(flat: dict[str, Any]) -> dict[str, Any]:
    """Convert flat ML/CSV result to nested shape (mentor + scores)."""
    mentor_data = {
        "mentor_id": flat.get("mentor_id"),
        "first_name": flat.get("first_name"),
        "last_name": flat.get("last_name"),
        "mentor_type": flat.get("mentor_type"),
        "university": flat.get("university"),
        "field_of_study": flat.get("field_of_study"),
        "degree_level": flat.get("degree_level"),
        "years_in_country": flat.get("years_in_country"),
        "visa_experience": flat.get("visa_experience"),
        "housing_experience": flat.get("housing_experience"),
        "cultural_adaptation_experience": flat.get("cultural_adaptation_experience"),
        "career_guidance_experience": flat.get("career_guidance_experience"),
        "languages_spoken": flat.get("languages_spoken"),
        "bio": flat.get("bio"),
        "availability_hours_per_week": flat.get("availability_hours_per_week"),
        "sessions_completed": flat.get("sessions_completed"),
        "response_time_hours": flat.get("response_time_hours"),
        "graduation_year": flat.get("graduation_year"),
        "mentor_rating": flat.get("mentor_rating"),
        "mentoring_topics": flat.get("mentoring_topics"),
    }
    return {
        "mentor": mentor_data,
        "similarity": flat.get("similarity"),
        "quality_score": flat.get("quality_score"),
        "final_score": flat.get("final_score"),
        "interaction_count": flat.get("interaction_count"),
        "success_rate": flat.get("success_rate"),
    }


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

    # If request_text mentions a university (e.g. "Monash University"), filter mentors to that university
    # and run the recommendation model on the filtered list only.
    university_filter = _extract_university(user_profile, req_text)

    rec = _get_ml_recommender()
    try:
        ml_results = rec.recommend(
            user_id=user_id if not req_text else None,
            user_profile=user_profile,
            request_text=req_text or None,
            top_k=top_k,
            candidate_pool=80,
            w_similarity=0.85,
            w_quality=0.15,
            candidate_university=university_filter,
        )
    except Exception:
        ml_results = []
    # When user asked for a specific university, do not fall back to unfiltered results.

    # Return mentors from DB when possible; use ML only for ranking, then fetch full mentor from DB.
    if db_session is not None and ml_results:
        from models.mentor_model import Mentor

        ordered_mentor_ids = [r.get("mentor_id") for r in ml_results if r.get("mentor_id") is not None]
        scores_by_id = {
            r["mentor_id"]: {
                "similarity": r.get("similarity"),
                "quality_score": r.get("quality_score"),
                "final_score": r.get("final_score"),
                "interaction_count": r.get("interaction_count"),
                "success_rate": r.get("success_rate"),
            }
            for r in ml_results
            if r.get("mentor_id") is not None
        }
        db_mentors = (
            db_session.query(Mentor)
            .filter(Mentor.id.in_(ordered_mentor_ids))
            .all()
        )
        # When university was requested, only include mentors from that university (DB may differ from ML data).
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
        # If no ML mentor_ids exist in DB (e.g. DB empty or different seed), return ML results
        # so the API still returns recommendations; once DB is seeded from same source as ML, we return DB.
        if not results:
            results = [_ml_result_to_recommendation_item(r) for r in ml_results]
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

    results = [_ml_result_to_recommendation_item(r) for r in ml_results]
    results = _rerank_by_requirements(results, req_text)
    results = _filter_results_by_university(results, university_filter)
    return results, profile_used


def evaluate(sample_size: Optional[int] = 200, top_k: int = 5, seed: int = 42) -> dict[str, Any]:
    """Run offline evaluation; returns hit_rate_at_k, mrr, n_eval, top_k."""
    rec = _get_ml_recommender()
    return rec.evaluate(sample_size=sample_size, top_k=top_k, seed=seed)
