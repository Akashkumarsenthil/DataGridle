from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "DataGridle"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "postgresql+asyncpg://datagridle:datagridle@localhost:5432/datagridle"
    DATABASE_URL_SYNC: str = "postgresql://datagridle:datagridle@localhost:5432/datagridle"

    REDIS_URL: str = "redis://localhost:6379/0"

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
