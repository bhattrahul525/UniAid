# ML recommendation service

Train and run the mentor recommendation model here. The **Backend** calls this service over HTTP for `/mentors/recommendations`; it does not import ML code or use ML dependencies.

## Setup and run

1. **Build the index** (from repo root):
   ```bash
   python ML/recommender.py build
   ```
2. **(Optional) Train LTR:** `python -m ML.train_ltr`
3. **Start the ML service** — from the **ML** directory, use the venv’s uvicorn (otherwise the reload worker may use a different Python and miss `sentence_transformers`):
   ```bash
   cd ML
   pip install -r requirements.txt   # if not done yet
   ./run.sh
   ```
   Or: ` .venv/bin/uvicorn api:app --reload --port 8001`  
   Do **not** use plain `uvicorn` if you have multiple Pythons (e.g. conda base); use `./run.sh` or `.venv/bin/uvicorn`.
4. In Backend `.env`, set `ML_SERVICE_URL=http://127.0.0.1:8001`.

## Deployment

### Google Cloud Run (Docker, recommended)

A **Dockerfile** and step-by-step instructions are in **[DEPLOY_CLOUD_RUN.md](./DEPLOY_CLOUD_RUN.md)**. Summary:

1. From repo root: `gcloud builds submit --tag gcr.io/PROJECT_ID/unicaid-ml ./ML`
2. Deploy: `gcloud run deploy unicaid-ml --image gcr.io/PROJECT_ID/unicaid-ml --region REGION --allow-unauthenticated --memory 2Gi --port 8080`
3. Set Backend env **`ML_SERVICE_URL`** to the Cloud Run URL.

### Railway

- **Root directory:** Set to `ML` so the service runs from the ML folder.
- **Dataset:** The code looks for `Dataset/` inside `ML/` first, then as a sibling (repo root). For a self-contained deploy, **copy the repo’s `Dataset` folder into `ML/`** so the deployed app has `ML/Dataset/` with `mentors_dataset.csv`, `mentees_dataset.csv`, `interactions_dataset.csv`. Alternatively deploy the full repo with root = repo root and start command: `cd ML && uvicorn api:app --host 0.0.0.0 --port $PORT`.
- **Start command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
- **Models:** Ensure `ML/models/` contains the built artifacts (e.g. `mentors_df.joblib`, `mentor_embeddings.npy`, `mentor_nn.joblib`, and optionally LTR files). Build them locally and commit, or run a build step in deploy.

## Endpoints used by Backend

- **POST /recommend** – Body: `{ "request_text?", "user_profile?", "top_k", "candidate_university?" }`. Returns `[{ "mentor_id", "final_score" }, ...]`.
- **GET /evaluate** – Query: `sample_size`, `top_k`, `seed`. Returns `{ "hit_rate_at_k", "mrr", "n_eval", "top_k" }`.
- **GET /health** – Health check.
