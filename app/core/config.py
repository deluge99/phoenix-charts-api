from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Phoenix Charts API"
    version: str = "0.1.0"


settings = Settings()

# Backwards-compatible constants
API_TITLE = settings.app_name
API_VERSION = settings.version
