from typing import Optional, Dict, Any

from pydantic import BaseModel


class WheelPdfRequest(BaseModel):
    """
    Request payload for generating a natal wheel PDF.
    Mirrors the working test_wheel_perfection.py payload.
    """

    name: str
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    tz_str: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    theme: Optional[str] = "classic"

    # Full kerykeion payload from Astro-Bot (preferred)
    kerykeion_data: Optional[Dict[str, Any]] = None

    # Optional chart type marker
    chart_type: Optional[str] = "natal"
