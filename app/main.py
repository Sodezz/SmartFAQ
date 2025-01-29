from fastapi import FastAPI

from app.core.services.uploading_document import upload_documents
from app.core.services.creating_document import create_document
from app.core.schemas.documents.documents import Document

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post(
    "/documents/" ,
        tags=["Документы"],
        summary="Документы",
        response_model=Document
)

async def create_document():
    await create_document()


@app.post(
    "/upload",
    tags=["Документы"],
    summary="Загрузка документов"
)

async def upload_document():
    await upload_documents()