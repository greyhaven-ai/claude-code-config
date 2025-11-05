---
name: grey-haven-testing-strategy
description: Grey Haven's testing strategy - Vitest unit/integration/e2e for TypeScript, pytest markers for Python, >80% coverage requirement, fixture patterns, and Doppler for test environment variables. Use when writing tests or setting up test infrastructure.
---

# Grey Haven Testing Strategy

Follow Grey Haven Studio's comprehensive testing approach for TypeScript (Vitest) and Python (pytest) projects.

## Testing Philosophy

### Coverage Requirements
- **Minimum: 80% code coverage** for all projects
- **Target: 90%+ coverage** for critical paths
- **100% coverage** for security-critical code (auth, payments, multi-tenant isolation)

### Test Types (Markers)

Grey Haven uses consistent test markers across languages:

1. **unit**: Fast, isolated tests of single functions/classes
2. **integration**: Tests involving multiple components or external dependencies
3. **e2e**: End-to-end tests through full user flows
4. **benchmark**: Performance tests measuring speed/memory

## TypeScript Testing (Vitest)

### Project Structure

```
src/
├── lib/
│   ├── components/
│   │   └── UserProfile.tsx
│   ├── server/
│   │   └── functions/
│   │       └── users.ts
│   └── utils/
│       └── format.ts
tests/
├── unit/                           # Fast, isolated tests
│   ├── lib/
│   │   ├── components/
│   │   │   └── UserProfile.test.tsx
│   │   └── utils/
│   │       └── format.test.ts
│   └── server/
│       └── functions/
│           └── users.test.ts
├── integration/                    # Multi-component tests
│   └── auth-flow.test.ts
└── e2e/                           # Playwright tests
    └── user-registration.spec.ts
```

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "tests/",
        "**/*.config.ts",
        "**/*.d.ts",
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
    // Load environment variables from Doppler for tests
    env: {
      // Doppler provides these at runtime
      DATABASE_URL_ADMIN: process.env.DATABASE_URL_ADMIN || "postgresql://localhost/test",
      REDIS_URL: process.env.REDIS_URL || "redis://localhost:6379",
    },
  },
  resolve: {
    alias: {
      "~": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Test Setup (tests/setup.ts)

```typescript
// tests/setup.ts
import { afterEach, beforeAll, afterAll, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

// Cleanup after each test
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// Mock environment variables from Doppler
beforeAll(() => {
  process.env.VITE_API_URL = "http://localhost:3000";
  process.env.DATABASE_URL_ADMIN = "postgresql://localhost/test";
});

// Setup test database connection
afterAll(async () => {
  // Cleanup test database
});
```

### Unit Tests (Vitest)

```typescript
// tests/unit/lib/utils/format.test.ts
import { describe, it, expect } from "vitest";
import { formatDate, formatCurrency } from "~/lib/utils/format";

describe("formatDate", () => {
  it("formats ISO date to readable format", () => {
    const date = new Date("2025-10-20T12:00:00Z");
    expect(formatDate(date)).toBe("Oct 20, 2025");
  });

  it("handles null dates", () => {
    expect(formatDate(null)).toBe("N/A");
  });
});

describe("formatCurrency", () => {
  it("formats USD currency with 2 decimals", () => {
    expect(formatCurrency(1234.56, "USD")).toBe("$1,234.56");
  });

  it("handles zero values", () => {
    expect(formatCurrency(0, "USD")).toBe("$0.00");
  });
});
```

### Component Tests (React Testing Library)

```typescript
// tests/unit/lib/components/UserProfile.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import UserProfile from "~/lib/components/UserProfile";
import * as userFunctions from "~/lib/server/functions/users";

// Mock server functions
vi.mock("~/lib/server/functions/users");

describe("UserProfile", () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  it("displays user name when loaded", async () => {
    const mockUser = {
      id: "123",
      name: "John Doe",
      email: "john@example.com",
    };

    vi.mocked(userFunctions.getUserById).mockResolvedValue(mockUser);

    render(<UserProfile userId="123" />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText("John Doe")).toBeInTheDocument();
    });
  });

  it("displays loading state initially", () => {
    vi.mocked(userFunctions.getUserById).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<UserProfile userId="123" />, { wrapper });

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("displays error message on fetch failure", async () => {
    vi.mocked(userFunctions.getUserById).mockRejectedValue(
      new Error("Network error")
    );

    render(<UserProfile userId="123" />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

### Integration Tests (TanStack Query + Server Functions)

```typescript
// tests/integration/auth-flow.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { QueryClient } from "@tanstack/react-query";
import { login, logout, getCurrentUser } from "~/lib/server/functions/auth";

describe("Authentication Flow", () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
  });

  it("completes full login and logout cycle", async () => {
    // Login
    const loginResult = await login({
      email: "test@example.com",
      password: "password123",
    });

    expect(loginResult.success).toBe(true);
    expect(loginResult.user).toBeDefined();

    // Verify session
    const user = await getCurrentUser();
    expect(user.email).toBe("test@example.com");

    // Logout
    const logoutResult = await logout();
    expect(logoutResult.success).toBe(true);

    // Verify session cleared
    const userAfterLogout = await getCurrentUser();
    expect(userAfterLogout).toBeNull();
  });
});
```

### E2E Tests (Playwright)

```typescript
// tests/e2e/user-registration.spec.ts
import { test, expect } from "@playwright/test";

