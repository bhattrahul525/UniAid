# UniAid Backend

Steps to run the backend after cloning the repo.

## Data model (relevant tables)

- **users** – `email`, `password` (stored hashed), and optionally `mentor_id` (FK to `mentors.id`) or `mentee_id` if the user is a mentee.
- **mentors** – Mentor profile (student, parent, professor, etc.). Referenced by `users.mentor_id` when a user account is linked to a mentor.

## 1. Go to the Backend directory

```bash
cd Backend
```

## 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate (macOS)
Windows (PowerShell) .venv\Scripts\Activate.ps1
```



## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment

Create a `.env` file in the `Backend` directory with your PostgreSQL URL:

```
DATABASE_URL=postgresql://user:password@localhost:5432/uniaid
```

## 5. Run the server

```bash
uvicorn main:app --reload --port 8000
```

Or use the run script:

```bash
./run.sh
```

API: **http://127.0.0.1:8000** — Docs: **http://127.0.0.1:8000/docs**

## Resetting the database

If you get **500 Internal Server Error** in Postman or errors like `column users.first_name does not exist`, the database tables don’t match the app schema. Drop and recreate them:

**Option A – with psql:**

```bash
psql "postgresql://user:password@localhost:5432/uniaid" -f scripts/reset_tables.sql
```

**Option B – with Python (venv activated):**

```bash
python scripts/drop_tables.py
```

Then restart the server so tables are created again.

## Recommendation API (mentee_id + payload, accuracy)

Recommendations use `Data/users.csv`, `Data/mentors.csv`, and `Data/interactions.csv` (and optional ML index in `Backend/ML/models/`).

- **POST /recommendations** – Recommend mentors:
  - **mentee_id**: load mentee from DB and build a profile (users.csv shape) for the model.
  - **user_profile**: optional payload with same fields as users.csv (for testing without DB).
  - **request_text**: optional free-text (e.g. "help with visa").
  - Returns ranked mentors with `similarity`, `quality_score`, `final_score`.

- **GET /recommendations/evaluate** – Offline accuracy for testing:
  - Uses a sample of (user_id, mentor_id) from interactions and checks if the actual mentor is in top_k.
  - Query params: `sample_size` (default 200), `top_k` (default 5), `seed` (default 42).
  - Returns `hit_rate_at_k` and `mrr` (mean reciprocal rank).

**Build ML index once** (from `Backend/ML`):

```bash
cd Backend/ML
python recommender.py build
```

Then run the main backend; the first recommendation call will load the index.
