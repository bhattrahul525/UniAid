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

## Endpoints used by Backend

- **POST /recommend** – Body: `{ "request_text?", "user_profile?", "top_k", "candidate_university?" }`. Returns `[{ "mentor_id", "final_score" }, ...]`.
- **GET /evaluate** – Query: `sample_size`, `top_k`, `seed`. Returns `{ "hit_rate_at_k", "mrr", "n_eval", "top_k" }`.
- **GET /health** – Health check.
