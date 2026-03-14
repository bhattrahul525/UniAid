"""Mentor registration and listing service."""

from sqlalchemy.orm import Session

from models.mentor_model import Mentor
from schemas.mentor_schema import MentorCreate, MentorRead


class MentorService:
    """Service for mentor operations."""

    @staticmethod
    def register(db: Session, payload: MentorCreate) -> Mentor:
        """Create a new mentor and return the model instance."""
        mentor = Mentor(
            mentor_type=payload.mentor_type,
            university=payload.university,
            field_of_study=payload.field_of_study,
            country=payload.country,
            years_in_country=payload.years_in_country,
            languages_spoken=payload.languages_spoken,
            mentor_rating=payload.mentor_rating or 0.0,
            sessions_completed=payload.sessions_completed or 0,
        )
        db.add(mentor)
        db.commit()
        db.refresh(mentor)
        return mentor

    @staticmethod
    def get_all(db: Session) -> list[Mentor]:
        """Return all mentors."""
        return db.query(Mentor).all()

    @staticmethod
    def to_read(mentor: Mentor) -> MentorRead:
        """Map Mentor model to MentorRead schema."""
        return MentorRead.model_validate(mentor)
