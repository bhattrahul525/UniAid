# UniAid Backend

Steps to run the backend after cloning the repo.

## 1. Go to the Backend directory

```bash
cd Backend
```

## 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
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

If you see errors like `column users.user_id does not exist`, the database tables don’t match the app schema. Drop and recreate them:

**Option A – with psql:**

```bash
psql "postgresql://user:password@localhost:5432/uniaid" -f scripts/reset_tables.sql
```

**Option B – with Python (venv activated):**

```bash
python scripts/drop_tables.py
```

Then restart the server so tables are created again.
