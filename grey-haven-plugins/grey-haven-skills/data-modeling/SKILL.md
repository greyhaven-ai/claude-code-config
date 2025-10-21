---
name: grey-haven-data-modeling
description: Design database schemas for Grey Haven multi-tenant SaaS - SQLModel models, Drizzle schema, multi-tenant isolation with tenant_id and RLS, timestamp fields, foreign keys, indexes, migrations, and relationships. Use when creating database tables.
---

# Grey Haven Data Modeling Standards

Design **database schemas** for Grey Haven Studio's multi-tenant SaaS applications using SQLModel (FastAPI) and Drizzle ORM (TanStack Start) with PostgreSQL and RLS.

## Multi-Tenant Data Model Principles

### Tenant Isolation Strategy
- **tenant_id column**: Every table includes `tenant_id UUID NOT NULL`
- **Foreign key to tenants**: `REFERENCES tenants(id) ON DELETE CASCADE`
- **RLS policies**: Row-level security enforces tenant isolation at database level
- **JWT claims**: Extract tenant_id from JWT for automatic filtering
- **Composite indexes**: Index on `(tenant_id, ...)` for performance

### Core Tenant Tables

#### Tenants Table (Root of Hierarchy)
```python
# app/models/tenant.py (SQLModel - FastAPI)
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Tenant(SQLModel, table=True):
    """Root tenant table - all other tables reference this."""
    __tablename__ = "tenants"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique tenant identifier (UUID)",
    )
    name: str = Field(
        max_length=255,
        description="Tenant organization name",
    )
    slug: str = Field(
        max_length=100,
        unique=True,
        description="URL-friendly tenant identifier",
    )
    is_active: bool = Field(
        default=True,
        description="Tenant subscription status",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Tenant creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )
```

```typescript
// app/db/schema.ts (Drizzle - TanStack Start)
import { pgTable, uuid, varchar, boolean, timestamp } from "drizzle-orm/pg-core";

export const tenantsTable = pgTable("tenants", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: varchar("name", { length: 255 }).notNull(),
  slug: varchar("slug", { length: 100 }).notNull().unique(),
  isActive: boolean("is_active").notNull().default(true),
  createdAt: timestamp("created_at").notNull().defaultNow(),
  updatedAt: timestamp("updated_at").notNull().defaultNow(),
});
```

#### Users Table (With Tenant Isolation)
```python
# app/models/user.py (SQLModel)
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """User model with multi-tenant isolation."""
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
    )
    tenant_id: str = Field(
        foreign_key="tenants.id",
        nullable=False,
        index=True,  # Index for performance
        description="Tenant this user belongs to",
    )
    email: str = Field(
        max_length=255,
        index=True,
        description="User email (unique per tenant)",
    )
    full_name: str = Field(
        max_length=255,
        description="User's full name",
    )
    hashed_password: Optional[str] = Field(
        default=None,
        description="Bcrypt hashed password (null for OAuth users)",
    )
    is_active: bool = Field(
        default=True,
        description="User account status",
    )
    is_superuser: bool = Field(
        default=False,
        description="Admin privileges (cross-tenant access)",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )

    # Relationships
    tenant: Optional["Tenant"] = Relationship(back_populates="users")

    class Config:
        # Composite unique constraint (email unique per tenant)
        table_args = (
            UniqueConstraint("tenant_id", "email", name="uq_tenant_email"),
        )
```

```typescript
// app/db/schema.ts (Drizzle)
import { pgTable, uuid, varchar, boolean, timestamp, uniqueIndex } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

export const usersTable = pgTable(
  "users",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    tenantId: uuid("tenant_id")
      .notNull()
      .references(() => tenantsTable.id, { onDelete: "cascade" }),
    email: varchar("email", { length: 255 }).notNull(),
    fullName: varchar("full_name", { length: 255 }).notNull(),
    hashedPassword: varchar("hashed_password", { length: 255 }),
    isActive: boolean("is_active").notNull().default(true),
    isSuperuser: boolean("is_superuser").notNull().default(false),
    createdAt: timestamp("created_at").notNull().defaultNow(),
    updatedAt: timestamp("updated_at").notNull().defaultNow(),
  },
  (table) => ({
    // Composite unique constraint (email unique per tenant)
    tenantEmailIdx: uniqueIndex("uq_tenant_email").on(table.tenantId, table.email),
    // Index for tenant filtering
    tenantIdIdx: index("idx_users_tenant_id").on(table.tenantId),
  })
);

// Define relationships
export const usersRelations = relations(usersTable, ({ one }) => ({
  tenant: one(tenantsTable, {
    fields: [usersTable.tenantId],
    references: [tenantsTable.id],
  }),
}));
```

