from pydantic import BaseModel, EmailStr, SecretStr, Field, field_validator
from pydantic_core import PydanticCustomError
from typing import Annotated


class UserRead(BaseModel):
    id: Annotated[int, Field(..., gt=0)]
    username: Annotated[
        str,
        Field(
            min_length=3, max_length=20, examples=["Sodez"], pattern=r"^[a-zA-Z0-9_]+$"
        ),
    ]
    email: Annotated[EmailStr, Field(..., examples=["sodez@gmail.com"])]

    @field_validator("username")
    def check_username(cls, username: str) -> str:
        if username.lower() == "admin":
            raise PydanticCustomError("bad_username", f"{username} - недопустимое имя!")
        return username

    model_config = {
        "from_attributes": True,
        "frozen": True,
        "str_strip_whitespace": True,
        "extra": "forbid"
    }

class UserCreate(BaseModel):
    username: Annotated[
        str,
        Field(
            min_length=3, max_length=20, examples=["Sodez"], pattern=r"^[a-zA-Z0-9_]+$"
        ),
    ]
    email: Annotated[EmailStr, Field(..., examples=["sodez@gmail.com"])]
    password: Annotated[SecretStr, Field(..., min_length=4)]

    @field_validator("username")
    def check_username(cls, username: str) -> str:
        if username.lower() == "admin":
            raise PydanticCustomError("bad_username", f"{username} - недопустимое имя!")
        return username
    