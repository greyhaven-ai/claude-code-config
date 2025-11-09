# Pull Request Checklist

**Use before requesting PR review.**

## Code Quality

- [ ] Code follows Grey Haven style guidelines (90 char TS, 130 char Python)
- [ ] Type hints added (Python) or types maintained (TypeScript)
- [ ] No console.log or print statements (except intentional logging)
- [ ] Variable and function names are descriptive
- [ ] Comments explain **why**, not **what**

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated (if applicable)
- [ ] E2e tests added/updated (if applicable)
- [ ] Test coverage meets 80% threshold
- [ ] Manual testing completed
- [ ] Edge cases tested

## Database (if applicable)

- [ ] Migrations tested (up and down)
- [ ] snake_case field names used
- [ ] tenant_id included with RLS policies
- [ ] Indexes added for foreign keys
- [ ] Migration includes rollback strategy

## Multi-Tenant (if applicable)

- [ ] tenant_id filtering in all queries
- [ ] RLS policies created/updated
- [ ] Tenant isolation verified with tests
- [ ] JWT claims include tenant_id

## Documentation

- [ ] README updated (if needed)
- [ ] API documentation updated (if applicable)
- [ ] Inline code comments added for complex logic
- [ ] Migration guide provided (if breaking changes)

## Pre-Commit

- [ ] Pre-commit hooks passing
- [ ] Prettier/Ruff formatting applied
- [ ] ESLint/mypy checks passing
- [ ] Virtual environment activated (Python projects)

## Pull Request Description

- [ ] Summary: 2-4 sentences describing changes
- [ ] Motivation: Why changes are needed
- [ ] Implementation: Technical approach with file references
- [ ] Testing: Automated and manual testing steps
- [ ] Linear issue referenced (GREY-123)
- [ ] Breaking changes documented (if any)

## Security

- [ ] No sensitive data in code (passwords, keys, tokens)
- [ ] Input validation implemented
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (proper escaping)
- [ ] Rate limiting considered (if API changes)

## Final Checks

- [ ] Commit messages follow commitlint format
- [ ] No merge conflicts
- [ ] Branch is up to date with main
- [ ] All checklist items completed
