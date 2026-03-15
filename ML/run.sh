#!/usr/bin/env bash
# Run the ML recommendation service (uses ML venv so sentence_transformers etc. are available).
# From ML directory: ./run.sh
# Or from repo root: ML/run.sh
cd "$(dirname "$0")"
exec .venv/bin/python -m uvicorn api:app --reload --port 8001
