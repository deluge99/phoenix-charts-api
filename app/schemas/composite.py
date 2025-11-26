from pydantic import BaseModel

from app.schemas.subject import SubjectInput


class CompositeRequest(BaseModel):
    first: SubjectInput
    second: SubjectInput
    theme: str = "dark-high-contrast"
