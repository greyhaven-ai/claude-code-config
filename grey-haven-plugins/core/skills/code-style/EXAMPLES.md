# Code Examples

Copy-paste ready examples from Grey Haven Studio production templates.

## TypeScript/React Examples

### React Component Structure

Complete example from [cvi-template/src/routes/settings/profile.tsx](https://github.com/greyhaven-ai/cvi-template):

```typescript
import { createFileRoute } from "@tanstack/react-router";
import { useRef, useState } from "react";
import { useAuth } from "~/components/auth/provider";
import { ImageUploadDialog } from "~/components/settings/image-upload-dialog";
import { SettingsWrapper } from "~/components/settings/wrapper";
import { Button } from "~/components/ui/button";
import { Input } from "~/components/ui/input";
import { SmartAvatar } from "~/components/ui/smart-avatar";
import authClient from "~/utils/auth-client";

export const Route = createFileRoute("/settings/profile")({
  component: RouteComponent,
});

function RouteComponent() {
  // 1. Custom hooks
  const { user } = useAuth<SignedInContext>();

  // 2. State management
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false);
  const urlInputRef = useRef<HTMLInputElement>(null);

  // 3. Event handlers
  const saveChanges = async (data: Record<keyof NonNullable<User>, any>) => {
    await authClient.updateUser({ name: data.name, image: data.image });
    location.reload();
    return true;
  };

  // 4. Main render with form fields
  return (
    <>
      <SettingsWrapper
        title="Edit Profile"
        saveChanges={saveChanges}
        fields={[
          {
            id: "name",
            type: "data",
            value: { defaultValue: user.name },
            validate: (name: string) => {
              if (!name || name.length < 3) {
                return { error: "Has to be at least 3 characters long" };
              }
            },
            component: ({ value, disabled, update, error }) => (
              <>
                <span className="text-sm font-semibold">Username</span>
                <Input
                  defaultValue={value}
                  disabled={disabled}
                  type="text"
                  onBlur={(e) => update(e.currentTarget.value)}
                  placeholder="Your user name"
                  className={`max-w-[70%] ${error && "border-red-400"}`}
                />
              </>
            ),
          },
          {
            id: "image",
            type: "data",
            value: { defaultValue: user.image },
            component: ({ value, disabled, update }) => (
              <>
                <span className="text-sm font-semibold">Avatar</span>
                <div className="flex max-w-[70%] gap-2">
                  <Input
                    ref={urlInputRef}
                    defaultValue={value}
                    disabled={disabled}
                    type="text"
                    onBlur={(e) => update(e.currentTarget.value)}
                    placeholder="Your avatar url"
                    className="flex-1"
                  />
                  <Button
                    variant="secondary"
                    size="default"
                    disabled={disabled}
                    onClick={() => setIsUploadDialogOpen(true)}
                    type="button"
                    className="max-w-max"
                  >
                    Upload
                  </Button>
                </div>
              </>
            ),
          },
        ]}
      />
    </>
  );
}
```

### Custom React Hook

Example from [cvi-template/src/hooks/use-plan.ts](https://github.com/greyhaven-ai/cvi-template):

```typescript
import type { CustomerState } from "@polar-sh/sdk/models/components/customerstate.js";
import { useQuery } from "@tanstack/react-query";
import { polarProducts } from "~/config/polar-config";
import { queryClient } from "~/lib/query-client";
import authClient from "~/utils/auth-client";

export type PlanType = "free" | string;

export interface UsePlanReturn {
  planType: PlanType;
  activeSubscription: any | null;
  customerState: CustomerState | null;
  isLoading: boolean;
  error: any;
}

export function usePlan(): UsePlanReturn {
  // TanStack Query with proper configuration
  const {
    data: customerState,
    isPending,
    error,
  } = useQuery(
    {
      queryKey: ["customerState"],
      queryFn: async () => {
        const { data: customerState, error } = await authClient.customer.state();
        if (error) throw error;
        return customerState;
      },
    },
    queryClient,
  );

  // Helper function
  const getPlanType = (): PlanType => {
    if (
      !customerState?.activeSubscriptions ||
      customerState.activeSubscriptions.length === 0
    ) {
      return "free";
    }

    const type = polarProducts.find(
      (p) => p.productId === customerState.activeSubscriptions[0].productId,
    )?.slug;

    return type || "free";
  };

  const planType = getPlanType();
  const activeSubscription = customerState?.activeSubscriptions?.[0] || null;

  return {
    planType,
    activeSubscription,
    customerState: customerState || null,
    isLoading: isPending,
    error,
  };
}
```

### Database Schema (Drizzle with snake_case)

Example from [cvi-template/src/server/schema/auth.schema.ts](https://github.com/greyhaven-ai/cvi-template):

```typescript
import { SQL, sql } from "drizzle-orm";
import {
  AnyPgColumn,
  boolean,
  index,
  pgEnum,
  pgPolicy,
  pgTable,
  text,
  timestamp,
  unique,
} from "drizzle-orm/pg-core";

// Helper functions for RLS policies
const getUserId = (): SQL => sql`current_setting('app.user_id', true)`;
const getTenantId = (): SQL => sql`current_setting('app.tenant_id', true)`;
const getUserRole = (): SQL => sql`current_setting('app.user_role', true)`;

// Helper to check if user ID matches
export const authUid = (userIdColumn: AnyPgColumn): SQL =>
  sql`${getUserId()} = ${userIdColumn}::text`;

// Helper for tenant isolation
export const isSameTenant = (tenantIdCol: AnyPgColumn): SQL =>
  sql`(${getTenantId()} = ${tenantIdCol}::text)`;

export const isAppAdmin = (): SQL => sql`${getUserRole()} = 'app_admin'::text`;

export const inSameTenant = (tenantIdCol: AnyPgColumn, query: SQL): SQL =>
  sql`${isSameTenant(tenantIdCol)} and (${query})`;

// User role enum
export const userRoleEnum = pgEnum("role", ["user", "org_admin", "app_admin"]);

// User table with multi-tenant support and RLS policies
export const user = pgTable(
  "users",
  {
    id: text("id").primaryKey(),
    name: text("name").notNull(),
    email: text("email").notNull(),
    emailVerified: boolean("email_verified").notNull(),
    image: text("image"),
    createdAt: timestamp("created_at").notNull(),
    updatedAt: timestamp("updated_at"),
    role: userRoleEnum().default("user"),
    userId: text("user_id"),
    tenantId: text("tenant_id").notNull().default("dev"),  // Multi-tenant field
    serviceId: text("service_id").default("default"),
  },
  (table) => [
    // Indexes for query performance
    index("user_email_idx").on(table.email),
    index("user_user_id_idx").on(table.userId),
    index("user_tenant_id_idx").on(table.tenantId),
    index("user_service_id_idx").on(table.serviceId),
    unique("user_email_tenant_id_unique").on(table.email, table.tenantId),

    // RLS Policy: Authenticated users can read their own record or if they're app admin, within same tenant
    pgPolicy("user_authenticated_select", {
      for: "select",
      to: "public",
      using: inSameTenant(
        table.tenantId,
        sql`(${getUserId()} = ${table.id}::text) or ${isAppAdmin()}`,
      ),
    }),

    // RLS Policy: Insert with tenant isolation
    pgPolicy("user_authenticated_insert", {
      for: "insert",
      to: "public",
      withCheck: inSameTenant(
        table.tenantId,
        sql`${authUid(table.id)} or ${isAppAdmin()}`,
      ),
    }),

    // RLS Policy: Update own record or admin
    pgPolicy("user_authenticated_update", {
      for: "update",
      to: "public",
      using: inSameTenant(table.tenantId, sql`${authUid(table.id)} or ${isAppAdmin()}`),
      withCheck: inSameTenant(
        table.tenantId,
        sql`${authUid(table.id)} or ${isAppAdmin()}`,
      ),
    }),

    // RLS Policy: Delete own record or admin
    pgPolicy("user_authenticated_delete", {
      for: "delete",
      to: "public",
      using: inSameTenant(table.tenantId, sql`${authUid(table.id)} or ${isAppAdmin()}`),
    }),
  ],
);
```

### Environment Variables with Validation

Example from [cvi-template/src/utils/env.ts](https://github.com/greyhaven-ai/cvi-template):

```typescript
import { createEnv } from "@t3-oss/env-core";
import { z } from "zod";

/**
 * Client-side environment variables accessible in the browser.
 * All client variables must be prefixed with VITE_ for Vite to expose them.
 */
const clientVariables = {
  /** Application display name shown in UI components */
  VITE_APP_NAME: z.string(),

  /** Base URL of the application */
  VITE_BASE_URL: z.string().url(),

  /** Feature flag to enable/disable billing features */
  VITE_ENABLE_BILLING: z.enum(["true", "false"]),

  /** Cloudflare Turnstile site key for CAPTCHA verification */
  VITE_TURNSTILE_SITE_KEY: z.string(),

  /** PostHog API key for analytics */
  VITE_POSTHOG_KEY: z.string(),

  /** PostHog host URL */
  VITE_POSTHOG_HOST: z.string(),

  /** Tenant identifier for multi-tenant authentication */
  VITE_TENANT_ID: z.string(),

  /** Service identifier for API authentication */
  VITE_SERVICE_ID: z.string(),

  /** API mode switch for demo vs production */
  VITE_API_MODE: z.enum(["demo", "prod"]),

  /** Production API base URL */
  VITE_PROD_BASE_URL: z.string().url(),
};

/**
 * Server-side environment variables configuration.
 * These variables are only accessible on the server and contain sensitive data.
 */
export const env = createEnv({
  server: {
    /** Application name used in emails and server-side operations */
    APP_NAME: z.string(),

    /** Secret key for Better Auth session management (min 25 chars) */
    BETTER_AUTH_SECRET: z.string().min(25),

    /** Better Auth base URL */
    BETTER_AUTH_URL: z.string().url(),

    /** PostgreSQL database connection URL */
    DATABASE_URL: z.string().url(),

    /** Redis connection URL for session storage */
    REDIS_URL: z.string().url(),

    /** Google OAuth client ID */
    GOOGLE_CLIENT_ID: z.string(),

    /** Google OAuth client secret */
    GOOGLE_CLIENT_SECRET: z.string(),

    /** AWS S3 bucket name for file storage */
    AWS_S3_BUCKET: z.string(),

    /** AWS region */
    AWS_REGION: z.string(),

    /** AWS access key ID */
    AWS_ACCESS_KEY_ID: z.string(),

    /** AWS secret access key */
    AWS_SECRET_ACCESS_KEY: z.string(),
  },
  client: clientVariables,
  runtimeEnv: import.meta.env,
  skipValidation: import.meta.env.NODE_ENV === "test",
});

// Usage in code
import { env } from "~/utils/env";

const dbUrl = env.DATABASE_URL; // Fully typed and validated!
const apiUrl = env.VITE_API_URL; // Fully typed and validated!
```

## Python/FastAPI Examples

### FastAPI Router Structure

Example from [cvi-backend-template/app/routers/accounts.py](https://github.com/greyhaven-ai/cvi-backend-template):

```python
import uuid
from app.db.models.account import AccountDB
from app.db.repositories import AccountRepository, TenantRepository
from app.dependencies import get_account_repository, get_tenant_repository, verify_api_key_with_tenant
from app.schemas.accounts import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
    AccountWithTenants,
    TenantResponse,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Annotated

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(verify_api_key_with_tenant)],
)


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    account_repo: Annotated[AccountRepository, Depends(get_account_repository)],
) -> AccountResponse:
    """Create a new account with optional Polar customer creation."""
    # Check if slug already exists
    existing = await account_repo.get_by_slug(account_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Account with slug '{account_data.slug}' already exists",
        )

    # Create account
    account = AccountDB(id=f"acc-{uuid.uuid4()}", **account_data.model_dump())

    created_account = await account_repo.create(account)
    return AccountResponse.model_validate(created_account)


@router.get("/{account_id}", response_model=AccountWithTenants)
async def get_account(
    account_id: str,
    account_repo: Annotated[AccountRepository, Depends(get_account_repository)],
    tenant_repo: Annotated[TenantRepository, Depends(get_tenant_repository)],
) -> AccountWithTenants:
    """Get account details with associated tenants."""
    account = await account_repo.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found",
        )

    # Get associated tenants
    tenants = await tenant_repo.list_by_account(account_id, include_inactive=True)

    return AccountWithTenants(
        **AccountResponse.model_validate(account).model_dump(),
        tenants=[TenantResponse.model_validate(t) for t in tenants],
        tenant_count=len(tenants),
    )


@router.get("/", response_model=list[AccountResponse])
async def list_accounts(
    account_repo: Annotated[AccountRepository, Depends(get_account_repository)],
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> list[AccountResponse]:
    """List all active accounts."""
    accounts = await account_repo.list_active(limit=limit, offset=offset)
    return [AccountResponse.model_validate(a) for a in accounts]


@router.patch("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    update_data: AccountUpdate,
    account_repo: Annotated[AccountRepository, Depends(get_account_repository)],
) -> AccountResponse:
    """Update account details."""
    account = await account_repo.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found",
        )

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(account, field, value)

    updated_account = await account_repo.update(account)
    return AccountResponse.model_validate(updated_account)
```

### SQLModel Database Models

Example from [cvi-backend-template/app/db/models/tenant.py](https://github.com/greyhaven-ai/cvi-backend-template):

```python
from __future__ import annotations

import secrets
from app.db.db_types import UTCDateTime, utc_now
from datetime import datetime
from sqlalchemy import Column as SAColumn
from sqlmodel import JSON, Column, Field, SQLModel
from typing import Any


def generate_api_key() -> str:
    """Generate a secure API key for tenant authentication."""
    return f"sk_tenant_{secrets.token_urlsafe(32)}"


class TenantDB(SQLModel, table=True):  # type: ignore[call-arg]
    """Database model representing a tenant (frontend application instance).

    Each tenant is a specific frontend app owned by an account. Tenants have
    their own API keys, users, and service configurations. This is the primary
    isolation boundary for data access.
    """

    __tablename__ = "tenants"

    # Primary identification
    id: str = Field(
        primary_key=True,
        description="Unique tenant identifier, e.g. 'tenant-acme-healthcare'",
    )
    account_id: str = Field(
        foreign_key="accounts.id",
        index=True,
        description="The account that owns this tenant",
    )

    # Tenant information
    name: str = Field(
        description="Friendly name for the frontend app, e.g. 'Acme Healthcare Portal'"
    )
    slug: str = Field(index=True, description="URL-friendly identifier")
    description: str | None = Field(
        default=None, description="Optional description of the tenant's purpose"
    )

    # Authentication
    api_key: str = Field(
        default_factory=generate_api_key,
        unique=True,
        index=True,
        description="API key for backend authentication",
    )
    api_key_provider_id: str | None = Field(
        default=None,
        index=True,
        description="External API key provider ID (e.g., Unkey key ID)",
    )

    # Access control
    allowed_origins: list[str] | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Allowed CORS origins for this tenant",
    )
    allowed_ip_ranges: list[str] | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Optional IP allowlist in CIDR notation",
    )

    # Status flags
    is_active: bool = Field(
        default=True, description="Whether tenant is active and can make API calls"
    )
    is_demo: bool = Field(
        default=False, description="Whether this is a demo/sandbox tenant"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=SAColumn(UTCDateTime, nullable=False),
        description="Tenant creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=SAColumn(UTCDateTime, nullable=False, onupdate=utc_now),
        description="Last update timestamp",
    )
```

### User Model with Multi-Tenant Support

Example from [cvi-backend-template/app/db/models/user.py](https://github.com/greyhaven-ai/cvi-backend-template):

```python
from app.db.db_types import UTCDateTime, utc_now
from datetime import datetime
from sqlalchemy import Column as SAColumn
from sqlmodel import Field, SQLModel


class UserDB(SQLModel, table=True):  # type: ignore[call-arg]
    """User database model with multi-tenant support."""

    __tablename__ = "users"

    id: str = Field(primary_key=True, description="User's unique identifier")
    name: str = Field(description="User's full name")
    email: str = Field(index=True, unique=True, description="User's email address")
    email_verified: bool = Field(
        default=False, description="Whether the user's email has been verified"
    )
    image: str | None = Field(default=None, description="URL of the user's profile image")

    role: str = Field(
        default="user", description="Role of the user (e.g., user, org_admin, cvi_admin)"
    )

    # Multi-tenant fields (CRITICAL)
    tenant_id: str = Field(index=True, description="Owning tenant/organisation identifier")
    service_id: str | None = Field(
        default=None, index=True, description="Logical domain (e.g. healthcare, education)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=utc_now, sa_column=SAColumn(UTCDateTime, nullable=False)
    )
    updated_at: datetime | None = Field(
        default_factory=utc_now,
        sa_column=SAColumn(UTCDateTime, nullable=True, onupdate=utc_now),
    )
```

### Pydantic Request/Response Schemas

Example from [cvi-backend-template/app/schemas/accounts.py](https://github.com/greyhaven-ai/cvi-backend-template):

```python
import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Any


class AccountBase(BaseModel):
    """Base account schema with shared fields."""

    name: str = Field(..., description="Company/Organization name")
    slug: str = Field(..., description="URL-friendly identifier")
    billing_tier: str = Field(default="starter", description="Subscription tier")
    billing_email: str = Field(..., description="Primary billing contact email")
    billing_address: dict[str, Any] | None = Field(
        default=None, description="Billing address"
    )

    # Limits
    max_tenants: int = Field(default=3, ge=1, description="Maximum number of tenants")
    max_users_per_tenant: int = Field(default=100, ge=1, description="Maximum users per tenant")
    max_api_calls_per_month: int = Field(
        default=1000000, ge=0, description="Monthly API call limit"
    )

    # Metadata
    account_metadata: dict[str, Any] | None = Field(
        default=None, description="Arbitrary metadata"
    )

    @field_validator("slug")
    def validate_slug(cls, v: str) -> str:
        """Validate slug format."""
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("Slug must contain only lowercase letters, numbers, and hyphens")
        return v

    @field_validator("billing_email")
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Invalid email format")
        return v


class AccountCreate(AccountBase):
    """Schema for creating an account."""

    pass


class AccountUpdate(BaseModel):
    """Schema for updating an account (all fields optional)."""

    name: str | None = None
    billing_tier: str | None = None
    billing_email: str | None = None
    billing_address: dict[str, Any] | None = None
    billing_provider_id: str | None = None

    # Limits
    max_tenants: int | None = Field(None, ge=1)
    max_users_per_tenant: int | None = Field(None, ge=1)
    max_api_calls_per_month: int | None = Field(None, ge=0)

    # Metadata
    account_metadata: dict[str, Any] | None = None


class AccountResponse(AccountBase):
    """Account response schema."""

    id: str
    billing_provider_id: str | None = None
    polar_subscription_id: str | None = None
    billing_status: str = "pending"
    billing_period_end: datetime | None = None

    # Status
    is_active: bool
    is_trial: bool
    trial_ends_at: datetime | None = None
    suspended_at: datetime | None = None
    suspension_reason: str | None = None

    # Timestamps
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### Repository Pattern with Tenant Isolation

Example from [cvi-backend-template/app/db/repositories/tenant_repository.py](https://github.com/greyhaven-ai/cvi-backend-template):

```python
from __future__ import annotations

from app.db.models.tenant import TenantDB, generate_api_key
from datetime import UTC, datetime
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class TenantRepository:
    """Repository for tenant-related database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tenant: TenantDB) -> TenantDB:
        """Create a new tenant."""
        self.session.add(tenant)
        await self.session.commit()
        await self.session.refresh(tenant)
        return tenant

    async def get_by_id(self, tenant_id: str) -> TenantDB | None:
        """Get tenant by ID."""
        stmt = select(TenantDB).where(TenantDB.id == tenant_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_api_key(self, api_key: str) -> TenantDB | None:
        """Get tenant by API key."""
        stmt = select(TenantDB).where(TenantDB.api_key == api_key)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_slug(self, account_id: str, slug: str) -> TenantDB | None:
        """Get tenant by slug within an account (tenant isolation)."""
        stmt = select(TenantDB).where(
            and_(TenantDB.account_id == account_id, TenantDB.slug == slug)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_by_account(
        self, account_id: str, include_inactive: bool = False
    ) -> list[TenantDB]:
        """List all tenants for an account."""
        stmt = select(TenantDB).where(TenantDB.account_id == account_id)
        if not include_inactive:
            stmt = stmt.where(TenantDB.is_active == True)
        stmt = stmt.order_by(TenantDB.created_at.desc())

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, tenant: TenantDB) -> TenantDB:
        """Update an existing tenant."""
        await self.session.commit()
        await self.session.refresh(tenant)
        return tenant

    async def rotate_api_key(self, tenant_id: str) -> TenantDB | None:
        """Rotate the API key for a tenant."""
        tenant = await self.get_by_id(tenant_id)
        if tenant:
            tenant.api_key = generate_api_key()
            return await self.update(tenant)
        return None

    async def suspend(self, tenant_id: str, reason: str) -> TenantDB | None:
        """Suspend a tenant."""
        tenant = await self.get_by_id(tenant_id)
        if tenant:
            tenant.is_active = False
            tenant.suspended_at = datetime.now(UTC)
            tenant.suspension_reason = reason
            return await self.update(tenant)
        return None

    async def reactivate(self, tenant_id: str) -> TenantDB | None:
        """Reactivate a suspended tenant."""
        tenant = await self.get_by_id(tenant_id)
        if tenant:
            tenant.is_active = True
            tenant.suspended_at = None
            tenant.suspension_reason = None
            return await self.update(tenant)
        return None
```

### Pytest Unit Tests

Example from [cvi-backend-template/tests/unit/repositories/test_tenant_repository.py](https://github.com/greyhaven-ai/cvi-backend-template):

```python
"""Unit tests for TenantRepository."""
import pytest
from app.db.models.tenant import TenantDB, generate_api_key
from app.db.repositories.tenant_repository import TenantRepository
from datetime import UTC, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, MagicMock


class TestTenantRepository:
    """Test TenantRepository methods."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        session = AsyncMock(spec=AsyncSession)
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        session.execute = AsyncMock()
        return session

    @pytest.fixture
    def repository(self, mock_session):
        """Create repository instance with mock session."""
        return TenantRepository(mock_session)

    @pytest.fixture
    def sample_tenant(self):
        """Create a sample tenant for testing."""
        return TenantDB(
            id="tenant-123",
            account_id="acc-123",
            slug="test-tenant",
            name="Test Tenant",
            api_key="sk_tenant_test123",
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    @pytest.mark.asyncio
    async def test_create_tenant(self, repository, mock_session, sample_tenant):
        """Test creating a new tenant."""
        # Act
        result = await repository.create(sample_tenant)

        # Assert
        mock_session.add.assert_called_once_with(sample_tenant)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_tenant)
        assert result == sample_tenant

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repository, mock_session, sample_tenant):
        """Test getting tenant by ID when it exists."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sample_tenant
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_by_id("tenant-123")

        # Assert
        assert result == sample_tenant

    @pytest.mark.asyncio
    async def test_get_by_slug_with_tenant_isolation(self, repository, mock_session, sample_tenant):
        """Test getting tenant by slug within an account (tenant isolation)."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sample_tenant
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_by_slug("acc-123", "test-tenant")

        # Assert
        assert result == sample_tenant
        # Verify both account_id and slug are in query
        query = mock_session.execute.call_args[0][0]
        query_str = str(query)
        assert "account_id" in query_str
        assert "slug" in query_str

    @pytest.mark.asyncio
    async def test_suspend(self, repository, mock_session, sample_tenant):
        """Test suspending a tenant."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sample_tenant
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.suspend("tenant-123", "Violation of terms")

        # Assert
        assert result is not None
        assert result.is_active is False
        assert result.suspended_at is not None
        assert result.suspension_reason == "Violation of terms"
        mock_session.commit.assert_called_once()


class TestGenerateApiKey:
    """Test the generate_api_key function."""

    def test_generate_api_key_format(self):
        """Test that generated API keys have correct format."""
        key = generate_api_key()

        assert key.startswith("sk_tenant_")
        suffix = key[len("sk_tenant_") :]
        assert len(suffix) >= 40
        assert len(suffix) <= 50

    def test_generate_api_key_uniqueness(self):
        """Test that generated API keys are unique."""
        keys = [generate_api_key() for _ in range(100)]

        # All keys should be unique
        assert len(set(keys)) == 100
```

## Before/After Comparisons

### Wrong: camelCase in Database Schema

```typescript
// ❌ WRONG - Don't do this
export const users = pgTable("users", {
  id: uuid("id"),
  createdAt: timestamp("createdAt"), // Wrong!
  tenantId: uuid("tenantId"), // Wrong!
  emailAddress: text("emailAddress"), // Wrong!
  displayName: text("displayName"), // Wrong!
  isActive: boolean("isActive"), // Wrong!
});
```

### Correct: snake_case in Database Schema

```typescript
// ✅ CORRECT - Always use snake_case
export const users = pgTable("users", {
  id: uuid("id"),
  created_at: timestamp("created_at"), // Correct!
  tenant_id: uuid("tenant_id"), // Correct!
  email_address: text("email_address"), // Correct!
  display_name: text("display_name"), // Correct!
  is_active: boolean("is_active"), // Correct!
});
```

### Wrong: Missing Type Hints (Python)

```python
# ❌ WRONG - Don't do this
def get_user(user_id):  # Missing type hints!
    return db.query(User).filter(User.id == user_id).first()

async def create_user(data):  # Missing type hints!
    user = User(**data)
    db.add(user)
    await db.commit()
    return user
```

### Correct: Type Hints Required (Python)

```python
# ✅ CORRECT - Always include type hints
from typing import Optional

def get_user(user_id: str) -> Optional[User]:  # Type hints!
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

async def create_user(data: UserCreate) -> User:  # Type hints!
    """Create new user."""
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    return user
```

## Key Patterns Summary

### TypeScript/React

- ✅ Imports auto-sorted by prettier-plugin-organize-imports
- ✅ Custom hooks use `use-` prefix
- ✅ TanStack Query with `staleTime: 60000` (1 minute default)
- ✅ Database fields use `snake_case` (even in TypeScript schemas)
- ✅ Environment validation with @t3-oss/env-core and Zod
- ✅ RLS policies for multi-tenant isolation

### Python/FastAPI

- ✅ Type hints with `Annotated` for dependency injection
- ✅ Proper HTTP status codes and error handling
- ✅ Repository pattern for data access
- ✅ Pydantic schemas with `field_validator`
- ✅ SQLModel with `snake_case` fields
- ✅ Pytest with `@pytest.mark.asyncio` and fixtures
- ✅ Multi-tenant isolation in all queries
