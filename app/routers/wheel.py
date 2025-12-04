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
    f"[wheel] /wheel/pdf-bytes called name={req.name or 'Unknown'} "
    f"theme={req.theme or 'classic'} tz={req.tz_str or 'None'} "
    f"lat={req.lat} lng={req.lng}"
    )
    try:
        pdf_bytes = generate_wheel_pdf_bytes(req)
        return Response(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        logger.error("[wheel] wheel_pdf_bytes failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Wheel generation failed: {e}")
