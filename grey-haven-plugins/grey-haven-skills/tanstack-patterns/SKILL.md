---
name: grey-haven-tanstack-patterns
description: Apply Grey Haven's TanStack ecosystem patterns - Router file-based routing, Query data fetching with staleTime, and Start server functions. Use when building React applications with TanStack Start.
---

# Grey Haven TanStack Patterns

Follow Grey Haven Studio's patterns for TanStack Start, Router, and Query in React 19 applications.

## TanStack Stack Overview

Grey Haven uses the complete TanStack ecosystem:
- **TanStack Start**: Full-stack React framework with server functions
- **TanStack Router**: Type-safe file-based routing with loaders
- **TanStack Query**: Server state management with caching
- **TanStack Table** (optional): Data grids and tables
- **TanStack Form** (optional): Type-safe form handling

## TanStack Router Patterns

### File-Based Routing

Routes are defined by file structure in `src/routes/`:

```
src/routes/
├── __root.tsx              # Root layout (wraps all routes)
├── index.tsx               # Homepage (/)
├── _authenticated/         # Protected routes group (underscore prefix)
│   ├── _layout.tsx        # Auth layout wrapper
│   ├── dashboard.tsx      # /dashboard
│   ├── profile.tsx        # /profile
│   └── settings/
│       ├── index.tsx      # /settings
│       └── billing.tsx    # /settings/billing
├── auth/
│   ├── login.tsx          # /auth/login
│   └── signup.tsx         # /auth/signup
└── users/
    ├── index.tsx          # /users
    └── $userId.tsx        # /users/:userId (dynamic param)
```

### Root Layout (__root.tsx)

```typescript
// src/routes/__root.tsx

import { Outlet, createRootRoute } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

// Create QueryClient with Grey Haven defaults
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60000, // 1 minute default stale time
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background">
        <Outlet /> {/* Child routes render here */}
      </div>
      <ReactQueryDevtools initialIsOpen={false} />
      <TanStackRouterDevtools position="bottom-right" />
    </QueryClientProvider>
  );
}
```

### Route Layouts (_layout.tsx)

```typescript
// src/routes/_authenticated/_layout.tsx

import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { Header } from "~/lib/components/layout/Header";
import { Sidebar } from "~/lib/components/layout/Sidebar";
import { getSession } from "~/lib/server/functions/auth";

export const Route = createFileRoute("/_authenticated/_layout")({
  // Loader runs on server for data fetching
  beforeLoad: async ({ context }) => {
    const session = await getSession();

    if (!session) {
      throw redirect({
        to: "/auth/login",
        search: {
          redirect: context.location.href,
        },
      });
    }

    return { session };
  },
  component: AuthenticatedLayout,
});

function AuthenticatedLayout() {
  const { session } = Route.useRouteContext();

  return (
    <div className="flex min-h-screen">
      <Sidebar user={session.user} />
      <div className="flex-1">
        <Header user={session.user} />
        <main className="p-6">
          <Outlet /> {/* Child routes render here */}
        </main>
      </div>
    </div>
  );
}
```

### Page Routes with Loaders

```typescript
// src/routes/_authenticated/dashboard.tsx

import { createFileRoute } from "@tanstack/react-router";
import { getDashboardData } from "~/lib/server/functions/dashboard";
import { DashboardStats } from "~/lib/components/dashboard/DashboardStats";

export const Route = createFileRoute("/_authenticated/dashboard")({
  // Loader fetches data on server before rendering
  loader: async ({ context }) => {
    const tenantId = context.session.tenantId;
    return await getDashboardData(tenantId);
  },
  component: DashboardPage,
});

function DashboardPage() {
  const data = Route.useLoaderData(); // Type-safe loader data

  return (
    <div>
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <DashboardStats data={data} />
    </div>
  );
}
```

### Dynamic Routes ($param.tsx)

```typescript
// src/routes/users/$userId.tsx

import { createFileRoute } from "@tanstack/react-router";
import { getUserById } from "~/lib/server/functions/users";
import { UserProfile } from "~/lib/components/users/UserProfile";

export const Route = createFileRoute("/users/$userId")({
  // Access route params in loader
  loader: async ({ params, context }) => {
    const { userId } = params;
    const tenantId = context.session.tenantId;
    return await getUserById(userId, tenantId);
  },
  component: UserPage,
});

function UserPage() {
  const user = Route.useLoaderData();
  const { userId } = Route.useParams(); // Also available in component

  return (
    <div>
      <h1 className="text-2xl font-bold">{user.name}</h1>
      <UserProfile user={user} />
    </div>
  );
}
```

### Navigation

```typescript
import { Link, useNavigate } from "@tanstack/react-router";

function Navigation() {
  const navigate = useNavigate();

  return (
    <nav>
      {/* Type-safe Link component */}
      <Link to="/" className="...">
        Home
      </Link>

      <Link
        to="/users/$userId"
        params={{ userId: "123" }}
        className="..."
      >
        User Profile
      </Link>

      {/* Programmatic navigation */}
      <button
        onClick={() => {
          navigate({
            to: "/dashboard",
            replace: true, // Replace history entry
          });
        }}
      >
        Go to Dashboard
      </button>
    </nav>
  );
}
```

## TanStack Query Patterns

### Query Basics with Grey Haven Defaults

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

### Query Key Patterns

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

### Mutations with Optimistic Updates

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

### Infinite Queries (Pagination)

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

### Prefetching (Performance Optimization)

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

