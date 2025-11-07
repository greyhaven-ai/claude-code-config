# Project Scaffolder Examples

Real-world examples of scaffolding production-ready projects with Grey Haven stack.

---

## Quick Navigation

### Scaffold Types

| Example | Stack | Time | Files | Description |
|---------|-------|------|-------|-------------|
| [Cloudflare Worker API](cloudflare-worker-scaffold-example.md) | Hono + TypeScript + D1 | 15 min | 18 | Production API with auth, logging, tests |
| [React Component](react-component-scaffold-example.md) | React + TypeScript + Vitest | 5 min | 6 | Reusable component with tests, stories |
| [Python API](python-api-scaffold-example.md) | FastAPI + Pydantic + PostgreSQL | 20 min | 22 | Async API with validation, migrations |
| [Full-Stack App](full-stack-scaffold-example.md) | React + Worker + D1 | 30 min | 35 | Complete app with frontend/backend |

---

## What's Included in Each Example

### Structure
- **Complete file tree** - Every file that gets created
- **Configuration files** - Package management, tooling, deployment
- **Source code** - Production-ready starting point
- **Tests** - Pre-written test suites
- **Documentation** - README with next steps

### Tooling
- **Type Safety** - TypeScript strict mode, Pydantic validation
- **Testing** - Vitest for TS/JS, pytest for Python
- **Linting** - ESLint, Prettier, Ruff
- **CI/CD** - GitHub Actions workflows
- **Deployment** - Cloudflare Pages/Workers config

---

## Scaffold Comparison

### When to Use Each

| Use Case | Scaffold | Why |
|----------|----------|-----|
| **REST API** | Cloudflare Worker | Fast, serverless, global edge deployment |
| **GraphQL API** | Cloudflare Worker | Hono supports GraphQL, D1 for persistence |
| **Web App** | Full-Stack | Frontend + backend in monorepo |
| **Static Site** | React Component | Build with Vite, deploy to Pages |
| **Background Jobs** | Python API | Long-running tasks, async processing |
| **Data Pipeline** | Python API | ETL, data validation with Pydantic |

---

## Quick Reference

### Cloudflare Worker API
```bash
# Generate
scaffold-worker --name my-api

# Structure
my-api/
├── src/
│   ├── index.ts       # Hono app
│   ├── routes/        # API handlers
│   └── middleware/    # Auth, CORS
├── tests/
├── wrangler.toml
└── package.json

# Deploy
cd my-api && npm install && npm run deploy
```

### React Component
```bash
# Generate
scaffold-component --name Button --path src/components

# Structure
src/components/Button/
├── Button.tsx         # Implementation
├── Button.test.tsx    # Tests
├── Button.stories.tsx # Storybook
└── Button.module.css  # Styles
```

### Python API
```bash
# Generate
scaffold-python --name my-api

# Structure
my-api/
├── app/
│   ├── main.py        # FastAPI
│   ├── schemas/       # Pydantic
│   └── models/        # SQLAlchemy
├── tests/
├── pyproject.toml
└── alembic/

# Run
cd my-api && uv venv && uv pip install -e .[dev] && uvicorn app.main:app
```

### Full-Stack App
```bash
# Generate
scaffold-fullstack --name my-app

# Structure
my-app/
├── frontend/          # React + Vite
├── backend/           # Worker
└── docs/

# Dev
cd my-app && npm install && npm run dev
```

---

## Common Patterns

### All Scaffolds Include

**Configuration**:
- ✅ TypeScript/Python type checking
- ✅ Linting (ESLint/Ruff)
- ✅ Formatting (Prettier)
- ✅ Testing framework
- ✅ Git ignore rules

**Development**:
- ✅ Local development server
- ✅ Hot reload
- ✅ Environment variables
- ✅ Debug configuration

**Production**:
- ✅ Build optimization
- ✅ Deployment configuration
- ✅ Error handling
- ✅ Logging setup

---

## Grey Haven Conventions Applied

### Naming
- Components: `PascalCase` (Button, UserProfile)
- Files: `kebab-case` for routes, `PascalCase` for components
- Variables: `camelCase` (userId, isActive)
- Constants: `UPPER_SNAKE_CASE` (API_URL, MAX_RETRIES)
- Database: `snake_case` (user_profiles, api_keys)

### Structure
```
src/
├── routes/        # API endpoints or page routes
├── components/    # Reusable UI components
├── services/      # Business logic
├── utils/         # Pure helper functions
└── types/         # TypeScript type definitions

tests/             # Mirror src/ structure
├── routes/
├── components/
└── services/
```

### Dependencies
- **Package Manager**: npm (Node.js), uv (Python)
- **Frontend**: Vite + React + TypeScript + TanStack
- **Backend**: Cloudflare Workers + Hono
- **Database**: PlanetScale PostgreSQL
- **Testing**: Vitest (TS), pytest (Python)
- **Validation**: Zod (TS), Pydantic (Python)

---

## Metrics

### Scaffold Generation Speed

| Scaffold | Files Created | LOC | Time |
|----------|--------------|-----|------|
| Cloudflare Worker | 18 | ~450 | 15 min |
| React Component | 6 | ~120 | 5 min |
| Python API | 22 | ~600 | 20 min |
| Full-Stack | 35 | ~850 | 30 min |

### Developer Productivity Gains

**Before Scaffolding**:
- Setup time: 2-4 hours
- Configuration errors: Common
- Inconsistent structure: Yes
- Missing best practices: Often

**After Scaffolding**:
- Setup time: 5-30 minutes
- Configuration errors: Rare
- Consistent structure: Always
- Best practices: Built-in

**Time Savings**: 80-90% reduction in project setup time

---

## Next Steps

After scaffolding:

1. **Review generated code** - Understand structure and conventions
2. **Customize for your needs** - Modify templates, add features
3. **Run tests** - Verify everything works: `npm test` or `pytest`
4. **Start development** - Add your business logic
5. **Deploy** - Use provided deployment configuration

---

**Total Examples**: 4 complete scaffold types
**Coverage**: Frontend, backend, full-stack, component
**Tooling**: Modern Grey Haven stack with best practices
