"""Todo API endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.models.todo import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
    TodoStatus,
    TodoPriority
)
from app.services.todo_service import TodoService

router = APIRouter()


@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
    description="Create a new todo item with the provided data."
)
async def create_todo(todo_data: TodoCreate) -> TodoResponse:
    """
    Create a new todo.
    
    Args:
        todo_data: Todo creation data.
        
    Returns:
        TodoResponse: The created todo.
        
    Raises:
        HTTPException: If creation fails.
    """
    try:
        service = TodoService()
        return await service.create_todo(todo_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create todo: {str(e)}"
        )


@router.get(
    "/",
    response_model=TodoListResponse,
    summary="Get todos with pagination and filtering",
    description="Retrieve todos with optional filtering by status and priority, plus pagination and sorting."
)
async def get_todos(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    size: int = Query(10, ge=1, le=100, description="Page size (max 100)"),
    status: Optional[TodoStatus] = Query(None, description="Filter by status"),
    priority: Optional[TodoPriority] = Query(None, description="Filter by priority"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order")
) -> TodoListResponse:
    """
    Get todos with filtering, sorting, and pagination.
    
    Args:
        page: Page number (1-based).
        size: Page size (max 100).
        status: Optional status filter.
        priority: Optional priority filter.
        sort_by: Field to sort by.
        sort_order: Sort order (asc or desc).
        
    Returns:
        TodoListResponse: Paginated list of todos.
        
    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        service = TodoService()
        return await service.get_todos(
            page=page,
            size=size,
            status=status,
            priority=priority,
            sort_by=sort_by,
            sort_order=sort_order
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve todos: {str(e)}"
        )


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get a todo by ID",
    description="Retrieve a specific todo by its ID."
)
async def get_todo(todo_id: str) -> TodoResponse:
    """
    Get a todo by ID.
    
    Args:
        todo_id: The todo ID.
        
    Returns:
        TodoResponse: The requested todo.
        
    Raises:
        HTTPException: If todo not found or retrieval fails.
    """
    try:
        service = TodoService()
        todo = await service.get_todo(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve todo: {str(e)}"
        )


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Update a todo",
    description="Update an existing todo with the provided data."
)
async def update_todo(todo_id: str, todo_data: TodoUpdate) -> TodoResponse:
    """
    Update a todo.
    
    Args:
        todo_id: The todo ID.
        todo_data: Update data.
        
    Returns:
        TodoResponse: The updated todo.
        
    Raises:
        HTTPException: If todo not found or update fails.
    """
    try:
        service = TodoService()
        updated_todo = await service.update_todo(todo_id, todo_data)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update todo: {str(e)}"
        )


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
    description="Delete a todo by its ID."
)
async def delete_todo(todo_id: str) -> None:
    """
    Delete a todo.
    
    Args:
        todo_id: The todo ID.
        
    Raises:
        HTTPException: If todo not found or deletion fails.
    """
    try:
        service = TodoService()
        deleted = await service.delete_todo(todo_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete todo: {str(e)}"
        )


@router.get(
    "/status/{status}",
    response_model=list[TodoResponse],
    summary="Get todos by status",
    description="Retrieve all todos with a specific status."
)
async def get_todos_by_status(status: TodoStatus) -> list[TodoResponse]:
    """
    Get todos by status.
    
    Args:
        status: The status to filter by.
        
    Returns:
        list[TodoResponse]: List of todos with the specified status.
        
    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        service = TodoService()
        return await service.get_todos_by_status(status)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve todos by status: {str(e)}"
        )


@router.get(
    "/overdue/list",
    response_model=list[TodoResponse],
    summary="Get overdue todos",
    description="Retrieve all todos that are past their due date and not completed."
)
async def get_overdue_todos() -> list[TodoResponse]:
    """
    Get overdue todos.
    
    Returns:
        list[TodoResponse]: List of overdue todos.
        
    Raises:
        HTTPException: If retrieval fails.
    """
    try:
        service = TodoService()
        return await service.get_overdue_todos()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve overdue todos: {str(e)}"
        )
