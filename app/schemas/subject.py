from pydantic import BaseModel


class SubjectInput(BaseModel):
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    lat: float
    lng: float
    tz_str: str
    city: str
    country: str
