---
name: grey-haven-api-design
description: Design RESTful APIs following Grey Haven standards - FastAPI routes, Pydantic schemas, HTTP status codes, pagination, filtering, error responses, OpenAPI docs, and multi-tenant patterns. Use when creating API endpoints.
---

# Grey Haven API Design Standards

Design **RESTful APIs** following Grey Haven Studio's conventions for FastAPI backends and TanStack Start server functions.

## API Architecture Principles

### RESTful Resource Design
- **Resources as nouns**: `/users`, `/organizations`, `/teams` (NOT `/getUsers`, `/createOrganization`)
- **HTTP verbs for actions**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Hierarchical URLs**: `/organizations/{org_id}/teams/{team_id}/members`
- **Plural nouns**: `/users` (NOT `/user`)
- **Lowercase with hyphens**: `/api/user-profiles` (NOT `/api/userProfiles` or `/api/user_profiles`)

### Multi-Tenant Isolation
- **Tenant context from JWT**: Extract `tenant_id` from JWT claims
- **Automatic filtering**: Repository pattern enforces tenant isolation
- **Admin endpoints**: Require `is_superuser` flag in JWT
- **Cross-tenant queries**: Explicitly forbidden (except superusers)

### Versioning Strategy
- **URL versioning**: `/api/v1/users`, `/api/v2/users`
- **Major versions only**: Increment for breaking changes
- **Deprecation timeline**: 6 months notice before removing old version
- **Version in headers** (alternative): `Accept: application/vnd.greyhaven.v1+json`

## FastAPI Route Structure

### Repository Pattern (Recommended)
```python
# app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[UserRead]:
    """
    List all users in the current tenant.

    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return (max 100)
    - **Returns**: List of users with public fields only
    """
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    users = await repository.list(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Get a single user by ID (tenant-isolated)."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Create a new user in the current tenant."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.create(user_data)
    return user

@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Update an existing user (tenant-isolated)."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.update(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Soft-delete a user (tenant-isolated)."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    success = await repository.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
```

### Nested Resources
```python
# app/api/routes/organizations.py
@router.get("/{org_id}/teams", response_model=list[TeamRead])
async def list_organization_teams(
    org_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TeamRead]:
    """List all teams in an organization (tenant-isolated)."""
    # Verify organization exists and belongs to tenant
    org_repo = OrganizationRepository(db, tenant_id=current_user.tenant_id)
    org = await org_repo.get_by_id(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {org_id} not found",
        )

    # Fetch teams for organization
    team_repo = TeamRepository(db, tenant_id=current_user.tenant_id)
    teams = await team_repo.list_by_organization(org_id, skip=skip, limit=limit)
    return teams
```

## Pydantic Schema Design

### Request/Response Schemas
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Shared fields for User schemas."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    """Schema for updating an existing user (all fields optional)."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None

class UserRead(UserBase):
    """Schema for reading user data (public fields only)."""
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserReadWithPassword(UserRead):
    """Internal schema with password hash (use carefully!)."""
    hashed_password: str
```

### Nested Schemas
```python
# app/schemas/organization.py
from pydantic import BaseModel
from app.schemas.team import TeamRead

class OrganizationRead(BaseModel):
    """Organization with nested teams."""
    id: str
    name: str
    tenant_id: str
    teams: list[TeamRead] = []  # Nested teams
    created_at: datetime
    updated_at: datetime
```

### Validation Examples
```python
# app/schemas/user.py
from pydantic import field_validator, model_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Ensure password meets complexity requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        """Ensure password and password_confirm match."""
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self
```

## HTTP Status Codes

### Success Codes
- **200 OK**: Successful GET, PUT, PATCH requests
- **201 Created**: Successful POST request (resource created)
- **204 No Content**: Successful DELETE request (no response body)

### Client Error Codes
- **400 Bad Request**: Invalid request data (validation errors)
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: Authenticated but not authorized (insufficient permissions)
- **404 Not Found**: Resource doesn't exist or tenant isolation prevents access
- **409 Conflict**: Resource conflict (duplicate email, concurrent update)
- **422 Unprocessable Entity**: Validation errors (Pydantic schema validation)
- **429 Too Many Requests**: Rate limit exceeded

### Server Error Codes
- **500 Internal Server Error**: Unhandled exception (should be rare in production)
- **503 Service Unavailable**: Database connection error, external service down

### Status Code Examples
```python
# 201 Created with Location header
@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, response: Response) -> UserRead:
    user = await repository.create(user_data)
    response.headers["Location"] = f"/api/v1/users/{user.id}"
    return user

