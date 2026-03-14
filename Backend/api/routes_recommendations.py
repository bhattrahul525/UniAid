"""Recommendation API – request_text and/or user_id; response: mentor + final_score as percentage."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.session import get_db
from schemas.recommendation_schema import (
    EvaluateResponse,
    MentorRecommendationItem,
    RecommendRequest,
    RecommendResponse,
)
from services import recommender_service

router = APIRouter(prefix="/mentors/recommendations", tags=["recommendations"])


@router.post("", response_model=RecommendResponse)
def recommend_mentors(
    payload: RecommendRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> RecommendResponse:
    """
    Recommend mentors. Both given → use only request_text. Only request_text → rank by text.
    Only user_id → rank by user's mentee profile. Returns mentors with final_score as percentage (2 decimals).
    """
    try:
        mentors, _ = recommender_service.recommend(
            user_id=payload.user_id,
            request_text=(payload.request_text or "").strip(),
            top_k=payload.top_k,
            db_session=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    items = [
        MentorRecommendationItem(
            mentor=m["mentor"],
            final_score=round((m.get("final_score") or 0) * 100, 2),
        )
        for m in mentors
    ]
    return RecommendResponse(mentors=items)


@router.get("/evaluate", response_model=EvaluateResponse)
def get_accuracy(
    sample_size: int = 200,
    top_k: int = 5,
    seed: int = 42,
    current_user=Depends(get_current_user),
) -> EvaluateResponse:
    """
    Run offline evaluation on interactions (users.csv + mentors.csv).
    For a sample of (user_id, mentor_id) pairs, checks if the actual mentor
    appears in the top_k recommendations. Returns hit_rate_at_k and MRR.
    Use for testing accuracy.
    """
    try:
        metrics = recommender_service.evaluate(
            sample_size=sample_size,
            top_k=top_k,
            seed=seed,
        )
        return EvaluateResponse(**metrics)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {e}",
        ) from e
