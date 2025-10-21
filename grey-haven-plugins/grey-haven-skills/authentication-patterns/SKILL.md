---
name: grey-haven-authentication-patterns
description: Grey Haven's authentication patterns using better-auth - magic links, passkeys, OAuth providers, session management with Redis, JWT claims with tenant_id, and Doppler for auth secrets. Use when implementing authentication features.
---

# Grey Haven Authentication Patterns

Follow Grey Haven Studio's authentication patterns using better-auth for TanStack Start projects.

## Better-Auth Configuration

### Installation and Setup

```bash
# Install better-auth and dependencies
npm install better-auth @better-auth/drizzle
npm install -D @better-auth/cli

# Doppler provides auth secrets (never commit!)
# BETTER_AUTH_SECRET - Secret key for signing tokens
# BETTER_AUTH_URL - Base URL for callbacks
```

### Basic Configuration

```typescript
// lib/server/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "@better-auth/drizzle";
import { db } from "~/lib/server/db";
import * as schema from "~/lib/server/schema";

// Doppler provides these at runtime
const BETTER_AUTH_SECRET = process.env.BETTER_AUTH_SECRET!;
const BETTER_AUTH_URL = process.env.BETTER_AUTH_URL!;

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema,
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  secret: BETTER_AUTH_SECRET,
  baseURL: BETTER_AUTH_URL,
  trustedOrigins: [BETTER_AUTH_URL],
});
```

## Database Schema for Auth

### Auth Tables (Drizzle)

```typescript
// lib/server/schema/auth.ts
import { pgTable, uuid, text, timestamp, boolean } from "drizzle-orm/pg-core";

// Users table with multi-tenant support
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
  tenant_id: uuid("tenant_id").notNull(), // CRITICAL for multi-tenant

  // Auth fields
  email_address: text("email_address").notNull().unique(),
  email_verified: boolean("email_verified").default(false).notNull(),
  name: text("name").notNull(),
  image: text("image"),

  // Account status
  is_active: boolean("is_active").default(true).notNull(),
  last_login_at: timestamp("last_login_at"),
});

// Sessions table (managed by better-auth)
export const sessions = pgTable("sessions", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  expires_at: timestamp("expires_at").notNull(),
  token: text("token").notNull().unique(),
  user_id: uuid("user_id").references(() => users.id).notNull(),
  ip_address: text("ip_address"),
  user_agent: text("user_agent"),

  // Multi-tenant context
  tenant_id: uuid("tenant_id").notNull(),
});

// OAuth accounts table
export const accounts = pgTable("accounts", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  user_id: uuid("user_id").references(() => users.id).notNull(),
  tenant_id: uuid("tenant_id").notNull(),

  // OAuth provider details
  provider: text("provider").notNull(), // "google", "github", etc.
  provider_account_id: text("provider_account_id").notNull(),
  access_token: text("access_token"),
  refresh_token: text("refresh_token"),
  expires_at: timestamp("expires_at"),
  scope: text("scope"),
});

// Verification tokens (email, magic link)
export const verification_tokens = pgTable("verification_tokens", {
  id: uuid("id").primaryKey().defaultRandom(),
  created_at: timestamp("created_at").defaultNow().notNull(),
  expires_at: timestamp("expires_at").notNull(),
  token: text("token").notNull().unique(),
  identifier: text("identifier").notNull(), // email address
  tenant_id: uuid("tenant_id").notNull(),
});
```

### Enable RLS on Auth Tables

```sql
-- Enable RLS for multi-tenant isolation
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users (tenant isolation)
CREATE POLICY "Users can only access their tenant's data"
  ON users FOR ALL TO authenticated
  USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);

CREATE POLICY "Sessions scoped to tenant"
  ON sessions FOR ALL TO authenticated
  USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);

CREATE POLICY "Accounts scoped to tenant"
  ON accounts FOR ALL TO authenticated
  USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);
```

## Magic Link Authentication

### Configuration

```typescript
// lib/server/auth.ts
import { betterAuth } from "better-auth";
import { magicLink } from "better-auth/plugins";

// Doppler provides RESEND_API_KEY
const RESEND_API_KEY = process.env.RESEND_API_KEY!;

export const auth = betterAuth({
  // ... other config
  plugins: [
    magicLink({
      // Send magic link via email (using Resend)
      sendMagicLink: async ({ email, url, token }) => {
        const { Resend } = await import("resend");
        const resend = new Resend(RESEND_API_KEY);

        await resend.emails.send({
          from: "auth@greyhaven.studio",
          to: email,
          subject: "Sign in to Grey Haven",
          html: `
            <p>Click the link below to sign in:</p>
            <a href="${url}">Sign in to Grey Haven</a>
            <p>This link expires in 15 minutes.</p>
            <p>If you didn't request this, ignore this email.</p>
          `,
        });
      },
      // Token expires in 15 minutes
      expiresIn: 15 * 60,
    }),
  ],
});
```

