# Testing Patterns Reference

Comprehensive patterns for Vitest (TypeScript) and pytest (Python) covering unit tests, integration tests, and advanced mocking.

## AAA Pattern (Arrange-Act-Assert)

**The Gold Standard** for test structure - makes tests readable and maintainable.

### TypeScript/Vitest

```typescript
import { describe, it, expect } from 'vitest';

describe('Calculator', () => {
  it('should add two numbers correctly', () => {
    // Arrange: Set up test data and dependencies
    const calculator = new Calculator();
    const a = 5;
    const b = 3;

    // Act: Execute the function being tested
    const result = calculator.add(a, b);

    // Assert: Verify the result
    expect(result).toBe(8);
  });
});
```

### Python/pytest

```python
import pytest

class TestCalculator:
    def test_add_two_numbers(self):
        # Arrange
        calculator = Calculator()
        a = 5
        b = 3

        # Act
        result = calculator.add(a, b)

        # Assert
        assert result == 8
```

## Fixtures and Setup/Teardown

### Vitest Fixtures

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

describe('UserService', () => {
  let userService: UserService;
  let mockDatabase: any;

  // Run before each test
  beforeEach(() => {
    mockDatabase = {
      query: vi.fn(),
      insert: vi.fn(),
    };
    userService = new UserService(mockDatabase);
  });

  // Run after each test
  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should create user', async () => {
    mockDatabase.insert.mockResolvedValue({ id: '123' });

    const user = await userService.createUser({ email: 'test@example.com' });

    expect(user.id).toBe('123');
    expect(mockDatabase.insert).toHaveBeenCalledOnce();
  });
});
```

### pytest Fixtures

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_database():
    """Create a mock database for testing"""
    db = Mock()
    db.query.return_value = []
    db.insert.return_value = {'id': '123'}
    return db

@pytest.fixture
def user_service(mock_database):
    """Create UserService with mocked database"""
    return UserService(mock_database)

class TestUserService:
    def test_create_user(self, user_service, mock_database):
        """Test user creation"""
        user = user_service.create_user(email='test@example.com')

        assert user['id'] == '123'
        mock_database.insert.assert_called_once()
```

## Async Testing Patterns

### Vitest Async/Await

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('Async Operations', () => {
  it('should fetch data successfully', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ data: 'test' }),
    });
    global.fetch = mockFetch;

    const result = await fetchData();

    expect(result.data).toBe('test');
  });

  it('should handle fetch errors', async () => {
    const mockFetch = vi.fn().mockRejectedValue(new Error('Network error'));
    global.fetch = mockFetch;

    await expect(fetchData()).rejects.toThrow('Network error');
  });
});
```

### pytest Async (pytest-asyncio)

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_data_success():
    """Test successful async data fetch"""
    mock_client = AsyncMock()
    mock_client.get.return_value = {'data': 'test'}

    result = await fetch_data(mock_client)

    assert result['data'] == 'test'
    mock_client.get.assert_awaited_once()

@pytest.mark.asyncio
async def test_fetch_data_error():
    """Test async error handling"""
    mock_client = AsyncMock()
    mock_client.get.side_effect = NetworkError('Connection failed')

    with pytest.raises(NetworkError, match='Connection failed'):
        await fetch_data(mock_client)
```

## TanStack Query Testing Patterns

### Testing Queries

```typescript
import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUsers } from './useUsers';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe('useUsers', () => {
  it('should fetch users successfully', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [{ id: '1', name: 'John' }],
    });
    global.fetch = mockFetch;

    const { result } = renderHook(() => useUsers(), {
      wrapper: createWrapper(),
    });

    // Initially loading
    expect(result.current.isLoading).toBe(true);

    // Wait for success
    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual([{ id: '1', name: 'John' }]);
  });

  it('should handle query errors', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
    });
    global.fetch = mockFetch;

    const { result } = renderHook(() => useUsers(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error).toBeDefined();
  });
});
```

