from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text
)

from app.core.database.postgres.database import base

class DocumentBase(base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content_doc = Column(Text) #Хранение файла документа
    vector_doc = Column(Text)

class FAQ(base):
    __tablename__ = "FAQ"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    vector_store_doc = Column(Float) #Хранение вектора документа

