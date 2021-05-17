import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.managers.user_manager import UserManager
from app.config import JWT_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(JWT_SECRET_KEY), algorithms=["HS256"])
        id = payload['id']
        user = await UserManager.get(id)
        if not user:
            raise credentials_exception
        return user
    except jwt.PyJWTError:
        raise credentials_exception


async def get_current_actif_user(current_user: UserManager.model = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
