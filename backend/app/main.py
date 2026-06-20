from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import auth, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyBrain API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "MyBrain API is running"}