# 204 No Content
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str) -> None:
    await repository.delete(user_id)

# 409 Conflict
@router.post("")
async def create_user(user_data: UserCreate) -> UserRead:
    try:
        user = await repository.create(user_data)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
```

## Pagination and Filtering

### Offset-Based Pagination
```python
# app/api/routes/users.py
from pydantic import BaseModel

class PaginatedResponse[T](BaseModel):
    """Generic paginated response."""
    items: list[T]
    total: int
    skip: int
    limit: int
    has_more: bool

@router.get("", response_model=PaginatedResponse[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[UserRead]:
    """List users with pagination."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    users = await repository.list(skip=skip, limit=limit)
    total = await repository.count()

    return PaginatedResponse(
        items=users,
        total=total,
        skip=skip,
        limit=limit,
        has_more=(skip + limit) < total,
    )
```

### Cursor-Based Pagination (Recommended for Large Datasets)
```python
@router.get("", response_model=list[UserRead])
async def list_users(
    cursor: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """List users with cursor pagination."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    users = await repository.list_cursor(cursor=cursor, limit=limit)

    # Generate next cursor from last item
    next_cursor = None
    if len(users) == limit:
        next_cursor = users[-1].id

    return {
        "items": users,
        "next_cursor": next_cursor,
        "has_more": next_cursor is not None,
    }
```

### Filtering and Sorting
```python
@router.get("", response_model=list[UserRead])
async def list_users(
    is_active: Optional[bool] = None,
    email_contains: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[UserRead]:
    """List users with filtering and sorting."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)

    # Build filter criteria
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active
    if email_contains:
        filters["email_contains"] = email_contains

    users = await repository.list(
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )
    return users
```

## Error Response Format

### Standard Error Schema
```python
# app/schemas/error.py
from pydantic import BaseModel
from typing import Optional

class ErrorDetail(BaseModel):
    """Individual error detail."""
    field: Optional[str] = None  # Field name (for validation errors)
    message: str
    code: Optional[str] = None  # Error code (e.g., "DUPLICATE_EMAIL")

class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str  # Human-readable error message
    detail: Optional[str | list[ErrorDetail]] = None
    status_code: int
```

### Custom Exception Handler
```python
# app/core/exceptions.py
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException with standard error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
        },
    )

async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "code": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "detail": errors,
            "status_code": 422,
        },
    )

# Register exception handlers in main.py
from app.core.exceptions import http_exception_handler, validation_exception_handler

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
```

### Error Response Examples
```json
// 404 Not Found
{
  "error": "User with ID abc123 not found",
  "status_code": 404
}

// 422 Validation Error
{
  "error": "Validation error",
  "detail": [
    {
      "field": "email",
      "message": "value is not a valid email address",
      "code": "value_error.email"
    },
    {
      "field": "password",
      "message": "Password must be at least 8 characters",
      "code": "value_error"
    }
  ],
  "status_code": 422
}

// 409 Conflict
{
  "error": "User with this email already exists",
  "detail": "Email jane@example.com is already registered",
  "status_code": 409
}
```

## OpenAPI Documentation

### FastAPI Metadata
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="Grey Haven API",
    description="RESTful API for Grey Haven multi-tenant SaaS platform",
    version="1.0.0",
    contact={
        "name": "Grey Haven Studio",
        "url": "https://greyhaven.studio",
        "email": "support@greyhaven.studio",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "User management operations",
        },
        {
            "name": "organizations",
            "description": "Organization management operations",
        },
        {
            "name": "auth",
            "description": "Authentication and authorization",
        },
    ],
)
```

### Route Documentation
```python
@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="""
    Create a new user in the current tenant.

    - **email**: Valid email address (unique per tenant)
    - **password**: At least 8 characters, must include uppercase, digit
    - **full_name**: User's full name (1-255 characters)

    **Returns**: Created user with ID, timestamps, and public fields.

    **Errors**:
    - 409 Conflict: Email already exists in tenant
    - 422 Validation Error: Invalid email or weak password
    """,
    response_description="Successfully created user",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_user(user_data: UserCreate) -> UserRead:
    """Create a new user."""
    pass
```

### OpenAPI Customization
```python
# app/main.py
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    """Customize OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Grey Haven API",
        version="1.0.0",
        description="Multi-tenant SaaS platform",
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security globally
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

## TanStack Start Server Functions

### Server Function Pattern
```typescript
// app/routes/api/users.ts
import { createServerFn } from "@tanstack/start";
import { z } from "zod";
import { db } from "~/utils/db.server";
import { usersTable } from "~/db/schema";
import { getAuthUser } from "~/utils/auth.server";

// Validation schema
const createUserSchema = z.object({
  email: z.string().email(),
  fullName: z.string().min(1).max(255),
  password: z.string().min(8),
});

// Server function for creating user
export const createUser = createServerFn({ method: "POST" })
  .validator(createUserSchema)
  .handler(async ({ data, context }) => {
    // Get authenticated user from JWT
    const authUser = await getAuthUser(context);
    if (!authUser) {
      throw new Error("Unauthorized", { status: 401 });
    }

    // Check for duplicate email (tenant-isolated)
    const existing = await db
      .select()
      .from(usersTable)
      .where(
        and(
          eq(usersTable.email, data.email),
          eq(usersTable.tenantId, authUser.tenantId)
        )
      )
      .limit(1);

    if (existing.length > 0) {
      throw new Error("Email already exists", { status: 409 });
    }

    // Hash password
    const hashedPassword = await hashPassword(data.password);

    // Create user (tenant_id from auth context)
    const [user] = await db
      .insert(usersTable)
      .values({
        email: data.email,
        fullName: data.fullName,
        hashedPassword,
        tenantId: authUser.tenantId,
      })
      .returning();

    // Don't return password hash
    const { hashedPassword: _, ...userPublic } = user;
    return userPublic;
  });

// Client-side usage
import { useMutation } from "@tanstack/react-query";

function CreateUserForm() {
  const createUserMutation = useMutation({
    mutationFn: createUser,
    onSuccess: (user) => {
      console.log("User created:", user);
    },
    onError: (error) => {
      console.error("Error creating user:", error.message);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        createUserMutation.mutate({
          email: formData.get("email") as string,
          fullName: formData.get("fullName") as string,
          password: formData.get("password") as string,
        });
      }}
    >
      {/* Form fields */}
    </form>
  );
}
```

## Rate Limiting

### Upstash Redis Rate Limiter
```python
# app/core/rate_limit.py
from fastapi import Request, HTTPException, status
from upstash_redis import Redis
import os

# Doppler provides REDIS_URL
redis = Redis.from_url(os.getenv("REDIS_URL"))

async def rate_limit(request: Request, max_requests: int = 100, window: int = 60):
    """
    Rate limit based on IP address.

    - **max_requests**: Maximum requests allowed in window
    - **window**: Time window in seconds
    """
    # Get client IP
    client_ip = request.client.host

    # Rate limit key
    key = f"rate_limit:{client_ip}"

    # Increment counter
    count = redis.incr(key)

    # Set expiration on first request
    if count == 1:
        redis.expire(key, window)

    # Check if limit exceeded
    if count > max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {window} seconds.",
        )

# Apply to routes
@router.get("", dependencies=[Depends(rate_limit)])
async def list_users() -> list[UserRead]:
    """List users (rate limited)."""
    pass
```

## CORS Configuration

### FastAPI CORS
```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# IMPORTANT: Use Doppler for allowed origins in production
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # From Doppler: "https://app.greyhaven.studio"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight for 1 hour
)
```

**Doppler Configuration**:
```bash
# dev environment
CORS_ALLOWED_ORIGINS="http://localhost:3000"

# production environment
CORS_ALLOWED_ORIGINS="https://app.greyhaven.studio"
```

## Authentication and Authorization

### JWT Dependencies
```python
# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
import jwt
import os

from app.core.database import get_db
from app.models.user import User

security = HTTPBearer()

# Doppler provides JWT_SECRET_KEY
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Extract user from JWT token."""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")

        if user_id is None or tenant_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Fetch user from database (tenant-isolated)
    user = await db.get(User, user_id)
    if user is None or user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

async def require_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Require superuser privileges."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user
```

### Protected Routes
```python
@router.get("", response_model=list[UserRead])
async def list_users(
    current_user: User = Depends(get_current_user),  # JWT required
) -> list[UserRead]:
    """List users (authenticated)."""
    pass

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_superuser),  # Superuser required
) -> None:
    """Delete user (superuser only)."""
    pass
```

## Multi-Tenant API Patterns

### Automatic Tenant Filtering
```python
# app/repositories/user_repository.py
from sqlmodel import Session, select
from app.models.user import User

class UserRepository:
    """Repository with automatic tenant filtering."""

    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List users (automatically filtered by tenant_id)."""
        statement = (
            select(User)
            .where(User.tenant_id == self.tenant_id)  # Automatic tenant filter
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID (tenant-isolated)."""
        statement = select(User).where(
            User.id == user_id,
            User.tenant_id == self.tenant_id,  # Automatic tenant filter
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
```

### Cross-Tenant Queries (Superuser Only)
```python
@router.get("/admin/users", response_model=list[UserRead])
async def list_all_users(
    tenant_id: Optional[str] = None,
    current_user: User = Depends(require_superuser),  # Superuser only
    db: Session = Depends(get_db),
) -> list[UserRead]:
    """List users across all tenants (superuser only)."""
    # No tenant filtering - superuser can see all tenants
    statement = select(User)
    if tenant_id:
        statement = statement.where(User.tenant_id == tenant_id)

    result = await db.execute(statement)
    return result.scalars().all()
```

## Testing API Endpoints

### pytest with Doppler
```python
# tests/api/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """Test creating a new user."""
    response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "SecurePass123",
        },
        headers={"Authorization": f"Bearer {get_test_token()}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Should not return password

def test_duplicate_email():
    """Test creating user with duplicate email."""
    # Create first user
    client.post("/api/v1/users", json={...})

    # Try creating duplicate
    response = client.post("/api/v1/users", json={
        "email": "test@example.com",  # Same email
        "full_name": "Another User",
        "password": "SecurePass123",
    })
    assert response.status_code == 409
    assert "already exists" in response.json()["error"]

def test_unauthorized_access():
    """Test accessing endpoint without JWT."""
    response = client.get("/api/v1/users")
    assert response.status_code == 401
```

**Run tests with Doppler**:
```bash
doppler run --config test -- pytest tests/api/
```

## When to Apply This Skill

Use this API design skill when:
- Creating new FastAPI endpoints or TanStack Start server functions
- Designing RESTful resource hierarchies
- Implementing pagination, filtering, or sorting
- Writing Pydantic schemas for request/response validation
- Configuring OpenAPI documentation
- Setting up error response formats
- Implementing rate limiting or CORS
- Designing multi-tenant API isolation
- Testing API endpoints with pytest
- Reviewing API design in pull requests

## Template References

These API design patterns come from Grey Haven's actual templates:
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel + Repository Pattern)
- **Frontend**: `cvi-template` (TanStack Start server functions)
- **OpenAPI Docs**: FastAPI auto-generated at `/docs` and `/redoc`

## Critical Reminders

1. **Repository pattern for multi-tenant isolation** - Always use tenant-aware repositories
2. **Pydantic schemas for validation** - Don't return password hashes or sensitive fields
3. **HTTP status codes** - 201 for create, 204 for delete, 404 for not found
4. **Pagination for large datasets** - Use cursor-based for better performance
5. **Error response format** - Consistent error structure across all endpoints
6. **OpenAPI documentation** - Document all parameters, responses, errors
7. **Rate limiting** - Protect public endpoints with Upstash Redis
8. **CORS configuration** - Use Doppler for allowed origins (never hardcode)
9. **JWT authentication** - Extract tenant_id from JWT claims
10. **Testing with Doppler** - Run pytest with `doppler run --config test`
