# Grey Haven Conventions

Complete style guide for Grey Haven projects - naming, structure, patterns, and standards.

---

## Naming Conventions

### Code Elements

| Element | Convention | Examples |
|---------|------------|----------|
| **Components** | PascalCase | `Button`, `UserProfile`, `DataTable` |
| **Functions** | camelCase | `getUserById`, `calculateTotal` |
| **Variables** | camelCase | `userId`, `isActive`, `firstName` |
| **Constants** | UPPER_SNAKE_CASE | `API_URL`, `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| **Types/Interfaces** | PascalCase | `User`, `ApiResponse`, `Config` |
| **Enums** | PascalCase | `Status`, `UserRole`, `HttpMethod` |

### Files and Directories

| Type | Convention | Examples |
|------|------------|----------|
| **Components** | PascalCase | `Button.tsx`, `UserProfile.tsx` |
| **Routes** | kebab-case | `user-profile.tsx`, `api-client.ts` |
| **Utilities** | kebab-case | `string-utils.ts`, `date-helpers.ts` |
| **Tests** | Match source + `.test` | `Button.test.tsx`, `api-client.test.ts` |
| **Stories** | Match source + `.stories` | `Button.stories.tsx` |
| **Directories** | kebab-case | `user-management/`, `api-routes/` |

### Database Schema

```sql
-- Tables: snake_case (plural)
CREATE TABLE user_profiles (...);
CREATE TABLE api_keys (...);

-- Columns: snake_case
user_id, first_name, created_at

-- Indexes: table_column_idx
CREATE INDEX user_profiles_email_idx ON user_profiles(email);

-- Foreign keys: table_column_fkey
FOREIGN KEY (user_id) REFERENCES users(id)
```

### API Endpoints

```
GET    /api/users              # List (plural)
GET    /api/users/:id          # Get single
POST   /api/users              # Create
PUT    /api/users/:id          # Update
DELETE /api/users/:id          # Delete

GET    /api/user-profiles      # kebab-case for multi-word
POST   /api/auth/login         # Nested resources
```

---

## Project Structure

### Frontend (React + Vite)

```
frontend/
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Root component
│   ├── routes/                 # TanStack Router routes
│   │   ├── index.tsx           # Home route
│   │   ├── users/
│   │   │   ├── index.tsx       # /users
│   │   │   └── $id.tsx         # /users/:id
│   │   └── __root.tsx          # Root layout
│   ├── components/             # Reusable components
│   │   ├── ui/                 # Generic UI (Button, Input)
│   │   ├── forms/              # Form components
│   │   └── layout/             # Layout components
│   ├── services/               # API clients, integrations
│   │   ├── api.ts              # API client
│   │   └── auth.ts             # Auth service
│   ├── lib/                    # Third-party setup
│   │   ├── query-client.ts     # TanStack Query config
│   │   └── router.ts           # Router config
│   ├── utils/                  # Pure utility functions
│   │   ├── string-utils.ts
│   │   └── date-utils.ts
│   ├── types/                  # TypeScript types
│   │   ├── api.ts              # API types
│   │   └── models.ts           # Domain models
│   └── assets/                 # Static assets
│       ├── images/
│       └── styles/
├── tests/                      # Mirror src/ structure
│   ├── routes/
│   ├── components/
│   └── services/
├── public/                     # Static files (favicon, etc.)
├── package.json
├── vite.config.ts
├── tsconfig.json
└── .env.example
```

### Backend (Cloudflare Worker)

```
backend/
├── src/
│   ├── index.ts                # Entry point
│   ├── routes/                 # API route handlers
│   │   ├── health.ts           # Health check
│   │   ├── users.ts            # User routes
│   │   └── auth.ts             # Auth routes
│   ├── middleware/             # Request middleware
│   │   ├── auth.ts             # Authentication
│   │   ├── cors.ts             # CORS config
│   │   ├── logger.ts           # Logging
│   │   └── error-handler.ts   # Error handling
│   ├── services/               # Business logic
│   │   ├── user-service.ts
│   │   └── auth-service.ts
│   ├── utils/                  # Helper functions
│   │   ├── db.ts               # Database helpers
│   │   └── jwt.ts              # JWT utilities
│   └── types/                  # TypeScript types
│       └── environment.d.ts    # Env types
├── tests/                      # Mirror src/
├── wrangler.toml               # Cloudflare config
├── package.json
└── tsconfig.json
```

### Python API (FastAPI)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── dependencies.py         # Dependency injection
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── users.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── db/                     # Database
│       ├── __init__.py
│       ├── base.py
│       └── session.py
├── tests/                      # Mirror app/
├── alembic/                    # Migrations
├── pyproject.toml              # uv config
└── .env.example
```

