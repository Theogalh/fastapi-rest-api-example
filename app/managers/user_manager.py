import hashlib
import os

from app.models.user import UserModel
from app.managers.generic_manager import GenericManager
from app.database import db
from app.errors.exceptions import EmailAlreadyExists, LoginError


def generate_hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key


class UserManager(GenericManager):

    model = UserModel

    collection = db.get_collection("users")

    @classmethod
    def get_by_token(cls, token):
        return cls.collection.find_one()

    @classmethod
    async def create(cls, data):
        if await cls.collection.find_one({"email": data['email']}):
            raise EmailAlreadyExists
        data["password_hash"] = generate_hash_password(data['password'])
        del data['password']
        return await super().create(data)

    @classmethod
    async def update(cls, object_id, data) -> bool:
        password = data.get('password', None)
        if password:
            data['password_hash'] = generate_hash_password(password)
            del data['password']
        return await super().update(object_id, data)

    @classmethod
    async def login_user(cls, username, password) -> str:
        user_data = await cls.collection.find_one({"username": username})
        if user_data:
            user = cls.model(**user_data)
        if not user_data or not user.verify_password(password):
            raise LoginError
        # By default a JWT is valid 7 days.
        return user.get_jwt()
