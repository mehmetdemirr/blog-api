from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return {"message":"root"}

@app.get("/about")
def about():
    return {"message":"about"}