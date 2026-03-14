"""
Database engine and base configuration.

Uses DATABASE_URL from environment. Supports postgres:// and postgresql://
and normalises to postgresql+psycopg for SQLAlchemy.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

load_dotenv()
_raw_url = os.getenv("DATABASE_URL", "")
if not _raw_url:
    raise ValueError(
        "DATABASE_URL environment variable is required. "
        "See .env.example for the expected format."
    )
if _raw_url.startswith("postgres://"):
    _raw_url = _raw_url.replace("postgres://", "postgresql+psycopg://", 1)
elif _raw_url.startswith("postgresql://") and "+" not in _raw_url:
    _raw_url = _raw_url.replace("postgresql://", "postgresql+psycopg://", 1)

DATABASE_URL = _raw_url

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

Base = declarative_base()


def check_db_connection() -> bool:
    """Verify database connectivity with a simple query."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
