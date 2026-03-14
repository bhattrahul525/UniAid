"""Recommendation API – by mentee_id or user_profile payload (users.csv / mentors.csv aligned)."""

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

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("", response_model=RecommendResponse)
def recommend_mentors(
    payload: RecommendRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> RecommendResponse:
    """
    Recommend mentors for a mentee.
    - **mentee_id**: load mentee from DB and build profile (users.csv shape) for the model.
    - **user_profile**: optional payload matching users.csv; use for testing without DB.
    - **request_text**: free-text request (e.g. "help with visa").
    Returns ranked mentors with similarity and quality scores.
    """
    if payload.mentee_id is None and payload.user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one of: mentee_id, user_profile",
        )
    user_profile_dict = None
    if payload.user_profile is not None:
        user_profile_dict = payload.user_profile.to_recommender_profile()
    try:
        mentors, profile_used = recommender_service.recommend(
            mentee_id=payload.mentee_id,
            user_profile=user_profile_dict or None,
            request_text=payload.request_text,
            top_k=payload.top_k,
            candidate_pool=payload.candidate_pool,
            w_similarity=payload.w_similarity,
            w_quality=payload.w_quality,
            db_session=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    items = [MentorRecommendationItem(**m) for m in mentors]
    return RecommendResponse(
        mentors=items,
        profile_used=profile_used,
        accuracy=None,
    )


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
