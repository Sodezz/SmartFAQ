from fastapi import APIRouter

from sqlalchemy import select

from app.core.database.postgres.database import session



router = APIRouter(tags=["Документы"])

@router.get("/documents", summary="Получить все документы")
def get_all_documents():
        pass
