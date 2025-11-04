---
name: grey-haven-commit-format
description: Format commit messages according to Grey Haven Studio's actual commitlint configuration (100 char header, lowercase subject, conventional commits). Use when creating git commits or reviewing commit messages.
---

# Grey Haven Commit Message Format

Follow Grey Haven Studio's **actual** commit message standards, enforced by commitlint configuration from production templates.

## Format Structure (Commitlint Enforced)

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**CRITICAL Rules** (from `commitlint.config.cjs`):
- **Header max length: 100 characters** (NOT 72 or 50!)
- **Type: REQUIRED** and must be lowercase
- **Subject: REQUIRED** and lowercase (NO sentence-case, start-case, pascal-case, or upper-case)
- **Body: blank line before** (if included)
- **Footer: blank line before** (if included)

## Commit Types (Enforced)

Use **exactly** these types from Grey Haven's commitlint configuration:

### Primary Types
- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Documentation changes only
- **style**: Code style changes (formatting, semicolons, etc.) - no logic changes
- **refactor**: Code refactoring - neither fixes a bug nor adds a feature
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates, tooling changes

### Additional Types
- **perf**: Performance improvements
- **ci**: CI/CD configuration changes
- **build**: Build system or dependency changes
- **revert**: Revert a previous commit

**Any other type will be REJECTED by commitlint.**

## Scope Guidelines

The scope should indicate which part of the codebase is affected:

### Frontend Scopes (TanStack Start/React)
- `auth`: Authentication components/flows
- `ui`: UI components (Shadcn)
- `forms`: Form components
- `layout`: Layout components
- `routes`: TanStack Router routes
- `queries`: TanStack Query hooks
- `db`: Database schema (Drizzle)
- `server`: Server functions (TanStack Start)

### Backend Scopes (FastAPI/Python)
- `api`: API endpoints/routers
- `models`: SQLModel database models
- `repositories`: Repository pattern classes
- `services`: Service layer business logic
- `schemas`: Pydantic schemas (API contracts)
- `db`: Database migrations/queries
- `utils`: Utility functions
- `config`: Application settings

### Infrastructure Scopes
- `deps`: Dependency updates (npm/pip)
- `docker`: Docker configuration
- `deploy`: Deployment scripts/configuration
- `scripts`: Build/utility scripts
- `ci`: CI/CD pipeline (GitHub Actions)
- `hooks`: Pre-commit/commit-msg hooks

### Examples
```
feat(auth): add magic link authentication
fix(api): resolve race condition in order processing
docs(readme): update TanStack Start setup guide
chore(deps): upgrade React to v19.1.0
refactor(repositories): simplify user query logic
```

**Scope is optional** - omit if change affects multiple areas or is global.

## Subject Line Rules (Commitlint Enforced)

### Requirements (from commitlint.config.cjs)
- **Max length: 100 characters** (header includes type + scope + subject)
- **Case: lowercase ONLY** - NO sentence-case, start-case, pascal-case, or upper-case
- **Format: imperative mood** - "add" not "added" or "adds"
- **No period** at the end
- **Be specific** about what changed

### Calculating Header Length
```
feat(auth): add OAuth provider for Google authentication
^---------^ = 9 chars (type + scope)
            ^----------------------------------------^ = 45 chars (subject)
Total: 54 characters (within 100 limit [OK])
```

### Good Examples (Pass Commitlint)
```
feat(auth): add password reset with email verification
fix(api): prevent duplicate user email registrations
docs: update API authentication guide with examples
refactor(utils): simplify date formatting helper functions
perf(db): add composite index on user_id and created_at
test(auth): add integration tests for OAuth flow
chore(deps): upgrade TypeScript to v5.6.0
```

### Bad Examples (Fail Commitlint)
```
[X] feat(auth): Add OAuth provider     # Uppercase 'A' (violates subject-case)
[X] Fix bug in API                      # Uppercase 'F' (violates subject-case)
[X] feat: add new feature.              # Period at end
[X] WIP                                 # Not a valid type
[X] added new endpoint                  # Missing type
[X] feat(api): Added a new endpoint for user authentication and also updated the database schema and added validation logic and wrote tests and updated documentation
   # Exceeds 100 characters
```

## Body (Optional)

Use the body to provide additional context when needed.

