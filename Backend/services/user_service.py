"""User registration and retrieval service."""

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from models.mentee_model import Mentee
from models.mentor_model import Mentor
from models.user_model import User
from schemas.user_schema import ProfileType, UserProfilePayload, UserRead, UserSignup
from schemas.mentor_schema import MentorCreate
from services.mentor_service import MentorService
from utils.password import hash_password, verify_password


class UserService:
    """Service for user operations."""

    @staticmethod
    def signup(db: Session, payload: UserSignup) -> User:
        """Create a new user: email, password; optional mentor_id or mentee_id."""
        if UserService.get_by_email(db, payload.email) is not None:
            raise ValueError("A user with this email already exists")
        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            mentor_id=payload.mentor_id,
            mentee_id=payload.mentee_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def add_profile(db: Session, payload: UserProfilePayload) -> User:
        """Create mentor or mentee profile for an existing user based on user_type; link via mentor_id or mentee_id."""
        user = UserService.get_by_id(db, payload.user_id)
        if not user:
            raise ValueError("User not found")
        if payload.user_type == ProfileType.mentor:
            # Mentor: create if user has no mentor_id, else update existing (upsert by user_id)
            if user.mentor_id is None:
                mentor = MentorService.create(db, payload.mentor)
                user.mentor_id = mentor.id
                db.commit()
                db.refresh(user)
            else:
                mentor = db.query(Mentor).filter(Mentor.id == user.mentor_id).first()
                if mentor:
                    m = payload.mentor
                    mentor.first_name = m.first_name
                    mentor.last_name = m.last_name
                    mentor.mentor_type = m.mentor_type
                    mentor.university = m.university
                    mentor.field_of_study = m.field_of_study
                    mentor.degree_level = m.degree_level
                    mentor.years_in_country = m.years_in_country
                    mentor.visa_experience = m.visa_experience
                    mentor.housing_experience = m.housing_experience
                    mentor.cultural_adaptation_experience = m.cultural_adaptation_experience
                    mentor.career_guidance_experience = m.career_guidance_experience
                    mentor.languages_spoken = m.languages_spoken
                    mentor.availability_hours_per_week = m.availability_hours_per_week
                    mentor.sessions_completed = m.sessions_completed if m.sessions_completed is not None else 0
                    mentor.response_time_hours = m.response_time_hours
                    mentor.graduation_year = m.graduation_year
                    mentor.mentor_rating = m.mentor_rating
                db.commit()
                db.refresh(user)
        else:
            # Mentee: create if user has no mentee_id, else update existing (upsert by user_id)
            if user.mentee_id is None:
                mentee = Mentee(
                    user_type=payload.mentee.user_type,
                    home_country=payload.mentee.home_country,
                    preferred_destination_country=payload.mentee.preferred_destination_country,
                    field_of_study=payload.mentee.field_of_study,
                    degree_level=payload.mentee.degree_level,
                    budget_range=payload.mentee.budget_range,
                    preferred_language=payload.mentee.preferred_language,
                )
                db.add(mentee)
                db.flush()
                user.mentee_id = mentee.mentee_id
            else:
                mentee = db.query(Mentee).filter(Mentee.mentee_id == user.mentee_id).first()
                if mentee:
                    mentee.user_type = payload.mentee.user_type
                    mentee.home_country = payload.mentee.home_country
                    mentee.preferred_destination_country = payload.mentee.preferred_destination_country
                    mentee.field_of_study = payload.mentee.field_of_study
                    mentee.degree_level = payload.mentee.degree_level
                    mentee.budget_range = payload.mentee.budget_range
                    mentee.preferred_language = payload.mentee.preferred_language
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Return user by user_id or None."""
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_id_with_details(db: Session, user_id: int) -> Optional[User]:
        """Return user by user_id with mentor and mentee eager-loaded, or None."""
        return (
            db.query(User)
            .options(joinedload(User.mentor), joinedload(User.mentee))
            .filter(User.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Return user by email or None."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def to_read(user: User) -> UserRead:
        """Map User model to UserRead schema (includes mentee if loaded)."""
        return UserRead.model_validate(user)

    @staticmethod
    def to_response(user: User) -> "UserResponse":
        """Map User to UserResponse."""
        from schemas.user_schema import UserResponse
        return UserResponse.model_validate(user)

    @staticmethod
    def login(db: Session, email: str, password: str) -> Optional[User]:
        """Verify email/password and return user if valid, else None."""
        user = UserService.get_by_email(db, email)
        if user is None:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
