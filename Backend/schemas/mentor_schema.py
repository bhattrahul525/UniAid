"""Pydantic schemas for Mentor."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MentorBase(BaseModel):
    """Shared mentor fields."""

    mentor_type: str = Field(..., description="student | parent | professor")
    university: Optional[str] = None
    field_of_study: Optional[str] = None
    country: Optional[str] = None
    years_in_country: Optional[int] = None
    languages_spoken: Optional[str] = None  # comma-separated
    mentor_rating: Optional[float] = 0.0
    sessions_completed: Optional[int] = 0


class MentorCreate(MentorBase):
    """Schema for creating a mentor (POST /mentors/register)."""

    pass


class MentorRead(MentorBase):
    """Schema for mentor in responses."""

    model_config = ConfigDict(from_attributes=True)
    mentor_id: int
