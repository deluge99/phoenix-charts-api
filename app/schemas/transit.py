from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import ChartResponse, SubjectBase


class TransitRequest(BaseModel):
    natal_subject: SubjectBase
    transit_datetime: datetime = Field(..., example="2025-01-01T00:00:00Z")
    transit_city: Optional[str] = None
    transit_country: Optional[str] = None
    transit_lat: Optional[float] = None
    transit_lng: Optional[float] = None


class TransitResponse(ChartResponse):
    chart_type: str = "transit"
