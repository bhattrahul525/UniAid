"""
Model loader and data preparation for the recommendation engine.

For a rule-based compatibility score there is no serialized model to load.
This module can be extended to load a trained model (e.g. sklearn, PyTorch)
or feature weights from disk.
"""
from typing import Any


def mentor_to_dict(mentor: Any) -> dict[str, Any]:
    """
    Convert a Mentor ORM instance to a dict for the recommendation model.
    """
    return {
        "mentor_id": getattr(mentor, "mentor_id", mentor.get("mentor_id")),
        "mentor_type": getattr(mentor, "mentor_type", mentor.get("mentor_type", "")).lower(),
        "university": getattr(mentor, "university", mentor.get("university")),
        "field_of_study": getattr(mentor, "field_of_study", mentor.get("field_of_study")),
        "country": getattr(mentor, "country", mentor.get("country")),
        "years_in_country": getattr(mentor, "years_in_country", mentor.get("years_in_country")),
        "languages_spoken": getattr(mentor, "languages_spoken", mentor.get("languages_spoken")),
        "mentor_rating": getattr(mentor, "mentor_rating", mentor.get("mentor_rating")),
        "sessions_completed": getattr(mentor, "sessions_completed", mentor.get("sessions_completed")),
    }


def user_to_dict(user: Any) -> dict[str, Any]:
    """Convert a User ORM instance to a dict for the recommendation model.
    Profile fields come from user.user_details if present.
    """
    details = getattr(user, "user_details", None) or (user.get("user_details") if isinstance(user, dict) else None)
    if details is None:
        return {
            "user_type": None,
            "home_country": None,
            "preferred_destination_country": None,
            "field_of_study": None,
            "degree_level": None,
            "budget_range": None,
            "preferred_language": None,
        }
    return {
        "user_type": getattr(details, "user_type", details.get("user_type") if isinstance(details, dict) else None),
        "home_country": getattr(details, "home_country", details.get("home_country") if isinstance(details, dict) else None),
        "preferred_destination_country": getattr(
            details, "preferred_destination_country", details.get("preferred_destination_country") if isinstance(details, dict) else None
        ),
        "field_of_study": getattr(details, "field_of_study", details.get("field_of_study") if isinstance(details, dict) else None),
        "degree_level": getattr(details, "degree_level", details.get("degree_level") if isinstance(details, dict) else None),
        "budget_range": getattr(details, "budget_range", details.get("budget_range") if isinstance(details, dict) else None),
        "preferred_language": getattr(details, "preferred_language", details.get("preferred_language") if isinstance(details, dict) else None),
    }


def load_mentors_for_recommendation(mentors: list[Any]) -> list[dict[str, Any]]:
    """Convert a list of Mentor ORM objects to list of dicts for scoring."""
    return [mentor_to_dict(m) for m in mentors]
