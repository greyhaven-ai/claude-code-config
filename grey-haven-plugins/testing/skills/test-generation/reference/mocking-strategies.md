# Mocking Strategies

Complete guide to mocking - when to mock, how to mock, mock verification, and avoiding over-mocking.

## When to Mock

### Good Reasons to Mock

**External APIs and Services**:
```typescript
// ✅ Mock external payment API
vi.mock('stripe', () => ({
  default: {
    charges: {
      create: vi.fn().mockResolvedValue({ id: 'ch_123', status: 'succeeded' }),
    },
  },
}));
```

**Why**: External services are slow, cost money, or unavailable in test environment.

**Database Calls**:
```python
# ✅ Mock database queries for unit tests
@patch('app.database.get_session')
def test_create_user(mock_get_session):
    mock_session = Mock()
    mock_get_session.return_value = mock_session
    # Test business logic without real database
```

**Why**: Database calls are slow and require setup/teardown.

**Time-Dependent Code**:
```typescript
// ✅ Mock current time for consistent tests
vi.useFakeTimers();
vi.setSystemTime(new Date('2024-01-15T10:00:00Z'));
```

**Why**: Tests should be deterministic, not dependent on when they run.

**Non-Deterministic Functions**:
```typescript
// ✅ Mock random number generation
vi.spyOn(Math, 'random').mockReturnValue(0.5);
```

**Why**: Tests need consistent, predictable results.

### Bad Reasons to Mock

**Simple Utility Functions**:
```typescript
// ❌ Don't mock simple utilities
// Bad:
vi.mock('./utils', () => ({
  formatCurrency: vi.fn().mockReturnValue('$99.99'),
}));

// ✅ Good: Just call the real function
import { formatCurrency } from './utils';
expect(formatCurrency(99.99)).toBe('$99.99');
```

**Why**: Testing real implementation is faster and more valuable.

**Internal Business Logic**:
```typescript
// ❌ Don't mock your own business logic
// Bad:
vi.mock('./calculateDiscount');

// ✅ Good: Test the real calculation
import { calculateDiscount } from './calculateDiscount';
expect(calculateDiscount(100, 0.2)).toBe(80);
```

**Why**: You want to test actual behavior, not mocked behavior.

**React Components** (in most cases):
```typescript
// ❌ Don't mock child components unless necessary
// Bad:
vi.mock('./Button', () => ({ Button: () => <div>Mocked Button</div> }));

// ✅ Good: Render real component
render(<UserProfile />); // Includes real Button component
```

**Why**: Integration between components is important to test.

## Mocking APIs

### Vitest: Mocking fetch

**Basic fetch mock**:
```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('fetchUser', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('should fetch user successfully', async () => {
    const mockUser = { id: '123', name: 'John Doe' };

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const user = await fetchUser('123');

    expect(fetch).toHaveBeenCalledWith('/api/users/123');
    expect(user).toEqual(mockUser);
  });

  it('should handle API errors', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 404,
    });

    await expect(fetchUser('999')).rejects.toThrow('User not found');
  });
});
```

### pytest: Mocking httpx or requests

**Mocking httpx client**:
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@patch('app.services.httpx.AsyncClient')
async def test_fetch_user(mock_client):
    """Should fetch user from external API"""
    # Setup mock
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'id': '123', 'name': 'John Doe'}

    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

    # Test
    user = await fetch_user('123')

    assert user['name'] == 'John Doe'
```

## Mocking TanStack Query

### Mocking Queries

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

describe('useUser', () => {
  it('should fetch user successfully', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: '123', name: 'John' }),
    });

    const { result } = renderHook(() => useUser('123'), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual({ id: '123', name: 'John' });
  });

  it('should handle loading state', () => {
    global.fetch = vi.fn().mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    const { result } = renderHook(() => useUser('123'), {
      wrapper: createWrapper(),
    });

    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBeUndefined();
  });
});
```

### Mocking Mutations

