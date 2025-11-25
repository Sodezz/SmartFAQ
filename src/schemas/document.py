from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SearchRequest(BaseModel):
    question: str


class SearchResponse(BaseModel):
    answer: str
    sources: List[str]


class DocumentRead(BaseModel):
    id: int
    filename: str
    content_document: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
