# Common Testing Patterns

Frequently used patterns for testing loading states, errors, infinite queries, and prefetching.

## Testing Loading States

### Skeleton Loader

```typescript
// src/components/UserListSkeleton.tsx
export function UserListSkeleton() {
  return (
    <div data-testid="skeleton">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="skeleton-item">
          <div className="skeleton-avatar" />
          <div className="skeleton-text" />
        </div>
      ))}
    </div>
  );
}

// src/components/UserList.tsx
export function UserList() {
  const { data: users, isLoading } = useUsers();

  if (isLoading) {
    return <UserListSkeleton />;
  }

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Test Suite

```typescript
// src/components/UserList.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import { renderWithQuery } from '../test/test-utils';
import { UserList } from './UserList';

describe('UserList', () => {
  it('shows skeleton loader while loading', () => {
    renderWithQuery(<UserList />);

    expect(screen.getByTestId('skeleton')).toBeInTheDocument();
    expect(screen.getAllByClassName('skeleton-item')).toHaveLength(3);
  });

  it('hides skeleton after data loads', async () => {
    renderWithQuery(<UserList />);

    // Wait for data to load
    await screen.findByText('Alice');

    expect(screen.queryByTestId('skeleton')).not.toBeInTheDocument();
  });
});
```

## Testing Error States

### Error Component

```typescript
// src/components/ErrorMessage.tsx
interface ErrorMessageProps {
  error: Error;
  onRetry?: () => void;
}

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      {onRetry && <button onClick={onRetry}>Try Again</button>}
    </div>
  );
}

// src/components/UserList.tsx
export function UserList() {
  const { data: users, isLoading, error, refetch } = useUsers();

  if (error) {
    return <ErrorMessage error={error} onRetry={() => refetch()} />;
  }

  // ...
}
```

### Test Suite

```typescript
// src/components/UserList.test.tsx
import { server } from '../test/msw/server';
import { http, HttpResponse } from 'msw';

describe('UserList', () => {
  it('shows error message on fetch failure', async () => {
    server.use(
      http.get('/api/users', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    renderWithQuery(<UserList />);

    expect(await screen.findByRole('alert')).toHaveTextContent('Something went wrong');
  });

  it('retries on error retry button click', async () => {
    const user = userEvent.setup();

    server.use(
      http.get('/api/users', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    renderWithQuery(<UserList />);

    await screen.findByRole('alert');

    // Fix the error
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json([{ id: '1', name: 'Alice' }]);
      })
    );

    await user.click(screen.getByRole('button', { name: 'Try Again' }));

    expect(await screen.findByText('Alice')).toBeInTheDocument();
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });
});
```

## Testing Infinite Queries

### Infinite Query Component

```typescript
// src/hooks/useInfiniteUsers.ts
import { useInfiniteQuery } from '@tanstack/react-query';

export function useInfiniteUsers() {
  return useInfiniteQuery({
    queryKey: ['users', 'infinite'],
    queryFn: async ({ pageParam = 0 }) => {
      const response = await fetch(`/api/users?page=${pageParam}&limit=10`);
      return response.json();
    },
    getNextPageParam: (lastPage, pages) => {
      return lastPage.hasMore ? pages.length : undefined;
    },
    initialPageParam: 0,
  });
}

// src/components/InfiniteUserList.tsx
export function InfiniteUserList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteUsers();

  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.users.map((user) => (
            <div key={user.id}>{user.name}</div>
          ))}
        </div>
      ))}

      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

### Test Suite

```typescript
// src/components/InfiniteUserList.test.tsx
import { server } from '../test/msw/server';
import { http, HttpResponse } from 'msw';

beforeAll(() => {
  const mockPages = [
    { users: [{ id: '1', name: 'Alice' }, { id: '2', name: 'Bob' }], hasMore: true },
    { users: [{ id: '3', name: 'Charlie' }, { id: '4', name: 'Diana' }], hasMore: true },
    { users: [{ id: '5', name: 'Eve' }], hasMore: false },
  ];

  server.use(
    http.get('/api/users', ({ request }) => {
      const url = new URL(request.url);
      const page = parseInt(url.searchParams.get('page') || '0');
      return HttpResponse.json(mockPages[page] || { users: [], hasMore: false });
    })
  );
});

describe('InfiniteUserList', () => {
  it('loads first page initially', async () => {
    renderWithQuery(<InfiniteUserList />);

    expect(await screen.findByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });

  it('loads next page on load more click', async () => {
    const user = userEvent.setup();
    renderWithQuery(<InfiniteUserList />);

    await screen.findByText('Alice');

    await user.click(screen.getByRole('button', { name: 'Load More' }));

    expect(await screen.findByText('Charlie')).toBeInTheDocument();
    expect(screen.getByText('Diana')).toBeInTheDocument();
  });

  it('hides load more button when no more pages', async () => {
    const user = userEvent.setup();
    renderWithQuery(<InfiniteUserList />);

    await screen.findByText('Alice');

    // Load page 2
    await user.click(screen.getByRole('button', { name: 'Load More' }));
    await screen.findByText('Charlie');

    // Load page 3 (last page)
    await user.click(screen.getByRole('button', { name: 'Load More' }));
    await screen.findByText('Eve');

    expect(screen.queryByRole('button', { name: 'Load More' })).not.toBeInTheDocument();
  });
});
```

## Testing Intersection Observer (Infinite Scroll)

### Auto-loading Infinite List

