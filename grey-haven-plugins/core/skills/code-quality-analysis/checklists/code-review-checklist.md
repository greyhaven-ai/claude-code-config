# Code Quality Review Checklist

Systematic code review checklist covering security, clarity, performance, and maintainability.

## Security Review

### Input Validation
- [ ] All user input validated (Zod for TS, Pydantic for Python)
- [ ] Email addresses validated with proper format
- [ ] Numeric inputs have min/max bounds
- [ ] String inputs have length limits
- [ ] Arrays have maximum size constraints

### SQL Injection Prevention
- [ ] No raw SQL string concatenation
- [ ] ORM used for all queries (Drizzle, SQLModel)
- [ ] Parameterized queries only
- [ ] No dynamic table/column names from user input

### XSS Prevention
- [ ] React JSX used for rendering (auto-escapes)
- [ ] No dangerouslySetInnerHTML without DOMPurify
- [ ] API responses don't include executable code
- [ ] User content sanitized before display

### Authentication & Authorization
- [ ] Authentication required on protected routes
- [ ] Authorization checks present
- [ ] Multi-tenant: tenant_id checked in all queries
- [ ] No privilege escalation possible

### Secret Management
- [ ] No secrets hardcoded
- [ ] Doppler used for all secrets
- [ ] No .env files committed
- [ ] Secrets not logged

## Clarity & Readability

### Naming
- [ ] Variables have descriptive names
- [ ] Functions named with verbs (getUserById, calculateTotal)
- [ ] Boolean variables prefixed (isValid, hasAccess)
- [ ] Constants in UPPER_SNAKE_CASE
- [ ] Database fields in snake_case

### Function Complexity
- [ ] Functions are < 50 lines
- [ ] Functions do one thing (Single Responsibility)
- [ ] Cyclomatic complexity < 10
- [ ] No deeply nested conditionals (max 3 levels)
- [ ] Early returns used to reduce nesting

### Comments & Documentation
- [ ] Complex logic has explanatory comments
- [ ] JSDoc/docstrings on public functions
- [ ] No commented-out code
- [ ] TODOs tracked in issue system
- [ ] README updated if public API changed

### Code Structure
- [ ] Similar code grouped together
- [ ] Related functions in same file/module
- [ ] Proper separation of concerns
- [ ] No circular dependencies
- [ ] File organization follows conventions

## Performance

### Database Queries
- [ ] No N+1 queries
- [ ] Appropriate indexes exist
- [ ] Queries limited (pagination implemented)
- [ ] Eager loading used where appropriate
- [ ] Database connection pooling configured

### Algorithms
- [ ] Appropriate data structures chosen
- [ ] Time complexity acceptable (avoid O(n²) if possible)
- [ ] No unnecessary iterations
- [ ] Efficient string operations (avoid concatenation in loops)

### Memory
- [ ] No memory leaks (event listeners removed)
- [ ] Large objects not held in memory unnecessarily
- [ ] Streams used for large files
- [ ] Caches have eviction policies

### Network
- [ ] API calls batched where possible
- [ ] Response caching implemented
- [ ] Compression enabled
- [ ] Appropriate HTTP methods used

## Maintainability

### Error Handling
- [ ] Errors caught and handled appropriately
- [ ] Error messages are helpful
- [ ] Errors logged with context
- [ ] No swallowed exceptions
- [ ] Retry logic for transient failures

### Testing
- [ ] Unit tests exist and pass
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Integration tests for critical flows
- [ ] Test coverage > 80%

### Dependencies
- [ ] No unnecessary dependencies added
- [ ] Dependencies up to date
- [ ] No security vulnerabilities (npm audit, pip-audit)
- [ ] License compatibility checked

### Code Duplication
- [ ] No copy-pasted code
- [ ] Common logic extracted to utilities
- [ ] Shared types defined once
- [ ] No magic numbers (use constants)

## TypeScript/JavaScript Specific

### Type Safety
- [ ] No `any` types (unless Grey Haven pragmatic style)
- [ ] Proper type annotations on functions
- [ ] Interfaces/types defined for complex objects
- [ ] Discriminated unions used for variants
- [ ] Type guards implemented where needed

### React Best Practices
- [ ] Components are focused (< 250 lines)
- [ ] Props properly typed
- [ ] useEffect cleanup implemented
- [ ] Keys provided for lists
- [ ] Memoization used appropriately (useMemo, useCallback)

## Python Specific

### Type Hints
- [ ] Type hints on all functions
- [ ] Return types specified
- [ ] Complex types use typing module
- [ ] mypy passes with no errors

### Python Conventions
- [ ] PEP 8 style followed
- [ ] Docstrings on classes and functions
- [ ] Context managers used for resources
- [ ] List comprehensions used appropriately

## Deployment Readiness

### Configuration
- [ ] Environment variables documented
- [ ] Sensible defaults provided
- [ ] Different configs for dev/staging/prod
- [ ] Feature flags for risky changes

### Monitoring
- [ ] Critical operations logged
- [ ] Performance metrics tracked
- [ ] Error tracking configured
- [ ] Alerts defined for failures

### Documentation
- [ ] README updated
- [ ] API documentation current
- [ ] Migration guide if breaking changes
- [ ] Deployment notes added

## Scoring

- **90+ items checked**: Excellent - Ship it! ✅
- **75-89 items**: Good - Minor improvements needed ⚠️
- **60-74 items**: Fair - Significant work required 🔴
- **<60 items**: Poor - Not ready for review ❌

## Priority Issues

Address these first if unchecked:
1. **Security items** (SQL injection, XSS, auth)
2. **Multi-tenant isolation** (tenant_id checks)
3. **Secret management** (no hardcoded secrets)
4. **Error handling** (no swallowed exceptions)
5. **Testing** (critical paths covered)

## Related Resources

- [Security Practices](../../security-practices/SKILL.md)
- [OWASP Top 10](../../security-analysis/reference/owasp-top-10.md)
- [Code Style Guide](../../code-style/SKILL.md)
- [Performance Optimization](../../performance-optimization/SKILL.md)

---

**Total Items**: 100+ quality checks
**Critical Items**: Security, Multi-tenant, Error Handling, Testing
**Last Updated**: 2025-11-09
