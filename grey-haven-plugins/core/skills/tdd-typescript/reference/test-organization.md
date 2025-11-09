# Test Organization

File structure, naming conventions, and organization patterns for test suites.

## File Structure

### Collocated Tests (Recommended)

```
src/
├── components/
│   ├── UserCard.tsx
│   └── UserCard.test.tsx          # Test next to component
├── hooks/
│   ├── useCounter.ts
│   └── useCounter.test.ts          # Test next to hook
└── utils/
    ├── formatCurrency.ts
    └── formatCurrency.test.ts      # Test next to utility
```

**Pros**: Easy to find tests, imports are simple
**Cons**: Clutters source directory

### Separate Test Directory

```
src/
├── components/
│   └── UserCard.tsx
├── hooks/
│   └── useCounter.ts
└── __tests__/
    ├── components/
    │   └── UserCard.test.tsx
    └── hooks/
        └── useCounter.test.ts
```

**Pros**: Cleaner source directory
**Cons**: Harder to find related tests

## Naming Conventions

### Test Files

- **Pattern**: `{filename}.test.{ts|tsx}`
- **Examples**:
  - `UserCard.test.tsx`
  - `useCounter.test.ts`
  - `formatCurrency.test.ts`

### Test Suites

```typescript
describe('ComponentName', () => {
  describe('method/feature', () => {
    it('does something specific', () => {});
  });
});
```

**Example**:
```typescript
describe('UserCard', () => {
  describe('rendering', () => {
    it('displays user name', () => {});
    it('displays user email', () => {});
  });

  describe('interactions', () => {
    it('calls onClick when clicked', () => {});
  });
});
```

### Test Names

**Good**:
- `it('displays user name')`
- `it('returns 404 when user not found')`
- `it('validates email format')`

**Bad**:
- `it('works')`
- `it('test1')`
- `it('should work correctly')`

## Test Grouping

### By Feature

```typescript
describe('User Authentication', () => {
  describe('login', () => {
    it('succeeds with valid credentials', () => {});
    it('fails with invalid password', () => {});
  });

  describe('logout', () => {
    it('clears session', () => {});
  });
});
```

### By State

```typescript
describe('UserProfile', () => {
  describe('when loading', () => {
    it('shows skeleton loader', () => {});
  });

  describe('when loaded', () => {
    it('displays user data', () => {});
  });

  describe('when error', () => {
    it('shows error message', () => {});
  });
});
```

## Test Data Management

### Inline Data (Simple Cases)

```typescript
it('formats currency', () => {
  expect(formatCurrency(100)).toBe('$100.00');
});
```

### Test Fixtures (Reusable Data)

```typescript
// fixtures/users.ts
export const mockUser = {
  id: '1',
  name: 'Alice',
  email: 'alice@example.com'
};

// In tests
import { mockUser } from '../fixtures/users';

it('displays user', () => {
  render(<UserCard user={mockUser} />);
});
```

### Factory Functions (Dynamic Data)

```typescript
// factories/user.ts
export function createUser(overrides = {}) {
  return {
    id: crypto.randomUUID(),
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  };
}

// In tests
it('creates multiple users', () => {
  const user1 = createUser({ name: 'Alice' });
  const user2 = createUser({ name: 'Bob' });
});
```

## Test Coverage

### What to Test

✅ **Test**:
- Public API (exported functions/components)
- Edge cases (null, empty, boundary values)
- Error handling
- User interactions
- State changes

❌ **Don't Test**:
- Implementation details
- Third-party libraries
- Framework internals
- Private functions (test through public API)

### Coverage Thresholds

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      lines: 80,           // 80% line coverage
      functions: 80,       // 80% function coverage
      branches: 80,        // 80% branch coverage
      statements: 80       // 80% statement coverage
    }
  }
});
```

## Test Pyramid

```
      /\
     /  \    E2E (Few)
    /    \
   /------\  Integration (Some)
  /        \
 /----------\ Unit (Many)
```

**Unit Tests** (70-80%):
- Fast, isolated, test single functions/components
- Mock dependencies
- Run in milliseconds

**Integration Tests** (15-25%):
- Test multiple units together
- Some real dependencies
- Run in seconds

**E2E Tests** (5-10%):
- Test full user workflows
- Real browser, database, APIs
- Run in minutes

## Test Utilities

### Custom Test Utils

```typescript
// test-utils.tsx
export function renderWithProviders(component) {
  return render(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router}>
        {component}
      </RouterProvider>
    </QueryClientProvider>
  );
}

export { screen, userEvent } from '@testing-library/react';
```

### Mock Utilities

```typescript
// mocks/api.ts
export function mockApiResponse(data) {
  return Promise.resolve({ json: () => Promise.resolve(data) });
}
```

## Quick Reference

| Aspect | Recommendation |
|--------|---------------|
| **Location** | Collocated (next to source) |
| **Naming** | `{filename}.test.{ts\|tsx}` |
| **Structure** | describe → it → expect |
| **Data** | Fixtures for reusable, inline for simple |
| **Coverage** | 80% threshold |
| **Pyramid** | Many unit, some integration, few e2e |

---

**Best Practice**: Organize tests to match source structure, use descriptive names, aim for 80% coverage with focus on unit tests.