// Doppler provides PLAYWRIGHT_BASE_URL
const baseUrl = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";

test.describe("User Registration", () => {
  test("completes registration with magic link", async ({ page }) => {
    await page.goto(`${baseUrl}/auth/signup`);

    // Fill registration form
    await page.fill('input[name="email"]', "newuser@example.com");
    await page.fill('input[name="name"]', "New User");
    await page.click('button[type="submit"]');

    // Verify email sent message
    await expect(page.locator("text=Check your email")).toBeVisible();

    // Simulate magic link click (in real test, check email)
    // This would use email testing service in CI
  });

  test("validates email format", async ({ page }) => {
    await page.goto(`${baseUrl}/auth/signup`);

    await page.fill('input[name="email"]', "invalid-email");
    await page.click('button[type="submit"]');

    await expect(page.locator("text=Invalid email")).toBeVisible();
  });
});
```

### Running TypeScript Tests

```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run specific test type
npm run test tests/unit/           # Unit tests only
npm run test tests/integration/    # Integration tests only
npm run test:e2e                   # E2E tests with Playwright

# Watch mode
npm run test:watch

# UI mode
npm run test:ui
```

## Python Testing (pytest)

### Project Structure

```
app/
├── db/
│   ├── repositories/
│   │   └── user_repository.py
│   └── models/
│       └── user.py
└── services/
    └── user_service.py
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── unit/                          # @pytest.mark.unit
│   ├── __init__.py
│   ├── repositories/
│   │   └── test_user_repository.py
│   └── services/
│       └── test_user_service.py
├── integration/                   # @pytest.mark.integration
│   ├── __init__.py
│   └── test_user_api.py
├── e2e/                          # @pytest.mark.e2e
│   ├── __init__.py
│   └── test_full_user_flow.py
└── benchmark/                    # @pytest.mark.benchmark
    ├── __init__.py
    └── test_repository_performance.py
```

### Pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]
markers = [
    "unit: Fast, isolated unit tests",
    "integration: Tests involving multiple components",
    "e2e: End-to-end tests through full flows",
    "benchmark: Performance tests",
]

# Coverage configuration
[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/conftest.py",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### Test Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from app.main import app
from app.db.models import Base

# Doppler provides DATABASE_URL_TEST at runtime
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST", "postgresql+asyncpg://localhost/test")


@pytest.fixture(scope="session")
async def engine():
    """Create test database engine."""
    engine = create_async_engine(DATABASE_URL_TEST, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def session(engine):
    """Create test database session."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client():
    """Create test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def tenant_id():
    """Provide test tenant ID."""
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
async def test_user(session, tenant_id):
    """Create test user."""
    from app.db.models.user import User
    user = User(
        tenant_id=tenant_id,
        email_address="test@example.com",
        name="Test User",
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

### Unit Tests (pytest)

```python
# tests/unit/repositories/test_user_repository.py
import pytest
from uuid import uuid4
from app.db.repositories.user_repository import UserRepository
from app.db.models.user import User


