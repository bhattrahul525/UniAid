"""Pydantic schemas for User and Mentee."""

from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

if TYPE_CHECKING:
    from schemas.mentor_schema import MentorCreate, MentorRead


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
    """User response for login and registration."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    email: str
    mentor_id: Optional[int] = None
    mentee_id: Optional[int] = None


class LoginResponse(BaseModel):
    """Response for POST /users/login: token (Bearer + JWT) and user."""

    token: str = Field(..., description="Bearer token, e.g. 'Bearer <access_token>'")
    user: UserResponse


class UserRead(BaseModel):
    """Schema for user in responses (login fields + optional mentor/mentee)."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    email: str
    mentor_id: Optional[int] = None
    mentee_id: Optional[int] = None
    mentor: Optional["MentorRead"] = None
    mentee: Optional["MenteeRead"] = None


# ----- Profile (unified mentor / mentee) -----


class ProfileType(str, Enum):
    """Whether the user profile is a mentor or mentee."""

    mentor = "mentor"
    mentee = "mentee"


class UserProfilePayload(BaseModel):
    """Unified payload for POST /user/profile: user_type (mentor|mentee) + respective data."""

    user_id: int = Field(..., description="ID of the user to attach this profile to")
    user_type: ProfileType = Field(..., description="Whether to create a mentor or mentee profile")
    mentor: Optional["MentorCreate"] = Field(None, description="Mentor data; required when user_type=mentor")
    mentee: Optional["MenteeProfileData"] = Field(None, description="Mentee data; required when user_type=mentee")

    @model_validator(mode="after")
    def require_profile_data_matches_user_type(self) -> "UserProfilePayload":
        if self.user_type == ProfileType.mentor:
            if self.mentor is None:
                raise ValueError("mentor data is required when user_type is mentor")
            if self.mentee is not None:
                raise ValueError("mentee must be null when user_type is mentor")
        else:
            if self.mentee is None:
                raise ValueError("mentee data is required when user_type is mentee")
            if self.mentor is not None:
                raise ValueError("mentor must be null when user_type is mentee")
        return self


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


class MenteeProfileData(MenteeBase):
    """Mentee data for unified profile payload (POST /user/profile when user_type=mentee)."""

    user_type: str = Field(..., description="e.g. student, parent")


class MenteeRead(MenteeBase):
    """Schema for mentee in responses."""

    model_config = ConfigDict(from_attributes=True)
    mentee_id: int


class MenteeUpdate(BaseModel):
    """Schema for partial update of mentee. All fields optional."""

    user_type: Optional[str] = None
    home_country: Optional[str] = None
    preferred_destination_country: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    budget_range: Optional[str] = None
    preferred_language: Optional[str] = None


# Resolve forward refs (MentorCreate, MentorRead used in UserRead / UserProfilePayload)
from schemas.mentor_schema import MentorCreate, MentorRead  # noqa: E402

UserRead.model_rebuild()
UserProfilePayload.model_rebuild()
