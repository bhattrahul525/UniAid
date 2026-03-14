"""User SQLAlchemy model – login/account fields."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    """
    User account (login): email, password.
    Optional mentee profile is linked via mentee_id.
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    mentee_id = Column(
        Integer,
        ForeignKey("mentee.mentee_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    mentee = relationship("Mentee", back_populates="user", uselist=False)