@pytest.mark.unit
class TestUserRepository:
    """Unit tests for UserRepository."""

    async def test_get_by_id_with_tenant_isolation(
        self, session, tenant_id, test_user
    ):
        """Test get_by_id enforces tenant isolation."""
        repo = UserRepository(session)

        # Should find user with correct tenant_id
        user = await repo.get_by_id(test_user.id, tenant_id)
        assert user is not None
        assert user.id == test_user.id

        # Should NOT find user with different tenant_id
        different_tenant = uuid4()
        user = await repo.get_by_id(test_user.id, different_tenant)
        assert user is None

    async def test_list_with_pagination(self, session, tenant_id):
        """Test list with limit and offset."""
        repo = UserRepository(session)

        # Create multiple users
        for i in range(10):
            user = User(
                tenant_id=tenant_id,
                email_address=f"user{i}@example.com",
                name=f"User {i}",
            )
            session.add(user)
        await session.commit()

        # Test pagination
        page1 = await repo.list(tenant_id, limit=5, offset=0)
        assert len(page1) == 5

        page2 = await repo.list(tenant_id, limit=5, offset=5)
        assert len(page2) == 5

        # Pages should not overlap
        page1_ids = {u.id for u in page1}
        page2_ids = {u.id for u in page2}
        assert page1_ids.isdisjoint(page2_ids)
