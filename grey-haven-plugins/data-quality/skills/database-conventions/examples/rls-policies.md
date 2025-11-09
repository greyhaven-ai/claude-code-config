# Row Level Security Examples

**RLS policy patterns for multi-tenant isolation.**

## Enable RLS

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

## Tenant Isolation Policy

```sql
CREATE POLICY "tenant_isolation" ON users
  FOR ALL TO authenticated
  USING (tenant_id = (current_setting('request.jwt.claims')::json->>'tenant_id')::uuid);
```

## Admin Override Policy

```sql
CREATE POLICY "admin_access" ON users
  FOR ALL TO admin
  USING (true);
```

**See [../reference/rls-policies.md](../reference/rls-policies.md) for complete RLS guide.**
