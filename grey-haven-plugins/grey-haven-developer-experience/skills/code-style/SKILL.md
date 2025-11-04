---
name: grey-haven-code-style
description: Apply Grey Haven Studio's actual coding standards from cvi-template (TypeScript/React) and cvi-backend-template (Python/FastAPI). Use when writing or reviewing code for Grey Haven projects. Includes Prettier, ESLint, Ruff, database conventions, and multi-tenant patterns.
---

# Grey Haven Code Style Standards

These are the **actual** coding standards used in Grey Haven Studio projects, extracted from production templates. Follow these exactly when working on Grey Haven codebases.

## TypeScript/React Standards (Frontend)

Based on `cvi-template` - TanStack Start + React 19 template.

### Prettier Configuration

**CRITICAL: Use these exact settings** (from `.prettierrc`):

```json
{
  "tabWidth": 2,
  "semi": true,
  "printWidth": 90,
  "singleQuote": false,
  "endOfLine": "lf",
  "trailingComma": "all",
  "plugins": ["prettier-plugin-organize-imports", "prettier-plugin-tailwindcss"]
}
```

**Key Points**:
- **Line width: 90 characters** (NOT 80 or 120)
- **Tab width: 2 spaces**
- **Semicolons: REQUIRED**
- **Quotes: DOUBLE quotes** (singleQuote: false)
- **Trailing commas: ALWAYS** (all)
- **Auto-organize imports** via prettier-plugin-organize-imports
- **Auto-sort Tailwind classes** via prettier-plugin-tailwindcss

### ESLint Rules

**CRITICAL: Grey Haven allows flexibility** (from `.eslintrc`):

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "react-hooks/exhaustive-deps": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-unused-vars": "off",
    "no-unused-vars": "off",
    "react-refresh/only-export-components": "off"
  }
}
```

**Key Points**:
- **`any` type: ALLOWED** - Use when appropriate for flexibility
- **Unused vars: NOT enforced** - Clean up manually
- **Exhaustive deps: OFF** - Manage dependencies thoughtfully
- Still use TypeScript best practices, but pragmatic over pedantic

### TypeScript Configuration

**Compiler Options** (from `tsconfig.json`):

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "esModuleInterop": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "allowJs": true,
    "forceConsistentCasingInFileNames": true,
    "baseUrl": ".",
    "paths": {
      "~/*": ["./src/*"]
    },
    "noEmit": true
  }
}
```

**Key Points**:
- **Strict mode: true**
- **Path alias: `~/*` maps to `./src/*`** - Use for all imports
- **Module resolution: Bundler** (for Vite/TanStack)
- **Target: ES2022**

### Naming Conventions

**TypeScript/JavaScript**:
- **Variables/Functions**: camelCase (`getUserData`, `isAuthenticated`)
- **Components**: PascalCase (`UserProfile`, `AuthProvider`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`, `MAX_RETRIES`)
- **Types/Interfaces**: PascalCase (`User`, `AuthConfig`)
- **Files**:
  - Components: PascalCase (`UserProfile.tsx`)
  - Utilities: camelCase or kebab-case (`formatDate.ts`, `use-auth.ts`)
  - Routes: lowercase with hyphens (`user-profile.tsx`)

**Database Fields** (CRITICAL):
- **Always use snake_case** for database column names
- Examples: `user_id`, `created_at`, `tenant_id`, `is_active`
- Drizzle schema enforces this convention

### Project Structure (TanStack Start)

```
src/
├── routes/                    # File-based routing (TanStack Router)
│   ├── _authenticated/        # Protected routes (underscore prefix)
│   ├── _layout.tsx            # Layout wrapper
│   └── index.tsx              # Homepage
├── lib/
│   ├── components/
│   │   ├── ui/                # Shadcn UI components (PascalCase)
│   │   ├── auth/              # Auth-specific components
│   │   ├── billing/           # Billing-specific components
│   │   └── layout/            # Layout components
│   ├── server/
│   │   ├── schema/            # Drizzle database schema (snake_case)
│   │   ├── functions/         # Server functions
│   │   ├── auth.ts            # Better-auth configuration
│   │   └── db.ts              # Database connections (RLS)
│   ├── config/
│   │   ├── env.ts             # Environment validation (@t3-oss/env-core)
│   │   └── [feature].ts       # Feature configs
│   ├── middleware/            # Route guards and middleware
│   ├── hooks/                 # Custom React hooks (use-* naming)
│   ├── utils/                 # Utility functions
│   └── types/                 # TypeScript type definitions
├── public/                    # Static assets
└── tests/                     # Test files
```

**Key Patterns**:
- **Path imports**: Use `~/` alias for all imports from src
- **Server code**: Keep in `lib/server/` directory
- **Components**: Group by feature, not by type
- **Shadcn UI**: Install to `lib/components/ui/`

### React Component Structure

```typescript
// 1. Imports (auto-sorted by prettier-plugin-organize-imports)
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "~/lib/components/ui/button";

// 2. Types/Interfaces
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

// 3. Component (default export preferred for routes)
export default function UserProfile({ userId, onUpdate }: UserProfileProps) {
  // 4. State (hooks first)
  const [editing, setEditing] = useState(false);

  // 5. Queries/Mutations
  const { data: user, isLoading } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => fetchUser(userId),
    staleTime: 60000, // 1 minute (Grey Haven default)
  });

  // 6. Effects (if needed)
  useEffect(() => {
    // ...
  }, [userId]);

  // 7. Event handlers
  const handleSave = async () => {
    // ...
  };

  // 8. Conditional renders
  if (isLoading) return <LoadingSpinner />;
  if (!user) return <NotFound />;

  // 9. Main render
  return (
    <div className="...">
      {/* TailwindCSS classes auto-sorted by prettier-plugin-tailwindcss */}
    </div>
  );
}
```

### TanStack Query Patterns

```typescript
// Default stale time: 1 minute
const { data } = useQuery({
  queryKey: ["resource", id],
  queryFn: () => fetchResource(id),
  staleTime: 60000,
});

