from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.chat_service import chat_with_notes, chat_with_notes_stream
import json
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    response = chat_with_notes(request.query, current_user.id, db)
    return ChatResponse(response=response)

@router.post("/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    def generate():
        for chunk in chat_with_notes_stream(request.query, current_user.id, db):
            data = json.dumps({"chunk": chunk})
            yield f"data: {data}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")