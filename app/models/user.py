import datetime
import hashlib
import jwt
from typing import Optional
from bson import ObjectId

from pydantic import Field, EmailStr
from app.models.base_model import BasicModel
from app.config import JWT_SECRET_KEY


class UserModel(BasicModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password_hash: bytes = Field(...)
    discord_id: Optional[int]
    disabled: Optional[bool]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    def verify_password(self, password):
        salt = self.password_hash[:32]
        key = self.password_hash[32:]
        if hashlib.pbkdf2_hmac("sha256",
                               password.encode('utf-8'), salt, 100000) == key:
            return True
        return False

    def get_jwt(self, expire_at: datetime.timedelta = datetime.timedelta(days=7)):
        payload = {
            "id": str(self.id),
            "exp": datetime.datetime.now() + expire_at
        }
        return jwt.encode(payload, str(JWT_SECRET_KEY), algorithm="HS256")
