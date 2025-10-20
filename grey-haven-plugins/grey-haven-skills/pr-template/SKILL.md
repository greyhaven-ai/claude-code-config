---
name: grey-haven-pr-template
description: Generate pull request descriptions following Grey Haven Studio standards with clear summary, motivation, implementation details, testing strategy, and comprehensive checklist. Use when creating or reviewing pull requests.
---

# Grey Haven Pull Request Template

Create comprehensive, informative pull request descriptions that help reviewers understand the changes, context, and testing approach following Grey Haven Studio standards.

## PR Structure (Standard Template)

Every pull request should follow this structure:

```markdown
## Summary
[Concise 2-4 sentence description of changes]

## Motivation
[Why these changes are needed - business value, user impact, problem solved]

## Implementation Details
[Technical approach, key decisions, trade-offs considered]

## Testing
[Test strategy: unit/integration/e2e/benchmark, manual testing steps]

## Checklist
- [ ] Code follows Grey Haven style guidelines (90 char TS, 130 char Python)
- [ ] Type hints added (Python) or types maintained (TypeScript)
- [ ] Tests added/updated (unit, integration, e2e, benchmark)
- [ ] Database migrations tested (up and down)
- [ ] Multi-tenant isolation verified (tenant_id/RLS)
- [ ] Pre-commit hooks passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented with migration guide)
- [ ] Virtual environment activated (Python projects)
```

## Section Guidelines

### Summary

**Purpose**: Provide a brief, clear overview of what changed.

**Grey Haven Guidelines**:
- 2-4 sentences maximum
- Focus on **what** changed from user/system perspective
- Reference Linear issues using format: `GREY-123`
- Mention if multi-tenant or RLS changes included
- Use present tense

**Examples**:

✅ Good (Feature):
```markdown
## Summary

This PR adds magic link authentication using better-auth with email verification.
Users can now sign in via emailed links instead of passwords, reducing friction
and support requests. This addresses Linear issue GREY-234 and integrates with
our existing multi-tenant RLS policies.
```

✅ Good (Bug Fix):
```markdown
## Summary

Fixes race condition in user repository that caused duplicate email registrations
in multi-tenant environment. Resolves GREY-456.
```

✅ Good (Database):
```markdown
## Summary

Adds tenant_id column and RLS policies to organizations table for proper
multi-tenant data isolation. Migration includes backfill from service_id.
Related to GREY-890.
```

❌ Bad:
```markdown
## Summary

Updated some files and added new features and fixed bugs.
```

### Motivation

**Purpose**: Explain **why** these changes are necessary.

**Grey Haven Guidelines**:
- Describe the problem being solved
- Explain business value or user impact
- Reference Linear issues: `GREY-123` or GitHub issues: `#123`
- Include context not obvious from code
- Mention if addressing technical debt or performance

**Examples**:

✅ Good (Feature):
```markdown
## Motivation

Users reported frustration with password-based auth (GREY-234). Our analytics
show 35% of users abandon signup at password creation. Magic links offer:

- Passwordless authentication (modern UX)
- Better security (no password reuse/leaks)
- Reduced support burden (no password resets)
- Email verification built-in

This aligns with our Q1 goal of improving onboarding conversion by 20%.
```

✅ Good (Technical Debt):
```markdown
## Motivation

User repository has grown to 800 lines with repeated CRUD patterns across
multiple entity repositories. This refactoring:

- Extracts BaseRepository with common operations
- Ensures consistent tenant_id filtering
- Reduces duplication by ~60%
- Makes future repository additions faster
- Improves type safety with generics

Addresses technical debt flagged in architecture review (GREY-567).
```

### Implementation Details

**Purpose**: Explain **how** the changes work at technical level.

**Grey Haven Guidelines**:
- Mention Grey Haven tech stack: TanStack Start/Router/Query, FastAPI, Drizzle, SQLModel
- Reference Grey Haven patterns: repository pattern, multi-tenant RLS, server functions
- Note database schema changes (snake_case fields, tenant_id, indexes)
- Explain testing markers used: unit, integration, e2e, benchmark
- Include code references with file:line format

