"""
Recommendation engine: compatibility score and ranking.

Uses similarity on field_of_study, destination country, language,
and mentor experience (years, sessions, rating).
"""
from typing import Any


def _normalize(s: str | None) -> str:
    """Normalize string for comparison (lowercase, strip)."""
    if s is None or not isinstance(s, str):
        return ""
    return s.lower().strip()


def _match_field(a: str | None, b: str | None) -> float:
    """Return 1.0 if both set and equal (after normalize), else 0.0."""
    if not a or not b:
        return 0.0
    return 1.0 if _normalize(a) == _normalize(b) else 0.0


def _match_language(preferred: str | None, mentor_languages: str | None) -> float:
    """Return 1.0 if preferred language is in mentor's list (comma-separated)."""
    if not preferred or not mentor_languages:
        return 0.0
    pref = _normalize(preferred)
    langs = [x.strip().lower() for x in mentor_languages.split(",") if x.strip()]
    return 1.0 if pref in langs else 0.0


def _experience_score(years_in_country: int | None, sessions: int | None, rating: float | None) -> float:
    """Return a score in [0, 1] from mentor experience (years, sessions, rating)."""
    score = 0.0
    if years_in_country is not None:
        score += min(1.0, years_in_country / 10.0) * 0.4  # cap at 10 years
    if sessions is not None:
        score += min(1.0, sessions / 50.0) * 0.3  # cap at 50 sessions
    if rating is not None and isinstance(rating, (int, float)):
        score += min(1.0, max(0.0, rating / 5.0)) * 0.3  # assume 5-point scale
    return min(1.0, score)


def compute_compatibility_score(
    user: dict[str, Any],
    mentor: dict[str, Any],
) -> float:
    """
    Compute compatibility score between a user and a mentor in [0, 1].

    Factors:
    - field_of_study match
    - destination country (user preferred_destination_country vs mentor country)
    - preferred_language in mentor languages_spoken
    - mentor experience (years_in_country, sessions_completed, mentor_rating)
    """
    field_score = _match_field(
        user.get("field_of_study"),
        mentor.get("field_of_study"),
    )
    country_score = _match_field(
        user.get("preferred_destination_country"),
        mentor.get("country"),
    )
    lang_score = _match_language(
        user.get("preferred_language"),
        mentor.get("languages_spoken"),
    )
    exp_score = _experience_score(
        mentor.get("years_in_country"),
        mentor.get("sessions_completed"),
        mentor.get("mentor_rating"),
    )
    # Weights: field and country matter most, then language, then experience
    total = (
        field_score * 0.35
        + country_score * 0.30
        + lang_score * 0.20
        + exp_score * 0.15
    )
    return round(min(1.0, max(0.0, total)), 4)


def rank_mentors_for_user(
    user: dict[str, Any],
    mentors: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], float]]:
    """
    Rank mentors by compatibility score (descending).
    Returns list of (mentor_dict, score).
    """
    scored = [
        (m, compute_compatibility_score(user, m))
        for m in mentors
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
