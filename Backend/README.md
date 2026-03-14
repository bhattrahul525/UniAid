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

Create a `.env` file in the `Backend` directory with your PostgreSQL URL:

```
DATABASE_URL=postgresql://user:password@localhost:5432/uniaid
```

### 5. (Optional) Reset database and sync data
(Optional) Sync mentors/mentees from `Dataset/` CSVs into the DB:

```bash
python scripts/sync_dataset_to_db.py
```

### 6. Build the ML recommendation index

Recommendations need the embedding index. From the **Backend** directory:

```bash
python ML/recommender.py build
```

Or from `Backend/ML`:

```bash
cd ML
python recommender.py build
cd ..
```

This creates `ML/models/mentors_df.joblib`, `mentor_embeddings.npy`, `mentor_nn.joblib`, and `mentor_quality.joblib` from `Dataset/` (mentors, mentees, interactions).

### 7. (Optional) Train the Learning-to-Rank (LTR) model

For better recommendation ordering, train the LTR model **after** step 6:

```bash
python ML/train_ltr.py
```

Or from `Backend/ML`:

```bash
cd ML
python train_ltr.py
cd ..
```

This creates `ML/models/ltr_model.txt` and `ML/models/ltr_features.json`. The API uses them automatically when present.

### 8. Run the server

```bash
uvicorn main:app --reload --port 8000
```

Or:

```bash
./run.sh
```

- **API:** http://127.0.0.1:8000  
- **Docs:** http://127.0.0.1:8000/docs  

Restart the server after rebuilding the ML index (step 6) or retraining LTR (step 7) so it loads the new artifacts.

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

Recommendations use **Dataset/** (`mentors_dataset.csv`, `mentees_dataset.csv`, `interactions_dataset.csv`) and the ML index in `Backend/ML/models/`. The API returns mentor data from the DB when available.

- **POST /recommendations** – Payload: `request_text` (optional), `top_k`, `user_id` (optional). At least one of `request_text` or `user_id` required. Returns ranked mentors with `mentor` and `final_score` (percentage).
- **GET /recommendations/evaluate** – Offline accuracy; params: `sample_size`, `top_k`, `seed`. Returns `hit_rate_at_k` and `mrr`.

ML index and LTR model are built in **Steps 6 and 7** above. **Swagger:** http://127.0.0.1:8000/docs
