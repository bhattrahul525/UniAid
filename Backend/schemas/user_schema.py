"""Pydantic schemas for User and UserDetails."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ----- User (login) -----


class UserSignup(BaseModel):
    """Schema for registration (POST /users/register): name, email, password."""

    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for login (POST /users/login): email, password."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """User response for login and registration (no user_details)."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    first_name: str
    last_name: str
    email: str


class LoginResponse(BaseModel):
    """Response for POST /users/login: bearer token + user."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserRead(BaseModel):
    """Schema for user in responses (login fields + optional user_details)."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    first_name: str
    last_name: str
    email: str
    user_details_id: Optional[int] = None
    user_details: Optional["UserDetailsRead"] = None


# ----- UserDetails (profile) -----


class UserDetailsBase(BaseModel):
    """Shared user details fields."""

    user_type: Optional[str] = Field(None, description="e.g. student, parent")
    home_country: Optional[str] = None
    preferred_destination_country: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    budget_range: Optional[str] = None
    preferred_language: Optional[str] = None


class UserDetailsCreate(UserDetailsBase):
    """Schema for creating/updating user details (profile)."""

    user_type: str = Field(..., description="e.g. student, parent")


class UserDetailsRead(UserDetailsBase):
    """Schema for user details in responses."""

    model_config = ConfigDict(from_attributes=True)
    user_details_id: int


# For POST /users/register: add profile to an existing user (body has user_id + profile)
class UserCreate(UserDetailsCreate):
    """Schema for registering profile for an existing user (POST /users/register)."""

    user_id: int = Field(..., description="ID of the user to attach this profile to")


# Resolve forward ref for UserRead.user_details
UserRead.model_rebuild()
