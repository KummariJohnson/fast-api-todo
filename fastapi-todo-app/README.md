# FastAPI Todo Application

A production-ready FastAPI to-do list application with MongoDB integration, built using Poetry for dependency management.

## Features

- **CRUD Operations**: Create, read, update, and delete todos
- **MongoDB Integration**: Async MongoDB operations using Motor
- **Data Validation**: Pydantic models for request/response validation
- **Pagination**: Efficient pagination for todo lists
- **Filtering & Sorting**: Filter by status/priority and sort by various fields
- **Status Management**: Track todo status (pending, in_progress, completed)
- **Priority Levels**: Assign priority levels (low, medium, high)
- **Due Dates**: Set and track due dates for todos
- **Overdue Detection**: Identify overdue todos
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Production Ready**: Proper error handling, logging, and configuration

## Project Structure

\`\`\`
fastapi-todo-app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Application configuration
│   │   └── database.py        # Database connection management
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py            # Pydantic models and schemas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── todo_repository.py # Database operations
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py    # Business logic
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── api.py         # API router configuration
│           └── endpoints/
│               ├── __init__.py
│               └── todos.py   # Todo API endpoints
├── pyproject.toml             # Poetry configuration
├── .env.example              # Environment variables example
└── README.md                 # This file
\`\`\`

## Installation

### Prerequisites

- Python 3.9+
- Poetry
- MongoDB

### Setup

1. **Clone the repository**:
   \`\`\`bash
   git clone <repository-url>
   cd fastapi-todo-app
   \`\`\`

2. **Install dependencies using Poetry**:
   \`\`\`bash
   poetry install
   \`\`\`

3. **Set up environment variables**:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your MongoDB configuration
   \`\`\`

4. **Activate the virtual environment**:
   \`\`\`bash
   poetry shell
   \`\`\`

## Configuration

Create a `.env` file in the project root with the following variables:

\`\`\`env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=todo_app

# Application Configuration
APP_NAME=FastAPI Todo App
APP_VERSION=0.1.0
DEBUG=True
\`\`\`

## Running the Application

### Development

\`\`\`bash
# Using Poetry
poetry run python app/main.py

# Or with uvicorn directly
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

### Production

\`\`\`bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
\`\`\`

The application will be available at:
- **API**: http://localhost:8000
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Todo Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/todos/` | Create a new todo |
| GET | `/api/v1/todos/` | Get todos with pagination and filtering |
| GET | `/api/v1/todos/{todo_id}` | Get a specific todo by ID |
| PUT | `/api/v1/todos/{todo_id}` | Update a todo |
| DELETE | `/api/v1/todos/{todo_id}` | Delete a todo |
| GET | `/api/v1/todos/status/{status}` | Get todos by status |
| GET | `/api/v1/todos/overdue/list` | Get overdue todos |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |

## Data Models

### Todo Fields

- **title**: String (required, 1-200 characters)
- **description**: String (optional, max 1000 characters)
- **status**: Enum (pending, in_progress, completed)
- **priority**: Enum (low, medium, high)
- **due_date**: DateTime (optional)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-updated)

### Example Todo Creation

\`\`\`json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the FastAPI todo application",
  "status": "pending",
  "priority": "high",
  "due_date": "2024-01-15T10:00:00Z"
}
\`\`\`

## Query Parameters

### Get Todos Endpoint

- **page**: Page number (default: 1)
- **size**: Page size (default: 10, max: 100)
- **status**: Filter by status (pending, in_progress, completed)
- **priority**: Filter by priority (low, medium, high)
- **sort_by**: Sort field (default: created_at)
- **sort_order**: Sort order (asc, desc, default: desc)

Example:
\`\`\`
GET /api/v1/todos/?page=1&size=20&status=pending&priority=high&sort_by=due_date&sort_order=asc
\`\`\`

## Development

### Code Quality Tools

The project includes several development tools configured in `pyproject.toml`:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **MyPy**: Type checking

Run quality checks:

\`\`\`bash
# Format code
poetry run black app/

# Sort imports
poetry run isort app/

# Lint code
poetry run flake8 app/

# Type checking
poetry run mypy app/
\`\`\`

### Project Architecture

The application follows a clean architecture pattern:

1. **API Layer** (`app/api/`): FastAPI routes and request/response handling
2. **Service Layer** (`app/services/`): Business logic and orchestration
3. **Repository Layer** (`app/repositories/`): Data access and database operations
4. **Model Layer** (`app/models/`): Data models and validation schemas
5. **Core Layer** (`app/core/`): Configuration and shared utilities

This separation ensures:
- **Maintainability**: Clear separation of concerns
- **Testability**: Easy to unit test individual layers
- **Scalability**: Easy to extend and modify functionality
- **Reusability**: Components can be reused across different parts of the application

## Error Handling

The application includes comprehensive error handling:

- **Validation Errors**: Automatic validation using Pydantic models
- **Database Errors**: Proper error handling for MongoDB operations
- **HTTP Exceptions**: Appropriate HTTP status codes and error messages
- **Not Found**: 404 errors for non-existent resources
- **Server Errors**: 500 errors for unexpected server issues

## Performance Considerations

- **Async Operations**: All database operations are asynchronous
- **Connection Pooling**: MongoDB connection pooling via Motor
- **Pagination**: Efficient pagination to handle large datasets
- **Indexing**: Consider adding database indexes for frequently queried fields
- **Caching**: Can be extended with Redis for caching frequently accessed data

## Contributing

1. Follow the existing code style and architecture patterns
2. Add proper documentation for new functions and endpoints
3. Include appropriate error handling
4. Run code quality tools before submitting changes
5. Update this README if adding new features

## License

This project is licensed under the MIT License.
