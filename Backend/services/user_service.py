"""User registration and retrieval service."""

from typing import Optional

from sqlalchemy.orm import Session, joinedload

from models.user_details_model import UserDetails
from models.user_model import User
from schemas.user_schema import UserCreate, UserRead, UserSignup
from utils.password import hash_password


class UserService:
    """Service for user operations."""

    @staticmethod
    def signup(db: Session, payload: UserSignup) -> User:
        """Create a new user (login only: first_name, last_name, email, password)."""
        if UserService.get_by_email(db, payload.email) is not None:
            raise ValueError("A user with this email already exists")
        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def register(db: Session, payload: UserCreate) -> User:
        """Create user details for an existing user and link via user_details_id."""
        user = UserService.get_by_id(db, payload.user_id)
        if not user:
            raise ValueError("User not found")
        if user.user_details_id is not None:
            raise ValueError("User already has profile details")
        details = UserDetails(
            user_type=payload.user_type,
            home_country=payload.home_country,
            preferred_destination_country=payload.preferred_destination_country,
            field_of_study=payload.field_of_study,
            degree_level=payload.degree_level,
            budget_range=payload.budget_range,
            preferred_language=payload.preferred_language,
        )
        db.add(details)
        db.flush()  # get details.user_details_id
        user.user_details_id = details.user_details_id
        db.commit()
        db.refresh(user)
        db.refresh(details)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Return user by user_id or None."""
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_id_with_details(db: Session, user_id: int) -> Optional[User]:
        """Return user by user_id with user_details eager-loaded, or None."""
        return (
            db.query(User)
            .options(joinedload(User.user_details))
            .filter(User.user_id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Return user by email or None."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def to_read(user: User) -> UserRead:
        """Map User model to UserRead schema (includes user_details if loaded)."""
        return UserRead.model_validate(user)
