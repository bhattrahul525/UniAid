"""Interaction SQLAlchemy model (user–mentor sessions)."""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.database import Base


class Interaction(Base):
    """
    Record of a session between a user and a mentor.
    """

    __tablename__ = "interactions"

    interaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.mentor_id"), nullable=False, index=True)
    session_duration = Column(Integer, nullable=True)  # minutes
    rating_given = Column(Float, nullable=True)
    match_success = Column(Boolean, nullable=True)

    user = relationship("User", back_populates="interactions")
    mentor = relationship("Mentor", back_populates="interactions")
