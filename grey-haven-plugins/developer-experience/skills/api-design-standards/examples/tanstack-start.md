# TanStack Start Server Functions

**Complete server function examples with Drizzle ORM and tenant isolation.**

See [../templates/tanstack-server-function.ts](../templates/tanstack-server-function.ts) for full template.

## Complete CRUD Server Functions

```typescript
// app/routes/api/users.ts
import { createServerFn } from "@tanstack/start";
import { z } from "zod";
import { db } from "~/utils/db.server";
import { usersTable } from "~/db/schema";
import { getAuthUser } from "~/utils/auth.server";
import { eq, and, like, count, desc } from "drizzle-orm";
import { hashPassword } from "~/utils/password.server";

// Validation schemas
const createUserSchema = z.object({
  email: z.string().email(),
  fullName: z.string().min(1).max(255),
  password: z.string().min(8),
});

const updateUserSchema = z.object({
  email: z.string().email().optional(),
  fullName: z.string().min(1).max(255).optional(),
  isActive: z.boolean().optional(),
});

// List users
export const listUsers = createServerFn({ method: "GET" })
  .validator(z.object({ skip: z.number().min(0).default(0), limit: z.number().min(1).max(100).default(100) }))
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) throw new Error("Unauthorized", { status: 401 });

    const users = await db.select().from(usersTable)
      .where(eq(usersTable.tenantId, authUser.tenantId))
      .orderBy(desc(usersTable.createdAt))
      .limit(data.limit).offset(data.skip);

    const [{ count: total }] = await db.select({ count: count() })
      .from(usersTable).where(eq(usersTable.tenantId, authUser.tenantId));

    return {
      items: users.map(({ hashedPassword, ...user }) => user),
      total, skip: data.skip, limit: data.limit,
      hasMore: data.skip + data.limit < total,
    };
  });

// Create user
export const createUser = createServerFn({ method: "POST" })
  .validator(createUserSchema)
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) throw new Error("Unauthorized", { status: 401 });

    const [user] = await db.insert(usersTable).values({
      ...data, hashedPassword: await hashPassword(data.password),
      tenantId: authUser.tenantId,
    }).returning();

    const { hashedPassword: _, ...userPublic } = user;
    return userPublic;
  });
```

**See also:** [fastapi-crud.md](fastapi-crud.md) for FastAPI examples
