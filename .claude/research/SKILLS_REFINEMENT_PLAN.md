# Skills Refinement Plan

**Date**: 2025-10-20
**Purpose**: Refine Grey Haven Skills based on actual template repository analysis

## Analysis Summary

I examined two key template repositories to understand Grey Haven's actual coding standards:

1. **cvi-template** - TypeScript/React frontend template
2. **cvi-backend-template** - Python/FastAPI backend template

## Key Findings

### TypeScript/React Standards (cvi-template)

**Prettier Configuration**:
- Tab width: 2 spaces
- Semicolons: Required
- Print width: 90 characters (NOT 100 or 120)
- Single quotes: FALSE (use double quotes)
- Trailing commas: ALL
- Plugins: organize-imports, tailwindcss

**ESLint Rules**:
- Extends: eslint:recommended, @typescript-eslint/recommended, react-hooks/recommended
- `no-explicit-any`: OFF (allows `any` type)
- `no-unused-vars`: OFF (both TS and vanilla)
- `react-hooks/exhaustive-deps`: OFF
- `react-refresh/only-export-components`: OFF

**TypeScript Config**:
- Strict mode: TRUE
- Module: ESNext
- Module resolution: Bundler
- Target: ES2022
- Path aliases: `~/*` → `./src/*`

**Commitlint**:
- Conventional commits enforced
- Header max length: 100 characters (NOT 72)
- Subject case: lowercase, no sentence-case/start-case/pascal-case/upper-case
- Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert

**Project Structure**:
```
src/
├── routes/              # TanStack Router file-based routing
├── lib/
│   ├── components/
│   │   ├── ui/          # Shadcn UI components
│   │   └── [features]   # Feature-specific components
│   ├── server/
│   │   ├── schema/      # Database schema (snake_case)
│   │   ├── functions/   # Server functions
│   │   └── auth.ts      # Better-auth configuration
│   ├── config/          # Environment validation
│   └── middleware/      # Route guards
```

**Tech Stack**:
- TanStack Start, Router, Query
- React 19
- Better-auth (passkeys, magic links, OAuth)
- Drizzle ORM with Neon PostgreSQL
- Tailwind CSS v4 + Shadcn UI
- Redis for caching/sessions
- Cloudflare Workers deployment

**Key Patterns**:
- Multi-tenant via `tenantId` field
- Row Level Security (RLS) with JWT tokens
- Database fields: **snake_case** (CRITICAL!)
- Server functions for all mutations
- TanStack Query with 1-minute stale time
- Environment vars: client prefixed with `VITE_`

### Python/FastAPI Standards (cvi-backend-template)

**Ruff Configuration**:
- Line length: 130 characters (NOT 80 or 88)
- Indent width: 4 spaces
- fix-only: true
- show-fixes: true

**MyPy Configuration**:
- Python version: 3.11 (but pyproject.toml requires >=3.12,<3.13)
- warn_return_any: true
- warn_unused_configs: true
- disallow_untyped_defs: true
- check_untyped_defs: true

**Pytest Configuration**:
- Test paths: tests/
- Python files: test_*.py
- Python functions: test_*
- Python classes: Test*
- Asyncio mode: auto
- Markers: unit, integration, e2e, benchmark

**Project Structure**:
```
app/
├── config/              # Application settings
├── db/
│   ├── models/          # SQLModel entities
│   └── repositories/    # Repository pattern
├── routers/             # FastAPI endpoints
├── services/            # Business logic
│   └── ai/
│       ├── agents/      # AI agents
│       └── tools/       # Agent tools
├── schemas/             # Pydantic models
├── jobs/                # Temporal workflows
└── utils/               # Utilities
```

**Key Technologies**:
- Python 3.12
- FastAPI with async/await
- SQLAlchemy/SQLModel with PostgreSQL
- Redis caching
- TurboPuffer vector database
- Temporal workflow orchestration
- OpenTelemetry for observability

**Key Patterns**:
- Repository pattern for data access
- Service layer for business logic
- Dependency injection
- Multi-tenant via tenant_id/service_id
- AI agent registry architecture
- Pre-commit hooks required
- Virtual environment: ALWAYS activate before Python commands

## Issues with Current Skills

### 1. code-style Skill

**Current Issues**:
- Suggests 50-72 character line limits (actual: TS=90, Python=130)
- Suggests avoiding `any` type (actual: allowed in Grey Haven projects)
- Says "prefer `const` over `let`" without mentioning tab width, semicolons, etc.
- No mention of Prettier/ESLint/Ruff actual configurations
- No mention of snake_case database fields (CRITICAL for Grey Haven)
- No mention of TanStack patterns (Query, Router, Start)
- No mention of Better-auth patterns
- No mention of Repository pattern for Python

