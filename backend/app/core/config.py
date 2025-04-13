from typing import List
import os
from pathlib import Path

# Try to import from pydantic-settings if available, otherwise use pydantic v1 style
try:
    from pydantic_settings import BaseSettings
    from pydantic import field_validator
    PYDANTIC_V2 = True
except ImportError:
    try:
        from pydantic import BaseSettings
        from pydantic import validator
        PYDANTIC_V2 = False
    except ImportError:
        raise ImportError("Please install either pydantic<2.0.0 or pydantic-settings package")

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "AI Chat API"
    PROJECT_DESCRIPTION: str = "API for AI Chat Application with HR Analytics"
    PROJECT_VERSION: str = "0.2.0"

    # API settings
    API_PREFIX: str = "/api"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*", "http://localhost:8000", "http://localhost:3000", "file://", "null"]

    # Database settings
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/app/db/chat.db"
    HR_DATABASE_URL: str = f"sqlite:///{BASE_DIR}/app/db/hrattri_new.db"

    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"  # In production, use a secure key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Azure OpenAI settings
    API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""

    # Configure environment variables
    if PYDANTIC_V2:
        model_config = {"env_file": ".env"}
    else:
        class Config:
            env_file = ".env"


settings = Settings()
