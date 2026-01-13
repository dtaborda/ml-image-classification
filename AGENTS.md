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

### Commit Message Conventions (Conventional Commits)

We follow **Conventional Commits 1.0.0** standard with Angular convention for clear, semantic commit history.

#### Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

#### Types
- **feat**: New feature for the user (not a new feature for build script)
- **fix**: Bug fix for the user (not a fix to a build script)
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semicolons, etc; no code change)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes to build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

#### Scopes (for this project)
- **api**: FastAPI backend service
- **model**: ML model service
- **ui**: Streamlit UI service
- **db**: Database related
- **docker**: Docker/infrastructure changes
- **auth**: Authentication/authorization
- **tests**: Testing infrastructure
- **docs**: Documentation changes
- **deps**: Dependency updates

#### Subject Guidelines
- Use imperative, present tense: "add" not "added" nor "adds"
- Don't capitalize first letter
- No period (.) at the end
- Maximum 72 characters
- Be descriptive but concise

#### Body Guidelines (optional)
- Explain **why** not **what** (the diff shows what changed)
- Wrap at 72 characters
- Separate from subject with blank line
- Use bullet points for multiple changes

#### Footer Guidelines (optional)
- Reference issues/PRs: `Fixes #123`, `Closes #456`, `Refs #789`
- Breaking changes: `BREAKING CHANGE: <description>`

#### Examples

**Simple feature:**
```
feat(api): add user profile endpoint

- Implement GET /user/profile
- Add authentication middleware
- Include validation for user data

Closes #42
```

**Bug fix:**
```
fix(model): resolve memory leak in image preprocessing

The image buffers weren't being released after processing.
Added explicit cleanup in the finally block.

Fixes #156
```

**Documentation:**
```
docs(readme): update installation instructions for Apple Silicon

Added troubleshooting section for M1/M2/M3 chip compatibility.
```

**Breaking change:**
```
feat(api): change authentication to JWT Bearer tokens

BREAKING CHANGE: Old session-based auth is no longer supported.
Clients must now use Authorization: Bearer <token> header.

Migration guide added to docs/auth-migration.md
```

**Multiple scopes:**
```
refactor(api,model): standardize error response format

- API now returns consistent JSON error structure
- Model service updated to match new format
- Updated integration tests

Refs #234
```

#### Sprint-Specific Convention

For epic-based development, add epic tracking in the subject:

```
feat(api): [EPIC-2] implement ML prediction endpoint
fix(docker): [EPIC-1] resolve h5py compilation on ARM64
docs: [EPIC-0] add project setup documentation
```

#### Quick Reference

**Bad commits:**
```
✗ Fixed bug
✗ Update code
✗ WIP
✗ asdfasdf
✗ More changes
```

**Good commits:**
```
✓ fix(api): handle null user in authentication
✓ feat(model): add ResNet50 image classification
✓ docs(api): document prediction endpoint parameters
✓ refactor(ui): extract image upload component
✓ test(model): add unit tests for preprocessing
```

#### Tools

Use the `/commit` command for guided commit creation:
```bash
/commit
```

This will analyze staged changes and generate an appropriate commit message.

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

---

## Custom Commands for OpenCode

### /commit - Smart Commit Assistant

**Purpose:** Analyzes staged changes and generates a semantic commit message following Conventional Commits standard.

**Usage:**
```bash
/commit [options]
```

**Options:**
- `--epic <N>` - Add EPIC tracker (e.g., `--epic 2` → `[EPIC-2]`)
- `--breaking` - Mark as breaking change
- `--scope <scope>` - Override auto-detected scope

**Behavior:**

1. **Analyze Changes:**
   - Run `git status` and `git diff --staged`
   - Identify modified files and their locations
   - Auto-detect scope based on changed files:
     - Files in `api/` → scope: `api`
     - Files in `model/` → scope: `model`
     - Files in `ui/` → scope: `ui`
     - Files in `docs/` → scope: `docs`
     - `docker-compose.yml`, `Dockerfile*` → scope: `docker`
     - Multiple directories → use primary or `multi`

2. **Determine Type:**
   - New files → `feat`
   - Bug fixes (check diff for "fix", "bug", "error") → `fix`
   - Test files → `test`
   - Documentation → `docs`
   - Requirements.txt changes → `deps` or `fix`
   - Refactoring (no functional change) → `refactor`

3. **Generate Subject:**
   - Concise, imperative mood
   - Max 72 chars (or 60 if epic tag included)
   - Lowercase, no period
   - Examples:
     - `feat(api): add user authentication endpoint`
     - `fix(docker): resolve h5py compilation on ARM64`
     - `test(model): add unit tests for image preprocessing`

4. **Generate Body:**
   - List key changes as bullet points
   - Explain WHY if not obvious from diff
   - Include affected files if significant
   - Add warnings or migration notes if needed

5. **Add Footer:**
   - Epic reference: `Refs: EPIC-X-TX` (if provided)
   - Issue references: `Fixes #123` (if mentioned in branch name)
   - Breaking change notice if `--breaking` flag used

6. **Preview & Confirm:**
   - Show generated commit message
   - Ask for confirmation or allow editing
   - Commit with the generated/edited message

**Examples:**

```bash
# Basic usage (auto-detect everything)
$ /commit

📝 Staged changes detected:
   - model/requirements.txt (modified)
   - model/ml_service.py (modified)

📋 Generated commit message:
┌─────────────────────────────────────────────
│ fix(model): resolve h5py compilation on ARM64
│ 
│ - Add h5py==3.8.0 before tensorflow to use pre-compiled wheel
│ - Prevents HDF5 compilation error on Apple Silicon
│ - Update ml_service imports for compatibility
│ 
│ Fixes build issues on M1/M2/M3 chips.
└─────────────────────────────────────────────

✓ Commit this message? (y/n/edit)
```

```bash
# With EPIC tracker
$ /commit --epic 2

📋 Generated commit message:
┌─────────────────────────────────────────────
│ feat(model): [EPIC-2] implement ResNet50 prediction
│ 
│ - Load ResNet50 model with ImageNet weights
│ - Add image preprocessing pipeline
│ - Implement predict() function
│ 
│ Refs: EPIC-2-T2
└─────────────────────────────────────────────
```

```bash
# Breaking change
$ /commit --breaking

📋 Generated commit message:
┌─────────────────────────────────────────────
│ feat(api): change authentication to JWT tokens
│ 
│ - Replace session-based auth with JWT Bearer tokens
│ - Update all endpoints to use Authorization header
│ - Add token refresh endpoint
│ 
│ BREAKING CHANGE: Old session-based authentication
│ is no longer supported. Clients must update to use
│ JWT Bearer tokens in Authorization header.
│ 
│ Migration guide: docs/auth-migration.md
└─────────────────────────────────────────────
```

**Implementation Notes:**

The `/commit` command should:
1. Check if there are staged changes (`git diff --staged`)
2. If no staged changes, offer to stage all modified files
3. Parse file paths to determine scope
4. Analyze diff content for keywords (feat/fix/test/docs)
5. Generate semantic commit following Conventional Commits
6. Show preview with syntax highlighting
7. Allow interactive editing before committing
8. Run `git commit -m "<message>"`

**Error Handling:**
- No staged changes: Suggest `git add` or exit
- Conflicts: Warn and show `git status`
- Empty message: Re-prompt for input
- Git errors: Display error and suggest resolution

This command helps maintain consistent, high-quality commit messages across the team.