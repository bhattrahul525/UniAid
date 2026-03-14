"""User API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user_schema import (
    UserCreate,
    UserRead,
    UserLogin,
    UserResponse,
    UserSignup,
    LoginResponse,
)
from services.user_service import UserService
from utils.jwt import create_access_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserSignup, db: Session = Depends(get_db)) -> UserResponse:
    """Register a new user. Rejects if email already exists."""
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
    """Login with email and password. Returns bearer token and user (no user_details)."""
    user = UserService.login(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    access_token = create_access_token(user_id=user.user_id, email=user.email)
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserService.to_response(user),
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserSignup, db: Session = Depends(get_db)) -> UserResponse:
    """Alias for POST /users/register: register a new user."""
    return register(payload, db)


@router.post("/profile", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_profile(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
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
