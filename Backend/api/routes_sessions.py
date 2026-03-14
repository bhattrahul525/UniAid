"""Session API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from models.mentor_model import Mentor
from schemas.session_schema import SessionCreate, SessionRead, SessionUpdate
from services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _require_mentor_exists(db: Session, mentor_id: int) -> None:
    """Raise 404 if mentor_id is not in the mentors table."""
    if db.query(Mentor).filter(Mentor.id == mentor_id).first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mentor with id {mentor_id} not found. Create a mentor first (e.g. POST /mentors or bulk-upload).",
        )


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)) -> SessionRead:
    """Create a new session (title, description, mentor_id, session_type, scheduled_at, optional user_ids)."""
    _require_mentor_exists(db, payload.mentor_id)
    session = SessionService.create(db, payload)
    return SessionService.to_read(session, db)


@router.get("", response_model=list[SessionRead])
def list_sessions(db: Session = Depends(get_db)) -> list[SessionRead]:
    """List all sessions with their users (each user includes nested mentee data)."""
    sessions = SessionService.get_all(db)
    return [SessionService.to_read(s, db) for s in sessions]


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db)) -> SessionRead:
    """Get a session by ID."""
    session = SessionService.get_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return SessionService.to_read(session, db)


@router.put("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: int,
    payload: SessionUpdate,
    db: Session = Depends(get_db),
) -> SessionRead:
    """Update a session by ID (partial update; can set scheduled_at)."""
    if payload.mentor_id is not None:
        _require_mentor_exists(db, payload.mentor_id)
    session = SessionService.update(db, session_id, payload)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return SessionService.to_read(session, db)


@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
def delete_session(session_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """Delete a session by ID."""
    if not SessionService.delete(db, session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return {"message": "Session deleted"}
