# Testing Examples

Copy-paste ready test examples from Grey Haven Studio production templates.

## Table of Contents

- [Vitest Examples](#vitest-examples)
  - [Unit Tests](#vitest-unit-tests)
  - [Component Tests](#vitest-component-tests)
  - [Integration Tests](#vitest-integration-tests)
  - [E2E Tests](#vitest-e2e-tests)
- [Pytest Examples](#pytest-examples)
  - [Unit Tests](#pytest-unit-tests)
  - [Integration Tests](#pytest-integration-tests)
  - [E2E Tests](#pytest-e2e-tests)
  - [Benchmark Tests](#pytest-benchmark-tests)
- [Test Factories and Fixtures](#test-factories-and-fixtures)

## Vitest Examples

### Vitest Unit Tests

**Testing utility functions:**

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

**Testing business logic:**

```typescript
// tests/unit/lib/utils/validation.test.ts
import { describe, it, expect } from "vitest";
import { validateEmail, validatePassword } from "~/lib/utils/validation";

describe("validateEmail", () => {
  it("accepts valid email addresses", () => {
    expect(validateEmail("user@example.com")).toBe(true);
    expect(validateEmail("test.user+tag@example.co.uk")).toBe(true);
  });

  it("rejects invalid email addresses", () => {
    expect(validateEmail("invalid")).toBe(false);
    expect(validateEmail("@example.com")).toBe(false);
    expect(validateEmail("user@")).toBe(false);
  });
});

describe("validatePassword", () => {
  it("requires minimum length of 8 characters", () => {
    expect(validatePassword("short")).toBe(false);
    expect(validatePassword("longenough")).toBe(true);
  });

  it("requires at least one number", () => {
    expect(validatePassword("noNumbers")).toBe(false);
    expect(validatePassword("hasNumber1")).toBe(true);
  });
});
```

### Vitest Component Tests

**Testing React components with React Testing Library:**

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

**Testing user interactions:**

```typescript
// tests/unit/lib/components/Counter.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Counter from "~/lib/components/Counter";

describe("Counter", () => {
  it("starts at zero", () => {
    render(<Counter />);
    expect(screen.getByText("Count: 0")).toBeInTheDocument();
  });

  it("increments when button clicked", () => {
    render(<Counter />);
    const button = screen.getByRole("button", { name: /increment/i });

    fireEvent.click(button);
    expect(screen.getByText("Count: 1")).toBeInTheDocument();

    fireEvent.click(button);
    expect(screen.getByText("Count: 2")).toBeInTheDocument();
  });

  it("decrements when decrement button clicked", () => {
    render(<Counter />);
    const increment = screen.getByRole("button", { name: /increment/i });
    const decrement = screen.getByRole("button", { name: /decrement/i });

    fireEvent.click(increment);
    fireEvent.click(increment);
    fireEvent.click(decrement);

    expect(screen.getByText("Count: 1")).toBeInTheDocument();
  });
});
```

### Vitest Integration Tests

**Testing TanStack Query with server functions:**

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

**Testing database operations:**

```typescript
// tests/integration/user-repository.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { db } from "~/lib/server/db";
import { users } from "~/lib/server/db/schema";
import { eq } from "drizzle-orm";

describe("User Repository Integration", () => {
  const testTenantId = "550e8400-e29b-41d4-a716-446655440000";

  beforeEach(async () => {
    // Clean up test data
    await db.delete(users).where(eq(users.tenant_id, testTenantId));
  });

  it("creates and retrieves user with tenant isolation", async () => {
    // Create user
    const [user] = await db
      .insert(users)
      .values({
        tenant_id: testTenantId,
        email_address: "test@example.com",
        name: "Test User",
      })
      .returning();

    expect(user).toBeDefined();
    expect(user.email_address).toBe("test@example.com");

    // Retrieve user
    const [retrieved] = await db
      .select()
      .from(users)
      .where(eq(users.id, user.id))
      .where(eq(users.tenant_id, testTenantId));

    expect(retrieved).toBeDefined();
    expect(retrieved.id).toBe(user.id);
  });
});
```

### Vitest E2E Tests

**Testing with Playwright:**

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

**Testing full user workflows:**

```typescript
// tests/e2e/user-workflow.spec.ts
import { test, expect } from "@playwright/test";

const baseUrl = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";

test.describe("User Workflow", () => {
  test("complete user profile update flow", async ({ page }) => {
    // 1. Login
    await page.goto(`${baseUrl}/auth/login`);
    await page.fill('input[name="email"]', "test@example.com");
    await page.fill('input[name="password"]', "password123");
    await page.click('button[type="submit"]');

    // 2. Navigate to profile
    await page.click('a[href="/settings/profile"]');
    await expect(page).toHaveURL(`${baseUrl}/settings/profile`);

    // 3. Update profile
    await page.fill('input[name="name"]', "Updated Name");
    await page.click('button:has-text("Save")');

    // 4. Verify update
    await expect(page.locator("text=Profile updated")).toBeVisible();
    await expect(page.locator('input[name="name"]')).toHaveValue("Updated Name");
  });
});
```

## Pytest Examples

### Pytest Unit Tests

**Testing repository with tenant isolation:**

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

**Testing service layer:**

```python
# tests/unit/services/test_user_service.py
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from app.services.user_service import UserService
from app.db.models.user import User


@pytest.mark.unit
class TestUserService:
    """Unit tests for UserService."""

    async def test_create_user_success(self, tenant_id):
        """Test creating a new user."""
        # Mock repository
        mock_repo = AsyncMock()
        mock_repo.create.return_value = User(
            id=uuid4(),
            tenant_id=tenant_id,
            email_address="new@example.com",
            name="New User",
        )

        # Create service with mocked repo
        service = UserService(mock_repo)

        # Call method
        user = await service.create_user(
            tenant_id=tenant_id,
            email="new@example.com",
            name="New User",
        )

        # Verify
        assert user.email_address == "new@example.com"
        mock_repo.create.assert_called_once()

    async def test_create_user_duplicate_email(self, tenant_id):
        """Test creating user with duplicate email raises error."""
        mock_repo = AsyncMock()
        mock_repo.create.side_effect = ValueError("Email already exists")

        service = UserService(mock_repo)

        with pytest.raises(ValueError, match="Email already exists"):
            await service.create_user(
                tenant_id=tenant_id,
                email="duplicate@example.com",
                name="Duplicate User",
            )
```

### Pytest Integration Tests

**Testing FastAPI endpoints:**

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

    async def test_update_user_endpoint(
        self, client: AsyncClient, test_user, tenant_id
    ):
        """Test PATCH /users/{id} updates user."""
        response = await client.patch(
            f"/api/users/{test_user.id}",
            json={"name": "Updated Name"},
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["id"] == str(test_user.id)
```

**Testing database transactions:**

```python
# tests/integration/test_transaction_handling.py
import pytest
from sqlalchemy.exc import IntegrityError
from app.db.repositories.user_repository import UserRepository
from app.db.models.user import User


@pytest.mark.integration
class TestTransactionHandling:
    """Integration tests for database transactions."""

    async def test_rollback_on_error(self, session, tenant_id):
        """Test that errors cause transaction rollback."""
        repo = UserRepository(session)

        # Create first user successfully
        user1 = User(
            tenant_id=tenant_id,
            email_address="user1@example.com",
            name="User 1",
        )
        session.add(user1)
        await session.commit()

        # Try to create duplicate email (should fail)
        with pytest.raises(IntegrityError):
            user2 = User(
                tenant_id=tenant_id,
                email_address="user1@example.com",  # Duplicate!
                name="User 2",
            )
            session.add(user2)
            await session.commit()

        # Verify only first user exists
        users = await repo.list(tenant_id)
        assert len(users) == 1
        assert users[0].email_address == "user1@example.com"
```

### Pytest E2E Tests

**Testing complete user lifecycle:**

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

**Testing authentication flow:**

```python
# tests/e2e/test_auth_flow.py
import pytest
from httpx import AsyncClient


@pytest.mark.e2e
class TestAuthFlowE2E:
    """End-to-end tests for authentication workflows."""

    async def test_registration_and_login_flow(self, client: AsyncClient):
        """Test complete registration and login flow."""
        # 1. Register new user
        response = await client.post(
            "/api/auth/register",
            json={
                "email_address": "newuser@example.com",
                "password": "SecurePass123!",
                "name": "New User",
            },
        )
        assert response.status_code == 201

        # 2. Login with credentials
        response = await client.post(
            "/api/auth/login",
            json={
                "email_address": "newuser@example.com",
                "password": "SecurePass123!",
            },
        )
        assert response.status_code == 200
        token = response.json()["access_token"]

        # 3. Access protected endpoint
        response = await client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["email_address"] == "newuser@example.com"

        # 4. Logout
        response = await client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
```

### Pytest Benchmark Tests

**Benchmarking database queries:**

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

    async def test_bulk_insert_performance(self, session, tenant_id, benchmark):
        """Benchmark bulk insert operations."""
        from app.db.models.user import User

        def create_users():
            users = [
                User(
                    tenant_id=tenant_id,
                    email_address=f"bulk{i}@example.com",
                    name=f"Bulk User {i}",
                )
                for i in range(100)
            ]
            session.add_all(users)
            return users

        result = benchmark(create_users)
        assert len(result) == 100
```

## Test Factories and Fixtures

### TypeScript Factory Pattern

**User factory:**

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

**Usage in tests:**

```typescript
// tests/unit/lib/components/UserList.test.tsx
import { createMockUsers } from "../../factories/user.factory";

it("displays list of users", () => {
  const users = createMockUsers(5, { tenant_id: "test-tenant" });
  render(<UserList users={users} />);

  expect(screen.getAllByRole("listitem")).toHaveLength(5);
});
```

### Python Factory Pattern

**User factory:**

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

**Usage in tests:**

```python
# tests/unit/test_user_service.py
from tests.factories.user_factory import create_users

async def test_bulk_user_creation(session, tenant_id):
    """Test creating multiple users."""
    users = create_users(10, tenant_id=tenant_id)
    session.add_all(users)
    await session.commit()

    # Verify all created with same tenant
    for user in users:
        assert user.tenant_id == tenant_id
```

### Python Pytest Fixtures

**Complete conftest.py example:**

```python
# tests/conftest.py
import pytest
import os
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


@pytest.fixture
async def authenticated_client(client, test_user):
    """Create authenticated HTTP client."""
    # Login and get token
    response = await client.post(
        "/api/auth/login",
        json={
            "email_address": test_user.email_address,
            "password": "testpassword",
        },
    )
    token = response.json()["access_token"]

    # Add auth header to client
    client.headers["Authorization"] = f"Bearer {token}"
    return client
```

## Mocking Patterns

### TypeScript Mocking (Vitest)

**Mocking modules:**

```typescript
// tests/unit/lib/services/api.test.ts
import { vi } from "vitest";
import * as apiClient from "~/lib/services/api-client";

// Mock entire module
vi.mock("~/lib/services/api-client", () => ({
  fetchUser: vi.fn(),
  updateUser: vi.fn(),
}));

it("calls API client with correct parameters", async () => {
  vi.mocked(apiClient.fetchUser).mockResolvedValue({
    id: "123",
    name: "Test User",
  });

  const user = await apiClient.fetchUser("123");

  expect(apiClient.fetchUser).toHaveBeenCalledWith("123");
  expect(user.name).toBe("Test User");
});
```

**Mocking environment variables:**

```typescript
// tests/unit/lib/config/env.test.ts
import { vi } from "vitest";

it("loads environment variables", () => {
  vi.stubEnv("VITE_API_URL", "https://test.example.com");

  const config = loadConfig();

  expect(config.apiUrl).toBe("https://test.example.com");

  vi.unstubAllEnvs();
});
```

### Python Mocking (pytest)

**Mocking with unittest.mock:**

```python
# tests/unit/test_email_service.py
import pytest
from unittest.mock import AsyncMock, patch
from app.services.email_service import EmailService


@pytest.mark.unit
async def test_send_email_success():
    """Test sending email successfully."""
    with patch("app.services.email_service.resend") as mock_resend:
        mock_resend.emails.send = AsyncMock(return_value={"id": "email-123"})

        service = EmailService()
        result = await service.send_email(
            to="user@example.com",
            subject="Test",
            body="Test email",
        )

        assert result["id"] == "email-123"
        mock_resend.emails.send.assert_called_once()
```

**Mocking external APIs:**

```python
# tests/unit/test_stripe_service.py
import pytest
from unittest.mock import MagicMock, patch
from app.services.stripe_service import StripeService


@pytest.mark.unit
async def test_create_payment_intent():
    """Test creating Stripe payment intent."""
    with patch("stripe.PaymentIntent.create") as mock_create:
        mock_create.return_value = MagicMock(
            id="pi_123",
            amount=1000,
            status="requires_payment_method",
        )

        service = StripeService()
        intent = await service.create_payment_intent(amount=1000, currency="usd")

        assert intent.id == "pi_123"
        assert intent.amount == 1000
        mock_create.assert_called_once_with(amount=1000, currency="usd")
```
