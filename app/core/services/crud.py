from sqlalchemy.orm import Session
from app.core.models.postgres.models import DocumentBase
from schemas.documents.documents import DocumentCreate
from services.vectorize_document import vectorized_document, cosine_similarity


def create_document(db: Session, document: DocumentCreate):
    vector = vectorized_document(document.content)
    db_document = DocumentBase(title=document.title, content_doc=document.content, vector_doc=vector)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, id: int):
    return db.query(DocumentBase).filter(DocumentBase.id == id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DocumentBase).offset(skip).limit(limit).all()
