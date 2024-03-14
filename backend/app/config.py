from typing import Any

from pydantic import PositiveInt, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Settings for this API.

    Modified from: https://stackoverflow.com/a/77506150
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    POSTGRES_SERVER: str | None = None
    POSTGRES_SERVER_PORT: PositiveInt | None = 5432
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None | str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        """Create the database connection URI from .env variables."""
        if isinstance(v, str):
            print("Loading SQLALCHEMY_DATABASE_URI from .docker.env file ...")  # noqa: T201
            return v
        print("Creating SQLALCHEMY_DATABASE_URI from .env file ...")  # noqa: T201
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=values.data.get("POSTGRES_SERVER_PORT"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    def get_db_uri_string(self) -> str:
        """Return the string format of the database URI."""
        return self.SQLALCHEMY_DATABASE_URI.unicode_string()


settings = APISettings()
