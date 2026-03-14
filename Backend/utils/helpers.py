"""Shared helper functions."""

from typing import Any


def safe_str(value: Any) -> str:
    """Return string representation; empty string for None."""
    if value is None:
        return ""
    return str(value).strip()
