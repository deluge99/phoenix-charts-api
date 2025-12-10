from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.ai_prompt import build_system_prompt, build_user_message
from app.services.kerykeion_normalizer import normalize_kerykeion_payload
from app.core.openai_client import openai_stream_chat

router = APIRouter(prefix="/v1/ai-astrologer", tags=["AI Astrologer"])


class ChatRequest(BaseModel):
  kerykeion_payload: Dict[str, Any]
  chart_type: str
  user_message: str = ""
  session_id: str | None = None

@router.post("/session")
async def create_session(request: ChatRequest):
  normalized = normalize_kerykeion_payload(request.kerykeion_payload, request.chart_type)
  system_prompt = build_system_prompt(request.chart_type, normalized)

  messages = [{"role": "system", "content": system_prompt}]
  if request.user_message:
    messages.append({"role": "user", "content": build_user_message(request.user_message, normalized)})

  return StreamingResponse(
    openai_stream_chat(messages, model="gpt-4o-mini"),
    media_type="text/event-stream"
  )
