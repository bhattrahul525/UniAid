"""Session CRUD service."""

from sqlalchemy import case, func
from sqlalchemy.orm import Session, joinedload

from models.session_model import Session as SessionModel, SessionType
from models.user_model import User
from schemas.session_schema import SessionCreate, SessionRead, SessionUpdate


class SessionService:
    """Service for session CRUD operations (sessions are linked to users, not mentees)."""

    @staticmethod
    def _users_from_user_ids(db: Session, user_ids: list[int]) -> list[User]:
        """Resolve user_ids to User instances."""
        if not user_ids:
            return []
        return db.query(User).filter(User.user_id.in_(user_ids)).all()

    @staticmethod
    def create(db: Session, payload: SessionCreate) -> SessionModel:
        """Create a new session and optionally link users via user_ids."""
        session = SessionModel(
            title=payload.title,
            description=payload.description,
            mentor_id=payload.mentor_id,
            session_type=SessionType(payload.session_type.value),
            scheduled_at=payload.scheduled_at,
        )
        db.add(session)
        db.flush()
        if payload.user_ids:
            session.users = SessionService._users_from_user_ids(db, payload.user_ids)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_all(db: Session) -> list[SessionModel]:
        """Return all sessions with users and each user's mentee loaded.

        Sessions that are about to start (future scheduled_at) appear first, ordered by
        soonest start time; past sessions follow, ordered from most recent to oldest.
        """
        return (
            db.query(SessionModel)
            .filter(SessionModel.scheduled_at.isnot(None))
            .options(
                joinedload(SessionModel.users).joinedload(User.mentee),
            )
            .order_by(
                case(
                    (SessionModel.scheduled_at >= func.now(), 0),
                    else_=1,
                ),
                SessionModel.scheduled_at.asc(),
                SessionModel.id.asc(),
            )
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, session_id: int) -> SessionModel | None:
        """Return session by id with users and each user's mentee loaded, or None."""
        return (
            db.query(SessionModel)
            .options(
                joinedload(SessionModel.users).joinedload(User.mentee),
            )
            .filter(SessionModel.id == session_id)
            .first()
        )

    @staticmethod
    def update(db: Session, session_id: int, payload: SessionUpdate) -> SessionModel | None:
        """Update session by id; return updated session or None if not found."""
        session = SessionService.get_by_id(db, session_id)
        if not session:
            return None
        data = payload.model_dump(exclude_unset=True)
        user_ids = data.pop("user_ids", None)
        for key, value in data.items():
            if key == "session_type" and value is not None:
                setattr(session, key, SessionType(value.value))
            elif key not in ("user_ids",):
                setattr(session, key, value)
        if user_ids is not None:
            session.users = SessionService._users_from_user_ids(db, user_ids)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def delete(db: Session, session_id: int) -> bool:
        """Delete session by id. Return True if deleted, False if not found."""
        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if not session:
            return False
        db.delete(session)
        db.commit()
        return True

    @staticmethod
    def to_read(session: SessionModel, db: Session) -> SessionRead:
        """Map Session model to SessionRead; include mentor name and count of subscribed users."""
        mentor_user = db.query(User).filter(User.mentor_id == session.mentor_id).first()
        users_count = len(session.users or [])
        data = {
            "id": session.id,
            "title": session.title,
            "description": session.description,
            "mentor_id": session.mentor_id,
            "mentor_first_name": mentor_user.first_name if mentor_user else None,
            "mentor_last_name": mentor_user.last_name if mentor_user else None,
            "session_type": session.session_type,
            "scheduled_at": session.scheduled_at,
            "users_count": users_count,
        }
        return SessionRead.model_validate(data)
