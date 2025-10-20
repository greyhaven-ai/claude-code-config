---
name: grey-haven-project-structure
description: Organize Grey Haven projects following standard structures for TanStack Start (frontend) and FastAPI (backend). Use when creating new projects, organizing files, or refactoring project layout.
---

# Grey Haven Project Structure

Follow Grey Haven Studio's standardized project structures for TypeScript/React (TanStack Start) and Python/FastAPI projects.

## Frontend Structure (TanStack Start + React 19)

Based on `cvi-template` - TanStack Start, React 19, Drizzle, Better-auth.

### Directory Layout

```
project-root/
├── .claude/                     # Claude Code configuration
│   ├── hooks/                   # Pre-commit, post-commit hooks
│   └── settings.local.json      # MCP permissions
├── .github/                     # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml              # Continuous integration
│       └── deploy.yml          # Cloudflare Workers deployment
├── public/                      # Static assets served at root
│   ├── favicon.ico
│   ├── robots.txt
│   └── images/
├── src/                         # Source code (use ~/* path alias)
│   ├── routes/                  # TanStack Router file-based routes
│   │   ├── __root.tsx          # Root layout
│   │   ├── index.tsx           # Homepage (/)
│   │   ├── _authenticated/     # Protected routes group
│   │   │   ├── _layout.tsx    # Auth layout wrapper
│   │   │   ├── dashboard.tsx  # /dashboard
│   │   │   └── profile.tsx    # /profile
│   │   └── auth/               # Auth routes
│   │       ├── login.tsx      # /auth/login
│   │       └── signup.tsx     # /auth/signup
│   ├── lib/                     # Library code
│   │   ├── components/          # React components
│   │   │   ├── ui/             # Shadcn UI components (PascalCase)
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   └── input.tsx
│   │   │   ├── auth/           # Auth-specific components
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── SignupForm.tsx
│   │   │   ├── billing/        # Billing components
│   │   │   ├── layout/         # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Sidebar.tsx
│   │   │   └── shared/         # Shared components
│   │   ├── server/              # Server-side code
│   │   │   ├── schema/         # Drizzle database schema
│   │   │   │   ├── index.ts   # Schema exports
│   │   │   │   ├── users.ts   # User table (snake_case fields)
│   │   │   │   ├── organizations.ts
│   │   │   │   └── teams.ts
│   │   │   ├── functions/      # TanStack Start server functions
│   │   │   │   ├── auth.ts    # Auth server functions
│   │   │   │   ├── users.ts   # User CRUD
│   │   │   │   └── billing.ts
│   │   │   ├── auth.ts         # Better-auth configuration
│   │   │   └── db.ts           # Database connections (RLS roles)
│   │   ├── config/              # Configuration files
│   │   │   ├── env.ts          # Environment validation (@t3-oss/env-core)
│   │   │   ├── auth.ts         # Auth configuration
│   │   │   └── billing.ts      # Billing/Stripe config
│   │   ├── middleware/          # Route middleware
│   │   │   ├── auth.ts         # Auth guards
│   │   │   └── tenant.ts       # Tenant context
│   │   ├── hooks/               # Custom React hooks (use-* naming)
│   │   │   ├── use-auth.ts
│   │   │   ├── use-user.ts
│   │   │   └── use-tenant.ts
│   │   ├── utils/               # Utility functions
│   │   │   ├── cn.ts           # Class name utility
│   │   │   ├── format.ts       # Formatting helpers
│   │   │   └── api.ts          # API client
│   │   └── types/               # TypeScript type definitions
│   │       ├── auth.ts
│   │       ├── user.ts
│   │       └── billing.ts
│   └── tests/                   # Test files
│       ├── unit/               # Vitest unit tests
│       ├── integration/        # Vitest integration tests
│       └── e2e/                # Playwright E2E tests
│           └── auth.spec.ts
├── migrations/                  # Drizzle database migrations
│   ├── 0000_initial.sql
│   └── 0001_add_tenant_id.sql
├── .env.example                 # Example environment variables
├── .env                         # Local environment (gitignored)
├── .prettierrc                  # Prettier config (90 chars, double quotes)
├── .eslintrc                    # ESLint config (any allowed, strict off)
├── tsconfig.json                # TypeScript config (~/* path alias)
├── commitlint.config.cjs        # Commitlint (100 char header)
├── drizzle.config.ts            # Drizzle ORM configuration
├── vite.config.ts               # Vite configuration
├── vitest.config.ts             # Vitest test configuration
├── package.json                 # Dependencies and scripts
└── README.md                    # Project documentation
```

