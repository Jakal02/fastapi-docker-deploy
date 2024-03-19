"""Main for Simple App."""

from fastapi import FastAPI, HTTPException
from app.database import SessionDep, SearchDep
from app.models import Post


app = FastAPI()

@app.get("/")
def root_of_app():
    return {"message": "Hello World! 3"}

@app.get("/num_posts")
def get_num_posts(db: SessionDep):
    try:
        num = db.query(Post).count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
    return {"message": f"number of posts is {num}"}

@app.get("/meili_health")
def get_meili_health(client: SearchDep):
    try:
        return {"message": client.health()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
