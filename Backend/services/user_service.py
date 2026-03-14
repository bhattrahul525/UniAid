"""User registration and retrieval service."""

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from models.mentee_model import Mentee
from models.user_model import User
from schemas.user_schema import UserCreate, UserRead, UserSignup
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
    def register(db: Session, payload: UserCreate) -> User:
        """Create mentee profile for an existing user and link via mentee_id."""
        user = UserService.get_by_id(db, payload.user_id)
        if not user:
            raise ValueError("User not found")
        if user.mentee_id is not None:
            raise ValueError("User already has a mentee profile")
        mentee = Mentee(
            user_type=payload.user_type,
            home_country=payload.home_country,
            preferred_destination_country=payload.preferred_destination_country,
            field_of_study=payload.field_of_study,
            degree_level=payload.degree_level,
            budget_range=payload.budget_range,
            preferred_language=payload.preferred_language,
        )
        db.add(mentee)
        db.flush()
        user.mentee_id = mentee.mentee_id
        db.commit()
        db.refresh(user)
        db.refresh(mentee)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Return user by user_id or None."""
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_id_with_details(db: Session, user_id: int) -> Optional[User]:
        """Return user by user_id with mentee eager-loaded, or None."""
        return (
            db.query(User)
            .options(joinedload(User.mentee))
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
