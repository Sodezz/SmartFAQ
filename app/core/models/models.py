from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

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

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(14), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
