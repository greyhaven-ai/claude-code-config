# API Design Checklist

**Use this checklist before creating PR for new API endpoints.**

## RESTful Design

- [ ] URLs use plural nouns (`/users` not `/user`)
- [ ] URLs use lowercase with hyphens (`/user-profiles` not `/userProfiles`)
- [ ] No verbs in URLs (`/users` not `/getUsers`)
- [ ] Hierarchical resources follow pattern `/parent/{id}/child`
- [ ] HTTP verbs used correctly (GET=read, POST=create, PUT=update, DELETE=delete)

## Multi-Tenant Isolation

- [ ] All queries filtered by `tenant_id` from JWT
- [ ] Repository pattern used with automatic tenant filtering
- [ ] No direct database queries bypassing repository
- [ ] Cross-tenant access blocked (except superuser endpoints)
- [ ] Test cases verify tenant isolation

## Request/Response Schemas

- [ ] Pydantic schemas defined for all requests
- [ ] Pydantic schemas defined for all responses
- [ ] Password hashes never returned in responses
- [ ] Sensitive fields excluded from public schemas
- [ ] Validation rules enforced (min/max length, format, etc.)
- [ ] Field-level validation implemented where needed
- [ ] Model-level validation for cross-field rules

## HTTP Status Codes

- [ ] 200 OK for successful GET/PUT/PATCH
- [ ] 201 Created for successful POST
- [ ] 204 No Content for successful DELETE
- [ ] 400 Bad Request for invalid data
- [ ] 401 Unauthorized for missing/invalid auth
- [ ] 403 Forbidden for insufficient permissions
- [ ] 404 Not Found for missing resources
- [ ] 409 Conflict for duplicates
- [ ] 422 Validation Error for schema failures

## Error Handling

- [ ] Consistent error response format (`error`, `status_code`, `detail`)
- [ ] Custom exception handlers registered
- [ ] Validation errors return field-level details
- [ ] Integrity errors handled gracefully (409 Conflict)
- [ ] Generic exceptions caught and logged

## Pagination

- [ ] List endpoints support pagination (`skip`, `limit`)
- [ ] Maximum limit enforced (100 default)
- [ ] Paginated response includes `total`, `has_more`
- [ ] Cursor-based pagination for large datasets
- [ ] Pagination tested with edge cases

## Authentication

- [ ] JWT authentication required on protected endpoints
- [ ] `tenant_id` extracted from JWT claims
- [ ] Superuser flag checked for admin endpoints
- [ ] Public endpoints explicitly marked (no auth)
- [ ] Authentication tested in integration tests

## OpenAPI Documentation

- [ ] Endpoint docstrings describe purpose
- [ ] All parameters documented
- [ ] Response schemas documented
- [ ] Error responses documented (409, 422, etc.)
- [ ] Examples provided for complex schemas
- [ ] Tags assigned for logical grouping

## Rate Limiting

- [ ] Public endpoints have rate limiting
- [ ] Critical endpoints (create, update) have stricter limits
- [ ] Rate limit uses Upstash Redis
- [ ] Rate limit headers included in response

## Testing

- [ ] Unit tests for repository methods
- [ ] Integration tests for all CRUD operations
- [ ] Tenant isolation verified in tests
- [ ] Duplicate detection tested (409 Conflict)
- [ ] Validation errors tested (422 Unprocessable)
- [ ] Authentication tested (401 Unauthorized)
- [ ] Tests run with Doppler (`doppler run --config test`)

## Security

- [ ] No SQL injection vulnerabilities (using ORM)
- [ ] No hardcoded secrets or credentials
- [ ] CORS origins from Doppler (not hardcoded)
- [ ] Input validation on all fields
- [ ] Output encoding prevents XSS
- [ ] Rate limiting protects against abuse

## Performance

- [ ] Database queries use indexes
- [ ] N+1 queries avoided
- [ ] Pagination prevents loading all records
- [ ] Heavy operations use background jobs
- [ ] Caching implemented where appropriate

## Before Merging

- [ ] All tests pass (`pytest`)
- [ ] Coverage >80% for new code
- [ ] OpenAPI docs reviewed at `/docs`
- [ ] Tested locally with Doppler
- [ ] Code reviewed by teammate
- [ ] No console.log or debug prints
- [ ] Migration created if schema changed