### Key Patterns (Frontend)

#### Path Imports - Always Use ~/* Alias

```typescript
// ✅ Correct - Use ~/* path alias
import { Button } from "~/lib/components/ui/button";
import { getUserById } from "~/lib/server/functions/users";
import { env } from "~/lib/config/env";
import { useAuth } from "~/lib/hooks/use-auth";

// ❌ Wrong - Relative paths
import { Button } from "../../lib/components/ui/button";
import { getUserById } from "../../../lib/server/functions/users";
```

#### File Naming Conventions

- **Components**: PascalCase (`UserProfile.tsx`, `LoginForm.tsx`)
- **Routes**: lowercase with hyphens (`user-profile.tsx`, `auth/login.tsx`)
- **Utilities**: camelCase or kebab-case (`formatDate.ts`, `use-auth.ts`)
- **Server functions**: camelCase (`auth.ts`, `users.ts`)
- **Schema files**: plural lowercase (`users.ts`, `organizations.ts`)

#### Component Organization

```typescript
// Component structure order
import { useState } from "react";                    // 1. External imports
import { useQuery } from "@tanstack/react-query";
import { Button } from "~/lib/components/ui/button"; // 2. Internal imports
import { getUserById } from "~/lib/server/functions/users";

interface UserProfileProps {                         // 3. Types/Interfaces
  userId: string;
}

export default function UserProfile({ userId }: UserProfileProps) { // 4. Component
  const [editing, setEditing] = useState(false);    // 5. State hooks

  const { data: user } = useQuery({                 // 6. Queries/Mutations
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
    staleTime: 60000,
  });

  const handleSave = async () => {                  // 7. Event handlers
    // ...
  };

  if (!user) return <LoadingSpinner />;            // 8. Conditional renders

  return (                                          // 9. Main render
    <div className="...">
      {/* TailwindCSS classes auto-sorted by prettier-plugin-tailwindcss */}
    </div>
  );
}
```

## Backend Structure (FastAPI + SQLModel)

Based on `cvi-backend-template` - FastAPI, SQLModel, Repository Pattern.

### Directory Layout

```
project-root/
├── .claude/                     # Claude Code configuration
│   ├── hooks/                   # Python hooks
│   └── settings.local.json
├── .github/                     # GitHub Actions
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── app/                         # Application code
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config/                 # Configuration
│   │   ├── __init__.py
│   │   └── settings.py        # Pydantic settings
│   ├── db/                     # Database layer
│   │   ├── __init__.py
│   │   ├── models/            # SQLModel entities (snake_case fields)
│   │   │   ├── __init__.py
│   │   │   ├── user.py       # User model
│   │   │   ├── organization.py
│   │   │   └── team.py
│   │   └── repositories/      # Repository pattern
│   │       ├── __init__.py
│   │       ├── base.py       # BaseRepository with tenant isolation
│   │       ├── user_repository.py
│   │       └── organization_repository.py
│   ├── routers/                # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── auth.py           # /auth/* endpoints
│   │   ├── users.py          # /users/* endpoints
│   │   ├── organizations.py
│   │   └── health.py         # Health check endpoint
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── billing_service.py
│   ├── schemas/                # Pydantic models (API contracts)
│   │   ├── __init__.py
│   │   ├── user.py           # UserCreate, UserResponse, etc.
│   │   ├── auth.py
│   │   └── common.py         # Shared schemas
│   ├── middleware/             # FastAPI middleware
│   │   ├── __init__.py
│   │   ├── auth.py           # JWT validation
│   │   └── tenant.py         # Tenant context
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── caching.py        # Redis caching
│   │   ├── logging.py        # Logging setup
│   │   └── security.py       # Security helpers
│   └── dependencies.py         # FastAPI dependencies
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── unit/                  # Unit tests (@pytest.mark.unit)
│   │   ├── __init__.py
│   │   ├── test_user_service.py
│   │   └── repositories/
│   │       └── test_user_repository.py
│   ├── integration/           # Integration tests (@pytest.mark.integration)
│   │   ├── __init__.py
│   │   └── test_user_api.py
│   ├── e2e/                   # E2E tests (@pytest.mark.e2e)
│   │   ├── __init__.py
│   │   └── test_full_flow.py
│   └── benchmark/             # Performance tests (@pytest.mark.benchmark)
│       ├── __init__.py
│       └── test_repository_performance.py
├── migrations/                 # Alembic database migrations
│   ├── versions/
│   │   ├── 001_initial.py
│   │   └── 002_add_tenant_id.py
│   ├── env.py
│   └── script.py.mako
├── .venv/                      # Virtual environment (gitignored)
├── .env.example                # Example environment variables
├── .env                        # Local environment (gitignored)
├── pyproject.toml              # Project config (Ruff, mypy, pytest)
├── alembic.ini                 # Alembic configuration
├── Taskfile.yml                # Task runner commands
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── README.md                   # Project documentation
```

