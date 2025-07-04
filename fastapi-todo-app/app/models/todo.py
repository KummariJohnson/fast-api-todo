"""Todo data models and schemas."""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from bson import ObjectId


class TodoStatus(str, Enum):
    """Enumeration for todo status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    """Enumeration for todo priority values."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TodoBase(BaseModel):
    """Base todo model with common fields."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    status: TodoStatus = Field(default=TodoStatus.PENDING, description="Todo status")
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM, description="Todo priority")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo")


class TodoCreate(TodoBase):
    """Schema for creating a new todo."""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    status: Optional[TodoStatus] = Field(None, description="Todo status")
    priority: Optional[TodoPriority] = Field(None, description="Todo priority")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo")


class TodoInDB(TodoBase):
    """Todo model as stored in database."""
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TodoResponse(TodoBase):
    """Schema for todo API responses."""
    
    id: str = Field(..., description="Todo ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema for paginated todo list responses."""
    
    todos: list[TodoResponse] = Field(..., description="List of todos")
    total: int = Field(..., description="Total number of todos")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
