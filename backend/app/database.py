from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, engine

from app.config import settings


if settings.NODE == "production":
    # copied from: https://cloud.google.com/sql/docs/postgres/connect-run#connect-unix-socket

    def connect_unix_socket() -> Engine:
        """Initializes a Unix socket connection pool for a Cloud SQL instance of Postgres."""
        # Note: Saving credentials in environment variables is convenient, but not
        # secure - consider a more secure solution such as
        # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
        # keep secrets safe.
        db_user = settings.POSTGRES_USER  # e.g. 'my-database-user'
        db_pass = settings.POSTGRES_PASSWORD  # e.g. 'my-database-password'
        db_name = settings.POSTGRES_DB  # e.g. 'my-database'
        unix_socket_path = settings.INSTANCE_UNIX_SOCKET # e.g. '/cloudsql/project:region:instance'

        pool = create_engine(
            # Equivalent URL:
            # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
            #                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
            # Note: Some drivers require the `unix_sock` query parameter to use a different key.
            # For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
            engine.url.URL.create(
                drivername="postgresql+psycopg2",
                username=db_user,
                password=db_pass,
                database=db_name,
                query={"host": f"{unix_socket_path}/.s.PGSQL.5432"},
            ),
            # ...
            # connect_args={
            # }
        )
        return pool
    engine = connect_unix_socket()

else:
    engine = create_engine(
        settings.get_db_uri_string(),
        # connect_args={
        #     "check_same_thread": False,
        # }
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]
