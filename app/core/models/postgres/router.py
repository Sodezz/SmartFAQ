from fastapi import APIRouter

from sqlalchemy import select

from core.database.postgres.database import async_session

from models import DocumentBase

router = APIRouter(prefix="/документы", tags=["Документы"])

@router.get("/documents", summary="Получить все документы")
async def get_all_documents():
    async with async_session() as session:
        query = select(DocumentBase)
        result = await session.execute(query)
        documents = result.scalars().all()
        return documents
