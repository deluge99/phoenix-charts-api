from pydantic import BaseModel

from app.schemas.base import ChartResponse, SubjectBase


class SynastryRequest(BaseModel):
    first_subject: SubjectBase
    second_subject: SubjectBase


class SynastryResponse(ChartResponse):
    chart_type: str = "synastry"
