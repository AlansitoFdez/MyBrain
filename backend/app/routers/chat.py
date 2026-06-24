from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.chat_service import chat_with_notes

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    response = chat_with_notes(request.query, current_user.id)
    return ChatResponse(response=response)