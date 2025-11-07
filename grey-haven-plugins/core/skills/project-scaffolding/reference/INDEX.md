# Project Scaffolder Reference

Complete reference for Grey Haven project scaffolding - conventions, specifications, and tooling.

---

## Navigation

| Reference | Description |
|-----------|-------------|
| [Grey Haven Conventions](grey-haven-conventions.md) | Naming, structure, and code standards |
| [Scaffold Specifications](scaffold-specifications.md) | Technical specs for each scaffold type |
| [Tooling Configurations](tooling-configurations.md) | Config files for Vite, Wrangler, pytest, etc. |

---

## Quick Reference

### Grey Haven Stack

| Layer | Technology | Use Case |
|-------|------------|----------|
| **Frontend** | React + Vite + TanStack | Web applications |
| **Backend** | Cloudflare Workers + Hono | REST/GraphQL APIs |
| **Database** | PlanetScale PostgreSQL (or D1) | Relational data |
| **Validation** | Zod (TS), Pydantic (Python) | Type-safe validation |
| **Testing** | Vitest (TS), pytest (Python) | Unit & integration tests |
| **Deployment** | Cloudflare Pages + Workers | Global edge deployment |

### Naming Conventions

```
Components:     PascalCase   (Button, UserProfile)
Files:          kebab-case   (user-profile.tsx, api-client.ts)
Variables:      camelCase    (userId, isActive)
Constants:      UPPER_SNAKE  (API_URL, MAX_RETRIES)
Database:       snake_case   (user_profiles, api_keys)
Routes:         kebab-case   (/api/user-profiles)
```

### Folder Structure

```
src/
├── routes/        # API endpoints or page routes
├── components/    # Reusable UI components
├── services/      # Business logic
├── utils/         # Pure helper functions
├── types/         # TypeScript type definitions
└── lib/           # Third-party integrations

tests/             # Mirror src/ structure
├── routes/
├── components/
└── services/
```

### Configuration Standards

**TypeScript Projects**:
- Strict mode enabled
- ESLint with recommended rules
- Prettier for formatting
- Vitest for testing
- Path aliases (`@/` for src/)

**Python Projects**:
- Python 3.11+
- uv for package management
- Ruff for linting
- mypy for type checking
- pytest for testing

---

## Scaffold Templates

### Minimum Files Required

**Cloudflare Worker**:
- wrangler.toml
- package.json
- tsconfig.json
- src/index.ts
- tests/

**React App**:
- package.json
- vite.config.ts
- tsconfig.json
- src/main.tsx
- src/routes/
- tests/

**Python API**:
- pyproject.toml
- app/main.py
- app/schemas/
- app/models/
- tests/

---

## Tooling Versions

### Recommended Versions (2024)

```json
{
  "typescript": "^5.3.0",
  "vite": "^5.0.0",
  "react": "^18.2.0",
  "hono": "^4.0.0",
  "wrangler": "^3.25.0",
  "vitest": "^1.2.0"
}
```

```toml
# Python (pyproject.toml)
[project]
requires-python = ">=3.11"
dependencies = [
  "fastapi[standard]>=0.109.0",
  "pydantic>=2.5.0",
  "uvicorn>=0.27.0"
]
```

---

## Best Practices

### DO

- ✅ Use TypeScript strict mode
- ✅ Include tests in scaffold
- ✅ Configure linting and formatting
- ✅ Add .gitignore
- ✅ Include README with setup instructions
- ✅ Add CI/CD configuration
- ✅ Use environment variables for secrets
- ✅ Include health check endpoint

### DON'T

- ❌ Commit node_modules or .venv
- ❌ Hard-code secrets or API keys
- ❌ Skip type definitions
- ❌ Omit error handling
- ❌ Forget database migrations
- ❌ Skip documentation

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing
- [ ] TypeScript/mypy checks pass
- [ ] Linting passes
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Secrets set in production
- [ ] Build succeeds
- [ ] Health check endpoint working

### Post-Deployment

- [ ] Health check returns 200
- [ ] API endpoints accessible
- [ ] Database connections working
- [ ] Authentication functioning
- [ ] Monitoring enabled
- [ ] Error tracking active
- [ ] Logs accessible

---

## Common Issues

### Issue: TypeScript errors after scaffold

**Solution**: Run `npm install` and ensure tsconfig.json is correct

### Issue: Wrangler fails to deploy

**Solution**: Check wrangler.toml config and Cloudflare authentication

### Issue: Database connection fails

**Solution**: Verify connection string and database credentials

### Issue: Tests fail after scaffold

**Solution**: Check test setup and mock configuration

---

**Total References**: 3 comprehensive guides
**Coverage**: Conventions, specifications, configurations
**Standards**: Production-ready Grey Haven stack
