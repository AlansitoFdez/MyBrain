from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    title: str
    source: str
    source_type: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}