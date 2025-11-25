from typing import List, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    documents: Mapped[List["Document"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"<User id: {self.id}, username: {self.username}>"

    def __str__(self) -> str:
        return self.username


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_document: Mapped[Optional[str]] = mapped_column(Text)
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(768))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="documents")

    def __repr__(self) -> str:
        return f"<Document id: {self.id}, filename: {self.filename}>"
