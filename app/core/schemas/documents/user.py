from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)
from pydantic_core import PydanticCustomError

class User(BaseModel):
    """
    Базовая схема пользователя.

    Attributes:
        id: Уникальный идентификатор пользователя.
        username: Имя пользователя (3-30 символов, буквы/цифры/_).
        email: Валидный email-адрес.
    """
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        str_strip_whitespace=True
    )

    id: int = Field(..., description="Уникальный ID юзера", examples=[1])
    username: str = Field(
        ...,
        description="Имя пользователя",
        examples=["Puger", "Sodez"],
        min_length=3,
        max_length=20
    )
    email: EmailStr = Field(..., description="Почта пользователя", examples=["user@gmail.com"])

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        if value.lower() == "admin":
            raise PydanticCustomError("not_allowed_uesrname", "Username 'admin' запрещен")
        return value

class UserCreate(User):
    password: str = Field(..., min_length=3, max_length=20)