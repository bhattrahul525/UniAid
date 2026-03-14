"""Mentor CRUD service.

Mentors are referenced by users via users.mentor_id (FK). A user with mentor_id set
is the account for that mentor; use the users API to manage those accounts.
"""

from sqlalchemy.orm import Session

from models.mentor_model import Mentor
from schemas.mentor_schema import MentorCreate, MentorRead, MentorUpdate


class MentorService:
    """Service for mentor CRUD operations."""

    @staticmethod
    def create(db: Session, payload: MentorCreate) -> Mentor:
        """Create a new mentor and return the model instance."""
        mentor = Mentor(
            first_name=payload.first_name,
            last_name=payload.last_name,
            mentor_type=payload.mentor_type,
            university=payload.university,
            field_of_study=payload.field_of_study,
            degree_level=payload.degree_level,
            years_in_country=payload.years_in_country,
            visa_experience=payload.visa_experience,
            housing_experience=payload.housing_experience,
            cultural_adaptation_experience=payload.cultural_adaptation_experience,
            career_guidance_experience=payload.career_guidance_experience,
            languages_spoken=payload.languages_spoken,
            availability_hours_per_week=payload.availability_hours_per_week,
            sessions_completed=payload.sessions_completed or 0,
            response_time_hours=payload.response_time_hours,
            graduation_year=payload.graduation_year,
            mentor_rating=payload.mentor_rating,
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
    def get_by_id(db: Session, mentor_id: int) -> Mentor | None:
        """Return mentor by id or None."""
        return db.query(Mentor).filter(Mentor.id == mentor_id).first()

    @staticmethod
    def update(db: Session, mentor_id: int, payload: MentorUpdate) -> Mentor | None:
        """Update mentor by id; return updated mentor or None if not found."""
        mentor = MentorService.get_by_id(db, mentor_id)
        if not mentor:
            return None
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(mentor, key, value)
        db.commit()
        db.refresh(mentor)
        return mentor

    @staticmethod
    def delete(db: Session, mentor_id: int) -> bool:
        """Delete mentor by id. Return True if deleted, False if not found."""
        mentor = MentorService.get_by_id(db, mentor_id)
        if not mentor:
            return False
        db.delete(mentor)
        db.commit()
        return True

    @staticmethod
    def to_read(mentor: Mentor) -> MentorRead:
        """Map Mentor model to MentorRead schema."""
        return MentorRead.model_validate(mentor)
