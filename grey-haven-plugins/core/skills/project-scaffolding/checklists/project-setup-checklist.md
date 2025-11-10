# Grey Haven Project Setup Checklist

Comprehensive checklist for scaffolding new Grey Haven projects with TanStack Start, FastAPI, or both.

## Pre-Project Planning

- [ ] **Define project scope** (MVP features, future roadmap)
- [ ] **Choose architecture**:
  - [ ] TanStack Start only (frontend + BFF)
  - [ ] FastAPI only (backend API)
  - [ ] Full-stack (TanStack Start + FastAPI)
  - [ ] Monorepo or separate repos

- [ ] **Define multi-tenant strategy**:
  - [ ] Single-tenant (one customer)
  - [ ] Multi-tenant (multiple customers)
  - [ ] Tenant isolation: subdomain, custom domain, path-based

- [ ] **Plan authentication**:
  - [ ] Better Auth (recommended for Grey Haven)
  - [ ] OAuth providers (Google, GitHub, etc.)
  - [ ] Email/password
  - [ ] Magic links

- [ ] **Database choice**:
  - [ ] PostgreSQL (recommended for Grey Haven)
  - [ ] MySQL
  - [ ] SQLite (development only)

- [ ] **Hosting platform**:
  - [ ] Vercel (TanStack Start)
  - [ ] Railway (FastAPI)
  - [ ] AWS (ECS, Lambda)
  - [ ] Self-hosted

## Repository Setup

### Initialize Git

- [ ] **Create repository** (GitHub, GitLab, Bitbucket)
- [ ] **Initialize git**: `git init`
- [ ] **Add .gitignore**:
  ```
  node_modules/
  .env
  .env.local
  __pycache__/
  *.pyc
  .venv/
  dist/
  .output/
  .vercel/
  .DS_Store
  ```

- [ ] **Initial commit**: `git commit -m "Initial commit"`
- [ ] **Create dev branch**: `git checkout -b dev`
- [ ] **Set up branch protection** (require PRs for main)

### Project Structure

- [ ] **Create standard directories**:
  ```
  .
  ├── .claude/                  # Claude Code config (optional)
  ├── apps/                     # Monorepo applications
  │   ├── web/                 # TanStack Start app
  │   └── api/                 # FastAPI app
  ├── packages/                 # Shared packages (monorepo)
  │   ├── shared-types/        # TypeScript types
  │   ├── ui/                  # Shared UI components
  │   └── utils/               # Shared utilities
  ├── docs/                     # Documentation
  ├── scripts/                  # Automation scripts
  └── .github/                  # GitHub workflows
      └── workflows/
  ```

- [ ] **Add README.md** with:
  - [ ] Project description
  - [ ] Tech stack
  - [ ] Getting started guide
  - [ ] Environment variables
  - [ ] Deployment instructions

## TanStack Start Setup

### Installation

- [ ] **Create Vite project**:
  ```bash
  npm create vite@latest my-app -- --template react-ts
  cd my-app
  ```

- [ ] **Install TanStack Start**:
  ```bash
  npm install @tanstack/react-router @tanstack/react-query
  npm install -D @tanstack/router-vite-plugin @tanstack/router-devtools
  ```

- [ ] **Install dependencies**:
  ```bash
  npm install zod drizzle-orm @better-auth/react
  npm install -D drizzle-kit tailwindcss postcss autoprefixer
  ```

### Configure Vite

- [ ] **Update vite.config.ts**:
  ```typescript
  import { defineConfig } from 'vite'
  import react from '@vitejs/plugin-react'
  import { TanStackRouterVite } from '@tanstack/router-vite-plugin'

  export default defineConfig({
    plugins: [
      react(),
      TanStackRouterVite()
    ],
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true
        }
      }
    }
  })
  ```

### Configure TailwindCSS

- [ ] **Initialize Tailwind**:
  ```bash
  npx tailwindcss init -p
  ```

- [ ] **Update tailwind.config.js**:
  ```javascript
  export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  ```

