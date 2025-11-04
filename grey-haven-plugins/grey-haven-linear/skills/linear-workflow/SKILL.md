---
name: grey-haven-linear-workflow
description: Grey Haven's Linear issue workflow - creating well-documented issues, proper branch naming from issue IDs, commit message integration, PR linking, and status management. Use when creating issues, starting work, or managing project workflow.
---

# Grey Haven Linear Workflow

Follow Grey Haven Studio's workflow for Linear issue management, Git branching, and pull request integration.

## Linear Issue Management

### Issue Creation

Always create Linear issues BEFORE starting work to track progress and context.

#### Issue Templates by Type

**Feature Issue**:
```markdown
Title: Add magic link authentication

## Description
Implement magic link authentication using better-auth to reduce password friction.

## Motivation
- 35% of users abandon signup at password creation
- Better security (no password reuse/leaks)
- Reduces support burden (no password resets)

## Acceptance Criteria
- [ ] User can request magic link via email
- [ ] Magic link tokens expire after 15 minutes
- [ ] Single-use tokens (can't reuse same link)
- [ ] Tenant isolation enforced via RLS
- [ ] Integration tests pass with >80% coverage

## Technical Notes
- Use better-auth magic link provider
- Store tokens in `magic_link_tokens` table
- Implement server function for sending/verifying links
- Use Doppler for RESEND_API_KEY in deployment

## Related Issues
- Blocks: GREY-125 (OAuth providers)
- Related: GREY-89 (Better-auth migration)

Labels: feature, auth, high-priority
Estimate: 8 points
```

**Bug Issue**:
```markdown
Title: Fix race condition in user repository

## Description
User creation fails intermittently due to concurrent requests checking email uniqueness.

## Steps to Reproduce
1. Send 2 simultaneous POST /users requests with same email
2. Both requests check email uniqueness
3. Both pass check and attempt INSERT
4. One fails with IntegrityError

## Expected Behavior
Second request should receive 409 Conflict immediately.

## Actual Behavior
Second request fails with 500 Internal Server Error (IntegrityError).

## Impact
- ~5% of user registrations fail
- Poor user experience (unclear error)
- Potential data corruption

## Proposed Solution
Add database-level unique constraint + proper error handling in repository.

## Environment
- Backend: cvi-backend-template
- Database: PostgreSQL 15 with RLS
- Doppler config: production

Labels: bug, database, critical
Priority: Urgent
```

**Database Migration Issue**:
```markdown
Title: Add tenant_id to organizations table

## Description
Add tenant_id column and RLS policies to organizations table for multi-tenant isolation.

## Migration Steps
1. Add tenant_id column (nullable initially)
2. Backfill from service_id column
3. Make tenant_id NOT NULL
4. Add foreign key constraint
5. Create indexes
6. Enable RLS
7. Create tenant isolation policies

## Rollback Plan
Drop RLS policies → drop indexes → drop FK → drop column

## Testing
- [ ] Migration up/down tested locally
- [ ] Backfill logic validated on test data
- [ ] RLS policies tested with different tenant contexts
- [ ] EXPLAIN ANALYZE on queries with tenant_id filter

## Risk Assessment
- **Data volume**: ~50K organizations
- **Migration time**: ~30 seconds estimated
- **Downtime required**: No (nullable initially)

## Doppler Variables Needed
- DATABASE_URL_ADMIN (for migration)
- DATABASE_URL_AUTHENTICATED (for RLS testing)

Labels: database, migration, multi-tenant
Estimate: 5 points
```

### Issue Naming Conventions

```
[OK] Good issue titles (specific, actionable):
- Add magic link authentication
- Fix race condition in user repository
- Migrate organizations table to multi-tenant
- Update TanStack Query to v5.62.0

[X] Bad issue titles (vague, non-actionable):
- Auth improvements
- Fix bug
- Update dependencies
- Refactor code
```

### Labels

