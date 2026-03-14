"""
Bulk upload mentors from a CSV file (e.g. UniAid/Data/mentors.csv).

Run from the Backend directory with venv activated:

    python scripts/bulk_upload_mentors.py [path/to/mentors.csv]

If no path is given, uses ../Data/mentors.csv relative to this script.
"""

import argparse
import sys
from pathlib import Path

# Allow importing from Backend root when run as script
_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from db.session import SessionLocal
from services.mentor_service import MentorService


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk upload mentors from CSV")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=None,
        help="Path to mentors.csv (default: Data/mentors.csv relative to Backend)",
    )
    args = parser.parse_args()

    if args.csv_path:
        csv_path = Path(args.csv_path)
    else:
        csv_path = _backend_root.parent / "Data" / "mentors.csv"

    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)

    content = csv_path.read_text(encoding="utf-8", errors="replace")
    db = SessionLocal()
    try:
        created, errors = MentorService.bulk_create_from_csv(db, content)
        print(f"Created {created} mentor(s).")
        if errors:
            print(f"Errors ({len(errors)}):")
            for err in errors[:20]:
                print(f"  - {err}")
            if len(errors) > 20:
                print(f"  ... and {len(errors) - 20} more")
    finally:
        db.close()


if __name__ == "__main__":
    main()
