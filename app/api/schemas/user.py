from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from copy import deepcopy


class ConfigUser:
    schema_extra = {
        "example": {
            "username": "totodu34",
            "email": "totodu34@x.edu.ng",
            "discord_id": "132213134223"
        }
    }


class UserIn(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    discord_id: Optional[int]
    password: str = Field(...)

    class Config(ConfigUser):
        schema_extra = deepcopy(ConfigUser.schema_extra)
        schema_extra['example']['password'] = "qwerty1234"


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    discord_id: Optional[int]
    password: Optional[str]

    class Config(ConfigUser):
        schema_extra = deepcopy(ConfigUser.schema_extra)
        schema_extra['example']['password'] = "qwerty1234"


class UserOut(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    discord_id: Optional[int]

    class Config(ConfigUser):
        pass
