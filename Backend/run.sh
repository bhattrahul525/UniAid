#!/usr/bin/env bash
# Run the UniAid backend on port 8000 (uses Backend venv so deps like PyJWT are available).
# From Backend directory: ./run.sh
# Or from project root: Backend/run.sh
cd "$(dirname "$0")"
exec .venv/bin/uvicorn main:app --reload --port 8000
