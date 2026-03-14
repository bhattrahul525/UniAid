"""
Sync SQLAlchemy model schema to the database on startup.

Adds any new columns that exist in the models but not in the database.
Does not drop columns or change types (safe for development).
"""
import logging

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

logger = logging.getLogger("uvicorn.error")


def _get_column_sql(engine: Engine, column) -> str:
    """Build ADD COLUMN clause for a SQLAlchemy column (PostgreSQL)."""
    type_str = column.type.compile(engine.dialect)
    parts = [f'ADD COLUMN "{column.name}"', type_str]
    # Only add NOT NULL if column is non-nullable (may fail if table has rows and no default)
    if not column.nullable and column.server_default is None:
        parts.append("NOT NULL")
    return " ".join(parts)


def sync_schema(engine: Engine, metadata) -> None:
    """
    Add any missing columns to existing tables.
    Tables are created by create_all; this only alters existing tables.
    """
    inspector = inspect(engine)
    for table_name, table in metadata.tables.items():
        if not inspector.has_table(table_name):
            continue
        existing = {c["name"] for c in inspector.get_columns(table_name)}
        for column in table.c:
            if column.name in existing:
                continue
            try:
                add_sql = f'ALTER TABLE "{table_name}" {_get_column_sql(engine, column)}'
                with engine.connect() as conn:
                    conn.execute(text(add_sql))
                    conn.commit()
                logger.info("Added column %s.%s", table_name, column.name)
            except Exception as e:
                logger.warning("Could not add column %s.%s: %s", table_name, column.name, e)