```typescript
// src/components/AutoLoadingList.tsx
import { useRef, useEffect } from 'react';

export function AutoLoadingList() {
  const { data, fetchNextPage, hasNextPage } = useInfiniteUsers();
  const observerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasNextPage) {
        fetchNextPage();
      }
    });

    if (observerRef.current) {
      observer.observe(observerRef.current);
    }

    return () => observer.disconnect();
  }, [fetchNextPage, hasNextPage]);

  return (
    <div>
      {data?.pages.map((page) =>
        page.users.map((user) => <div key={user.id}>{user.name}</div>)
      )}
      <div ref={observerRef} data-testid="load-more-trigger" />
    </div>
  );
}
```

### Test Suite

```typescript
// src/components/AutoLoadingList.test.tsx
describe('AutoLoadingList', () => {
  it('loads next page when scrolling to bottom', async () => {
    renderWithQuery(<AutoLoadingList />);

    await screen.findByText('Alice');

    // Simulate intersection observer trigger
    const trigger = screen.getByTestId('load-more-trigger');
    const observer = (window as any).IntersectionObserver.mock.calls[0][0];

    // Trigger intersection
    observer([{ isIntersecting: true, target: trigger }]);

    // Wait for next page
    expect(await screen.findByText('Charlie')).toBeInTheDocument();
  });
});
```

## Testing Prefetching

### Hover Prefetch

```typescript
// src/components/UserCard.tsx
import { useQueryClient } from '@tanstack/react-query';

export function UserCard({ userId, name }: { userId: string; name: string }) {
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    // Prefetch user details on hover
    queryClient.prefetchQuery({
      queryKey: ['user', userId],
      queryFn: () => fetch(`/api/users/${userId}`).then((r) => r.json()),
    });
  };

  return (
    <Link to={`/users/${userId}`} onMouseEnter={handleMouseEnter}>
      {name}
    </Link>
  );
}
```

### Test Suite

```typescript
// src/components/UserCard.test.tsx
describe('UserCard', () => {
  it('prefetches user data on hover', async () => {
    const user = userEvent.setup();
    const queryClient = createTestQueryClient();
    const prefetchSpy = vi.spyOn(queryClient, 'prefetchQuery');

    renderWithQuery(<UserCard userId="123" name="Alice" />, { queryClient });

    const link = screen.getByRole('link', { name: 'Alice' });
    await user.hover(link);

    expect(prefetchSpy).toHaveBeenCalledWith({
      queryKey: ['user', '123'],
      queryFn: expect.any(Function),
    });
  });

  it('caches prefetched data', async () => {
    const user = userEvent.setup();
    const queryClient = createTestQueryClient();

    renderWithQuery(<UserCard userId="123" name="Alice" />, { queryClient });

    const link = screen.getByRole('link', { name: 'Alice' });
    await user.hover(link);

    // Wait for prefetch to complete
    await waitFor(() => {
      const cachedData = queryClient.getQueryData(['user', '123']);
      expect(cachedData).toBeDefined();
    });
  });
});
```

## Testing Optimistic Updates

### Optimistic Delete

```typescript
// src/hooks/useDeleteUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useDeleteUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userId: string) => {
      const response = await fetch(`/api/users/${userId}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Delete failed');
    },
    onMutate: async (userId) => {
      // Cancel outgoing queries
      await queryClient.cancelQueries({ queryKey: ['users'] });

      // Snapshot previous value
      const previousUsers = queryClient.getQueryData(['users']);

      // Optimistically remove user
      queryClient.setQueryData(['users'], (old: any[]) =>
        old.filter((user) => user.id !== userId)
      );

      return { previousUsers };
    },
    onError: (_error, _userId, context) => {
      // Rollback on error
      if (context?.previousUsers) {
        queryClient.setQueryData(['users'], context.previousUsers);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Test Suite

```typescript
// src/hooks/useDeleteUser.test.tsx
describe('useDeleteUser', () => {
  it('removes user optimistically', async () => {
    const queryClient = createTestQueryClient();
    queryClient.setQueryData(['users'], [
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ]);

    const { result } = renderHookWithQuery(() => useDeleteUser(), { queryClient });

    result.current.mutate('1');

    // Immediately check optimistic update
    const cachedUsers = queryClient.getQueryData(['users']);
    expect(cachedUsers).toEqual([{ id: '2', name: 'Bob' }]);
  });

  it('rolls back on error', async () => {
    server.use(
      http.delete('/api/users/:id', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    const queryClient = createTestQueryClient();
    const originalUsers = [
      { id: '1', name: 'Alice' },
      { id: '2', name: 'Bob' },
    ];
    queryClient.setQueryData(['users'], originalUsers);

    const { result } = renderHookWithQuery(() => useDeleteUser(), { queryClient });

    result.current.mutate('1');

    await waitFor(() => expect(result.current.isError).toBe(true));

    // Verify rollback
    const cachedUsers = queryClient.getQueryData(['users']);
    expect(cachedUsers).toEqual(originalUsers);
  });
});
```

## Key Takeaways

1. **Loading States**: Always test skeleton loaders and spinners
2. **Error Handling**: Test error display and retry functionality
3. **Infinite Queries**: Test pagination, load more, and end of list
4. **Intersection Observer**: Mock IntersectionObserver for auto-loading
5. **Prefetching**: Test hover prefetch and cache population
6. **Optimistic Updates**: Test immediate UI updates and rollback on error

---

**Previous**: [Server Components](server-components-testing.md) | **Index**: [Reference Index](INDEX.md)
