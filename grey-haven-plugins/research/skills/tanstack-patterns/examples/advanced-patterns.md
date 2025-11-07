# Advanced TanStack Query Patterns

Complete examples for dependent queries, parallel queries, and custom hooks.

## Dependent Queries

```typescript
function UserOrganization({ userId }: { userId: string }) {
  // First query: get user
  const { data: user } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
  });

  // Second query: get organization (depends on user)
  const { data: organization } = useQuery({
    queryKey: ["organization", user?.organization_id],
    queryFn: () => getOrganizationById(user!.organization_id),
    enabled: !!user?.organization_id, // Only run if user exists
  });

  if (!user) return <LoadingSpinner />;

  return (
    <div>
      <h2>{user.name}</h2>
      {organization && <p>Organization: {organization.name}</p>}
    </div>
  );
}
```

## Parallel Queries

```typescript
function Dashboard() {
  // Run multiple queries in parallel
  const userQuery = useQuery({
    queryKey: ["user", "current"],
    queryFn: () => getCurrentUser(),
  });

  const statsQuery = useQuery({
    queryKey: ["stats", "dashboard"],
    queryFn: () => getDashboardStats(),
  });

  const recentQuery = useQuery({
    queryKey: ["recent", "activity"],
    queryFn: () => getRecentActivity(),
  });

  // All queries run simultaneously (parallel fetching)
  const isLoading = userQuery.isLoading || statsQuery.isLoading || recentQuery.isLoading;

  if (isLoading) return <LoadingSpinner />;

  return (
    <div>
      <UserHeader user={userQuery.data} />
      <StatsCards stats={statsQuery.data} />
      <ActivityFeed activity={recentQuery.data} />
    </div>
  );
}
```

## Custom Query Hooks

```typescript
// src/lib/hooks/use-user.ts

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getUserById, updateUser } from "~/lib/server/functions/users";

export function useUser(userId: string) {
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
    staleTime: 60000,
  });

  const updateMutation = useMutation({
    mutationFn: (data: UserUpdate) => updateUser(userId, data),
    onSuccess: (updatedUser) => {
      queryClient.setQueryData(["user", userId], updatedUser);
    },
  });

  return {
    user: query.data,
    isLoading: query.isLoading,
    error: query.error,
    update: updateMutation.mutate,
    isUpdating: updateMutation.isPending,
  };
}
```

```typescript
// Using custom hook
function UserProfile({ userId }: { userId: string }) {
  const { user, isLoading, update, isUpdating } = useUser(userId);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div>
      <h1>{user.name}</h1>
      <button
        onClick={() => update({ name: "New Name" })}
        disabled={isUpdating}
      >
        {isUpdating ? "Updating..." : "Update"}
      </button>
    </div>
  );
}
```

## Query Composition

```typescript
// Base hook for fetching user
function useUserQuery(userId: string) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
    staleTime: 60000,
  });
}

// Composed hook with additional functionality
function useUserWithPermissions(userId: string) {
  const userQuery = useUserQuery(userId);

  const permissionsQuery = useQuery({
    queryKey: ["user", userId, "permissions"],
    queryFn: () => getUserPermissions(userId),
    enabled: !!userQuery.data,
    staleTime: 60000,
  });

  return {
    user: userQuery.data,
    permissions: permissionsQuery.data,
    isLoading: userQuery.isLoading || permissionsQuery.isLoading,
    error: userQuery.error || permissionsQuery.error,
  };
}
```

## Background Refetching

```typescript
function RealtimeNotifications() {
  const { data: notifications } = useQuery({
    queryKey: ["notifications"],
    queryFn: () => getNotifications(),
    staleTime: 0, // Always stale
    refetchInterval: 30000, // Refetch every 30 seconds
    refetchIntervalInBackground: true, // Even when tab is not focused
  });

  return (
    <div>
      {notifications?.map((notif) => (
        <NotificationItem key={notif.id} notification={notif} />
      ))}
    </div>
  );
}
```

## Suspense Mode

```typescript
import { Suspense } from "react";
import { useSuspenseQuery } from "@tanstack/react-query";

function UserProfile({ userId }: { userId: string }) {
  // Suspense mode - no loading state needed
  const { data: user } = useSuspenseQuery({
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
  });

  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

## Placeholders and Initial Data

```typescript
function UserProfile({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const { data: user } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
    // Placeholder data while loading
    placeholderData: () => {
      // Try to find user in list cache
      const users = queryClient.getQueryData<User[]>(["users"]);
      return users?.find(u => u.id === userId);
    },
    staleTime: 60000,
  });

  return <div>{user?.name}</div>;
}
```

## Query Cancellation

```typescript
import { useQuery } from "@tanstack/react-query";

function SearchResults({ query }: { query: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ["search", query],
    queryFn: async ({ signal }) => {
      // Pass AbortSignal to fetch
      const response = await fetch(`/api/search?q=${query}`, { signal });
      return response.json();
    },
    staleTime: 60000,
    // Query automatically cancelled when query key changes
  });

  return <div>...</div>;
}
```

## Key Patterns

### When to Use Custom Hooks
- Reusing query logic across components
- Combining multiple queries
- Adding business logic to queries
- Simplifying component code

### When to Use Dependent Queries
- Second query needs data from first query
- Use `enabled` option to control execution

### When to Use Parallel Queries
- Multiple independent data sources
- No dependencies between queries
- Want to show loading state for all together

### When to Use Suspense
- React 18+ with Suspense boundaries
- Want declarative loading states
- Component tree can suspend

### Performance Tips
- Use `placeholderData` for instant UI feedback
- Use `staleTime` to reduce unnecessary refetches
- Use `refetchInterval` for real-time updates
- Cancel queries when component unmounts (automatic)