Grey Haven uses these standard labels:

**Type Labels**:
- `feature`: New functionality
- `bug`: Something broken
- `chore`: Maintenance work
- `docs`: Documentation updates
- `refactor`: Code improvements (no new features)
- `performance`: Performance optimizations

**Component Labels**:
- `frontend`: TanStack Start/React
- `backend`: FastAPI/Python
- `database`: Schema/migrations
- `auth`: Authentication/authorization
- `multi-tenant`: Tenant isolation
- `testing`: Test infrastructure

**Priority Labels**:
- `critical`: Production outage
- `high-priority`: Blocks other work
- `low-priority`: Nice to have

### Estimates

Use Fibonacci sequence for story points:
- **1 point**: < 1 hour (simple fix, config change)
- **2 points**: 1-2 hours (small feature, simple bug)
- **3 points**: Half day (moderate feature)
- **5 points**: 1 day (complex feature, migration)
- **8 points**: 2-3 days (large feature, major refactor)
- **13 points**: 1 week (epic-sized, should be broken down)

## Git Branching Strategy

### Branch Naming Convention

**Format**: `<issue-id>-<type>-<short-description>`

```bash
# Feature branches
GREY-234-feat-magic-link-auth
GREY-125-feat-oauth-providers

# Bug fix branches
GREY-456-fix-user-race-condition
GREY-789-fix-rls-policy-organizations

# Database migration branches
GREY-890-migrate-add-tenant-id
GREY-567-migrate-create-teams-table

# Chore branches
GREY-123-chore-update-dependencies
GREY-456-chore-improve-test-coverage

# Documentation branches
GREY-789-docs-update-api-guide
GREY-234-docs-add-testing-examples
```

### Creating Branches from Linear Issues

```bash
# 1. Get Linear issue ID (e.g., GREY-234)
# 2. Check issue title and type
# 3. Create branch following naming convention

# Feature example
git checkout main
git pull origin main
git checkout -b GREY-234-feat-magic-link-auth

# Bug fix example
git checkout main
git pull origin main
git checkout -b GREY-456-fix-user-race-condition

# Always branch from latest main!
```

### Branch Protection Rules

```bash
# Main branch protection:
[OK] Require pull request before merging
[OK] Require 1 approval
[OK] Require status checks to pass (tests, linting)
[OK] Require branches to be up to date
[OK] Require linear history (squash merges)
[X] Do NOT allow force pushes
[X] Do NOT allow deletions
```

## Commit Message Integration

### Linking Commits to Linear

Always reference Linear issue ID in commit messages:

```bash
# Single commit referencing issue
git commit -m "feat(auth): add magic link server functions

Implement sendMagicLink and verifyMagicLink server functions with
tenant context from JWT claims.

Related to GREY-234"

# Multiple commits on same branch
git commit -m "feat(auth): scaffold magic link provider

GREY-234"

git commit -m "feat(auth): add token verification logic

GREY-234"

git commit -m "test(auth): add magic link integration tests

GREY-234"
```

### Commit Message Format with Linear

```
<type>(<scope>): <subject>

[optional body]

[Linear issue reference]
```

**Examples**:

```bash
# Feature commit
feat(auth): add magic link authentication

Implement magic link provider using better-auth with email
verification via Resend.

- Single-use tokens with 15 minute expiry
- Tenant isolation via RLS policies
- Server functions for sending/verifying links

Closes GREY-234

# Bug fix commit
fix(repositories): prevent race condition in user creation

Add database-level unique constraint and proper IntegrityError
handling in UserRepository.

- Unique constraint on email_address + tenant_id
- Return 409 Conflict for duplicate emails
- Integration tests for concurrent requests

Fixes GREY-456

# Migration commit
feat(db): add tenant_id to organizations table

Add tenant_id column and RLS policies for multi-tenant isolation.

- Backfill from service_id column
- Created indexes for tenant_id queries
- RLS policies for authenticated role

Related to GREY-890
```