### Magic Link Routes

```typescript
// routes/auth/magic-link.tsx
import { createFileRoute } from "@tanstack/react-router";
import { authClient } from "~/lib/client/auth";

export const Route = createFileRoute("/auth/magic-link")({
  component: MagicLinkPage,
});

function MagicLinkPage() {
  const [email, setEmail] = React.useState("");
  const [sent, setSent] = React.useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    await authClient.signIn.magicLink({
      email,
      callbackURL: "/dashboard",
    });

    setSent(true);
  };

  if (sent) {
    return (
      <div>
        <h1>Check your email</h1>
        <p>We sent a magic link to {email}</p>
        <p>Click the link to sign in. It expires in 15 minutes.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Sign in with Magic Link</h1>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter your email"
        required
      />
      <button type="submit">Send magic link</button>
    </form>
  );
}
```

### Magic Link Verification

```typescript
// routes/auth/verify.tsx
import { createFileRoute, redirect } from "@tanstack/react-router";
import { authClient } from "~/lib/client/auth";

export const Route = createFileRoute("/auth/verify")({
  beforeLoad: async ({ search }) => {
    const { token } = search as { token: string };

    if (!token) {
      throw redirect({ to: "/auth/login" });
    }

    // Verify magic link token
    const result = await authClient.signIn.magicLink.verify({
      token,
    });

    if (result.error) {
      throw redirect({
        to: "/auth/login",
        search: { error: "Invalid or expired magic link" },
      });
    }

    // Successfully authenticated - redirect to dashboard
    throw redirect({ to: "/dashboard" });
  },
  component: () => <div>Verifying...</div>,
});
```

## Passkey Authentication

### Configuration

```typescript
// lib/server/auth.ts
import { betterAuth } from "better-auth";
import { passkey } from "better-auth/plugins";

export const auth = betterAuth({
  // ... other config
  plugins: [
    passkey({
      // Relying party (your domain)
      rpName: "Grey Haven Studio",
      rpID: "greyhaven.studio",
      // Require user verification (biometric/PIN)
      userVerification: "required",
    }),
  ],
});
```

### Passkey Registration

```typescript
// routes/auth/passkey-register.tsx
import { createFileRoute } from "@tanstack/react-router";
import { authClient } from "~/lib/client/auth";

export const Route = createFileRoute("/auth/passkey-register")({
  component: PasskeyRegisterPage,
});

function PasskeyRegisterPage() {
  const handleRegisterPasskey = async () => {
    try {
      await authClient.passkey.register({
        name: "My Device", // Device name for user reference
      });

      alert("Passkey registered successfully!");
    } catch (error) {
      console.error("Passkey registration failed:", error);
      alert("Failed to register passkey");
    }
  };

  return (
    <div>
      <h1>Register Passkey</h1>
      <p>Use your device's biometric authentication (Face ID, Touch ID, etc.)</p>
      <button onClick={handleRegisterPasskey}>Register Passkey</button>
    </div>
  );
}
```

### Passkey Authentication

```typescript
// routes/auth/passkey-login.tsx
import { createFileRoute, redirect } from "@tanstack/react-router";
import { authClient } from "~/lib/client/auth";

export const Route = createFileRoute("/auth/passkey-login")({
  component: PasskeyLoginPage,
});

function PasskeyLoginPage() {
  const handlePasskeyLogin = async () => {
    try {
      await authClient.signIn.passkey();

      // Redirect to dashboard after successful login
      window.location.href = "/dashboard";
    } catch (error) {
      console.error("Passkey authentication failed:", error);
      alert("Authentication failed");
    }
  };

  return (
    <div>
      <h1>Sign in with Passkey</h1>
      <button onClick={handlePasskeyLogin}>Authenticate</button>
    </div>
  );
}
```

## OAuth Providers

### Google OAuth Configuration

```typescript
// lib/server/auth.ts
import { betterAuth } from "better-auth";
import { google } from "better-auth/providers";

// Doppler provides OAuth credentials
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID!;
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET!;

export const auth = betterAuth({
  // ... other config
  socialProviders: {
    google: {
      clientId: GOOGLE_CLIENT_ID,
      clientSecret: GOOGLE_CLIENT_SECRET,
      scopes: ["email", "profile"],
    },
  },
});
```

### OAuth Login Button

```typescript
// lib/components/auth/OAuthButtons.tsx
import { authClient } from "~/lib/client/auth";

export function OAuthButtons() {
  const handleGoogleLogin = async () => {
    await authClient.signIn.social({
      provider: "google",
      callbackURL: "/dashboard",
    });
  };

  return (
    <div>
      <button onClick={handleGoogleLogin}>
        <img src="/google-icon.svg" alt="Google" />
        Continue with Google
      </button>
    </div>
  );
}
```

