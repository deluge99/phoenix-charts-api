#!/usr/bin/env bash
set -e

# Always run using the project virtual environment so kerykeion and
# other dependencies are present and consistent.
VENV_UVICORN="$(pwd)/.venv/bin/uvicorn"

if [ ! -x "$VENV_UVICORN" ]; then
  echo "uvicorn not found in .venv; did you create the virtualenv?" >&2
  echo "Try: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

PYTHONPATH="$(pwd)" \
"$VENV_UVICORN" app.main:app --reload --host 0.0.0.0 --port 8000
