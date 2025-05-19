from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import User
from app.core.services import crud
from app.core.database.postgres.database import get_db

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get(
    "/get_users", response_model=list[User], summary="Получение списка пользователей"
)
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.delete("/delete_user/{user_id}", summary="Удаление пользователя по id")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    users = crud.delete_user(db=db, user_id=user_id)
    return users
