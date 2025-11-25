from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.schemas.composite import CompositeRequest
from app.schemas.natal import NatalRequest
from app.schemas.synastry import SynastryRequest
from app.schemas.transit import TransitRequest
from app.services import chart_generator

router = APIRouter(prefix="/api/v1", tags=["charts"])


@router.post("/natal", summary="Generate natal chart")
def natal(req: NatalRequest):
    try:
        return chart_generator.generate_natal(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synastry", summary="Generate synastry chart")
def synastry(req: SynastryRequest):
    try:
        return chart_generator.generate_synastry(req.first_subject, req.second_subject)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transit", summary="Generate transit chart")
def transit(req: TransitRequest):
    try:
        return chart_generator.generate_transit(req.natal_subject, req.transit_datetime)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/composite", summary="Generate composite chart")
def composite(req: CompositeRequest):
    try:
        return chart_generator.generate_composite(req.first_subject, req.second_subject)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
