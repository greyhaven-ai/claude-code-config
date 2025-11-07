# OWASP Top 10 2021 - Grey Haven Implementation Guide

Complete OWASP Top 10 coverage mapped to Grey Haven stack (TanStack Start, FastAPI, PostgreSQL, Cloudflare Workers).

## A01: Broken Access Control

**Risk**: Users can act outside their intended permissions (multi-tenant data leaks, privilege escalation)

### Grey Haven Patterns

```typescript
// ✅ SECURE: Row-Level Security (RLS) in PostgreSQL
CREATE POLICY tenant_isolation ON users
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

// ✅ Server-side authorization checks
export const getOrder = createServerFn({ method: 'GET' })
  .handler(async ({ data }) => {
    const session = await auth.api.getSession({ headers: request.headers });

    // Check tenant isolation
    const order = await db.query.orders.findFirst({
      where: and(
        eq(orders.id, data.orderId),
        eq(orders.tenant_id, session.user.tenantId)  // ✅ Tenant filter
      )
    });

    if (!order) throw new Error('Not found');

    // Check user permissions
    if (order.userId !== session.user.id && session.user.role !== 'admin') {
      throw new Error('Forbidden');
    }

    return order;
  });
```

**Prevention**:
- Enforce RLS policies on all PostgreSQL tables
- Never trust client-side access control
- Use TanStack server functions for authorization
- Include `tenant_id` in ALL queries
- Deny by default, permit by exception

## A02: Cryptographic Failures

**Risk**: Exposure of sensitive data (passwords, API keys, session tokens)

### Grey Haven Patterns

```typescript
// ✅ SECURE: Doppler for secrets, Argon2id for passwords
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  emailAndPassword: {
    async hashPassword(password) {
      return await hash(password, {
        memoryCost: 19456,  // 19 MiB
        timeCost: 2,
        outputLen: 32,
        parallelism: 1
      });  // Argon2id - OWASP recommended
    }
  },

  session: {
    cookieName: "session",
    cookieCache: { enabled: true, maxAge: 300 }
  },

  advanced: {
    useSecureCookies: true,  // HTTPS only
  }
});

// ✅ Encrypt sensitive fields in database
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT NOT NULL,
  password_hash TEXT NOT NULL,  -- Argon2id hash
  ssn TEXT,                     -- Encrypted at rest
  created_at TIMESTAMPTZ DEFAULT NOW()
);

// Enable pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

// Encrypt sensitive data
INSERT INTO users (ssn) VALUES (
  pgp_sym_encrypt('123-45-6789', current_setting('app.encryption_key'))
);
```

**Prevention**:
- Store all secrets in Doppler (never in code)
- Use Argon2id for password hashing
- Enable PostgreSQL encryption at rest
- Use HTTPS only (Cloudflare enforced)
- Encrypt PII/PHI fields with pgcrypto

## A03: Injection

**Risk**: SQL injection, XSS, command injection

### Grey Haven Patterns

```typescript
// ✅ SECURE: Drizzle ORM (parameterized queries)
import { eq, and } from 'drizzle-orm';

const users = await db.query.users.findMany({
  where: and(
    eq(users.email, searchQuery),  // ✅ Parameterized
    eq(users.tenant_id, tenantId)
  )
});

// ✅ React auto-escapes JSX
function SearchResults({ query }: { query: string }) {
  return <p>Results for: {query}</p>;  // ✅ Auto-escaped
}

// ✅ If HTML needed, use DOMPurify
import DOMPurify from 'isomorphic-dompurify';

<div dangerouslySetInnerHTML={{
  __html: DOMPurify.sanitize(userContent, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em'],
    ALLOWED_ATTR: []
  })
}} />
```

**Prevention**:
- Use Drizzle ORM (never raw SQL)
- Rely on React's auto-escaping
- Sanitize with DOMPurify if HTML required
- Validate inputs with Zod/Pydantic
- Implement Content Security Policy

## A04: Insecure Design

