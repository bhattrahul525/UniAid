"""Pydantic schemas for Session."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .user_schema import MenteeRead


class SessionTypeEnum(str, Enum):
    """Session visibility (enum: public or private)."""

    public = "public"
    private = "private"


class UserInSessionRead(BaseModel):
    """User in session response: user fields plus nested mentee data."""

    model_config = ConfigDict(from_attributes=True)
    user_id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mentee: Optional[MenteeRead] = None


class SessionBase(BaseModel):
    """Shared session fields."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    mentor_id: int = Field(..., description="FK to mentors.id")
    session_type: SessionTypeEnum = Field(
        default=SessionTypeEnum.public,
        description="Enum: public | private",
    )
    scheduled_at: datetime = Field(..., description="Date and time of the session (ISO 8601)")


class SessionCreate(SessionBase):
    """Schema for creating a session. Optionally pass user IDs to link users to the session."""

    user_ids: list[int] = Field(default_factory=list, description="List of user_id to link to the session")


class SessionUserAdd(BaseModel):
    """Payload for linking a user to a session (row in session_users)."""

    session_id: int = Field(..., description="Session ID to link the user to")
    user_id: int = Field(..., description="User ID to link to the session")


class SessionUpdate(BaseModel):
    """Schema for partial update. All fields optional."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    mentor_id: Optional[int] = None
    session_type: Optional[SessionTypeEnum] = None
    scheduled_at: Optional[datetime] = Field(None, description="Date and time of the session (ISO 8601)")
    user_ids: Optional[list[int]] = Field(None, description="Replace session's users with these user IDs")


class SessionRead(BaseModel):
    """Schema for session in responses (includes list of users with nested mentee, and mentor name from user table)."""

    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    mentor_id: int
    mentor_first_name: Optional[str] = Field(None, description="From user table (user linked to this mentor)")
    mentor_last_name: Optional[str] = Field(None, description="From user table (user linked to this mentor)")
    session_type: SessionTypeEnum
    scheduled_at: Optional[datetime] = Field(None, description="Date and time of the session (ISO 8601)")
    users: list[UserInSessionRead] = Field(default_factory=list)

    @field_validator("session_type", mode="before")
    @classmethod
    def coerce_session_type(cls, v: Any) -> SessionTypeEnum:
        """Accept ORM enum or string."""
        if isinstance(v, SessionTypeEnum):
            return v
        if hasattr(v, "value"):
            return SessionTypeEnum(v.value)
        return SessionTypeEnum(v)
