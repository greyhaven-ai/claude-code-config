# Security Audit Checklist

Use this checklist before deploying Grey Haven applications to production.

## Secret Management

- [ ] **NO secrets committed to git** (check with `git log -p | grep -E "sk-|api_key|secret"`)
- [ ] All secrets managed through Doppler
- [ ] Development config uses dev secrets (Doppler dev)
- [ ] Production config uses prod secrets (Doppler production)
- [ ] No `.env` files committed
- [ ] `.env.example` documents required variables

## Authentication & Authorization

- [ ] Sessions use secure, httpOnly cookies
- [ ] sameSite="lax" or "strict" set on session cookies
- [ ] Passwords require min 12 characters
- [ ] Passwords validated for complexity (uppercase, lowercase, number, special char)
- [ ] Failed login attempts rate-limited
- [ ] Session expiry configured (max 7 days)
- [ ] Logout properly invalidates sessions

## Multi-Tenant Isolation

- [ ] RLS enabled on ALL multi-tenant tables
- [ ] `tenant_id` field on ALL multi-tenant tables
- [ ] ALL queries filter by tenant_id
- [ ] No direct SQL queries (use ORM)
- [ ] Tenant isolation tested (cannot access other tenant's data)
- [ ] Admin operations respect tenant boundaries

## Input Validation

- [ ] ALL user input validated (Zod for TS, Pydantic for Python)
- [ ] Email addresses validated
- [ ] Numeric inputs have min/max constraints
- [ ] String inputs have length limits
- [ ] File uploads validate type AND content
- [ ] File upload size limits enforced (5MB default)

## Output Sanitization

- [ ] React JSX used for HTML rendering (auto-escapes)
- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] DOMPurify used if HTML rendering needed
- [ ] API responses don't include sensitive data
- [ ] Error messages don't leak implementation details

## SQL Injection Prevention

- [ ] Drizzle ORM used for all database queries (TypeScript)
- [ ] SQLModel used for all database queries (Python)
- [ ] NO raw SQL string concatenation
- [ ] Parameterized queries ONLY
- [ ] Database migrations reviewed for security

## XSS Prevention

- [ ] Content-Security-Policy header configured
- [ ] No inline JavaScript in HTML
- [ ] No eval() or similar dangerous functions
- [ ] User-generated content sanitized before display
- [ ] File uploads don't allow HTML/JavaScript

## CSRF Protection

- [ ] sameSite cookies enabled
- [ ] CSRF tokens on state-changing operations (if needed)
- [ ] Origin header validation
- [ ] Double-submit cookie pattern (if applicable)

## CORS Configuration

- [ ] CORS origins explicitly whitelisted
- [ ] NO wildcard CORS origin in production
- [ ] credentials: true only for trusted origins
- [ ] Preflight requests handled correctly

## Rate Limiting

- [ ] Login endpoint rate-limited (10 attempts/hour)
- [ ] Email send rate-limited (10 emails/hour per user)
- [ ] API endpoints rate-limited (100 req/min per IP)
- [ ] Expensive operations rate-limited
- [ ] Rate limit headers returned (X-RateLimit-*)

## HTTPS/TLS

- [ ] HTTPS enforced in production
- [ ] HTTP redirects to HTTPS
- [ ] Strict-Transport-Security header set (HSTS)
- [ ] Valid TLS certificate
- [ ] TLS 1.2+ only (no TLS 1.0/1.1)

## Headers Security

- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] X-Content-Type-Options: nosniff
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Referrer-Policy: strict-origin-when-cross-origin
- [ ] Permissions-Policy configured

## Error Handling

- [ ] Production errors don't leak stack traces
- [ ] Errors logged server-side only
- [ ] Generic error messages to users
- [ ] Sentry/logging configured for production
- [ ] No sensitive data in error messages

## Database Security

- [ ] Database credentials rotated regularly
- [ ] Database uses TLS connection
- [ ] Separate database users for dev/prod
- [ ] Database backups encrypted
- [ ] PII encrypted at rest (if applicable)

## File Upload Security

- [ ] File type validation (MIME type + magic numbers)
- [ ] File size limits enforced
- [ ] Uploaded files scanned for malware
- [ ] Files stored outside web root
- [ ] Random filenames generated (prevent path traversal)
- [ ] Upload endpoint requires authentication

## Dependencies

- [ ] No high/critical vulnerabilities (npm audit, pip-audit)
- [ ] Dependencies up to date
- [ ] Dependabot/Renovate configured
- [ ] Package-lock.json / poetry.lock committed
- [ ] Unused dependencies removed

## Logging & Monitoring

- [ ] Security events logged (failed logins, permission changes)
- [ ] Logs don't contain sensitive data (passwords, tokens)
- [ ] Anomaly detection configured
- [ ] Alerts for suspicious activity
- [ ] Audit trail for admin actions

## Testing

- [ ] Security tests written and passing
- [ ] Tenant isolation tested
- [ ] Rate limiting tested
- [ ] Input validation tested
- [ ] Authentication flows tested
- [ ] Permission boundaries tested

## Compliance (if applicable)

- [ ] GDPR compliance verified (EU users)
- [ ] CCPA compliance verified (CA users)
- [ ] SOC 2 requirements met
- [ ] HIPAA compliance (if healthcare)
- [ ] Data retention policies implemented

## Scoring

- **45+ items checked**: Excellent - Production ready ✅
- **35-44 items**: Good - Minor gaps to address ⚠️
- **25-34 items**: Fair - Significant security work needed 🔴
- **<25 items**: Poor - NOT production ready ❌

## Next Steps

If score < 45:
1. Address all unchecked critical items (secrets, RLS, input validation)
2. Run `npm audit` / `pip-audit` and fix vulnerabilities
3. Test multi-tenant isolation thoroughly
4. Review OWASP Top 10 reference
5. Re-run checklist

## Related Resources

- [OWASP Top 10](../reference/owasp-top-10.md)
- [Security Configuration](../reference/security-configuration.md)
- [Examples](../examples/INDEX.md)

---

**Total Items**: 70+ security checks
**Critical Items**: Secrets, RLS, Input Validation, SQL Injection
**Last Updated**: 2025-11-09
