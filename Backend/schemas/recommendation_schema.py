"""Schemas for recommendation API – payload aligned with users.csv and mentor output."""

from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator, field_validator


# ----- User profile payload (users.csv shape) for testing -----

class UserProfilePayload(BaseModel):
    """Optional profile fields matching users.csv columns. Used for recommendation by payload."""
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[str] = Field(None, description="e.g. student, parent")
    home_country: Optional[str] = None
    preferred_city_type: Optional[str] = None
    target_university: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    intended_start_year: Optional[int] = None
    budget_range_aud: Optional[str] = None
    scholarship_interest: Optional[int] = Field(None, ge=0, le=1)
    concern_visa: Optional[int] = Field(None, ge=0, le=1)
    concern_accommodation: Optional[int] = Field(None, ge=0, le=1)
    concern_safety: Optional[int] = Field(None, ge=0, le=1)
    concern_academics: Optional[int] = Field(None, ge=0, le=1)
    concern_career: Optional[int] = Field(None, ge=0, le=1)
    concern_culture: Optional[int] = Field(None, ge=0, le=1)
    preferred_language: Optional[str] = None
    accommodation_type: Optional[str] = None
    work_while_studying_interest: Optional[int] = Field(None, ge=0, le=1)

    def to_recommender_profile(self) -> dict[str, Any]:
        """Convert to dict for ML recommender (drop None so recommender uses defaults)."""
        return self.model_dump(exclude_none=True)


# ----- Request/Response -----

class RecommendRequest(BaseModel):
    """
    Request: recommend mentors. Provide at least one of request_text or user_id.
    - Both given: use only request_text (user profile ignored).
    - Only request_text: rank by free-text.
    - Only user_id: rank by user's mentee profile from DB.
    """
    request_text: Optional[str] = Field(None, description="Free-text request (e.g. mentor from Monash University)")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of mentors to return")
    user_id: Optional[int] = Field(None, description="User ID; used only when request_text is not provided")

    @model_validator(mode="after")
    def require_request_text_or_user_id(self) -> "RecommendRequest":
        has_text = self.request_text is not None and str(self.request_text).strip() != ""
        has_user = self.user_id is not None
        if not has_text and not has_user:
            raise ValueError("Provide at least one of: request_text, user_id")
        return self


class MentorData(BaseModel):
    """Full mentor profile (nested in recommendation response)."""
    mentor_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mentor_type: Optional[str] = None
    university: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    years_in_country: Optional[int] = None
    visa_experience: Optional[int] = None
    housing_experience: Optional[int] = None
    cultural_adaptation_experience: Optional[int] = None
    career_guidance_experience: Optional[int] = None
    languages_spoken: Optional[str] = None
    bio: Optional[str] = None
    availability_hours_per_week: Optional[int] = None
    sessions_completed: Optional[int] = None
    response_time_hours: Optional[int] = None
    graduation_year: Optional[int] = None
    mentor_rating: Optional[float] = None
    mentoring_topics: Optional[str] = None

    model_config = {"extra": "ignore"}


class MentorRecommendationItem(BaseModel):
    """One recommendation: mentor data and match score as percentage only."""
    mentor: MentorData = Field(..., description="Full mentor profile")
    final_score: float = Field(..., description="Match score as percentage (0–100), 2 decimal places")

    @field_validator("final_score", mode="before")
    @classmethod
    def round_final_score(cls, v: float) -> float:
        """Ensure final_score is always a float with exactly 2 decimal places."""
        return round(float(v), 2)


class RecommendResponse(BaseModel):
    """Response: ranked list of recommended mentors with match percentage."""
    mentors: list[MentorRecommendationItem] = Field(..., description="Ranked list of recommended mentors")


class EvaluateResponse(BaseModel):
    """Response for GET /recommendations/evaluate – accuracy metrics."""
    hit_rate_at_k: float = Field(..., description="Fraction of (user, mentor) pairs where mentor in top_k")
    mrr: float = Field(..., description="Mean reciprocal rank")
    n_eval: int = Field(..., description="Number of pairs evaluated")
    top_k: int = Field(..., description="top_k used")
