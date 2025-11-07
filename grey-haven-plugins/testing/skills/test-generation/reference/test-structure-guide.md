# Test Structure Guide

How to organize test files, naming conventions, and test suite structure for maximum maintainability.

## File Naming Conventions

### TypeScript/JavaScript

**Pattern**: `{ComponentName}.test.{ts|tsx}`

```
src/
├── components/
│   ├── Button.tsx
│   ├── Button.test.tsx          ✅ Co-located with component
│   ├── UserCard.tsx
│   └── UserCard.test.tsx
├── lib/
│   ├── validation.ts
│   ├── validation.test.ts       ✅ Co-located with module
│   ├── api.ts
│   └── api.test.ts
└── hooks/
    ├── useUsers.ts
    └── useUsers.test.ts          ✅ Co-located with hook
```

**Why co-location**:
- Easy to find tests
- Refactoring moves tests with code
- Clear 1:1 relationship

### Python

**Pattern**: `test_{module_name}.py`

```
app/
├── routers/
│   ├── users.py
│   └── orders.py
├── services/
│   ├── payment.py
│   └── email.py
tests/
├── test_users.py                ✅ Mirrors app structure
├── test_orders.py
├── test_payment.py
└── test_email.py
```

**Why separate directory**:
- Python convention (pytest discovers tests/)
- Keeps production code clean
- Clear test vs implementation separation

## Directory Structure

### Small Projects (< 20 files)

**TypeScript**:
```
src/
├── components/
│   ├── Component.tsx
│   └── Component.test.tsx
├── lib/
│   ├── utils.ts
│   └── utils.test.ts
└── App.test.tsx
```

**Python**:
```
app/
├── main.py
├── models.py
└── routers/
tests/
├── conftest.py              # Shared fixtures
├── test_main.py
└── test_models.py
```

### Medium Projects (20-100 files)

**TypeScript**:
```
src/
├── components/
│   ├── common/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx
│   └── features/
│       ├── UserProfile/
│       │   ├── UserProfile.tsx
│       │   └── UserProfile.test.tsx
│       └── Dashboard/
├── lib/
└── __tests__/
    ├── integration/         # Integration tests separate
    │   └── checkout-flow.test.tsx
    └── e2e/                 # E2E tests separate
        └── user-journey.test.tsx
```

**Python**:
```
app/
├── routers/
├── services/
└── models/
tests/
├── unit/                    # Unit tests
│   ├── test_users.py
│   └── test_orders.py
├── integration/             # Integration tests
│   └── test_checkout_flow.py
├── fixtures/                # Shared test data
│   └── sample_data.py
└── conftest.py
```

### Large Projects (100+ files)

**TypeScript**:
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── LoginForm.test.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useAuth.test.ts
│   │   └── __tests__/
│   │       └── auth-flow.integration.test.tsx
│   └── checkout/
│       ├── components/
│       └── __tests__/
tests/
├── integration/             # Cross-feature tests
├── e2e/                     # End-to-end tests
└── utils/                   # Test utilities
    ├── setup.ts
    └── factories.ts
