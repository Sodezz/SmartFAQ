from pydantic import BaseModel, Field
from typing import Annotated


class QuestionCreate(BaseModel):
    question_text: Annotated[str, Field(..., min_length=6, max_length=200, examples=["Что такое Python?"])]
    document_ids: list[int] | None