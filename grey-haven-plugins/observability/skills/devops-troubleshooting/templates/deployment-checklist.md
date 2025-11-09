# Deployment Checklist

Comprehensive checklist for safe production deployments to Cloudflare Workers, PlanetScale databases, and Grey Haven infrastructure.

---

## Pre-Deployment Verification

### Code Review and Testing

- [ ] **Pull Request Approved**: PR reviewed by at least 2 team members
- [ ] **All Tests Passing**: CI/CD pipeline green (unit, integration, e2e)
  ```bash
  npm run test
  npm run test:integration
  npm run test:e2e
  ```
- [ ] **Test Coverage**: Coverage ≥ 80% for new code
  ```bash
  npm run test:coverage
  ```
- [ ] **No Linter Errors**: ESLint, Prettier, type checking clean
  ```bash
  npm run lint
  npm run type-check
  ```
- [ ] **Security Scan**: No high/critical vulnerabilities
  ```bash
  npm audit
  snyk test
  ```

### Bundle and Dependencies

- [ ] **Bundle Size Check**: Worker bundle < 1MB (Free) or < 10MB (Paid)
  ```bash
  npm run build
  ls -lh dist/worker.js
  ```
- [ ] **Tree Shaking Verified**: No unnecessary dependencies bundled
  ```bash
  npm run build -- --analyze
  ```
- [ ] **Dependencies Updated**: All deps up-to-date and compatible
  ```bash
  npm outdated
  npm update
  ```
- [ ] **Lock File Committed**: package-lock.json or bun.lockb committed
- [ ] **Node Version Verified**: Matches production (check .nvmrc)

### Configuration

- [ ] **Environment Variables**: All required secrets set in Cloudflare
  ```bash
  wrangler secret list
  # Verify: DATABASE_URL, API_KEYS, etc.
  ```
- [ ] **wrangler.toml Updated**: Correct routes, bindings, vars
- [ ] **Database Migrations Ready**: Schema changes tested in staging
  ```bash
  pscale deploy-request create greyhaven-db migration-name
  ```
- [ ] **Feature Flags Configured**: New features behind flags if needed
- [ ] **Rate Limits Configured**: API rate limits set appropriately

### Documentation

- [ ] **CHANGELOG Updated**: User-facing changes documented
- [ ] **API Docs Updated**: If API changes, docs reflect new behavior
- [ ] **Runbook Updated**: New deployment procedures documented
- [ ] **Rollback Plan Documented**: Clear steps to revert if needed

### Staging Verification

- [ ] **Deployed to Staging**: Changes tested in staging environment
  ```bash
  wrangler deploy --env staging
  ```
- [ ] **Smoke Tests Passed**: Basic functionality verified in staging
- [ ] **Performance Testing**: Load testing completed, no degradation
  ```bash
  npm run load-test -- --env staging
  ```
- [ ] **Database Migration Tested**: Schema changes work in staging branch
  ```bash
  pscale branch create greyhaven-db staging-migration
  ```

### Team Coordination

- [ ] **Deployment Window Scheduled**: Team aware of deployment time
- [ ] **Oncall Engineer Notified**: Oncall knows about deployment
- [ ] **Stakeholders Informed**: Product/Customer Success aware if needed
- [ ] **Rollback Owner Identified**: Who will execute rollback if needed
- [ ] **Communication Channel Ready**: Slack channel for deployment updates

---

## Deployment Execution

### Pre-Deployment Backup

- [ ] **Database Backup Created**: Snapshot before schema changes
  ```bash
  pscale backup create greyhaven-db main
  ```
- [ ] **Current Version Tagged**: Git tag for current production state
  ```bash
  git tag -a prod-YYYY-MM-DD-HH-MM -m "Pre-deployment snapshot"
  git push origin prod-YYYY-MM-DD-HH-MM
  ```
- [ ] **Environment Config Exported**: Backup current secrets/vars
  ```bash
  wrangler secret list > secrets-backup-YYYY-MM-DD.txt
  ```

### Database Migration (If Applicable)

- [ ] **Migration Script Reviewed**: SQL reviewed for correctness
- [ ] **Deploy Request Created**: PlanetScale deploy request opened
  ```bash
  pscale deploy-request create greyhaven-db migration-name
  ```
- [ ] **Schema Diff Reviewed**: Changes reviewed in PlanetScale UI
- [ ] **Migration Deployed**: Deploy request merged to main
  ```bash
  pscale deploy-request deploy greyhaven-db <request-number>
  ```
