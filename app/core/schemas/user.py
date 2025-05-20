from pydantic import (BaseModel, ConfigDict, EmailStr, Field, SecretStr,
                      field_validator)
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
        from_attributes=True, frozen=True, str_strip_whitespace=True
    )

    id: int = Field(..., description="Уникальный ID юзера", examples=[1])
    username: str = Field(
        ...,
        description="Имя пользователя",
        examples=["Puger", "Sodez"],
        min_length=3,
        max_length=20,
    )
    email: EmailStr = Field(
        ..., description="Почта пользователя", examples=["user@gmail.com"]
    )

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        """
        Валидатор поля username.

        Запрещает использовать имя 'admin' (в любом регистре).
        Обрезает пробелы и проверяет длину/символы через Field.
        """
        if value.lower() == "admin":
            raise PydanticCustomError(
                "not_allowed_username", "Username 'admin' запрещен"
            )
        return value


class UserCreate(User):
    """
    Схема для создания нового пользователя.

    Наследует все поля из User, плюс:
    - password: защищённая строка (минимум 6 символов).
    """

    password: SecretStr = Field(
        ...,
        description="Пароль пользователя",
        examples=["<PASSWORD>"],
        min_length=6,
    )
