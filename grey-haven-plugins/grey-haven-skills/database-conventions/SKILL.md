---
name: grey-haven-database-conventions
description: Apply Grey Haven Studio's database conventions - snake_case fields, multi-tenant architecture with tenant_id and RLS policies, proper indexing, and migration patterns for Drizzle (TypeScript) and SQLModel (Python). Use when designing schemas or writing database code.
---

# Grey Haven Database Conventions

Follow Grey Haven Studio's database standards for both TypeScript (Drizzle ORM) and Python (SQLModel/SQLAlchemy) projects.

## Core Principles

### 1. Field Naming: ALWAYS snake_case

**CRITICAL**: Database column names use snake_case, not camelCase.

```typescript
// ✅ Correct - Drizzle schema (TypeScript)
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(),
  email_address: text("email_address").notNull().unique(),
  is_active: boolean("is_active").default(true).notNull(),
  last_login_at: timestamp("last_login_at"),
});

// ❌ Wrong - Don't use camelCase
export const users = pgTable("users", {
  id: uuid("id").primaryKey(),
  createdAt: timestamp("createdAt"),        // WRONG!
  tenantId: uuid("tenantId"),              // WRONG!
  emailAddress: text("emailAddress"),      // WRONG!
  isActive: boolean("isActive"),           // WRONG!
});
```

```python
# ✅ Correct - SQLModel schema (Python)
class User(SQLModel, table=True):
    """User database model."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    email_address: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    last_login_at: Optional[datetime] = None

# ❌ Wrong - Don't use camelCase
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    createdAt: datetime = Field(default_factory=datetime.utcnow)  # WRONG!
    tenantId: UUID = Field()  # WRONG!
```

### 2. Multi-Tenant Architecture: tenant_id Required

**Every table must include tenant_id for data isolation.**

```typescript
// TypeScript - Drizzle schema with tenant_id
export const organizations = pgTable("organizations", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(), // REQUIRED for all tables
  name: text("name").notNull(),
  slug: text("slug").notNull().unique(),
});

// Add index for tenant_id queries
export const organizationsIndex = index("organizations_tenant_id_idx").on(
  organizations.tenant_id
);
```

```python
# Python - SQLModel with tenant_id
class Organization(SQLModel, table=True):
    """Organization model with tenant isolation."""

    __tablename__ = "organizations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)  # REQUIRED
    name: str = Field(max_length=255)
    slug: str = Field(unique=True, max_length=100)
```

### 3. Row Level Security (RLS) Policies

Enable RLS on all tables with tenant_id for automatic isolation.

```sql
-- Enable RLS on table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users (tenant isolation)
CREATE POLICY "Users can only access their tenant's data"
  ON users
  FOR ALL
  TO authenticated
  USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);

-- Policy for admin role (cross-tenant access)
CREATE POLICY "Admins can access all tenants"
  ON users
  FOR ALL
  TO admin
  USING (true);

-- Policy for anonymous (no access)
CREATE POLICY "Anonymous users have no access"
  ON users
  FOR SELECT
  TO anon
  USING (false);
```

### 4. Standard Timestamp Fields

All tables should have created_at and updated_at.

```typescript
// TypeScript - Drizzle timestamps
export const baseTimestamps = {
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull()
    .$onUpdate(() => new Date()),
};

// Use in table definition
export const teams = pgTable("teams", {
  id: uuid("id").primaryKey().defaultRandom(),
  ...baseTimestamps,
  tenant_id: uuid("tenant_id").notNull(),
  name: text("name").notNull(),
});
```

```python
# Python - SQLModel timestamps with auto-update
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

class Team(TimestampMixin, SQLModel, table=True):
    """Team model with automatic timestamps."""
    __tablename__ = "teams"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    name: str = Field(max_length=255)
```

## Field Naming Patterns

### Boolean Fields

Prefix with `is_`, `has_`, or `can_`:

```typescript
// ✅ Good boolean names
is_active: boolean("is_active").default(true)
is_verified: boolean("is_verified").default(false)
has_access: boolean("has_access").default(false)
can_edit: boolean("can_edit").default(false)

// ❌ Bad boolean names
active: boolean("active")              // Missing 'is_' prefix
verified: boolean("verified")          // Missing 'is_' prefix
```

### Timestamp Fields

Use `_at` suffix for timestamps:

```typescript
// ✅ Good timestamp names
created_at: timestamp("created_at")
updated_at: timestamp("updated_at")
deleted_at: timestamp("deleted_at")      // Soft delete
last_login_at: timestamp("last_login_at")
verified_at: timestamp("verified_at")
expires_at: timestamp("expires_at")

// ❌ Bad timestamp names
created: timestamp("created")            // Missing '_at' suffix
last_login: timestamp("last_login")      // Missing '_at' suffix
```

