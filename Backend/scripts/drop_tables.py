"""
Drop all UniAid tables so the app can recreate them on next startup.

Run from Backend dir with venv activated:
  python scripts/drop_tables.py
Then restart: uvicorn main:app --reload --port 8000
"""
import sys

# Run from Backend so imports work
sys.path.insert(0, ".")

from sqlalchemy import text

from db.database import engine

# Same order as reset_tables.sql (users first due to FKs)
TABLES = ["users", "mentee", "mentors"]


def main() -> None:
    with engine.connect() as conn:
        for table in TABLES:
            conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
        conn.commit()
    print("Dropped tables:", ", ".join(TABLES))
    print("Restart the server so tables are recreated.")


if __name__ == "__main__":
    main()
