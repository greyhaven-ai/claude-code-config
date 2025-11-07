# Migration Checklist

**Use before applying database migrations.**

## Before Migration

- [ ] Backup database
- [ ] Test migration in development
- [ ] Test migration rollback
- [ ] Review generated SQL
- [ ] Check for breaking changes
- [ ] Coordinate with team if breaking

## Migration Quality

- [ ] Migration is reversible (has downgrade)
- [ ] No data loss
- [ ] Preserves existing data
- [ ] Handles NULL values correctly
- [ ] Default values provided for NOT NULL

## After Migration

- [ ] Migration applied successfully
- [ ] Application tested
- [ ] Rollback tested
- [ ] Performance verified
- [ ] No errors in logs