```typescript
describe('useCreateUser', () => {
  it('should create user and invalidate queries', async () => {
    const queryClient = new QueryClient();
    const invalidateQueriesSpy = vi.spyOn(queryClient, 'invalidateQueries');

    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: '123', name: 'John' }),
    });

    const wrapper = ({ children }: any) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );

    const { result } = renderHook(() => useCreateUser(), { wrapper });

    result.current.mutate({ name: 'John', email: 'john@example.com' });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(invalidateQueriesSpy).toHaveBeenCalledWith({ queryKey: ['users'] });
  });
});
```

## Mocking Databases

### TypeScript: Mocking Drizzle

```typescript
import { describe, it, expect, vi } from 'vitest';
import * as schema from './schema';

describe('UserService', () => {
  it('should create user', async () => {
    const mockDb = {
      insert: vi.fn().mockReturnThis(),
      values: vi.fn().mockReturnThis(),
      returning: vi.fn().mockResolvedValue([{ id: '123', name: 'John' }]),
    };

    const userService = new UserService(mockDb as any);

    const user = await userService.createUser({ name: 'John', email: 'john@example.com' });

    expect(mockDb.insert).toHaveBeenCalledWith(schema.users);
    expect(user.name).toBe('John');
  });
});
```

### Python: Mocking SQLModel Session

```python
import pytest
from unittest.mock import Mock, patch
from app.models import User
from app.services import UserService

def test_create_user():
    """Should create user with valid data"""
    # Mock session
    mock_session = Mock()
    mock_user = User(id='123', name='John Doe', email='john@example.com')
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock(side_effect=lambda obj: setattr(obj, 'id', '123'))

    # Test
    service = UserService(mock_session)
    user = service.create_user('John Doe', 'john@example.com')

    # Verify
    assert mock_session.add.called
    assert mock_session.commit.called
```

**Better approach: Use in-memory database**:
```python
@pytest.fixture
def session():
    """Create in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

def test_create_user(session):
    """Should create user in database"""
    service = UserService(session)
    user = service.create_user('John Doe', 'john@example.com')

    # Test against real database (fast in-memory)
    assert user.id is not None
    assert user.name == 'John Doe'
```

## Spy vs Stub vs Mock

### Spy

**Calls real function but records calls**:

```typescript
import { vi } from 'vitest';

it('should log user creation', async () => {
  const logSpy = vi.spyOn(console, 'log');

  await createUser({ name: 'John' });

  expect(logSpy).toHaveBeenCalledWith('User created: John');

  logSpy.mockRestore(); // Clean up
});
```

```python
from unittest.mock import Mock

def test_log_user_creation(mocker):
    """Should log user creation"""
    log_spy = mocker.spy(logger, 'info')

    create_user('John Doe')

    log_spy.assert_called_once_with('User created: John Doe')
```

**When to use**: When you want real behavior + call tracking.

### Stub

**Returns fixed data, doesn't track calls**:

```typescript
it('should use current date', () => {
  const originalDate = Date.now;
  Date.now = () => 1705334400000; // Fixed timestamp

  const result = createTimestamp();

  expect(result).toBe(1705334400000);

  Date.now = originalDate; // Restore
});
```

**When to use**: When you need predictable return values.

### Mock

**Full replacement with call tracking**:

```typescript
it('should send email notification', async () => {
  const sendEmailMock = vi.fn().mockResolvedValue({ success: true });

  const emailService = { sendEmail: sendEmailMock };

  await notifyUser(emailService, 'john@example.com');

  expect(sendEmailMock).toHaveBeenCalledWith('john@example.com', expect.any(String));
});
```

**When to use**: When you need to replace behavior + track calls.

## Module Mocking

### Vitest: vi.mock

**Mock entire module**:
```typescript
vi.mock('./emailService', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true }),
  EmailService: vi.fn(() => ({
    send: vi.fn().mockResolvedValue({ success: true }),
  })),
}));
```

