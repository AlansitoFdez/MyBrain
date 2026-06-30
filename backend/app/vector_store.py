from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.embedding import Embedding

model = SentenceTransformer("all-MiniLM-L6-v2")

def add_note(db: Session, note_id: int, text: str, user_id: int):
    embedding_vector = model.encode(text).tolist()

    existing = db.query(Embedding).filter(Embedding.source_id == note_id).first()

    if existing:
        existing.content = text
        existing.vector = embedding_vector
    else:
        new_embedding = Embedding(
            source_id=note_id,
            user_id=user_id,
            content=text,
            vector=embedding_vector
        )
        db.add(new_embedding)

    db.commit()

def delete_note(db: Session, note_id: int):
    db.query(Embedding).filter(Embedding.source_id == note_id).delete()
    db.commit()

def search_notes(db: Session, query: str, user_id: int, n_results: int = 5) -> list[str]:
    query_vector = model.encode(query).tolist()

    results = (
        db.query(Embedding)
        .filter(Embedding.user_id == user_id)
        .order_by(Embedding.vector.l2_distance(query_vector))
        .limit(n_results)
        .all()
    )

    return [r.content for r in results]