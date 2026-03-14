"""User SQLAlchemy model – login/account fields."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    """
    User account: email, password.
    Optional mentor_id (FK to mentors) if user is a mentor; optional mentee_id (FK to mentee) if user is a mentee.
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    mentor_id = Column(
        Integer,
        ForeignKey("mentors.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    mentee_id = Column(
        Integer,
        ForeignKey("mentee.mentee_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    mentor = relationship("Mentor", back_populates="users", foreign_keys=[mentor_id])
    mentee = relationship("Mentee", back_populates="user", uselist=False)