**Risk**: Missing security controls in design phase

### Grey Haven Patterns

```typescript
// ✅ SECURE: Threat modeling for features
/**
 * Feature: User File Upload
 *
 * Threat Model:
 * - Malicious file upload → File type validation, virus scanning
 * - Path traversal → Sanitize filenames, UUID-based storage
 * - DoS via large files → Size limit (10MB), rate limiting
 * - Public exposure → Signed URLs with expiry
 */

export const uploadFile = createServerFn({ method: 'POST' })
  .handler(async ({ data }) => {
    // ✅ Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!allowedTypes.includes(data.file.type)) {
      throw new Error('Invalid file type');
    }

    // ✅ Validate file size (10MB limit)
    if (data.file.size > 10 * 1024 * 1024) {
      throw new Error('File too large');
    }

    // ✅ Generate safe filename (no path traversal)
    const fileId = crypto.randomUUID();
    const ext = data.file.name.split('.').pop();
    const safeFilename = `${fileId}.${ext}`;

    // ✅ Upload to R2 with signed URL
    const url = await uploadToR2(safeFilename, data.file);

    return { url, expiresIn: 3600 };  // 1 hour expiry
  });
```

**Prevention**:
- Threat model all features before implementation
- Security by design, not bolted on
- Least privilege principle
- Defense in depth (multiple layers)

## A05: Security Misconfiguration

**Risk**: Default configurations, unnecessary features, missing security headers

### Grey Haven Patterns

```typescript
// ✅ SECURE: Cloudflare Workers security headers
export default {
  async fetch(request: Request, env: Env) {
    const response = await handleRequest(request, env);

    // ✅ Security headers
    response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('X-XSS-Protection', '1; mode=block');
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

    // ✅ Content Security Policy
    response.headers.set('Content-Security-Policy', [
      "default-src 'self'",
      "script-src 'self' 'wasm-unsafe-eval'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' https: data:",
      "connect-src 'self' https://api.greyhaven.io",
      "frame-ancestors 'none'"
    ].join('; '));

    return response;
  }
};

// ✅ PostgreSQL hardening
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_statement = 'all';
```

**Prevention**:
- Implement all security headers (CSP, HSTS, etc.)
- Disable directory listing
- Remove default accounts
- Enable PostgreSQL audit logging
- Regular security configuration reviews

## A06: Vulnerable and Outdated Components

**Risk**: Using dependencies with known CVEs

### Grey Haven Patterns

```bash
# ✅ SECURE: Regular dependency auditing
bun audit  # Weekly
pip-audit  # Weekly

# Automated updates
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Prevention**:
- Run `bun audit` and `pip-audit` weekly
- Enable Dependabot for automated updates
- Use lock files (bun.lockb, requirements.txt)
- Monitor Snyk/GitHub Security Advisories
- Minimize dependencies

## A07: Identification and Authentication Failures

**Risk**: Broken authentication, weak passwords, missing MFA

### Grey Haven Patterns

```typescript
// ✅ SECURE: better-auth with MFA
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  emailAndPassword: {
    minPasswordLength: 12,  // ✅ OWASP recommendation
    requireEmailVerification: true
  },

  plugins: [
    twoFactor({
      issuer: "Grey Haven",
      backupCodes: { enabled: true, amount: 8 }
    })
  ],

  session: {
    expiresIn: 60 * 60 * 24 * 7,  // 7 days
  },

  rateLimit: {
    enabled: true,
    window: 60,  // 1 minute
    max: 5       // 5 attempts
  }
});
```

**Prevention**:
- Use better-auth (production-ready)
- Require MFA for admin accounts
- Enforce password complexity (12+ chars)
- Implement rate limiting (5 attempts/minute)
- Session expiry after inactivity

## A08: Software and Data Integrity Failures

**Risk**: Insecure CI/CD, unsigned updates, deserialization attacks

### Grey Haven Patterns

```yaml
# ✅ SECURE: GitHub Actions with security
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # ✅ OIDC

    steps:
      - uses: actions/checkout@v4

      - name: Security scan
        run: |
          bun audit
          gitleaks detect

      - name: Deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: bun run deploy
