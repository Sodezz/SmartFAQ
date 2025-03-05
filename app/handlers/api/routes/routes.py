"""from main import app
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database.postgres.database import get_db
from app.core.services import crud
from schemas.documents.documents import DocumentCreate, DocumentResponse, QuestionRequest


@app.post("/documents/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db())):
    return crud.create_document(document=document, db=db)

@app.get("/documents/{document_id}", response_model=DocumentResponse)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Документ не найден")
    return db_document

@app.post("/ask/")
def ask_question(question: QuestionRequest, db: Session = Depends(get_db)):
    return {"question": question.question, "answer": question.answer}

"""