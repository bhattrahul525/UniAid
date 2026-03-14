"""JWT access token creation and validation."""

import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


def create_access_token(
    *,
    user_id: int,
    email: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT bearer token for the given user."""
    now = datetime.now(UTC)
    expire = now + (expires_delta or timedelta(minutes=JWT_EXPIRE_MINUTES))
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT; return payload or None if invalid."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
