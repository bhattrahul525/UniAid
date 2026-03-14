"""Pydantic schemas for Mentor – aligned with mentors.csv.

Users table links to mentors via users.mentor_id (FK to mentors.mentor_id)
when a user account is for a mentor; users.mentee_id is set when the user is a mentee.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MentorBase(BaseModel):
    """Shared mentor fields (create/update)."""

    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    mentor_type: str = Field(..., description="e.g. student, parent, professor")
    university: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    years_in_country: Optional[int] = None
    visa_experience: Optional[int] = Field(None, ge=0, le=1)
    housing_experience: Optional[int] = Field(None, ge=0, le=1)
    cultural_adaptation_experience: Optional[int] = Field(None, ge=0, le=1)
    career_guidance_experience: Optional[int] = Field(None, ge=0, le=1)
    languages_spoken: Optional[str] = None
    availability_hours_per_week: Optional[int] = None
    sessions_completed: Optional[int] = Field(None, ge=0)
    response_time_hours: Optional[int] = None
    graduation_year: Optional[int] = None
    mentor_rating: Optional[float] = None


class MentorCreate(MentorBase):
    """Schema for creating a mentor (POST)."""

    pass


class MentorUpdate(BaseModel):
    """Schema for partial update (PUT/PATCH). All fields optional."""

    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    mentor_type: Optional[str] = None
    university: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    years_in_country: Optional[int] = None
    visa_experience: Optional[int] = Field(None, ge=0, le=1)
    housing_experience: Optional[int] = Field(None, ge=0, le=1)
    cultural_adaptation_experience: Optional[int] = Field(None, ge=0, le=1)
    career_guidance_experience: Optional[int] = Field(None, ge=0, le=1)
    languages_spoken: Optional[str] = None
    availability_hours_per_week: Optional[int] = None
    sessions_completed: Optional[int] = Field(None, ge=0)
    response_time_hours: Optional[int] = None
    graduation_year: Optional[int] = None
    mentor_rating: Optional[float] = None


class MentorRead(MentorBase):
    """Schema for mentor in responses. Primary key is `id` (matches mentors table and mentors.csv)."""

    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Primary key of the mentors table")


class MentorBulkUploadResponse(BaseModel):
    """Response for POST /mentors/bulk-upload."""

    created: int = Field(..., description="Number of mentors created")
    errors: list[str] = Field(default_factory=list, description="Error messages for failed rows")
