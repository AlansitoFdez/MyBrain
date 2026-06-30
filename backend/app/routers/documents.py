from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.auth_service import get_current_user
from app.services.document_service import extract_text_from_pdf, extract_text_from_url
from app import vector_store

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/pdf", response_model=DocumentResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from PDF"
        )

    document = Document(
        title=file.filename,
        source=file.filename,
        source_type="pdf",
        user_id=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    vector_store.add_note(db, document.id, text, current_user.id)

    return document

@router.post("/url", response_model=DocumentResponse)
async def upload_url(
    url: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        text = extract_text_from_url(url)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from URL"
        )

    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text content found at URL"
        )

    document = Document(
        title=url,
        source=url,
        source_type="url",
        user_id=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    vector_store.add_note(db, document.id, text, current_user.id)

    return document

@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()
    return documents

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()

    vector_store.delete_note(db, document_id)

    return {"message": "Document deleted successfully"}