### Testing Mutations

```typescript
describe('useCreateUser', () => {
  it('should create user successfully', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: '123', name: 'John' }),
    });
    global.fetch = mockFetch;

    const { result } = renderHook(() => useCreateUser(), {
      wrapper: createWrapper(),
    });

    // Trigger mutation
    result.current.mutate({ name: 'John', email: 'john@example.com' });

    // Wait for success
    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual({ id: '123', name: 'John' });
    expect(mockFetch).toHaveBeenCalledWith('/api/users', {
      method: 'POST',
      body: JSON.stringify({ name: 'John', email: 'john@example.com' }),
    });
  });

  it('should call onSuccess callback', async () => {
    const onSuccess = vi.fn();
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: '123' }),
    });
    global.fetch = mockFetch;

    const { result } = renderHook(() => useCreateUser(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ name: 'John' }, { onSuccess });

    await waitFor(() => expect(onSuccess).toHaveBeenCalled());
  });
});
```

## React Testing Library Patterns

### User Interactions

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('should handle form submission', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    // Type into inputs
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    // Click submit button
    await user.click(screen.getByRole('button', { name: /log in/i }));

    // Verify submission
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('should handle keyboard navigation', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);

    // Tab through form
    await user.tab();
    expect(screen.getByLabelText(/email/i)).toHaveFocus();

    await user.tab();
    expect(screen.getByLabelText(/password/i)).toHaveFocus();

    await user.tab();
    expect(screen.getByRole('button', { name: /log in/i })).toHaveFocus();

    // Submit with Enter
    await user.keyboard('{Enter}');
  });
});
```

### Accessibility Testing

```typescript
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<LoginForm />);

    const results = await axe(container);

    expect(results).toHaveNoViolations();
  });

  it('should associate errors with inputs', async () => {
    render(<LoginForm />);

    const emailInput = screen.getByLabelText(/email/i);

    // Trigger validation error
    await userEvent.click(screen.getByRole('button', { name: /log in/i }));

    // Check ARIA attributes
    expect(emailInput).toHaveAttribute('aria-invalid', 'true');
    expect(emailInput).toHaveAttribute('aria-describedby');

    // Error should be announced to screen readers
    const error = screen.getByRole('alert');
    expect(error).toBeInTheDocument();
  });
});
```

## FastAPI Testing Patterns

### Testing with TestClient

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """Test user creation endpoint"""
    response = client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User"},
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```

### Testing with Database

```python
import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    """Create test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with database session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_and_get_user(client, session):
    """Test user creation and retrieval"""
    # Create user
    create_response = client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test"},
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Get user
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "test@example.com"

    # Verify in database
    user = session.get(User, user_id)
    assert user is not None
    assert user.email == "test@example.com"
```

### Testing Authentication

```python
@pytest.fixture
def auth_headers(user_token):
    """Authenticated request headers"""
    return {"Authorization": f"Bearer {user_token}"}

def test_protected_endpoint_without_auth(client):
    """Test that protected endpoints require auth"""
    response = client.get("/users/me")
    assert response.status_code == 401

def test_protected_endpoint_with_auth(client, auth_headers):
    """Test authenticated request"""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
```

## Parametrized Testing

### Vitest Parametrized

```typescript
import { describe, it, expect } from 'vitest';

describe.each([
  { input: 'test@example.com', expected: true },
  { input: 'invalid-email', expected: false },
  { input: '@example.com', expected: false },
  { input: 'test@', expected: false },
  { input: '', expected: false },
])('validateEmail($input)', ({ input, expected }) => {
  it(`should return ${expected}`, () => {
    expect(validateEmail(input)).toBe(expected);
  });
});
```

### pytest Parametrized

```python
import pytest

@pytest.mark.parametrize("input_email,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("@example.com", False),
    ("test@", False),
    ("", False),
])
def test_validate_email(input_email, expected):
    """Test email validation with various inputs"""
    assert validate_email(input_email) == expected
```

