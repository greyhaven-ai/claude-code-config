# TanStack Router Patterns

Complete examples for file-based routing, layouts, and navigation.

## File-Based Routing Structure

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

## Root Layout (__root.tsx)

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

## Route Layouts (_layout.tsx)

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

## Page Routes with Loaders

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

## Dynamic Routes ($param.tsx)

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

## Navigation

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

## Key Patterns

### Underscore Prefix for Groups
- `_authenticated/` - Route group (doesn't add to URL)
- `_layout.tsx` - Layout wrapper for group

### beforeLoad vs loader
- `beforeLoad` - Auth checks, redirects
- `loader` - Data fetching

### Type Safety
- Route params are type-safe
- Loader data is type-safe
- Navigation is type-safe