## Field Naming Conventions

### Snake Case for Database Columns
**CRITICAL**: Always use `snake_case` for database column names, regardless of language.

```python
# ✅ Correct - snake_case in database
class User(SQLModel, table=True):
    full_name: str = Field(sa_column_kwargs={"name": "full_name"})  # Explicit
    created_at: datetime  # Implicit snake_case

# ❌ Wrong - camelCase in database
class User(SQLModel, table=True):
    fullName: str  # Will create "fullName" column (WRONG!)
```

```typescript
// ✅ Correct - snake_case in Drizzle
export const usersTable = pgTable("users", {
  fullName: varchar("full_name", { length: 255 }),  // JS camelCase → DB snake_case
  createdAt: timestamp("created_at"),
});

// ❌ Wrong - camelCase in database
export const usersTable = pgTable("users", {
  fullName: varchar("fullName"),  // Creates "fullName" column (WRONG!)
});
```

### Timestamp Fields (Required)
Every table MUST include:
- **created_at**: `timestamp NOT NULL DEFAULT now()`
- **updated_at**: `timestamp NOT NULL DEFAULT now()`

```python
# SQLModel
from datetime import datetime

created_at: datetime = Field(default_factory=datetime.utcnow)
updated_at: datetime = Field(default_factory=datetime.utcnow)
```

```typescript
// Drizzle
createdAt: timestamp("created_at").notNull().defaultNow(),
updatedAt: timestamp("updated_at").notNull().defaultNow(),
```

### Boolean Fields
```python
# ✅ Correct - is_* prefix for booleans
is_active: bool = Field(default=True)
is_verified: bool = Field(default=False)
is_deleted: bool = Field(default=False)  # Soft delete flag

# ❌ Wrong - ambiguous names
active: bool  # Unclear type
verified: bool
```

### Foreign Key Naming
```python
# ✅ Correct - {table}_id format
tenant_id: str = Field(foreign_key="tenants.id")
organization_id: str = Field(foreign_key="organizations.id")
created_by_id: str = Field(foreign_key="users.id")

# ❌ Wrong - inconsistent naming
tenant: str = Field(foreign_key="tenants.id")  # Confusing with relationship
org_id: str  # Abbreviated
```

## Row-Level Security (RLS)

### Enable RLS on Multi-Tenant Tables
```sql
-- migrations/001_enable_rls.sql

-- Enable RLS on users table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users (tenant-isolated)
CREATE POLICY users_tenant_isolation ON users
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::uuid)
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);

-- Policy for superusers (cross-tenant access)
CREATE POLICY users_superuser_access ON users
    FOR ALL
    USING (
        current_setting('app.is_superuser', true)::boolean = true
    );
```

### Set Tenant Context in Application
```python
# app/repositories/base_repository.py
from sqlmodel import Session

class BaseRepository:
    """Base repository with automatic tenant filtering."""

    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

        # Set tenant context for RLS
        self.db.execute(f"SET app.tenant_id = '{tenant_id}'")

    async def list(self, skip: int = 0, limit: int = 100):
        # RLS automatically filters by tenant_id
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(statement)
        return result.scalars().all()
```

```typescript
// app/utils/db.server.ts (Drizzle)
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

export async function getDbWithTenant(tenantId: string) {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });

  // Set tenant context for RLS
  await pool.query(`SET app.tenant_id = '${tenantId}'`);

  return drizzle(pool);
}
```

## Relationships and Foreign Keys

