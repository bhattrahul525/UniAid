from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from recommender import MentorRecommender, RecommenderPaths


APP_DIR = Path(__file__).resolve().parent   # UniAid/Backend/ML
DATA_DIR = APP_DIR.parent.parent / "Data"  # UniAid/Data
MODELS_DIR = APP_DIR / "models"            # UniAid/Backend/ML/models

recommender = MentorRecommender(
    paths=RecommenderPaths(data_dir=DATA_DIR, models_dir=MODELS_DIR),
    model_name="all-MiniLM-L6-v2",
)

app = FastAPI(title="UniAid Mentor Recommendations")


class RecommendRequest(BaseModel):
    user_id: Optional[int] = Field(default=None, description="If provided, load user profile from users.csv")
    request_text: Optional[str] = Field(default=None, description="Free-text request from user (recommended)")
    user_profile: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional profile fields (same shape as users.csv columns). Overrides user_id if provided.",
    )
    top_k: int = Field(default=5, ge=1, le=20)
    candidate_pool: int = Field(default=80, ge=10, le=500)
    w_similarity: float = Field(default=0.85, ge=0.0, le=1.0)
    w_quality: float = Field(default=0.15, ge=0.0, le=1.0)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend_mentors")
def recommend_mentors(payload: RecommendRequest) -> List[Dict[str, Any]]:
    """
    Returns a ranked list of mentors with similarity/final_score.
    Your frontend should render these as selectable mentor cards.
    """
    return recommender.recommend(
        user_id=payload.user_id,
        user_profile=payload.user_profile,
        request_text=payload.request_text,
        top_k=payload.top_k,
        candidate_pool=payload.candidate_pool,
        w_similarity=payload.w_similarity,
        w_quality=payload.w_quality,
    )

