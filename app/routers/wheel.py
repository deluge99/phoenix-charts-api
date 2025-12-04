import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.schemas.wheel import WheelPdfRequest
from app.services.chart_generator import generate_wheel_pdf_bytes

router = APIRouter(prefix="/wheel", tags=["wheel"])
logger = logging.getLogger("phoenix_charts.wheel")


@router.post("/pdf-bytes")
async def wheel_pdf_bytes(req: WheelPdfRequest):
    """
    Generate a natal wheel PDF using the Phoenix perfection pipeline.
    """
    logger.info(
        "[wheel] /wheel/pdf-bytes called name=%s theme=%s tz=%s lat=%.4f lng=%.4f",
        req.name,
        req.theme,
        req.tz_str,
        req.lat,
        req.lng,
    )
    try:
        pdf_bytes = generate_wheel_pdf_bytes(req)
        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        logger.error("[wheel] wheel_pdf_bytes failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Wheel generation failed: {e}")