- [ ] **Add Tailwind directives** to `src/index.css`:
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```

### Setup Drizzle (Database)

- [ ] **Install Drizzle**:
  ```bash
  npm install drizzle-orm postgres
  npm install -D drizzle-kit
  ```

- [ ] **Create drizzle.config.ts**:
  ```typescript
  import { defineConfig } from 'drizzle-kit'

  export default defineConfig({
    schema: './src/db/schema.ts',
    out: './drizzle',
    dialect: 'postgresql',
    dbCredentials: {
      url: process.env.DATABASE_URL!
    }
  })
  ```

- [ ] **Create schema file** `src/db/schema.ts`:
  ```typescript
  import { pgTable, uuid, text, timestamp } from 'drizzle-orm/pg-core'

  export const users = pgTable('users', {
    id: uuid('id').defaultRandom().primaryKey(),
    email: text('email').notNull().unique(),
    name: text('name').notNull(),
    tenantId: uuid('tenant_id').notNull(),
    createdAt: timestamp('created_at').defaultNow(),
    updatedAt: timestamp('updated_at').defaultNow()
  })

  export const tenants = pgTable('tenants', {
    id: uuid('id').defaultRandom().primaryKey(),
    name: text('name').notNull(),
    slug: text('slug').notNull().unique(),
    createdAt: timestamp('created_at').defaultNow()
  })
  ```

- [ ] **Create migration**: `npx drizzle-kit generate`
- [ ] **Run migration**: `npx drizzle-kit migrate`

### Setup Better Auth

- [ ] **Install Better Auth**:
  ```bash
  npm install better-auth @better-auth/react
  ```

- [ ] **Create auth config** `src/lib/auth.ts`:
  ```typescript
  import { betterAuth } from 'better-auth'
  import { drizzleAdapter } from 'better-auth/adapters/drizzle'

  export const auth = betterAuth({
    database: drizzleAdapter(db, {
      provider: 'pg'
    }),
    emailAndPassword: {
      enabled: true
    },
    socialProviders: {
      google: {
        clientId: process.env.GOOGLE_CLIENT_ID!,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET!
      }
    }
  })
  ```

- [ ] **Create auth context** for React
- [ ] **Add protected route wrapper**

### Router Setup

- [ ] **Create routes directory** `src/routes/`
- [ ] **Create index route** `src/routes/index.tsx`
- [ ] **Create auth routes** (login, register, logout)
- [ ] **Create protected routes** (dashboard, settings)
- [ ] **Configure router** in `src/main.tsx`

### Environment Variables

- [ ] **Create .env.local**:
  ```
  DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
  BETTER_AUTH_SECRET=generate-with-openssl-rand-base64-32
  GOOGLE_CLIENT_ID=your-google-client-id
  GOOGLE_CLIENT_SECRET=your-google-client-secret
  VITE_API_URL=http://localhost:8000
  ```

- [ ] **Create .env.example** (without secrets)
- [ ] **Add to .gitignore**: `.env.local`

## FastAPI Setup

### Installation

- [ ] **Create project directory**:
  ```bash
  mkdir my-api && cd my-api
  ```

- [ ] **Setup Python virtual environment**:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # or .venv\Scripts\activate on Windows
  ```

- [ ] **Install FastAPI and dependencies**:
  ```bash
  pip install fastapi uvicorn sqlmodel psycopg2-binary pydantic python-dotenv
  pip install pytest pytest-asyncio httpx  # Testing
  ```

- [ ] **Create requirements.txt**:
  ```bash
  pip freeze > requirements.txt
  ```

### Project Structure

- [ ] **Create standard structure**:
  ```
  my-api/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py              # FastAPI app
  │   ├── models/              # SQLModel models
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   └── tenant.py
  │   ├── repositories/        # Data access layer
  │   │   ├── __init__.py
  │   │   ├── base.py
  │   │   └── user_repository.py
  │   ├── services/            # Business logic
  │   │   ├── __init__.py
  │   │   └── user_service.py
  │   ├── api/                 # API routes
  │   │   ├── __init__.py
  │   │   ├── deps.py          # Dependencies
  │   │   └── v1/
  │   │       ├── __init__.py
  │   │       ├── users.py
  │   │       └── auth.py
  │   ├── core/                # Config, security
  │   │   ├── __init__.py
  │   │   ├── config.py
  │   │   └── security.py
  │   └── db/                  # Database
  │       ├── __init__.py
  │       └── session.py
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py
  │   └── test_users.py
  ├── alembic/                 # Migrations
  ├── .env
  └── requirements.txt
  ```

### Database Setup (SQLModel)

- [ ] **Create SQLModel models** `app/models/user.py`:
  ```python
  from sqlmodel import SQLModel, Field
  from uuid import UUID, uuid4
  from datetime import datetime

  class User(SQLModel, table=True):
      __tablename__ = "users"

      id: UUID = Field(default_factory=uuid4, primary_key=True)
      email: str = Field(unique=True, index=True)
      name: str
      tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
      created_at: datetime = Field(default_factory=datetime.utcnow)
      updated_at: datetime = Field(default_factory=datetime.utcnow)
  ```

- [ ] **Create database session** `app/db/session.py`:
  ```python
  from sqlmodel import create_engine, Session
  from app.core.config import settings

  engine = create_engine(settings.DATABASE_URL, echo=True)

  def get_session():
      with Session(engine) as session:
          yield session
  ```

