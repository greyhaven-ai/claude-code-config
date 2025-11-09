# TanStack Query Testing Examples

Complete examples for testing TanStack Query (React Query) hooks and components.

## Test Setup

### QueryClient Configuration

```typescript
// src/test/query-client.ts
import { QueryClient } from '@tanstack/react-query';

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,        // Don't retry in tests
        gcTime: 0,          // No garbage collection
        staleTime: 0,       // Always stale
      },
      mutations: {
        retry: false,
      },
    },
  });
}
```

### Custom Render with QueryClientProvider

```typescript
// src/test/test-utils.tsx
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { createTestQueryClient } from './query-client';

export function renderWithQuery(
  ui: ReactElement,
  options?: RenderOptions
) {
  const queryClient = createTestQueryClient();

  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>,
    options
  );
}
```

## Example 1: Testing Query Hooks

### Hook Under Test

```typescript
// src/hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users');
      if (!response.ok) throw new Error('Failed to fetch users');
      return response.json() as Promise<User[]>;
    },
  });
}
```

### Test Suite

```typescript
// src/hooks/useUsers.test.ts
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { createTestQueryClient } from '../test/query-client';
import { useUsers } from './useUsers';

// Mock API server
const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('useUsers', () => {
  it('fetches users successfully', async () => {
    const queryClient = createTestQueryClient();
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );

    const { result } = renderHook(() => useUsers(), { wrapper });

    // Initially loading
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBeUndefined();

    // Wait for success
    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual([
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);
  });
});
```

## Example 2: Testing Mutation Hooks

### Hook Under Test

```typescript
// src/hooks/useCreateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CreateUserInput {
  name: string;
  email: string;
}

interface User extends CreateUserInput {
  id: string;
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: CreateUserInput) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });
      if (!response.ok) throw new Error('Failed to create user');
      return response.json() as Promise<User>;
    },
    onSuccess: () => {
      // Invalidate users query to refetch
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Test Suite

```typescript
// src/hooks/useCreateUser.test.ts
import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { createTestQueryClient } from '../test/query-client';
import { useCreateUser } from './useCreateUser';

const server = setupServer(
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      id: '3',
      ...body,
    });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('useCreateUser', () => {
  it('creates user successfully', async () => {
    const queryClient = createTestQueryClient();
    const invalidateQueriesSpy = vi.spyOn(queryClient, 'invalidateQueries');

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );

    const { result } = renderHook(() => useCreateUser(), { wrapper });

    // Initially idle
    expect(result.current.isPending).toBe(false);

    // Trigger mutation
    result.current.mutate({
      name: 'Charlie',
      email: 'charlie@example.com',
    });

    // Wait for success
    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual({
      id: '3',
      name: 'Charlie',
      email: 'charlie@example.com',
    });

    // Verify cache invalidation
    expect(invalidateQueriesSpy).toHaveBeenCalledWith({ queryKey: ['users'] });
  });
});
```

## Example 3: Testing Components with Queries

### Component Under Test

```typescript
// src/components/UserList.tsx
import { useUsers } from '../hooks/useUsers';

export function UserList() {
  const { data: users, isLoading, error } = useUsers();

  if (isLoading) {
    return <div data-testid="loading">Loading users...</div>;
  }

  if (error) {
    return <div role="alert">Error: {error.message}</div>;
  }

  if (!users || users.length === 0) {
    return <div data-testid="empty">No users found</div>;
  }

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          {user.name} - {user.email}
        </li>
      ))}
    </ul>
  );
}
```

### Test Suite

```typescript
// src/components/UserList.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { renderWithQuery } from '../test/test-utils';
import { UserList } from './UserList';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('UserList', () => {
  it('displays users after loading', async () => {
    renderWithQuery(<UserList />);

    await waitFor(() => {
      expect(screen.getByText('Alice - alice@example.com')).toBeInTheDocument();
    });

    expect(screen.getByText('Bob - bob@example.com')).toBeInTheDocument();
  });
});
```

## Example 4: Testing Optimistic Updates

### Hook with Optimistic Update

```typescript
// src/hooks/useUpdateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (user: User) => {
      const response = await fetch(`/api/users/${user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user),
      });
      if (!response.ok) throw new Error('Failed to update user');
      return response.json() as Promise<User>;
    },
    onMutate: async (updatedUser) => {
      // Cancel outgoing queries
      await queryClient.cancelQueries({ queryKey: ['users'] });

      // Snapshot previous value
      const previousUsers = queryClient.getQueryData<User[]>(['users']);

      // Optimistically update
      if (previousUsers) {
        queryClient.setQueryData<User[]>(
          ['users'],
          previousUsers.map((user) =>
            user.id === updatedUser.id ? updatedUser : user
          )
        );
      }

      // Return context for rollback
      return { previousUsers };
    },
    onError: (_error, _variables, context) => {
      // Rollback on error
      if (context?.previousUsers) {
        queryClient.setQueryData(['users'], context.previousUsers);
      }
    },
    onSettled: () => {
      // Refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Test Suite

```typescript
// src/hooks/useUpdateUser.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { createTestQueryClient } from '../test/query-client';
import { useUpdateUser } from './useUpdateUser';

const server = setupServer(
  http.put('/api/users/:id', async ({ request, params }) => {
    const body = await request.json();
    return HttpResponse.json({ ...body, id: params.id });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('useUpdateUser', () => {
  it('applies optimistic update immediately', async () => {
    const queryClient = createTestQueryClient();

    // Pre-populate cache
    queryClient.setQueryData(['users'], [
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );

    const { result } = renderHook(() => useUpdateUser(), { wrapper });

    // Trigger mutation
    result.current.mutate({
      id: '1',
      name: 'Alice Updated',
      email: 'alice.updated@example.com',
    });

    // Immediately check optimistic update
    const cachedUsers = queryClient.getQueryData(['users']);
    expect(cachedUsers).toEqual([
      { id: '1', name: 'Alice Updated', email: 'alice.updated@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);

    // Wait for mutation to complete
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
  });

  it('rolls back on mutation failure', async () => {
    server.use(
      http.put('/api/users/:id', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    const queryClient = createTestQueryClient();

    // Pre-populate cache
    const originalUsers = [
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ];
    queryClient.setQueryData(['users'], originalUsers);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );

    const { result } = renderHook(() => useUpdateUser(), { wrapper });

    // Trigger mutation
    result.current.mutate({
      id: '1',
      name: 'Alice Updated',
      email: 'alice.updated@example.com',
    });

    // Wait for error
    await waitFor(() => expect(result.current.isError).toBe(true));

    // Verify rollback
    const cachedUsers = queryClient.getQueryData(['users']);
    expect(cachedUsers).toEqual(originalUsers);
  });
});
```

## Key Takeaways

1. **Test QueryClient Setup**: Always create test-specific QueryClient with retries disabled
2. **MSW for Mocking**: Use MSW to mock API endpoints realistically
3. **Test All States**: Loading, success, error, and empty states
4. **Optimistic Updates**: Test immediate UI changes and rollback on failure
5. **Cache Invalidation**: Verify queries are invalidated after mutations

---

**Next**: [TanStack Router Testing](tanstack-router-testing.md) | **Index**: [Examples Index](INDEX.md)
