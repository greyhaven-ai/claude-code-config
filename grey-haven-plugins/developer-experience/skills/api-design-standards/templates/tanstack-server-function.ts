// Grey Haven Studio - TanStack Start Server Function Template
// Copy this template for new TanStack Start server functions

import { createServerFn } from "@tanstack/start";
import { z } from "zod";
import { db } from "~/utils/db.server";
import { resourcesTable } from "~/db/schema";  // TODO: Update import
import { getAuthUser } from "~/utils/auth.server";
import { eq, and, like, count, desc } from "drizzle-orm";

// TODO: Update validation schemas
const createResourceSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().optional(),
});

const updateResourceSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  description: z.string().optional(),
  isActive: z.boolean().optional(),
});

const listResourcesSchema = z.object({
  skip: z.number().min(0).default(0),
  limit: z.number().min(1).max(100).default(100),
  // TODO: Add filter fields
});

// List resources
export const listResources = createServerFn({ method: "GET" })
  .validator(listResourcesSchema)
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) {
      throw new Error("Unauthorized", { status: 401 });
    }

    // Build query with tenant filter
    let query = db
      .select()
      .from(resourcesTable)
      .where(eq(resourcesTable.tenantId, authUser.tenantId));

    // TODO: Apply additional filters

    // Apply pagination
    const resources = await query
      .orderBy(desc(resourcesTable.createdAt))
      .limit(data.limit)
      .offset(data.skip);

    // Get total count
    const [{ count: total }] = await db
      .select({ count: count() })
      .from(resourcesTable)
      .where(eq(resourcesTable.tenantId, authUser.tenantId));

    return {
      items: resources,
      total,
      skip: data.skip,
      limit: data.limit,
      hasMore: data.skip + data.limit < total,
    };
  });

// Get resource by ID
export const getResource = createServerFn({ method: "GET" })
  .validator(z.object({ resourceId: z.string() }))
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) {
      throw new Error("Unauthorized", { status: 401 });
    }

    const [resource] = await db
      .select()
      .from(resourcesTable)
      .where(
        and(
          eq(resourcesTable.id, data.resourceId),
          eq(resourcesTable.tenantId, authUser.tenantId)
        )
      )
      .limit(1);

    if (!resource) {
      throw new Error("Resource not found", { status: 404 });
    }

    return resource;
  });

// Create resource
export const createResource = createServerFn({ method: "POST" })
  .validator(createResourceSchema)
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) {
      throw new Error("Unauthorized", { status: 401 });
    }

    // TODO: Check for duplicates if needed

    // Create resource (tenant_id from auth context)
    const [resource] = await db
      .insert(resourcesTable)
      .values({
        ...data,
        tenantId: authUser.tenantId,
      })
      .returning();

    return resource;
  });

// Update resource
export const updateResource = createServerFn({ method: "PUT" })
  .validator(
    z.object({
      resourceId: z.string(),
      data: updateResourceSchema,
    })
  )
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) {
      throw new Error("Unauthorized", { status: 401 });
    }

    // Verify resource exists and belongs to tenant
    const [existing] = await db
      .select()
      .from(resourcesTable)
      .where(
        and(
          eq(resourcesTable.id, data.resourceId),
          eq(resourcesTable.tenantId, authUser.tenantId)
        )
      )
      .limit(1);

    if (!existing) {
      throw new Error("Resource not found", { status: 404 });
    }

    // Update resource
    const [resource] = await db
      .update(resourcesTable)
      .set({
        ...data.data,
        updatedAt: new Date(),
      })
      .where(eq(resourcesTable.id, data.resourceId))
      .returning();

    return resource;
  });

// Delete resource
export const deleteResource = createServerFn({ method: "DELETE" })
  .validator(z.object({ resourceId: z.string() }))
  .handler(async ({ data, context }) => {
    const authUser = await getAuthUser(context);
    if (!authUser) {
      throw new Error("Unauthorized", { status: 401 });
    }

    // Soft delete by setting deletedAt
    const result = await db
      .update(resourcesTable)
      .set({ deletedAt: new Date() })
      .where(
        and(
          eq(resourcesTable.id, data.resourceId),
          eq(resourcesTable.tenantId, authUser.tenantId)
        )
      )
      .returning();

    if (result.length === 0) {
      throw new Error("Resource not found", { status: 404 });
    }

    return { success: true };
  });
