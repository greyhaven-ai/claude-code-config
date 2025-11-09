# Drizzle Schema Examples

**Complete TypeScript/Drizzle ORM schema patterns.**

## Basic Table with Multi-Tenant

```typescript
// db/schema/users.ts
import { pgTable, uuid, text, timestamp, boolean, index } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  // Primary key
  id: uuid("id").primaryKey().defaultRandom(),
  
  // Timestamps (required on all tables)
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
  
  // Multi-tenant (required on all tables)
  tenant_id: uuid("tenant_id").notNull(),
  
  // User fields
  email_address: text("email_address").notNull().unique(),
  full_name: text("full_name").notNull(),
  hashed_password: text("hashed_password").notNull(),
  is_active: boolean("is_active").default(true).notNull(),
  is_verified: boolean("is_verified").default(false).notNull(),
  last_login_at: timestamp("last_login_at"),
  
  // Soft delete
  deleted_at: timestamp("deleted_at"),
});

// Indexes
export const usersIndex = index("users_tenant_id_idx").on(users.tenant_id);
export const usersEmailIndex = index("users_email_idx").on(users.email_address);
```

## Reusable Timestamp Pattern

```typescript
// db/schema/base.ts
export const baseTimestamps = {
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
};

// Use in tables
export const teams = pgTable("teams", {
  id: uuid("id").primaryKey().defaultRandom(),
  ...baseTimestamps,
  tenant_id: uuid("tenant_id").notNull(),
  name: text("name").notNull(),
});
```

## One-to-Many Relationships

```typescript
// db/schema/posts.ts
import { relations } from "drizzle-orm";

export const posts = pgTable("posts", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(),
  
  // Foreign key to users
  author_id: uuid("author_id").notNull(),
  
  title: text("title").notNull(),
  content: text("content").notNull(),
  is_published: boolean("is_published").default(false).notNull(),
});

// Define relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),  // User has many posts
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.author_id], references: [users.id] }),
}));
```

**See [../templates/drizzle-table.ts](../templates/drizzle-table.ts) for complete template.**