### Linear Keywords

Use these keywords to automatically update Linear issues:

- **Closes GREY-123**: Marks issue as Done when PR merges
- **Fixes GREY-123**: Same as Closes (for bugs)
- **Related to GREY-123**: Links issue without closing
- **Blocks GREY-123**: Indicates dependency
- **Blocked by GREY-123**: Indicates blocker

## Pull Request Integration

### PR Title Format

Match commit message format and include Linear ID:

```
<type>(<scope>): <description> [GREY-123]
```

**Examples**:

```
feat(auth): add magic link authentication [GREY-234]
fix(repositories): prevent race condition in user creation [GREY-456]
feat(db): add tenant_id to organizations table [GREY-890]
```

### PR Description Template

```markdown
## Summary
[2-4 sentence description]. Closes GREY-XXX.

## Linear Issue
https://linear.app/grey-haven/issue/GREY-XXX/issue-title

## Motivation
[Why these changes are needed]

## Implementation Details

### Key Changes
- **File/Component**: [what changed]
- **Database**: [schema changes with snake_case fields]
- **Tests**: [test coverage with markers]

### Multi-Tenant Considerations
- tenant_id added to [tables]
- RLS policies created for [tables]
- Queries filter by tenant_id

### Doppler Configuration
- Added/updated: [environment variables]
- Required in: [dev/test/staging/production]

## Testing

### Automated Tests
- [OK] Unit tests: [files] (`@pytest.mark.unit` or Vitest)
- [OK] Integration tests: [files] (`@pytest.mark.integration`)
- [OK] E2E tests: [files] (Playwright or `@pytest.mark.e2e`)
- [OK] Coverage: X% (target: >80%)

### Manual Testing Steps
1. Setup: `doppler run --config dev -- [command]`
2. Test [scenario]
3. Verify [expected result]

### Doppler Testing
Run tests with Doppler:
```bash
doppler run --config test -- npm run test  # TypeScript
doppler run --config test -- pytest        # Python
```

## Database Changes
[If applicable]
- Migration: [file name]
- Tested up/down: [OK]
- Indexes added: [list]
- RLS policies: [list]

## Checklist
- [ ] Code follows Grey Haven style (90 char TS, 130 char Python)
- [ ] Tests added/updated (unit/integration/e2e markers)
- [ ] Coverage maintained (>80%)
- [ ] Multi-tenant isolation verified
- [ ] Doppler env vars documented
- [ ] Pre-commit hooks passing
- [ ] Database migrations tested (if applicable)
- [ ] Linear issue linked and referenced
```

### PR Labels

Automatically synced from Linear issue labels:
- Type: `feature`, `bug`, `chore`, `docs`, `refactor`
- Component: `frontend`, `backend`, `database`, `auth`
- Priority: `critical`, `high-priority`, `low-priority`

## Linear Status Management

### Issue Lifecycle

```
Backlog → Todo → In Progress → In Review → Done
   ↓                                ↓
Canceled                        Canceled
```

### Status Transitions

**Todo → In Progress**:
```bash
# When starting work:
1. Create branch: GREY-234-feat-magic-link-auth
2. Linear automatically moves to "In Progress" (via GitHub integration)
3. Start coding
```

**In Progress → In Review**:
```bash
# When opening PR:
1. Push commits to branch
2. Create PR with "Closes GREY-234" in description
3. Linear automatically moves to "In Review"
4. Request review from team
```

**In Review → Done**:
```bash
# When PR merges:
1. Squash and merge PR to main
2. Linear automatically closes issue (via "Closes GREY-234")
3. Delete feature branch
```

**Any Status → Canceled**:
```bash
# If work is abandoned:
1. Update Linear issue status to "Canceled"
2. Add comment explaining why
3. Delete feature branch
4. No PR required
```

## GitHub Integration

