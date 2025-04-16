from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr
)

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
