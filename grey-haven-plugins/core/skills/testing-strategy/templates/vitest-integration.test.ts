// tests/integration/FEATURE-flow.test.ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { db } from "~/lib/server/db";
import { users } from "~/lib/server/db/schema";
import { eq } from "drizzle-orm";

describe("Feature Integration Tests", () => {
  const testTenantId = "550e8400-e29b-41d4-a716-446655440000";

  beforeEach(async () => {
    // Setup test data
    await db.delete(users).where(eq(users.tenant_id, testTenantId));
  });

  afterEach(async () => {
    // Cleanup test data
    await db.delete(users).where(eq(users.tenant_id, testTenantId));
  });

  it("completes full workflow successfully", async () => {
    // 1. Create resource
    const [created] = await db
      .insert(users)
      .values({
        tenant_id: testTenantId,
        email_address: "test@example.com",
        name: "Test User",
      })
      .returning();

    expect(created).toBeDefined();
    expect(created.email_address).toBe("test@example.com");

    // 2. Retrieve resource
    const [retrieved] = await db
      .select()
      .from(users)
      .where(eq(users.id, created.id))
      .where(eq(users.tenant_id, testTenantId));

    expect(retrieved).toBeDefined();
    expect(retrieved.id).toBe(created.id);

    // 3. Update resource
    const [updated] = await db
      .update(users)
      .set({ name: "Updated Name" })
      .where(eq(users.id, created.id))
      .returning();

    expect(updated.name).toBe("Updated Name");

    // 4. Delete resource
    await db.delete(users).where(eq(users.id, created.id));

    // 5. Verify deletion
    const [deleted] = await db
      .select()
      .from(users)
      .where(eq(users.id, created.id));

    expect(deleted).toBeUndefined();
  });

  it("enforces tenant isolation", async () => {
    const differentTenantId = "00000000-0000-0000-0000-000000000000";

    // Create user in tenant 1
    const [user] = await db
      .insert(users)
      .values({
        tenant_id: testTenantId,
        email_address: "tenant1@example.com",
        name: "Tenant 1 User",
      })
      .returning();

    // Attempt to access with different tenant_id
    const [result] = await db
      .select()
      .from(users)
      .where(eq(users.id, user.id))
      .where(eq(users.tenant_id, differentTenantId));

    expect(result).toBeUndefined();
  });
});
