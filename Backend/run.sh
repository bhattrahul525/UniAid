#!/usr/bin/env bash
# Run the UniAid backend on port 8000.
# From Backend directory: ./run.sh
# Or from project root: Backend/run.sh
cd "$(dirname "$0")"
uvicorn main:app --reload --port 8000
