"""Mentee SQLAlchemy model – profile/preferences for a user."""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from db.database import Base


class Mentee(Base):
    """
    Mentee profile (linked from users.mentee_id).
    """

    __tablename__ = "mentee"

    mentee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_type = Column(String(50), nullable=True, index=True)  # e.g. student, parent
    home_country = Column(String(100), nullable=True)
    university = Column(String(100), nullable=True, index=True)
    field_of_study = Column(String(200), nullable=True, index=True)
    degree_level = Column(String(50), nullable=True)
    budget_range = Column(String(50), nullable=True)
    preferred_language = Column(String(50), nullable=True, index=True)
    bio = Column(Text, nullable=True)  # short mentee bio / description (optional)

    user = relationship("User", back_populates="mentee", uselist=False)
