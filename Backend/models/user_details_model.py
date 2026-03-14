"""UserDetails SQLAlchemy model – profile/preferences for a user."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class UserDetails(Base):
    """
    Profile and preference details for a user (linked from users.user_details_id).
    """

    __tablename__ = "user_details"

    user_details_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_type = Column(String(50), nullable=True, index=True)  # e.g. student, parent
    home_country = Column(String(100), nullable=True)
    preferred_destination_country = Column(String(100), nullable=True, index=True)
    field_of_study = Column(String(200), nullable=True, index=True)
    degree_level = Column(String(50), nullable=True)
    budget_range = Column(String(50), nullable=True)
    preferred_language = Column(String(50), nullable=True, index=True)

    user = relationship("User", back_populates="user_details", uselist=False)
