from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine, engine

from app.config import settings


engine = create_engine(
    settings.get_uri_to_make_sqlalchemy_engine(),
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
