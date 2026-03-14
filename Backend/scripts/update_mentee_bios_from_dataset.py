"""
Update mentee bios in the database from Dataset/mentees_dataset.csv.

Uses user_id as the identifier:
- Looks up User.user_id matching the CSV user_id
- If the user has an attached mentee (user.mentee), updates mentee.bio

Run from the Backend directory with venv activated:

    python scripts/update_mentee_bios_from_dataset.py [path/to/mentees_dataset.csv]

If no path is given, the default is ../Dataset/mentees_dataset.csv
relative to the Backend directory.
"""

import argparse
import csv
import sys
from pathlib import Path

# Ensure we can import from the Backend package when run as a script
_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from db.session import SessionLocal  # type: ignore  # noqa: E402
from models.user_model import User  # type: ignore  # noqa: E402


def update_bios(csv_path: Path) -> None:
    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)

    with csv_path.open("r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        if "user_id" not in reader.fieldnames or "bio" not in reader.fieldnames:
            print("Error: CSV must contain 'user_id' and 'bio' columns.")
            sys.exit(1)

        db = SessionLocal()
        updated = 0
        missing_user = 0
        missing_mentee = 0
        try:
            for row in reader:
                raw_id = (row.get("user_id") or "").strip()
                bio = (row.get("bio") or "").strip()
                if not raw_id:
                    continue
                try:
                    user_id = int(raw_id)
                except ValueError:
                    print(f"Skipping row with invalid user_id: {raw_id!r}")
                    continue

                user = db.query(User).filter(User.user_id == user_id).first()
                if not user:
                    missing_user += 1
                    continue
                if not user.mentee:
                    missing_mentee += 1
                    continue

                user.mentee.bio = bio or None
                updated += 1

            db.commit()
        finally:
            db.close()

        print(f"Updated bios for {updated} mentee(s).")
        if missing_user:
            print(f"Warning: {missing_user} user_id value(s) from CSV not found in the database.")
        if missing_mentee:
            print(f"Warning: {missing_mentee} user(s) had no attached mentee profile.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update mentee bios in the DB from mentees_dataset.csv"
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=None,
        help="Path to mentees_dataset.csv (default: Dataset/mentees_dataset.csv relative to Backend)",
    )
    args = parser.parse_args()

    if args.csv_path:
        csv_path = Path(args.csv_path)
    else:
        csv_path = _backend_root.parent / "Dataset" / "mentees_dataset.csv"

    update_bios(csv_path)


if __name__ == "__main__":
    main()

