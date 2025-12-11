# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import charts
from app.routers import wheel as wheel_routes  # ← import your wheel router

import logging
import os

app = FastAPI(title="Phoenix Charts API", version="0.1.0")

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

# Debug toggle for phoenix-charts
PHOENIX_DEBUG = os.getenv("PHOENIX_DEBUG", "0") == "1"

wheel_logger = logging.getLogger("phoenix_charts.wheel")
wheel_logger.setLevel(logging.DEBUG if PHOENIX_DEBUG else logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charts (existing)
app.include_router(charts.router, prefix="/api/v1")

# Wheel router (versioned)
app.include_router(wheel_routes.router, prefix="/api/v1")
# -> endpoint: POST http://localhost:8001/api/v1/wheel/pdf-bytes
