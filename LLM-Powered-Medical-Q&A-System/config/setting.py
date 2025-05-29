from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration for the Medical Q&A backend system.
    Includes token settings, app metadata, and DB/Redis connection.
    """

    # Environment: 'dev' or 'pro'
    ENVIRONMENT: Literal['dev', 'pro']

    # App metadata
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000
    FASTAPI_TITLE: str = 'Medical LLM Q&A'
    FASTAPI_VERSION: str = '0.1.0'
    FASTAPI_API_PREFIX: str = '/api'

    # MySQL Database
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # Token settings
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = ['*']

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
