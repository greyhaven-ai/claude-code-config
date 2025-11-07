## Summary

[2-4 sentences describing what was added and why]

## Motivation

[Explain the problem being solved and business value]

- **Problem**: [Describe user pain point or business need]
- **Impact**: [Expected user/business benefit]
- **Linear Issue**: GREY-XXX

## Implementation Details

### Key Changes
- **[Component/Module]**: [What changed]
- **[Database/Schema]**: [Schema changes with snake_case, tenant_id]
- **[Routes/API]**: [New endpoints or routes]

### Design Decisions
- **Decision 1**: [Rationale]
- **Decision 2**: [Rationale]

### Multi-Tenant Considerations
- tenant_id filtering in [location]
- RLS policies on [tables]
- Tested with multiple tenants

## Testing

### Automated Tests
- **Unit tests** (X new): [What's tested]
- **Integration tests** (X new): [What's tested]
- **E2e tests** (X new): [What's tested]

### Manual Testing
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Coverage
- New code: X% coverage
- Critical paths: 100% coverage

## Checklist
- [ ] Code follows Grey Haven style guidelines
- [ ] Type hints added/maintained
- [ ] Tests added/updated (80%+ coverage)
- [ ] Database migrations tested
- [ ] Multi-tenant isolation verified
- [ ] Pre-commit hooks passing
- [ ] Documentation updated
- [ ] No breaking changes
