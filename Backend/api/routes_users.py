"""User API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user_schema import UserCreate, UserRead, UserSignup
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserSignup, db: Session = Depends(get_db)) -> UserRead:
    """Sign up a new user (first_name, last_name, email, password)."""
    try:
        user = UserService.signup(db, payload)
        return UserService.to_read(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """Add profile (user_details) to an existing user. Body must include user_id."""
    try:
        user = UserService.register(db, payload)
        user = UserService.get_by_id_with_details(db, user.user_id)
        return UserService.to_read(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    """Get a user by ID (includes user_details if set)."""
    user = UserService.get_by_id_with_details(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserService.to_read(user)
