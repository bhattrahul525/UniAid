"""
Drop first_name and last_name from users table (one-off after removing them from the app).

Run from Backend dir with venv activated:
  python scripts/drop_user_name_columns.py
"""
import sys

sys.path.insert(0, ".")

from sqlalchemy import text

from db.database import engine


def main() -> None:
    with engine.connect() as conn:
        for col in ("first_name", "last_name"):
            conn.execute(text(f'ALTER TABLE users DROP COLUMN IF EXISTS "{col}"'))
        conn.commit()
    print("Dropped users.first_name and users.last_name if present.")


if __name__ == "__main__":
    main()