### Foreign Keys

Use singular form with `_id` suffix:

```typescript
// ✅ Good foreign key names
user_id: uuid("user_id").references(() => users.id)
organization_id: uuid("organization_id").references(() => organizations.id)
parent_id: uuid("parent_id").references(() => categories.id) // Self-reference

// ❌ Bad foreign key names
user: uuid("user")                      // Missing '_id' suffix
users_id: uuid("users_id")              // Should be singular
```

### JSON/JSONB Fields

Use `_data` or descriptive name:

```typescript
// ✅ Good JSON field names
metadata: jsonb("metadata").default({})
settings_data: jsonb("settings_data").default({})
oauth_profile: jsonb("oauth_profile")

// ❌ Bad JSON field names
meta: jsonb("meta")                     // Too generic
json: jsonb("json")                     // Not descriptive
```

## Indexing Strategies

### Required Indexes

1. **Primary keys**: Automatically indexed
2. **Foreign keys**: ALWAYS index for join performance
3. **tenant_id**: ALWAYS index for multi-tenant queries
4. **Unique constraints**: Automatically indexed

```typescript
// TypeScript - Drizzle indexes
import { index, unique } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(),
  email_address: text("email_address").notNull(),
  organization_id: uuid("organization_id"),
});

// Index for tenant isolation queries
export const usersTenantIdx = index("users_tenant_id_idx").on(users.tenant_id);

// Index for foreign key joins
export const usersOrgIdx = index("users_organization_id_idx").on(
  users.organization_id
);

// Composite index for common query pattern
export const usersTenantEmailIdx = index("users_tenant_email_idx").on(
  users.tenant_id,
  users.email_address
);

// Unique constraint (automatically indexed)
export const usersEmailUnique = unique("users_email_unique").on(
  users.email_address
);
```

```python
# Python - SQLModel indexes
from sqlmodel import Field, SQLModel, Index

class User(SQLModel, table=True):
    """User model with proper indexing."""

    __tablename__ = "users"
    __table_args__ = (
        Index("users_tenant_id_idx", "tenant_id"),
        Index("users_organization_id_idx", "organization_id"),
        Index("users_tenant_email_idx", "tenant_id", "email_address"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id")
    email_address: str = Field(unique=True, max_length=255)
    organization_id: Optional[UUID] = Field(foreign_key="organizations.id")
```

### Performance Indexing

```sql
-- Verify index usage with EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT * FROM users
WHERE tenant_id = 'uuid-here'
  AND email_address = 'user@example.com';

-- Should show: Index Scan using users_tenant_email_idx
-- NOT: Seq Scan on users (sequential scan is slow!)
```

## Migration Patterns

### TypeScript - Drizzle Migrations

```typescript
// Example migration: Add tenant_id to existing table
// migrations/0001_add_tenant_id_to_posts.ts

import { sql } from "drizzle-orm";
import { pgTable, uuid } from "drizzle-orm/pg-core";

export async function up(db) {
  // 1. Add column (nullable initially)
  await db.execute(sql`
    ALTER TABLE posts
    ADD COLUMN tenant_id UUID;
  `);

  // 2. Backfill data (important for multi-tenant!)
  await db.execute(sql`
    UPDATE posts
    SET tenant_id = users.tenant_id
    FROM users
    WHERE posts.user_id = users.id;
  `);

  // 3. Make NOT NULL after backfill
  await db.execute(sql`
    ALTER TABLE posts
    ALTER COLUMN tenant_id SET NOT NULL;
  `);

  // 4. Add foreign key constraint
  await db.execute(sql`
    ALTER TABLE posts
    ADD CONSTRAINT posts_tenant_id_fkey
    FOREIGN KEY (tenant_id) REFERENCES tenants(id);
  `);

  // 5. Add index for performance
  await db.execute(sql`
    CREATE INDEX posts_tenant_id_idx ON posts(tenant_id);
  `);

  // 6. Enable RLS
  await db.execute(sql`
    ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
  `);

  // 7. Create RLS policy
  await db.execute(sql`
    CREATE POLICY "Tenant isolation for posts"
      ON posts
      FOR ALL
      TO authenticated
      USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);
  `);
}

export async function down(db) {
  // Reverse migration (important for rollback!)
  await db.execute(sql`DROP POLICY IF EXISTS "Tenant isolation for posts" ON posts;`);
  await db.execute(sql`ALTER TABLE posts DISABLE ROW LEVEL SECURITY;`);
  await db.execute(sql`DROP INDEX IF EXISTS posts_tenant_id_idx;`);
  await db.execute(sql`ALTER TABLE posts DROP CONSTRAINT IF EXISTS posts_tenant_id_fkey;`);
  await db.execute(sql`ALTER TABLE posts DROP COLUMN IF EXISTS tenant_id;`);
}
```