### One-to-Many Relationships
```python
# app/models/organization.py (SQLModel)
from sqlmodel import SQLModel, Field, Relationship
from typing import List

class Organization(SQLModel, table=True):
    __tablename__ = "organizations"

    id: str = Field(primary_key=True)
    tenant_id: str = Field(foreign_key="tenants.id")
    name: str

    # One-to-many relationship
    teams: List["Team"] = Relationship(back_populates="organization")

class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: str = Field(primary_key=True)
    tenant_id: str = Field(foreign_key="tenants.id")
    organization_id: str = Field(foreign_key="organizations.id")
    name: str

    # Many-to-one relationship
    organization: Optional["Organization"] = Relationship(back_populates="teams")
```

```typescript
// app/db/schema.ts (Drizzle)
export const organizationsTable = pgTable("organizations", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenantId: uuid("tenant_id")
    .notNull()
    .references(() => tenantsTable.id, { onDelete: "cascade" }),
  name: varchar("name", { length: 255 }).notNull(),
});

export const teamsTable = pgTable("teams", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenantId: uuid("tenant_id")
    .notNull()
    .references(() => tenantsTable.id, { onDelete: "cascade" }),
  organizationId: uuid("organization_id")
    .notNull()
    .references(() => organizationsTable.id, { onDelete: "cascade" }),
  name: varchar("name", { length: 255 }).notNull(),
});

// Define relationships
export const organizationsRelations = relations(organizationsTable, ({ many }) => ({
  teams: many(teamsTable),
}));

export const teamsRelations = relations(teamsTable, ({ one }) => ({
  organization: one(organizationsTable, {
    fields: [teamsTable.organizationId],
    references: [organizationsTable.id],
  }),
}));
```

### Many-to-Many Relationships (Junction Table)
```python
# app/models/user_team.py (SQLModel)
from sqlmodel import SQLModel, Field

class UserTeamLink(SQLModel, table=True):
    """Junction table for many-to-many relationship."""
    __tablename__ = "user_team_links"

    user_id: str = Field(
        foreign_key="users.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    team_id: str = Field(
        foreign_key="teams.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    tenant_id: str = Field(
        foreign_key="tenants.id",
        nullable=False,
    )
    role: str = Field(
        default="member",
        description="User role in team (owner, admin, member)",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    # Many-to-many relationship
    teams: List["Team"] = Relationship(
        back_populates="users",
        link_model=UserTeamLink,
    )

class Team(SQLModel, table=True):
    # Many-to-many relationship
    users: List["User"] = Relationship(
        back_populates="teams",
        link_model=UserTeamLink,
    )
```

```typescript
// app/db/schema.ts (Drizzle)
export const userTeamLinksTable = pgTable(
  "user_team_links",
  {
    userId: uuid("user_id")
      .notNull()
      .references(() => usersTable.id, { onDelete: "cascade" }),
    teamId: uuid("team_id")
      .notNull()
      .references(() => teamsTable.id, { onDelete: "cascade" }),
    tenantId: uuid("tenant_id")
      .notNull()
      .references(() => tenantsTable.id, { onDelete: "cascade" }),
    role: varchar("role", { length: 50 }).notNull().default("member"),
    createdAt: timestamp("created_at").notNull().defaultNow(),
  },
  (table) => ({
    pk: primaryKey(table.userId, table.teamId),
  })
);

// Define many-to-many relationships
export const usersRelations = relations(usersTable, ({ many }) => ({
  userTeamLinks: many(userTeamLinksTable),
}));

export const teamsRelations = relations(teamsTable, ({ many }) => ({
  userTeamLinks: many(userTeamLinksTable),
}));
```

## Indexes for Performance

### Single-Column Indexes
```python
# SQLModel (defined in model)
class User(SQLModel, table=True):
    email: str = Field(index=True)  # Creates index on email
    tenant_id: str = Field(index=True)  # Creates index on tenant_id
```

```typescript
// Drizzle (defined in table schema)
export const usersTable = pgTable(
  "users",
  {
    email: varchar("email", { length: 255 }).notNull(),
    tenantId: uuid("tenant_id").notNull(),
  },
  (table) => ({
    emailIdx: index("idx_users_email").on(table.email),
    tenantIdx: index("idx_users_tenant_id").on(table.tenantId),
  })
);
```

