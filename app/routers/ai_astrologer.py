# app/routers/ai_astrologer.py  ← FINAL VERSION
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.kerykeion_normalizer import normalize_kerykeion_payload
from app.services.ai_prompt import build_system_prompt
from app.core.openai_client import openai_stream_chat
from pydantic import BaseModel
from typing import Any, Dict

router = APIRouter(prefix="/v1/ai-astrologer", tags=["AI Astrologer"])

class ChatRequest(BaseModel):
    kerykeion_payload: Dict[str, Any] = {}
    chart_type: str = "natal"
    user_message: str = ""

@router.post("/session")
async def create_session(request: Request):
    body = await request.json()
    
    # Extract fields with defaults — works no matter how the client sends it
    kerykeion_payload = body.get("kerykeion_payload", {})
    chart_type = body.get("chart_type", "natal")
    user_message = body.get("user_message", "").strip()

    normalized = normalize_kerykeion_payload(kerykeion_payload, chart_type)
    
    messages = [
        {"role": "system", "content": build_system_prompt(chart_type, normalized)}
    ]
    if user_message:
        messages.append({"role": "user", "content": user_message})

    return StreamingResponse(
        openai_stream_chat(messages, model="gpt-4o-mini"),
        media_type="text/event-stream"
    )