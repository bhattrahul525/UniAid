"""Mentor API routes."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from db.session import get_db
from schemas.mentor_schema import MentorBulkUploadResponse, MentorCreate, MentorRead, MentorUpdate
from services.mentor_service import MentorService

router = APIRouter(prefix="/mentors", tags=["mentors"])


@router.post("/register", response_model=MentorRead, status_code=status.HTTP_201_CREATED)
def register_mentor(
    payload: MentorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MentorRead:
    """Register a new mentor (student, parent, or professor)."""
    mentor = MentorService.create(db, payload)
    return MentorService.to_read(mentor)


@router.post("", response_model=MentorRead, status_code=status.HTTP_201_CREATED)
def create_mentor(
    payload: MentorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MentorRead:
    """Alias for POST /mentors/register: create a new mentor."""
    return register_mentor(payload, db)


@router.post("/bulk-upload", response_model=MentorBulkUploadResponse)
def bulk_upload_mentors(
    file: UploadFile = File(..., description="CSV file (e.g. mentors.csv with header: id, first_name, last_name, ...)"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MentorBulkUploadResponse:
    """Upload a CSV of mentors. CSV must match mentors.csv format."""
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV (.csv)",
        )
    content = file.file.read()
    created, errors = MentorService.bulk_create_from_csv(db, content)
    return MentorBulkUploadResponse(created=created, errors=errors)


@router.get("", response_model=list[MentorRead])
def list_mentors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[MentorRead]:
    """List all mentors."""
    mentors = MentorService.get_all(db)
    return [MentorService.to_read(m) for m in mentors]


@router.get("/{mentor_id}", response_model=MentorRead)
def get_mentor(
    mentor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MentorRead:
    """Get a mentor by ID."""
    mentor = MentorService.get_by_id(db, mentor_id)
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor not found",
        )
    return MentorService.to_read(mentor)


@router.put("/{mentor_id}", response_model=MentorRead)
def update_mentor(
    mentor_id: int,
    payload: MentorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> MentorRead:
    """Update a mentor by ID (partial update)."""
    mentor = MentorService.update(db, mentor_id, payload)
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor not found",
        )
    return MentorService.to_read(mentor)


@router.delete("/{mentor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mentor(
    mentor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> None:
    """Delete a mentor by ID. User accounts with mentor_id set to this mentor are not deleted (mentor_id may be set to NULL by DB)."""
    if not MentorService.delete(db, mentor_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor not found",
        )
