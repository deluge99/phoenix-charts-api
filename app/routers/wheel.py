from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import logging

from app.services.chart_generator import generate_wheel_pdf_bytes

router = APIRouter(prefix="/wheel", tags=["wheel"])
logger = logging.getLogger("phoenix_charts.wheel")


class WheelRequest(BaseModel):
    name: str
    chart_type: str
    kerykeion_data: dict


@router.post("/pdf-bytes")
async def wheel_pdf_bytes(req: WheelRequest):
    """
    Logs request and returns a generated wheel PDF (pure SVG -> PDF).
    """
    logger.info(
        "[wheel] /wheel/pdf-bytes called name=%s chart_type=%s k_keys=%s",
        req.name,
        req.chart_type,
        list(req.kerykeion_data.keys())
        if isinstance(req.kerykeion_data, dict)
        else type(req.kerykeion_data),
    )
    if isinstance(req.kerykeion_data, dict) and "subject" in req.kerykeion_data:
        subj = req.kerykeion_data.get("subject")
        logger.info(
            "[wheel] subject keys=%s iso_local=%s",
            list(subj.keys()) if isinstance(subj, dict) else subj,
            subj.get("iso_formatted_local_datetime") if isinstance(subj, dict) else None,
        )
    try:
        pdf_bytes = generate_wheel_pdf_bytes(req)
        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        logger.error("[wheel] wheel_pdf_bytes failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Wheel generation failed: {e}")
