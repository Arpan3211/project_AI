from pydantic import BaseSettings
from typing import List
import os
from pathlib import Path

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "AI Chat API"
    PROJECT_DESCRIPTION: str = "API for AI Chat Application"
    PROJECT_VERSION: str = "0.1.0"

    # API settings
    API_PREFIX: str = "/api"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*", "http://localhost:8000", "http://localhost:3000", "file://", "null"]

    # Database settings
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/app/db/chat.db"

    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"  # In production, use a secure key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
