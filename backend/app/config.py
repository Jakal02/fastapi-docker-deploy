from typing import Any, Literal

from sqlalchemy.engine.url import URL

from pydantic import PositiveInt, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Settings for this API.

    Modified from: https://stackoverflow.com/a/77506150
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    NODE: Literal["development","production", None] = "development"

    POSTGRES_SERVER: str | None = None
    POSTGRES_SERVER_PORT: PositiveInt | None = 5432
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None | str | None = None

    # GCP Cloud SQL Unix Connection
    INSTANCE_UNIX_SOCKET: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        """Create the database connection URI from .env variables."""
        if values.data.get("NODE") == "production":
            print("Creating SQLALCHEMY_DATABASE_URI from GCP Secrets...") # noqa T201
            return cls._create_prod_db_url(cls, values)
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
    
    def _create_prod_db_url(self, values: ValidationInfo) -> str:
        """Initializes a Unix socket connection pool for a Cloud SQL instance of Postgres."""
        # copied from: https://cloud.google.com/sql/docs/postgres/connect-run#connect-unix-socket
        # Note: Saving credentials in environment variables is convenient, but not
        # secure - consider a more secure solution such as
        # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
        # keep secrets safe.
        db_user = values.data.get("POSTGRES_USER")  # e.g. 'my-database-user'
        db_pass = values.data.get("POSTGRES_PASSWORD")  # e.g. 'my-database-password'
        db_name = values.data.get("POSTGRES_DB")  # e.g. 'my-database'
        unix_socket_path = values.data.get("INSTANCE_UNIX_SOCKET") # e.g. '/cloudsql/project:region:instance'

        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
        # Note: Some drivers require the `unix_sock` query parameter to use a different key.
        # For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
        return URL.create(
                drivername="postgresql+psycopg2",
                username=db_user,
                password=db_pass,
                database=db_name,
                query={"host": f"{unix_socket_path}/.s.PGSQL.5432"},
            )


settings = APISettings()