### Python - Alembic Migrations

```python
# migrations/versions/001_add_tenant_id_to_posts.py

"""Add tenant_id to posts table

Revision ID: 001_tenant_posts
Revises:
Create Date: 2025-10-20 12:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '001_tenant_posts'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add tenant_id with proper multi-tenant setup."""
    # 1. Add column (nullable initially)
    op.add_column('posts', sa.Column('tenant_id', UUID(as_uuid=True), nullable=True))

    # 2. Backfill data from users table
    op.execute("""
        UPDATE posts
        SET tenant_id = users.tenant_id
        FROM users
        WHERE posts.user_id = users.id
    """)

    # 3. Make NOT NULL after backfill
    op.alter_column('posts', 'tenant_id', nullable=False)

    # 4. Add foreign key constraint
    op.create_foreign_key(
        'posts_tenant_id_fkey',
        'posts',
        'tenants',
        ['tenant_id'],
        ['id']
    )

    # 5. Add index
    op.create_index('posts_tenant_id_idx', 'posts', ['tenant_id'])

    # 6. Enable RLS
    op.execute('ALTER TABLE posts ENABLE ROW LEVEL SECURITY')

    # 7. Create RLS policy
    op.execute("""
        CREATE POLICY "Tenant isolation for posts"
          ON posts
          FOR ALL
          TO authenticated
          USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid)
    """)


def downgrade() -> None:
    """Reverse tenant_id changes."""
    op.execute('DROP POLICY IF EXISTS "Tenant isolation for posts" ON posts')
    op.execute('ALTER TABLE posts DISABLE ROW LEVEL SECURITY')
    op.drop_index('posts_tenant_id_idx', table_name='posts')
    op.drop_constraint('posts_tenant_id_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'tenant_id')
```

## Query Patterns with Tenant Isolation

### TypeScript - Drizzle Queries

```typescript
import { eq, and } from "drizzle-orm";
import { db } from "~/lib/server/db";

// ✅ Correct - Always filter by tenant_id
export async function getUserById(userId: string, tenantId: string) {
  return await db.query.users.findFirst({
    where: and(
      eq(users.id, userId),
      eq(users.tenant_id, tenantId) // REQUIRED for isolation!
    ),
  });
}

// ✅ Correct - List query with tenant filter
export async function listUsers(tenantId: string, limit = 50, offset = 0) {
  return await db.query.users.findMany({
    where: eq(users.tenant_id, tenantId),
    limit,
    offset,
  });
}

// ❌ Wrong - Missing tenant_id filter (security risk!)
export async function getUserById(userId: string) {
  return await db.query.users.findFirst({
    where: eq(users.id, userId), // Missing tenant_id check!
  });
}
```

### Python - SQLModel/SQLAlchemy Queries

```python
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

# ✅ Correct - Repository pattern with tenant isolation
class UserRepository:
    """User repository with automatic tenant filtering."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID, tenant_id: UUID) -> Optional[User]:
        """Get user by ID with tenant isolation."""
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .where(User.tenant_id == tenant_id)  # REQUIRED!
        )
        return result.scalar_one_or_none()

    async def list(
        self, tenant_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[User]:
        """List users with tenant isolation."""
        result = await self.session.execute(
            select(User)
            .where(User.tenant_id == tenant_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

# ❌ Wrong - Missing tenant_id filtering
async def get_user(session: AsyncSession, user_id: UUID) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.id == user_id)  # Missing tenant check!
    )
    return result.scalar_one_or_none()
```

## Database Connection Roles

Grey Haven uses PostgreSQL with three roles:

### 1. Admin Role (admin)
- Full access to all data
- Used for migrations and system operations
- Bypasses RLS policies

### 2. Authenticated Role (authenticated)
- Normal user queries
- RLS policies enforced
- tenant_id from JWT claims

### 3. Anonymous Role (anon)
- Public read-only access (if needed)
- Heavily restricted by RLS

