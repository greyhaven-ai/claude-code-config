# Deployment Checklist

**Use before deploying to production.**

## Pre-Deployment

### Doppler Configuration
- [ ] All required secrets set in Doppler production environment
- [ ] DOPPLER_TOKEN added to GitHub repository secrets
- [ ] CLOUDFLARE_API_TOKEN added to GitHub repository secrets
- [ ] Test Doppler access: `doppler secrets --config production`

### Wrangler Configuration
- [ ] wrangler.production.toml configured with correct routes
- [ ] KV namespaces created and IDs added to wrangler.toml
- [ ] R2 buckets created and names added to wrangler.toml
- [ ] Custom domain DNS configured in Cloudflare
- [ ] Connection pool settings match database capacity

### Database
- [ ] Migrations tested locally
- [ ] Migration reversible (has downgrade)
- [ ] Seed data prepared for production (if needed)
- [ ] DATABASE_URL_ADMIN has elevated permissions for migrations
- [ ] Connection pooling configured (Neon/Supabase)

### Application
- [ ] All tests passing locally
- [ ] All tests passing in CI
- [ ] Build completes without errors
- [ ] No TypeScript errors
- [ ] No console.log statements in production code
- [ ] Environment variables validated

### GitHub Actions
- [ ] Workflow file present (.github/workflows/deploy-production.yml)
- [ ] Workflow triggers configured (push to main)
- [ ] Node.js version matches local (22)
- [ ] Doppler CLI action configured
- [ ] Smoke tests configured

## During Deployment

### Deployment Steps
- [ ] Merge PR to main branch
- [ ] GitHub Actions workflow triggered
- [ ] Tests pass in CI
- [ ] Build completes successfully
- [ ] Database migrations run successfully
- [ ] Workers deployment completes
- [ ] Secrets injected into Workers
- [ ] Smoke tests pass

### Monitoring
- [ ] Watch deployment logs in GitHub Actions
- [ ] Monitor Cloudflare Workers dashboard
- [ ] Check Wrangler tail for errors
- [ ] Verify no Sentry errors
- [ ] Verify application loads at production URL

## Post-Deployment

### Validation
- [ ] Production URL loads successfully
- [ ] Authentication works (login/logout)
- [ ] Database queries work (tenant isolation)
- [ ] File uploads work (R2 storage)
- [ ] Session management works (KV storage)
- [ ] API endpoints respond correctly

### Smoke Tests
- [ ] Critical user flows tested
- [ ] Multi-tenant isolation verified
- [ ] Performance acceptable (< 500ms response time)
- [ ] No console errors in browser
- [ ] Mobile responsive (if applicable)

### Rollback Readiness
- [ ] Know how to rollback Workers: `npx wrangler rollback`
- [ ] Know how to rollback database: `drizzle-kit migrate:rollback`
- [ ] Emergency contacts notified
- [ ] Linear issue updated with deployment status

## Rollback Triggers

Rollback immediately if:
- [ ] Smoke tests fail
- [ ] Critical user flow broken
- [ ] 500 errors in production
- [ ] Database connection failures
- [ ] Authentication broken
- [ ] Multi-tenant isolation breach

## Post-Deployment Documentation

- [ ] Update Linear issue with deployment notes
- [ ] Document any manual steps taken
- [ ] Update team on deployment status
- [ ] Schedule postmortem if issues occurred
- [ ] Update runbook with any new learnings
