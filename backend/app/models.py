from sqlalchemy import Column, Integer, String

from app.database import Base

class Post(Base):
    """Post table definition."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    body = Column(String, nullable=False)
