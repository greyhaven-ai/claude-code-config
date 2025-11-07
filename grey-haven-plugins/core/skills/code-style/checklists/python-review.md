# Python/FastAPI Code Review Checklist

Use this checklist when reviewing Python/FastAPI code or creating pull requests for Grey Haven projects.

## Formatting & Style

- [ ] **Line length**: Code lines do not exceed 130 characters (CRITICAL!)
- [ ] **Indentation**: Uses 4 spaces (not tabs or 2 spaces)
- [ ] **Quotes**: Uses double quotes for strings (Ruff default)
- [ ] **Line endings**: Uses Unix-style line endings (\\n)
- [ ] **Ruff formatted**: Code is formatted with Ruff (`ruff format .`)
- [ ] **Ruff linting**: No Ruff linting errors (`ruff check .`)

## Type Hints

- [ ] **Function signatures**: ALL functions have type hints (CRITICAL!)
  - Parameters: `def get_user(user_id: str) -> Optional[User]:`
  - Return types: Always include return type annotation
- [ ] **MyPy passing**: `mypy app/` has no type errors
- [ ] **Optional types**: Uses `Optional[T]` or `T | None` for nullable values
- [ ] **Generic types**: Uses proper generic types (`list[str]`, `dict[str, Any]`)
- [ ] **Type imports**: Imports types from `typing` module

## Database Models (SQLModel)

- [ ] **snake_case fields**: ALL database column names use snake_case (CRITICAL!)
  - ✅ `created_at`, `tenant_id`, `email_address`, `is_active`
  - ❌ `createdAt`, `tenantId`, `emailAddress`, `isActive`
- [ ] **Multi-tenant**: Models include `tenant_id` field
- [ ] **Field descriptions**: All fields have `description` parameter
- [ ] **Indexes**: Frequently queried fields have `index=True`
- [ ] **Constraints**: Foreign keys, unique constraints properly defined
- [ ] **Timestamps**: Uses UTC datetime (`UTCDateTime` type if available)
- [ ] **Table names**: Uses `__tablename__` with lowercase plural names

## Pydantic Schemas

- [ ] **Schema hierarchy**: Follows Base/Create/Update/Response pattern
- [ ] **Validators**: Uses `@field_validator` for custom validation
- [ ] **ConfigDict**: Response schemas have `model_config = ConfigDict(from_attributes=True)`
- [ ] **Field constraints**: Uses appropriate constraints (`ge`, `le`, `max_length`, etc.)
- [ ] **Optional fields**: Update schemas use `| None` for optional fields
- [ ] **Descriptions**: All fields have descriptions in `Field(..., description="...")`

## FastAPI Endpoints

- [ ] **Type hints**: ALL endpoint functions fully typed with `Annotated`
- [ ] **Docstrings**: Endpoints have comprehensive docstrings (Args, Returns, Raises)
- [ ] **Status codes**: Uses appropriate HTTP status codes from `status` module
- [ ] **Response models**: Endpoints specify `response_model`
- [ ] **Dependencies**: Uses Depends() for repository and auth dependencies
- [ ] **Error handling**: Raises HTTPException with proper status codes and messages
- [ ] **Router prefix**: Router has appropriate prefix and tags

## Repository Pattern

- [ ] **Tenant isolation**: ALL queries filter by `tenant_id` (CRITICAL!)
- [ ] **Type hints**: Repository methods fully typed
- [ ] **Async/await**: Uses async/await for database operations
- [ ] **Session management**: Properly commits and refreshes after changes
- [ ] **Error handling**: Handles database errors appropriately
- [ ] **CRUD methods**: Implements standard create, read, update, delete methods

## Multi-Tenant Architecture

- [ ] **Tenant filtering**: All queries include tenant_id filter
- [ ] **Repository methods**: Accept `tenant_id` parameter
- [ ] **Validation**: Validates user has access to requested tenant
- [ ] **Isolation**: No cross-tenant data leakage possible
- [ ] **Foreign keys**: Multi-tenant relationships properly enforced

## Imports Organization

- [ ] **Import order**: Follows Ruff isort rules:
  1. Standard library imports
  2. Third-party imports
  3. Local imports (app.*)
- [ ] **Absolute imports**: Uses absolute imports (not relative)
- [ ] **Grouped imports**: Related imports grouped together
- [ ] **No unused imports**: All imports are used

## Testing (Pytest)

- [ ] **Tests exist**: Endpoints/functions have corresponding tests
- [ ] **Test markers**: Uses pytest markers (@pytest.mark.unit, @pytest.mark.integration)
- [ ] **Fixtures**: Uses pytest fixtures for setup
- [ ] **Async tests**: Async tests decorated with `@pytest.mark.asyncio`
- [ ] **Mocking**: Uses AsyncMock/MagicMock for external dependencies
- [ ] **Coverage**: Maintains or improves test coverage (aim for >80%)
- [ ] **Assertions**: Tests have clear, specific assertions

## Security

- [ ] **Input validation**: Uses Pydantic schemas for input validation
- [ ] **SQL injection**: Uses parameterized queries (SQLModel handles this)
- [ ] **Authentication**: Endpoints require authentication via dependencies
- [ ] **Authorization**: Validates user has permission for actions
- [ ] **Secrets**: Uses environment variables for secrets (never hardcode)
- [ ] **Rate limiting**: Critical endpoints have rate limiting

## Error Handling

- [ ] **HTTPException**: Raises HTTPException with proper status codes
- [ ] **Error messages**: Error messages are descriptive and user-friendly
- [ ] **Logging**: Errors are logged appropriately
- [ ] **Validation errors**: Pydantic validation errors return 422
- [ ] **Not found**: Returns 404 for missing resources

## Performance

- [ ] **Database queries**: Queries are efficient (no N+1 problems)
- [ ] **Indexes**: Frequently filtered columns have indexes
- [ ] **Pagination**: List endpoints implement pagination (limit/offset)
- [ ] **Async operations**: Uses async/await for I/O operations
- [ ] **Connection pooling**: Database uses connection pooling

## Documentation

- [ ] **Docstrings**: All functions have comprehensive docstrings
- [ ] **OpenAPI docs**: FastAPI auto-docs are accurate and complete
- [ ] **Type annotations**: Type hints serve as documentation
- [ ] **README updated**: README reflects any new features/changes
- [ ] **API examples**: Complex endpoints have usage examples

## Pre-commit Checks

- [ ] **Virtual env active**: Ran commands with `source .venv/bin/activate`
- [ ] **Ruff formatting**: `ruff format .` applied
- [ ] **Ruff linting**: `ruff check --fix .` passing
- [ ] **MyPy**: `mypy app/` passing with no type errors
- [ ] **Tests passing**: `pytest` passes all tests
- [ ] **Coverage**: Test coverage meets threshold (>80%)
- [ ] **Pre-commit hooks**: All pre-commit hooks pass

## API Design

- [ ] **RESTful**: Endpoints follow REST principles
- [ ] **Naming**: Endpoints use clear, descriptive names
- [ ] **Versioning**: API versioned appropriately (`/v1/`)
- [ ] **Consistency**: Similar endpoints have consistent patterns
- [ ] **CRUD complete**: Resource has full CRUD operations if needed
