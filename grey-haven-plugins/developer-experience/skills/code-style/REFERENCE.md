# Technical Reference

Complete configuration files and detailed technical information for Grey Haven coding standards.

## TypeScript/React Configuration Files

### .prettierrc

Complete Prettier configuration from cvi-template:

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

**Field Explanations:**

- `tabWidth: 2` - Use 2 spaces for indentation (NOT 4)
- `semi: true` - Always add semicolons at the end of statements
- `printWidth: 90` - Wrap lines at 90 characters (NOT 80 or 120)
- `singleQuote: false` - Use double quotes for strings
- `endOfLine: "lf"` - Use Unix-style line endings (\\n)
- `trailingComma: "all"` - Add trailing commas wherever possible
- `prettier-plugin-organize-imports` - Auto-organize imports by type
- `prettier-plugin-tailwindcss` - Auto-sort Tailwind CSS classes

### .eslintrc

Complete ESLint configuration from cvi-template:

```json
{
  "root": true,
  "env": { "browser": true, "es2020": true },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["react-refresh"],
  "rules": {
    "react-hooks/exhaustive-deps": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-unused-vars": "off",
    "no-unused-vars": "off",
    "react-refresh/only-export-components": "off"
  }
}
```

**Rule Explanations:**

- `react-hooks/exhaustive-deps: "off"` - Don't enforce exhaustive deps in useEffect (manage manually)
- `@typescript-eslint/no-explicit-any: "off"` - Allow `any` type for flexibility
- `@typescript-eslint/no-unused-vars: "off"` - Don't error on unused variables (clean up manually)
- `no-unused-vars: "off"` - Same as above for non-TypeScript files
- `react-refresh/only-export-components: "off"` - Allow exporting non-components from module

**Philosophy:** Grey Haven takes a pragmatic approach over pedantic enforcement. The codebase values developer velocity and allows `any` types, unused variables, and manual dependency management when appropriate.

### tsconfig.json

Complete TypeScript configuration from cvi-template:

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
    "noEmit": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", ".wrangler", ".output"]
}
```

**Key Settings:**

- `strict: true` - Enable all strict type checking options
- `target: "ES2022"` - Compile to ES2022 JavaScript
- `module: "ESNext"` - Use ESNext module syntax
- `moduleResolution: "Bundler"` - Use bundler resolution for Vite/TanStack
- `jsx: "react-jsx"` - Use React 17+ JSX transform
- `paths: { "~/*": ["./src/*"] }` - Path alias for imports (e.g., `import { foo } from "~/lib/utils"`)
- `noEmit: true` - Don't emit compiled files (Vite handles this)

### package.json Scripts

Standard scripts from cvi-template:

```json
{
  "scripts": {
    "dev": "vinxi dev",
    "build": "vinxi build",
    "start": "vinxi start",
    "lint": "eslint .",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio",
    "prepare": "husky"
  }
}
```

## Python/FastAPI Configuration Files

### pyproject.toml (Ruff)

Complete Ruff configuration from cvi-backend-template:

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

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

**Field Explanations:**

- `line-length = 130` - Wrap lines at 130 characters (CRITICAL: NOT 80 or 88!)
- `indent-width = 4` - Use 4 spaces for indentation
- `fix-only = true` - Auto-fix issues without showing unfixable errors
- `show-fixes = true` - Show what was fixed
- `select = [...]` - Enable specific linter rules:
  - `E`, `W` - pycodestyle style enforcement
  - `F` - pyflakes error detection
  - `I` - isort import sorting
  - `B` - flake8-bugbear bug detection
  - `C4` - flake8-comprehensions list/dict comprehension improvements
  - `UP` - pyupgrade automatic Python version upgrades

### pyproject.toml (MyPy)

Complete MyPy configuration from cvi-backend-template:

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
ignore_missing_imports = false
strict_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
```

**Key Settings:**

- `disallow_untyped_defs: true` - **CRITICAL**: Require type hints on all function definitions
- `python_version = "3.11"` - Target Python 3.11+ (projects use 3.12+)
- `strict_optional: true` - Strict checking of Optional types
- `warn_return_any: true` - Warn when returning Any from typed functions
- `warn_unused_configs: true` - Warn about unused mypy config

**Philosophy:** Type hints are **required** in Grey Haven Python projects. Unlike TypeScript's relaxed rules, Python enforces strict typing.

### pyproject.toml (Pytest)

Complete pytest configuration from cvi-backend-template:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "unit: Unit tests (fast, isolated, mocked)",
    "integration: Integration tests (database, external services)",
    "e2e: End-to-end tests (full system)",
    "benchmark: Performance benchmark tests",
    "slow: Tests that take > 1 second",
]
addopts = [
    "-ra",  # Show summary of all test outcomes
    "--strict-markers",  # Require markers to be registered
    "--strict-config",  # Raise on config warnings
    "--tb=short",  # Shorter traceback format
]

