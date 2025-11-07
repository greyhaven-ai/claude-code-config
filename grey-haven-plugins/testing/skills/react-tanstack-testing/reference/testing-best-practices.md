# Testing Best Practices

Patterns and utilities for effective React and TanStack testing.

## Custom Render Functions

### Basic Custom Render

```typescript
// src/test/test-utils.tsx
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  queryClient?: QueryClient;
}

export function renderWithQuery(
  ui: ReactElement,
  options?: CustomRenderOptions
) {
  const queryClient = options?.queryClient ?? new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0, staleTime: 0 },
      mutations: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>,
    options
  );
}
```

### Complete Provider Wrapper

```typescript
// src/test/test-utils.tsx
import { RouterProvider, createRouter, createMemoryHistory } from '@tanstack/react-router';
import { AuthProvider } from '../contexts/AuthContext';

interface AllProvidersOptions {
  queryClient?: QueryClient;
  initialRoute?: string;
  authContext?: {
    isAuthenticated: boolean;
    user?: any;
  };
}

export function createWrapper(options: AllProvidersOptions = {}) {
  const queryClient = options.queryClient ?? createTestQueryClient();
  const history = createMemoryHistory({
    initialEntries: [options.initialRoute || '/'],
  });
  const router = createRouter({ routeTree, history });

  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <AuthProvider value={options.authContext}>
          <RouterProvider router={router}>
            {children}
          </RouterProvider>
        </AuthProvider>
      </QueryClientProvider>
    );
  };
}

export function renderWithAllProviders(
  ui: ReactElement,
  options?: AllProvidersOptions & RenderOptions
) {
  const Wrapper = createWrapper(options);
  return render(ui, { wrapper: Wrapper, ...options });
}
```

## Mock Data Factories

### User Factory

```typescript
// src/test/factories/userFactory.ts
import { faker } from '@faker-js/faker';

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: string;
}

export function createMockUser(overrides?: Partial<User>): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    role: 'user',
    createdAt: faker.date.past().toISOString(),
    ...overrides,
  };
}

export function createMockUsers(count: number, overrides?: Partial<User>): User[] {
  return Array.from({ length: count }, () => createMockUser(overrides));
}

// Usage in tests
it('displays user list', () => {
  const users = createMockUsers(5);
  render(<UserList users={users} />);
  // ...
});
```

### Query Data Factory

```typescript
// src/test/factories/queryDataFactory.ts
import { QueryClient } from '@tanstack/react-query';

export function createQueryClientWithData(queryKey: any[], data: any) {
  const queryClient = createTestQueryClient();
  queryClient.setQueryData(queryKey, data);
  return queryClient;
}

// Usage in tests
it('shows cached users', () => {
  const users = createMockUsers(3);
  const queryClient = createQueryClientWithData(['users'], users);

  renderWithQuery(<UserList />, { queryClient });
  // Users are already in cache, no loading state
});
```

## Test Organization

### File Structure

```
src/
├── components/
│   ├── UserList/
│   │   ├── UserList.tsx
│   │   ├── UserList.test.tsx
│   │   └── index.ts
├── hooks/
│   ├── useUsers.ts
│   ├── useUsers.test.ts
└── test/
    ├── setup.ts
    ├── test-utils.tsx
    ├── factories/
    │   ├── userFactory.ts
    │   └── postFactory.ts
    └── msw/
        ├── server.ts
        └── handlers.ts
```

### Test File Patterns

```typescript
// Component test pattern
describe('UserList', () => {
  // Group by functionality
  describe('rendering', () => {
    it('displays all users', () => {});
    it('shows empty state when no users', () => {});
  });

  describe('interactions', () => {
    it('navigates to user detail on click', async () => {});
    it('deletes user on delete button click', async () => {});
  });

  describe('loading states', () => {
    it('shows skeleton while loading', () => {});
    it('shows error message on failure', async () => {});
  });
});
```

## MSW Best Practices

### Handler Organization

```typescript
// src/test/msw/handlers/users.ts
import { http, HttpResponse } from 'msw';

export const userHandlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([/* default users */]);
  }),
];

// src/test/msw/handlers/auth.ts
export const authHandlers = [
  http.post('/api/auth/login', async ({ request }) => {
    // Auth logic
  }),
];

// src/test/msw/handlers/index.ts
import { userHandlers } from './users';
import { authHandlers } from './auth';

export const handlers = [...userHandlers, ...authHandlers];
```

### Dynamic Handlers

```typescript
// src/test/msw/handlers/users.ts
let mockUsers = [/* default users */];

export const userHandlers = [
  http.get('/api/users', () => {
    return HttpResponse.json(mockUsers);
  }),

  http.post('/api/users', async ({ request }) => {
    const newUser = await request.json();
    mockUsers = [...mockUsers, newUser];
    return HttpResponse.json(newUser, { status: 201 });
  }),
];

// Reset between tests
export function resetMockUsers() {
  mockUsers = [/* default users */];
}

// In setup.ts
afterEach(() => {
  resetMockUsers();
});
```