### When to Include a Body
- Explaining **why** the change was made (motivation)
- Describing **implementation approach** that isn't obvious
- Noting **breaking changes** or important considerations
- Referencing **related Linear issues** or GitHub issues
- Listing **multiple changes** in a larger commit

### Body Format (Commitlint Rules)
- **Blank line REQUIRED** between subject and body
- Wrap at **90 characters per line** (matches Grey Haven's TypeScript printWidth)
- Use **bullet points** for lists (markdown format)
- Write in **present tense**, imperative mood

### Example with Body
```
feat(api): add rate limiting to authentication endpoints

Implement Redis-based rate limiting to prevent brute force attacks on
login and password reset endpoints.

- 5 requests per minute per IP for login
- 3 requests per hour for password reset
- Uses Redis for distributed rate limiting across Workers
- Returns 429 status when limit exceeded

Addresses security concerns from audit in Linear issue GREY-123.
```

## Footer (Optional)

Use the footer for metadata, breaking changes, and issue references.

### Breaking Changes (CRITICAL)
Start with `BREAKING CHANGE:` followed by description:

```
feat(api): migrate user IDs to UUID format

Change user ID format from sequential integers to UUIDs for better
scalability and security in multi-tenant architecture.

BREAKING CHANGE: User IDs are now UUIDs instead of sequential integers.
All API clients must update to handle UUID format. Database migration
required before deploying this change.
```

### Linear Issue References
Reference Linear issues using standard format:

```
fix(auth): resolve session timeout on tab focus

Session was expiring when user switched browser tabs due to incorrect
activity tracking logic.

Fixes GREY-456
Related to GREY-123
```

### GitHub Issue References
For open-source or public repos:

```
fix(ui): correct button alignment in mobile view

Fixes #234
Closes #456
Related to #789
```

## Complete Examples (Grey Haven Standards)

### Simple Feature (TypeScript)
```
feat(ui): add loading skeleton for user profile card
```

### Bug Fix with Context (Python)
```
fix(repositories): prevent race condition in user creation

User creation was failing intermittently due to concurrent requests
checking email uniqueness. Added database-level unique constraint and
proper error handling for IntegrityError.

- Added unique constraint migration
- Handle IntegrityError in UserRepository
- Return 409 Conflict for duplicate emails

Fixes GREY-234
```

### Breaking Change (API)
```
feat(api): migrate authentication to better-auth

Replace custom auth implementation with better-auth library for
improved security and OAuth provider support.

BREAKING CHANGE: Authentication endpoints have changed. Old endpoints
under /api/auth/* are deprecated. New endpoints follow better-auth
conventions. Clients must update to new auth flow.

Migration guide: docs/auth-migration.md
Fixes GREY-567
```

### Dependency Update (Frontend)
```
chore(deps): upgrade TanStack Query to v5.62.0

- Fixes type inference issues with useQuery
- Improves DevTools performance
- No breaking changes in our usage
```

### Database Schema Change (Multi-tenant)
```
feat(db): add tenant isolation to organizations table

Add tenant_id column and RLS policies to organizations table for
multi-tenant data isolation.

- Added tenant_id UUID column with index
- Created RLS policies for authenticated role
- Migration includes data backfill from service_id
- Updated Drizzle schema with snake_case fields

BREAKING CHANGE: All organization queries must include tenant_id.
Update repositories to use tenant context from JWT.

Related to GREY-890
```

### Refactoring (Repository Pattern)
```
refactor(repositories): extract base repository class

Create BaseRepository with common CRUD operations and tenant filtering
to reduce duplication across repository classes.

- BaseRepository with get_by_id, list, create, update, delete
- Automatic tenant_id filtering in all queries
- Type hints for generic model types
- Async/await throughout
```

## Grey Haven Specific Patterns

### Multi-Tenant Changes
Always mention tenant_id when working with multi-tenant features:

```
feat(db): add RLS policies for tenant data isolation

- Enable RLS on users, organizations, teams tables
- Create policies for admin, authenticated, anon roles
- JWT claims include tenant_id for automatic filtering
```

### TanStack Start Server Functions
```
feat(server): add server function for user profile update

Create TanStack Start server function with proper validation and
tenant isolation for user profile updates.
```

### FastAPI Endpoints
```
feat(api): add GET /users endpoint with pagination

- Repository pattern with UserRepository
- Pydantic schema validation
- Tenant filtering from JWT claims
- Pagination with limit/offset
```

### Database Migrations
```
feat(db): add created_at and updated_at to all tables

Add timestamp tracking to remaining tables following Grey Haven
conventions (snake_case fields, defaultNow()).
```

## Testing and Validation

### Pre-commit Hooks
Grey Haven projects include commitlint validation in pre-commit hooks:

```bash
# Automatically runs on git commit
# Validates: type, subject case, header length, blank lines
```

### Manual Validation
Test your commit message before committing:

```bash
echo "feat(auth): add OAuth provider" | npx commitlint
```

### Commitlint Configuration Reference
Grey Haven uses `@commitlint/config-conventional` with these modifications:

```javascript
// commitlint.config.cjs
{
  rules: {
    "type-enum": [2, "always", [
      "feat", "fix", "docs", "style", "refactor",
      "test", "chore", "perf", "ci", "build", "revert"
    ]],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
    "subject-case": [2, "never", [
      "sentence-case", "start-case", "pascal-case", "upper-case"
    ]],
    "header-max-length": [2, "always", 100],
    "body-leading-blank": [2, "always"],
    "footer-leading-blank": [2, "always"]
  }
}
```

## Commit Message Checklist

Before committing, verify:

- [ ] Type is one of: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- [ ] Type is lowercase
- [ ] Scope is meaningful and lowercase (if included)
- [ ] Subject uses imperative mood ("add" not "added")
- [ ] Subject is lowercase (NO capitals anywhere)
- [ ] Full header (type + scope + subject) is under 100 characters
- [ ] Subject doesn't end with a period
- [ ] Body has blank line after subject (if included)
- [ ] Body wraps at 90 characters per line
- [ ] Breaking changes start with "BREAKING CHANGE:"
- [ ] Linear/GitHub issues are referenced (if applicable)
- [ ] No sensitive information (passwords, keys, tokens)

## Multi-Commit Workflows

### Feature Branch Commits
During development on feature branches, commits can be granular:

```
feat(auth): scaffold OAuth provider interface
feat(auth): implement Google OAuth provider
feat(auth): add OAuth callback handler
test(auth): add OAuth integration tests
docs(auth): document OAuth configuration
```

### Squashing Before Merge
Before merging to main, squash to a single descriptive commit:

```
feat(auth): add OAuth authentication with Google provider

Implement OAuth 2.0 authentication using better-auth with Google
provider support.

- Google OAuth provider configuration
- Callback URL handler with tenant context
- Token management and refresh logic
- User profile sync from OAuth claims
- Integration tests with mock OAuth server

Fixes GREY-456
```

## Special Cases

### Revert Commits
Reference the original commit hash:

```
revert: feat(auth): add OAuth authentication

This reverts commit abc123def456.

Reverting due to session persistence issues in production. OAuth
implementation needs additional testing with Redis session store.

See GREY-789 for tracking rewrite.
```

### Merge Commits (Squash Preferred)
Grey Haven typically uses **squash merges** on main branch. When merge commits are needed:

```
Merge branch 'feature/oauth' into main

feat(auth): add OAuth authentication support
```

### Virtual Environment Activation (Python Projects)
When making commits in Python projects, **ALWAYS activate virtual environment first**:

```bash
source .venv/bin/activate
git commit -m "feat(api): add user endpoint"
```

Pre-commit hooks require virtual environment to run Ruff, mypy, and pytest.

## When to Apply This Skill

Use this skill when:
- Creating git commits in Grey Haven projects
- Reviewing pull requests and commit messages
- Setting up commit message templates
- Configuring commitlint for new projects
- Writing release notes from commit history
- Squashing commits before merging
- Teaching git best practices to team members

## Template References

These standards come from Grey Haven's actual templates:
- **Frontend**: `cvi-template` (TanStack Start + React 19) - [commitlint.config.cjs](../../../cvi-template/commitlint.config.cjs)
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel) - uses same commitlint config

## Critical Reminders

1. **Header max: 100 characters** (NOT 72 or 50!)
2. **Subject: lowercase ONLY** (NO capitals anywhere)
3. **Types: exact match required** (feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert)
4. **Body/footer: blank line before** (enforced by commitlint)
5. **Breaking changes: use BREAKING CHANGE:** prefix
6. **Linear issues: reference as GREY-123**
7. **Multi-tenant: mention tenant_id when relevant**
8. **Python projects: activate .venv before committing**
9. **Pre-commit hooks: will validate format automatically**
10. **Squash merges: preferred for main branch**