**Partial module mock**:
```typescript
import * as emailService from './emailService';

vi.spyOn(emailService, 'sendEmail').mockResolvedValue({ success: true });
// Other exports remain real
```

### pytest: patch decorator

**Mock function**:
```python
from unittest.mock import patch

@patch('app.services.email.send_email')
def test_notify_user(mock_send_email):
    """Should send notification email"""
    mock_send_email.return_value = {'success': True}

    notify_user('john@example.com', 'Welcome!')

    mock_send_email.assert_called_once_with('john@example.com', 'Welcome!')
```

**Mock class**:
```python
@patch('app.services.email.EmailService')
def test_email_service(mock_email_service_class):
    """Should use email service"""
    mock_instance = Mock()
    mock_email_service_class.return_value = mock_instance
    mock_instance.send.return_value = {'success': True}

    service = EmailService()
    result = service.send('john@example.com', 'Hello')

    assert result['success'] is True
```

## Mock Verification

### Vitest Matchers

```typescript
// Called at least once
expect(mockFn).toHaveBeenCalled();

// Called exactly N times
expect(mockFn).toHaveBeenCalledTimes(3);

// Called with specific arguments
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');

// Called with partial match
expect(mockFn).toHaveBeenCalledWith(expect.objectContaining({
  name: 'John',
}));

// Last call
expect(mockFn).toHaveBeenLastCalledWith('lastArg');

// Nth call
expect(mockFn).toHaveBeenNthCalledWith(2, 'secondCallArg');

// Return value
expect(mockFn).toHaveReturnedWith({ success: true });
```

### pytest Assertions

```python
# Called at least once
mock_fn.assert_called()

# Called exactly once
mock_fn.assert_called_once()

# Called with specific arguments
mock_fn.assert_called_with('arg1', 'arg2')

# Called once with specific arguments
mock_fn.assert_called_once_with('arg1', 'arg2')

# Any call matches
mock_fn.assert_any_call('arg1')

# Check call count
assert mock_fn.call_count == 3

# Check all calls
assert mock_fn.call_args_list == [
    call('first'),
    call('second'),
    call('third'),
]
```

## Avoiding Over-Mocking

### Problem: Testing Mock Behavior

```typescript
// ❌ Bad: Testing mock behavior, not real code
it('should format user', () => {
  const formatUser = vi.fn().mockReturnValue('John Doe (john@example.com)');

  const result = formatUser({ name: 'John Doe', email: 'john@example.com' });

  expect(result).toBe('John Doe (john@example.com)');
});
```

This test passes but doesn't verify the real `formatUser` function works!

```typescript
// ✅ Good: Test real implementation
it('should format user', () => {
  const result = formatUser({ name: 'John Doe', email: 'john@example.com' });

  expect(result).toBe('John Doe (john@example.com)');
});
```

### Problem: Mocking Everything

```typescript
// ❌ Bad: Mocking all dependencies
it('should create order', () => {
  const mockValidate = vi.fn().mockReturnValue(true);
  const mockCalculate = vi.fn().mockReturnValue(99.99);
  const mockSave = vi.fn().mockResolvedValue({ id: '123' });

  // What are we actually testing here?
});
```

```typescript
// ✅ Good: Only mock external dependencies
it('should create order', async () => {
  const mockDb = createMockDb(); // Only mock database

  // Test real validation and calculation logic
  const order = await createOrder(mockDb, { items: [...] });

  expect(order.total).toBe(99.99); // Real calculation tested
});
```

### Problem: Brittle Tests

```typescript
// ❌ Bad: Over-specified mocks
it('should update user', () => {
  const mockDb = {
    update: vi.fn(),
    where: vi.fn(),
    set: vi.fn(),
  };

  updateUser(mockDb, '123', { name: 'John' });

  // Test breaks if implementation changes slightly
  expect(mockDb.update).toHaveBeenCalledWith('users');
  expect(mockDb.where).toHaveBeenCalledWith({ id: '123' });
  expect(mockDb.set).toHaveBeenCalledWith({ name: 'John' });
});
```