[tool.coverage.run]
source = ["app"]
omit = ["tests/*", "*/migrations/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

**Marker Explanations:**

- `@pytest.mark.unit` - Fast, isolated tests with mocked dependencies
- `@pytest.mark.integration` - Tests with database or external services
- `@pytest.mark.e2e` - Full system end-to-end tests
- `@pytest.mark.benchmark` - Performance measurement tests
- `@pytest.mark.slow` - Tests taking over 1 second

**Coverage:** Aim for >80% code coverage across the project.

## Project Structure Details

### TypeScript/React Structure (cvi-template)

```plaintext
cvi-template/
├── src/
│   ├── routes/                      # TanStack Router file-based routing
│   │   ├── __root.tsx               # Root layout
│   │   ├── index.tsx                # Homepage (/)
│   │   ├── _authenticated/          # Protected routes (requires auth)
│   │   │   └── dashboard.tsx        # /dashboard
│   │   └── settings/
│   │       ├── index.tsx            # /settings
│   │       └── profile.tsx          # /settings/profile
│   │
│   ├── lib/
│   │   ├── components/              # React components
│   │   │   ├── ui/                  # Shadcn UI components (button, card, etc.)
│   │   │   ├── auth/                # Authentication components
│   │   │   └── layout/              # Layout components (header, sidebar)
│   │   │
│   │   ├── server/                  # Server-side code
│   │   │   ├── schema/              # Drizzle database schemas (snake_case!)
│   │   │   ├── functions/           # TanStack Start server functions
│   │   │   ├── auth.ts              # Better-auth configuration
│   │   │   └── db.ts                # Database connection with RLS
│   │   │
│   │   ├── config/                  # Configuration files
│   │   │   └── env.ts               # Environment validation (@t3-oss/env-core)
│   │   │
│   │   ├── hooks/                   # Custom React hooks (use-* naming)
│   │   ├── utils/                   # Utility functions
│   │   └── types/                   # TypeScript type definitions
│   │
│   ├── clients/                     # API client code
│   ├── data/                        # Zod schemas for data validation
│   ├── middleware/                  # Route middleware and guards
│   ├── services/                    # Business logic services
│   ├── workers/                     # Cloudflare Workers code
│   ├── index.css                    # Global styles (Tailwind)
│   └── router.tsx                   # Router configuration
│
├── public/                          # Static assets
├── tests/                           # Test files
├── .prettierrc                      # Prettier config
├── .eslintrc                        # ESLint config
├── tsconfig.json                    # TypeScript config
├── drizzle.config.ts                # Drizzle ORM config
├── vite.config.ts                   # Vite bundler config
├── wrangler.jsonc                   # Cloudflare Workers config
└── package.json                     # Dependencies and scripts
```

### Python/FastAPI Structure (cvi-backend-template)

```plaintext
cvi-backend-template/
├── app/
│   ├── config/                      # Application configuration
│   │   └── settings.py              # Pydantic settings with env vars
│   │
│   ├── db/                          # Database layer
│   │   ├── models/                  # SQLModel database models (snake_case!)
│   │   │   ├── account.py           # Account model
│   │   │   ├── tenant.py            # Tenant model (multi-tenant)
│   │   │   └── user.py              # User model
│   │   │
│   │   ├── repositories/            # Repository pattern (data access)
│   │   │   ├── base.py              # Base repository
│   │   │   ├── account_repository.py
│   │   │   ├── tenant_repository.py
│   │   │   └── user_repository.py
│   │   │
│   │   ├── db_types.py              # Custom database types (UTCDateTime)
│   │   └── session.py               # Database session management
│   │
│   ├── routers/                     # FastAPI routers (endpoints)
│   │   ├── accounts.py              # /accounts endpoints
│   │   ├── tenants.py               # /tenants endpoints
│   │   └── users.py                 # /users endpoints
│   │
│   ├── services/                    # Business logic layer
│   │   ├── auth_service.py          # Authentication service
│   │   └── billing_service.py       # Billing service
│   │
│   ├── schemas/                     # Pydantic schemas (API contracts)
│   │   ├── accounts.py              # Account request/response schemas
│   │   ├── tenants.py               # Tenant request/response schemas
│   │   └── users.py                 # User request/response schemas
│   │
│   ├── utils/                       # Utility functions
│   │   ├── logging.py               # Logging configuration
│   │   └── security.py              # Security utilities
│   │
│   ├── dependencies.py              # FastAPI dependencies
│   └── main.py                      # FastAPI app entry point
│
├── tests/                           # Test files
│   ├── unit/                        # Unit tests (@pytest.mark.unit)
│   ├── integration/                 # Integration tests (@pytest.mark.integration)
│   ├── e2e/                         # E2E tests (@pytest.mark.e2e)
│   ├── conftest.py                  # Pytest fixtures
│   └── __init__.py
│
├── alembic/                         # Database migrations (if using Alembic)
├── pyproject.toml                   # Python project config (Ruff, MyPy, pytest)
├── requirements.txt                 # Python dependencies
└── .env.example                     # Example environment variables
```

## Database Naming Standards

### Field Naming Rules

**ALWAYS use snake_case for database columns:**

```text
✅ CORRECT          ❌ WRONG
created_at          createdAt
tenant_id           tenantId
email_address       emailAddress
is_active           isActive
first_name          firstName
last_name           lastName
phone_number        phoneNumber
billing_tier        billingTier
max_retries         maxRetries
api_key_hash        apiKeyHash
```

### Table Naming Rules

**Use lowercase plural names:**

```text
✅ CORRECT          ❌ WRONG
users               User, Users, user
accounts            Account, ACCOUNTS
tenants             Tenant, Tenants
organizations       Organization
subscriptions       Subscription
```

### Index Naming Rules

**Use descriptive index names:**

```text
Format: {table}_{column}_idx

✅ CORRECT                    ❌ WRONG
user_email_idx                idx_1, email_index
user_tenant_id_idx            tenant_idx
organization_slug_idx         slug
```

### Foreign Key Naming Rules

**Reference the parent table:**

```text
Format: {parent_table}_{singular}_id

✅ CORRECT          ❌ WRONG
tenant_id           tenant
account_id          acc_id, accountId
organization_id     org_id, orgId
user_id             userId, uid
```

## Multi-Tenant Architecture

### Tenant Isolation Levels

Grey Haven projects use **row-level** tenant isolation:

1. **Every table** includes a `tenant_id` or `account_id` field
2. **Every query** filters by tenant ID
3. **Row Level Security (RLS)** policies enforce tenant boundaries
4. **Repository pattern** centralizes tenant filtering

### RLS Policy Pattern

Standard RLS policy structure:

```typescript
// TypeScript/Drizzle RLS helper
export const inSameTenant = (tenantIdCol: AnyPgColumn, query: SQL): SQL =>
  sql`${isSameTenant(tenantIdCol)} and (${query})`;

// Apply to table
pgPolicy("table_name_select", {
  for: "select",
  to: "public",
  using: inSameTenant(table.tenantId, sql`true`),
});
```

```sql
-- SQL RLS Policy
CREATE POLICY tenant_isolation_policy ON users
  USING (tenant_id = current_setting('app.tenant_id')::text);
```

### Repository Tenant Filtering

Every repository method filters by tenant:

```python
# Python repository pattern
async def get_by_id(self, id: UUID, tenant_id: UUID) -> Optional[Model]:
    """Get record by ID with tenant isolation."""
    result = await self.session.execute(
        select(self.model)
        .where(self.model.id == id)
        .where(self.model.tenant_id == tenant_id)  # Tenant filter!
    )
    return result.scalar_one_or_none()
```

## Import Organization

### TypeScript Import Order

Auto-organized by `prettier-plugin-organize-imports`:

```typescript
// 1. External libraries
import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";

// 2. Internal modules (path alias)
import { Button } from "~/lib/components/ui/button";
import { useAuth } from "~/lib/hooks/use-auth";
import { env } from "~/lib/config/env";

// 3. Relative imports
import { helpers } from "./helpers";
```

### Python Import Order

Auto-organized by Ruff `isort`:

```python
# 1. Standard library imports
import os
from datetime import datetime
from typing import Optional

# 2. Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from pydantic import BaseModel

# 3. Local imports (app.*)
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
```

## Line Length Reasoning

### TypeScript: 90 Characters

**Why 90?**

- Comfortable reading width on modern displays
- Allows two editor panes side-by-side
- Balances readability with code density
- TailwindCSS classes can be long - 90 gives room
- Standard 80 is too restrictive for modern development

### Python: 130 Characters

**Why 130?**

- Type hints can be verbose: `Annotated[AccountRepository, Depends(get_account_repository)]`
- Pydantic field definitions: `Field(default=None, description="Long description here")`
- Allows descriptive variable names without constant wrapping
- FastAPI decorators are long: `@router.post("/endpoint", response_model=ResponseSchema)`
- PEP 8's 79 is outdated for modern development

## Pre-commit Hooks

Both templates use pre-commit hooks for code quality:

### TypeScript Pre-commit

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run linting
npm run lint

# Run formatting check
npm run format:check

# Run type checking
npx tsc --noEmit
```

### Python Pre-commit

```bash
#!/usr/bin/env sh

# Activate virtual environment
source .venv/bin/activate

# Run Ruff formatter
ruff format .

# Run Ruff linter
ruff check --fix .

# Run MyPy type checking
mypy app/

# Run tests
pytest -m "not slow"
```

## Additional Resources

- **Frontend Template**: [cvi-template](https://github.com/greyhaven-ai/cvi-template) - TanStack Start + React 19 + Drizzle
- **Backend Template**: [cvi-backend-template](https://github.com/greyhaven-ai/cvi-backend-template) - FastAPI + SQLModel + PostgreSQL
- **Prettier Docs**: https://prettier.io/docs/en/configuration.html
- **ESLint Docs**: https://eslint.org/docs/latest/use/configure/
- **Ruff Docs**: https://docs.astral.sh/ruff/
- **Drizzle ORM**: https://orm.drizzle.team/docs/overview
- **TanStack Start**: https://tanstack.com/router/latest/docs/framework/react/start/overview
