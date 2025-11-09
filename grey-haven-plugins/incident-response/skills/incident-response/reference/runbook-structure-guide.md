# Runbook Structure Guide

Best practices for writing effective, actionable runbooks that enable fast incident response.

## Runbook Template

```markdown
# [Problem Title]

**Alert**: [Alert name that triggers this runbook]
**Severity**: [SEV1/SEV2/SEV3]
**Owner**: [Team/Person responsible]
**Last Updated**: [YYYY-MM-DD]

## Problem Description

[1-2 sentence description of the problem]

**Symptoms**:
- [Observable symptom 1]
- [Observable symptom 2]

**Impact**:
- Customer Impact: [What users experience]
- Business Impact: [Revenue, SLA, etc.]

---

## Diagnosis Steps

### Step 1: [Check X]

```bash
# Command to run
[command]

# Expected output
[what you should see if healthy]

# Problem indicator
[what you see if there's an issue]
```

### Step 2: [Verify Y]

```bash
[commands]
```

**If X, then**:
- Go to Step 3
- Skip to [Mitigation](#mitigation)

---

## Mitigation

### Quick Fix (Temporary)

**If**: [Condition when to use quick fix]

```bash
# Commands to mitigate
[command 1]
[command 2]
```

**Verification**:
```bash
# Check fix worked
[verification command]
```

### Permanent Fix

**After** temporary mitigation:

1. [Action 1]
2. [Action 2]
3. [Action 3]

---

## Escalation

**Escalate if**:
- Mitigation doesn't work after 15 minutes
- Issue is SEV1 and unresolved after 30 minutes
- Root cause unclear

**Escalation Path**:
1. @oncall-engineer → @team-lead (15 min)
2. @team-lead → @engineering-manager (30 min)
3. @engineering-manager → @vp-engineering (60 min)

---

## Related Links

- Alert: [Link to alert definition]
- Dashboard: [Link to Grafana/metrics]
- Documentation: [Link to relevant docs]
- Past Incidents: [Link to similar incidents]
```

---

## Runbook Best Practices

### 1. Write for Future You

- Assume zero context (you're woken up at 3am)
- No jargon or tribal knowledge
- Step-by-step instructions (no skipped steps)

### 2. Include Commands

**Bad** (too vague):
```
Check if the database is healthy
```

**Good** (specific command):
```bash
# Check database health
pscale shell greyhaven-db main --execute "SELECT 1"

# Expected: Should return "1"
# Problem: Connection timeout or error
```

### 3. Decision Trees

Use if/then logic for common scenarios:

```
IF error rate >10%:
  └─ Check recent deployments
     ├─ Deployment in last hour? → Rollback
     └─ No recent deployment? → Check database

IF error rate <10% BUT latency high:
  └─ Check external dependencies
     ├─ External API slow? → Enable circuit breaker
     └─ Database slow? → Check slow queries
```

### 4. Success Criteria

Always include verification:

```bash
# After fix, verify:
curl https://api.greyhaven.io/health
# Expected: HTTP 200, {"status": "healthy"}

# Check metrics:
# Error rate: <0.1%
# p95 latency: <500ms
```

---

## Runbook Examples

### Example 1: Database Connection Failure

```markdown
# Database Connection Failure

**Alert**: DatabaseConnectionTimeout
**Severity**: SEV1
**Owner**: Database Team

## Diagnosis

```bash
# 1. Check database status
pscale db status greyhaven-db main

# Healthy output:
# Status: Healthy
# Connections: 45/100

# Problem indicators:
# Status: Unhealthy
# OR Connections: 100/100 (exhausted)
```

## Mitigation

### If Connection Pool Exhausted:

```bash
# Restart application pods (releases connections)
kubectl rollout restart deployment/api-server

# Verify recovery
kubectl get pods -l app=api-server
# All pods should show Running and Ready
```

### If Database Down:

```bash
# Promote replica to primary
pscale db promote greyhaven-db replica-1

# Update app DATABASE_URL
wrangler secret put DATABASE_URL
# Enter new connection string
```

## Escalation

Escalate to @database-oncall if:
- Connection pool normal but still timeouts
- Database promotion fails
- Issue unresolved after 30 minutes
```

### Example 2: API Latency High

```markdown
# API High Latency

**Alert**: APILatencyHigh (p95 >1s)
**Severity**: SEV2

## Diagnosis

```bash
# 1. Check distributed trace
open https://jaeger.greyhaven.io
# Search for recent slow requests (>1s)
# Identify which service is slow in the trace

# 2. Check database slow queries
pscale database insights greyhaven-db main --slow-queries
# Look for queries >100ms

# 3. Check external API status
curl -w "\nTotal: %{time_total}s\n" https://api.partner.com/health
# Should be <500ms
```

## Mitigation

### If Database Slow:
```bash
# Check for missing indexes
# Add index for frequently queried columns
# (See database optimization runbook)
```

### If External API Slow:
```bash
# Enable circuit breaker (stops calling slow API)
# Deploy code with circuit breaker enabled
# External API calls will fail fast instead of timing out
```

## Escalation

Escalate to @backend-oncall after 2 hours if unresolved
```

---

## Runbook Maintenance

### Regular Review

- **Frequency**: Quarterly or after each incident
- **Update**: Commands, endpoints, team contacts
- **Test**: Run through runbook in staging
- **Archive**: Remove outdated runbooks

### Version Control

```bash
# Store runbooks in Git
docs/runbooks/database-connection-failure.md

# Review in PRs
# Track changes over time
# Easy to roll back if needed
```

### Testing Runbooks

**Chaos Engineering**:
- Intentionally trigger failure scenarios
- Follow runbook step-by-step
- Verify commands work as documented
- Update runbook based on learnings

**Example Test**:
```bash
# Test database failover runbook
# 1. Take database offline (staging)
# 2. Follow runbook to promote replica
# 3. Verify application recovers
# 4. Document time taken
# 5. Update runbook with improvements
```

---

## Common Mistakes

### Mistake 1: Too High Level

**Bad**:
```
Fix the database connection issue
```

**Good**:
```
1. SSH to database server: ssh ubuntu@db-primary.greyhaven.io
2. Check disk space: df -h /var/lib/postgresql
3. If disk >90% full: rm /var/lib/postgresql/logs/*.gz
4. Restart PostgreSQL: sudo systemctl restart postgresql
```

### Mistake 2: Assumes Context

**Bad**:
```
Use the usual commands to restart the workers
```

**Good**:
```
kubectl rollout restart deployment/api-server
kubectl rollout status deployment/api-server
# Wait for: "deployment 'api-server' successfully rolled out"
```

### Mistake 3: No Verification

**Bad**:
```
Restart the service
(runbook ends here)
```

**Good**:
```
kubectl rollout restart deployment/api-server

Verify:
- curl https://api.greyhaven.io/health (should return 200)
- Check Grafana: error rate <0.1%
- Monitor for 10 minutes
```

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Incidents that led to runbook creation
- **Severity Matrix**: [incident-severity-matrix.md](incident-severity-matrix.md) - When to use runbooks
- **Templates**: [Runbook Template](../templates/runbook-template.md) - Copy-paste template

---

Return to [reference index](INDEX.md)
