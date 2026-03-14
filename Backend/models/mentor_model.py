"""Mentor SQLAlchemy model – matches UniAid/Data/mentors.csv."""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Mentor(Base):
    """
    Mentor: current student, alumni, parent, or professor.
    Columns aligned with mentors.csv for seed/import.
    Users table links via users.mentor_id (FK to mentors.id) when a user is a mentor.
    """

    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    mentor_type = Column(String(50), nullable=False, index=True)  # student, parent, professor, etc.
    university = Column(String(200), nullable=True, index=True)
    field_of_study = Column(String(200), nullable=True, index=True)
    degree_level = Column(String(50), nullable=True)
    years_in_country = Column(Integer, nullable=True)
    visa_experience = Column(Integer, nullable=True, default=0)  # 0/1
    housing_experience = Column(Integer, nullable=True, default=0)  # 0/1
    cultural_adaptation_experience = Column(Integer, nullable=True, default=0)  # 0/1
    career_guidance_experience = Column(Integer, nullable=True, default=0)  # 0/1
    languages_spoken = Column(String(255), nullable=True)  # e.g. "English,French"
    availability_hours_per_week = Column(Integer, nullable=True)
    sessions_completed = Column(Integer, nullable=True, default=0)
    response_time_hours = Column(Integer, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    mentor_rating = Column(Float, nullable=True)

    users = relationship("User", back_populates="mentor", foreign_keys="User.mentor_id")
