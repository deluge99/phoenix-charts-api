from app.schemas.base import ChartResponse, SubjectBase


class NatalRequest(SubjectBase):
    """Request body for natal chart generation."""


class NatalResponse(ChartResponse):
    chart_type: str = "natal"
