from typing import Optional

from sqlalchemy import (
    String,
    Text
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

class BaseSQL(DeclarativeBase): 
    pass

class UserBase(BaseSQL):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(14), nullable=False)
    hashed_pass: Mapped[str] = mapped_column(String(32), nullable=False)

class Document(BaseSQL):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(100), nullable=False)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)

