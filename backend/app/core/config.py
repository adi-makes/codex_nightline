"""Typed, environment-backed application settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings that are safe to expose only where explicitly needed."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ASK_KOCHI_",
        extra="ignore",
    )

    app_name: str = "Ask Kochi API"
    environment: str = "development"
    version: str = "0.1.0"
    cors_origins: str = Field(default="")
    gemini_api_key: str | None = None
    generation_model: str = "gemini-3.1-flash-lite"
    max_generation_tokens: int = Field(default=512, ge=128, le=800)

    @property
    def allowed_cors_origins(self) -> list[str]:
        """Convert an optional comma-separated environment value into origins."""

        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return immutable process-level settings."""

    return Settings()
