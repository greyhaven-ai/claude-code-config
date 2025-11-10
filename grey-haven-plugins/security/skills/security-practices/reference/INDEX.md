# Security Practices Reference

Complete technical reference for Grey Haven security standards and practices.

## Reference Materials

1. **[OWASP Top 10 for Grey Haven Stack](owasp-top-10.md)** - Vulnerability prevention
   - A01: Broken Access Control
   - A02: Cryptographic Failures
   - A03: Injection
   - A04: Insecure Design
   - A05: Security Misconfiguration
   - A06: Vulnerable Components
   - A07: Authentication Failures
   - A08: Data Integrity Failures
   - A09: Logging Failures
   - A10: Server-Side Request Forgery

2. **[Security Configuration](security-configuration.md)** - Complete settings guide
   - Authentication configuration
   - Session management
   - CORS settings
   - Rate limiting config
   - Environment variables

3. **[Secret Management](secret-management.md)** - Doppler integration guide
   - Required secrets
   - Doppler CLI reference
   - Access patterns
   - Rotation procedures

4. **[Multi-Tenant Security](multi-tenant-security.md)** - Tenant isolation patterns
   - RLS policies
   - Query patterns
   - Testing strategies
   - Common pitfalls

## Quick Links

- For examples: See [examples/](../examples/INDEX.md)
- For checklists: See [checklists/](../checklists/)
- For templates: See [templates/](../templates/)

---

**Coverage**: OWASP Top 10, Configuration, Secrets, Multi-tenancy
**Last Updated**: 2025-11-09
