from sqlalchemy.orm import Session

import app.core.models.models as models


def user_exists(db: Session, username: str, email: str) -> bool:
    """
    Проверяет, существует ли в базе пользователь с данным именем пользователя или электронной почтой.

    Аргументы:
        db (Session): сессия SQLAlchemy для доступа к базе данных.
        username (str): имя пользователя для проверки.
        email (str): адрес электронной почты для проверки.

    Возвращает:
        bool: True, если пользователь с таким username или email уже есть в БД, иначе False.
    """
    return (
        db.query(models.UserORM).filter(models.UserORM.username == username)
        or (models.UserORM.email == email).first() is not None
    )
