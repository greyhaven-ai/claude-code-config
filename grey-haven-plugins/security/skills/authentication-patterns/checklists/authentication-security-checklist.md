# Authentication & Authorization Security Checklist

Comprehensive checklist for implementing secure authentication and authorization patterns with Better Auth and multi-tenant architecture.

## Pre-Implementation Planning

- [ ] **Choose authentication method** (Better Auth, custom, OAuth only)
- [ ] **Define user roles** (admin, user, viewer, etc.)
- [ ] **Map permissions** to roles
- [ ] **Choose session strategy** (JWT, database sessions, cookies)
- [ ] **Plan multi-tenant isolation** (tenant-level permissions)
- [ ] **Review compliance requirements** (GDPR, HIPAA, SOC2)

## Better Auth Setup

### Installation & Configuration

- [ ] **Better Auth installed** (`npm install better-auth`)
- [ ] **Configuration file created** (`auth.config.ts` or similar)
- [ ] **Database adapter configured** (Drizzle, Prisma, etc.)
- [ ] **Environment variables set** (secrets, URLs)
- [ ] **CSRF protection enabled** (default in Better Auth)

### OAuth Providers

- [ ] **OAuth providers configured** (Google, GitHub, etc.):
  ```typescript
  providers: [
    google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }),
    github({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    })
  ]
  ```

