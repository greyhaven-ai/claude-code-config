# Project Setup Checklist

**Use when creating new Grey Haven projects.**

## Initial Setup

### Choose Template
- [ ] Frontend: Use cvi-template (TanStack Start + React 19)
- [ ] Backend: Use cvi-backend-template (FastAPI + Python)
- [ ] Clone from Grey Haven GitHub organization
- [ ] Remove .git directory and re-initialize

### Environment Configuration
- [ ] Copy .env.example to .env
- [ ] Set up Doppler project (dev, test, staging, production)
- [ ] Add required secrets to Doppler
- [ ] Test Doppler access: `doppler run --config dev -- echo "Working"`
- [ ] Add .env to .gitignore (verify)

## Frontend Setup (TanStack Start)

### Directory Structure
- [ ] Verify src/routes/ structure (file-based routing)
- [ ] Verify src/lib/ organization (components, server, config, etc.)
- [ ] Verify public/ for static assets
- [ ] Verify migrations/ for Drizzle migrations

### Configuration Files
- [ ] Update tsconfig.json (verify ~/* path alias)
- [ ] Update package.json (project name, description)
- [ ] Verify .prettierrc (90 char line length, double quotes)
- [ ] Verify .eslintrc (any allowed, strict off)
- [ ] Update commitlint.config.cjs (100 char header)
- [ ] Update vite.config.ts (project-specific settings)
- [ ] Update vitest.config.ts (coverage thresholds >80%)

### Dependencies
- [ ] Run `bun install` (NOT npm!)
- [ ] Verify Drizzle ORM installed
- [ ] Verify better-auth installed
- [ ] Verify TanStack Start/Query/Router installed
- [ ] Verify Shadcn UI components

### Database Setup
- [ ] Create PostgreSQL database (Neon/Supabase)
- [ ] Add DATABASE_URL to Doppler
- [ ] Add DATABASE_URL_ADMIN to Doppler
- [ ] Generate initial migration: `bun run db:generate`
- [ ] Apply migration: `doppler run --config dev -- bun run db:migrate`

### Authentication
- [ ] Configure better-auth in src/lib/server/auth.ts
- [ ] Add BETTER_AUTH_SECRET to Doppler
- [ ] Add BETTER_AUTH_URL to Doppler
- [ ] Set up OAuth providers (if needed)
- [ ] Test auth flow locally

## Backend Setup (FastAPI)

### Directory Structure
- [ ] Verify app/ structure (routers, services, db, etc.)
- [ ] Verify tests/ organization (unit, integration, e2e)
- [ ] Verify alembic/ for migrations

### Configuration Files
- [ ] Update pyproject.toml (project name, dependencies)
- [ ] Verify Ruff configuration (130 char line length)
- [ ] Verify mypy configuration (strict type checking)
- [ ] Verify pytest configuration (markers, coverage >80%)
- [ ] Update alembic.ini (database URL from Doppler)
- [ ] Create Taskfile.yml (common commands)

### Dependencies
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install deps: `pip install -r requirements.txt`
- [ ] Install dev deps: `pip install -r requirements-dev.txt`
- [ ] Verify SQLModel installed
- [ ] Verify FastAPI installed
- [ ] Verify Alembic installed

### Database Setup
- [ ] Create PostgreSQL database (Neon/Supabase)
- [ ] Add DATABASE_URL to Doppler
- [ ] Add DATABASE_URL_ADMIN to Doppler
- [ ] Generate initial migration: `alembic revision --autogenerate -m "Initial"`
- [ ] Apply migration: `doppler run --config dev -- alembic upgrade head`

## GitHub Setup

### Repository
- [ ] Create GitHub repository
- [ ] Push initial commit
- [ ] Set up branch protection rules (main branch)
- [ ] Require PR before merging
- [ ] Require 1 approval
- [ ] Require status checks to pass

### GitHub Actions
- [ ] Add DOPPLER_TOKEN to repository secrets
- [ ] Add CLOUDFLARE_API_TOKEN to repository secrets (if deploying)
- [ ] Verify .github/workflows/ci.yml
- [ ] Verify .github/workflows/deploy.yml
- [ ] Test CI/CD pipeline

## Testing

### Frontend Testing
- [ ] Run unit tests: `bun test`
- [ ] Run integration tests: `bun test:integration`
- [ ] Run E2E tests: `bun test:e2e`
- [ ] Verify coverage >80%

### Backend Testing
- [ ] Run unit tests: `pytest -m unit`
- [ ] Run integration tests: `pytest -m integration`
- [ ] Run E2E tests: `pytest -m e2e`
- [ ] Verify coverage >80%

## Documentation

### README.md
- [ ] Update project name and description
- [ ] Document getting started steps
- [ ] Document Doppler setup
- [ ] Document database setup
- [ ] Document testing commands
- [ ] Document deployment process

### Additional Docs
- [ ] Create API documentation (if applicable)
- [ ] Document architecture decisions
- [ ] Document multi-tenant setup
- [ ] Create onboarding guide

## Deployment

### Cloudflare Workers (Frontend)
- [ ] Create wrangler.toml files (dev, staging, production)
- [ ] Create KV namespaces
- [ ] Create R2 buckets (if needed)
- [ ] Configure custom domains
- [ ] Test deployment to staging

### Production Readiness
- [ ] Set up monitoring (Sentry, Axiom)
- [ ] Configure error tracking
- [ ] Set up performance monitoring
- [ ] Configure rate limiting
- [ ] Set up backup strategy
- [ ] Document rollback procedure

## Post-Setup

### Team Onboarding
- [ ] Share Doppler access with team
- [ ] Share repository access
- [ ] Document local setup process
- [ ] Schedule team walkthrough

### Maintenance
- [ ] Set up dependency update schedule
- [ ] Set up security scanning
- [ ] Schedule regular code reviews
- [ ] Document support procedures
