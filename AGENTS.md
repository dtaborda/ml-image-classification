# AGENTS.md - Coding Guidelines for Sprint Project 3

This document provides comprehensive guidelines for coding agents working on this FastAPI ML microservices project. It covers build commands, testing, code style, and development conventions.

## Build, Lint, and Test Commands

### Formatting and Linting
```bash
# Format code with Black (88 char line length) and sort imports with isort
make format
# or manually:
black .
isort . --recursive --profile black

# Check formatting in CI (GitHub Actions)
# Uses python-black-check action with line-length: '88'
```

### Testing Commands

#### Unit Tests (Individual Services)
```bash
# Run single test file
pytest api/tests/test_router_user.py
pytest model/tests/test_model.py
pytest ui/tests/test_image_classifier_app.py

# Run all tests for a service
pytest api/tests/
pytest model/tests/
pytest ui/tests/

# Run tests with Docker (multi-stage build)
cd api && docker build -t fastapi_test --progress=plain --target test .
cd model && docker build -t model_test --progress=plain --target test .
cd ui && docker build -t ui_test --progress=plain --target test .
```

#### Integration Tests
```bash
# Install dependencies
pip3 install -r tests/requirements.txt

# Run end-to-end integration tests (requires full pipeline running)
python tests/test_integration.py
```

#### All Tests via Makefile
```bash
make test  # Runs pytest tests/
```

### Build and Deployment
```bash
# Build all services
docker-compose up --build -d

# Stop services
docker-compose down

# Build specific service
docker-compose build api
docker-compose build model
docker-compose build ui

# Populate database
cd api && cp .env.original .env && docker-compose up --build -d
```

## Code Style Guidelines

### Python Standards
- **Formatter**: Black with 88 character line length
- **Import Sorter**: isort with `--profile black`
- **Python Version**: 3.8+ (based on Docker images)
- **Docstrings**: Use Google-style docstrings for all functions
- **Type Hints**: Use typing module for all function parameters and return values

### Import Organization
```python
# Standard library imports
from typing import List, Optional
import json

# Third-party imports (alphabetized)
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Local imports (relative)
from app import db
from . import models, schema, services
```