### OAuth Callback Handling

Better-auth automatically handles OAuth callbacks at `/auth/callback`.

```typescript
// routes/auth/callback.tsx (optional custom handling)
import { createFileRoute, redirect } from "@tanstack/react-router";

export const Route = createFileRoute("/auth/callback")({
  beforeLoad: async ({ search }) => {
    // Better-auth handles the OAuth flow automatically
    // This route is only needed for custom error handling

    const { error } = search as { error?: string };

    if (error) {
      throw redirect({
        to: "/auth/login",
        search: { error },
      });
    }

    // Successful auth - redirect to dashboard
    throw redirect({ to: "/dashboard" });
  },
  component: () => <div>Completing authentication...</div>,
});
```

## Session Management with Redis

### Redis Configuration

```typescript
// lib/server/auth.ts
import { betterAuth } from "better-auth";
import { RedisStore } from "better-auth/session-stores/redis";
import { Redis } from "@upstash/redis";

// Doppler provides REDIS_URL
const REDIS_URL = process.env.REDIS_URL!;

const redis = new Redis({
  url: REDIS_URL,
});

export const auth = betterAuth({
  // ... other config
  session: {
    // Store sessions in Redis for distributed systems
    store: new RedisStore(redis),
    // Session expires in 7 days
    expiresIn: 7 * 24 * 60 * 60,
    // Update session activity every request
    updateAge: 24 * 60 * 60,
  },
});
```

### Session Middleware

```typescript
// lib/middleware/auth.ts
import { getSession } from "~/lib/server/auth";

export async function requireAuth() {
  const session = await getSession();

  if (!session) {
    throw new Error("Unauthorized");
  }

  return session;
}

export async function requireTenant() {
  const session = await requireAuth();

  if (!session.user.tenant_id) {
    throw new Error("Tenant not found");
  }

  return {
    session,
    tenantId: session.user.tenant_id,
  };
}
```

### Using Session in Routes

```typescript
// routes/_authenticated/dashboard.tsx
import { createFileRoute } from "@tanstack/react-router";
import { requireTenant } from "~/lib/middleware/auth";

export const Route = createFileRoute("/_authenticated/dashboard")({
  beforeLoad: async () => {
    // Require authentication and tenant context
    const { session, tenantId } = await requireTenant();

    return { session, tenantId };
  },
  component: DashboardPage,
});

function DashboardPage() {
  const { session, tenantId } = Route.useRouteContext();

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>Tenant: {tenantId}</p>
    </div>
  );
}
```

## JWT Claims with tenant_id

### Custom JWT Claims

```typescript
// lib/server/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  // ... other config
  session: {
    jwt: {
      // Add custom claims to JWT
      additionalClaims: async ({ user }) => {
        return {
          tenant_id: user.tenant_id,
          role: user.role || "member",
        };
      },
    },
  },
});
```

### Accessing JWT Claims

```typescript
// lib/server/functions/users.ts
import { createServerFn } from "@tanstack/start";
import { getSession } from "~/lib/server/auth";
import { db } from "~/lib/server/db";

export const getCurrentUser = createServerFn("GET", async () => {
  const session = await getSession();

  if (!session) {
    throw new Error("Unauthorized");
  }

  // JWT claims include tenant_id
  const tenantId = session.user.tenant_id;

  // All queries automatically filtered by tenant_id via RLS
  const user = await db.query.users.findFirst({
    where: (users, { eq }) => eq(users.id, session.user.id),
  });

  return user;
});
```

### JWT Claims in Database Queries

```sql
-- RLS policies automatically use JWT claims
CREATE POLICY "Tenant isolation"
  ON users FOR ALL TO authenticated
  USING (
    tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid
  );
```

## Doppler Environment Variables

### Required Auth Variables

```bash
# Doppler provides these (NEVER commit to .env!)

# Better-auth core
BETTER_AUTH_SECRET=<random-secret-key>  # Generate with: openssl rand -hex 32
BETTER_AUTH_URL=http://localhost:3000   # Base URL for callbacks

# Email (Resend for magic links)
RESEND_API_KEY=re_...

# OAuth providers
GOOGLE_CLIENT_ID=*.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-...

GITHUB_CLIENT_ID=Iv1...
GITHUB_CLIENT_SECRET=...

MICROSOFT_CLIENT_ID=...
MICROSOFT_CLIENT_SECRET=...

# Redis (session storage)
REDIS_URL=redis://localhost:6379

# Database
DATABASE_URL_ADMIN=postgresql://...
DATABASE_URL_AUTHENTICATED=postgresql://...
DATABASE_URL_ANON=postgresql://...
```

