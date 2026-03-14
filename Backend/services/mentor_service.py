"""Mentor CRUD service.

Mentors are referenced by users via users.mentor_id (FK). A user with mentor_id set
is the account for that mentor; use the users API to manage those accounts.
"""

import csv
import io
from typing import Any

from sqlalchemy.orm import Session

from models.mentor_model import Mentor
from schemas.mentor_schema import MentorCreate, MentorRead, MentorUpdate


def _optional_int(value: Any) -> int | None:
    if value is None or value == "" or (isinstance(value, str) and value.strip().upper() == "NULL"):
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def _optional_float(value: Any) -> float | None:
    if value is None or value == "" or (isinstance(value, str) and value.strip().upper() == "NULL"):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _optional_str(value: Any) -> str | None:
    if value is None or (isinstance(value, str) and value.strip().upper() == "NULL"):
        return None
    s = str(value).strip() if value else ""
    return s if s else None


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
            bio=payload.bio,
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

    @staticmethod
    def bulk_create_from_csv(db: Session, csv_content: str | bytes) -> tuple[int, list[str]]:
        """
        Parse CSV (mentors.csv format: id, first_name, last_name, ...) and create mentor records.
        Returns (created_count, list of error messages for failed rows).
        """
        if isinstance(csv_content, bytes):
            csv_content = csv_content.decode("utf-8", errors="replace")
        reader = csv.DictReader(io.StringIO(csv_content))
        created = 0
        errors: list[str] = []
        for row_num, row in enumerate(reader, start=2):
            try:
                first_name = (row.get("first_name") or "").strip()
                last_name = (row.get("last_name") or "").strip()
                mentor_type = (row.get("mentor_type") or "").strip()
                if not first_name or not last_name or not mentor_type:
                    errors.append(f"Row {row_num}: first_name, last_name and mentor_type are required")
                    continue
                payload = MentorCreate(
                    first_name=first_name,
                    last_name=last_name,
                    mentor_type=mentor_type,
                    university=_optional_str(row.get("university")),
                    field_of_study=_optional_str(row.get("field_of_study")),
                    degree_level=_optional_str(row.get("degree_level")),
                    years_in_country=_optional_int(row.get("years_in_country")),
                    visa_experience=_optional_int(row.get("visa_experience")),
                    housing_experience=_optional_int(row.get("housing_experience")),
                    cultural_adaptation_experience=_optional_int(row.get("cultural_adaptation_experience")),
                    career_guidance_experience=_optional_int(row.get("career_guidance_experience")),
                    languages_spoken=_optional_str(row.get("languages_spoken")),
                    bio=_optional_str(row.get("bio")),
                    availability_hours_per_week=_optional_int(row.get("availability_hours_per_week")),
                    sessions_completed=_optional_int(row.get("sessions_completed")),
                    response_time_hours=_optional_int(row.get("response_time_hours")),
                    graduation_year=_optional_int(row.get("graduation_year")),
                    mentor_rating=_optional_float(row.get("mentor_rating")),
                )
                MentorService.create(db, payload)
                created += 1
            except Exception as e:
                db.rollback()
                errors.append(f"Row {row_num}: {e}")
        return created, errors
