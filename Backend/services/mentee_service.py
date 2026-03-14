"""Mentee CRUD service.

Mentees are referenced by users via users.mentee_id (FK). A user with mentee_id set
is the account for that mentee; use the users API to manage those accounts.
"""

from typing import Optional

from sqlalchemy.orm import Session

from models.mentee_model import Mentee
from schemas.user_schema import MenteeBase, MenteeRead, MenteeUpdate


class MenteeService:
    """Service for mentee CRUD operations."""

    @staticmethod
    def create(db: Session, payload: MenteeBase) -> Mentee:
        """Create a new mentee and return the model instance."""
        mentee = Mentee(
            user_type=payload.user_type,
            home_country=payload.home_country,
            preferred_destination_country=payload.preferred_destination_country,
            field_of_study=payload.field_of_study,
            degree_level=payload.degree_level,
            budget_range=payload.budget_range,
            preferred_language=payload.preferred_language,
            bio=payload.bio,
        )
        db.add(mentee)
        db.commit()
        db.refresh(mentee)
        return mentee

    @staticmethod
    def get_all(db: Session) -> list[Mentee]:
        """Return all mentees."""
        return db.query(Mentee).all()

    @staticmethod
    def get_by_id(db: Session, mentee_id: int) -> Optional[Mentee]:
        """Return mentee by mentee_id or None."""
        return db.query(Mentee).filter(Mentee.mentee_id == mentee_id).first()

    @staticmethod
    def update(db: Session, mentee_id: int, payload: MenteeUpdate) -> Optional[Mentee]:
        """Update mentee by id; return updated mentee or None if not found."""
        mentee = MenteeService.get_by_id(db, mentee_id)
        if not mentee:
            return None
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(mentee, key, value)
        db.commit()
        db.refresh(mentee)
        return mentee

    @staticmethod
    def delete(db: Session, mentee_id: int) -> bool:
        """Delete mentee by id. Return True if deleted, False if not found."""
        mentee = MenteeService.get_by_id(db, mentee_id)
        if not mentee:
            return False
        db.delete(mentee)
        db.commit()
        return True

    @staticmethod
    def to_read(mentee: Mentee) -> MenteeRead:
        """Map Mentee model to MenteeRead schema."""
        return MenteeRead.model_validate(mentee)
