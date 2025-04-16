from SmartFAQ.app.main import app
from SmartFAQ.app.handlers.users import get_user_id
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Пользователи"])

@app.get("/{user_id}")
async def get_user(user_id: int):
    return await get_user_id(user_id)
