# Scaffold Quality Checklist

Comprehensive checklist for validating generated scaffolds before delivery.

---

## Configuration Files

### TypeScript Projects

- [ ] **package.json** present with correct project name
- [ ] **tsconfig.json** with strict mode enabled
- [ ] **Scripts** configured (dev, build, test, deploy)
- [ ] **Dependencies** at correct versions
- [ ] **devDependencies** include linting/testing tools

### Python Projects

- [ ] **pyproject.toml** present with project metadata
- [ ] **Dependencies** specified with version ranges
- [ ] **Dev dependencies** include pytest, ruff, mypy
- [ ] **Tool configurations** (ruff, mypy, pytest) configured

### All Projects

- [ ] **.gitignore** includes node_modules, .env, build artifacts
- [ ] **.env.example** provided for environment variables
- [ ] **README.md** with setup instructions
- [ ] **License file** (if applicable)

---

## Source Code Structure

### Directory Organization

- [ ] **src/** directory exists
- [ ] **routes/** for API endpoints or pages
- [ ] **components/** for UI components (frontend)
- [ ] **services/** for business logic
- [ ] **utils/** for helper functions
- [ ] **types/** for TypeScript definitions

### Entry Points

- [ ] **Main file** exists (index.ts, main.py, App.tsx)
- [ ] **Exports** correctly configured
- [ ] **Health check endpoint** implemented
- [ ] **Error handling** middleware included

---

## Code Quality

### TypeScript

- [ ] **Strict mode** enabled in tsconfig.json
- [ ] **Type annotations** on all functions
- [ ] **Interfaces** defined for props/config
- [ ] **ESLint** configuration present
- [ ] **Prettier** configuration present
- [ ] **No `any` types** (except explicit)

### Python

- [ ] **Type hints** on all functions
- [ ] **Pydantic models** for validation
- [ ] **Async/await** used correctly
- [ ] **Docstrings** on public functions
- [ ] **Ruff configuration** present
- [ ] **mypy strict mode** enabled

### All Languages

- [ ] **Consistent naming** (camelCase, snake_case)
- [ ] **No hard-coded secrets** or API keys
- [ ] **Environment variables** used correctly
- [ ] **Error handling** implemented
- [ ] **Logging** configured

---

## Testing

### Test Files

- [ ] **tests/** directory exists
- [ ] **Test files** mirror src/ structure
- [ ] **Test fixtures** configured (conftest.py, setup.ts)
- [ ] **Coverage** configuration present

### Test Quality

- [ ] **Sample tests** included
- [ ] **Tests pass** out of the box
- [ ] **Health check test** present
- [ ] **Test commands** in package.json/pyproject.toml

---

## Deployment

### Cloudflare Workers

- [ ] **wrangler.toml** configured
- [ ] **Database bindings** defined (if D1)
- [ ] **Environment** sections (production, staging)
- [ ] **Secrets** documented in README

### Cloudflare Pages

- [ ] **Build command** configured
- [ ] **Output directory** specified
- [ ] **Environment variables** documented

### Python

- [ ] **Dockerfile** (if containerized)
- [ ] **Requirements** frozen
- [ ] **Database migrations** configured (Alembic)

---

## Documentation

### README.md

- [ ] **Project description** clear
- [ ] **Quick start** instructions
- [ ] **Setup steps** documented
- [ ] **Development** commands listed
- [ ] **Deployment** instructions
- [ ] **Environment variables** documented
- [ ] **API endpoints** listed (if API)

### Additional Docs

- [ ] **Architecture** diagram/description (full-stack)
- [ ] **API documentation** (FastAPI auto-docs, etc.)
- [ ] **Contributing** guidelines (if open source)

---

## Security

### Secrets Management

- [ ] **No secrets** committed to git
- [ ] **.env** in .gitignore
- [ ] **.env.example** provided
- [ ] **Secret management** documented

### Authentication

- [ ] **Auth middleware** included (if applicable)
- [ ] **JWT handling** implemented correctly
- [ ] **CORS** configured properly

### Input Validation

- [ ] **Zod/Pydantic** validation on inputs
- [ ] **SQL injection** prevention (parameterized queries)
- [ ] **XSS prevention** (sanitized outputs)

---

## Dependencies

### Version Management

- [ ] **Package versions** pinned or ranged appropriately
- [ ] **No deprecated** packages
- [ ] **Security** vulnerabilities checked
- [ ] **License** compatibility verified

### Peer Dependencies

- [ ] **React version** compatible (if React)
- [ ] **Node version** specified (engines field)
- [ ] **Python version** specified (requires-python)

---

## CI/CD

### GitHub Actions

- [ ] **.github/workflows/** directory exists
- [ ] **Test workflow** configured
- [ ] **Deploy workflow** configured
- [ ] **Lint workflow** configured

### Workflow Quality

- [ ] **Tests run** on PR
- [ ] **Deployment** on main branch
- [ ] **Secrets** properly configured
- [ ] **Environment variables** set

---

## User Experience

### Developer Experience

- [ ] **Setup time** < 5 minutes
- [ ] **All commands work** (dev, test, build)
- [ ] **Hot reload** functional
- [ ] **Error messages** helpful

### Production Readiness

- [ ] **Health endpoint** returns 200
- [ ] **Error handling** doesn't expose internals
- [ ] **Logging** configured
- [ ] **Monitoring** hooks present

---

## Checklist Summary

### Must Have (Critical)

- ✅ Configuration files present and correct
- ✅ Source code structure follows Grey Haven conventions
- ✅ Tests included and passing
- ✅ README with setup instructions
- ✅ No secrets committed

### Should Have (Important)

- ✅ Type safety (TypeScript strict, Python type hints)
- ✅ Linting and formatting configured
- ✅ CI/CD pipeline included
- ✅ Health check endpoint
- ✅ Error handling

### Nice to Have (Optional)

- ✅ Architecture documentation
- ✅ API documentation
- ✅ Storybook (components)
- ✅ Database migrations
- ✅ Monitoring setup

---

## Quick Validation Script

```bash
#!/bin/bash
# Quick scaffold validation

echo "Checking scaffold quality..."

# Check files exist
test -f package.json && echo "✅ package.json" || echo "❌ package.json"
test -f README.md && echo "✅ README.md" || echo "✅ README.md"
test -d src && echo "✅ src/" || echo "❌ src/"
test -d tests && echo "✅ tests/" || echo "❌ tests/"

# Check no secrets
! grep -r "api[_-]key" . && echo "✅ No API keys" || echo "⚠️  API key found"

# Install and test
npm install && npm test && echo "✅ Tests pass" || echo "❌ Tests fail"
```

---

**Version**: 1.0
**Last Updated**: 2024-01-15
