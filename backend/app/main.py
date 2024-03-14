"""Main for Simple App."""

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root_of_app():
    return {"message": "Hello World! 2"}
