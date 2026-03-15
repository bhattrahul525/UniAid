# UniAid Backend

Steps to run the backend and ML pipeline after cloning the repo.

---

## Steps to run the project

### 1. Go to the Backend directory

```bash
cd Backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the `Backend` directory:

```
DATABASE_URL=postgresql://user:password@localhost:5432/uniaid
# Required for /mentors/recommendations: base URL of the ML service (no trailing slash)
ML_SERVICE_URL=http://127.0.0.1:8001
```

### 5. (Optional) Reset database and sync data
(Optional) Sync mentors/mentees from `Dataset/` CSVs into the DB:

```bash
python scripts/sync_dataset_to_db.py
```

### 6. Build the ML recommendation index

Recommendations need the embedding index. **ML lives at repo root** (`UniAid/ML/`). From the **repo root**:

```bash
python ML/recommender.py build
```

Or from `ML/`:

```bash
cd ML
python recommender.py build
cd ..
```

This creates `ML/models/mentors_df.joblib`, `mentor_embeddings.npy`, `mentor_nn.joblib`, and `mentor_quality.joblib` from `Dataset/` (mentors, mentees, interactions).

### 7. (Optional) Train the Learning-to-Rank (LTR) model

For better recommendation ordering, train the LTR model **after** step 6. From **repo root**:

```bash
python -m ML.train_ltr
```

Or from `ML/`:

```bash
cd ML
python train_ltr.py
cd ..
```

This creates `ML/models/ltr_model.txt` and `ML/models/ltr_features.json`. The Backend API uses them automatically when present. **If the codebase adds new LTR features (e.g. language_match), retrain LTR** so the saved model matches the current feature set.

### 8. Start the ML service (separate process)

The Backend calls an external ML service for recommendations; it does not bundle ML code or heavy ML dependencies. From **repo root**:

```bash
cd ML
pip install -r requirements.txt
uvicorn api:app --reload --port 8001
```

Leave this running. Ensure `ML_SERVICE_URL` in Backend `.env` matches (e.g. `http://127.0.0.1:8001`).

### 9. Run the Backend server

From the **Backend** directory, use the project venv (so PyJWT and other deps are available):

```bash
./run.sh
```

Or activate the venv then run uvicorn:

```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

- **Backend API:** http://127.0.0.1:8000  
- **Backend docs:** http://127.0.0.1:8000/docs  
- **ML service:** http://127.0.0.1:8001 (health: http://127.0.0.1:8001/health)

Restart the ML service after rebuilding the index (step 6) or retraining LTR (step 7).

### Deploying Backend and ML separately

Backend has no ML dependencies; it calls the ML service over HTTP. For production:

1. **Deploy the ML service** (e.g. from `ML/` with its own runtime, or a separate container). Build the index and train LTR there (steps 6–7). Set the ML service’s base URL.
2. **Deploy the Backend** with `ML_SERVICE_URL` set to that base URL (e.g. `https://your-ml-service.example.com`).

See [docs/DEPLOYMENT_OPTIONS.md](docs/DEPLOYMENT_OPTIONS.md) for more.

---

## Data model (relevant tables)

- **users** – `email`, `password` (stored hashed), and optionally `mentor_id` (FK to `mentors.id`) or `mentee_id` if the user is a mentee.
- **mentors** – Mentor profile (student, parent, professor, etc.). Referenced by `users.mentor_id` when a user account is linked to a mentor.

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

## Recommendation API

Recommendations are computed by the **ML service** (repo root `ML/`). The Backend calls it via `ML_SERVICE_URL` and enriches results with mentor data from the DB. The `/mentors/recommendations` API returns mentor rows with `final_score`.

- **POST /mentors/recommendations** – Payload: `request_text` (optional), `top_k`, `user_id` (optional). At least one of `request_text` or `user_id` required. Returns ranked mentors with `mentor` and `final_score` (percentage).
- **GET /mentors/recommendations/evaluate** – Offline accuracy; params: `sample_size`, `top_k`, `seed`. Returns `hit_rate_at_k` and `mrr`.

ML index and LTR model are built in **Steps 6 and 7** above. **Swagger:** http://127.0.0.1:8000/docs

## Deployment: ML vs backend

If your deploy build times out (e.g. on Railway) because of heavy ML deps, you can either **separate ML and backend** into two services or **keep one app** and use CPU-only PyTorch. See [docs/DEPLOYMENT_OPTIONS.md](docs/DEPLOYMENT_OPTIONS.md) for details.
