# Multi-Tenant Patterns with TanStack

Multi-tenant isolation patterns for TanStack Start applications.

## Server Function Pattern

**ALWAYS include tenant_id parameter:**

```typescript
// ✅ CORRECT
export const getUsers = createServerFn("GET", async (tenantId: string) => {
  return await db.query.users.findMany({
    where: eq(users.tenant_id, tenantId),
  });
});

// ❌ WRONG - Missing tenant_id
export const getUsers = createServerFn("GET", async () => {
  return await db.query.users.findMany();
});
```

## Query Key Pattern

Include tenant_id in query keys:

```typescript
// ✅ CORRECT
const { data } = useQuery({
  queryKey: ["users", tenantId],
  queryFn: () => getUsers(tenantId),
});

// ❌ WRONG - Missing tenant_id in key
const { data } = useQuery({
  queryKey: ["users"],
  queryFn: () => getUsers(tenantId),
});
```

## Tenant Context Hook

```typescript
// src/lib/hooks/use-tenant.ts
import { useQuery } from "@tanstack/react-query";
import { getAuthenticatedUser } from "~/lib/server/functions/auth";

export function useTenant() {
  const { data: authData } = useQuery({
    queryKey: ["auth", "current-user"],
    queryFn: () => getAuthenticatedUser(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  return {
    tenantId: authData?.tenantId,
    user: authData?.user,
  };
}
```

## Usage in Components

```typescript
function UsersList() {
  const { tenantId } = useTenant();

  const { data: users } = useQuery({
    queryKey: ["users", tenantId],
    queryFn: () => getUsers(tenantId!),
    enabled: !!tenantId, // Only run when tenantId is available
  });

  return <div>...</div>;
}
```

## Row Level Security (RLS)

With RLS, tenant_id filtering is automatic:

```typescript
// Server function with RLS-enabled connection
export const getUsers = createServerFn("GET", async () => {
  // Uses authenticated database connection
  // RLS policies automatically filter by tenant_id
  return await db.query.users.findMany();
});
```

## Best Practices

1. **Always include tenant_id**: In server functions and query keys
2. **Use tenant context**: Create `useTenant()` hook for consistency
3. **Enable guards**: Use `enabled: !!tenantId` for queries
4. **RLS when possible**: Prefer RLS over manual filtering
5. **Test isolation**: Verify tenant isolation in tests
