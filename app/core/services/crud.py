from sqlalchemy.orm import Session

import app.core.models.models as models
import app.core.schemas.user as user_schema


def get_user(db: Session, user_id: int):
    """
    Получить одного пользователя по ID.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        user_id (int): идентификатор пользователя.
    """
    return db.query(models.UserBase).filter(models.UserBase.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Получить список пользователей с пагинацией.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        skip (int): сколько первых записей пропустить. По умолчанию 0.
        limit (int): максимальное число возвращаемых записей. По умолчанию 10.
    """
    return db.query(models.UserBase).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    """
    Создать нового пользователя.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        user (UserCreate): Pydantic-схема с данными для создания пользователя:
            - username: str — логин пользователя.
            - email: EmailStr — электронная почта пользователя.
            - password: SecretStr - пароль пользователя. ( добавить)
    """
    db_user = models.UserBase(username=user.username, email=str(user.email))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
    Удалить пользователя по ID.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        user_id (int): идентификатор пользователя для удаления.
    """
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
