from fastapi import FastAPI, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_database

from app.models import basemodel, Document

import os


app = FastAPI()

upload_folder = "uploaded_documents"
os.makedirs(upload_folder, exist_ok=True)

basemodel.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/documents/")
def create_document(id: int, name: str, database: Session = Depends(get_database)):
    document = Document(id=id, name=name)
    database.add(document)
    database.commit()
    database.refresh(document)
    return document

@app.post("/upload")
async def upload_documents(file: UploadFile):
    file_path = os.path.join(upload_folder, file.filename)
    try:
        with open(file_path, "wb") as f:
            content_read = await file.read()
            f.write(content_read)
            return {"filename": file.filename, "message": "Документ успешно загружен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {e}")