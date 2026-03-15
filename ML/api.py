from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from recommender import MentorRecommender, RecommenderPaths


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "Dataset"
MODELS_DIR = APP_DIR / "models"

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


class RecommendForBackendRequest(BaseModel):
    """Minimal payload for Backend: request_text and/or user_profile, top_k, candidate_university."""
    request_text: Optional[str] = Field(default=None)
    user_profile: Optional[Dict[str, Any]] = Field(default=None)
    top_k: int = Field(default=5, ge=1, le=20)
    candidate_university: Optional[str] = Field(default=None)


class MentorScoreItem(BaseModel):
    mentor_id: int
    final_score: float


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=List[MentorScoreItem])
def recommend_for_backend(payload: RecommendForBackendRequest) -> List[Dict[str, Any]]:
    """
    Used by the Backend: returns only mentor_id and final_score (0-1).
    Backend enriches mentor data from DB. At least one of request_text or user_profile required.
    """
    if not (payload.request_text or payload.user_profile) or (
        payload.request_text and not payload.request_text.strip()
    ):
        return []
    raw = recommender.recommend(
        user_id=None,
        user_profile=payload.user_profile,
        request_text=(payload.request_text or "").strip() or None,
        top_k=payload.top_k,
        candidate_pool=80,
        w_similarity=0.85,
        w_quality=0.15,
        candidate_university=payload.candidate_university,
    )
    return [
        {"mentor_id": int(r["mentor_id"]), "final_score": float(r.get("final_score", 0.0))}
        for r in raw
        if r.get("mentor_id") is not None
    ]


@app.get("/evaluate")
def evaluate_for_backend(
    sample_size: int = Query(default=200, ge=1, le=2000),
    top_k: int = Query(default=5, ge=1, le=20),
    seed: int = Query(default=42),
) -> Dict[str, Any]:
    """Used by the Backend: offline evaluation metrics (hit_rate_at_k, mrr, n_eval, top_k)."""
    return recommender.evaluate(sample_size=sample_size, top_k=top_k, seed=seed)


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
