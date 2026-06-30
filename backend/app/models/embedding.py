from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector
from app.database import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    content = Column(String, nullable=False)
    vector = Column(Vector(384), nullable=False)