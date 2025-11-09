# TanStack Query Caching Strategy

Detailed caching patterns for Grey Haven projects.

## Grey Haven staleTime Standards

```typescript
const STALE_TIMES = {
  auth: 5 * 60 * 1000,        // 5 minutes (auth data)
  user: 1 * 60 * 1000,        // 1 minute (user profiles)
  list: 1 * 60 * 1000,        // 1 minute (lists)
  static: 10 * 60 * 1000,     // 10 minutes (static/config data)
  realtime: 0,                // 0 (always refetch, e.g., notifications)
};
```

## Cache Behavior

### Fresh vs Stale

```typescript
// Data is "fresh" for staleTime duration
const { data } = useQuery({
  queryKey: ["user", userId],
  queryFn: () => getUserById(userId),
  staleTime: 60000, // Fresh for 60 seconds
});

// During "fresh" period:
// - No background refetch
// - Instant return from cache
// - New component mounts get cached data immediately

// After "stale" period:
// - Background refetch on mount
// - Cached data shown while refetching
// - UI updates when new data arrives
```

## Cache Invalidation

```typescript
import { useQueryClient } from "@tanstack/react-query";

const queryClient = useQueryClient();

// Invalidate all user queries
queryClient.invalidateQueries({ queryKey: ["users"] });

// Invalidate specific user
queryClient.invalidateQueries({ queryKey: ["user", userId] });

// Invalidate and refetch immediately
queryClient.invalidateQueries({
  queryKey: ["users"],
  refetchType: "active" // Only refetch active queries
});
```

## Manual Cache Updates

```typescript
// Update cache directly (optimistic update)
queryClient.setQueryData(["user", userId], (old: User) => ({
  ...old,
  name: "New Name"
}));

// Get cached data
const cachedUser = queryClient.getQueryData<User>(["user", userId]);
```

## Cache Persistence

TanStack Query cache is in-memory only. For persistence:

```typescript
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { createSyncStoragePersister } from "@tanstack/query-sync-storage-persister";

const persister = createSyncStoragePersister({
  storage: window.localStorage,
});

persistQueryClient({
  queryClient,
  persister,
  maxAge: 1000 * 60 * 60 * 24, // 24 hours
});
```

## Best Practices

1. **Use staleTime**: Always set appropriate staleTime
2. **Invalidate after mutations**: Use `onSuccess` to invalidate
3. **Specific keys**: Use specific query keys for targeted invalidation
4. **Prefetch**: Prefetch data on hover/navigation
5. **Background refetch**: Let queries refetch in background