- [ ] **OAuth redirect URIs whitelisted** in provider dashboards
- [ ] **OAuth scopes minimal** (only request what's needed)
- [ ] **OAuth state parameter validated** (CSRF protection)
- [ ] **OAuth error handling** implemented

### Email/Password Authentication

- [ ] **Password hashing** with secure algorithm (bcrypt, Argon2)
- [ ] **Password requirements** enforced:
  - [ ] Minimum 8 characters
  - [ ] Mix of uppercase, lowercase, numbers, symbols
  - [ ] Password strength meter on frontend
  - [ ] Common password blocklist

- [ ] **Email verification** implemented:
  - [ ] Verification email sent on registration
  - [ ] Token expires after reasonable time (24 hours)
  - [ ] User cannot access protected routes until verified
  - [ ] Resend verification email option

- [ ] **Password reset** flow:
  - [ ] Reset link sent to email
  - [ ] Token single-use and time-limited
  - [ ] Old password invalidated after reset
  - [ ] User notified of password change

## Session Management

### Session Storage

- [ ] **Sessions stored securely**:
  - [ ] Database sessions (recommended for multi-tenant)
  - [ ] Encrypted session cookies
  - [ ] No sensitive data in localStorage

- [ ] **Session expiration** configured:
  - [ ] Reasonable timeout (30 minutes idle, 24 hours absolute)
  - [ ] Refresh token flow (if using JWT)
  - [ ] Grace period for session extension

- [ ] **Session invalidation** on:
  - [ ] Logout
  - [ ] Password change
  - [ ] Security event (suspicious activity)
  - [ ] User deletion

### Session Security

- [ ] **httpOnly cookies** (JavaScript cannot access)
- [ ] **secure flag** set (HTTPS only)
- [ ] **sameSite attribute** configured (Strict or Lax)
- [ ] **Session fixation prevented** (regenerate session ID on login)
- [ ] **Concurrent session management** (limit sessions per user)

## Multi-Tenant Authentication

### Tenant Context

- [ ] **Tenant identified** during authentication:
  - [ ] From subdomain (`tenant.example.com`)
  - [ ] From custom domain (`example.com`)
  - [ ] From user selection (post-login)
  - [ ] From invitation link

- [ ] **tenant_id stored** in session
- [ ] **User-tenant relationship** verified on each request
- [ ] **Tenant switching** requires re-authentication (or explicit action)
- [ ] **Cross-tenant access blocked** at authentication layer

### Organization Roles

- [ ] **Organization model** defined (one tenant = one org)
- [ ] **User-Organization membership** table created
- [ ] **Roles per organization**:
  - [ ] Owner (full control)
  - [ ] Admin (manage users, cannot delete org)
  - [ ] Member (standard access)
  - [ ] Viewer (read-only)

- [ ] **Role inheritance** (Owner has all Admin permissions)
- [ ] **Role assignment** restricted (only Owner/Admin can assign roles)

### Invitation System

- [ ] **Invitation flow** implemented:
  - [ ] Admin generates invitation link
  - [ ] Link includes tenant_id + role
  - [ ] Link expires after set time
  - [ ] Link single-use or limited-use
  - [ ] Email sent with invitation

- [ ] **Invitation acceptance** creates user-tenant relationship
- [ ] **Invitation revocation** possible before acceptance
- [ ] **Pending invitations** tracked in database

## Authorization Patterns

### Role-Based Access Control (RBAC)

- [ ] **Roles defined** at application level
- [ ] **Permissions mapped** to roles
- [ ] **Permission checks** in:
  - [ ] API route handlers
  - [ ] Repository methods (data access layer)
  - [ ] UI components (hide/disable unauthorized actions)

- [ ] **Authorization middleware** created:
  ```typescript
  function requireRole(role: Role) {
    return async (req, res, next) => {
      const user = req.user;
      if (!user || user.role !== role) {
        return res.status(403).json({ error: 'Forbidden' });
      }
      next();
    };
  }
  ```

### Attribute-Based Access Control (ABAC)

- [ ] **User attributes** checked (tenant_id, role, team_id)
- [ ] **Resource attributes** checked (owner_id, tenant_id, visibility)
- [ ] **Context attributes** checked (time, IP, device)
- [ ] **Policy evaluation** centralized (authorization service)

### Row-Level Security (RLS)

- [ ] **RLS policies enabled** on multi-tenant tables:
  ```sql
  CREATE POLICY tenant_isolation ON users
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
  ```

- [ ] **tenant_id set** in database context for each request
- [ ] **Admin bypass** policy (when needed):
  ```sql
  CREATE POLICY admin_all_access ON users
  USING (
    current_setting('app.user_role') = 'admin'
    OR tenant_id = current_setting('app.tenant_id')::uuid
  );
  ```

- [ ] **RLS tested** (cannot access other tenant's data)

## API Security

### Authentication Endpoints

- [ ] **Rate limiting** on auth endpoints:
  - [ ] Login: 5 attempts per 15 minutes
  - [ ] Registration: 3 accounts per hour per IP
  - [ ] Password reset: 3 requests per hour per email

- [ ] **Brute force protection**:
  - [ ] Account lockout after failed attempts
  - [ ] CAPTCHA after 3 failed attempts
  - [ ] Delay responses on failure (same time as success)

- [ ] **Account enumeration prevented**:
  - [ ] Same response for existing/non-existing users
  - [ ] Generic error messages ("Invalid credentials")

### Protected Endpoints

- [ ] **Authentication required** (middleware on all protected routes)
- [ ] **Authorization verified** (role/permission checks)
- [ ] **tenant_id validated** (user belongs to tenant)
- [ ] **Input validation** (Zod/Pydantic on all inputs)
- [ ] **CORS configured** (whitelist allowed origins)

### Token Security

- [ ] **JWT tokens** (if used):
  - [ ] Short expiration (15 minutes for access token)
  - [ ] Signed with secret key (HS256 or RS256)
  - [ ] Claims validated (iss, aud, exp)
  - [ ] Refresh token rotation
  - [ ] Refresh token revocation on logout

- [ ] **API keys** (if used):
  - [ ] Stored hashed in database
  - [ ] Scoped to specific tenant
  - [ ] Can be revoked
  - [ ] Expiration date set
  - [ ] Usage tracked (rate limits per key)

## Frontend Security

### Client-Side Auth

- [ ] **Auth state managed** (React context, store)
- [ ] **Protected routes** implemented:
  ```typescript
  function ProtectedRoute({ children }) {
    const { user, loading } = useAuth();
    if (loading) return <Loading />;
    if (!user) return <Navigate to="/login" />;
    return children;
  }
  ```

- [ ] **Role-based UI** (hide/disable unauthorized actions)
- [ ] **Token refresh** handled automatically
- [ ] **Logout on 401** responses

### Secure Storage

- [ ] **No sensitive data** in localStorage:
  - [ ] No passwords
  - [ ] No full credit card numbers
  - [ ] No SSNs or PII

- [ ] **Session storage** for temporary data only
- [ ] **Cookies** for authentication tokens (httpOnly)

### CSRF Protection

- [ ] **CSRF tokens** on state-changing requests
- [ ] **SameSite cookies** (Strict or Lax)
- [ ] **Referer header** validation (optional defense in depth)

## Password Security

### Password Storage

- [ ] **Never store plaintext** passwords
- [ ] **Use bcrypt or Argon2** (not SHA-256 or MD5)
- [ ] **Salt per password** (automatic with bcrypt/Argon2)
- [ ] **Cost factor appropriate** (10-12 for bcrypt)
- [ ] **Pepper used** (additional application-wide secret)

### Password Policies

- [ ] **Minimum length** 8 characters (12+ recommended)
- [ ] **Complexity requirements** (optional, often counterproductive)
- [ ] **Password history** (prevent reuse of last 5 passwords)
- [ ] **Password expiration** (only if required by compliance)
- [ ] **Compromised password check** (Have I Been Pwned API)

## Social Engineering Prevention

- [ ] **Email verification** required before account activation
- [ ] **Suspicious activity alerts**:
  - [ ] Login from new device
  - [ ] Login from new location
  - [ ] Password change
  - [ ] Email change
  - [ ] Role change

- [ ] **Security questions** avoided (weak authentication)
- [ ] **2FA encouraged** (optional or required)
- [ ] **Account recovery** requires multiple factors (email + SMS)

## Two-Factor Authentication (2FA)

- [ ] **2FA supported** (TOTP, SMS, or hardware keys)
- [ ] **2FA enrollment** flow:
  - [ ] User scans QR code (TOTP)
  - [ ] User verifies code to confirm setup
  - [ ] Backup codes generated
  - [ ] 2FA cannot be disabled without authentication

- [ ] **2FA enforcement** (optional or required):
  - [ ] Required for admins
  - [ ] Optional for users
  - [ ] Grace period for enrollment (7 days)

- [ ] **Backup codes** provided (10 single-use codes)
- [ ] **2FA recovery** flow (if device lost)

## Logging & Monitoring

### Authentication Events

- [ ] **Log all auth events**:
  - [ ] Successful logins (user, tenant, IP, timestamp)
  - [ ] Failed login attempts
  - [ ] Logout events
  - [ ] Password changes
  - [ ] Role changes
  - [ ] 2FA enrollment/removal

- [ ] **Structured logging** (JSON format for parsing)
- [ ] **PII handling** in logs (hash or redact sensitive data)
- [ ] **Log retention** policy (90 days minimum for security events)

### Anomaly Detection

- [ ] **Monitor for**:
  - [ ] Multiple failed logins from same IP
  - [ ] Login from unusual location
  - [ ] Rapid API requests (potential bot)
  - [ ] Privilege escalation attempts
  - [ ] Mass data access (potential breach)

- [ ] **Alerts configured** for suspicious activity
- [ ] **Automated responses** (account lock, CAPTCHA)
- [ ] **Security team notified** for critical events

## Compliance & Privacy

### GDPR Compliance

- [ ] **Consent captured** for data processing
- [ ] **Privacy policy** accessible
- [ ] **Right to access** (users can export data)
- [ ] **Right to deletion** (users can delete account)
- [ ] **Data minimization** (only collect necessary data)
- [ ] **Breach notification** process defined

### SOC2 Requirements

- [ ] **Access logging** comprehensive
- [ ] **Session management** secure
- [ ] **Encryption** in transit (HTTPS) and at rest
- [ ] **MFA available** for privileged accounts
- [ ] **Security training** for developers

## Testing Authentication

### Unit Tests

- [ ] **Password hashing** tested
- [ ] **Token generation/validation** tested
- [ ] **Permission checks** tested
- [ ] **Role assignment** tested
- [ ] **Tenant isolation** tested

### Integration Tests

- [ ] **Login flow** tested (email/password, OAuth)
- [ ] **Registration flow** tested
- [ ] **Password reset** tested
- [ ] **Session expiration** tested
- [ ] **2FA flow** tested

### Security Tests

- [ ] **Penetration testing** performed
- [ ] **OWASP Top 10** vulnerabilities checked:
  - [ ] Broken authentication
  - [ ] SQL injection
  - [ ] XSS
  - [ ] CSRF
  - [ ] Security misconfiguration

- [ ] **Automated security scans** (SAST, DAST)
- [ ] **Dependency vulnerabilities** checked (npm audit, Snyk)

## Deployment Security

- [ ] **Secrets management** (Doppler, AWS Secrets Manager)
- [ ] **Environment variables** not committed to git
- [ ] **HTTPS enforced** (redirect HTTP to HTTPS)
- [ ] **Security headers** set:
  - [ ] Strict-Transport-Security
  - [ ] X-Content-Type-Options
  - [ ] X-Frame-Options
  - [ ] Content-Security-Policy

- [ ] **Database encryption** at rest
- [ ] **Backup encryption**
- [ ] **Secure key rotation** process

## Incident Response

- [ ] **Incident response plan** documented
- [ ] **Security contacts** defined
- [ ] **Breach notification** process:
  - [ ] Identify affected users
  - [ ] Notify within 72 hours (GDPR)
  - [ ] Invalidate all sessions
  - [ ] Force password reset
  - [ ] Investigate root cause

- [ ] **Post-incident review** process
- [ ] **Security patches** deployment process

## Scoring

- **90+ items checked**: Excellent - Production-ready security ✅
- **70-89 items**: Good - Most security covered ⚠️
- **50-69 items**: Fair - Significant security gaps 🔴
- **<50 items**: Poor - Not secure for production ❌

## Priority Items

Address these first:
1. **Password security** - Hashing, policies, reset flow
2. **Session management** - Secure storage, expiration, invalidation
3. **Multi-tenant isolation** - tenant_id in session, RLS policies
4. **Rate limiting** - Prevent brute force attacks
5. **Logging** - Audit trail for security events

## Common Mistakes

❌ **Don't:**
- Store passwords in plaintext or with weak hashing
- Use long-lived tokens without refresh mechanism
- Trust client-side validation/authorization
- Share sessions across tenants
- Log passwords or tokens
- Use JWT for sessions (use database sessions for multi-tenant)

✅ **Do:**
- Use proven auth libraries (Better Auth, NextAuth)
- Validate sessions on every request
- Implement defense in depth (multiple security layers)
- Test authentication thoroughly
- Monitor for suspicious activity
- Rotate secrets regularly

## Related Resources

- [Better Auth Documentation](https://better-auth.com)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [authentication-patterns skill](../SKILL.md)

---

**Total Items**: 150+ security checks
**Critical Items**: Password security, Session management, Multi-tenant, Rate limiting
**Coverage**: Better Auth, Multi-tenant, OAuth, RBAC, RLS
**Last Updated**: 2025-11-10