```

**Prevention**:
- Sign commits (GPG keys)
- Verify package integrity (lock files)
- Scan code in CI/CD pipeline
- Use OIDC for GitHub Actions
- Validate checksums for downloads

## A09: Security Logging and Monitoring Failures

**Risk**: Insufficient logging, no alerting, delayed breach detection

### Grey Haven Patterns

```typescript
// ✅ SECURE: Structured logging with DataDog
import { logger } from '@/lib/logger';

export const loginHandler = async (req: Request) => {
  const { username, success, error } = await attemptLogin(req);

  // ✅ Security event logging
  logger.security({
    event: 'login_attempt',
    username,
    success,
    ip: req.headers.get('CF-Connecting-IP'),
    userAgent: req.headers.get('User-Agent'),
    timestamp: new Date().toISOString(),
    error: error?.message
  });

  // ✅ Alert on anomalies
  if (!success) {
    await checkForBruteForce(username, req.headers.get('CF-Connecting-IP'));
  }
};
```

**Prevention**:
- Log all authentication events
- Monitor for brute force attacks
- Alert on privilege escalation
- Centralized logging (DataDog/Sentry)
- Retain logs for 90+ days

## A10: Server-Side Request Forgery (SSRF)

**Risk**: Application fetches attacker-controlled URL

### Grey Haven Patterns

```typescript
// ✅ SECURE: URL validation and allowlisting
const ALLOWED_DOMAINS = ['api.greyhaven.io', 'cdn.greyhaven.io'];

export const fetchExternal = createServerFn({ method: 'POST' })
  .handler(async ({ data }) => {
    // ✅ Validate URL
    let url: URL;
    try {
      url = new URL(data.url);
    } catch {
      throw new Error('Invalid URL');
    }

    // ✅ Block private IPs
    const privateIPRanges = [
      /^10\./,
      /^172\.(1[6-9]|2[0-9]|3[01])\./,
      /^192\.168\./,
      /^127\./,
      /^169\.254\./  // AWS metadata
    ];

    if (privateIPRanges.some(range => range.test(url.hostname))) {
      throw new Error('Private IP blocked');
    }

    // ✅ Allowlist domains
    if (!ALLOWED_DOMAINS.includes(url.hostname)) {
      throw new Error('Domain not allowed');
    }

    return await fetch(url.toString());
  });
```

**Prevention**:
- Validate and sanitize URLs
- Block private IP ranges (10.0.0.0/8, 192.168.0.0/16, etc.)
- Allowlist allowed domains
- Disable URL redirects
- Use Cloudflare egress filtering

## Summary Table

| Category | Key Risk | Grey Haven Control | Priority |
|----------|----------|-------------------|----------|
| **A01: Access Control** | Multi-tenant leak | PostgreSQL RLS | Critical |
| **A02: Crypto Failures** | Secret exposure | Doppler + Argon2id | Critical |
| **A03: Injection** | SQL injection | Drizzle ORM | Critical |
| **A04: Insecure Design** | Missing controls | Threat modeling | High |
| **A05: Misconfiguration** | Missing headers | CSP + HSTS | High |
| **A06: Vulnerable Components** | CVEs | bun audit | High |
| **A07: Auth Failures** | Weak auth | better-auth + MFA | Critical |
| **A08: Integrity Failures** | Unsigned code | CI/CD scanning | Medium |
| **A09: Logging Failures** | No monitoring | DataDog logging | High |
| **A10: SSRF** | Cloud metadata | URL validation | Medium |

**Compliance Mapping**: See [compliance-requirements.md](compliance-requirements.md)

---

**Related**: [CVSS Scoring](cvss-scoring.md) | [Security Tools](security-tools.md) | **Index**: [Reference Index](INDEX.md)
