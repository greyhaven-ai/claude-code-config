# Testing Reference

Complete configurations, project structures, and setup guides for Grey Haven testing infrastructure.

## Table of Contents

- [TypeScript Configuration](#typescript-configuration)
- [Python Configuration](#python-configuration)
- [Project Structures](#project-structures)
- [Doppler Configuration](#doppler-configuration)
- [GitHub Actions Configuration](#github-actions-configuration)
- [Coverage Configuration](#coverage-configuration)

## TypeScript Configuration

### Complete vitest.config.ts

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    // Enable global test APIs (describe, it, expect)
    globals: true,

    // Use jsdom for browser-like environment
    environment: "jsdom",

    // Run setup file before tests
    setupFiles: ["./tests/setup.ts"],

    // Coverage configuration
    coverage: {
      // Use V8 coverage provider (faster than Istanbul)
      provider: "v8",

      // Coverage reporters
      reporter: ["text", "json", "html"],

      // Exclude from coverage
      exclude: [
        "node_modules/",
        "tests/",
        "**/*.config.ts",
        "**/*.d.ts",
        "**/types/",
        "**/__mocks__/",
      ],

      // Minimum coverage thresholds (enforced in CI)
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },

    // Environment variables for tests
    env: {
      // Doppler provides these at runtime
      DATABASE_URL_ADMIN: process.env.DATABASE_URL_ADMIN || "postgresql://localhost/test",
      REDIS_URL: process.env.REDIS_URL || "redis://localhost:6379",
      VITE_API_URL: process.env.VITE_API_URL || "http://localhost:3000",
    },

    // Test timeout (ms)
    testTimeout: 10000,

    // Hook timeouts
    hookTimeout: 10000,

    // Retry failed tests
    retry: 0,

    // Run tests in parallel
    threads: true,

    // Maximum concurrent threads
    maxThreads: 4,

    // Minimum concurrent threads
    minThreads: 1,
  },

  // Path aliases
  resolve: {
    alias: {
      "~": path.resolve(__dirname, "./src"),
    },
  },
});
```

**Field Explanations:**

- `globals: true` - Makes test APIs available without imports
- `environment: "jsdom"` - Simulates browser environment for React components
- `setupFiles` - Runs before each test file
- `coverage.provider: "v8"` - Fast coverage using V8 engine
- `coverage.thresholds` - Enforces minimum coverage percentages
- `testTimeout: 10000` - Each test must complete within 10 seconds
- `threads: true` - Run tests in parallel for speed
- `retry: 0` - Don't retry failed tests (fail fast)

### Test Setup File (tests/setup.ts)

```typescript
// tests/setup.ts
import { afterEach, beforeAll, afterAll, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

// Cleanup after each test case
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// Setup before all tests
beforeAll(() => {
  // Mock environment variables
  process.env.VITE_API_URL = "http://localhost:3000";
  process.env.DATABASE_URL_ADMIN = "postgresql://localhost/test";

  // Mock window.matchMedia (for responsive components)
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });

  // Mock IntersectionObserver
  global.IntersectionObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  }));
});

// Cleanup after all tests
afterAll(async () => {
  // Close database connections
  // Clean up any resources
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/react": "^14.1.2",
    "@testing-library/user-event": "^14.5.1",
    "@vitest/ui": "^1.0.4",
    "@faker-js/faker": "^8.3.1",
    "vitest": "^1.0.4",
    "@vitest/coverage-v8": "^1.0.4"
  }
}
```

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",

  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000",
    trace: "on-first-retry",
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
  ],

  webServer: {
    command: "bun run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
```

## Python Configuration

### Complete pyproject.toml