## Testing Hooks

### renderHook with Providers

```typescript
// src/test/test-utils.tsx
import { renderHook, RenderHookOptions } from '@testing-library/react';

export function renderHookWithQuery<TProps, TResult>(
  hook: (props: TProps) => TResult,
  options?: RenderHookOptions<TProps> & { queryClient?: QueryClient }
) {
  const queryClient = options?.queryClient ?? createTestQueryClient();

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  return renderHook(hook, { wrapper, ...options });
}

// Usage
it('fetches users', async () => {
  const { result } = renderHookWithQuery(() => useUsers());

  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toHaveLength(3);
});
```

## Async Testing Patterns

### Using waitFor

```typescript
import { waitFor } from '@testing-library/react';

it('loads data asynchronously', async () => {
  render(<AsyncComponent />);

  // Wait for loading to complete
  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});
```

### Using findBy Queries

```typescript
it('displays user after loading', async () => {
  render(<UserProfile userId="123" />);

  // findBy automatically waits (up to 1000ms by default)
  const userName = await screen.findByText('Alice Johnson');
  expect(userName).toBeInTheDocument();
});
```

## Testing User Interactions

### userEvent Setup

```typescript
import userEvent from '@testing-library/user-event';

it('handles user input', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.type(screen.getByLabelText('Email'), 'alice@example.com');
  await user.type(screen.getByLabelText('Password'), 'password123');
  await user.click(screen.getByRole('button', { name: 'Login' }));

  expect(await screen.findByText('Welcome')).toBeInTheDocument();
});
```

### Keyboard Navigation

```typescript
it('navigates form with keyboard', async () => {
  const user = userEvent.setup();
  render(<Form />);

  await user.tab(); // Focus first field
  await user.keyboard('Alice');
  await user.tab(); // Move to next field
  await user.keyboard('alice@example.com');
  await user.keyboard('{Enter}'); // Submit form
});
```

## Testing Accessibility

### Query by Role

```typescript
it('has accessible structure', () => {
  render(<UserList users={mockUsers} />);

  expect(screen.getByRole('list')).toBeInTheDocument();
  expect(screen.getAllByRole('listitem')).toHaveLength(3);
  expect(screen.getByRole('button', { name: 'Add User' })).toBeInTheDocument();
});
```

### Aria Labels

```typescript
it('has proper aria labels', () => {
  render(<DeleteButton onDelete={mockDelete} />);

  const button = screen.getByRole('button', { name: 'Delete user' });
  expect(button).toHaveAttribute('aria-label', 'Delete user');
});
```

## Performance Testing

### Test Rendering Performance

```typescript
it('renders large list efficiently', () => {
  const users = createMockUsers(1000);
  const start = performance.now();

  render(<VirtualizedUserList users={users} />);

  const duration = performance.now() - start;
  expect(duration).toBeLessThan(100); // Should render in <100ms
});
```

### Test Query Performance

```typescript
it('avoids N+1 queries', () => {
  const spy = vi.spyOn(window, 'fetch');

  render(<UsersWithPosts />);

  waitFor(() => {
    expect(spy).toHaveBeenCalledTimes(1); // Single query with join
  });
});
```

## Snapshot Testing

### Component Snapshot

```typescript
it('matches snapshot', () => {
  const { container } = render(<UserCard user={mockUser} />);
  expect(container).toMatchSnapshot();
});
```

### Inline Snapshot

```typescript
it('renders correct HTML', () => {
  render(<Button>Click me</Button>);

  expect(screen.getByRole('button')).toMatchInlineSnapshot(`
    <button>
      Click me
    </button>
  `);
});
```

## Coverage Exclusions

### Exclude from Coverage

```typescript
/* v8 ignore start */
if (process.env.NODE_ENV === 'development') {
  // Dev-only code excluded from coverage
}
/* v8 ignore stop */
```

### Exclude Test Files

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      exclude: [
        'src/test/**',
        '**/*.test.{ts,tsx}',
        '**/*.spec.{ts,tsx}',
        '**/mockData.ts',
      ],
    },
  },
});
```

## CI/CD Best Practices

### Parallel Testing

```bash
# Run tests in parallel
vitest --threads --maxThreads=4

# Run specific tests
vitest src/components/UserList
```

### Coverage Enforcement

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
      // Fail CI if below thresholds
      reporter: ['text', 'json-summary'],
    },
  },
});
```

## Key Takeaways

1. **Custom Utilities**: Create reusable render functions with all providers
2. **Mock Factories**: Use faker for consistent test data
3. **MSW Organization**: Group handlers by domain (users, auth, posts)
4. **Async Testing**: Prefer `findBy` and `waitFor` for async operations
5. **Accessibility**: Always query by role first
6. **Coverage**: Aim for 80%+ with meaningful tests

---

**Next**: [Server Components Testing](server-components-testing.md) | **Previous**: [Testing Setup](testing-setup.md)