---

## Code Style

### TypeScript

```typescript
// Imports: grouped and sorted
import { useState, useEffect } from 'react';  // React
import { useQuery } from '@tanstack/react-query';  // Third-party
import { Button } from '@/components/ui/Button';  // Internal
import type { User } from '@/types/models';  // Types

// Interfaces: PascalCase, descriptive
export interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

// Components: PascalCase, typed props
export const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {
  // Hooks first
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.users.get(userId),
  });

  // Early returns
  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  // JSX
  return (
    <div>
      <h1>{user.name}</h1>
      <Button onClick={() => onUpdate?.(user)}>Update</Button>
    </div>
  );
};
```

### Python

```python
# Imports: grouped and sorted
from datetime import datetime  # Standard library
from uuid import UUID

from fastapi import APIRouter, Depends  # Third-party
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db  # Internal
from app.services.user_service import UserService

# Type hints: Always use
router = APIRouter()

# Functions: snake_case, typed
@router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get user by ID.

    Args:
        user_id: User UUID
        db: Database session

    Returns:
        User data dictionary

    Raises:
        HTTPException: If user not found
    """
    service = UserService(db)
    user = await service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.model_dump()
```

---

## Testing Conventions

### Test File Organization

```
tests/
├── unit/                       # Unit tests (isolated)
│   ├── components/
│   ├── services/
│   └── utils/
├── integration/                # Integration tests
│   ├── api/
│   └── database/
└── e2e/                        # End-to-end tests
    └── user-flow.test.ts
```

### Test Naming

```typescript
// Describe: Component/function name
describe('Button', () => {
  // It: Should + behavior
  it('should render with label', () => {
    render(<Button label="Click me" />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button label="Click" onClick={handleClick} />);

    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

```python
# Class: Test + ClassName
class TestUserService:
    """Test suite for UserService."""

    # Method: test_ + behavior
    async def test_get_user_returns_user_when_exists(self, db_session):
        """Should return user when user exists."""
        service = UserService(db_session)
        user = await service.get_user(user_id)

        assert user is not None
        assert user.email == "test@example.com"

    async def test_get_user_returns_none_when_not_exists(self, db_session):
        """Should return None when user doesn't exist."""
        service = UserService(db_session)
        user = await service.get_user(UUID4())

        assert user is None
```

---

## Git Conventions

### Branch Naming

```
feature/user-authentication    # New feature
fix/login-button-crash         # Bug fix
refactor/api-client            # Code refactoring
docs/api-documentation         # Documentation
chore/update-dependencies      # Maintenance
```

### Commit Messages

```
feat: add user authentication system
fix: resolve login button crash on mobile
refactor: extract API client into separate module
docs: add API endpoint documentation
chore: update dependencies to latest versions

# Format: type: description (lowercase, no period)
# Types: feat, fix, refactor, docs, chore, test, style
```

---

## Environment Variables

### Naming

```bash
# Format: UPPER_SNAKE_CASE with prefix
DATABASE_URL=postgresql://...
API_URL=https://api.example.com
JWT_SECRET=...

# Cloudflare-specific
CLOUDFLARE_API_TOKEN=...
CLOUDFLARE_ACCOUNT_ID=...

# Feature flags
FEATURE_NEW_UI=true
```

### Management

- Use `.env.example` for template
- Never commit `.env` files
- Use Wrangler secrets for Cloudflare
- Use environment-specific configs

---

**Version**: 1.0
**Last Updated**: 2024-01-15
