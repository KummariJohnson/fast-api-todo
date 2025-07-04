"""Todo business logic service."""

from typing import List, Optional
from math import ceil

from app.core.database import get_database
from app.repositories.todo_repository import TodoRepository
from app.models.todo import (
    TodoCreate, 
    TodoUpdate, 
    TodoResponse, 
    TodoListResponse,
    TodoStatus, 
    TodoPriority
)


class TodoService:
    """Service class for todo business logic."""
    
    def __init__(self):
        """Initialize the todo service."""
        self.database = get_database()
        self.repository = TodoRepository(self.database)
    
    async def create_todo(self, todo_data: TodoCreate) -> TodoResponse:
        """
        Create a new todo.
        
        Args:
            todo_data: Todo creation data.
            
        Returns:
            TodoResponse: The created todo.
        """
        todo_in_db = await self.repository.create_todo(todo_data)
        return self._convert_to_response(todo_in_db)
    
    async def get_todo(self, todo_id: str) -> Optional[TodoResponse]:
        """
        Get a todo by ID.
        
        Args:
            todo_id: The todo ID.
            
        Returns:
            TodoResponse or None: The todo if found, None otherwise.
        """
        todo_in_db = await self.repository.get_todo_by_id(todo_id)
        if todo_in_db:
            return self._convert_to_response(todo_in_db)
        return None
    
    async def get_todos(
        self,
        page: int = 1,
        size: int = 10,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> TodoListResponse:
        """
        Get todos with filtering, sorting, and pagination.
        
        Args:
            page: Page number (1-based).
            size: Page size.
            status: Filter by status.
            priority: Filter by priority.
            sort_by: Field to sort by.
            sort_order: Sort order (asc or desc).
            
        Returns:
            TodoListResponse: Paginated list of todos.
        """
        # Calculate skip value
        skip = (page - 1) * size
        
        # Get todos and total count
        todos_in_db, total = await self.repository.get_todos(
            skip=skip,
            limit=size,
            status=status,
            priority=priority,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Convert to response format
        todos = [self._convert_to_response(todo) for todo in todos_in_db]
        
        # Calculate total pages
        pages = ceil(total / size) if total > 0 else 1
        
        return TodoListResponse(
            todos=todos,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    async def update_todo(self, todo_id: str, todo_data: TodoUpdate) -> Optional[TodoResponse]:
        """
        Update a todo.
        
        Args:
            todo_id: The todo ID.
            todo_data: Update data.
            
        Returns:
            TodoResponse or None: The updated todo if found, None otherwise.
        """
        todo_in_db = await self.repository.update_todo(todo_id, todo_data)
        if todo_in_db:
            return self._convert_to_response(todo_in_db)
        return None
    
    async def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo.
        
        Args:
            todo_id: The todo ID.
            
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        return await self.repository.delete_todo(todo_id)
    
    async def get_todos_by_status(self, status: TodoStatus) -> List[TodoResponse]:
        """
        Get todos by status.
        
        Args:
            status: The status to filter by.
            
        Returns:
            List[TodoResponse]: List of todos with the specified status.
        """
        todos_in_db = await self.repository.get_todos_by_status(status)
        return [self._convert_to_response(todo) for todo in todos_in_db]
    
    async def get_overdue_todos(self) -> List[TodoResponse]:
        """
        Get overdue todos.
        
        Returns:
            List[TodoResponse]: List of overdue todos.
        """
        todos_in_db = await self.repository.get_overdue_todos()
        return [self._convert_to_response(todo) for todo in todos_in_db]
    
    def _convert_to_response(self, todo_in_db) -> TodoResponse:
        """
        Convert TodoInDB to TodoResponse.
        
        Args:
            todo_in_db: Todo from database.
            
        Returns:
            TodoResponse: Todo response format.
        """
        return TodoResponse(
            id=str(todo_in_db.id),
            title=todo_in_db.title,
            description=todo_in_db.description,
            status=todo_in_db.status,
            priority=todo_in_db.priority,
            due_date=todo_in_db.due_date,
            created_at=todo_in_db.created_at,
            updated_at=todo_in_db.updated_at
        )
