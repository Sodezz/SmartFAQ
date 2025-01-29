from app.core.database.postgres.database import get_database
from app.core.models.postgres.models import DocumentBase

from sqlalchemy.orm import Session

from fastapi import Depends

async def create_document(id: int, name: str, database: Session = Depends(get_database)):
    document = DocumentBase(id=id, name=name)
    database.add(document)
    database.commit()
    database.refresh(document)
    return document