### Linear ↔ GitHub Sync

Grey Haven uses Linear's GitHub integration for automatic syncing:

**Automatic Actions**:
- Branch created → Issue moves to "In Progress"
- PR opened → Issue moves to "In Review"
- PR merged with "Closes GREY-XXX" → Issue moves to "Done"
- Commits pushed → Activity logged on issue

**Manual Actions**:
- Comment on PR → Synced to Linear
- Label PR → Synced to Linear
- Close PR without merge → Issue returns to previous status

### Branch Linking

Linear automatically detects branches that start with issue ID:

```bash
# [OK] Automatically linked to GREY-234
GREY-234-feat-magic-link-auth

# [OK] Also automatically linked
GREY-234-add-magic-link

# [X] NOT automatically linked (missing issue ID)
feat-magic-link-auth

# [X] NOT automatically linked (wrong format)
234-magic-link-auth
```

## Workflow Examples

### Feature Development Workflow

```bash
# 1. Create Linear issue
# Title: Add magic link authentication
# ID: GREY-234
# Labels: feature, auth
# Estimate: 8 points

# 2. Create branch from main
git checkout main
git pull origin main
git checkout -b GREY-234-feat-magic-link-auth
# Linear auto-moves to "In Progress"

# 3. Implement feature with frequent commits
git add .
git commit -m "feat(auth): scaffold magic link provider

GREY-234"

git add .
git commit -m "feat(auth): add token verification

GREY-234"

git add .
git commit -m "test(auth): add integration tests

GREY-234"

# 4. Push branch
git push origin GREY-234-feat-magic-link-auth

# 5. Create PR
gh pr create \
  --title "feat(auth): add magic link authentication [GREY-234]" \
  --body "$(cat <<'EOF'
## Summary
Implements magic link authentication using better-auth. Closes GREY-234.

## Linear Issue
https://linear.app/grey-haven/issue/GREY-234/add-magic-link-authentication

[Rest of PR template...]
EOF
)"
# Linear auto-moves to "In Review"

# 6. Address review feedback
git add .
git commit -m "fix(auth): address PR feedback

- Improve error handling
- Add missing test cases

GREY-234"
git push origin GREY-234-feat-magic-link-auth

# 7. Squash and merge PR
gh pr merge --squash
# Linear auto-closes issue (moves to "Done")

# 8. Delete branch
git branch -d GREY-234-feat-magic-link-auth
git push origin --delete GREY-234-feat-magic-link-auth
```

### Bug Fix Workflow

```bash
# 1. Create Linear issue
# Title: Fix race condition in user repository
# ID: GREY-456
# Labels: bug, database, critical
# Priority: Urgent

# 2. Create hotfix branch
git checkout main
git pull origin main
git checkout -b GREY-456-fix-user-race-condition

# 3. Fix bug with minimal changes
git add app/db/repositories/user_repository.py
git commit -m "fix(repositories): prevent race condition

Add unique constraint and proper IntegrityError handling.

Fixes GREY-456"

# 4. Add regression tests
git add tests/integration/test_user_repository.py
git commit -m "test(repositories): add race condition regression tests

GREY-456"

# 5. Push and create PR
git push origin GREY-456-fix-user-race-condition
gh pr create \
  --title "fix(repositories): prevent race condition in user creation [GREY-456]" \
  --body "Closes GREY-456"

# 6. Merge immediately if critical
gh pr merge --squash
```

### Database Migration Workflow

