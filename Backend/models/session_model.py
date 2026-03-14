"""Session SQLAlchemy model – mentor sessions linked to users (not mentees)."""

import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db.database import Base


class SessionType(str, enum.Enum):
    """Session visibility."""

    public = "public"
    private = "private"


# Association table: session <-> user (many-to-many)
session_users = Table(
    "session_users",
    Base.metadata,
    Column("session_id", Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
)


class Session(Base):
    """
    Session: title, description, mentor, type (public/private), and list of users.
    """

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(2000), nullable=True)
    mentor_id = Column(
        Integer,
        ForeignKey("mentors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_type = Column(
        Enum(SessionType, name="session_type_enum", create_constraint=True, native_enum=True),
        nullable=False,
        default=SessionType.public,
        index=True,
    )

    mentor = relationship("Mentor", back_populates="sessions", foreign_keys=[mentor_id])
    users = relationship(
        "User",
        secondary=session_users,
        back_populates="sessions",
    )