```

**Python**:
```
app/
├── features/
│   ├── auth/
│   │   ├── routes.py
│   │   └── service.py
│   └── checkout/
tests/
├── unit/
│   ├── auth/
│   │   ├── test_routes.py
│   │   └── test_service.py
│   └── checkout/
├── integration/
│   └── test_checkout_flow.py
├── fixtures/
│   ├── __init__.py
│   ├── auth.py
│   └── database.py
└── conftest.py
```

## Test Suite Organization with describe/class

### Vitest: Nested describe Blocks

```typescript
describe('UserService', () => {
  // Group by method or feature
  describe('createUser', () => {
    it('should create user with valid data', () => {
      // Test implementation
    });

    it('should reject duplicate email', () => {
      // Test implementation
    });

    it('should validate required fields', () => {
      // Test implementation
    });

    describe('edge cases', () => {
      it('should handle very long names', () => {
        // Test implementation
      });

      it('should handle special characters in email', () => {
        // Test implementation
      });
    });
  });

  describe('updateUser', () => {
    it('should update user fields', () => {
      // Test implementation
    });

    it('should not update immutable fields', () => {
      // Test implementation
    });
  });

  describe('deleteUser', () => {
    it('should soft delete user', () => {
      // Test implementation
    });

    it('should cascade delete related data', () => {
      // Test implementation
    });
  });
});
```

### pytest: Test Classes

```python
class TestUserService:
    """Tests for UserService class"""

    class TestCreateUser:
        """Tests for create_user method"""

        def test_create_user_with_valid_data(self):
            """Should create user with valid data"""
            # Test implementation

        def test_reject_duplicate_email(self):
            """Should reject duplicate email"""
            # Test implementation

        def test_validate_required_fields(self):
            """Should validate required fields"""
            # Test implementation

        class TestEdgeCases:
            """Edge case tests for user creation"""

            def test_handle_very_long_names(self):
                """Should handle very long names"""
                # Test implementation

    class TestUpdateUser:
        """Tests for update_user method"""

        def test_update_user_fields(self):
            """Should update user fields"""
            # Test implementation

        def test_not_update_immutable_fields(self):
            """Should not update immutable fields"""
            # Test implementation
```

## Test Naming Conventions

### Good Test Names

**Pattern**: `should {expected behavior} when {condition}`

```typescript
// ✅ Good: Clear, descriptive, explains behavior
it('should return 404 when user not found', () => {});
it('should calculate total price including tax', () => {});
it('should disable submit button while form is submitting', () => {});
it('should validate email format before saving', () => {});

// ❌ Bad: Vague, doesn't explain what's being tested
it('works', () => {});
it('test user', () => {});
it('returns data', () => {});
```

### Python Docstring Convention

```python
def test_create_user_with_valid_data():
    """
    Should create user with valid data and return user object.

    Given: Valid user data (email, name, role)
    When: createUser is called
    Then: User is saved to database and returned
    """
    # Test implementation
```

## Grouping Related Tests

### By Feature

```typescript
describe('Shopping Cart', () => {
  describe('Adding Items', () => {
    it('should add item to cart');
    it('should increment quantity if item exists');
    it('should apply quantity limits');
  });

  describe('Removing Items', () => {
    it('should remove item from cart');
    it('should update total price');
  });

  describe('Calculating Totals', () => {
    it('should calculate subtotal');
    it('should apply discounts');
    it('should calculate tax');
    it('should calculate final total');
  });
});
```

### By Scenario

```typescript
describe('User Authentication', () => {
  describe('When user provides valid credentials', () => {
    it('should return access token');
    it('should return refresh token');
    it('should set authentication cookie');
  });

  describe('When user provides invalid credentials', () => {
    it('should return 401 error');
    it('should not set authentication cookie');
    it('should log failed attempt');
  });

  describe('When user is locked out', () => {
    it('should return 403 error');
    it('should not allow login');
    it('should show account locked message');
  });
});
```

## Shared Setup Patterns

### TypeScript: beforeEach with Factories

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

// Test factories
const createUser = (overrides = {}) => ({
  id: '123',
  email: 'test@example.com',
  name: 'Test User',
  role: 'member',
  ...overrides,
});

const createOrder = (overrides = {}) => ({
  id: 'order-1',
  userId: '123',
  total: 99.99,
  status: 'pending',
  ...overrides,
});

describe('OrderService', () => {
  let orderService: OrderService;
  let mockDatabase: any;

  beforeEach(() => {
    mockDatabase = createMockDatabase();
    orderService = new OrderService(mockDatabase);
  });

  it('should create order for user', () => {
    const user = createUser();
    const order = createOrder({ userId: user.id });

    // Test uses clean, predictable data
  });
});
```

### Python: Fixtures with Factories

