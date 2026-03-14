"""Mentee API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.session import get_db
from models.mentee_model import Mentee
from models.mentor_model import Mentor
from models.session_model import Session as SessionModel
from models.user_model import User
from schemas.pagination_schema import EntityCounts, PaginationMeta
from schemas.user_schema import MenteeBase, MenteeListResponse, MenteeRead, MenteeUpdate
from services.mentee_service import MenteeService

router = APIRouter(prefix="/mentees", tags=["mentees"])


@router.post("", response_model=MenteeRead, status_code=status.HTTP_201_CREATED)
def create_mentee(
    payload: MenteeBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MenteeRead:
    """Create a new mentee (user_type, home_country, university, field_of_study, degree_level, budget_range, preferred_language)."""
    mentee = MenteeService.create(db, payload)
    return MenteeService.to_read(mentee)


@router.get("", response_model=MenteeListResponse)
def list_mentees(
    page: int = Query(0, ge=0, description="Page index (0-based)"),
    size: int = Query(10, gt=0, le=100, description="Page size (items per page)"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MenteeListResponse:
    """List mentees with pagination and global counts."""
    base_query = db.query(Mentee)
    total_items = base_query.count()
    mentees = (
        base_query.order_by(Mentee.mentee_id)
        .offset(page * size)
        .limit(size)
        .all()
    )
    items = [MenteeService.to_read(m) for m in mentees]

    # Global counts
    total_users = db.query(User).count()
    total_mentors = db.query(Mentor).count()
    total_mentees = total_items
    total_sessions = db.query(SessionModel).count()

    pagination = PaginationMeta(
        page=page,
        size=size,
        total_items=total_items,
        total_pages=(total_items + size - 1) // size if total_items else 0,
    )
    counts = EntityCounts(
        total_users=total_users,
        total_mentors=total_mentors,
        total_mentees=total_mentees,
        total_sessions=total_sessions,
    )
    return MenteeListResponse(items=items, pagination=pagination, counts=counts)


@router.get("/{mentee_id}", response_model=MenteeRead)
def get_mentee(
    mentee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MenteeRead:
    """Get a mentee by ID."""
    mentee = MenteeService.get_by_id(db, mentee_id)
    if not mentee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentee not found",
        )
    return MenteeService.to_read(mentee)


@router.put("/{mentee_id}", response_model=MenteeRead)
def update_mentee(
    mentee_id: int,
    payload: MenteeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MenteeRead:
    """Update a mentee by ID (partial update)."""
    mentee = MenteeService.update(db, mentee_id, payload)
    if not mentee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentee not found",
        )
    return MenteeService.to_read(mentee)


@router.delete("/{mentee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentee(
    mentee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> None:
    """Delete a mentee by ID. User accounts with mentee_id set to this mentee are not deleted (mentee_id may be set to NULL by DB)."""
    if not MenteeService.delete(db, mentee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentee not found",
        )
