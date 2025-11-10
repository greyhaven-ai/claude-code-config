# Security Practices Examples

Real-world security implementation examples for Grey Haven's TanStack Start and FastAPI stack.

## Available Examples

1. **[Input Validation](input-validation-example.md)** - Comprehensive input validation patterns
   - Zod schemas for TypeScript
   - Pydantic models for Python
   - Common validation patterns

2. **[Multi-Tenant RLS](multi-tenant-rls-example.md)** - Row Level Security implementation
   - RLS policies for PostgreSQL
   - Tenant isolation in queries
   - Testing tenant separation

3. **[Secret Management](secret-management-example.md)** - Doppler integration
   - Setting up Doppler
   - Accessing secrets in code
   - Environment-specific configs

4. **[Rate Limiting](rate-limiting-example.md)** - Redis-based rate limiting
   - Per-user rate limits
   - Per-endpoint limits
   - Graceful degradation

## Recommended Path

**For new projects:**
1. Start with [secret-management-example.md](secret-management-example.md)
2. Implement [input-validation-example.md](input-validation-example.md)
3. Add [multi-tenant-rls-example.md](multi-tenant-rls-example.md)
4. Finish with [rate-limiting-example.md](rate-limiting-example.md)

**For security reviews:**
1. Check [multi-tenant-rls-example.md](multi-tenant-rls-example.md) for data leakage
2. Verify [input-validation-example.md](input-validation-example.md) is applied
3. Audit [secret-management-example.md](secret-management-example.md) compliance

## Quick Reference

### TypeScript/React Security
- See [input-validation-example.md](input-validation-example.md#typescript)
- See [multi-tenant-rls-example.md](multi-tenant-rls-example.md#typescript)

### Python/FastAPI Security
- See [input-validation-example.md](input-validation-example.md#python)
- See [multi-tenant-rls-example.md](multi-tenant-rls-example.md#python)

## Related Materials

- **[Security Checklist](../checklists/security-audit-checklist.md)** - Pre-deployment verification
- **[OWASP Top 10 Reference](../reference/owasp-top-10.md)** - Common vulnerabilities
- **[Configuration Guide](../reference/security-configuration.md)** - Complete settings

---

**Total Examples**: 4 comprehensive guides
**Stack Coverage**: TanStack Start + FastAPI
**Last Updated**: 2025-11-09
