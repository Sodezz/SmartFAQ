from pydantic import BaseModel

class DocumentUpload(BaseModel):
    filename: str