from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///./my_app.db",
    connect_args={
        "check_same_thread": False,
    }
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
