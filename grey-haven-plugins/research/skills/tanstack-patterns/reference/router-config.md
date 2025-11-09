# TanStack Router Configuration

Router setup and configuration reference.

## File Structure

```
src/routes/
├── __root.tsx           # Root layout (required)
├── index.tsx            # Homepage
├── _layout/            # Route group (underscore prefix)
│   ├── _layout.tsx    # Group layout
│   └── page.tsx       # /page
└── $param.tsx         # Dynamic route
```

## Root Route Setup

```typescript
// src/routes/__root.tsx
import { Outlet, createRootRoute } from "@tanstack/react-router";
import { QueryClientProvider } from "@tanstack/react-query";

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  );
}
```

## Route Naming Conventions

| File | URL | Description |
|------|-----|-------------|
| `index.tsx` | `/` | Homepage |
| `about.tsx` | `/about` | Static route |
| `_layout.tsx` | - | Layout wrapper (no URL) |
| `$userId.tsx` | `/:userId` | Dynamic param |
| `_authenticated/` | - | Route group (no URL) |

## beforeLoad vs loader

- **beforeLoad**: Auth checks, redirects, context setup
- **loader**: Data fetching

```typescript
export const Route = createFileRoute("/_authenticated/_layout")({
  beforeLoad: async () => {
    const session = await getSession();
    if (!session) throw redirect({ to: "/login" });
    return { session };
  },
});

export const Route = createFileRoute("/dashboard")({
  loader: async ({ context }) => {
    return await getDashboardData(context.session.tenantId);
  },
});
```
