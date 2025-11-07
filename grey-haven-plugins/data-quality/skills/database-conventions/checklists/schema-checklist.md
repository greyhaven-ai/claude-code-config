# Database Schema Checklist

**Use before creating PR for new database schemas.**

## Naming Conventions

- [ ] All field names use snake_case (NOT camelCase)
- [ ] Boolean fields use is_/has_/can_ prefix
- [ ] Timestamp fields use _at suffix
- [ ] Foreign keys use _id suffix
- [ ] Email field named `email_address` (not `email`)
- [ ] Phone field named `phone_number` (not `phone`)

## Multi-Tenant Requirements

- [ ] tenant_id field present on all tables
- [ ] tenant_id has NOT NULL constraint
- [ ] tenant_id has index for performance
- [ ] tenant_id has foreign key to tenants table
- [ ] RLS policy created for tenant isolation
- [ ] Test cases verify tenant isolation

## Standard Fields

- [ ] id field (UUID primary key)
- [ ] created_at timestamp (NOT NULL, default now())
- [ ] updated_at timestamp (NOT NULL, auto-update)
- [ ] tenant_id (NOT NULL, indexed)
- [ ] deleted_at timestamp (for soft delete)

## Indexes

- [ ] tenant_id indexed
- [ ] Foreign keys indexed
- [ ] Unique fields indexed
- [ ] Frequently queried fields indexed
- [ ] Composite indexes for common query patterns

## Relationships

- [ ] Foreign keys defined explicitly
- [ ] Relationships documented in schema
- [ ] Cascade delete configured appropriately
- [ ] Join tables for many-to-many

## Migrations

- [ ] Migration generated (Drizzle Kit or Alembic)
- [ ] Migration tested locally
- [ ] Migration reversible (has downgrade)
- [ ] Migration reviewed by teammate
- [ ] No breaking changes without coordination

## Row Level Security

- [ ] RLS enabled on table
- [ ] Tenant isolation policy created
- [ ] Admin override policy (if needed)
- [ ] Anonymous policy (if public data)
- [ ] RLS tested with different roles

## Performance

- [ ] Appropriate indexes created
- [ ] No N+1 query patterns
- [ ] Large text fields use TEXT (not VARCHAR)
- [ ] Consider partitioning for large tables

## Security

- [ ] No sensitive data in plain text
- [ ] Passwords hashed (never store plain)
- [ ] PII properly handled
- [ ] Input validation at model level
- [ ] SQL injection prevented (using ORM)

## Testing

- [ ] Model tests written
- [ ] Migration tested
- [ ] Relationships tested
- [ ] Tenant isolation tested
- [ ] Unique constraints tested
- [ ] Foreign key constraints tested

## Documentation

- [ ] Schema documented in code comments
- [ ] README updated if needed
- [ ] ERD diagram updated (if exists)
- [ ] Migration notes added
