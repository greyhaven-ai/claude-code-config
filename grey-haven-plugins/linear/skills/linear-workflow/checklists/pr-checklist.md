# Pull Request Checklist

**Use before opening pull requests.**

## Before Opening PR

### Code Quality
- [ ] Code follows Grey Haven style guide (90 char TS, 130 char Python)
- [ ] No commented-out code
- [ ] No console.log or print statements (use structured logging)
- [ ] No TODO comments (create Linear issues instead)
- [ ] All imports organized and unused imports removed
- [ ] Pre-commit hooks passing

### Testing
- [ ] Unit tests added for new functions/components
- [ ] Integration tests added for new features
- [ ] E2E tests added for critical user flows
- [ ] All tests passing locally with Doppler: `doppler run --config test -- bun test`
- [ ] Test coverage >80% (verify with coverage report)
- [ ] Tests use appropriate markers (@pytest.mark.unit, Vitest describe blocks)

### Multi-Tenant Compliance
- [ ] All new tables include tenant_id column (NOT NULL, indexed)
- [ ] All queries filter by tenant_id
- [ ] RLS policies created for new tables
- [ ] Tenant isolation tested with different tenant contexts
- [ ] No cross-tenant data leakage possible

### Database Changes (if applicable)
- [ ] Migration generated (Drizzle Kit or Alembic)
- [ ] Migration tested up (apply)
- [ ] Migration tested down (rollback)
- [ ] Schema uses snake_case field names (NOT camelCase)
- [ ] Indexes created for foreign keys and tenant_id
- [ ] Migration reviewed by teammate

### Doppler Configuration
- [ ] New environment variables added to Doppler
- [ ] Environment variables documented in PR description
- [ ] Environment variables added to all environments (dev/test/staging/production)
- [ ] No secrets committed to git
- [ ] .env.example updated (if applicable)

### Git & Linear
- [ ] Branch follows naming convention: GREY-XXX-type-description
- [ ] Commits follow conventional commits format
- [ ] Linear issue ID in commits (Closes GREY-XXX / Fixes GREY-XXX)
- [ ] Branch up to date with main: `git pull origin main`

## PR Content

### Title
- [ ] PR title follows format: `<type>(<scope>): <description> [GREY-XXX]`
- [ ] PR title matches issue title (or explains deviation)
- [ ] PR title is under 100 characters

### Description
- [ ] Summary section explains changes (2-4 sentences)
- [ ] "Closes GREY-XXX" keyword included
- [ ] Linear issue URL included
- [ ] Motivation section explains "why"
- [ ] Implementation details section covers key changes

### Implementation Details
- [ ] Key changes documented by component
- [ ] Database changes listed (if applicable)
- [ ] Multi-tenant considerations documented
- [ ] Doppler configuration changes documented
- [ ] Breaking changes called out (if applicable)

### Testing Section
- [ ] Automated test results documented
- [ ] Test coverage percentage included
- [ ] Manual testing steps included (if applicable)
- [ ] Doppler test command included
- [ ] Screenshots/recordings attached (if UI changes)

### Checklist
- [ ] All PR description checklist items checked
- [ ] Reviewers assigned
- [ ] Labels synced from Linear issue

## After Opening PR

### CI/CD
- [ ] GitHub Actions passing (tests, linting)
- [ ] No merge conflicts with main
- [ ] Branch protection checks passing
- [ ] Deployment preview working (if applicable)

### Review Process
- [ ] At least 1 reviewer assigned
- [ ] Responded to review comments within 24 hours
- [ ] All requested changes addressed
- [ ] Re-requested review after changes
- [ ] Approved by required reviewers

### Before Merging
- [ ] All conversations resolved
- [ ] CI/CD passing
- [ ] Branch up to date with main
- [ ] Squash merge selected (for clean history)
- [ ] Linear issue will auto-close (verified "Closes GREY-XXX" in description)

## After Merging

### Post-Merge
- [ ] Feature branch deleted
- [ ] Linear issue automatically closed (verify)
- [ ] Deployment to staging successful (if applicable)
- [ ] Smoke tests passing in staging
- [ ] Team notified of significant changes

### Deployment
- [ ] Production deployment successful
- [ ] Smoke tests passing in production
- [ ] Monitoring shows no errors (Sentry, Axiom)
- [ ] Performance metrics acceptable
- [ ] Linear issue updated with deployment notes
