# TanStack Start Server Functions

Complete examples for creating and using server functions.

## Creating Server Functions

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

## Using Server Functions in Components

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

## Server Functions with Auth Context

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

## Multi-Tenant Server Functions

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

## RLS with Server Functions

```typescript
// Server function uses RLS-enabled database connection
export const getUsers = createServerFn("GET", async () => {
  // Uses authenticated database connection with RLS
  // tenant_id automatically filtered by RLS policies
  return await db.query.users.findMany();
});
```

## Key Patterns

### HTTP Methods
- **GET**: Read operations (automatic caching)
- **POST**: Create operations
- **PUT**: Update operations
- **DELETE**: Delete operations

### Multi-Tenant Isolation
Always include `tenant_id` parameter:
```typescript
export const someFunction = createServerFn("GET", async (
  param: string,
  tenantId: string // REQUIRED
) => {
  // Filter by tenant_id
});
```

### Error Handling
```typescript
export const getUser = createServerFn("GET", async (userId: string) => {
  const user = await db.query.users.findFirst({
    where: eq(users.id, userId),
  });

  if (!user) {
    throw new Error("User not found"); // Automatically returns 500
  }

  return user;
});
```

### Type Safety
Server functions are fully type-safe:
```typescript
// Server function
export const updateUser = createServerFn("POST", async (
  userId: string,
  data: UserUpdate // Type-safe parameter
): Promise<User> => { // Type-safe return
  // ...
});

// Client usage (types inferred)
const mutation = useMutation({
  mutationFn: (data: UserUpdate) => updateUser(userId, data),
  // TypeScript knows the return type is Promise<User>
});
```
