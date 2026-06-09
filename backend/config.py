"""Application settings and the shared OpenAI client.

We talk to an OpenAI-compatible gateway (NOT the Anthropic SDK). `base_url`,
`api_key`, and `model` all come from the environment.
"""

from functools import lru_cache

from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed configuration.

    Field names map to env vars case-insensitively, so `DATABASE_URL`,
    `LLM_API_KEY`, `BASE_URL`, and `MODEL_NAME` are read directly.
    """

    database_url: str = "postgresql+psycopg://meetmind:meetmind@localhost:5432/meetmind"
    llm_api_key: str = "sk-replace-me"
    base_url: str = "https://your-gateway.example.com/v1"
    model_name: str = "claude-opus-4-6"

    # CORS origins for the Vite dev server.
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings (read once per process)."""
    return Settings()


@lru_cache
def get_client() -> OpenAI:
    """Return the shared OpenAI-compatible client.

    Pointed at `BASE_URL`. Do NOT use `response_format` json mode with this
    gateway — parse JSON out of the text response instead (see BaseAgent).
    """
    settings = get_settings()
    return OpenAI(api_key=settings.llm_api_key, base_url=settings.base_url)
