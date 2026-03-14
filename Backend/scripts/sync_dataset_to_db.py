#!/usr/bin/env python3
"""
Sync mentor and mentee data from Dataset CSVs into the DB (upsert).
- Reads Dataset/mentors_dataset.csv and Dataset/mentees_dataset.csv.
- For each row: if the id exists in the DB, updates that row from the CSV; otherwise inserts.
- Preserves mentor_id / user_id from the CSV so IDs stay in sync with the Dataset.

Run from Backend (venv activated):
  python scripts/sync_dataset_to_db.py
"""
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import text

_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND_ROOT = _SCRIPT_DIR.parent
_PROJECT_ROOT = _BACKEND_ROOT.parent
_DATASET = _PROJECT_ROOT / "Dataset"


def _ensure_path():
    if str(_BACKEND_ROOT) not in sys.path:
        sys.path.insert(0, str(_BACKEND_ROOT))


def _bool_to_int(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return 0
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, (int, float)):
        return 1 if val else 0
    s = str(val).strip().lower()
    if s in ("true", "1", "yes"):
        return 1
    return 0


def _safe_int(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def _safe_float(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _str(val, max_len=None):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    if not s or s.lower() == "nan":
        return None
    if max_len and len(s) > max_len:
        return s[:max_len]
    return s


def main():
    load_dotenv(_BACKEND_ROOT / ".env")
    _ensure_path()

    from db.database import engine
    from db.session import SessionLocal
    from models.mentee_model import Mentee
    from models.mentor_model import Mentor

    mentees_path = _DATASET / "mentees_dataset.csv"
    mentors_path = _DATASET / "mentors_dataset.csv"
    for p in (mentees_path, mentors_path):
        if not p.exists():
            raise SystemExit(f"Not found: {p}")

    df_mentors = pd.read_csv(mentors_path)
    df_mentees = pd.read_csv(mentees_path)

    db = SessionLocal()
    try:
        # --- Mentors: upsert from CSV ---
        added_mentors = 0
        updated_mentors = 0
        for _, row in df_mentors.iterrows():
            mid = _safe_int(row.get("mentor_id"))
            if mid is None:
                continue
            m = db.query(Mentor).filter(Mentor.id == mid).first()
            if m is None:
                m = Mentor(id=mid)
                db.add(m)
                added_mentors += 1
            else:
                updated_mentors += 1
            m.first_name = _str(row.get("first_name"), 100) or "Unknown"
            m.last_name = _str(row.get("last_name"), 100) or "Unknown"
            m.mentor_type = _str(row.get("mentor_type"), 50) or "student"
            m.university = _str(row.get("university"), 200)
            m.field_of_study = _str(row.get("field_of_study"), 200)
            m.degree_level = _str(row.get("degree_level"), 50)
            m.years_in_country = _safe_int(row.get("years_in_country"))
            m.visa_experience = _bool_to_int(row.get("visa_experience"))
            m.housing_experience = _bool_to_int(row.get("housing_experience"))
            m.cultural_adaptation_experience = _bool_to_int(row.get("cultural_adaptation_experience"))
            m.career_guidance_experience = _bool_to_int(row.get("career_guidance_experience"))
            m.languages_spoken = _str(row.get("languages_spoken"), 255)
            m.bio = _str(row.get("bio"))
            m.availability_hours_per_week = _safe_int(row.get("availability_hours_per_week"))
            m.sessions_completed = _safe_int(row.get("sessions_completed"))
            m.response_time_hours = _safe_int(row.get("response_time_hours"))
            m.mentor_rating = _safe_float(row.get("mentor_rating"))

        if added_mentors or updated_mentors:
            db.flush()
            if added_mentors:
                db.execute(text("SELECT setval(pg_get_serial_sequence('mentors', 'id'), (SELECT COALESCE(MAX(id), 1) FROM mentors))"))
            db.commit()
        print(f"Mentors: {added_mentors} inserted, {updated_mentors} updated (total from CSV: {len(df_mentors)})")

        # --- Mentees: upsert from CSV ---
        added_mentees = 0
        updated_mentees = 0
        for _, row in df_mentees.iterrows():
            uid = _safe_int(row.get("user_id"))
            if uid is None:
                continue
            me = db.query(Mentee).filter(Mentee.mentee_id == uid).first()
            if me is None:
                me = Mentee(mentee_id=uid)
                db.add(me)
                added_mentees += 1
            else:
                updated_mentees += 1
            me.user_type = _str(row.get("user_type"), 50) or "student"
            me.home_country = _str(row.get("home_country"), 100)
            me.preferred_destination_country = _str(row.get("target_university"), 100)
            me.field_of_study = _str(row.get("field_of_study"), 200)
            me.degree_level = _str(row.get("degree_level"), 50)
            me.budget_range = _str(row.get("budget_range_aud"), 50)
            me.preferred_language = _str(row.get("preferred_language"), 50)
            me.bio = _str(row.get("bio"))

        if added_mentees or updated_mentees:
            db.flush()
            if added_mentees:
                db.execute(text("SELECT setval(pg_get_serial_sequence('mentee', 'mentee_id'), (SELECT COALESCE(MAX(mentee_id), 1) FROM mentee))"))
            db.commit()
        print(f"Mentees: {added_mentees} inserted, {updated_mentees} updated (total from CSV: {len(df_mentees)})")
    finally:
        db.close()


if __name__ == "__main__":
    main()