**Missing**:
- Actual Prettier config (90 char width, 2 spaces, double quotes, trailing commas)
- Actual ESLint rules (`any` allowed, unused vars off, exhaustive-deps off)
- Actual Ruff config (130 char width, 4 spaces)
- Database naming: snake_case for fields
- Multi-tenant patterns (tenantId, tenant_id)
- Path aliases (`~/*`)
- Server function patterns
- Row Level Security patterns

### 2. commit-format Skill

**Current Issues**:
- Suggests 72 character subject line (actual: 100 per commitlint.config.cjs)
- Doesn't mention commitlint enforcement
- Subject case rules not specific enough

**Missing**:
- Commitlint configuration reference
- Header max-length: 100
- Subject case rules (no sentence-case, start-case, pascal-case, upper-case)
- Actual enforced types from commitlint.config.cjs

### 3. pr-template Skill

**Seems OK** - General enough to work, but could reference:
- Actual commit types from commitlint
- Testing markers (unit, integration, e2e, benchmark)
- Pre-commit hooks requirement

## Recommended New Skills

### 1. grey-haven-database-conventions

**Purpose**: Database schema and multi-tenant architecture patterns

**Content**:
- Snake_case for all database fields
- Multi-tenant patterns (tenantId/tenant_id)
- Row Level Security (RLS) with JWT
- Drizzle ORM patterns
- SQLModel entity patterns
- Repository pattern implementation
- Migration patterns (Alembic, Drizzle)

### 2. grey-haven-project-structure

**Purpose**: Standard project layouts for TS and Python

**Content**:
- TanStack Start frontend structure
- FastAPI backend structure
- File naming conventions
- Path organization
- Config file locations

### 3. grey-haven-tanstack-patterns

**Purpose**: TanStack ecosystem best practices

**Content**:
- TanStack Router file-based routing
- TanStack Query patterns (stale time, invalidation)
- TanStack Start server functions
- Data fetching patterns
- Route guards and middleware

### 4. grey-haven-testing-standards

**Purpose**: Testing patterns and markers

**Content**:
- Pytest markers (unit, integration, e2e, benchmark)
- Test structure mirroring app structure
- Coverage requirements
- Async test patterns
- Pre-commit hooks

### 5. grey-haven-environment-config

**Purpose**: Environment variable patterns

**Content**:
- @t3-oss/env-core validation
- VITE\_ prefix for client vars
- Doppler integration
- Environment file structure

## Action Items

### High Priority (Do First)

1. **Completely rewrite code-style Skill** with actual configurations
   - Remove generic advice, add SPECIFIC configs
   - Include Prettier settings (90 chars, 2 spaces, double quotes)
   - Include ESLint rules (`any` allowed, etc.)
   - Include Ruff settings (130 chars, 4 spaces)
   - Add snake_case database convention
   - Add multi-tenant patterns

2. **Update commit-format Skill** with actual commitlint rules
   - Change 72 → 100 character limit
   - Add subject case rules
   - Reference commitlint.config.cjs

3. **Create database-conventions Skill**
   - Critical for Grey Haven projects
   - snake_case fields
   - RLS patterns
   - Multi-tenant architecture

### Medium Priority

4. **Create project-structure Skill**
   - TanStack Start structure
   - FastAPI structure
   - File organization

5. **Create tanstack-patterns Skill**
   - Router, Query, Start patterns
   - Server functions
   - Data fetching

### Low Priority

6. **Create testing-standards Skill**
   - Pytest markers
   - Coverage
   - Pre-commit

7. **Create environment-config Skill**
   - Env validation
   - Doppler
   - VITE\_ prefix

## Implementation Plan

### Phase 1: Critical Updates (Today)

1. Rewrite `code-style/SKILL.md` with ACTUAL Grey Haven standards
2. Update `commit-format/SKILL.md` with 100-char limit and commitlint rules
3. Create `database-conventions/SKILL.md`

### Phase 2: Additional Skills (Next)

4. Create `project-structure/SKILL.md`
5. Create `tanstack-patterns/SKILL.md`

### Phase 3: Optional Enhancements (Future)

6. Create `testing-standards/SKILL.md`
7. Create `environment-config/SKILL.md`

## Notes

- All Skills should reference ACTUAL config files from templates
- Include concrete examples from real codebases
- Avoid generic "best practices" - use Grey Haven ACTUAL practices
- Link to template repositories when relevant
- Update plugin.json to include all new Skills

## Template References

- Frontend: `/Users/jayscambler/Repositories/cvi-template`
- Backend: `/Users/jayscambler/Repositories/cvi-backend-template`

Key config files:
- `.prettierrc` - Prettier settings
- `.eslintrc` - ESLint rules
- `tsconfig.json` - TypeScript config
- `commitlint.config.cjs` - Commit message rules
- `pyproject.toml` - Python/Ruff/MyPy settings
- `pytest.ini` - Test configuration
- `CLAUDE.md` - Project-specific guidance
