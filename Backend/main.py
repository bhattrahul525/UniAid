"""
UniAid FastAPI application.

Run: uvicorn main:app --reload --port 8000
"""
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from api.routes_mentees import router as mentees_router
from api.routes_mentors import router as mentors_router
from api.routes_recommendations import router as recommendations_router
from api.routes_sessions import router as sessions_router
from api.routes_users import router as users_router
from db.database import Base, check_db_connection, engine
from db.sync_schema import sync_schema
from models import Mentee, Mentor, Session, User  # noqa: F401 - register models with Base
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# App config
# -----------------------------------------------------------------------------

APP_TITLE = "UniAid API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "User accounts (mentors and mentees), authentication, and profile management."
)


# -----------------------------------------------------------------------------
# Lifespan
# -----------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and sync schema on startup; no teardown required."""
    try:
        Base.metadata.create_all(bind=engine)
        sync_schema(engine, Base.metadata)
    except Exception as exc:
        logger.warning(
            "Database unavailable at startup: %s. Set DATABASE_URL and ensure Postgres is running.",
            exc,
            exc_info=False,
        )
    yield


# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(mentors_router)
app.include_router(mentees_router)
app.include_router(recommendations_router)


# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Health & root
# -----------------------------------------------------------------------------


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    """API root; confirms the service is up."""
    return {"message": "UniAid API is running"}


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """Liveness check (no dependencies)."""
    return {"status": "ok"}


@app.get("/db-health", tags=["Health"])
def db_health() -> dict[str, Any]:
    """Readiness check; verifies database connectivity."""
    try:
        check_db_connection()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}
