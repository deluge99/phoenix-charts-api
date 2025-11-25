from pydantic import BaseModel

from app.schemas.base import ChartResponse, SubjectBase


class CompositeRequest(BaseModel):
    first_subject: SubjectBase
    second_subject: SubjectBase


class CompositeResponse(ChartResponse):
    chart_type: str = "composite"