- [ ] **Migration Verified**: Schema changes applied correctly
  ```bash
  pscale shell greyhaven-db main
  \d tablename  -- Verify schema
  ```

### Worker Deployment

- [ ] **Final Build**: Fresh production build
  ```bash
  npm run build
  ```
- [ ] **Bundle Size Verified**: Within limits
  ```bash
  ls -lh dist/worker.js
  ```
- [ ] **Deployment Started**: Deploy to production
  ```bash
  wrangler deploy --env production
  ```
- [ ] **Deployment Confirmed**: Check deployment status
  ```bash
  wrangler deployments list
  ```
- [ ] **Global Propagation Verified**: Changes live in all regions (~60s)
  ```bash
  # Test multiple regions
  curl -H "CF-IPCountry: US" https://api.greyhaven.io/health
  curl -H "CF-IPCountry: EU" https://api.greyhaven.io/health
  ```

### Configuration Updates

- [ ] **Secrets Updated**: New secrets deployed if needed
  ```bash
  wrangler secret put NEW_SECRET_KEY
  ```
- [ ] **Environment Variables Set**: New vars updated in wrangler.toml
- [ ] **Feature Flags Enabled**: Gradual rollout if using flags
- [ ] **DNS Updates**: Any DNS changes propagated (if applicable)

---

## Post-Deployment Monitoring

### Immediate Verification (First 5 Minutes)

- [ ] **Health Check Passing**: `/health` endpoint returns 200
  ```bash
  curl -i https://api.greyhaven.io/health
  # Expected: HTTP/2 200
  ```
- [ ] **Basic Functionality**: Core features work end-to-end
- [ ] **Error Rate Check**: No spike in 5xx errors
  ```bash
  wrangler tail --format pretty | grep -i error
  ```
- [ ] **Latency Check**: Response times normal (p95 < 500ms)
- [ ] **Database Connectivity**: Queries executing successfully
  ```bash
  pscale shell greyhaven-db main --execute "SELECT 1"
  ```

### Short-Term Monitoring (First 30 Minutes)

- [ ] **Grafana Dashboard**: Metrics look normal
  - Error rate < 0.1%
  - p95 latency < 500ms
  - Database pool utilization < 80%
  - Worker CPU < 40ms average
- [ ] **Logs Review**: No unexpected errors in logs
  ```bash
  wrangler tail --format pretty
  ```
- [ ] **User Reports**: No complaints in support channels
- [ ] **Synthetic Monitoring**: Automated tests passing
  ```bash
  npm run smoke-test:production
  ```
- [ ] **Alerts Silent**: No alerts firing in PagerDuty/Datadog

### Medium-Term Monitoring (First 2 Hours)

- [ ] **Performance Stable**: No degradation in latency or throughput
- [ ] **Error Budget**: Within SLA limits (99.9% uptime)
- [ ] **Database Performance**: No slow queries introduced
  ```bash
  pscale database insights greyhaven-db main --slow-queries
  ```
- [ ] **Cache Hit Rates**: Cache performance normal (if applicable)
- [ ] **Third-Party APIs**: All external dependencies healthy

### Long-Term Monitoring (First 24 Hours)

- [ ] **User Metrics**: DAU, engagement, conversion rates normal
- [ ] **Business Metrics**: No negative impact on KPIs
- [ ] **Cost Monitoring**: No unexpected increases in infrastructure costs
  ```bash
  # Check Cloudflare Workers analytics
  # Check PlanetScale billing dashboard
  ```
- [ ] **Cumulative Error Budget**: SLA compliance maintained

---

## Rollback Procedures

### When to Rollback

**Rollback immediately if**:
- Error rate > 5% for > 5 minutes
- p95 latency > 3x baseline for > 5 minutes
- Critical functionality broken
- Database corruption detected
- Security vulnerability introduced

**Consider rollback if**:
- Error rate > 1% for > 10 minutes
- p95 latency > 2x baseline for > 10 minutes
- Non-critical functionality broken
- User complaints increasing rapidly

### Worker Rollback

- [ ] **Identify Previous Version**: Get previous deployment ID
  ```bash
  wrangler deployments list
  ```
- [ ] **Rollback to Previous**: Promote previous deployment
  ```bash
  wrangler rollback --message "Rolling back due to [REASON]"
  ```
- [ ] **Verify Rollback**: Check logs and metrics
  ```bash
  wrangler tail --format pretty
  ```
- [ ] **Confirm Stable**: Error rate and latency back to normal

### Database Rollback

