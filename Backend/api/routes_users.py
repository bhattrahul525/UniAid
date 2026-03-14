"""User API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.session import get_db
from schemas.user_schema import (
    UserProfilePayload,
    UserRead,
    UserLogin,
    UserResponse,
    UserSignup,
    LoginResponse,
)
from services.user_service import UserService
from utils.jwt import create_access_token

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserSignup, db: Session = Depends(get_db)) -> UserResponse:
    """Register a new user (email, password). Rejects if email already exists."""
    try:
        user = UserService.signup(db, payload)
        return UserService.to_response(user)
    except ValueError as e:
        if "already exists" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            ) from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> LoginResponse:
    """Login existing user. Returns bearer token and user."""
    user = UserService.login(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    access_token = create_access_token(user_id=user.user_id, email=user.email)
    return LoginResponse(
        token=f"Bearer {access_token}",
        user=UserService.to_response(user),
    )


@router.post("/profile", response_model=UserRead)
def add_profile(
    payload: UserProfilePayload,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> UserRead:
    """Create or update profile by user_id: for both mentor and mentee, creates if none else updates (upsert)."""
    try:
        user = UserService.add_profile(db, payload)
        user = UserService.get_by_id_with_details(db, user.user_id)
        return UserService.to_read(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> UserRead:
    """Get a user by ID (includes mentor or mentee profile if set)."""
    user = UserService.get_by_id_with_details(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserService.to_read(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> None:
    """Delete the given user. Only the same user can delete their own account."""
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account.",
        )
    if not UserService.delete(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