// Server functions (TanStack Start)
import { createServerFn } from "@tanstack/start";

export const getUser = createServerFn("GET", async (userId: string) => {
  // Server-side code with database access
  return await db.query.users.findFirst({
    where: eq(users.id, userId),
  });
});
```

### Database Conventions (CRITICAL)

**Always use snake_case for database fields**:

```typescript
// [OK] Correct - Drizzle schema
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(), // Multi-tenant field
  email_address: text("email_address").notNull(),
  is_active: boolean("is_active").default(true),
});

// [X] Wrong - Don't use camelCase
export const users = pgTable("users", {
  id: uuid("id").primaryKey(),
  createdAt: timestamp("createdAt"), // WRONG!
  tenantId: uuid("tenantId"),        // WRONG!
});
```

**Multi-tenant Patterns**:
- Every table has `tenant_id` (UUID) for tenant isolation
- Use Row Level Security (RLS) with JWT tokens
- Database connections: admin, authenticated, anon roles

### Environment Variables

```typescript
// Use @t3-oss/env-core for validation
import { createEnv } from "@t3-oss/env-core";

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    REDIS_URL: z.string().url(),
  },
  client: {
    VITE_API_URL: z.string().url(), // Client vars prefixed with VITE_
  },
  runtimeEnv: import.meta.env,
});
```

## Python/FastAPI Standards (Backend)

Based on `cvi-backend-template` - FastAPI + SQLModel template.

### Ruff Configuration

**CRITICAL: Use these exact settings** (from `pyproject.toml`):

```toml
[tool.ruff]
fix-only = true
show-fixes = true
indent-width = 4
line-length = 130  # NOT 80 or 88!

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
```

**Key Points**:
- **Line length: 130 characters** (NOT 80 or 88)
- **Indent: 4 spaces**
- **Auto-fix enabled**: Ruff fixes issues automatically
- **Show fixes**: Always show what was fixed

### MyPy Configuration

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
```

**Key Points**:
- **Type hints REQUIRED** on all function definitions
- Strict type checking enabled
- Python 3.12 required for projects (despite mypy config showing 3.11)

### Naming Conventions

