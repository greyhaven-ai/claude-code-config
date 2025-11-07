# TanStack Query Patterns

Complete examples for queries, mutations, and infinite queries.

## Query Basics

```typescript
import { useQuery } from "@tanstack/react-query";
import { getUserById } from "~/lib/server/functions/users";

function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ["user", userId], // Array key for cache
    queryFn: () => getUserById(userId),
    staleTime: 60000, // Grey Haven default: 1 minute
    // Data is "fresh" for 60 seconds, no refetch during this time
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;

  return <div>{user.name}</div>;
}
```

## Query Key Patterns

Use consistent query key structure:

```typescript
// ✅ Good query keys (specific to general)
queryKey: ["user", userId]                    // Single user
queryKey: ["users", { tenantId, page: 1 }]   // List with filters
queryKey: ["organizations", orgId, "teams"]  // Nested resource

// ❌ Bad query keys (inconsistent, not cacheable)
queryKey: [userId]                            // Missing resource type
queryKey: ["getUser", userId]                // Don't include function name
queryKey: [{ id: userId, type: "user" }]     // Object first is confusing
```

## Mutations with Optimistic Updates

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateUser } from "~/lib/server/functions/users";

function EditUserForm({ user }: { user: User }) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (data: UserUpdate) => updateUser(user.id, data),
    // Optimistic update (immediate UI feedback)
    onMutate: async (newData) => {
      // Cancel ongoing queries
      await queryClient.cancelQueries({ queryKey: ["user", user.id] });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(["user", user.id]);

      // Optimistically update cache
      queryClient.setQueryData(["user", user.id], (old: User) => ({
        ...old,
        ...newData,
      }));

      return { previousUser };
    },
    // On error, rollback
    onError: (err, newData, context) => {
      queryClient.setQueryData(["user", user.id], context.previousUser);
    },
    // Always refetch after mutation
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["user", user.id] });
    },
  });

  const handleSubmit = (data: UserUpdate) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      handleSubmit({ name: "Updated Name" });
    }}>
      <button disabled={mutation.isPending}>
        {mutation.isPending ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

## Infinite Queries (Pagination)

```typescript
import { useInfiniteQuery } from "@tanstack/react-query";
import { listUsers } from "~/lib/server/functions/users";

function UsersList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ["users"],
    queryFn: ({ pageParam = 0 }) => listUsers({
      limit: 50,
      offset: pageParam,
    }),
    getNextPageParam: (lastPage, allPages) => {
      // Return next offset or undefined if no more pages
      return lastPage.length === 50 ? allPages.length * 50 : undefined;
    },
    initialPageParam: 0,
    staleTime: 60000,
  });

  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.map((user) => (
            <UserCard key={user.id} user={user} />
          ))}
        </div>
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? "Loading more..."
          : hasNextPage
          ? "Load More"
          : "No more users"}
      </button>
    </div>
  );
}
```

## Prefetching (Performance Optimization)

```typescript
import { useQueryClient } from "@tanstack/react-query";
import { getUserById } from "~/lib/server/functions/users";

function UsersList({ users }: { users: User[] }) {
  const queryClient = useQueryClient();

  // Prefetch user details on hover
  const handleMouseEnter = (userId: string) => {
    queryClient.prefetchQuery({
      queryKey: ["user", userId],
      queryFn: () => getUserById(userId),
      staleTime: 60000,
    });
  };

  return (
    <div>
      {users.map((user) => (
        <Link
          key={user.id}
          to="/users/$userId"
          params={{ userId: user.id }}
          onMouseEnter={() => handleMouseEnter(user.id)}
        >
          {user.name}
        </Link>
      ))}
    </div>
  );
}
```

## Query Error Handling

```typescript
import { useQuery } from "@tanstack/react-query";
import { Alert } from "~/lib/components/ui/alert";

function DataComponent() {
  const { data, error, isLoading } = useQuery({
    queryKey: ["data"],
    queryFn: () => fetchData(),
    retry: 1, // Retry once on failure
    staleTime: 60000,
  });

  if (isLoading) return <LoadingSpinner />;

  if (error) {
    return (
      <Alert variant="destructive">
        <h3>Error loading data</h3>
        <p>{error.message}</p>
      </Alert>
    );
  }

  return <DataDisplay data={data} />;
}
```

## Key Patterns

### Query States
- `isLoading` - First time loading
- `isFetching` - Background refetch
- `isPending` - No cached data yet
- `isError` - Query failed
- `isSuccess` - Query succeeded

### Mutation States
- `isPending` - Mutation in progress
- `isSuccess` - Mutation succeeded
- `isError` - Mutation failed

### Cache Invalidation
```typescript
// Invalidate all user queries
queryClient.invalidateQueries({ queryKey: ["users"] });

// Invalidate specific user
queryClient.invalidateQueries({ queryKey: ["user", userId] });

// Refetch immediately
queryClient.invalidateQueries({
  queryKey: ["users"],
  refetchType: "active"
});
```
