from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import charts


app = FastAPI(title="Phoenix Charts API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(charts.router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok"}
