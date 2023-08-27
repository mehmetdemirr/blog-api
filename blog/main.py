from fastapi import FastAPI
from blog import models
from .database import engine
from .router import blog,user,auth

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(
    user.router,
    tags=["User",],
    prefix="/user"
    )
app.include_router(
    blog.router,
    tags=["Blog",],
    prefix="/blog"
    )
app.include_router(
    auth.router,
    tags=["Auth",],
    prefix=""
    )

@app.get("/")
def index():
    return {"message":"restart"}
