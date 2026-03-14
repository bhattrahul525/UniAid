"""
Bulk upload mentees from a CSV file.

Run from the Backend directory with venv activated:

    python scripts/bulk_upload_mentees.py [path/to/users_10000.csv]

If no path is given, uses ../../Dataset/users_10000.csv relative to this
script (i.e. UniAid/Dataset/users_10000.csv).

Architecture:
  Each CSV row creates TWO linked DB records:
    1. User  — first_name, last_name, email (generated), hashed_password
    2. Mentee — user_type, home_country, preferred_destination_country,
                field_of_study, degree_level, budget_range, preferred_language

  The User.mentee_id FK is set to the newly created Mentee.mentee_id.
  No existing UserService method handles bulk CSV creation, so this script
  calls the DB models directly (same pattern the service uses internally).

CSV → DB field mapping:
  first_name              → users.first_name
  last_name               → users.last_name
  (generated)             → users.email         e.g. firstname.lastname.N@uniaid.test
  (generated)             → users.hashed_password  bcrypt of "ChangeMe123!"
  user_type               → mentee.user_type
  home_country            → mentee.home_country
  "Australia"             → mentee.preferred_destination_country (constant — all plan to study in AU)
  field_of_study          → mentee.field_of_study
  degree_level            → mentee.degree_level
  budget_range_aud (int)  → mentee.budget_range  stored as "$15,000 – $30,000" bucket string
  preferred_language      → mentee.preferred_language

Columns silently skipped (not in Mentee/User model):
  user_id, preferred_city_type, target_university, intended_start_year,
  scholarship_interest, concern_*, work_while_studying_interest, goals,
  accommodation_type

Sampling:
  Exactly 2000 rows, stratified across user_type × home_country ×
  target_university for a balanced and diverse upload.
"""

import argparse
import csv
import io
import random
import sys
from collections import defaultdict
from pathlib import Path

_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from db.session import SessionLocal
from models.mentee_model import Mentee
from models.user_model import User
from utils.password import hash_password

UPLOAD_LIMIT = 2000
DEFAULT_PASSWORD = "ChangeMe123!"
DESTINATION_COUNTRY = "Australia"


# ── Helpers ──────────────────────────────────────────────────────────────────

def _budget_bucket(raw: str) -> str:
    """
    Convert a raw AUD integer string from the CSV into a human-readable
    budget range string that fits the Mentee.budget_range String column.

    Buckets (AUD per year):
      < 20,000          → "Under $20,000"
      20,000 – 29,999   → "$20,000 – $29,999"
      30,000 – 39,999   → "$30,000 – $39,999"
      40,000 – 49,999   → "$40,000 – $49,999"
      50,000 – 59,999   → "$50,000 – $59,999"
      >= 60,000          → "$60,000+"
    """
    try:
        amount = int(float(raw))
    except (ValueError, TypeError):
        return raw  # pass through unparseable values unchanged

    if amount < 20_000:
        return "Under $20,000"
    elif amount < 30_000:
        return "$20,000 – $29,999"
    elif amount < 40_000:
        return "$30,000 – $39,999"
    elif amount < 50_000:
        return "$40,000 – $49,999"
    elif amount < 60_000:
        return "$50,000 – $59,999"
    else:
        return "$60,000+"


def _make_email(first: str, last: str, index: int) -> str:
    """
    Generate a unique, deterministic test email from name + row index.
    e.g. "john.smith.42@uniaid.test"
    """
    clean = lambda s: "".join(c.lower() for c in s if c.isalpha())
    return f"{clean(first)}.{clean(last)}.{index}@uniaid.test"


def _stratified_sample(rows: list[dict], n: int, seed: int = 42) -> list[dict]:
    """
    Return n rows sampled proportionally across every unique combination of
    (user_type, home_country, target_university) so the upload stays diverse.
    """
    rng = random.Random(seed)

    strata: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = (
            row.get("user_type", "").strip(),
            row.get("home_country", "").strip(),
            row.get("target_university", "").strip(),
        )
        strata[key].append(row)

    total = len(rows)
    n = min(n, total)

    allocation: dict[tuple, int] = {
        key: max(1, round(len(group) / total * n))
        for key, group in strata.items()
    }

    # Resolve rounding drift
    while sum(allocation.values()) > n:
        allocation[max(allocation, key=lambda k: allocation[k])] -= 1
    while sum(allocation.values()) < n:
        headroom = {k: len(strata[k]) - allocation[k] for k in strata}
        best = max(headroom, key=lambda k: headroom[k])
        if headroom[best] <= 0:
            break
        allocation[best] += 1

    sampled: list[dict] = []
    for key, group in strata.items():
        k = min(allocation[key], len(group))
        sampled.extend(rng.sample(group, k))

    rng.shuffle(sampled)
    return sampled[:n]


