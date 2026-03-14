# scripts/reset_mentors.py
import sys
from pathlib import Path

_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from db.session import SessionLocal
from models.mentor_model import Mentor

db = SessionLocal()
try:
    count_before = db.query(Mentor).count()
    db.query(Mentor).delete()
    db.commit()
    count_after = db.query(Mentor).count()
    print(f"Deleted {count_before - count_after} mentors. Remaining: {count_after}")
finally:
    db.close()