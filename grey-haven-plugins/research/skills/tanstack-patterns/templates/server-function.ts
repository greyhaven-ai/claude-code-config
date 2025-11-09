// Grey Haven Studio - Server Function Template
// Copy this template for creating server functions

import { createServerFn } from "@tanstack/start";
import { db } from "~/lib/server/db";
// TODO: Import your database schema
// import { resources } from "~/lib/server/schema/resources";
import { eq, and } from "drizzle-orm";

// GET server function (for fetching data)
// TODO: Update function name and return type
export const getResource = createServerFn("GET", async (
  resourceId: string,
  tenantId: string // ALWAYS include tenant_id!
) => {
  // TODO: Replace with your query
  const resource = await db.query.resources.findFirst({
    where: and(
      eq(resources.id, resourceId),
      eq(resources.tenant_id, tenantId) // Multi-tenant isolation!
    ),
  });

  if (!resource) {
    throw new Error("Resource not found");
  }

  return resource;
});

// POST server function (for creating data)
// TODO: Update function name and parameters
export const createResource = createServerFn("POST", async (
  data: { name: string; description?: string },
  tenantId: string // ALWAYS include tenant_id!
) => {
  // TODO: Replace with your insert
  const resource = await db.insert(resources).values({
    ...data,
    tenant_id: tenantId, // Include tenant_id in insert!
  }).returning();

  return resource[0];
});

// DELETE server function (for deleting data)
// TODO: Update function name
export const deleteResource = createServerFn("DELETE", async (
  resourceId: string,
  tenantId: string // ALWAYS include tenant_id!
) => {
  // TODO: Replace with your delete
  await db.delete(resources).where(
    and(
      eq(resources.id, resourceId),
      eq(resources.tenant_id, tenantId) // Ensure tenant isolation!
    )
  );

  return { success: true };
});
