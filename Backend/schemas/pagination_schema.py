"""Shared pagination and count schemas."""

from pydantic import BaseModel, Field


class EntityCounts(BaseModel):
    """Global counts across core entities."""

    total_users: int = Field(..., description="Total number of users")
    total_mentors: int = Field(..., description="Total number of mentors")
    total_mentees: int = Field(..., description="Total number of mentees")
    total_sessions: int = Field(..., description="Total number of sessions")


class PaginationMeta(BaseModel):
    """Standard pagination metadata."""

    page: int = Field(..., description="Current page index (0-based)")
    size: int = Field(..., description="Page size (items per page)")
    total_pages: int = Field(..., description="Total number of pages")
    total_items: int = Field(..., description="Total number of items for this query")

