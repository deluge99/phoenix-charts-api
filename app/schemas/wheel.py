from typing import Optional

from pydantic import BaseModel


class WheelPdfRequest(BaseModel):
    """
    Request payload for generating a natal wheel PDF.
    Mirrors the working test_wheel_perfection.py payload.
    """

    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    lat: float
    lng: float
    tz_str: str
    city: Optional[str] = None
    country: Optional[str] = None
    theme: Optional[str] = "classic"

    # 👇 NEW FIELD — this is what generate_wheel_pdf_bytes is trying to read
    chart_type: Optional[str] = "natal"
