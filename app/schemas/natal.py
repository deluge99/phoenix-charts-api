from typing import Optional

from pydantic import BaseModel, Field


class NatalRequest(BaseModel):
    name: str = Field(..., description="Person name")
    year: int
    month: int
    day: int
    hour: int = 12
    minute: int = 0

    city: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    tz_str: Optional[str] = "UTC"

    theme: str = "dark_high_contrast"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "year": 1990,
                "month": 6,
                "day": 15,
                "hour": 12,
                "minute": 30,
                "city": "New York",
                "country": "US",
                "lat": 40.7128,
                "lng": -74.006,
                "tz_str": "America/New_York",
                "theme": "classic",
            }
        }
