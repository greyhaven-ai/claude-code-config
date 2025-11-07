# API Documentation Reference

Configuration references and patterns for API documentation generation.

## Available References

### [openapi-3-1-patterns.md](openapi-3-1-patterns.md)
OpenAPI 3.1 specification patterns and best practices.
- Complete OpenAPI 3.1 schema structure
- Path item definitions (GET, POST, PUT, DELETE, PATCH)
- Parameter definitions (path, query, header, cookie)
- Request body schemas with examples
- Response schemas with status codes
- Component schemas and reusable types
- Security schemes (Bearer JWT, OAuth2, API keys)
- Webhook definitions (OpenAPI 3.1 feature)
- JSON Schema 2020-12 support

### [schema-patterns.md](schema-patterns.md)
Common schema patterns for API documentation.
- Pagination schemas (page, limit, total, hasMore)
- Error response schemas (code, message, field, details)
- Timestamp patterns (ISO 8601, Unix timestamps)
- UUID and ID patterns
- Enum definitions for status codes
- Nested object schemas
- Array schemas with constraints
- Polymorphic schemas (oneOf, anyOf, allOf)
- File upload/download schemas

### [deployment-configs.md](deployment-configs.md)
Deployment configuration for documentation sites.
- Cloudflare Pages deployment with wrangler
- GitHub Actions CI/CD workflow
- Coverage threshold configuration
- OpenAPI spec validation in CI/CD
- Multi-environment deployment (staging, production)
- Custom domain configuration
- Cache invalidation strategies
- Rollback procedures

### [validation-rules.md](validation-rules.md)
Validation rules for OpenAPI specifications.
- Required field validation
- Schema structure validation
- HTTP method validation
- Status code validation
- $ref reference validation
- Example conformance validation
- Security scheme validation
- OpenAPI 3.1 compliance checks

## Quick Reference

**Need OpenAPI patterns?** → [openapi-3-1-patterns.md](openapi-3-1-patterns.md)
**Need schema patterns?** → [schema-patterns.md](schema-patterns.md)
**Need deployment config?** → [deployment-configs.md](deployment-configs.md)
**Need validation rules?** → [validation-rules.md](validation-rules.md)
