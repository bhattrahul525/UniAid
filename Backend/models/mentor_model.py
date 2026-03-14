"""Mentor SQLAlchemy model."""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Mentor(Base):
    """
    Mentor (student, parent, or professor) offering guidance.
    mentor_type: 'student' | 'parent' | 'professor'
    """

    __tablename__ = "mentors"

    mentor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mentor_type = Column(String(50), nullable=False, index=True)  # student | parent | professor
    university = Column(String(200), nullable=True)
    field_of_study = Column(String(200), nullable=True, index=True)
    country = Column(String(100), nullable=True, index=True)  # country where mentor is based
    years_in_country = Column(Integer, nullable=True)
    languages_spoken = Column(String(500), nullable=True)  # comma-separated
    mentor_rating = Column(Float, nullable=True, default=0.0)
    sessions_completed = Column(Integer, nullable=True, default=0)

    interactions = relationship("Interaction", back_populates="mentor", foreign_keys="Interaction.mentor_id")
