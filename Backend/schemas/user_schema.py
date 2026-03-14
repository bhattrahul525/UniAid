"""Pydantic schemas for User and Mentee."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ----- User (login) -----


class UserSignup(BaseModel):
    """Schema for registration (POST /user/register): email, password; optional mentor_id or mentee_id."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    mentor_id: Optional[int] = Field(None, description="Set if this user is a mentor (FK to mentors)")
    mentee_id: Optional[int] = Field(None, description="Set if this user is a mentee")


class UserLogin(BaseModel):
    """Schema for login (POST /users/login): email, password."""

    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """User response for login and registration (first_name, last_name not required)."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    mentor_id: Optional[int] = None
    mentee_id: Optional[int] = None


class LoginResponse(BaseModel):
    """Response for POST /users/login: token (Bearer + JWT) and user."""

    token: str = Field(..., description="Bearer token, e.g. 'Bearer <access_token>'")
    user: UserResponse


class UserRead(BaseModel):
    """Schema for user in responses (login fields + optional mentee)."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    mentor_id: Optional[int] = None
    mentee_id: Optional[int] = None
    mentee: Optional["MenteeRead"] = None


# ----- Mentee (profile) -----


class MenteeBase(BaseModel):
    """Shared mentee fields."""

    user_type: Optional[str] = Field(None, description="e.g. student, parent")
    home_country: Optional[str] = None
    preferred_destination_country: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    budget_range: Optional[str] = None
    preferred_language: Optional[str] = None


class MenteeCreate(MenteeBase):
    """Schema for creating/updating mentee profile."""

    user_type: str = Field(..., description="e.g. student, parent")


class MenteeRead(MenteeBase):
    """Schema for mentee in responses."""

    model_config = ConfigDict(from_attributes=True)
    mentee_id: int


class UserCreate(MenteeCreate):
    """Schema for adding mentee profile to an existing user (POST /users/profile)."""

    user_id: int = Field(..., description="ID of the user to attach this profile to")


# Resolve forward ref for UserRead.mentee
UserRead.model_rebuild()