```toml
# pyproject.toml

[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Command line options
addopts = [
    "--strict-markers",       # Error on unknown markers
    "--strict-config",        # Error on config errors
    "-ra",                    # Show extra test summary
    "--cov=app",             # Measure coverage of app/ directory
    "--cov-report=term-missing",  # Show missing lines in terminal
    "--cov-report=html",     # Generate HTML coverage report
    "--cov-report=xml",      # Generate XML for CI tools
    "--cov-fail-under=80",   # Fail if coverage < 80%
    "-v",                    # Verbose output
]

# Test markers (use with @pytest.mark.unit, etc.)
markers = [
    "unit: Fast, isolated unit tests",
    "integration: Tests involving multiple components",
    "e2e: End-to-end tests through full flows",
    "benchmark: Performance tests",
    "slow: Tests that take >5 seconds",
]

# Async support
asyncio_mode = "auto"

# Test output
console_output_style = "progress"

# Warnings
filterwarnings = [
    "error",                                    # Treat warnings as errors
    "ignore::DeprecationWarning",              # Ignore deprecation warnings
    "ignore::PendingDeprecationWarning",       # Ignore pending deprecations
]

# Coverage configuration
[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/conftest.py",
    "*/__init__.py",
    "*/migrations/*",
    "*/config/*",
]
branch = true
parallel = true

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "def __str__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

**Configuration Explanations:**

- `testpaths = ["tests"]` - Only look for tests in tests/ directory
- `--strict-markers` - Fail if test uses undefined marker
- `--cov=app` - Measure coverage of app/ directory
- `--cov-fail-under=80` - CI fails if coverage < 80%
- `asyncio_mode = "auto"` - Auto-detect async tests
- `branch = true` - Measure branch coverage (more thorough)
- `parallel = true` - Support parallel test execution

### Development Dependencies

```txt
# requirements-dev.txt

# Testing
pytest==8.0.0
pytest-asyncio==0.23.3
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-benchmark==4.0.0

# Test utilities
faker==22.0.0
factory-boy==3.3.0
httpx==0.26.0

# Type checking
mypy==1.8.0

# Linting
ruff==0.1.9

# Task runner
taskipy==1.12.2
```

### Taskfile Configuration

```toml
# pyproject.toml (continued)

[tool.taskipy.tasks]
# Testing tasks
test = "doppler run -- pytest"
test-unit = "doppler run -- pytest -m unit"
test-integration = "doppler run -- pytest -m integration"
test-e2e = "doppler run -- pytest -m e2e"
test-benchmark = "doppler run -- pytest -m benchmark"
test-coverage = "doppler run -- pytest --cov=app --cov-report=html"
test-watch = "doppler run -- pytest-watch"

# Linting and formatting
lint = "ruff check app tests"
format = "ruff format app tests"
typecheck = "mypy app"