### Key Patterns (Backend)

#### Import Organization (Automatic with Ruff)

```python
"""Module docstring describing purpose."""

# 1. Standard library imports
import os
from datetime import datetime
from typing import Optional
from uuid import UUID

# 2. Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

# 3. Local imports
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
```

#### File Naming Conventions

- **Modules**: snake_case (`user_service.py`, `auth_middleware.py`)
- **Models**: PascalCase class, snake_case file (`User` in `user.py`)
- **Tests**: `test_` prefix (`test_user_service.py`)

#### Repository Pattern

```python
# Base repository with tenant isolation
# app/db/repositories/base.py

from typing import Generic, TypeVar, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """Base repository with CRUD and tenant isolation."""

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_by_id(
        self, id: UUID, tenant_id: UUID
    ) -> Optional[T]:
        """Get by ID with automatic tenant filtering."""
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == id)
            .where(self.model.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        tenant_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> list[T]:
        """List with tenant isolation and pagination."""
        result = await self.session.execute(
            select(self.model)
            .where(self.model.tenant_id == tenant_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
```

```python
# Specific repository extending base
# app/db/repositories/user_repository.py

from app.db.repositories.base import BaseRepository
from app.db.models.user import User

class UserRepository(BaseRepository[User]):
    """User repository with custom queries."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(
        self, email: str, tenant_id: UUID
    ) -> Optional[User]:
        """Get user by email with tenant isolation."""
        result = await self.session.execute(
            select(User)
            .where(User.email_address == email)
            .where(User.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()
```

#### Service Layer Pattern

```python
# app/services/user_service.py

from uuid import UUID
from typing import Optional
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

class UserService:
    """User business logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(
        self, data: UserCreate, tenant_id: UUID
    ) -> UserResponse:
        """Create new user with validation."""
        # Business logic, validation, etc.
        existing = await self.user_repo.get_by_email(
            data.email_address, tenant_id
        )
        if existing:
            raise ValueError("Email already registered")

        user = await self.user_repo.create(data, tenant_id)
        return UserResponse.model_validate(user)
```

#### Router/Endpoint Pattern

```python
# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.db.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse
from app.dependencies import get_current_tenant_id, get_user_repository

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    tenant_id: UUID = Depends(get_current_tenant_id),
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    """Create a new user."""
    service = UserService(user_repo)
    try:
        return await service.create_user(data, tenant_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

## Virtual Environment (CRITICAL for Python)

**ALWAYS activate virtual environment before running Python commands:**

```bash
# Activate virtual environment
source .venv/bin/activate

