from pydantic import BaseModel

from app.schemas.subject import SubjectInput


class SynastryRequest(BaseModel):
    first: SubjectInput
    second: SubjectInput
    theme: str = "dark-high-contrast"
