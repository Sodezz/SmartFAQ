from sqlalchemy import String, Integer, ForeignKey, DateTime, func, Text, Float
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

# Базовый класс для всех ORM-моделей
Base = declarative_base()


class UserORM(Base):
    """
    ORM-модель пользователя.

    Представляет таблицу "user_account" в базе данных PostgreSQL.

    Attributes:
        id (int): Уникальный идентификатор пользователя, первичный ключ, автоинкремент.
        username (str): Логин пользователя (до 14 символов), обязательное поле.
        email (str): Адрес электронной почты пользователя, обязательное поле.
        password (str): Пароль пользователя
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer ,primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    documents: Mapped[list["Document"]] = relationship(back_populates="user")
    questions: Mapped[list["Question"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"UserORM(id={self.id}, username={self.username}, email={self.email})"

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(255))
    uploaded_at: Mapped[DateTime] = mapped_column(default=func.now())

    user: Mapped["UserORM"] = relationship(back_populates="documents")
    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document", cascade="all, delete")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column()
    score: Mapped[float] = mapped_column(Float, default=0.0)

    document: Mapped["Document"] = relationship(back_populates="chunks")

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    question_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(default=func.now())

    user: Mapped["UserORM"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="questions", cascade="all, delete")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"))
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"))

    score: Mapped[float] = mapped_column()
    answer_text: Mapped[str] = mapped_column(Text)
    source_excerpt: Mapped[str] = mapped_column(Text)

    question: Mapped["Question"] = relationship(back_populates="answers")
    document: Mapped["Document"] = relationship()

