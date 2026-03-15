# UniAid ML recommendation service for Google Cloud Run
# Build from ML/ directory: docker build -t unicaid-ml .
# Cloud Run sets PORT (default 8080).

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code, dataset, and built models
COPY . .

# Cloud Run injects PORT; default 8080 for local runs
ENV PORT=8080
EXPOSE 8080

# Run FastAPI with uvicorn; must listen on 0.0.0.0 for Cloud Run
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT}
