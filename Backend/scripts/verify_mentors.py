# scripts/verify_mentors.py
import sys
from pathlib import Path

_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from collections import Counter
from db.session import SessionLocal
from models.mentor_model import Mentor

db = SessionLocal()
try:
    mentors = db.query(Mentor).all()
    print(f"Total mentors in DB: {len(mentors)}\n")

    types = Counter(m.mentor_type for m in mentors)
    print("By mentor_type:")
    for k, v in sorted(types.items()):
        print(f"  {k}: {v}")

    unis = Counter(m.university for m in mentors)
    print(f"\nBy university ({len(unis)} unique):")
    for k, v in sorted(unis.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

    nulls = sum(1 for m in mentors if not m.first_name or not m.last_name)
    print(f"\nRows with missing name: {nulls}")

    ratings = [m.mentor_rating for m in mentors if m.mentor_rating is not None]
    print(f"Ratings — min: {min(ratings):.1f}, max: {max(ratings):.1f}, avg: {sum(ratings)/len(ratings):.2f}")
finally:
    db.close()