### Composite Indexes (Multi-Column)
```sql
-- migrations/002_composite_indexes.sql

-- ✅ Composite index for tenant + email queries
CREATE INDEX idx_users_tenant_email ON users (tenant_id, email);

-- ✅ Composite index for tenant + created_at (sorting/filtering)
CREATE INDEX idx_users_tenant_created ON users (tenant_id, created_at DESC);

-- ✅ Partial index (only active users)
CREATE INDEX idx_users_active ON users (tenant_id, created_at)
WHERE is_active = true;
```

### When to Add Indexes
- **Foreign keys**: Always index `tenant_id`, `organization_id`, etc.
- **Query filters**: Index columns in WHERE clauses (e.g., `is_active`, `status`)
- **Sorting**: Index columns in ORDER BY (e.g., `created_at`, `updated_at`)
- **Unique constraints**: Index unique columns (e.g., `email`, `slug`)
- **Composite queries**: Use composite indexes for multi-column queries

## Database Migrations

### Alembic (SQLModel - FastAPI)
```bash
# Generate migration
alembic revision --autogenerate -m "Add users table with RLS"

# Apply migration
doppler run --config dev -- alembic upgrade head

# Rollback migration
doppler run --config dev -- alembic downgrade -1
```

**Example migration**:
```python
# alembic/versions/001_add_users_table.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("tenant_id", "email", name="uq_tenant_email"),
    )

    # Create indexes
    op.create_index("idx_users_tenant_id", "users", ["tenant_id"])
    op.create_index("idx_users_email", "users", ["email"])

    # Enable RLS
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY")

    # Create RLS policy
    op.execute("""
        CREATE POLICY users_tenant_isolation ON users
        FOR ALL
        USING (tenant_id = current_setting('app.tenant_id')::uuid)
        WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid)
    """)

def downgrade():
    op.drop_table("users")
```

### Drizzle Kit (TanStack Start)
```bash
# Generate migration
doppler run --config dev -- drizzle-kit generate:pg

# Apply migration
doppler run --config dev -- drizzle-kit push:pg

# Studio (visual schema editor)
doppler run --config dev -- drizzle-kit studio
```

**Example migration**:
```typescript
// drizzle/migrations/0001_add_users_table.sql
CREATE TABLE "users" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL REFERENCES "tenants"("id") ON DELETE CASCADE,
  "email" VARCHAR(255) NOT NULL,
  "full_name" VARCHAR(255) NOT NULL,
  "hashed_password" VARCHAR(255),
  "is_active" BOOLEAN NOT NULL DEFAULT true,
  "created_at" TIMESTAMP NOT NULL DEFAULT now(),
  "updated_at" TIMESTAMP NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX "idx_users_tenant_id" ON "users" ("tenant_id");
CREATE INDEX "idx_users_email" ON "users" ("email");
CREATE UNIQUE INDEX "uq_tenant_email" ON "users" ("tenant_id", "email");

-- RLS
ALTER TABLE "users" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_tenant_isolation" ON "users"
FOR ALL
USING (tenant_id = current_setting('app.tenant_id')::uuid)
WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Soft Deletes

### Soft Delete Pattern
```python
# app/models/user.py (SQLModel)
class User(SQLModel, table=True):
    is_deleted: bool = Field(
        default=False,
        description="Soft delete flag",
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Deletion timestamp",
    )
    deleted_by_id: Optional[str] = Field(
        default=None,
        foreign_key="users.id",
        description="User who deleted this record",
    )
