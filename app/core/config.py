from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "pharmaco-api"
    redis_url: Optional[str] = None
    health_timeout: float = 1.0
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_name: str = "pharmaco"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

