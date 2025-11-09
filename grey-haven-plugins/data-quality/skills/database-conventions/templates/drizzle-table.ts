// Grey Haven Studio - Drizzle Table Template
// Copy this template for new database tables

import { pgTable, uuid, text, timestamp, boolean, index } from "drizzle-orm/pg-core";

// TODO: Update table name
export const resources = pgTable("resources", {
  // Primary key
  id: uuid("id").primaryKey().defaultRandom(),
  
  // Timestamps (REQUIRED on all tables)
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
  
  // Multi-tenant (REQUIRED on all tables)
  tenant_id: uuid("tenant_id").notNull(),
  
  // TODO: Add your fields here (use snake_case!)
  name: text("name").notNull(),
  description: text("description"),
  is_active: boolean("is_active").default(true).notNull(),
  
  // Soft delete (optional but recommended)
  deleted_at: timestamp("deleted_at"),
});

// Indexes (REQUIRED for tenant_id)
export const resourcesIndex = index("resources_tenant_id_idx").on(resources.tenant_id);