**Examples**:

✅ Good (Frontend - TanStack Start):
```markdown
## Implementation Details

### Authentication Flow
1. Added magic link server function in `lib/server/functions/auth.ts:45`
2. Created email template with Resend integration
3. Implemented token verification route at `/auth/verify`
4. Updated better-auth config for magic link provider

### Key Changes
- **Server Functions** (`lib/server/functions/auth.ts`): New `sendMagicLink`
  and `verifyMagicLink` server functions with tenant context from JWT
- **Database Schema** (`lib/server/schema/auth.ts`): Added `magic_link_tokens`
  table with snake_case fields, tenant_id for RLS, expires_at for cleanup
- **Routes** (`routes/auth/verify.tsx`): Magic link verification page with
  TanStack Router navigation after success

### Design Decisions
- **Token expiry: 15 minutes** (security vs UX balance)
- **Single-use tokens** stored in database with unique constraint
- **Tenant isolation** via RLS policies on magic_link_tokens table
- **Email via Resend** (better deliverability than SMTP)

### Multi-Tenant Considerations
- All tokens scoped to tenant_id from user context
- RLS policies prevent cross-tenant token access
- JWT claims include tenant_id for server function isolation
```

✅ Good (Backend - FastAPI):
```markdown
## Implementation Details

### Repository Pattern
Created `BaseRepository` class in `app/db/repositories/base.py`:

```python
class BaseRepository(Generic[T]):
    """Base repository with CRUD operations and tenant isolation."""

    async def get_by_id(
        self, id: UUID, tenant_id: UUID
    ) -> Optional[T]:
        """Get by ID with automatic tenant filtering."""
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == id)
            .where(self.model.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()
```

### Changes
- **BaseRepository**: Common CRUD with tenant_id filtering, type hints
- **UserRepository**: Inherits from BaseRepository, adds custom queries
- **OrganizationRepository**: Migrated to BaseRepository pattern
- **Type safety**: Generic[T] for model-specific type checking

### Benefits
- Eliminated 450 lines of duplicate code
- Consistent tenant isolation across all queries
- Type hints satisfy mypy strict mode
- Easier to add new repositories (3 methods vs 15)
```

### Testing

**Purpose**: Help reviewers and QA test the changes effectively.

**Grey Haven Guidelines**:
- List test markers used: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`, `@pytest.mark.benchmark`
- Mention test framework: Vitest (TypeScript) or pytest (Python)
- Include test coverage percentage
- Note virtual environment requirement for Python
- Describe multi-tenant test scenarios
- Include manual testing for UI changes

**Examples**:

✅ Good (TypeScript - Vitest):
```markdown
## Testing

### Automated Tests (Vitest)
- ✅ Unit tests for server functions (`lib/server/functions/auth.test.ts`)
- ✅ Integration tests for magic link flow (`tests/integration/auth.test.ts`)
- ✅ E2E tests with Playwright (`tests/e2e/magic-link.spec.ts`)
- ✅ Test coverage: 92% (up from 87%)

### Test Scenarios
- Happy path: email → token → verification → login
- Expired token (15+ minutes old)
- Invalid/tampered token
- Already-used token (single-use enforcement)
- Cross-tenant token access attempt (RLS verification)
- Email delivery failure handling

### Manual Testing Steps
1. **Setup**: Ensure `.env` has `RESEND_API_KEY`
2. **Test magic link**:
   - Visit `/auth/login`
   - Enter email address
   - Check email for magic link
   - Click link → verify redirects to dashboard
3. **Test multi-tenant**:
   - Request magic link for tenant A user
   - Attempt to use token with tenant B context
   - Verify RLS blocks cross-tenant access

### Database Testing
- Migration up/down tested locally
- RLS policies verified with different role contexts
- Indexes verified with EXPLAIN ANALYZE
```

✅ Good (Python - Pytest):
```markdown
## Testing

### Automated Tests (Pytest)
**IMPORTANT**: Activate virtual environment first: `source .venv/bin/activate`

- ✅ Unit tests: `tests/unit/repositories/test_base.py` (`@pytest.mark.unit`)
- ✅ Integration tests: `tests/integration/test_user_repository.py` (`@pytest.mark.integration`)
- ✅ Benchmark tests: `tests/benchmark/test_repository_performance.py` (`@pytest.mark.benchmark`)
- ✅ Test coverage: 94% (up from 88%)
- ✅ Type checking: mypy passes with strict mode
- ✅ Linting: ruff passes (130 char line length)

### Test Scenarios
- CRUD operations with tenant isolation
- Pagination and filtering
- Concurrent access (async tests)
- Invalid tenant_id handling
- Type safety verification

### Run Tests
```bash
source .venv/bin/activate
task test                    # All tests
task test:unit              # Unit tests only
task test:integration       # Integration tests
task test:benchmark         # Performance tests
```

### Performance Impact
Benchmark results show BaseRepository performs identically to
hand-written queries (within 2% margin).
```

### Checklist

**Purpose**: Ensure all Grey Haven standards are met before merge.

**Grey Haven Standard Checklist**:

```markdown
## Checklist

### Code Quality
- [ ] Code follows Grey Haven style guidelines
  - [ ] TypeScript: 90 char line width, double quotes, trailing commas
  - [ ] Python: 130 char line length, type hints on all functions
- [ ] Path imports use `~/` alias (TypeScript)
- [ ] No `console.log` or debug code remaining
- [ ] No commented-out code
- [ ] Error handling is comprehensive

### Testing
- [ ] Tests added/updated with appropriate markers:
  - [ ] `@pytest.mark.unit` or Vitest unit tests
  - [ ] `@pytest.mark.integration` or Vitest integration tests
  - [ ] `@pytest.mark.e2e` or Playwright tests (if UI changes)
  - [ ] `@pytest.mark.benchmark` (if performance-critical)
- [ ] All tests passing locally
- [ ] Test coverage maintained (>80%)
- [ ] Virtual environment activated for Python tests

### Database
- [ ] Database fields use snake_case (user_id, created_at, tenant_id)
- [ ] Migrations tested (up and down)
- [ ] Indexes added for new queries (check with EXPLAIN ANALYZE)
- [ ] Multi-tenant isolation enforced:
  - [ ] tenant_id column added to new tables
  - [ ] RLS policies created/updated
  - [ ] JWT claims include tenant_id

### Documentation
- [ ] README updated (if needed)
- [ ] API documentation updated (if needed)
- [ ] Inline comments for complex logic
- [ ] Migration guide included (if breaking changes)

### Grey Haven Specific
- [ ] Pre-commit hooks passing (Prettier, ESLint, Ruff, mypy)
- [ ] Commitlint format followed (100 char header, lowercase)
- [ ] Linear issues referenced (GREY-123)
- [ ] Template conventions followed:
  - [ ] TanStack Start patterns (server functions, routes)
  - [ ] FastAPI repository pattern
  - [ ] Better-auth integration (if auth changes)
  - [ ] Drizzle schema conventions (if TypeScript DB)
  - [ ] SQLModel conventions (if Python DB)

### Security
- [ ] No secrets in code (use environment variables)
- [ ] Input validation added
- [ ] Output sanitization added
- [ ] Multi-tenant data isolation verified

### Performance
- [ ] No N+1 queries introduced
- [ ] TanStack Query staleTime configured (default: 60000ms)
- [ ] Database indexes verified
- [ ] Redis caching considered (if applicable)

### Deployment
- [ ] Environment variables documented in README
- [ ] `.env.example` updated
- [ ] Rollback plan documented (if risky)
- [ ] Cloudflare Workers compatible (if frontend)
```

## PR Types and Grey Haven Templates

### Feature PR (TanStack Start Frontend)

```markdown
## Summary
[Brief feature description]. Addresses GREY-XXX.

## Motivation
- User story/requirement
- Business value and metrics
- Problem being solved

## Implementation Details

### Architecture
- TanStack Start server functions for data mutations
- TanStack Router routes and navigation
- TanStack Query for data fetching (staleTime: 60000ms)
- Shadcn UI components

### Key Changes
- **Server Functions** (`lib/server/functions/`): [description]
- **Routes** (`routes/`): [description]
- **Components** (`lib/components/`): [description]
- **Schema** (`lib/server/schema/`): Drizzle schema with snake_case fields

### Multi-Tenant
- tenant_id added to [tables]
- RLS policies created for [tables]
- JWT claims verified in server functions

## Testing
### Automated Tests (Vitest + Playwright)
- Unit tests: [files]
- Integration tests: [files]
- E2E tests: [files]
- Coverage: X%

### Manual Testing
[Step-by-step instructions]

## Checklist
- [ ] Grey Haven style guidelines (90 char, double quotes)
- [ ] Pre-commit hooks passing
- [ ] Multi-tenant RLS verified
- [ ] Tests added (unit/integration/e2e)
- [ ] Database migration tested
```

### Feature PR (FastAPI Backend)

```markdown
## Summary
[Brief feature description]. Addresses GREY-XXX.

## Motivation
- Business requirement
- API consumer needs
- Performance/scalability goals

## Implementation Details

### Architecture
- Repository pattern for data access
- Service layer for business logic
- Pydantic schemas for API contracts
- SQLModel for database models

### Key Changes
- **Routers** (`app/routers/`): FastAPI endpoints with dependency injection
- **Services** (`app/services/`): Business logic layer
- **Repositories** (`app/db/repositories/`): Data access with tenant isolation
- **Models** (`app/db/models/`): SQLModel with snake_case fields

### Multi-Tenant
- tenant_id filtering in all repository methods
- Service layer validates tenant context from JWT
- Database constraints enforce tenant isolation

## Testing

**IMPORTANT**: Activate virtual environment: `source .venv/bin/activate`

### Automated Tests (Pytest)
- `@pytest.mark.unit`: [files]
- `@pytest.mark.integration`: [files]
- `@pytest.mark.e2e`: [files]
- Type checking: mypy strict mode passes
- Linting: ruff passes (130 char lines)
- Coverage: X%

### Manual Testing
[API testing with curl/httpx examples]

## Checklist
- [ ] Virtual environment activated
- [ ] Type hints on all functions (mypy strict)
- [ ] Ruff passing (130 char lines)
- [ ] Repository pattern used
- [ ] Multi-tenant isolation tested
- [ ] Database migration tested (up/down)
```

### Bug Fix PR

```markdown
## Summary
[Brief bug description]. Fixes GREY-XXX.

## Root Cause
- What caused the bug
- Why tests didn't catch it
- Impact on users/system

## Solution
- Technical fix explanation
- Why this approach chosen
- Alternative approaches considered

### Changes
[Code changes with file references]

## Testing

### Regression Tests Added
- Unit test reproducing bug: [file:line]
- Integration test for end-to-end scenario: [file:line]

### Verification Steps
[How to verify fix works]

## Checklist
- [ ] Root cause documented
- [ ] Regression tests prevent recurrence
- [ ] Related code paths checked
- [ ] Multi-tenant scenarios tested (if applicable)
```

### Database Migration PR

```markdown
## Summary
[Migration description]. Related to GREY-XXX.

## Migration Details

### Schema Changes
- Tables: [added/modified/removed]
- Columns: All use snake_case (user_id, created_at, tenant_id)
- Indexes: [list with justification]

### Multi-Tenant
- [ ] tenant_id added to new tables
- [ ] RLS policies created
- [ ] Existing data backfilled with tenant context

### Performance Impact
- Index analysis: [EXPLAIN ANALYZE results]
- Data volume: [number of rows affected]
- Estimated migration time: [duration]

## Testing

### Migration Testing
```bash
# Up migration
npm run db:migrate  # or: alembic upgrade head

# Verify schema
npm run db:studio   # or: psql to inspect

# Down migration (rollback)
npm run db:rollback # or: alembic downgrade -1
```

### Data Integrity
- [ ] Foreign keys validated
- [ ] Unique constraints verified
- [ ] NOT NULL constraints checked
- [ ] Default values applied correctly

## Rollback Plan
[How to revert if issues occur in production]

## Checklist
- [ ] Migration tested up and down
- [ ] Indexes added for queries
- [ ] RLS policies created
- [ ] Drizzle/SQLModel schema updated
- [ ] No breaking changes to existing queries
```

## Advanced Techniques

### Linear Issue References

Grey Haven uses Linear for project management:

```markdown
## Summary
Add user profile editing. Closes GREY-123, GREY-124.
Partially addresses GREY-125.

## Related Issues
- Closes GREY-123: Edit basic profile info
- Closes GREY-124: Update profile picture
- Related to GREY-125: Full account management (phase 2)
```

### Performance Impact (Benchmarks)

Quantify performance changes with Grey Haven's benchmark test marker:

```markdown
## Performance Impact

### Benchmark Results (`@pytest.mark.benchmark`)
```bash
source .venv/bin/activate
task test:benchmark
```

Results:
- API response time: 450ms → 120ms (-73%)
- Database queries: 12 → 3 (-75%)
- Memory usage: 512MB → 380MB (-26%)

### TanStack Query Caching
- Configured staleTime: 60000ms (1 minute)
- Cache hit rate: 78% for repeated queries
- Reduced API calls by 60%
```

### Multi-Tenant Security

Highlight tenant isolation testing:

```markdown
## Multi-Tenant Security Verification

### RLS Policy Testing
```sql
-- Tested as authenticated user (tenant A)
SET request.jwt.claims TO '{"tenant_id": "uuid-a"}';
SELECT * FROM users; -- Returns only tenant A users

-- Tested as authenticated user (tenant B)
SET request.jwt.claims TO '{"tenant_id": "uuid-b"}';
SELECT * FROM users; -- Returns only tenant B users

-- Tested cross-tenant access attempt
SELECT * FROM users WHERE tenant_id = 'uuid-a';
-- Blocked by RLS policy (returns empty)
```

### Repository Pattern
- All queries include tenant_id filtering
- JWT claims validated in service layer
- Cross-tenant access returns 403 Forbidden
```

## PR Title Guidelines

Follow Grey Haven commit message conventions (commitlint):

**Format**: `<type>(<scope>): <description>` (max 100 chars, lowercase)

**Examples**:
```
feat(auth): add magic link authentication
fix(repositories): prevent race condition in user creation
docs(readme): update TanStack Start setup guide
refactor(db): extract base repository class
perf(api): add Redis caching for user queries
```

See `grey-haven-commit-format` skill for full details.

## When to Apply This Skill

Use this skill when:
- Creating new pull requests in Grey Haven projects
- Reviewing PR descriptions for completeness
- Teaching team members about PR standards
- Documenting complex multi-tenant changes
- Explaining database schema migrations
- Highlighting performance improvements

## Grey Haven PR Best Practices

1. **Reference Linear issues**: Always include GREY-XXX references
2. **Multi-tenant awareness**: Document tenant_id and RLS changes
3. **Test markers**: Use unit/integration/e2e/benchmark appropriately
4. **Virtual environment**: Remind about activation for Python projects
5. **Style adherence**: Confirm 90 char (TS) and 130 char (Python) limits
6. **Database conventions**: Verify snake_case fields, tenant_id, indexes
7. **Pre-commit hooks**: Ensure all hooks pass before PR
8. **Template patterns**: Reference TanStack or FastAPI patterns used

## Template References

These standards align with Grey Haven's actual templates:
- **Frontend**: `cvi-template` (TanStack Start + React 19 + Drizzle)
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel + Repository Pattern)

## Critical Reminders

1. **Linear issues**: Reference as GREY-123 (not #123)
2. **Line lengths**: 90 (TS), 130 (Python) - mention in checklist
3. **Database fields**: ALWAYS snake_case (user_id, created_at, tenant_id)
4. **Multi-tenant**: Document tenant_id and RLS for all DB changes
5. **Test markers**: unit, integration, e2e, benchmark
6. **Virtual env**: Remind activation for Python PRs
7. **Commit format**: 100 char header max, lowercase
8. **Pre-commit hooks**: Must pass (Prettier, ESLint, Ruff, mypy, commitlint)