# Combined checks
check = "task lint && task typecheck && task test"
```

## Project Structures

### TypeScript Project Structure

```plaintext
project-root/
├── src/
│   ├── routes/                     # TanStack Router pages
│   │   ├── index.tsx
│   │   ├── settings/
│   │   │   ├── profile.tsx
│   │   │   └── account.tsx
│   │   └── __root.tsx
│   ├── lib/
│   │   ├── components/             # React components
│   │   │   ├── auth/
│   │   │   │   ├── provider.tsx
│   │   │   │   └── login-form.tsx
│   │   │   ├── ui/                # UI primitives (shadcn)
│   │   │   │   ├── button.tsx
│   │   │   │   └── input.tsx
│   │   │   └── UserProfile.tsx
│   │   ├── server/                # Server-side code
│   │   │   ├── db/
│   │   │   │   ├── schema.ts      # Drizzle schema
│   │   │   │   └── index.ts       # DB connection
│   │   │   └── functions/         # Server functions
│   │   │       ├── users.ts
│   │   │       └── auth.ts
│   │   ├── hooks/                 # Custom React hooks
│   │   │   ├── use-auth.ts
│   │   │   └── use-users.ts
│   │   ├── utils/                 # Utility functions
│   │   │   ├── format.ts
│   │   │   └── validation.ts
│   │   └── types/                 # TypeScript types
│   │       ├── user.ts
│   │       └── api.ts
│   └── public/                    # Static assets
│       └── favicon.ico
├── tests/
│   ├── setup.ts                   # Test setup
│   ├── unit/                      # Unit tests
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   └── UserProfile.test.tsx
│   │   │   └── utils/
│   │   │       └── format.test.ts
│   │   └── server/
│   │       └── functions/
│   │           └── users.test.ts
│   ├── integration/               # Integration tests
│   │   ├── auth-flow.test.ts
│   │   └── user-repository.test.ts
│   ├── e2e/                      # Playwright E2E tests
│   │   ├── user-registration.spec.ts
│   │   └── user-workflow.spec.ts
│   └── factories/                # Test data factories
│       ├── user.factory.ts
│       └── tenant.factory.ts
├── vitest.config.ts              # Vitest configuration
├── playwright.config.ts          # Playwright configuration
├── package.json
└── tsconfig.json
```

### Python Project Structure

```plaintext
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Application settings
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                # Database connection
│   │   ├── models/                # SQLModel entities
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base model
│   │   │   ├── user.py
│   │   │   └── tenant.py
│   │   └── repositories/          # Repository pattern
│   │       ├── __init__.py
│   │       ├── base.py            # Base repository
│   │       └── user_repository.py
│   ├── routers/                   # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── auth.py
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── auth_service.py
│   ├── schemas/                   # Pydantic schemas (API contracts)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── auth.py
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── security.py
│       └── validation.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Shared fixtures
│   ├── unit/                     # Unit tests (@pytest.mark.unit)
│   │   ├── __init__.py
│   │   ├── repositories/
│   │   │   └── test_user_repository.py
│   │   └── services/
│   │       └── test_user_service.py
│   ├── integration/              # Integration tests
│   │   ├── __init__.py
│   │   └── test_user_api.py
│   ├── e2e/                     # E2E tests
│   │   ├── __init__.py
│   │   └── test_full_user_flow.py
│   ├── benchmark/               # Benchmark tests
│   │   ├── __init__.py
│   │   └── test_repository_performance.py
│   └── factories/               # Test data factories
│       ├── __init__.py
│       └── user_factory.py
├── pyproject.toml               # Python project config
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
└── .python-version             # Python version (3.12)
```

## Doppler Configuration

### Doppler Setup

```bash
# Install Doppler CLI
brew install dopplerhq/cli/doppler  # macOS
# or
curl -Ls https://cli.doppler.com/install.sh | sh  # Linux

# Authenticate with Doppler
doppler login

# Setup Doppler in project
doppler setup

# Select project and config
# Project: your-project-name
# Config: test (or dev, staging, production)
```

### Doppler Environment Configs

Grey Haven projects use these Doppler configs:

1. **dev** - Local development environment
2. **test** - Running tests (CI and local)
3. **staging** - Staging environment
4. **production** - Production environment

### Test Environment Variables

**Database URLs:**

```bash
# PostgreSQL connection URLs (Doppler managed)
DATABASE_URL_ADMIN=postgresql+asyncpg://admin_user:password@localhost:5432/app_db
DATABASE_URL_AUTHENTICATED=postgresql+asyncpg://authenticated_user:password@localhost:5432/app_db
DATABASE_URL_ANON=postgresql+asyncpg://anon_user:password@localhost:5432/app_db

# Test database (separate from dev)
DATABASE_URL_TEST=postgresql+asyncpg://test_user:password@localhost:5432/test_db
```

**Redis:**

```bash
# Use separate Redis DB for tests (0-15 available)
REDIS_URL=redis://localhost:6379/1  # DB 1 for tests (dev uses 0)
```

**Authentication:**

```bash
# Better Auth secrets
BETTER_AUTH_SECRET=test-secret-key-min-32-chars-long
BETTER_AUTH_URL=http://localhost:3000

# JWT secrets
JWT_SECRET_KEY=test-jwt-secret-key
```

**External Services (use test/sandbox keys):**

```bash
# Stripe (test mode)
STRIPE_SECRET_KEY=sk_test_51AbCdEfGhIjKlMnOpQrStUv
STRIPE_PUBLISHABLE_KEY=pk_test_51AbCdEfGhIjKlMnOpQrStUv

# Resend (test mode)
RESEND_API_KEY=re_test_1234567890abcdef

# OpenAI (separate test key)
OPENAI_API_KEY=sk-test-1234567890abcdef
```

**E2E Testing:**

```bash
# Playwright base URL
PLAYWRIGHT_BASE_URL=http://localhost:3000

