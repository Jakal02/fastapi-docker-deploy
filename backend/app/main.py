"""Main for Simple App."""

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from app.database import SessionDep
from app.models import Post


app = FastAPI()

@app.get("/")
def root_of_app():
    return {"message": "Hello World! 2"}

@app.get("/num_posts")
def get_num_posts(db: SessionDep):
    try:
        num = db.query(Post).count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
    return {"message": f"number of posts is {num}"}
