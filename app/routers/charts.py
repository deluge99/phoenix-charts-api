from fastapi import APIRouter, HTTPException

from app.schemas.natal import NatalRequest
from app.services.chart_generator import generate_natal_chart


router = APIRouter(tags=["charts"])


@router.post("/natal", summary="Generate natal chart with SVG")
async def natal_endpoint(req: NatalRequest):
    try:
        return generate_natal_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Natal chart generation failed: {e}")
