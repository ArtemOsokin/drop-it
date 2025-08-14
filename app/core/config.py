from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    APP_HOST: str = "localhost"
    APP_PORT: int = 32165

    ENV: Literal["local", "dev", "prod"] = "local"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str = "your-super-secret-key"
    ALGORITHM: str = "HS256"

    LOG_LEVEL: str = 'DEBUG'
    LOG_PATH: str = 'logs/app.log'

    # DB Settings
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'postgres'
    POSTGRES_URI: str = 'postgresql+psycopg2://postgres:postgres@localhost:5433/postgres'

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:  # pylint: disable=C0103
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()
