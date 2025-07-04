# app/models.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr

class UserResponse(User):
    id: str