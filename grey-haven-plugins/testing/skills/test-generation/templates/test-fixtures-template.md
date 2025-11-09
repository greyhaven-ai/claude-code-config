# Test Fixtures Template

Templates for test fixtures, factories, and test data builders with realistic examples.

## TypeScript Test Fixtures

### Basic Test Data

```typescript
// __tests__/fixtures/users.ts

export const VALID_USER = {
  id: 'user-123',
  email: 'john@example.com',
  name: 'John Doe',
  role: 'member',
  createdAt: '2024-01-15T00:00:00Z',
  updatedAt: '2024-01-15T00:00:00Z',
};

export const ADMIN_USER = {
  id: 'user-admin',
  email: 'admin@example.com',
  name: 'Admin User',
  role: 'admin',
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z',
};

export const USERS = [
  VALID_USER,
  ADMIN_USER,
  {
    id: 'user-456',
    email: 'jane@example.com',
    name: 'Jane Smith',
    role: 'member',
    createdAt: '2024-01-16T00:00:00Z',
    updatedAt: '2024-01-16T00:00:00Z',
  },
];

// Usage in tests
import { VALID_USER, ADMIN_USER } from './__tests__/fixtures/users';

it('should create user', () => {
  const user = createUser(VALID_USER);
  expect(user.email).toBe('john@example.com');
});
```

### Factory Functions

```typescript
// __tests__/factories/user.factory.ts

import type { User } from '../types';

let userIdCounter = 1;

export function createUser(overrides: Partial<User> = {}): User {
  const id = `user-${userIdCounter++}`;

  return {
    id,
    email: `user${userIdCounter}@example.com`,
    name: 'Test User',
    role: 'member',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    ...overrides,
  };
}

export function createAdminUser(overrides: Partial<User> = {}): User {
  return createUser({
    role: 'admin',
    ...overrides,
  });
}

export function createUsers(count: number, overrides: Partial<User> = {}): User[] {
  return Array.from({ length: count }, () => createUser(overrides));
}

// Usage
const user = createUser({ email: 'custom@example.com' });
const admin = createAdminUser();
const users = createUsers(5);
```

### Builder Pattern

```typescript
// __tests__/builders/UserBuilder.ts

export class UserBuilder {
  private user: Partial<User> = {
    id: 'user-123',
    email: 'test@example.com',
    name: 'Test User',
    role: 'member',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  withId(id: string): this {
    this.user.id = id;
    return this;
  }

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withName(name: string): this {
    this.user.name = name;
    return this;
  }

  withRole(role: 'admin' | 'member'): this {
    this.user.role = role;
    return this;
  }

  asAdmin(): this {
    this.user.role = 'admin';
    return this;
  }

  asMember(): this {
    this.user.role = 'member';
    return this;
  }

  createdAt(date: Date | string): this {
    this.user.createdAt = typeof date === 'string' ? date : date.toISOString();
    return this;
  }

  build(): User {
    return { ...this.user } as User;
  }
}

// Usage
const admin = new UserBuilder()
  .withEmail('admin@example.com')
  .asAdmin()
  .build();

const recentUser = new UserBuilder()
  .createdAt(new Date('2024-01-15'))
  .build();
```

### Mock Database

```typescript
// __tests__/mocks/mockDatabase.ts

import type { User, Order } from '../types';

export class MockDatabase {
  private users: Map<string, User> = new Map();
  private orders: Map<string, Order> = new Map();

  // User methods
  insertUser(user: User): User {
    this.users.set(user.id, user);
    return user;
  }

  findUser(id: string): User | undefined {
    return this.users.get(id);
  }

  findUsers(filter?: Partial<User>): User[] {
    const users = Array.from(this.users.values());

    if (!filter) return users;

    return users.filter(user =>
      Object.entries(filter).every(([key, value]) => user[key as keyof User] === value)
    );
  }

  updateUser(id: string, updates: Partial<User>): User | undefined {
    const user = this.users.get(id);
    if (!user) return undefined;

    const updated = { ...user, ...updates, updatedAt: new Date().toISOString() };
    this.users.set(id, updated);
    return updated;
  }

  deleteUser(id: string): boolean {
    return this.users.delete(id);
  }

  // Order methods
  insertOrder(order: Order): Order {
    this.orders.set(order.id, order);
    return order;
  }

  findOrder(id: string): Order | undefined {
    return this.orders.get(id);
  }

  // Utility methods
  clear(): void {
    this.users.clear();
    this.orders.clear();
  }

  seed(): void {
    // Add seed data for common test scenarios
    this.insertUser(createUser({ id: 'user-1', email: 'test1@example.com' }));
    this.insertUser(createUser({ id: 'user-2', email: 'test2@example.com' }));
  }
}

// Usage
let db: MockDatabase;

beforeEach(() => {
  db = new MockDatabase();
  db.seed(); // Optionally seed with data
});

it('should find user by id', () => {
  const user = db.findUser('user-1');
  expect(user?.email).toBe('test1@example.com');
});
```

## Python Test Fixtures

### pytest Fixtures

```python
# tests/conftest.py

import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.models import User, Order, Product

@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(name="session")
def session_fixture(engine):
    """Create database session"""
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_user(session: Session):
    """Create a sample user for testing"""
    user = User(
        name="John Doe",
        email="john@example.com",
        role="member",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def admin_user(session: Session):
    """Create an admin user for testing"""
    user = User(
        name="Admin User",
        email="admin@example.com",
        role="admin",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def sample_users(session: Session):
    """Create multiple sample users"""
    users = [
        User(name=f"User {i}", email=f"user{i}@example.com", role="member")
        for i in range(1, 6)
    ]
    for user in users:
        session.add(user)
    session.commit()

    for user in users:
        session.refresh(user)

    return users

# Usage
def test_with_sample_user(sample_user: User):
    """Test with pre-created user"""
    assert sample_user.email == "john@example.com"

def test_with_multiple_users(sample_users: list[User]):
    """Test with multiple users"""
    assert len(sample_users) == 5
```