```python
# tests/fixtures/factories.py
import pytest
from app.models import User, Order

@pytest.fixture
def user_factory(session):
    """Factory for creating test users"""
    def _create_user(**kwargs):
        defaults = {
            'email': 'test@example.com',
            'name': 'Test User',
            'role': 'member',
        }
        user = User(**{**defaults, **kwargs})
        session.add(user)
        session.commit()
        return user
    return _create_user

@pytest.fixture
def order_factory(session, user_factory):
    """Factory for creating test orders"""
    def _create_order(**kwargs):
        if 'user_id' not in kwargs:
            user = user_factory()
            kwargs['user_id'] = user.id

        defaults = {
            'total': 99.99,
            'status': 'pending',
        }
        order = Order(**{**defaults, **kwargs})
        session.add(order)
        session.commit()
        return order
    return _create_order

# tests/test_orders.py
def test_create_order(order_factory):
    """Should create order"""
    order = order_factory(total=199.99, status='confirmed')

    assert order.total == 199.99
    assert order.status == 'confirmed'
```

## Test Data Management

### Inline Test Data

**Best for**: Simple, one-off test data

```typescript
it('should validate email', () => {
  const email = 'test@example.com';  // Inline, clear
  expect(validateEmail(email)).toBe(true);
});
```

### Shared Test Data

**Best for**: Complex data used across multiple tests

```typescript
// __tests__/fixtures/users.ts
export const VALID_USER = {
  id: 'user-123',
  email: 'john@example.com',
  name: 'John Doe',
  role: 'admin',
  createdAt: '2024-01-15T00:00:00Z',
};

export const VALID_USER_2 = {
  id: 'user-456',
  email: 'jane@example.com',
  name: 'Jane Smith',
  role: 'member',
  createdAt: '2024-01-16T00:00:00Z',
};

// UserService.test.ts
import { VALID_USER } from './__tests__/fixtures/users';

it('should update user', () => {
  const updated = updateUser(VALID_USER.id, { name: 'John Smith' });
  expect(updated.name).toBe('John Smith');
});
```

### Test Data Builders

**Best for**: Flexible data creation with defaults

```typescript
// __tests__/builders/UserBuilder.ts
class UserBuilder {
  private user = {
    id: 'user-123',
    email: 'test@example.com',
    name: 'Test User',
    role: 'member',
  };

  withId(id: string) {
    this.user.id = id;
    return this;
  }

  withEmail(email: string) {
    this.user.email = email;
    return this;
  }

  asAdmin() {
    this.user.role = 'admin';
    return this;
  }

  build() {
    return { ...this.user };
  }
}

// Usage
it('should allow admin to delete user', () => {
  const admin = new UserBuilder().asAdmin().build();
  const result = deleteUser(admin, 'user-456');
  expect(result).toBe(true);
});
```

## Integration vs Unit Test Organization

### Keep Integration Tests Separate

```
src/
├── components/
│   ├── Button.test.tsx           # Unit test (co-located)
│   └── UserCard.test.tsx
tests/
├── integration/
│   ├── checkout-flow.test.tsx    # Integration test (separate)
│   └── user-registration.test.tsx
└── e2e/
    └── complete-purchase.test.tsx # E2E test (separate)
```

**Why**:
- Integration tests are slower (run less frequently)
- Different setup requirements
- Different CI/CD stages
- Clear separation of concerns

## Test Configuration

### Vitest Config

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.test.{ts,tsx}',
        '**/*.config.{ts,js}',
      ],
      threshold: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

### pytest Config

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests (skip in CI)
```

## Test Discovery Patterns

### Vitest Discovery

```bash
# Run all tests
npm test

# Run specific file
npm test UserService.test.ts

# Run tests matching pattern
npm test --grep "authentication"

# Run integration tests only
npm test tests/integration/

# Watch mode
npm test -- --watch
```

### pytest Discovery

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_users.py

# Run specific test
pytest tests/test_users.py::test_create_user

# Run by marker
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only

# Watch mode
pytest-watch
```

---

Related: [Testing Patterns](testing-patterns.md) | [Mocking Strategies](mocking-strategies.md) | [Coverage Standards](coverage-standards.md) | [Return to INDEX](INDEX.md)