### Doppler Configuration per Environment

```bash
# Development (doppler run --config dev)
BETTER_AUTH_URL=http://localhost:3000
RESEND_API_KEY=re_test_...  # Use test API key
REDIS_URL=redis://localhost:6379

# Test (doppler run --config test)
BETTER_AUTH_URL=http://localhost:3000
RESEND_API_KEY=re_test_...
REDIS_URL=redis://localhost:6379/1  # Use DB 1 for tests

# Production (doppler run --config production)
BETTER_AUTH_URL=https://app.greyhaven.studio
RESEND_API_KEY=re_...  # Production API key
REDIS_URL=redis://:password@redis.upstash.io:6379
```

## Authentication Patterns

### Multi-Tenant User Registration

```typescript
// lib/server/functions/auth.ts
import { createServerFn } from "@tanstack/start";
import { db } from "~/lib/server/db";
import { users, tenants } from "~/lib/server/schema";

export const registerUser = createServerFn("POST", async (data: {
  email: string;
  name: string;
  organizationName: string;
}) => {
  // 1. Create tenant first
  const [tenant] = await db.insert(tenants).values({
    name: data.organizationName,
    slug: data.organizationName.toLowerCase().replace(/\s+/g, "-"),
  }).returning();

  // 2. Create user with tenant_id
  const [user] = await db.insert(users).values({
    email_address: data.email,
    name: data.name,
    tenant_id: tenant.id,
    email_verified: false,
  }).returning();

  // 3. Send verification email
  // (better-auth handles this automatically)

  return { user, tenant };
});
```

### Protected Server Functions

```typescript
// lib/server/functions/protected.ts
import { createServerFn } from "@tanstack/start";
import { getSession } from "~/lib/server/auth";

export const protectedFunction = createServerFn("POST", async (data) => {
  // Require authentication
  const session = await getSession();
  if (!session) {
    throw new Error("Unauthorized");
  }

  // Get tenant_id from JWT claims
  const tenantId = session.user.tenant_id;

  // All database queries automatically scoped to tenant via RLS
  // ...
});
```

### Logout Handler

```typescript
// lib/components/auth/LogoutButton.tsx
import { authClient } from "~/lib/client/auth";

export function LogoutButton() {
  const handleLogout = async () => {
    await authClient.signOut();
    window.location.href = "/auth/login";
  };

  return <button onClick={handleLogout}>Sign Out</button>;
}
```

## Testing Authentication

### Auth Testing with Doppler

```typescript
// tests/integration/auth.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { authClient } from "~/lib/client/auth";

// Doppler provides test environment variables
describe("Authentication", () => {
  beforeEach(async () => {
    // Clear test sessions
  });

  it("completes magic link authentication flow", async () => {
    // Request magic link
    await authClient.signIn.magicLink({
      email: "test@example.com",
    });

    // In real tests, intercept email and extract token
    const token = "test-magic-link-token";

    // Verify token
    const result = await authClient.signIn.magicLink.verify({ token });

    expect(result.session).toBeDefined();
    expect(result.user.email).toBe("test@example.com");
  });

  it("enforces tenant isolation in sessions", async () => {
    // Login as tenant A user
    const sessionA = await authClient.signIn.email({
      email: "userA@example.com",
      password: "password",
    });

    expect(sessionA.user.tenant_id).toBe("tenant-a-uuid");

    // Login as tenant B user
    const sessionB = await authClient.signIn.email({
      email: "userB@example.com",
      password: "password",
    });

    expect(sessionB.user.tenant_id).toBe("tenant-b-uuid");
    expect(sessionB.user.tenant_id).not.toBe(sessionA.user.tenant_id);
  });
});
```

## When to Apply This Skill

Use this skill when:
- Implementing authentication flows
- Adding OAuth providers
- Setting up magic link authentication
- Configuring passkey authentication
- Managing user sessions
- Implementing multi-tenant auth
- Configuring Doppler for auth secrets
- Writing auth-related tests

## Template References

These authentication patterns are from Grey Haven's actual template:
- **Frontend**: `cvi-template` (TanStack Start + better-auth)

## Critical Reminders

1. **Doppler**: ALWAYS use for auth secrets (BETTER_AUTH_SECRET, OAuth keys)
2. **tenant_id**: REQUIRED in users, sessions, accounts tables
3. **RLS**: Enable on all auth tables for tenant isolation
4. **JWT claims**: Include tenant_id for database RLS
5. **Redis**: Use for session storage in distributed systems
6. **Magic links**: Expire in 15 minutes, single-use only
7. **OAuth**: Use test credentials in dev/test environments
8. **Passkeys**: Require user verification (biometric/PIN)
9. **Sessions**: Expire in 7 days, update on activity
10. **Testing**: Run with `doppler run --config test -- npm run test`