```typescript
// ✅ Good: Test outcomes, not implementation
it('should update user', async () => {
  const db = createTestDb(); // Real in-memory database
  await db.insert(users).values({ id: '123', name: 'Jane' });

  await updateUser(db, '123', { name: 'John' });

  const user = await db.select().from(users).where(eq(users.id, '123'));
  expect(user.name).toBe('John'); // Test actual result
});
```

## Real-World Mocking Example

### Scenario: Order Processing System

```typescript
// src/services/OrderService.ts
export class OrderService {
  constructor(
    private db: Database,
    private paymentGateway: PaymentGateway,
    private inventoryService: InventoryService,
    private emailService: EmailService,
  ) {}

  async createOrder(order: CreateOrderInput): Promise<Order> {
    // 1. Validate inventory (real logic - test it)
    const available = await this.inventoryService.checkAvailability(order.items);
    if (!available) {
      throw new Error('Items out of stock');
    }

    // 2. Calculate total (real logic - test it)
    const total = this.calculateTotal(order.items);

    // 3. Process payment (external - mock it)
    const payment = await this.paymentGateway.charge(total);

    // 4. Save to database (external - mock it)
    const savedOrder = await this.db.insert(orders).values({
      ...order,
      total,
      paymentId: payment.id,
    });

    // 5. Send confirmation (external - mock it)
    await this.emailService.sendOrderConfirmation(savedOrder);

    return savedOrder;
  }

  private calculateTotal(items: OrderItem[]): number {
    // Real business logic - don't mock
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }
}
```

**Good test strategy**:
```typescript
describe('OrderService', () => {
  it('should create order successfully', async () => {
    // Mock only external dependencies
    const mockDb = {
      insert: vi.fn().mockReturnThis(),
      values: vi.fn().mockResolvedValue({ id: '123' }),
    };

    const mockPayment = {
      charge: vi.fn().mockResolvedValue({ id: 'pay_123', status: 'succeeded' }),
    };

    const mockEmail = {
      sendOrderConfirmation: vi.fn().mockResolvedValue(undefined),
    };

    // Use real inventory service (or in-memory stub)
    const inventoryService = new InventoryService(inMemoryInventory);

    const service = new OrderService(
      mockDb as any,
      mockPayment,
      inventoryService, // Real service
      mockEmail,
    );

    const order = await service.createOrder({
      items: [
        { productId: '1', price: 50, quantity: 2 },
        { productId: '2', price: 25, quantity: 1 },
      ],
    });

    // Verify real calculation worked
    expect(order.total).toBe(125); // 50*2 + 25*1

    // Verify external services called correctly
    expect(mockPayment.charge).toHaveBeenCalledWith(125);
    expect(mockEmail.sendOrderConfirmation).toHaveBeenCalledWith(
      expect.objectContaining({ id: '123' })
    );
  });
});
```

## Quick Reference

### When to Mock
- ✅ External APIs and services
- ✅ Database calls (or use in-memory DB)
- ✅ Time-dependent code
- ✅ Non-deterministic functions
- ❌ Simple utility functions
- ❌ Internal business logic
- ❌ React components (usually)

### Mock Types
- **Spy**: Real function + call tracking
- **Stub**: Fixed return value
- **Mock**: Full replacement + call tracking

### Verification Patterns
```typescript
// Vitest
expect(mock).toHaveBeenCalled()
expect(mock).toHaveBeenCalledWith(args)
expect(mock).toHaveBeenCalledTimes(n)

// pytest
mock.assert_called()
mock.assert_called_with(args)
assert mock.call_count == n
```

---

Related: [Testing Patterns](testing-patterns.md) | [Test Structure Guide](test-structure-guide.md) | [Coverage Standards](coverage-standards.md) | [Return to INDEX](INDEX.md)
