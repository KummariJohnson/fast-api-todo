"""Todo repository for database operations."""

from datetime import datetime
from typing import List, Optional
from math import ceil

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING

from app.core.config import settings
from app.models.todo import TodoCreate, TodoUpdate, TodoInDB, TodoStatus, TodoPriority


class TodoRepository:
    """Repository class for todo database operations."""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize the todo repository.
        
        Args:
            database: MongoDB database instance.
        """
        self.database = database
        self.collection = database[settings.todos_collection]
    
    async def create_todo(self, todo_data: TodoCreate) -> TodoInDB:
        """
        Create a new todo in the database.
        
        Args:
            todo_data: Todo creation data.
            
        Returns:
            TodoInDB: The created todo with database fields.
        """
        now = datetime.utcnow()
        todo_dict = todo_data.dict()
        todo_dict.update({
            "created_at": now,
            "updated_at": now
        })
        
        result = await self.collection.insert_one(todo_dict)
        
        # Retrieve the created todo
        created_todo = await self.collection.find_one({"_id": result.inserted_id})
        return TodoInDB(**created_todo)
    
    async def get_todo_by_id(self, todo_id: str) -> Optional[TodoInDB]:
        """
        Retrieve a todo by its ID.
        
        Args:
            todo_id: The todo ID to search for.
            
        Returns:
            TodoInDB or None: The todo if found, None otherwise.
        """
        if not ObjectId.is_valid(todo_id):
            return None
            
        todo = await self.collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            return TodoInDB(**todo)
        return None
    
    async def get_todos(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> tuple[List[TodoInDB], int]:
        """
        Retrieve todos with filtering, sorting, and pagination.
        
        Args:
            skip: Number of todos to skip.
            limit: Maximum number of todos to return.
            status: Filter by todo status.
            priority: Filter by todo priority.
            sort_by: Field to sort by.
            sort_order: Sort order (asc or desc).
            
        Returns:
            tuple: List of todos and total count.
        """
        # Build filter query
        filter_query = {}
        if status:
            filter_query["status"] = status
        if priority:
            filter_query["priority"] = priority
        
        # Build sort query
        sort_direction = DESCENDING if sort_order.lower() == "desc" else ASCENDING
        sort_query = [(sort_by, sort_direction)]
        
        # Get total count
        total = await self.collection.count_documents(filter_query)
        
        # Get todos with pagination
        cursor = self.collection.find(filter_query).sort(sort_query).skip(skip).limit(limit)
        todos = []
        async for todo in cursor:
            todos.append(TodoInDB(**todo))
        
        return todos, total
    
    async def update_todo(self, todo_id: str, todo_data: TodoUpdate) -> Optional[TodoInDB]:
        """
        Update an existing todo.
        
        Args:
            todo_id: The ID of the todo to update.
            todo_data: The update data.
            
        Returns:
            TodoInDB or None: The updated todo if found, None otherwise.
        """
        if not ObjectId.is_valid(todo_id):
            return None
        
        # Build update query with only provided fields
        update_data = {k: v for k, v in todo_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_todo_by_id(todo_id)
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_todo_by_id(todo_id)
        return None
    
    async def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo by its ID.
        
        Args:
            todo_id: The ID of the todo to delete.
            
        Returns:
            bool: True if the todo was deleted, False otherwise.
        """
        if not ObjectId.is_valid(todo_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(todo_id)})
        return result.deleted_count > 0
    
    async def get_todos_by_status(self, status: TodoStatus) -> List[TodoInDB]:
        """
        Get all todos with a specific status.
        
        Args:
            status: The status to filter by.
            
        Returns:
            List[TodoInDB]: List of todos with the specified status.
        """
        cursor = self.collection.find({"status": status})
        todos = []
        async for todo in cursor:
            todos.append(TodoInDB(**todo))
        return todos
    
    async def get_overdue_todos(self) -> List[TodoInDB]:
        """
        Get all overdue todos.
        
        Returns:
            List[TodoInDB]: List of overdue todos.
        """
        now = datetime.utcnow()
        cursor = self.collection.find({
            "due_date": {"$lt": now},
            "status": {"$ne": TodoStatus.COMPLETED}
        })
        todos = []
        async for todo in cursor:
            todos.append(TodoInDB(**todo))
        return todos