# Email testing service (for E2E tests)
MAILTRAP_API_TOKEN=your_mailtrap_token
```

### Running Tests with Doppler

**TypeScript:**

```bash
# Run all tests with Doppler
doppler run -- bun run test

# Run with specific config
doppler run --config test -- bun run test

# Run coverage
doppler run -- bun run test:coverage

# Run E2E
doppler run -- bun run test:e2e
```

**Python:**

```bash
# Activate virtual environment first!
source .venv/bin/activate

# Run all tests with Doppler
doppler run -- pytest

# Run with specific config
doppler run --config test -- pytest

# Run specific markers
doppler run -- pytest -m unit
doppler run -- pytest -m integration
```

### Doppler in CI/CD

**GitHub Actions:**

```yaml
- name: Install Doppler CLI
  uses: dopplerhq/cli-action@v3

- name: Run tests with Doppler
  env:
    DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
  run: doppler run --config test -- bun run test:coverage
```

**Get Doppler Service Token:**

1. Go to Doppler dashboard
2. Select your project
3. Go to Access → Service Tokens
4. Create token for `test` config
5. Add as `DOPPLER_TOKEN_TEST` secret in GitHub

## GitHub Actions Configuration

### TypeScript CI Workflow

```yaml
# .github/workflows/test-typescript.yml
name: TypeScript Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "bun"

      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3

      - name: Install dependencies
        run: bun install

      - name: Run linter
        run: bun run lint

      - name: Run type check
        run: bun run typecheck

      - name: Run unit tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: doppler run --config test -- bun run test:unit

      - name: Run integration tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: doppler run --config test -- bun run test:integration

      - name: Run tests with coverage
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: doppler run --config test -- bun run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json
          flags: typescript
          name: typescript-coverage

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: doppler run --config test -- bun run test:e2e

      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Python CI Workflow

```yaml
# .github/workflows/test-python.yml
name: Python Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3

      - name: Create virtual environment
        run: python -m venv .venv

      - name: Install dependencies
        run: |
          source .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt -r requirements-dev.txt

      - name: Run linter
        run: |
          source .venv/bin/activate
          ruff check app tests

      - name: Run type checker
        run: |
          source .venv/bin/activate
          mypy app

      - name: Run unit tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: |
          source .venv/bin/activate
          doppler run --config test -- pytest -m unit

      - name: Run integration tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: |
          source .venv/bin/activate
          doppler run --config test -- pytest -m integration

      - name: Run all tests with coverage
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: |
          source .venv/bin/activate
          doppler run --config test -- pytest --cov=app --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
          flags: python
          name: python-coverage

      - name: Upload coverage HTML
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
          retention-days: 30
```

## Coverage Configuration

### Coverage Thresholds

**Minimum requirements (enforced in CI):**

- **Lines:** 80%
- **Functions:** 80%
- **Branches:** 80%
- **Statements:** 80%

**Target goals:**

- **Critical paths:** 90%+
- **Security code:** 100% (auth, payments, tenant isolation)
- **Utility functions:** 95%+

### Excluding from Coverage

**TypeScript (vitest.config.ts):**

```typescript
coverage: {
  exclude: [
    "node_modules/",
    "tests/",
    "**/*.config.ts",
    "**/*.d.ts",
    "**/types/",
    "**/__mocks__/",
    "**/migrations/",
  ],
}
```

**Python (pyproject.toml):**

```toml
[tool.coverage.run]
omit = [
    "*/tests/*",
    "*/conftest.py",
    "*/__init__.py",
    "*/migrations/*",
    "*/config/*",
]
```

### Coverage Reports

**Viewing coverage locally:**

```bash
# TypeScript
bun run test:coverage
open coverage/index.html

# Python
source .venv/bin/activate
doppler run -- pytest --cov=app --cov-report=html
open htmlcov/index.html
```

**Coverage in CI:**

- Upload to Codecov for tracking over time
- Fail build if coverage < 80%
- Comment coverage diff on PRs
- Track coverage trends

### Pre-commit Hook for Coverage

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: test-coverage
        name: Check test coverage
        entry: sh -c 'source .venv/bin/activate && pytest --cov=app --cov-fail-under=80'
        language: system
        pass_filenames: false
        always_run: true
```