**Python**:
- **Functions/Variables**: snake_case (`get_user_data`, `is_authenticated`)
- **Classes**: PascalCase (`UserRepository`, `AuthService`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`, `MAX_RETRIES`)
- **Private members**: Leading underscore (`_internal_method`)
- **Database models**: PascalCase class, snake_case fields

**Database Fields** (CRITICAL):
- **Always snake_case**: `user_id`, `created_at`, `tenant_id`
- **Boolean fields**: Prefix with `is_` or `has_` (`is_active`, `has_access`)

### Project Structure (FastAPI)

```
app/
├── config/                    # Application settings
│   └── settings.py
├── db/
│   ├── models/                # SQLModel entities
│   │   ├── user.py
│   │   ├── organization.py
│   │   └── team.py
│   └── repositories/          # Repository pattern
│       ├── base.py
│       └── user_repository.py
├── routers/                   # FastAPI endpoints
│   ├── auth.py
│   ├── users.py
│   └── organizations.py
├── services/                  # Business logic
│   ├── auth_service.py
│   └── user_service.py
├── schemas/                   # Pydantic models (API contracts)
│   ├── user.py
│   └── auth.py
├── utils/                     # Utilities
│   ├── caching.py
│   └── logging.py
└── main.py                    # FastAPI app entry point
```

**Key Patterns**:
- **Repository pattern**: All database access through repositories
- **Service layer**: Business logic separate from routes
- **Dependency injection**: Use FastAPI's DI system
- **Multi-tenant**: Every model has `tenant_id` or `service_id`

### Python Code Structure

```python
"""Module docstring describing purpose."""

# 1. Standard library imports
import os
from datetime import datetime
from typing import Optional

# 2. Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

# 3. Local imports
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

# 4. Constants
MAX_PAGE_SIZE = 100

# 5. Router/Class definition
router = APIRouter(prefix="/users", tags=["users"])


# 6. Functions with type hints
async def get_user(
    user_id: str,
    repo: UserRepository = Depends(),
) -> UserResponse:
    """
    Get user by ID.

    Args:
        user_id: The user's unique identifier
        repo: User repository dependency

    Returns:
        UserResponse: The user data

    Raises:
        HTTPException: If user not found
    """
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

### Type Hints (REQUIRED)

```python
# [OK] Correct - All functions have type hints
from typing import Optional

def get_user(user_id: str) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

async def create_user(data: UserCreate) -> User:
    """Create new user."""
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    return user

# [X] Wrong - Missing type hints
def get_user(user_id):  # Missing parameter and return types
    return db.query(User).filter(User.id == user_id).first()
```

### SQLModel/Pydantic Patterns

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

# Database model (snake_case fields)
class User(SQLModel, table=True):
    """User database model."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    email_address: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)

# API schema (for requests/responses)
class UserCreate(SQLModel):
    """User creation schema."""
    email_address: str
    tenant_id: UUID

class UserResponse(SQLModel):
    """User response schema."""
    id: UUID
    email_address: str
    created_at: datetime
    is_active: bool
```

### Testing Standards

```python
import pytest
from httpx import AsyncClient

# Test markers
@pytest.mark.unit
async def test_user_creation():
    """Unit test for user creation."""
    # ...

@pytest.mark.integration
async def test_user_api(client: AsyncClient):
    """Integration test for user API."""
    response = await client.post("/users", json={"email": "test@example.com"})
    assert response.status_code == 201

@pytest.mark.e2e
async def test_full_user_flow(client: AsyncClient):
    """End-to-end test for user flow."""
    # ...
```

**Test Structure**:
- Mirror app structure in `tests/` directory
- Use markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`, `@pytest.mark.benchmark`
- Async tests automatically handled (asyncio_mode = "auto")
- Coverage threshold: aim for >80%

### Virtual Environment (CRITICAL)

**ALWAYS activate virtual environment before running Python commands**:

```bash
source .venv/bin/activate
```

Required for:
- Running tests (`pytest`)
- Running pre-commit hooks (`pre-commit run --all-files`)
- Running any Python scripts
- Using task commands (`task test`, `task format`)

## Multi-Tenant Architecture

**Both TypeScript and Python projects use multi-tenancy**:

### TypeScript (Frontend)
- Field name: `tenantId` (camelCase in TypeScript, snake_case in DB)
- Stored in: Database schema, auth context
- Used in: Row Level Security (RLS) policies

### Python (Backend)
- Field name: `tenant_id` or `service_id` (snake_case)
- Every model includes tenant isolation
- Repository pattern enforces tenant filtering

```python
# Multi-tenant repository pattern
class BaseRepository:
    async def get_by_id(self, id: UUID, tenant_id: UUID) -> Optional[Model]:
        """Get record by ID with tenant isolation."""
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == id)
            .where(self.model.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()
```

## When to Apply This Skill

Use this skill when:
- Writing new TypeScript/React or Python/FastAPI code for Grey Haven
- Reviewing code in pull requests
- Setting up new projects based on templates
- Configuring linters and formatters
- Creating database schemas
- Implementing multi-tenant features

## Template References

These standards come from actual Grey Haven templates:
- **Frontend**: `cvi-template` (TanStack Start + React 19)
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel)

When in doubt, reference these templates for patterns and configurations.

## Critical Reminders

1. **Line lengths**: TypeScript=90, Python=130 (NOT 80/88)
2. **Database fields**: ALWAYS snake_case (both TS and Python)
3. **`any` type**: ALLOWED in Grey Haven TypeScript
4. **Double quotes**: TypeScript uses double quotes (singleQuote: false)
5. **Type hints**: REQUIRED in Python (disallow_untyped_defs: true)
6. **Virtual env**: MUST activate before Python commands
7. **Multi-tenant**: Every table has tenant_id/tenantId
8. **Path aliases**: Use `~/` for TypeScript imports
9. **Trailing commas**: ALWAYS in TypeScript (trailingComma: "all")
10. **Pre-commit hooks**: Run before every commit (both projects)
