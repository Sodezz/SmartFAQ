from bcrypt import gensalt, hashpw
from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.core.models.models as models
import app.core.schemas.user as user_schema
from app.core.services.check import user_exists


def get_user(db: Session, user_id: int) -> models.UserORM | None:
    """
    Получить одного пользователя по ID.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        user_id (int): идентификатор пользователя.
    Возвращает:
        UserORM | None: объект пользователя, или `None`, если пользователь не найден.
    """
    return db.query(models.UserORM).filter(models.UserORM.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Получить список пользователей с пагинацией.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        skip (int): сколько первых записей пропустить. По умолчанию 0.
        limit (int): максимальное число возвращаемых записей. По умолчанию 10.
    Возвращает:
        List[UserORM]: список объектов пользователей.
    """
    return db.query(models.UserORM).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate) -> models.UserORM:
    """
    Создать нового пользователя.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        user (UserCreate): Pydantic-схема с данными для создания пользователя:
            - username: str — логин пользователя.
            - email: EmailStr — электронная почта пользователя.
            - password: SecretStr - пароль пользователя.
    Возвращает:
        UserORM: созданный и сохраненный объект пользователя.
    """
    if user_exists(db, user.username, str(user.email)):
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким username или email уже существует.",
        )

    get_pass = user.password.get_secret_value().encode("utf8")
    hash_pass = hashpw(get_pass, gensalt())
    hash_pass_str = hash_pass.decode("utf8")

    db_user = models.UserORM(
        username=user.username, email=str(user.email), password=hash_pass_str
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> models.UserORM | None:
    """
    Удалить пользователя по ID.

    Аргументы:
        db (Session): сессия SQLAlchemy для работы с БД.
        user_id (int): идентификатор пользователя для удаления.
    Возвращает:
        UserORM | None: удаленный объект пользователя или `None`, если не найден.
    """
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
