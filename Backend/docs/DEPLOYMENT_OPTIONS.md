# Deployment options: ML vs backend

This doc explains whether you can separate the ML recommender from the main backend, and compares that with other ways to fix slow or failing builds (e.g. Railway build timeout).

---

## Can you separate ML and backend into two deployments?

**Yes.** You can run:

1. **Backend** – FastAPI app with auth, users, mentors, mentees, sessions. **No** PyTorch / sentence-transformers / heavy ML deps. For recommendations it calls the ML service over HTTP.
2. **ML service** – Small API (e.g. FastAPI) that loads the recommender (embeddings, NN index, LTR), exposes something like `POST /recommend`, and returns mentor IDs + scores. Backend then enriches with full mentor data from the DB.

### How it would work

- **Backend** keeps:
  - `DATABASE_URL`, auth, all existing routes except the recommendation logic.
  - Recommendation route: if `user_id` is present, load user/mentee profile from DB; then `POST` to ML service with `{ "request_text": "...", "user_profile": { ... }, "top_k": 5 }`.
- **ML service**:
  - Input: `request_text` (optional), `user_profile` (optional, for LTR/university), `top_k`.
  - Output: `[ { "mentor_id": 1, "final_score": 0.92 }, ... ]`.
  - Uses only Dataset CSVs + `ML/models/` (or builds them at deploy). No DB.
- **Backend** receives the list, fetches full mentor rows from DB by ID, builds the response (with slug, etc.) and returns.

### Pros of separating

- **Backend build** is much faster and lighter (no torch/sentence-transformers/CUDA), so it’s less likely to hit build timeouts.
- You can scale or restart backend and ML independently.
- ML service can run on a machine with more memory if needed.

### Cons of separating

- Two services to deploy, monitor, and (if not free) pay for.
- Extra network hop: every recommendation request goes Backend → ML service → Backend → client (slightly higher latency).
- You need to pass `user_profile` from backend to ML when using `user_id` (so ML can do university filter and LTR). Contract and error handling become your responsibility.

---

## Is separation a good idea?

- **If the main problem is build timeout** (e.g. on Railway): separation fixes it by moving heavy deps to a second service. The **backend** build becomes quick; only the **ML** build is slow.
- **If you want the simplest setup**: keeping a **single** deployment and making the build lighter is often better (see below).

---

## Implemented: single-deployment alternatives (lighter build)

These are **implemented** in the repo:

1. **CPU-only PyTorch**  
   `requirements.txt` uses the CPU-only PyTorch index so pip does not pull CUDA wheels. That reduces install size and time and helps avoid build timeouts.

2. **Optional: don’t build ML at deploy time (download artifacts)**  
   If the ML model files are not present on the server, the app can download them once from a URL:
   - Set env **`ML_ARTIFACTS_URL`** to a URL that returns a **zip file** containing the ML artifacts (e.g. `mentors_df.joblib`, `mentor_embeddings.npy`, `mentor_nn.joblib`, `mentor_quality.joblib`; optionally `ltr_model.txt`, `ltr_features.json`).
   - Build the artifacts once locally (or in CI): from repo root run `python ML/recommender.py build` and optionally `python -m ML.train_ltr`, then zip the contents of **`ML/models/`** (ML is at repo root) and upload that zip to S3, GCS, or any public URL.
   - On first recommendation request, if any required file is missing and `ML_ARTIFACTS_URL` is set, the app downloads the zip and extracts into `ML/models/`.
   - **Create the zip:** From Backend: `python scripts/build_ml_artifacts_zip.py` (writes `ML/models/ml-artifacts.zip` at repo root). Or from repo root: `cd ML/models && zip -r ml-artifacts.zip .` then upload.

3. **Increase build timeout**  
   If your host (e.g. Railway) allows it, increase the build timeout so the single-service build can finish.

---

## Recommendation

- **First try:** Single deployment + **CPU-only PyTorch** + (if needed) **higher build timeout**. Easiest and often sufficient.
- **If builds still time out or you want a clear split:** Separate **backend** (no ML deps) and **ML service** (heavy deps, exposes `/recommend`), and have the backend call the ML service over HTTP.
