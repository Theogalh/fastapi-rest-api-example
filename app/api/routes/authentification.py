from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from app.managers.user_manager import UserManager

from app.api.schemas.user import (
    UserIn,
    UserOut
)
from app.api.schemas.token import TokenResponse

from app.errors.exceptions import EmailAlreadyExists, LoginError

router = APIRouter()


@router.post("/register",
             response_description="user data added into the database",
             response_model=UserOut,
             status_code=201)
async def post_user(user: UserIn = Body(...)):
    user = jsonable_encoder(user)
    try:
        user = await UserManager.create(user)
        return user
    except EmailAlreadyExists:
        raise HTTPException(status_code=400, detail="User email already used")


@router.post("/login", response_description="get a token")
async def login(user_form: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await UserManager.login_user(user_form.username,
                                             user_form.password)
        return TokenResponse(access_token=token)
    except LoginError:
        raise HTTPException(status_code=403, detail="Not authorized")
