from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

class DocumentRead(BaseModel):
    id: int
    user_id: int
    filename: str
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }

class DocumentUpload(BaseModel):
    filename: Annotated[str, Field(..., examples=["document.pdf"])]