from fastapi import APIRouter, HTTPException

from app.schemas.natal import NatalRequest
from app.schemas.synastry import SynastryRequest
from app.schemas.transit import TransitRequest
from app.schemas.composite import CompositeRequest
from app.services.chart_generator import (
    generate_natal_chart,
    generate_synastry_chart,
    generate_transit_chart,
    generate_composite_chart,
)


router = APIRouter(tags=["charts"])


@router.post("/natal", summary="Generate natal chart with SVG")
async def natal_endpoint(req: NatalRequest):
    try:
        return generate_natal_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Natal chart generation failed: {e}")


@router.post("/synastry", summary="Generate synastry chart with SVG")
async def synastry_endpoint(req: SynastryRequest):
    try:
        return generate_synastry_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synastry chart generation failed: {e}")


@router.post("/transit", summary="Generate transit chart with SVG")
async def transit_endpoint(req: TransitRequest):
    try:
        return generate_transit_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transit chart generation failed: {e}")


@router.post("/composite", summary="Generate composite chart with SVG")
async def composite_endpoint(req: CompositeRequest):
    try:
        return generate_composite_chart(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Composite chart generation failed: {e}")
