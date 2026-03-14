"""Recommendation service – bridges Backend (mentee_id, DB) with ML recommender (users.csv, mentors.csv)."""

from pathlib import Path
from typing import Any, Optional

# Resolve paths: Backend/services -> Backend -> UniAid
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _BACKEND_ROOT.parent / "Data"
_ML_DIR = _BACKEND_ROOT / "ML"
_MODELS_DIR = _ML_DIR / "models"

_recommender_instance: Optional[Any] = None


def _get_ml_recommender():
    """Lazy-load the ML MentorRecommender (uses Data/ and ML/models)."""
    global _recommender_instance
    if _recommender_instance is not None:
        return _recommender_instance
    import sys
    if str(_ML_DIR) not in sys.path:
        sys.path.insert(0, str(_ML_DIR))
    from recommender import MentorRecommender, RecommenderPaths
    paths = RecommenderPaths(data_dir=_DATA_DIR, models_dir=_MODELS_DIR)
    _recommender_instance = MentorRecommender(paths=paths, model_name="all-MiniLM-L6-v2")
    return _recommender_instance


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
        "target_university": getattr(mentee, "preferred_destination_country", None),
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
    mentee_id: Optional[int] = None,
    user_profile: Optional[dict[str, Any]] = None,
    request_text: Optional[str] = None,
    top_k: int = 5,
    candidate_pool: int = 80,
    w_similarity: float = 0.85,
    w_quality: float = 0.15,
    db_session: Optional[Any] = None,
) -> tuple[list[dict[str, Any]], Optional[dict[str, Any]]]:
    """
    Get ranked mentor recommendations.
    Either pass mentee_id (and db_session to load mentee) or user_profile (users.csv shape).
    Returns (list of mentor dicts, profile_used for debugging).
    """
    profile_used: Optional[dict[str, Any]] = None
    if user_profile is not None:
        profile_used = user_profile
    elif mentee_id is not None and db_session is not None:
        from models.user_model import User
        from sqlalchemy.orm import joinedload
        user = (
            db_session.query(User)
            .options(joinedload(User.mentee))
            .filter(User.mentee_id == mentee_id)
            .first()
        )
        if user is None:
            raise ValueError(f"mentee_id {mentee_id} not found (no user with this mentee_id)")
        if user.mentee is None:
            raise ValueError(f"User for mentee_id {mentee_id} has no mentee profile")
        profile_used = mentee_to_user_profile(user.mentee, user)
        user_profile = profile_used

    rec = _get_ml_recommender()
    results = rec.recommend(
        user_id=None,
        user_profile=user_profile,
        request_text=request_text,
        top_k=top_k,
        candidate_pool=candidate_pool,
        w_similarity=w_similarity,
        w_quality=w_quality,
    )
    # Enrich results with mentor bios from the database (if a DB session is available).
    if db_session is not None and results:
        from models.mentor_model import Mentor

        mentor_ids = [r.get("mentor_id") for r in results if r.get("mentor_id") is not None]
        if mentor_ids:
            rows = (
                db_session.query(Mentor.id, Mentor.bio)
                .filter(Mentor.id.in_(mentor_ids))
                .all()
            )
            bio_by_id = {mid: bio for mid, bio in rows}
            for r in results:
                mid = r.get("mentor_id")
                if mid in bio_by_id:
                    r["bio"] = bio_by_id[mid]

    return results, profile_used


def evaluate(sample_size: Optional[int] = 200, top_k: int = 5, seed: int = 42) -> dict[str, Any]:
    """Run offline evaluation; returns hit_rate_at_k, mrr, n_eval, top_k."""
    rec = _get_ml_recommender()
    return rec.evaluate(sample_size=sample_size, top_k=top_k, seed=seed)
