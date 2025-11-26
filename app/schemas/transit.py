from pydantic import BaseModel

from app.schemas.subject import SubjectInput


class TransitRequest(BaseModel):
    natal: SubjectInput
    transit: SubjectInput
    theme: str = "dark-high-contrast"
