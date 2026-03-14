"""Mentor API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.mentor_schema import MentorCreate, MentorRead
from services.mentor_service import MentorService

router = APIRouter(prefix="/mentors", tags=["mentors"])


@router.post("/register", response_model=MentorRead, status_code=status.HTTP_201_CREATED)
def register_mentor(payload: MentorCreate, db: Session = Depends(get_db)) -> MentorRead:
    """Register a new mentor (student, parent, or professor)."""
    mentor = MentorService.register(db, payload)
    return MentorService.to_read(mentor)


@router.get("", response_model=list[MentorRead])
def list_mentors(db: Session = Depends(get_db)) -> list[MentorRead]:
    """List all mentors."""
    mentors = MentorService.get_all(db)
    return [MentorService.to_read(m) for m in mentors]
