"""User SQLAlchemy model – login/account fields."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    """
    User account: first_name, last_name, password.
    Optional mentor_id (FK to mentors) if user is a mentor; optional mentee_id if user is a mentee.
    Optional profile is in user_details (user_details_id).
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    mentor_id = Column(
        Integer,
        ForeignKey("mentors.mentor_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    mentee_id = Column(Integer, nullable=True, index=True)
    user_details_id = Column(
        Integer,
        ForeignKey("user_details.user_details_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    mentor = relationship("Mentor", back_populates="users", foreign_keys=[mentor_id])
    user_details = relationship("UserDetails", back_populates="user", uselist=False)
    interactions = relationship(
        "Interaction", back_populates="user", foreign_keys="Interaction.user_id"
    )
