"""Schemas for recommendation API – payload aligned with users.csv and mentor output."""

from typing import Any, Optional

from pydantic import BaseModel, Field


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
    """Request: recommend by mentee_id (DB) and/or user_profile (users.csv shape) for testing."""
    mentee_id: Optional[int] = Field(None, description="If set, load mentee from DB and build profile")
    user_profile: Optional[UserProfilePayload] = Field(
        None,
        description="Optional profile (users.csv shape). Overrides mentee_id profile if provided.",
    )
    request_text: Optional[str] = Field(None, description="Free-text request from user")
    top_k: int = Field(default=5, ge=1, le=20)
    candidate_pool: int = Field(default=80, ge=10, le=500)
    w_similarity: float = Field(default=0.85, ge=0.0, le=1.0)
    w_quality: float = Field(default=0.15, ge=0.0, le=1.0)


class MentorRecommendationItem(BaseModel):
    """One recommended mentor with scores (matches recommender output)."""
    mentor_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mentor_type: Optional[str] = None
    university: Optional[str] = None
    field_of_study: Optional[str] = None
    degree_level: Optional[str] = None
    mentoring_topics: Optional[str] = None
    languages_spoken: Optional[str] = None
    availability_hours_per_week: Optional[int] = None
    sessions_completed: Optional[int] = None
    response_time_hours: Optional[int] = None
    bio: Optional[str] = None
    mentor_rating: Optional[float] = None
    similarity: Optional[float] = None
    quality_score: Optional[float] = None
    final_score: Optional[float] = None
    interaction_count: Optional[int] = None
    success_rate: Optional[float] = None


class RecommendResponse(BaseModel):
    """Response: ranked mentors and (when available) evaluation metrics."""
    mentors: list[MentorRecommendationItem] = Field(..., description="Ranked list of recommended mentors")
    profile_used: Optional[dict[str, Any]] = Field(None, description="Profile sent to model (for debugging)")
    accuracy: Optional[dict[str, Any]] = Field(None, description="Optional eval metrics if requested")


class EvaluateResponse(BaseModel):
    """Response for GET /recommendations/evaluate – accuracy metrics."""
    hit_rate_at_k: float = Field(..., description="Fraction of (user, mentor) pairs where mentor in top_k")
    mrr: float = Field(..., description="Mean reciprocal rank")
    n_eval: int = Field(..., description="Number of pairs evaluated")
    top_k: int = Field(..., description="top_k used")
