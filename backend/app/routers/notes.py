from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.note import Note
from app.schemas.note import NoteResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", response_model=List[NoteResponse])
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    return notes