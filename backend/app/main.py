from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import auth, notes, chat, documents

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyBrain API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(chat.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {"message": "MyBrain API is running"}