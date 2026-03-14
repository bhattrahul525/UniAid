"""Recommendation API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.recommendation_schema import RecommendationResponse
from services.recommendation_service import get_recommendations

router = APIRouter(tags=["recommendation"])


@router.get("/recommend/{user_id}", response_model=RecommendationResponse)
def recommend_mentors(user_id: int, db: Session = Depends(get_db)) -> RecommendationResponse:
    """
    Get mentor recommendations for a user.
    Returns top 5 student mentors, top 2 parent mentors, top 1 professor mentor.
    """
    result = get_recommendations(db, user_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return result
