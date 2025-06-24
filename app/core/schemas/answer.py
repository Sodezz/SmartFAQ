from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

class AnswerChunk(BaseModel):
    document_id: int
    content: str
    score: float
    document_text: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    source: list[AnswerChunk]