```

```typescript
// app/db/schema.ts (Drizzle)
export const usersTable = pgTable("users", {
  isDeleted: boolean("is_deleted").notNull().default(false),
  deletedAt: timestamp("deleted_at"),
  deletedById: uuid("deleted_by_id").references(() => usersTable.id),
});
```

**Repository pattern with soft delete**:
```python
# app/repositories/user_repository.py
class UserRepository:
    async def delete(self, user_id: str, deleted_by_id: str) -> bool:
        """Soft delete a user."""
        statement = (
            update(User)
            .where(User.id == user_id, User.tenant_id == self.tenant_id)
            .values(
                is_deleted=True,
                deleted_at=datetime.utcnow(),
                deleted_by_id=deleted_by_id,
            )
        )
        await self.db.execute(statement)
        await self.db.commit()
        return True

    async def list(self, skip: int = 0, limit: int = 100):
        """List users (exclude soft-deleted)."""
        statement = (
            select(User)
            .where(
                User.tenant_id == self.tenant_id,
                User.is_deleted == False,  # Exclude deleted
            )
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(statement)
        return result.scalars().all()
```

## JSON Fields

### JSONB for Flexible Data
```python
# app/models/user.py (SQLModel)
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class User(SQLModel, table=True):
    metadata: dict = Field(
        sa_column=Column(JSONB),
        default={},
        description="Flexible metadata (JSONB)",
    )
    preferences: dict = Field(
        sa_column=Column(JSONB),
        default={"theme": "light", "language": "en"},
        description="User preferences (JSONB)",
    )
```

```typescript
// app/db/schema.ts (Drizzle)
import { jsonb } from "drizzle-orm/pg-core";

export const usersTable = pgTable("users", {
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  preferences: jsonb("preferences")
    .$type<{ theme: string; language: string }>()
    .notNull()
    .default({ theme: "light", language: "en" }),
});
```

### Query JSONB Fields
```python
# Query JSONB field
from sqlalchemy.dialects.postgresql import JSONB

statement = select(User).where(
    User.preferences["theme"].astext == "dark"
)
```

```typescript
// Query JSONB field (Drizzle)
import { sql } from "drizzle-orm";

const users = await db
  .select()
  .from(usersTable)
  .where(sql`${usersTable.preferences}->>'theme' = 'dark'`);
```

## Enum Types

### PostgreSQL Enums
```python
# app/models/user.py (SQLModel)
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum

class UserRole(str, PyEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

class UserTeamLink(SQLModel, table=True):
    role: UserRole = Field(
        sa_column=Column(SQLEnum(UserRole)),
        default=UserRole.MEMBER,
    )
```

```typescript
// app/db/schema.ts (Drizzle)
import { pgEnum } from "drizzle-orm/pg-core";

export const userRoleEnum = pgEnum("user_role", ["owner", "admin", "member", "guest"]);

export const userTeamLinksTable = pgTable("user_team_links", {
  role: userRoleEnum("role").notNull().default("member"),
});
```

## When to Apply This Skill

Use this data modeling skill when:
- Creating new database tables or modifying schemas
- Designing multi-tenant data models with tenant_id
- Setting up RLS policies for tenant isolation
- Defining relationships (one-to-many, many-to-many)
- Adding indexes for query performance
- Writing database migrations (Alembic or Drizzle Kit)
- Implementing soft delete functionality
- Using JSONB for flexible metadata
- Defining PostgreSQL enums for status fields
- Reviewing database schema in pull requests

## Template References

These data modeling patterns come from Grey Haven's actual templates:
- **Backend**: `cvi-backend-template` (SQLModel + Alembic)
- **Frontend**: `cvi-template` (Drizzle ORM + PostgreSQL)
- **Migrations**: Alembic (Python) and Drizzle Kit (TypeScript)

## Critical Reminders

1. **tenant_id everywhere** - Every table must include tenant_id foreign key
2. **RLS policies** - Enable RLS and create tenant isolation policies
3. **snake_case columns** - Always use snake_case in database (not camelCase)
4. **Timestamp fields** - Include created_at and updated_at on every table
5. **Foreign key naming** - Use {table}_id format (e.g., tenant_id, organization_id)
6. **Composite indexes** - Index (tenant_id, other_column) for multi-tenant queries
7. **Unique constraints** - Email unique per tenant, not globally
8. **Soft deletes** - Use is_deleted flag instead of hard deletes
9. **JSONB for metadata** - Use JSONB for flexible, non-relational data
10. **Migrations with Doppler** - Run migrations with `doppler run --config dev`