# Now you can run:
python app/main.py
pytest
ruff check .
mypy app/
task test
```

**Required for**:
- Running FastAPI server
- Running tests (pytest)
- Running linters (Ruff, mypy)
- Running migrations (Alembic)
- Installing packages (pip)
- Task commands (task test, task format)

## Common Commands

### Frontend (TypeScript/TanStack Start)

```bash
# Development
npm run dev                      # Start dev server (port 3000)
npm run build                    # Production build
npm run preview                  # Preview production build

# Database (Drizzle)
npm run db:generate              # Generate migration from schema
npm run db:migrate               # Apply migrations
npm run db:studio                # Open Drizzle Studio
npm run db:push                  # Push schema (dev only)

# Testing
npm run test                     # Run Vitest unit/integration tests
npm run test:e2e                 # Run Playwright E2E tests
npm run test:coverage            # Generate coverage report

# Linting/Formatting
npm run lint                     # Run ESLint
npm run format                   # Run Prettier
npm run typecheck                # Run TypeScript compiler

# Pre-commit (automatic via hooks)
npm run pre-commit               # Run all checks
```

### Backend (Python/FastAPI)

```bash
# ALWAYS activate virtual environment first!
source .venv/bin/activate

# Development
uvicorn app.main:app --reload    # Start dev server (port 8000)
python -m app.main               # Alternative start

# Database (Alembic)
alembic revision --autogenerate -m "Description"  # Generate migration
alembic upgrade head             # Apply migrations
alembic downgrade -1             # Rollback one migration

# Testing (with markers)
task test                        # All tests
task test:unit                   # Unit tests only
task test:integration            # Integration tests
task test:e2e                    # E2E tests
task test:benchmark              # Performance tests
pytest --cov=app tests/          # With coverage

# Linting/Formatting
ruff check .                     # Check with Ruff (130 char lines)
ruff check . --fix               # Auto-fix with Ruff
mypy app/                        # Type checking (strict mode)

# Pre-commit (automatic via hooks)
task pre-commit                  # Run all checks
```

## Environment Variables

### Frontend (.env)

```bash
# Database (Neon PostgreSQL with RLS roles)
DATABASE_URL_ADMIN=postgresql://admin:password@host/db
DATABASE_URL_AUTHENTICATED=postgresql://authenticated:password@host/db
DATABASE_URL_ANON=postgresql://anon:password@host/db

# Auth (Better-auth)
BETTER_AUTH_SECRET=secret-key-here
BETTER_AUTH_URL=http://localhost:3000

# OAuth Providers
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret

# Redis
REDIS_URL=redis://localhost:6379

# Cloudflare (for deployment)
CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_API_TOKEN=your-api-token

# Client-side vars (VITE_ prefix)
VITE_API_URL=http://localhost:3000
```

### Backend (.env)

```python
# Database
DATABASE_URL_ADMIN=postgresql+asyncpg://admin:password@host/db
DATABASE_URL_AUTHENTICATED=postgresql+asyncpg://authenticated:password@host/db

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=secret-key-here
JWT_ALGORITHM=HS256

# API Settings
API_V1_PREFIX=/api/v1
DEBUG=true
ENVIRONMENT=development

# External Services
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG....
```

## When to Apply This Skill

Use this skill when:
- Creating new Grey Haven projects
- Organizing/refactoring existing projects
- Adding new features (know where files go)
- Reviewing project structure
- Teaching team members about project layout
- Migrating from other frameworks
- Setting up development environment

## Template References

These structures are from Grey Haven's actual templates:
- **Frontend**: `cvi-template` (TanStack Start + React 19)
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel)

## Critical Reminders

1. **Path imports**: Use `~/` alias for all TypeScript imports
2. **Virtual environment**: MUST activate for Python commands
3. **snake_case**: Database schema files, Python modules
4. **PascalCase**: React components, TypeScript classes
5. **Repository pattern**: All database access in FastAPI
6. **Server functions**: TanStack Start server-side code
7. **Test markers**: unit, integration, e2e, benchmark
8. **RLS roles**: admin, authenticated, anon database connections
9. **Migrations**: Always test up AND down
10. **Pre-commit hooks**: Automatically enforce standards
