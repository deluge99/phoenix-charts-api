from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field("Phoenix Charts API", description="Service name")
    api_prefix: str = Field("/api/v1", description="API prefix")
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])


@lru_cache
def get_settings() -> Settings:
    return Settings()
