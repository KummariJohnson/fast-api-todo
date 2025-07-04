# app/crud.py
from app.database import user_collection
from app.models import User
from bson import ObjectId

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

async def create_user(user: User) -> dict:
    new_user = await user_collection.insert_one(user.dict())
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

async def get_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

async def get_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    return user_helper(user) if user else None

async def delete_user(id: str):
    result = await user_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0