```typescript
// TypeScript - Database connections by role
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";

// Admin connection (migrations, system ops)
const adminSql = neon(process.env.DATABASE_URL_ADMIN!);
export const adminDb = drizzle(adminSql);

// Authenticated connection (user queries with RLS)
const authenticatedSql = neon(process.env.DATABASE_URL_AUTHENTICATED!);
export const db = drizzle(authenticatedSql);

// Anonymous connection (public access)
const anonSql = neon(process.env.DATABASE_URL_ANON!);
export const anonDb = drizzle(anonSql);
```

```python
# Python - Database connections by role
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Admin engine (migrations, system ops)
admin_engine = create_async_engine(
    settings.DATABASE_URL_ADMIN,
    echo=settings.DEBUG,
)

# Authenticated engine (user queries with RLS)
authenticated_engine = create_async_engine(
    settings.DATABASE_URL_AUTHENTICATED,
    echo=settings.DEBUG,
)

# Session factory for authenticated role
AsyncSessionLocal = sessionmaker(
    authenticated_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

## Common Patterns

### Soft Deletes

```typescript
// Add deleted_at for soft delete pattern
export const posts = pgTable("posts", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  deleted_at: timestamp("deleted_at"), // NULL = not deleted
  tenant_id: uuid("tenant_id").notNull(),
  title: text("title").notNull(),
});

// Query pattern - exclude soft deleted
export async function listPosts(tenantId: string) {
  return await db.query.posts.findMany({
    where: and(
      eq(posts.tenant_id, tenantId),
      isNull(posts.deleted_at) // Only non-deleted posts
    ),
  });
}
```

### Audit Trails

```typescript
// Track who created/updated records
export const posts = pgTable("posts", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  created_by: uuid("created_by").references(() => users.id),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  updated_by: uuid("updated_by").references(() => users.id),
  tenant_id: uuid("tenant_id").notNull(),
});
```

### Enum Types

```typescript
// Use PostgreSQL enums for type safety
import { pgEnum } from "drizzle-orm/pg-core";

export const userRoleEnum = pgEnum("user_role", ["admin", "member", "guest"]);

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  role: userRoleEnum("role").default("member").notNull(),
  tenant_id: uuid("tenant_id").notNull(),
});
```

```python
# Python - Enum types
from enum import Enum

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role: UserRole = Field(default=UserRole.MEMBER, sa_column=Column(SQLEnum(UserRole)))
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
```

## Testing Database Code

### Migration Testing

```bash
# TypeScript - Test migrations up and down
npm run db:generate    # Generate migration from schema changes
npm run db:migrate     # Apply migration
npm run db:studio      # Verify schema in Drizzle Studio
npm run db:rollback    # Test rollback (down migration)
```

```bash
# Python - Test Alembic migrations
source .venv/bin/activate
alembic revision --autogenerate -m "Add tenant_id"
alembic upgrade head           # Apply migration
alembic downgrade -1           # Test rollback
```

### RLS Policy Testing

```sql
-- Test RLS policies with different roles
BEGIN;

-- Set JWT claims for tenant A user
SET LOCAL request.jwt.claims TO '{"tenant_id": "uuid-tenant-a", "role": "authenticated"}';

-- Should return only tenant A data
SELECT * FROM users;

ROLLBACK;

BEGIN;

-- Set JWT claims for tenant B user
SET LOCAL request.jwt.claims TO '{"tenant_id": "uuid-tenant-b", "role": "authenticated"}';

-- Should return only tenant B data (different from above)
SELECT * FROM users;

ROLLBACK;
```

## When to Apply This Skill

Use this skill when:
- Designing new database schemas
- Writing Drizzle or SQLModel models
- Creating database migrations
- Implementing multi-tenant features
- Adding RLS policies
- Optimizing database queries
- Reviewing database code
- Troubleshooting tenant isolation issues

## Template References

These conventions are used in Grey Haven's production templates:
- **Frontend**: `cvi-template` - Drizzle ORM with Neon PostgreSQL
- **Backend**: `cvi-backend-template` - SQLModel with PostgreSQL

## Critical Reminders

1. **Field names**: ALWAYS snake_case (user_id, created_at, tenant_id)
2. **tenant_id**: REQUIRED on every table for multi-tenant isolation
3. **RLS policies**: Enable on all tables with tenant_id
4. **Indexes**: ALWAYS index tenant_id and foreign keys
5. **Timestamps**: Use created_at and updated_at on all tables
6. **Booleans**: Prefix with is_, has_, or can_
7. **Migrations**: Always test up AND down (rollback)
8. **Queries**: ALWAYS filter by tenant_id for isolation
9. **Backfill**: When adding tenant_id, backfill before NOT NULL
10. **EXPLAIN ANALYZE**: Verify indexes are used in production queries
