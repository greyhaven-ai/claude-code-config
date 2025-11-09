# API Security Review Checklist

**Security-focused review for API endpoints.**

## Authentication & Authorization

- [ ] JWT required on all protected endpoints
- [ ] Token expiration enforced
- [ ] Superuser flag checked for admin operations
- [ ] No authentication bypass vulnerabilities
- [ ] Session management secure

## Multi-Tenant Security

- [ ] All queries filter by `tenant_id`
- [ ] No cross-tenant data leaks possible
- [ ] Repository pattern enforces isolation
- [ ] Admin endpoints verify superuser
- [ ] Test cases prove isolation

## Input Validation

- [ ] All inputs validated with Pydantic
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (output encoding)
- [ ] File uploads validated (type, size)
- [ ] Email format validated
- [ ] URL format validated
- [ ] Integer ranges validated
- [ ] String lengths validated

## Sensitive Data

- [ ] Passwords hashed with bcrypt
- [ ] Password hashes never returned
- [ ] Secrets from Doppler (not hardcoded)
- [ ] PII properly handled
- [ ] No sensitive data in logs
- [ ] No sensitive data in error messages

## Rate Limiting

- [ ] Public endpoints rate limited
- [ ] Login endpoints strictly rate limited
- [ ] Rate limit uses Redis
- [ ] Rate limit tested

## CORS

- [ ] Allowed origins from Doppler
- [ ] No `allow_origins=["*"]` in production
- [ ] Credentials allowed only for trusted origins
- [ ] Preflight requests handled

## Error Handling

- [ ] No stack traces in production responses
- [ ] Generic errors for security issues
- [ ] Detailed errors only in dev/test
- [ ] Errors logged server-side

## OWASP Top 10

- [ ] A01: Broken Access Control - ✅ Tenant isolation
- [ ] A02: Cryptographic Failures - ✅ Bcrypt, Doppler
- [ ] A03: Injection - ✅ ORM, validation
- [ ] A04: Insecure Design - ✅ Repository pattern
- [ ] A05: Security Misconfiguration - ✅ CORS, secrets
- [ ] A06: Vulnerable Components - ✅ Updated dependencies
- [ ] A07: Identification Failures - ✅ JWT, rate limiting
- [ ] A08: Integrity Failures - ✅ Input validation
- [ ] A09: Logging Failures - ✅ Error logging
- [ ] A10: SSRF - ✅ URL validation

## Before Production Deploy

- [ ] Security scan passed
- [ ] No hardcoded secrets
- [ ] Doppler secrets configured
- [ ] CORS origins configured
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Error handling tested
- [ ] Penetration test completed
