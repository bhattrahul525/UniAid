"""
Database session management.

Provides SessionLocal and get_db for dependency injection in FastAPI.
"""
from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from .database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session; ensure it is closed after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
