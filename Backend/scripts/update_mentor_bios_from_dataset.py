"""
Update mentor bios in the database from Dataset/mentors_dataset.csv.

Uses mentor_id as the identifier (matches mentors.id).

Run from the Backend directory with venv activated:

    python scripts/update_mentor_bios_from_dataset.py [path/to/mentors_dataset.csv]

If no path is given, the default is ../Dataset/mentors_dataset.csv
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
from models.mentor_model import Mentor  # type: ignore  # noqa: E402


def update_bios(csv_path: Path) -> None:
    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)

    with csv_path.open("r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        if "mentor_id" not in reader.fieldnames or "bio" not in reader.fieldnames:
            print("Error: CSV must contain 'mentor_id' and 'bio' columns.")
            sys.exit(1)

        db = SessionLocal()
        updated = 0
        missing = 0
        try:
            for row in reader:
                raw_id = (row.get("mentor_id") or "").strip()
                bio = (row.get("bio") or "").strip()
                if not raw_id:
                    continue
                try:
                    mentor_id = int(raw_id)
                except ValueError:
                    print(f"Skipping row with invalid mentor_id: {raw_id!r}")
                    continue

                mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
                if not mentor:
                    missing += 1
                    continue

                mentor.bio = bio or None
                updated += 1

            db.commit()
        finally:
            db.close()

        print(f"Updated bios for {updated} mentor(s).")
        if missing:
            print(f"Warning: {missing} mentor_id value(s) from CSV not found in the database.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update mentor bios in the DB from mentors_dataset.csv"
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=None,
        help="Path to mentors_dataset.csv (default: Dataset/mentors_dataset.csv relative to Backend)",
    )
    args = parser.parse_args()

    if args.csv_path:
        csv_path = Path(args.csv_path)
    else:
        csv_path = _backend_root.parent / "Dataset" / "mentors_dataset.csv"

    update_bios(csv_path)


if __name__ == "__main__":
    main()

