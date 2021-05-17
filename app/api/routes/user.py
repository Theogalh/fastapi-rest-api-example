from fastapi import APIRouter, Body, HTTPException
from pydantic.types import List
from app.managers.user_manager import UserManager

from app.api.schemas.user import (
    UserUpdate,
    UserOut
)

router = APIRouter()


@router.get("/", response_description="users retrieved",
            response_model=List[UserOut])
async def get_users():
    users = await UserManager.get_all()
    return users


@router.get("/{object_id}", response_description="user data retrieved",
            response_model=UserOut)
async def get_user(object_id):
    user = await UserManager.get(object_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/{object_id}", response_model=UserOut)
async def update_user_data(object_id: str, req: UserUpdate = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated = await UserManager.update(object_id, req)
    if updated:
        return await UserManager.get(object_id)
    raise HTTPException(
        status_code=400,
        detail="An error occurred",
    )


@router.delete("/{object_id}",
               response_description="user data deleted from the database")
async def delete_user_data(object_id: str):
    # TODO : Authorize only for Admin.
    deleted_user = await UserManager.delete(object_id)
    if deleted_user:
        return {"message": f"User {object_id} deleted"}
    raise HTTPException(status_code=404, detail="User not found")
