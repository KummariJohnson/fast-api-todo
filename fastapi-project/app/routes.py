# app/routes.py
from fastapi import APIRouter, HTTPException
from app.models import User, UserResponse
from app.crud import create_user, get_users, get_user, delete_user

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create(user: User):
    return await create_user(user)

@router.get("/users", response_model=list[UserResponse])
async def read_users():
    return await get_users()

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete(user_id: str):
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
    