## TanStack Start Server Functions

### Creating Server Functions

```typescript
// src/lib/server/functions/users.ts

import { createServerFn } from "@tanstack/start";
import { db } from "~/lib/server/db";
import { users } from "~/lib/server/schema/users";
import { eq, and } from "drizzle-orm";

// GET server function (automatic caching)
export const getUserById = createServerFn("GET", async (
  userId: string,
  tenantId: string
) => {
  // Server-side code with database access
  const user = await db.query.users.findFirst({
    where: and(
      eq(users.id, userId),
      eq(users.tenant_id, tenantId) // Multi-tenant isolation!
    ),
  });

  if (!user) {
    throw new Error("User not found");
  }

  return user;
});

// POST server function (mutations)
export const createUser = createServerFn("POST", async (
  data: { name: string; email: string },
  tenantId: string
) => {
  const user = await db.insert(users).values({
    ...data,
    tenant_id: tenantId,
  }).returning();

  return user[0];
});

// DELETE server function
export const deleteUser = createServerFn("DELETE", async (
  userId: string,
  tenantId: string
) => {
  await db.delete(users).where(
    and(
      eq(users.id, userId),
      eq(users.tenant_id, tenantId)
    )
  );

  return { success: true };
});
```

### Using Server Functions in Components

```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getUserById, createUser, deleteUser } from "~/lib/server/functions/users";

function UserManagement({ tenantId }: { tenantId: string }) {
  const queryClient = useQueryClient();

  // Query using server function
  const { data: user } = useQuery({
    queryKey: ["user", "123"],
    queryFn: () => getUserById("123", tenantId),
  });

  // Mutation using server function
  const createMutation = useMutation({
    mutationFn: (data: { name: string; email: string }) =>
      createUser(data, tenantId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (userId: string) => deleteUser(userId, tenantId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  return <div>...</div>;
}
```

### Server Functions with Auth Context

```typescript
// src/lib/server/functions/auth.ts

import { createServerFn } from "@tanstack/start";
import { getSession } from "~/lib/server/auth";

export const getAuthenticatedUser = createServerFn("GET", async () => {
  const session = await getSession();

  if (!session) {
    throw new Error("Not authenticated");
  }

  // Automatically includes tenant_id from session
  return {
    user: session.user,
    tenantId: session.tenantId,
  };
});
```

```typescript
// Using in a component
function ProfilePage() {
  const { data: authData } = useQuery({
    queryKey: ["auth", "current-user"],
    queryFn: () => getAuthenticatedUser(),
    staleTime: 300000, // 5 minutes for auth data
  });

  return <div>Welcome, {authData?.user.name}!</div>;
}
```

## Advanced Patterns

### Dependent Queries

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

### Parallel Queries

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

### Custom Query Hooks

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

### Query Error Handling

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

## Grey Haven Specific Patterns

### Multi-Tenant Query Pattern

```typescript
// ALWAYS include tenant_id in server functions
export const listOrganizations = createServerFn("GET", async (tenantId: string) => {
  return await db.query.organizations.findMany({
    where: eq(organizations.tenant_id, tenantId),
  });
});

// Use in component with tenant context
function OrganizationsList() {
  const { tenantId } = useTenant(); // Custom hook for tenant context

  const { data: orgs } = useQuery({
    queryKey: ["organizations", tenantId],
    queryFn: () => listOrganizations(tenantId),
    staleTime: 60000,
  });

  return <div>...</div>;
}
```

### RLS with TanStack Query

```typescript
// Server function uses RLS-enabled database connection
export const getUsers = createServerFn("GET", async () => {
  // Uses authenticated database connection with RLS
  // tenant_id automatically filtered by RLS policies
  return await db.query.users.findMany();
});
```

### Caching Strategy

Grey Haven uses these staleTime defaults:

```typescript
const STALE_TIMES = {
  auth: 5 * 60 * 1000,        // 5 minutes (auth data)
  user: 1 * 60 * 1000,        // 1 minute (user profiles)
  list: 1 * 60 * 1000,        // 1 minute (lists)
  static: 10 * 60 * 1000,     // 10 minutes (static/config data)
  realtime: 0,                // 0 (always refetch, e.g., notifications)
};

// Example usage
const { data } = useQuery({
  queryKey: ["users"],
  queryFn: () => listUsers(),
  staleTime: STALE_TIMES.list, // 1 minute
});
```

## When to Apply This Skill

Use this skill when:
- Building TanStack Start applications
- Implementing routing with TanStack Router
- Managing server state with TanStack Query
- Creating server functions for data fetching
- Optimizing query performance
- Implementing multi-tenant data access
- Setting up authentication flows
- Building data-heavy React applications

## Template References

These patterns are from Grey Haven's production template:
- **Frontend**: `cvi-template` (TanStack Start + Router + Query + React 19)

## Critical Reminders

1. **staleTime**: Default 60000ms (1 minute) for queries
2. **Query keys**: Specific to general (["user", userId], not [userId])
3. **Server functions**: Always include tenant_id parameter
4. **Multi-tenant**: Filter by tenant_id in all server functions
5. **Loaders**: Use for server-side data fetching before render
6. **Mutations**: Invalidate queries after successful mutation
7. **Prefetching**: Use for performance on hover/navigation
8. **Error handling**: Always handle error state in queries
9. **RLS**: Server functions use RLS-enabled database connection
10. **File-based routing**: Underscore prefix (_) for route groups/layouts