## Snapshot Testing

### Vitest Snapshots

```typescript
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';

describe('UserCard', () => {
  it('should match snapshot', () => {
    const { container } = render(
      <UserCard
        name="John Doe"
        email="john@example.com"
        role="admin"
      />
    );

    expect(container).toMatchSnapshot();
  });

  it('should match inline snapshot', () => {
    const user = { id: '123', name: 'John', role: 'admin' };

    expect(user).toMatchInlineSnapshot(`
      {
        "id": "123",
        "name": "John",
        "role": "admin",
      }
    `);
  });
});
```

## Error Testing Patterns

### TypeScript Error Handling

```typescript
describe('Error Handling', () => {
  it('should throw error for invalid input', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  it('should throw specific error type', () => {
    expect(() => validateUser(null)).toThrow(ValidationError);
  });

  it('should handle async errors', async () => {
    await expect(fetchUser('invalid-id')).rejects.toThrow('User not found');
  });

  it('should match error message pattern', () => {
    expect(() => processPayment(-100)).toThrow(/amount must be positive/i);
  });
});
```

### Python Error Handling

```python
import pytest

def test_division_by_zero():
    """Test that division by zero raises error"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_validation_error_message():
    """Test error message content"""
    with pytest.raises(ValidationError, match="Invalid email"):
        validate_user(email="not-an-email")

@pytest.mark.asyncio
async def test_async_error():
    """Test async error handling"""
    with pytest.raises(UserNotFoundError):
        await fetch_user("invalid-id")
```

## Spy, Stub, and Mock Patterns

### Vitest Spies

```typescript
describe('Spies', () => {
  it('should spy on method calls', () => {
    const logger = { log: vi.fn() };
    const service = new UserService(logger);

    service.createUser({ email: 'test@example.com' });

    expect(logger.log).toHaveBeenCalledWith('User created: test@example.com');
    expect(logger.log).toHaveBeenCalledTimes(1);
  });

  it('should spy on existing method', () => {
    const user = { save: () => true };
    const spy = vi.spyOn(user, 'save');

    user.save();

    expect(spy).toHaveBeenCalled();
  });
});
```

### pytest Mocks

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test using mock object"""
    mock_db = Mock()
    mock_db.query.return_value = [{'id': '1', 'name': 'John'}]

    service = UserService(mock_db)
    users = service.get_users()

    assert len(users) == 1
    mock_db.query.assert_called_once()

@patch('app.services.send_email')
def test_with_patch(mock_send_email):
    """Test using patch decorator"""
    mock_send_email.return_value = True

    result = notify_user(user_id='123')

    assert result is True
    mock_send_email.assert_called_with(
        to='user@example.com',
        subject='Notification'
    )
```

## Time-based Testing

### Vitest Fake Timers

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('Time-dependent', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should delay execution', () => {
    const callback = vi.fn();

    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalled();
  });

  it('should handle intervals', () => {
    const callback = vi.fn();

    setInterval(callback, 100);

    vi.advanceTimersByTime(250);

    expect(callback).toHaveBeenCalledTimes(2);
  });
});
```

### pytest Freezegun

```python
import pytest
from freezegun import freeze_time
from datetime import datetime

@freeze_time("2024-01-15 12:00:00")
def test_current_time():
    """Test with frozen time"""
    result = get_current_timestamp()
    assert result == datetime(2024, 1, 15, 12, 0, 0)

def test_time_progression():
    """Test time progression"""
    with freeze_time("2024-01-15") as frozen_time:
        initial = get_current_date()

        frozen_time.tick(delta=timedelta(days=1))

        next_day = get_current_date()
        assert next_day == initial + timedelta(days=1)
```

---

Related: [Test Structure Guide](test-structure-guide.md) | [Mocking Strategies](mocking-strategies.md) | [Coverage Standards](coverage-standards.md) | [Return to INDEX](INDEX.md)
