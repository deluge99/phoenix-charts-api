# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import charts
from app.routers import wheel as wheel_routes  # ← import your wheel router

app = FastAPI(title="Phoenix Charts API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charts (existing)
app.include_router(charts.router, prefix="/api/v1")

# ✅ Wheel router – choose ONE of these options:

# OPTION 1: Root-level wheel (path: /wheel/png-bytes)
app.include_router(wheel_routes.router)
#   -> endpoint: POST http://localhost:8001/wheel/png-bytes

# OR OPTION 2: Versioned wheel (path: /api/v1/wheel/png-bytes)
# app.include_router(wheel_routes.router, prefix="/api/v1")
#   -> endpoint: POST http://localhost:8001/api/v1/wheel/png-bytes

@app.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok"}