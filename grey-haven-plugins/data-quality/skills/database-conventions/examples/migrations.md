# Migration Examples

**Migration patterns for Drizzle (TypeScript) and Alembic (Python).**

## Drizzle Migrations (TypeScript)

```bash
# Generate migration
bun run drizzle-kit generate:pg

# Apply migration
bun run drizzle-kit push:pg

# Check migration status
bun run drizzle-kit check:pg
```

## Alembic Migrations (Python)

```bash
# Generate migration
alembic revision --autogenerate -m "Add users table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

**See [../reference/migrations.md](../reference/migrations.md) for complete setup.**
