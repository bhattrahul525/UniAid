#!/usr/bin/env python3
"""
Delete all sessions in the DB and seed ~300 new sessions.
Sessions are meaningful, hosted by real mentors from the DB, with a wide range of
topics and roughly 9 sessions per day over ~33 days.

Run from Backend directory (venv activated):
  python scripts/seed_sessions.py

Requires: DATABASE_URL in .env. Mentors must already exist in the DB.
"""
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND_ROOT = _SCRIPT_DIR.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from dotenv import load_dotenv
load_dotenv(_BACKEND_ROOT / ".env")

from sqlalchemy.orm import Session as DBSession
from db.session import SessionLocal
from models.session_model import Session as SessionModel, SessionType
from models.mentor_model import Mentor

# ~300 sessions, ~9 per day => ~33 days of sessions
TOTAL_SESSIONS = 300
SESSIONS_PER_DAY = 9

# Diverse, meaningful session topics (title + short description)
SESSION_TOPICS = [
    ("Visa and Immigration Q&A", "Get your visa and immigration questions answered by mentors who have been through the process."),
    ("Housing and Accommodation Tips", "Finding a place to live: on-campus, off-campus, and what to look for."),
    ("Cultural Adaptation and Settling In", "Adjusting to a new country: culture shock, making friends, and feeling at home."),
    ("Career Guidance and Employability", "Building your CV, job search strategies, and what employers look for."),
    ("Academic Success and Study Skills", "Time management, exam prep, and getting the most from your degree."),
    ("English Language Support", "Practical English for uni and everyday life: academic writing and conversation."),
    ("Finance and Budgeting for Students", "Managing money: budgets, part-time work, and avoiding debt."),
    ("Mental Health and Wellbeing", "Staying well under pressure: stress, isolation, and where to get support."),
    ("Networking and Industry Connections", "How to network as a student and connect with industry."),
    ("First Year Survival Guide", "What to expect in your first year: orientation, courses, and tips from current students."),
    ("Research and Writing Skills", "Academic writing, referencing, and research skills for assignments."),
    ("Part-Time Work and Visa Rules", "Working while studying: visa conditions, finding jobs, and balancing work and study."),
    ("Support for Parents of International Students", "For parents: how to support your child from afar and when to visit."),
    ("Health Services and Insurance", "Understanding health cover, GP visits, and mental health services on campus."),
    ("Scholarships and Funding", "Finding and applying for scholarships and bursaries."),
    ("Settling In: Orientation and Beyond", "Making the most of orientation week and your first month."),
    ("Building Confidence in a New Environment", "Overcoming shyness and building confidence in class and socially."),
    ("Post-Study Work and Migration", "Pathways after graduation: post-study work visas and migration options."),
    ("Cross-Cultural Communication", "Communicating across cultures: in the classroom and in the workplace."),
    ("Balancing Family and Study", "For parent-mentors: balancing your own commitments while supporting your child."),
    ("Industry Transition After Uni", "Moving from study to work: what to expect and how to prepare."),
    ("Student Safety and Rights", "Your rights as a student and staying safe on and off campus."),
    ("Choosing Electives and Planning Your Degree", "How to choose electives and plan your degree for your goals."),
    ("Managing Group Assignments", "Working in groups: communication, conflict, and getting the grade."),
    ("Campus Life and Clubs", "Getting involved: clubs, societies, and making the most of campus life."),
    ("Homesickness and Staying Connected", "Dealing with homesickness and staying connected with family back home."),
    ("Interview Skills and Job Applications", "Resume tips, cover letters, and how to perform in interviews."),
    ("Understanding Australian Academic Culture", "How Australian universities work: tutorials, assessments, and expectations."),
    ("Renting and Tenant Rights", "Renting in Australia: leases, bonds, and your rights as a tenant."),
    ("Public Transport and Getting Around", "Navigating public transport and getting around your city."),
]

def _random_scheduled_at(start: datetime, num_days: int) -> datetime:
    """Pick a random time within the window, favouring 9–17 (business hours)."""
    day_offset = random.randint(0, max(0, num_days - 1))
    # ~70% during 9am–5pm, rest in evening
    if random.random() < 0.7:
        hour = random.randint(9, 16)
        minute = random.choice([0, 15, 30, 45])
    else:
        hour = random.randint(17, 20)
        minute = random.choice([0, 30])
    d = start + timedelta(days=day_offset, hours=hour, minutes=minute)
    return d.replace(tzinfo=timezone.utc)


def run():
    db: DBSession = SessionLocal()
    try:
        # 1. Get all mentor IDs from DB (real mentors only)
        mentor_ids = [r.id for r in db.query(Mentor.id).all()]
        if not mentor_ids:
            print("No mentors in DB. Run sync_dataset_to_db.py or add mentors first.")
            return
        print(f"Found {len(mentor_ids)} mentors in DB.")

        # 2. Delete existing sessions (session_users cascade when sessions are deleted)
        deleted = db.query(SessionModel).delete()
        db.commit()
        print(f"Deleted {deleted} existing sessions.")

        # 3. Build list of (title, description) with variety (repeat topics to reach 300)
        topic_list = SESSION_TOPICS * (TOTAL_SESSIONS // len(SESSION_TOPICS) + 1)
        random.shuffle(topic_list)
        chosen = topic_list[:TOTAL_SESSIONS]

        # 4. Time window: ~33 days, starting from a few days ago so some are "past"
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=3)
        num_days = (TOTAL_SESSIONS // SESSIONS_PER_DAY) + 1

        # 5. Create sessions: diverse mentor_id, topic, type, scheduled_at
        sessions = []
        for (title, description) in chosen:
            mentor_id = random.choice(mentor_ids)
            session_type = SessionType.public if random.random() < 0.75 else SessionType.private
            scheduled_at = _random_scheduled_at(start, num_days)
            sessions.append(SessionModel(
                title=title,
                description=description,
                mentor_id=mentor_id,
                session_type=session_type,
                scheduled_at=scheduled_at,
            ))
        db.add_all(sessions)
        db.commit()
        print(f"Inserted {len(sessions)} new sessions (~{SESSIONS_PER_DAY} per day over ~{num_days} days).")
    finally:
        db.close()


if __name__ == "__main__":
    run()
