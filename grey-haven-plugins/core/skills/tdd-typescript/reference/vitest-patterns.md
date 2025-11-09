# Vitest Patterns

Essential Vitest patterns and best practices for TypeScript testing.

## Test Structure

### Basic Test

```typescript
import { describe, it, expect } from 'vitest';

describe('Calculator', () => {
  it('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

### Nested Describes

```typescript
describe('User', () => {
  describe('validation', () => {
    it('requires email', () => { ... });
    it('requires name', () => { ... });
  });

  describe('authentication', () => {
    it('hashes password', () => { ... });
  });
});
```

## Assertions

| Matcher | Use Case | Example |
|---------|----------|---------|
| `.toBe()` | Primitive equality | `expect(count).toBe(5)` |
| `.toEqual()` | Deep object equality | `expect(user).toEqual({ name: 'Alice' })` |
| `.toMatch()` | String/Regex match | `expect(email).toMatch(/@/)` |
| `.toContain()` | Array/String contains | `expect(list).toContain('item')` |
| `.toBeNull()` | Null check | `expect(value).toBeNull()` |
| `.toBeUndefined()` | Undefined check | `expect(value).toBeUndefined()` |
| `.toBeTruthy()` | Truthy check | `expect(value).toBeTruthy()` |
| `.toBeFalsy()` | Falsy check | `expect(value).toBeFalsy()` |
| `.toMatchObject()` | Partial object match | `expect(user).toMatchObject({ name: 'Alice' })` |
| `.toThrow()` | Exception thrown | `expect(() => fn()).toThrow('error')` |

## Setup and Teardown

### beforeEach / afterEach

```typescript
describe('Database', () => {
  beforeEach(async () => {
    await db.connect();
    await db.seed();
  });

  afterEach(async () => {
    await db.clean();
    await db.disconnect();
  });

  it('queries users', async () => { ... });
});
```

### beforeAll / afterAll

```typescript
describe('API', () => {
  let server;

  beforeAll(async () => {
    server = await startServer();
  });

  afterAll(async () => {
    await server.close();
  });

  it('responds to requests', () => { ... });
});
```

## Mocking

### Mock Functions

```typescript
import { vi } from 'vitest';

it('calls callback', () => {
  const callback = vi.fn();
  processData(data, callback);

  expect(callback).toHaveBeenCalled();
  expect(callback).toHaveBeenCalledWith(expectedData);
  expect(callback).toHaveBeenCalledTimes(1);
});
```

### Spy on Methods

```typescript
it('logs errors', () => {
  const spy = vi.spyOn(console, 'error');

  handleError(new Error('test'));

  expect(spy).toHaveBeenCalledWith('test');
  spy.mockRestore();
});
```

### Mock Modules

```typescript
vi.mock('./api', () => ({
  fetchUser: vi.fn(() => Promise.resolve({ id: '1', name: 'Alice' }))
}));

it('fetches user data', async () => {
  const user = await getUserProfile('1');
  expect(user.name).toBe('Alice');
});
```

### Mock Implementation

```typescript
const mockFetch = vi.fn();

mockFetch.mockResolvedValue({ json: () => ({ data: 'test' }) });
mockFetch.mockRejectedValue(new Error('Failed'));
mockFetch.mockImplementation((url) => {
  if (url === '/users') return { data: users };
  throw new Error('Not found');
});
```

## Async Testing

### Async/Await

```typescript
it('fetches user data', async () => {
  const user = await fetchUser('1');
  expect(user.name).toBe('Alice');
});
```

### Promises

```typescript
it('returns promise', () => {
  return fetchUser('1').then((user) => {
    expect(user.name).toBe('Alice');
  });
});
```

### Error Handling

```typescript
it('throws on invalid input', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Not found');
});
```

## Snapshot Testing

### Basic Snapshot

```typescript
it('renders correctly', () => {
  const result = renderComponent(<UserCard user={user} />);
  expect(result).toMatchSnapshot();
});
```

### Inline Snapshots

```typescript
it('formats output', () => {
  expect(formatUser(user)).toMatchInlineSnapshot(`
    {
      "name": "Alice",
      "email": "alice@example.com"
    }
  `);
});
```

### Update Snapshots

```bash
bun test -u  # Update all snapshots
bun test --update-snapshot  # Same
```

## Test Isolation

### Each Test Independent

```typescript
// Bad: Shared mutable state
let counter = 0;

it('increments', () => {
  counter++;
  expect(counter).toBe(1);
});

it('increments again', () => {
  counter++; // Depends on previous test
  expect(counter).toBe(2);
});

// Good: Fresh state per test
it('increments from 0', () => {
  const counter = createCounter(0);
  counter.increment();
  expect(counter.value).toBe(1);
});
```

## Test Filtering

### Run Specific Tests

```bash
bun test user          # Run tests matching "user"
bun test --grep login  # Run tests matching "login"
```

### Skip Tests

```typescript
it.skip('not ready yet', () => { ... });
describe.skip('feature disabled', () => { ... });
```

### Only Run Specific Tests

```typescript
it.only('focus on this test', () => { ... });
describe.only('only this suite', () => { ... });
```

## Watch Mode

```bash
bun test --watch  # Re-run on file changes
```

## Coverage

```bash
bun test --coverage       # Generate coverage report
bun test --coverage.all  # Include all files
```

### Coverage Thresholds

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80
    }
  }
});
```

## Performance

### Concurrent Tests

```typescript
it.concurrent('fast test 1', async () => { ... });
it.concurrent('fast test 2', async () => { ... });
```

### Timeouts

```typescript
it('slow operation', async () => {
  // ...
}, { timeout: 10000 }); // 10 seconds
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `describe()` | Group related tests |
| `it()` / `test()` | Individual test case |
| `beforeEach()` | Setup before each test |
| `afterEach()` | Cleanup after each test |
| `vi.fn()` | Create mock function |
| `vi.spyOn()` | Spy on existing function |
| `vi.mock()` | Mock entire module |
| `expect().toBe()` | Assert equality |
| `expect().toEqual()` | Assert deep equality |
| `.rejects` / `.resolves` | Test promises |
| `it.skip()` | Skip test |
| `it.only()` | Run only this test |

---

**Best Practice**: Keep tests fast, isolated, and focused. Use mocking sparingly and test behavior, not implementation.
