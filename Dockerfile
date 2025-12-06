# Dockerfile for phoenix-charts-api (FastAPI + uvicorn)
FROM python:3.11-slim

# System deps – adjust as needed (cairo, fonts, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libjpeg-dev \
    zlib1g-dev \
    libcairo2-dev \
    pkg-config \
    fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Make sure Python can import your packages as `api.*`
ENV PYTHONPATH=/app

# Expose the charts API port
# ... all the existing stuff above ...
EXPOSE 8001

# IMPORTANT: point to the FastAPI app in app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]