- [ ] **Create tables**: `SQLModel.metadata.create_all(engine)`

### Repository Pattern

- [ ] **Create base repository** `app/repositories/base.py`:
  ```python
  from typing import Generic, TypeVar, Type, Optional, List
  from sqlmodel import Session, select
  from uuid import UUID

  ModelType = TypeVar("ModelType", bound=SQLModel)

  class BaseRepository(Generic[ModelType]):
      def __init__(self, model: Type[ModelType], session: Session):
          self.model = model
          self.session = session

      def get(self, id: UUID) -> Optional[ModelType]:
          return self.session.get(self.model, id)

      def get_all(self, tenant_id: UUID) -> List[ModelType]:
          statement = select(self.model).where(
              self.model.tenant_id == tenant_id
          )
          return self.session.exec(statement).all()

      def create(self, obj: ModelType) -> ModelType:
          self.session.add(obj)
          self.session.commit()
          self.session.refresh(obj)
          return obj
  ```

- [ ] **Create specific repositories** (UserRepository, TenantRepository)

### API Routes

- [ ] **Create main app** `app/main.py`:
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware
  from app.api.v1 import users, auth

  app = FastAPI(title="My API", version="1.0.0")

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

  app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
  app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

  @app.get("/health")
  def health_check():
      return {"status": "healthy"}
  ```

- [ ] **Create route handlers** `app/api/v1/users.py`
- [ ] **Add dependency injection** for tenant_id, user auth

### Environment Variables

- [ ] **Create .env**:
  ```
  DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
  SECRET_KEY=generate-with-openssl-rand-hex-32
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  CORS_ORIGINS=http://localhost:3000
  ```

- [ ] **Create config** `app/core/config.py`:
  ```python
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      DATABASE_URL: str
      SECRET_KEY: str
      ALGORITHM: str = "HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

      class Config:
          env_file = ".env"

  settings = Settings()
  ```

## Testing Setup

### TypeScript/Vitest (Frontend)

- [ ] **Install Vitest**:
  ```bash
  npm install -D vitest @vitest/ui @testing-library/react @testing-library/jest-dom
  ```

- [ ] **Create vitest.config.ts**:
  ```typescript
  import { defineConfig } from 'vitest/config'
  import react from '@vitejs/plugin-react'

  export default defineConfig({
    plugins: [react()],
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: './src/test/setup.ts'
    }
  })
  ```

- [ ] **Add test script** to package.json: `"test": "vitest"`
- [ ] **Create sample test** `src/test/example.test.ts`

### Pytest (Backend)

- [ ] **Create conftest.py** with test fixtures:
  ```python
  import pytest
  from fastapi.testclient import TestClient
  from sqlmodel import Session, create_engine, SQLModel
  from app.main import app
  from app.db.session import get_session

  @pytest.fixture(name="session")
  def session_fixture():
      engine = create_engine("sqlite:///:memory:")
      SQLModel.metadata.create_all(engine)
      with Session(engine) as session:
          yield session

  @pytest.fixture(name="client")
  def client_fixture(session: Session):
      def get_session_override():
          return session
      app.dependency_overrides[get_session] = get_session_override
      client = TestClient(app)
      yield client
      app.dependency_overrides.clear()
  ```

- [ ] **Add test script**: `pytest tests/ -v`
- [ ] **Create sample test** `tests/test_users.py`

## Linting & Formatting

### TypeScript (ESLint + Prettier)

- [ ] **Install ESLint**:
  ```bash
  npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
  ```

- [ ] **Install Prettier**:
  ```bash
  npm install -D prettier eslint-config-prettier
  ```

- [ ] **Create .eslintrc.json**
- [ ] **Create .prettierrc**
- [ ] **Add scripts** to package.json:
  ```json
  "lint": "eslint src --ext ts,tsx",
  "format": "prettier --write src"
  ```

### Python (Ruff + Black)

- [ ] **Install Ruff and Black**:
  ```bash
  pip install ruff black
  ```

- [ ] **Create pyproject.toml**:
  ```toml
  [tool.black]
  line-length = 100

  [tool.ruff]
  line-length = 100
  select = ["E", "F", "I"]
  ```

- [ ] **Add to requirements.txt** (dev dependencies)

## CI/CD Setup

### GitHub Actions

- [ ] **Create workflow** `.github/workflows/ci.yml`:
  ```yaml
  name: CI

  on:
    push:
      branches: [main, dev]
    pull_request:
      branches: [main, dev]

  jobs:
    test-frontend:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-node@v3
          with:
            node-version: '20'
        - run: npm ci
        - run: npm run lint
        - run: npm test
        - run: npm run build

    test-backend:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
          with:
            python-version: '3.11'
        - run: pip install -r requirements.txt
        - run: pytest tests/ -v
  ```

- [ ] **Add deployment workflow** (Vercel, Railway, AWS)

## Database Migrations

- [ ] **Setup Drizzle migrations** (TanStack Start):
  - [ ] `npx drizzle-kit generate` to create migrations
  - [ ] `npx drizzle-kit migrate` to apply migrations

- [ ] **Setup Alembic** (FastAPI):
  ```bash
  pip install alembic
  alembic init alembic
  ```
  - [ ] Configure alembic.ini with DATABASE_URL
  - [ ] Create migration: `alembic revision --autogenerate -m "message"`
  - [ ] Apply migration: `alembic upgrade head`

## Secrets Management

- [ ] **Choose secrets manager**:
  - [ ] Doppler (recommended for Grey Haven)
  - [ ] AWS Secrets Manager
  - [ ] Environment variables (for local dev only)

- [ ] **Install Doppler CLI** (if using Doppler):
  ```bash
  # Install: https://docs.doppler.com/docs/install-cli
  doppler login
  doppler setup
  ```

- [ ] **Never commit secrets** to git
- [ ] **Use .env.example** for documentation

## Deployment

### Vercel (TanStack Start)

- [ ] **Install Vercel CLI**: `npm i -g vercel`
- [ ] **Connect to Vercel**: `vercel link`
- [ ] **Configure environment variables** in Vercel dashboard
- [ ] **Deploy**: `vercel --prod`
- [ ] **Setup custom domain** (if needed)

### Railway (FastAPI)

- [ ] **Install Railway CLI**: `npm i -g @railway/cli`
- [ ] **Login**: `railway login`
- [ ] **Initialize**: `railway init`
- [ ] **Add environment variables**: `railway variables`
- [ ] **Deploy**: `railway up`

## Multi-Tenant Configuration

- [ ] **Add tenant_id** to all relevant tables
- [ ] **Create RLS policies** (if using PostgreSQL RLS)
- [ ] **Repository pattern** enforces tenant filtering
- [ ] **Subdomain routing** (if applicable):
  - [ ] tenant1.myapp.com → tenant_id = uuid1
  - [ ] tenant2.myapp.com → tenant_id = uuid2

- [ ] **Tenant signup flow**:
  - [ ] Create tenant record
  - [ ] Create owner user
  - [ ] Associate user with tenant
  - [ ] Generate invitation links

## Monitoring & Observability

- [ ] **Setup error tracking** (Sentry, Datadog)
- [ ] **Add structured logging** (Pino for Node, structlog for Python)
- [ ] **Setup metrics** (Prometheus, Datadog)
- [ ] **Create health check endpoint** (`/health`)
- [ ] **Setup uptime monitoring** (Pingdom, UptimeRobot)

## Documentation

- [ ] **README.md** with setup instructions
- [ ] **API documentation** (auto-generated with FastAPI `/docs`)
- [ ] **Architecture diagram** (optional, but recommended)
- [ ] **Environment variables** documented in .env.example
- [ ] **Contributing guide** (if open-source or team project)

## Scoring

- **80+ items checked**: Excellent - Production-ready setup ✅
- **60-79 items**: Good - Most setup complete ⚠️
- **40-59 items**: Fair - Missing important pieces 🔴
- **<40 items**: Poor - Not ready for development ❌

## Priority Items

Complete these first:
1. **Repository setup** - Git, structure, README
2. **Database schema** - Models, migrations
3. **Authentication** - Better Auth, protected routes
4. **Testing setup** - Vitest, pytest
5. **CI/CD** - GitHub Actions, deployment

## Common Pitfalls

❌ **Don't:**
- Commit .env files (use .env.example instead)
- Skip testing setup (add it from day one)
- Ignore linting (consistent code quality matters)
- Deploy without health checks
- Skip multi-tenant isolation (add tenant_id early)

✅ **Do:**
- Use repository pattern for data access
- Set up CI/CD early (automate testing)
- Document environment variables
- Test authentication thoroughly
- Plan for scale (database indexes, caching)

## Related Resources

- [TanStack Start Documentation](https://tanstack.com/start)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Better Auth Documentation](https://better-auth.com)
- [Drizzle ORM Documentation](https://orm.drizzle.team)
- [project-scaffolding skill](../SKILL.md)

---

**Total Items**: 130+ setup checks
**Critical Items**: Repository, Database, Auth, Testing, Deployment
**Coverage**: TanStack Start, FastAPI, Multi-tenant, Testing, CI/CD
**Last Updated**: 2025-11-10
