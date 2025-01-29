from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.core.database.postgres.database import Base

class DocumentBase(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author = Column(String)