- [ ] **Assess Schema Changes**: Determine if rollback needed
- [ ] **Create Revert Request**: PlanetScale deploy request for revert
  ```bash
  pscale deploy-request create greyhaven-db revert-migration-name
  ```
- [ ] **Deploy Revert**: Merge revert request
  ```bash
  pscale deploy-request deploy greyhaven-db <request-number>
  ```
- [ ] **Verify Schema**: Confirm schema reverted correctly

### Code Rollback (Git)

- [ ] **Revert Commit**: Create revert commit
  ```bash
  git revert <commit-hash>
  git push origin main
  ```
- [ ] **Deploy Reverted Code**: Follow deployment steps with reverted code
  ```bash
  wrangler deploy --env production
  ```

### Communication

- [ ] **Team Notified**: Alert team in deployment channel
  ```
  🚨 ROLLBACK: Deployment rolled back due to [REASON]
  - Error rate: X%
  - Decision made by: [NAME]
  - Previous deployment restored
  ```
- [ ] **Stakeholders Informed**: Product/CS aware if user-facing
- [ ] **Post-Mortem Scheduled**: Schedule incident review
- [ ] **Incident Report Created**: Document what happened

---

## Post-Deployment Tasks

### Immediate (Day 1)

- [ ] **Monitor Metrics**: Continue watching dashboards
- [ ] **Review Logs**: Check for any anomalies
- [ ] **User Feedback**: Monitor support channels
- [ ] **Update Status Page**: Mark deployment as complete (if using)

### Short-Term (Week 1)

- [ ] **Performance Review**: Analyze deployment impact on metrics
- [ ] **Cost Review**: Check infrastructure costs
- [ ] **User Metrics**: Verify no negative impact on engagement
- [ ] **Technical Debt**: Address any shortcuts taken during deployment

### Documentation

- [ ] **Deployment Notes**: Document any issues encountered
- [ ] **Runbook Updates**: Update deployment procedures if needed
- [ ] **Lessons Learned**: Share with team (if issues occurred)

---

## Deployment Types

### Standard Deployment (Non-Breaking)

Use **full checklist** above for:
- New features (behind feature flags)
- Bug fixes
- Performance improvements
- Dependency updates

**Deployment Window**: Any time (prefer off-peak)

### Breaking Change Deployment

Additional requirements:
- [ ] **Migration Guide**: Document breaking changes for users
- [ ] **Backward Compatibility**: Maintain for 1 version if possible
- [ ] **Deprecation Warnings**: Add warnings before breaking change
- [ ] **Communication Plan**: Email users, update docs, blog post

**Deployment Window**: Scheduled maintenance window

### Emergency Hotfix

Streamlined checklist:
- [ ] **Critical Bug Identified**: Production outage or security issue
- [ ] **Fix Reviewed**: At least 1 reviewer (can be async)
- [ ] **Tests Passing**: Automated tests green
- [ ] **Deploy Immediately**: Skip staging if SEV1
  ```bash
  wrangler deploy --env production
  ```
- [ ] **Monitor Closely**: Watch for 30 minutes minimum
- [ ] **Retrospective**: Full incident report after

**Deployment Window**: Immediately upon fix

### Database-Only Migration

- [ ] **Create Branch**: PlanetScale branch for migration
  ```bash
  pscale branch create greyhaven-db migration-name
  ```
- [ ] **Test Migration**: Verify in branch
- [ ] **Deploy Request**: Create and review
- [ ] **Merge to Main**: Apply to production
- [ ] **Verify Schema**: Confirm changes applied
- [ ] **Monitor Queries**: Watch for slow queries

---

## Emergency Contacts

**On-Call Engineer**: [Name] - [Phone/Slack]
**Engineering Manager**: [Name] - [Phone/Slack]
**DevOps Lead**: [Name] - [Phone/Slack]
**Database Admin**: [Name] - [Phone/Slack]

**Escalation Path**:
1. On-Call Engineer (immediate)
2. Engineering Manager (if >30min)
3. CTO (if SEV1 >1hr)

---

## Template Notes

**Customize this checklist for your team**:
- Add team-specific requirements
- Remove items that don't apply
- Adjust thresholds (error rates, latency, etc.)

**Save this checklist**:
- Copy to GitHub issues for each deployment
- Use as PR description template
- Maintain in documentation

**Checklist Versioning**:
- Version: 1.0
- Last Updated: YYYY-MM-DD
- Next Review: YYYY-MM-DD

---

Return to [templates index](INDEX.md)
