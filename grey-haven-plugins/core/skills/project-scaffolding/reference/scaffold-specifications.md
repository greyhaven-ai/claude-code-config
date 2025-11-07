# Scaffold Specifications

Technical specifications for each Grey Haven scaffold type.

---

## Cloudflare Worker API Specification

**Purpose**: Production REST/GraphQL API on Cloudflare edge network

**Minimum Files** (18):
- wrangler.toml, package.json, tsconfig.json
- src/index.ts (entry), routes/ (3 files), middleware/ (4 files)
- services/ (2 files), types/ (1 file), utils/ (1 file)
- tests/ (3 files), .github/workflows/, README.md

**Dependencies**:
```json
{
  "dependencies": {
    "hono": "^4.0.0"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20240117.0",
    "typescript": "^5.3.3",
    "vitest": "^1.2.0",
    "wrangler": "^3.25.0"
  }
}
```

**Features**:
- Hono framework
- D1 database binding
- JWT authentication middleware
- CORS configuration
- Request logging
- Error handling
- Health check endpoint
- Vitest tests

---

## React Component Specification

**Purpose**: Reusable UI component with tests and stories

**Minimum Files** (6):
- Component.tsx, Component.test.tsx, Component.stories.tsx
- Component.module.css, index.ts, README.md

**Dependencies**:
```json
{
  "devDependencies": {
    "@testing-library/react": "^14.1.0",
    "@testing-library/user-event": "^14.5.0",
    "@storybook/react-vite": "^7.6.0",
    "vitest": "^1.2.0"
  }
}
```

**Features**:
- TypeScript prop types
- CSS modules styling
- Vitest + Testing Library tests
- Storybook stories
- Accessible markup
- JSDoc documentation

---

## Python API Specification

**Purpose**: Production-ready FastAPI with async PostgreSQL

**Minimum Files** (22):
- pyproject.toml, alembic.ini, .env.example
- app/main.py, config.py, dependencies.py
- app/api/ (3 files), models/ (2 files), schemas/ (2 files)
- app/services/ (2 files), db/ (3 files)
- tests/ (4 files), alembic/versions/, README.md

**Dependencies**:
```toml
[project]
dependencies = [
  "fastapi[standard]>=0.109.0",
  "pydantic>=2.5.0",
  "sqlalchemy[asyncio]>=2.0.25",
  "alembic>=1.13.0",
  "asyncpg>=0.29.0",
]
```

**Features**:
- FastAPI with async
- Pydantic v2 validation
- SQLAlchemy 2.0 async
- Alembic migrations
- pytest with asyncio
- uv package manager
- Ruff linting
- mypy type checking

---

## Full-Stack Specification

**Purpose**: Complete monorepo with frontend and backend

**Minimum Files** (35):
- package.json (root), pnpm-workspace.yaml
- frontend/ (15 files), backend/ (12 files)
- packages/types/ (4 files), docs/ (4 files)

**Structure**:
```
my-app/
├── frontend/     # React + Vite + TanStack
├── backend/      # Cloudflare Worker + D1
├── packages/     # Shared TypeScript types
└── docs/         # Architecture docs
```

**Features**:
- pnpm workspaces
- Shared types package
- TanStack Router + Query
- Cloudflare deployment
- CI/CD pipeline
- Monorepo scripts

---

**Total Specs**: 4 scaffold types
**Coverage**: Frontend, backend, component, full-stack
