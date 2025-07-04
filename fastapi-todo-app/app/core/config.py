"""Application configuration settings."""

import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings configuration."""
    
    # Application settings
    app_name: str = "FastAPI Todo App"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "todo_app"
    
    # Collection names
    todos_collection: str = "todos"
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