### Naming Conventions
- **Functions/Methods**: `snake_case` (e.g., `get_user_by_id`, `create_user_registration`)
- **Variables**: `snake_case` (e.g., `database`, `current_user`)
- **Classes**: `PascalCase` (e.g., `User`, `DisplayUser`, `UserService`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT = 30`)
- **Modules**: `snake_case` (e.g., `user_router.py`, `auth_service.py`)
- **Directories**: `snake_case` (e.g., `user/`, `auth/`, `model/`)

### File Structure Conventions
```
api/app/
├── auth/           # Authentication related code
├── user/           # User management
├── model/          # ML model endpoints
├── feedback/       # User feedback system
├── settings.py     # Configuration
├── db.py          # Database connection
└── utils.py       # Utility functions
```

### FastAPI Patterns
- **Router Prefixes**: Use descriptive prefixes (e.g., `/user`, `/model`, `/auth`)
- **Tags**: Group endpoints with tags (e.g., `tags=["Users"]`, `tags=["Model"]`)
- **Status Codes**: Use proper HTTP status codes from `fastapi.status`
- **Dependencies**: Use dependency injection for database sessions and authentication
- **Async/Await**: Use async functions for all endpoints and services

### Database Patterns (SQLAlchemy)
- **Models**: Inherit from `Base` in `models.py`
- **Schemas**: Use Pydantic `BaseModel` with proper validation
- **Services**: Keep business logic in service layer
- **Database Sessions**: Inject via FastAPI dependency (`Depends(db.get_db)`)

### Error Handling
- **HTTP Exceptions**: Use `HTTPException` with appropriate status codes
- **Status Codes**:
  - `400`: Bad Request (validation errors)
  - `401`: Unauthorized (authentication required)
  - `404`: Not Found (resource doesn't exist)
  - `409`: Conflict (resource already exists)
  - `500`: Internal Server Error (unexpected errors)
- **Error Messages**: Provide clear, user-friendly error messages
- **Validation**: Use Pydantic validation for input data

### Authentication & Security
- **JWT Tokens**: Use `create_access_token()` and `verify_token()` from `auth/jwt.py`
- **Password Hashing**: Use proper password hashing (bcrypt/argon2)
- **Token Expiration**: 30-minute expiration for access tokens
- **Protected Routes**: Use `Depends(get_current_user)` for authenticated endpoints

### Testing Conventions
- **Framework**: pytest with pytest-asyncio for async tests
- **Mocking**: Use `unittest.mock.MagicMock` for database and external dependencies
- **HTTP Client**: Use `httpx.AsyncClient` for API endpoint testing
- **Test Structure**:
  ```python
  @pytest.mark.asyncio
  async def test_function_name():
      # Arrange
      mock_session = MagicMock(spec=Session)
      # ... setup mocks

      # Act
      async with AsyncClient(app=app, base_url="http://test") as ac:
          response = await ac.get("/endpoint")

      # Assert
      assert response.status_code == 200
  ```
- **Test Naming**: `test_<function_name>_<scenario>` (e.g., `test_create_user_registration_success`)
- **Coverage**: Aim for comprehensive coverage of business logic and error cases

### Microservices Communication
- **Redis**: Use Redis for inter-service communication
- **Message Format**: JSON for data serialization
- **Error Handling**: Graceful handling of service unavailability
- **Timeouts**: Implement appropriate timeouts for external calls

### Docker Best Practices
- **Multi-stage Builds**: Use separate stages for dependencies, testing, and production
- **Base Images**: Use specific Python versions (e.g., `python:3.8-slim`)
- **Security**: Run as non-root user where possible
- **Caching**: Order COPY commands to optimize layer caching

### Configuration Management
- **Environment Variables**: Use `.env` files for configuration
- **Settings Module**: Centralize configuration in `settings.py`
- **Validation**: Use Pydantic settings for environment variable validation
- **Secrets**: Never commit secrets or sensitive data

### Logging
- **Framework**: Use Python's `logging` module
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Structured Logging**: Include relevant context in log messages
- **Log Format**: Include timestamp, level, module, and message

### Performance Considerations
- **Async Operations**: Use async/await for I/O operations
- **Database Queries**: Optimize queries, use select_related/prefetch_related
- **Caching**: Implement caching for frequently accessed data
- **Image Processing**: Handle large files efficiently, implement size limits

### Security Best Practices
- **Input Validation**: Always validate and sanitize user inputs
- **SQL Injection**: Use parameterized queries (SQLAlchemy handles this)
- **XSS Prevention**: Sanitize HTML content if displayed
- **Rate Limiting**: Implement rate limiting for API endpoints
- **CORS**: Configure CORS properly for web UI integration
- **HTTPS**: Use HTTPS in production environments

### Code Review Checklist
- [ ] Code formatted with Black and isort
- [ ] Type hints provided for all functions
- [ ] Docstrings present and descriptive
- [ ] Tests written and passing
- [ ] Error handling implemented
- [ ] Security considerations addressed
- [ ] Performance optimizations considered
- [ ] Database queries optimized
- [ ] Dependencies properly injected

### Commit Message Conventions
- **Format**: `<type>(<scope>): <description>`
- **Types**:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation
  - `style`: Code style changes
  - `refactor`: Code refactoring
  - `test`: Test additions/modifications
  - `chore`: Maintenance tasks

### Development Workflow
1. **Setup**: Copy `.env.original` to `.env`
2. **Development**: Use `docker-compose up --build -d` for local development
3. **Testing**: Run unit tests with `make test`, integration tests manually
4. **Formatting**: Run `make format` before committing
5. **CI/CD**: GitHub Actions will run formatting checks and build tests

### Common Patterns and Anti-patterns

#### Good Patterns
```python
# Dependency injection
async def get_user_by_id(
    id: int,
    database: Session = Depends(db.get_db),
    current_user: schema.User = Depends(get_current_user),
) -> models.User:
    return await services.get_user_by_id(id, database)

# Proper error handling
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id {id} is not available",
    )

# Type hints
async def new_user_register(request: schema.User, database: Session) -> models.User:
```

#### Anti-patterns to Avoid
```python
# DON'T: Hardcoded database connections
database = SessionLocal()

# DON'T: No type hints
def get_user(id):

# DON'T: Bare except clauses
try:
    # code
except:
    pass

# DON'T: Inline SQL queries
database.execute("SELECT * FROM users WHERE id = ?", id)
```

### Dependencies and Libraries
- **Web Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic
- **Testing**: pytest, pytest-asyncio, httpx
- **ML**: TensorFlow/Keras (ResNet50)
- **Async**: aiofiles, httpx
- **Security**: passlib (bcrypt), python-multipart
- **Message Queue**: Redis

This document should be updated as the codebase evolves and new patterns emerge.