# ── Core upload ───────────────────────────────────────────────────────────────

def _bulk_create(db, rows: list[dict]) -> tuple[int, list[str]]:
    """
    Create one User + one Mentee per row and link them.
    Returns (created_count, error_messages).
    """
    created = 0
    errors: list[str] = []

    for row_num, row in enumerate(rows, start=1):
        try:
            first = (row.get("first_name") or "").strip()
            last  = (row.get("last_name") or "").strip()
            if not first or not last:
                errors.append(f"Row {row_num}: first_name and last_name are required")
                continue

            email = _make_email(first, last, row_num)

            # 1. Create Mentee profile
            mentee = Mentee(
                user_type=row.get("user_type") or None,
                home_country=row.get("home_country") or None,
                preferred_destination_country=DESTINATION_COUNTRY,
                field_of_study=row.get("field_of_study") or None,
                degree_level=row.get("degree_level") or None,
                budget_range=_budget_bucket(row.get("budget_range_aud", "")),
                preferred_language=row.get("preferred_language") or None,
            )
            db.add(mentee)
            db.flush()  # get mentee_id before committing

            # 2. Create User linked to the Mentee
            user = User(
                first_name=first,
                last_name=last,
                email=email,
                hashed_password=hash_password(DEFAULT_PASSWORD),
                mentee_id=mentee.mentee_id,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            db.refresh(mentee)
            created += 1

        except Exception as exc:
            db.rollback()
            errors.append(f"Row {row_num}: {exc}")

    return created, errors


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk upload mentees from CSV")
    parser.add_argument(
        "csv_path",
        nargs="?",
        default=None,
        help="Path to mentees CSV (default: UniAid/Dataset/mentees_dataset.csv)",
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
        # UniAid/Backend/scripts/ → .parent.parent.parent = UniAid/
        csv_path = (
            Path(__file__).resolve().parent.parent.parent
            / "Dataset"
            / "mentees_dataset.csv"
        )

    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)

    print(f"Reading: {csv_path}")
    raw_content = csv_path.read_text(encoding="utf-8", errors="replace")

    reader = csv.DictReader(io.StringIO(raw_content))
    all_rows = list(reader)
    print(f"Total rows in dataset: {len(all_rows)}")

    # Stratified sample
    print(f"Sampling {UPLOAD_LIMIT} diverse rows (seed={args.seed}) ...")
    sampled = _stratified_sample(all_rows, UPLOAD_LIMIT, seed=args.seed)

    # Diversity summary
    type_counts:   dict[str, int] = defaultdict(int)
    country_counts: dict[str, int] = defaultdict(int)
    uni_counts:    dict[str, int] = defaultdict(int)
    degree_counts: dict[str, int] = defaultdict(int)
    for row in sampled:
        type_counts[row.get("user_type", "unknown")] += 1
        country_counts[row.get("home_country", "unknown")] += 1
        uni_counts[row.get("target_university", "unknown")] += 1
        degree_counts[row.get("degree_level", "unknown")] += 1

    print("\nSample diversity breakdown:")
    print("  User types:")
    for k, v in sorted(type_counts.items()):
        print(f"    {k}: {v}")
    print("  Home countries (top 10):")
    for k, v in sorted(country_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"    {k}: {v}")
    print("  Universities (target — used for sampling only, not stored):")
    for k, v in sorted(uni_counts.items()):
        print(f"    {k}: {v}")
    print("  Degree levels:")
    for k, v in sorted(degree_counts.items()):
        print(f"    {k}: {v}")
    print()

    # Upload
    db = SessionLocal()
    try:
        created, errors = _bulk_create(db, sampled)
        print(f"Created {created} mentee(s).")
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