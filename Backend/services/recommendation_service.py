"""Recommendation service: returns top mentors per type (5 students, 2 parents, 1 professor)."""

from sqlalchemy.orm import Session

from ml.model_loader import load_mentors_for_recommendation, user_to_dict
from ml.recommendation_model import rank_mentors_for_user
from models.mentor_model import Mentor
from schemas.recommendation_schema import RecommendationResponse, RecommendedMentor
from services.mentor_service import MentorService
from services.user_service import UserService


# Fixed ratio: 5 student, 2 parent, 1 professor
NUM_STUDENT = 5
NUM_PARENT = 2
NUM_PROFESSOR = 1


def _mentor_dict_to_read(d: dict, score: float) -> RecommendedMentor:
    """Build RecommendedMentor from mentor dict and compatibility score."""
    return RecommendedMentor(
        mentor_id=d["mentor_id"],
        mentor_type=d["mentor_type"],
        compatibility_score=score,
        university=d.get("university"),
        field_of_study=d.get("field_of_study"),
        country=d.get("country"),
        mentor_rating=d.get("mentor_rating"),
        sessions_completed=d.get("sessions_completed"),
    )


def get_recommendations(db: Session, user_id: int) -> RecommendationResponse | None:
    """
    Load user and mentors, score and rank, return top 5 students, 2 parents, 1 professor.
    Returns None if user not found.
    """
    user = UserService.get_by_id_with_details(db, user_id)
    if not user:
        return None

    mentors = MentorService.get_all(db)
    if not mentors:
        return RecommendationResponse(
            student_mentors=[],
            parent_mentors=[],
            professor_mentors=[],
        )

    user_dict = user_to_dict(user)
    mentor_dicts = load_mentors_for_recommendation(mentors)
    ranked = rank_mentors_for_user(user_dict, mentor_dicts)

    students: list[RecommendedMentor] = []
    parents: list[RecommendedMentor] = []
    professors: list[RecommendedMentor] = []

    for m_dict, score in ranked:
        m_type = (m_dict.get("mentor_type") or "").lower()
        rec = _mentor_dict_to_read(m_dict, score)
        if m_type == "student" and len(students) < NUM_STUDENT:
            students.append(rec)
        elif m_type == "parent" and len(parents) < NUM_PARENT:
            parents.append(rec)
        elif m_type == "professor" and len(professors) < NUM_PROFESSOR:
            professors.append(rec)
        if len(students) >= NUM_STUDENT and len(parents) >= NUM_PARENT and len(professors) >= NUM_PROFESSOR:
            break

    return RecommendationResponse(
        student_mentors=students,
        parent_mentors=parents,
        professor_mentors=professors,
    )
