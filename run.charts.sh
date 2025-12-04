#!/usr/bin/env bash

# ============================================
# 🔮 Phoenix Charts API Runner (Wheel Generator)
# ============================================

set -e

# Move into project root (directory containing app/)
cd "$(dirname "$0")"

echo "🜁 Starting Phoenix Charts API (wheel + theme engine)…"

# Load .env if present (non-fatal)
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️  No .env found (optional)."
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✨ Virtual environment activated (.venv)"
else
    echo "❌ No .venv found. Create it with: python3 -m venv .venv"
    exit 1
fi

# Ensure Python sees this project
echo "📦 Using PYTHONPATH: $(pwd)"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start API
echo "🚀 Launching Phoenix Charts on http://0.0.0.0:8001 ..."
uvicorn app.main:app \
    --reload \
    --host 0.0.0.0 \
    --port 8001