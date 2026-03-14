"""Interaction SQLAlchemy model – links users and mentors (sessions)."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Interaction(Base):
    """Session/interaction between a user and a mentor."""

    __tablename__ = "interactions"

    interaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False, index=True)
    interaction_type = Column(String(50), nullable=True)  # e.g. chat, video_call
    session_duration_minutes = Column(Integer, nullable=True)
    rating_given_by_user = Column(Integer, nullable=True)
    helpfulness_score = Column(Integer, nullable=True)
    match_success = Column(Integer, nullable=True)  # 0/1

    user = relationship("User", back_populates="interactions", foreign_keys=[user_id])
