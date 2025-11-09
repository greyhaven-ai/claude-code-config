# Indexing Strategies

**Always index:**
- tenant_id
- Foreign keys
- Unique constraints
- Frequently queried fields

**Composite indexes:**
```typescript
index("users_tenant_email_idx").on(users.tenant_id, users.email_address)
```
