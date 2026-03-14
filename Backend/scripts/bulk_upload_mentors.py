"""
Bulk upload mentors from a CSV file.

Run from the Backend directory with venv activated:

    python scripts/bulk_upload_mentors.py [path/to/mentors.csv]

If no path is given, uses ../../Dataset/mentors_dataset.csv relative to this
script (i.e. UniAid/Dataset/mentors_dataset.csv).

Compatibility notes (dataset -> DB):
  - Boolean columns (visa_experience, housing_experience,
    cultural_adaptation_experience, career_guidance_experience) are stored as
    "True"/"False" strings in the CSV; this script normalises them to 1/0
    before passing content to MentorService.
  - mentor_id in the CSV is ignored - the DB uses its own autoincrement id.
  - Extra columns (ethnicity, country_of_origin, mentoring_topics, bio) are
    not in the Mentor model and are silently skipped by MentorService.
  - graduation_year is not present in the dataset and will be stored as NULL,
    which is valid since the column is optional.

Sampling:
  - Only 1000 rows are uploaded, selected via stratified random sampling
    across mentor_type, ethnicity, and university to ensure diversity.
"""

import argparse
import csv
import io
import random
import sys
from collections import defaultdict
from pathlib import Path

# Allow importing from Backend root when run as script
_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from db.session import SessionLocal
from services.mentor_service import MentorService

# Columns stored as "True"/"False" in the CSV that must be 0/1 for the DB.
_BOOL_COLUMNS = {
    "visa_experience",
    "housing_experience",
    "cultural_adaptation_experience",
    "career_guidance_experience",
}

UPLOAD_LIMIT = 1000


def _stratified_sample(rows: list[dict], n: int, seed: int = 42) -> list[dict]:
    """
    Return n rows sampled proportionally across every unique combination of
    (mentor_type, ethnicity, university) so the uploaded subset stays diverse.

    Strategy:
      1. Group rows by stratum (mentor_type, ethnicity, university).
      2. Allocate slots proportionally to stratum size (at least 1 per stratum).
      3. Randomly sample each stratum up to its allocation.
      4. If total < n after proportional allocation (rounding losses), fill
         remaining slots by sampling from the largest strata first.
    """
    rng = random.Random(seed)

    # Group rows by stratum key
    strata: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (
            row.get("mentor_type", "").strip(),
            row.get("ethnicity", "").strip(),
            row.get("university", "").strip(),
        )
        strata[key].append(row)

    total = len(rows)
    n = min(n, total)

    # Proportional allocation - guarantee at least 1 per stratum
    allocation: dict[tuple, int] = {}
    for key, group in strata.items():
        allocation[key] = max(1, round(len(group) / total * n))

    # Trim if over-allocated
    while sum(allocation.values()) > n:
        max_key = max(allocation, key=lambda k: allocation[k])
        allocation[max_key] -= 1

    # Fill if under-allocated (rounding losses)
    while sum(allocation.values()) < n:
        headroom = {k: len(strata[k]) - allocation[k] for k in strata}
        best_key = max(headroom, key=lambda k: headroom[k])
        if headroom[best_key] <= 0:
            break
        allocation[best_key] += 1

    # Sample each stratum
    sampled: list[dict] = []
    for key, group in strata.items():
        k = min(allocation[key], len(group))
        sampled.extend(rng.sample(group, k))

    rng.shuffle(sampled)
    return sampled[:n]


def _normalise_booleans(rows: list[dict]) -> list[dict]:
    """
    Convert True/False strings in boolean columns to 1/0 in-place.
    Returns the same list for convenience.
    """
    for row in rows:
        for col in _BOOL_COLUMNS:
            if col in row:
                raw = row[col].strip().lower()
                if raw == "true":
                    row[col] = "1"
                elif raw == "false":
                    row[col] = "0"
    return rows


def _rows_to_csv(rows: list[dict], fieldnames: list[str]) -> str:
    """Serialise a list of row dicts back to a CSV string."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk upload mentors from CSV")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=None,
        help="Path to mentors CSV (default: UniAid/Dataset/mentors_dataset.csv)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible sampling (default: 42)",
    )
    args = parser.parse_args()

    if args.csv_path:
        csv_path = Path(args.csv_path)
    else:
        # Resolution: UniAid/Backend/scripts/bulk_upload_mentors.py
        #   parent            = UniAid/Backend/scripts
        #   parent.parent     = UniAid/Backend
        #   parent.parent.parent = UniAid
        csv_path = Path(__file__).resolve().parent.parent.parent / "Dataset" / "mentors_dataset.csv"

    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)

    print(f"Reading: {csv_path}")
    raw_content = csv_path.read_text(encoding="utf-8", errors="replace")

    # Parse all rows
    reader = csv.DictReader(io.StringIO(raw_content))
    fieldnames = list(reader.fieldnames or [])
    all_rows = list(reader)
    print(f"Total rows in dataset: {len(all_rows)}")

    # Stratified sample
    print(f"Sampling {UPLOAD_LIMIT} diverse rows (seed={args.seed}) ...")
    sampled = _stratified_sample(all_rows, UPLOAD_LIMIT, seed=args.seed)

    # Log diversity summary
    type_counts: dict[str, int] = defaultdict(int)
    eth_counts:  dict[str, int] = defaultdict(int)
    uni_counts:  dict[str, int] = defaultdict(int)
    for row in sampled:
        type_counts[row.get("mentor_type", "unknown")] += 1
        eth_counts[row.get("ethnicity", "unknown")] += 1
        uni_counts[row.get("university", "unknown")] += 1

    print("\nSample diversity breakdown:")
    print("  Mentor types:")
    for k, v in sorted(type_counts.items()):
        print(f"    {k}: {v}")
    print("  Ethnicities:")
    for k, v in sorted(eth_counts.items()):
        print(f"    {k}: {v}")
    print("  Universities:")
    for k, v in sorted(uni_counts.items()):
        print(f"    {k}: {v}")
    print()

    # Normalise booleans and re-serialise
    _normalise_booleans(sampled)
    content = _rows_to_csv(sampled, fieldnames)

    # Upload
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