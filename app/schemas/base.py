from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.enums import HouseSystem, Language, SiderealMode, Theme, ZodiacType


class SubjectBase(BaseModel):
    name: str = Field(..., example="Jane Doe")
    year: int = Field(..., ge=0, example=1990)
    month: int = Field(..., ge=1, le=12, example=6)
    day: int = Field(..., ge=1, le=31, example=15)
    hour: int = Field(..., ge=0, le=23, example=12)
    minute: int = Field(..., ge=0, le=59, example=30)
    city: Optional[str] = Field(None, example="New York")
    country: Optional[str] = Field(None, example="US")
    lat: Optional[float] = Field(None, example=40.7128)
    lng: Optional[float] = Field(None, example=-74.006)
    tz_str: Optional[str] = Field("UTC", example="UTC")

    houses_system: HouseSystem = Field(HouseSystem.placidus, example="P")
    zodiac_type: ZodiacType = Field(ZodiacType.tropic, example="Tropic")
    sidereal_mode: SiderealMode = Field(SiderealMode.lahiri, example="LAHIRI")
    theme: Theme = Field(Theme.classic, example="classic")
    language: Language = Field(Language.en, example="en")
    chart_language: Optional[Language] = Field(None, example="en")
    active_points: Optional[List[str]] = None


class ChartResponse(BaseModel):
    success: bool = True
    chart_type: str
    svg: str
    svg_base64: str
    data: dict
    generated_at: datetime
