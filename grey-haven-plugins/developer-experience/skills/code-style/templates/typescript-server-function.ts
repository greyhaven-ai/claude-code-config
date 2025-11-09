// Example TanStack Start Server Function Template
// Copy and adapt this for new Grey Haven server functions

import { createServerFn } from "@tanstack/start";
import { db } from "~/lib/server/db";
import { users } from "~/lib/server/schema/users";
import { eq } from "drizzle-orm";
import { z } from "zod";

// 1. Define input schema with Zod
const getUserInputSchema = z.object({
  userId: z.string().uuid(),
  tenantId: z.string(), // Always include tenant_id for multi-tenant isolation
});

// 2. Define output type
interface UserOutput {
  id: string;
  name: string;
  email: string;
  created_at: Date;
  tenant_id: string;
}

// 3. Create server function
export const getUser = createServerFn("GET", async (input: unknown): Promise<UserOutput> => {
  // Validate input
  const { userId, tenantId } = getUserInputSchema.parse(input);

  // Query database with tenant isolation
  const user = await db.query.users.findFirst({
    where: eq(users.id, userId) && eq(users.tenant_id, tenantId), // Tenant filtering!
  });

  if (!user) {
    throw new Error("User not found");
  }

  // Return typed result
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    created_at: user.created_at,
    tenant_id: user.tenant_id,
  };
});

// 4. Mutation example
const updateUserInputSchema = z.object({
  userId: z.string().uuid(),
  tenantId: z.string(),
  name: z.string().min(1),
  email: z.string().email(),
});

export const updateUser = createServerFn(
  "POST",
  async (input: unknown): Promise<UserOutput> => {
    // Validate input
    const { userId, tenantId, name, email } = updateUserInputSchema.parse(input);

    // Update with tenant isolation
    const [updatedUser] = await db
      .update(users)
      .set({ name, email, updated_at: new Date() })
      .where(eq(users.id, userId) && eq(users.tenant_id, tenantId)) // Tenant filtering!
      .returning();

    if (!updatedUser) {
      throw new Error("User not found or update failed");
    }

    return {
      id: updatedUser.id,
      name: updatedUser.name,
      email: updatedUser.email,
      created_at: updatedUser.created_at,
      tenant_id: updatedUser.tenant_id,
    };
  },
);

// 5. Usage in client components
// import { useQuery } from "@tanstack/react-query";
// import { getUser } from "~/lib/server/functions/users";
//
// const { data: user } = useQuery({
//   queryKey: ["user", userId],
//   queryFn: () => getUser({ userId, tenantId }),
//   staleTime: 60000,
// });
