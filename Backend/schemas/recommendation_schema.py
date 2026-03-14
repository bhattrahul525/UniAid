"""Pydantic schemas for recommendation API."""

from pydantic import BaseModel, Field


class RecommendedMentor(BaseModel):
    """A single recommended mentor with compatibility score."""

    mentor_id: int
    mentor_type: str
    compatibility_score: float = Field(..., ge=0, le=1, description="Score between 0 and 1")
    university: str | None = None
    field_of_study: str | None = None
    country: str | None = None
    mentor_rating: float | None = None
    sessions_completed: int | None = None


class RecommendationResponse(BaseModel):
    """Response for GET /recommend/{user_id}: 5 students, 2 parents, 1 professor."""

    student_mentors: list[RecommendedMentor] = Field(
        ..., description="Top 5 student mentors"
    )
    parent_mentors: list[RecommendedMentor] = Field(
        ..., description="Top 2 parent mentors"
    )
    professor_mentors: list[RecommendedMentor] = Field(
        ..., description="Top 1 professor mentor"
    )
