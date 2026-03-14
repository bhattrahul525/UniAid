"""
UniAid FastAPI application.

Run with: uvicorn main:app --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes_mentors import router as mentors_router
from api.routes_recommendations import router as recommendations_router
from api.routes_users import router as users_router
from db.database import Base, check_db_connection, engine
from db.sync_schema import sync_schema
from models import Mentee, User  # noqa: F401 - register models with Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup, then sync new columns from models to DB."""
    import logging
    log = logging.getLogger("uvicorn.error")
    try:
        Base.metadata.create_all(bind=engine)
        sync_schema(engine, Base.metadata)
    except Exception as e:
        log.warning(
            "Database not available at startup: %s. Set DATABASE_URL in .env and ensure Postgres is running.",
            e,
        )
    yield
    # shutdown: nothing to do


app = FastAPI(
    title="UniAid API",
    description="UniAid API – user registration, login, and mentee profile.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(users_router)
app.include_router(mentors_router)
app.include_router(recommendations_router)


@app.get("/")
def root() -> dict[str, str]:
    """Health check."""
    return {"message": "UniAid API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    """Basic health check."""
    return {"status": "ok"}


@app.get("/db-health")
def db_health() -> dict[str, str]:
    """Check database connectivity."""
    try:
        check_db_connection()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