```

### Integration Tests (FastAPI + Database)

```python
# tests/integration/test_user_api.py
import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestUserAPI:
    """Integration tests for User API endpoints."""

    async def test_create_user_endpoint(self, client: AsyncClient, tenant_id):
        """Test POST /users creates user with tenant isolation."""
        response = await client.post(
            "/api/users",
            json={
                "email_address": "newuser@example.com",
                "name": "New User",
            },
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email_address"] == "newuser@example.com"
        assert data["tenant_id"] == str(tenant_id)

    async def test_get_user_enforces_tenant_isolation(
        self, client: AsyncClient, test_user, tenant_id
    ):
        """Test GET /users/{id} enforces tenant isolation."""
        # Should succeed with correct tenant
        response = await client.get(
            f"/api/users/{test_user.id}",
            headers={"X-Tenant-ID": str(tenant_id)},
        )
        assert response.status_code == 200

        # Should fail with different tenant
        different_tenant = "00000000-0000-0000-0000-000000000000"
        response = await client.get(
            f"/api/users/{test_user.id}",
            headers={"X-Tenant-ID": different_tenant},
        )
        assert response.status_code == 404
```

### E2E Tests (Full Flow)

```python
# tests/e2e/test_full_user_flow.py
import pytest
from httpx import AsyncClient


@pytest.mark.e2e
class TestUserFlowE2E:
    """End-to-end tests for complete user workflows."""

    async def test_complete_user_lifecycle(self, client: AsyncClient, tenant_id):
        """Test create, read, update, delete user flow."""
        headers = {"X-Tenant-ID": str(tenant_id)}

        # 1. Create user
        response = await client.post(
            "/api/users",
            json={"email_address": "lifecycle@example.com", "name": "Lifecycle User"},
            headers=headers,
        )
        assert response.status_code == 201
        user_id = response.json()["id"]

        # 2. Read user
        response = await client.get(f"/api/users/{user_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Lifecycle User"

        # 3. Update user
        response = await client.patch(
            f"/api/users/{user_id}",
            json={"name": "Updated User"},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated User"

        # 4. Delete user
        response = await client.delete(f"/api/users/{user_id}", headers=headers)
        assert response.status_code == 204

        # 5. Verify deleted
        response = await client.get(f"/api/users/{user_id}", headers=headers)
        assert response.status_code == 404
```

### Benchmark Tests

```python
# tests/benchmark/test_repository_performance.py
import pytest
from uuid import uuid4
from app.db.repositories.user_repository import UserRepository


@pytest.mark.benchmark
class TestRepositoryPerformance:
    """Benchmark tests for repository performance."""

    async def test_list_query_performance(
        self, session, tenant_id, benchmark
    ):
        """Benchmark list query with 1000 users."""
        repo = UserRepository(session)

        # Setup: Create 1000 users
        from app.db.models.user import User
        users = [
            User(
                tenant_id=tenant_id,
                email_address=f"user{i}@example.com",
                name=f"User {i}",
            )
            for i in range(1000)
        ]
        session.add_all(users)
        await session.commit()

        # Benchmark the list query
        result = await benchmark(repo.list, tenant_id, limit=50, offset=0)

        assert len(result) == 50
        # Should complete in < 100ms
        assert benchmark.stats.mean < 0.1
```

### Running Python Tests

```bash
# IMPORTANT: Activate virtual environment first!
source .venv/bin/activate

# Doppler provides test environment variables
doppler run -- pytest

# Run with coverage
doppler run -- pytest --cov=app --cov-report=html

# Run specific test type
doppler run -- pytest -m unit              # Unit tests only
doppler run -- pytest -m integration       # Integration tests only
doppler run -- pytest -m e2e               # E2E tests only
doppler run -- pytest -m benchmark         # Benchmark tests only

# Run verbose
doppler run -- pytest -v

# Run with output
doppler run -- pytest -s

# Run specific file
doppler run -- pytest tests/unit/repositories/test_user_repository.py

# Run specific test
doppler run -- pytest tests/unit/repositories/test_user_repository.py::TestUserRepository::test_get_by_id_with_tenant_isolation
```

## Environment Variables with Doppler

### Doppler Configuration

Grey Haven uses **Doppler** for all environment variable management in testing and deployment.

```bash
# Install Doppler CLI
brew install dopplerhq/cli/doppler  # macOS
# or: curl -Ls https://cli.doppler.com/install.sh | sh

# Authenticate
doppler login

# Setup project
doppler setup

# Run tests with Doppler
doppler run -- npm run test          # TypeScript
doppler run -- pytest                # Python

# Access specific environment
doppler run --config test -- pytest  # Use 'test' config
doppler run --config dev -- npm run dev
```

### Doppler Environment Configs

Grey Haven projects have these Doppler configs:
- **dev**: Local development
- **test**: Running tests (CI and local)
- **staging**: Staging environment
- **production**: Production environment

### Test Environment Variables

```bash
# Doppler provides these for tests (do NOT commit .env!)

# Database
DATABASE_URL_ADMIN=postgresql+asyncpg://...
DATABASE_URL_AUTHENTICATED=postgresql+asyncpg://...
DATABASE_URL_TEST=postgresql+asyncpg://localhost/test_db

# Redis
REDIS_URL=redis://localhost:6379/1  # Use DB 1 for tests

# Auth
BETTER_AUTH_SECRET=test-secret-key
JWT_SECRET_KEY=test-jwt-secret

# External Services (use test/sandbox keys)
STRIPE_SECRET_KEY=sk_test_...
RESEND_API_KEY=re_test_...

# Playwright
PLAYWRIGHT_BASE_URL=http://localhost:3000
```

## Test Data Factories

### TypeScript Factory Pattern

```typescript
// tests/factories/user.factory.ts
import { faker } from "@faker-js/faker";

export function createMockUser(overrides = {}) {
  return {
    id: faker.string.uuid(),
    created_at: faker.date.past(),
    tenant_id: faker.string.uuid(),
    email_address: faker.internet.email(),
    name: faker.person.fullName(),
    is_active: true,
    ...overrides,
  };
}

export function createMockUsers(count: number, overrides = {}) {
  return Array.from({ length: count }, () => createMockUser(overrides));
}
```

### Python Factory Pattern

```python
# tests/factories/user_factory.py
from faker import Faker
from uuid import uuid4
from app.db.models.user import User

fake = Faker()


def create_user(tenant_id=None, **overrides):
    """Create test user with random data."""
    defaults = {
        "tenant_id": tenant_id or uuid4(),
        "email_address": fake.email(),
        "name": fake.name(),
        "is_active": True,
    }
    return User(**{**defaults, **overrides})


def create_users(count: int, tenant_id=None, **overrides):
    """Create multiple test users."""
    return [create_user(tenant_id=tenant_id, **overrides) for _ in range(count)]
```

## Continuous Integration

### GitHub Actions with Doppler

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test-typescript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3

      - name: Install dependencies
        run: npm ci

      - name: Run tests with Doppler
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: doppler run --config test -- npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt -r requirements-dev.txt

      - name: Run tests with Doppler
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN_TEST }}
        run: doppler run --config test -- pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

## When to Apply This Skill

Use this skill when:
- Writing new tests for features
- Setting up test infrastructure
- Configuring CI/CD pipelines
- Debugging failing tests
- Improving test coverage
- Reviewing test code quality
- Setting up Doppler for tests
- Creating test fixtures and factories

## Template References

These testing patterns are from Grey Haven's actual templates:
- **Frontend**: `cvi-template` (Vitest + Playwright + Testing Library)
- **Backend**: `cvi-backend-template` (pytest + FastAPI TestClient)

## Critical Reminders

1. **Coverage: 80% minimum** (enforced in CI)
2. **Test markers**: unit, integration, e2e, benchmark (both languages)
3. **Doppler**: ALWAYS use for test environment variables
4. **Virtual env**: MUST activate for Python tests (`source .venv/bin/activate`)
5. **Tenant isolation**: ALWAYS test multi-tenant scenarios
6. **Fixtures**: Use factories for test data generation
7. **Mocking**: Mock external services in unit tests
8. **CI**: Run tests with `doppler run --config test`
9. **Database**: Use separate test database (Doppler provides URL)
10. **Cleanup**: Clean up test data after each test