```bash
# 1. Create Linear issue
# Title: Add tenant_id to organizations table
# ID: GREY-890
# Labels: database, migration, multi-tenant
# Estimate: 5 points

# 2. Create migration branch
git checkout main
git pull origin main
git checkout -b GREY-890-migrate-add-tenant-id

# 3. Generate migration (TypeScript/Drizzle)
npm run db:generate
# Edit generated migration for backfill logic

# 4. Or generate migration (Python/Alembic)
source .venv/bin/activate
doppler run -- alembic revision --autogenerate -m "add tenant_id to organizations"
# Edit generated migration for backfill logic

# 5. Test migration up and down
doppler run --config dev -- npm run db:migrate
doppler run --config dev -- npm run db:rollback

# Or for Python:
doppler run --config dev -- alembic upgrade head
doppler run --config dev -- alembic downgrade -1

# 6. Commit migration
git add migrations/
git commit -m "feat(db): add tenant_id to organizations table

Add tenant_id column and RLS policies for multi-tenant isolation.

Migration includes:
- tenant_id column (backfilled from service_id)
- Foreign key constraint
- Indexes for performance
- RLS policies for authenticated role

Tested up/down with Doppler dev environment.

Related to GREY-890"

# 7. Create PR with migration details
gh pr create \
  --title "feat(db): add tenant_id to organizations table [GREY-890]" \
  --body "[Detailed migration PR template...]"
```

## Best Practices

### Linear Issue Management

1. **Create issues BEFORE coding** - Track context and decisions
2. **Write clear descriptions** - Future you will thank you
3. **Use proper labels** - Helps filtering and reporting
4. **Estimate accurately** - Improves sprint planning
5. **Link related issues** - Shows dependencies
6. **Close finished work** - Keep board clean

### Git Branching

1. **Always branch from main** - Avoid merge conflicts
2. **Use issue ID prefix** - Enables auto-linking
3. **One branch per issue** - Clear scope
4. **Keep branches short-lived** - Merge within 2-3 days
5. **Delete after merge** - Avoid clutter

### Commit Messages

1. **Reference Linear ID** - Enables tracking
2. **Follow conventional commits** - Consistent format (100 char header, lowercase)
3. **Explain WHY not WHAT** - Code shows what changed
4. **Use keywords** - Auto-close issues (Closes, Fixes)

### Pull Requests

1. **Link Linear issue** - Required context
2. **Use PR template** - Consistent structure
3. **Include test coverage** - With markers (unit/integration/e2e)
4. **Document Doppler vars** - Required environment setup
5. **Request review early** - Don't wait until "perfect"
6. **Squash merge** - Clean history

## Doppler Integration

### Environment Variables in Linear Issues

When creating issues that require new environment variables, document Doppler requirements:

```markdown
## Doppler Configuration

### New Variables
- `RESEND_API_KEY`: Resend API key for email sending
  - Required in: dev, test, staging, production
  - Get from: https://resend.com/api-keys

- `MAGIC_LINK_TOKEN_EXPIRY`: Token expiry in seconds
  - Required in: all environments
  - Default: 900 (15 minutes)

### Testing
Run tests with Doppler:
```bash
doppler run --config test -- npm run test
doppler run --config test -- pytest
```
```

## When to Apply This Skill

Use this skill when:
- Starting new work (create issue first!)
- Creating Git branches
- Writing commit messages
- Opening pull requests
- Managing project status in Linear
- Setting up GitHub integration
- Documenting Doppler requirements
- Reviewing team member workflows

## Template References

These workflow patterns are used in Grey Haven's actual projects:
- **Linear**: https://linear.app/grey-haven
- **GitHub**: All repositories follow this workflow
- **Doppler**: https://doppler.com for environment management

## Critical Reminders

1. **Issue first**: ALWAYS create Linear issue before coding
2. **Branch naming**: `GREY-XXX-type-description` format
3. **Commit references**: Include issue ID in all commits
4. **PR keywords**: Use "Closes GREY-XXX" to auto-close
5. **Squash merge**: Keep main history clean
6. **Delete branches**: After merging to main
7. **Doppler**: Document env vars in issues and PRs
8. **Test with Doppler**: `doppler run --config test -- [command]`
9. **Labels**: Apply appropriate type/component/priority labels
10. **Status tracking**: Let GitHub integration handle status updates