### Factory Fixtures

```python
# tests/fixtures/factories.py

import pytest
from app.models import User, Order, Product

@pytest.fixture
def user_factory(session):
    """Factory for creating test users"""
    created_users = []

    def _create_user(**kwargs):
        defaults = {
            "name": "Test User",
            "email": "test@example.com",
            "role": "member",
        }
        user = User(**{**defaults, **kwargs})
        session.add(user)
        session.commit()
        session.refresh(user)
        created_users.append(user)
        return user

    yield _create_user

    # Cleanup (optional)
    for user in created_users:
        session.delete(user)
    session.commit()

@pytest.fixture
def product_factory(session):
    """Factory for creating test products"""
    def _create_product(**kwargs):
        defaults = {
            "name": "Test Product",
            "price": 99.99,
            "inventory": 100,
        }
        product = Product(**{**defaults, **kwargs})
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

    return _create_product

@pytest.fixture
def order_factory(session, user_factory):
    """Factory for creating test orders"""
    def _create_order(**kwargs):
        if "user_id" not in kwargs:
            user = user_factory()
            kwargs["user_id"] = user.id

        defaults = {
            "total": 99.99,
            "status": "pending",
        }
        order = Order(**{**defaults, **kwargs})
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

    return _create_order

# Usage
def test_create_user(user_factory):
    """Should create user with factory"""
    user = user_factory(name="Custom User", email="custom@example.com")
    assert user.name == "Custom User"
    assert user.email == "custom@example.com"

def test_create_order(order_factory):
    """Should create order with associated user"""
    order = order_factory(total=199.99)
    assert order.total == 199.99
    assert order.user_id is not None
```

### Parametrized Fixtures

```python
# tests/conftest.py

import pytest

@pytest.fixture(params=["member", "admin", "owner"])
def user_with_role(request, session):
    """Create users with different roles"""
    user = User(
        name=f"{request.param.title()} User",
        email=f"{request.param}@example.com",
        role=request.param,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Usage - test runs 3 times with different roles
def test_user_permissions(user_with_role: User):
    """Test runs once for each role"""
    assert user_with_role.role in ["member", "admin", "owner"]
    # Test logic based on role
```

### Scoped Fixtures

```python
# tests/conftest.py

import pytest

@pytest.fixture(scope="session")
def app_config():
    """Application config - created once per test session"""
    return {
        "database_url": "sqlite:///:memory:",
        "debug": True,
    }

@pytest.fixture(scope="module")
def sample_data(session):
    """Sample data - created once per test module"""
    # Setup expensive data once
    products = [
        Product(name=f"Product {i}", price=10.00 * i, inventory=100)
        for i in range(1, 101)
    ]
    for product in products:
        session.add(product)
    session.commit()

    yield products

    # Cleanup after module completes
    for product in products:
        session.delete(product)
    session.commit()

@pytest.fixture(scope="function")  # Default scope
def clean_database(session):
    """Clean database before each test"""
    # Runs before each test function
    session.exec("DELETE FROM users")
    session.commit()
```

## Best Practices

### 1. Keep Fixtures Simple

```typescript
// ✅ Good: Simple, focused fixture
export function createUser(overrides = {}) {
  return {
    id: '123',
    email: 'test@example.com',
    ...overrides,
  };
}

// ❌ Bad: Over-engineered fixture
export function createComplexUser(options) {
  const user = { /* ... */ };
  if (options.withOrders) {
    user.orders = createOrders(options.orderCount);
  }
  if (options.withPayments) {
    user.payments = createPayments();
  }
  // Too much logic in fixture
  return user;
}
```

### 2. Use Factories for Variation

```python
# ✅ Good: Factory allows customization
@pytest.fixture
def user_factory(session):
    def _create(**kwargs):
        defaults = {"name": "Test", "email": "test@example.com"}
        return User(**{**defaults, **kwargs})
    return _create

# Usage: Flexible for different test scenarios
user1 = user_factory(email="custom1@example.com")
user2 = user_factory(role="admin")
```

### 3. Cleanup After Tests

```python
# ✅ Good: Fixture cleans up
@pytest.fixture
def temp_user(session):
    user = User(name="Temp", email="temp@example.com")
    session.add(user)
    session.commit()

    yield user

    # Cleanup
    session.delete(user)
    session.commit()
```

### 4. Composition Over Complexity

```typescript
// ✅ Good: Compose fixtures
const user = createUser();
const order = createOrder({ userId: user.id });
const payment = createPayment({ orderId: order.id });

// ❌ Bad: Single complex fixture
const everything = createUserWithOrdersAndPayments();
```

## Checklist

- [ ] Fixtures are simple and focused
- [ ] Factory functions allow customization
- [ ] Cleanup happens after tests
- [ ] Fixtures are reusable across tests
- [ ] Complex data uses builders or factories
- [ ] Fixtures have clear, descriptive names
- [ ] Fixtures are documented with comments

---

Related: [Unit Test Template](unit-test-template.md) | [Integration Test Template](integration-test-template.md) | [Return to INDEX](INDEX.md)
