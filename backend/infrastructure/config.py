"""
Application configuration.
All configuration is loaded from environment variables with sensible defaults.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    app_name: str = "Trimgram - Instagram Follower Analyzer"
    api_version: str = "1.0.0"
    debug: bool = False

    # CORS Configuration
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")

    # Session Configuration
    session_ttl_seconds: int = int(os.getenv("SESSION_TTL_SECONDS", "1800"))  # 30 minutes

    # Instagram API Configuration
    instagram_request_delay: float = float(os.getenv("INSTAGRAM_REQUEST_DELAY", "2.0"))

    # Analysis Configuration
    max_non_followers_shown: int = int(os.getenv("MAX_NON_FOLLOWERS_SHOWN", "100"))
    posts_to_analyze: int = int(os.getenv("POSTS_TO_ANALYZE", "12"))

    # Unfollow Configuration
    unfollow_delay_seconds: float = float(os.getenv("UNFOLLOW_DELAY_SECONDS", "15.0"))

    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False

    def get_cors_origins_list(self) -> list:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
