# SEV1: Critical Database Outage

Complete PostgreSQL primary failure causing total service outage, resolved through replica promotion and disk space remediation. Demonstrates full incident response workflow from detection to blameless postmortem.

## Incident Summary

**Incident ID**: INC-2024-1205-001
**Severity**: SEV1 (Critical - Total Outage)
**Date**: December 5, 2024
**MTTR**: 45 minutes (08:15 → 09:00 UTC)
**Impact**: 100% service outage, all customers affected
**Revenue Loss**: ~$37,500 (45 min × $50K/hour)
**Root Cause**: Disk full on PostgreSQL primary, caused by unbounded log growth
**Status**: Resolved, prevention measures in place

---

## Incident Timeline

| Time (UTC) | Event | Action | Owner |
|------------|-------|--------|-------|
| 08:15:23 | PagerDuty alert: Database connection timeout | Oncall paged | Auto |
| 08:15:45 | IC (Incident Commander) joins, declares SEV1 | War room created (#incident-001) | @jane |
| 08:16:00 | All services returning 500 errors | Verified 100% error rate | @jane |
| 08:17:30 | Database primary unreachable | SSH failed, console shows disk full | @mike |
| 08:19:00 | Attempted to clear disk space | rm /var/log/postgresql/*.gz | @mike |
| 08:21:15 | Disk clear failed (insufficient space) | Only 100MB freed, need 10GB | @mike |
| 08:23:00 | Decision: Promote replica to primary | Replica confirmed healthy | @jane |
| 08:25:30 | Replica promotion started | pscale db promote replica-1 | @mike |
| 08:30:00 | Replica promoted successfully | New primary accepting connections | @mike |
| 08:32:00 | App servers reconfigured | DATABASE_URL updated, pods restarted | @sarah |
| 08:35:00 | Health checks passing | 0% error rate, services recovering | @sarah |
| 08:40:00 | Customer comms sent | Status page updated, email sent | @alex |
| 08:45:00 | Full traffic restored | All services nominal | @jane |
| 09:00:00 | Old primary recovered | Disk cleaned, demoted to replica | @mike |
| 09:15:00 | Incident closed, postmortem scheduled | Blameless review in 2 hours | @jane |

**Total Duration**: 45 minutes from detection to full recovery

---

## Severity Classification

### Why SEV1?

**SEV1 Criteria Met**:
- ✅ Complete outage (100% error rate)
- ✅ All customers affected (no workaround)
- ✅ Revenue stopped ($50K/hour e-commerce site)
- ✅ Data unavailable (read/write operations failing)
- ✅ SLO violation >50% (99.9% uptime SLA breached)

**Business Impact**:
```
Revenue Loss: $37,500 (45 minutes downtime)
Customers Affected: 100% (~50,000 active users)
Failed Transactions: ~750 orders
Support Tickets: 127 (vs baseline 2/hour)
Brand Damage: Social media complaints: 43
SLA Breach: Yes (99.9% uptime SLA requires <43.2min/month)
```

---

## Detection

### Initial Alert

**PagerDuty Alert** (08:15:23 UTC):
```
ALERT: [P1] Database Connection Timeout
Service: postgresql-primary
Error: FATAL: could not write to file "pg_log/postgresql-2024-12-05.log": No space left on device
Threshold: >10 failed connections in 1 minute
Current: 147 failed connections
Runbook: https://docs.greyhaven.io/runbooks/database-connection-failure
```

**Monitoring Dashboards**:
```
Grafana: Database Health Dashboard
- Connection Pool: 0/100 (100% exhausted)
- Query Success Rate: 0% (was 99.99%)
- Disk Usage: 100% (was 75% 1 hour ago)
- Replication Lag: 0s (replica healthy)
```

**Application Symptoms**:
```
API Error Rate: 100% (HTTP 500)
Error Message: "Database connection failed: Connection refused"
User Impact: "We're sorry, something went wrong" error page
Failed Requests: ~15,000 in first minute
```

---

## Incident Command Structure

### Roles Assigned (08:16:00)

**Incident Commander** (@jane):
- Overall coordination and decision authority
- Communication hub (internal and external)
- Timeline management and scribe delegation
- Resource allocation (bring in experts as needed)

**Technical Lead** (@mike):
- Diagnosis and remediation execution
- Database expertise, infrastructure access
- Implementation of technical fixes

**Communications Lead** (@alex):
- Status page updates
- Customer emails (external communication)
- Executive briefings
- Support team coordination

**App Infra Lead** (@sarah):
- Application server reconfiguration
- Deployment coordination
- Health check verification

**Scribe** (@tom):
- Real-time timeline documentation
- Slack channel updates
- Action item tracking
- Postmortem notes

---

## Investigation

### Diagnosis Process

**Step 1: Verify Database Connectivity** (08:16:30)
```bash
# Attempt connection to primary
psql -h db-primary.greyhaven.io -U app_user -d production

Result: Connection timeout after 30 seconds
Error: FATAL: could not write to file "pg_log/postgresql-2024-12-05.log": No space left on device
```

**Step 2: Check Disk Space** (08:17:30)
```bash
# SSH to database primary
ssh ubuntu@db-primary.greyhaven.io

# Check disk usage
df -h /var/lib/postgresql

Filesystem      Size  Used  Avail  Use%  Mounted on
/dev/nvme0n1    500G  500G  0      100%  /var/lib/postgresql

# Identify large files
du -sh /var/lib/postgresql/*

450G    /var/lib/postgresql/14/main/pg_log
40G     /var/lib/postgresql/14/main/base
10G     /var/lib/postgresql/14/main/pg_wal
```

**Root Cause Identified**: PostgreSQL log directory filled entire disk (450GB of logs!)

**Step 3: Check Replica Health** (08:19:00)
```bash
# Verify replica is healthy and ready for promotion
pscale db status replica-1

Status: Healthy
Replication Lag: 0 seconds
Disk Usage: 45% (225GB used of 500GB)
Accepting Connections: Yes
Last Backup: 2 hours ago
```

**Replica confirmed healthy** - safe to promote

---

## Root Cause Analysis (5 Whys)

**Why 1**: Why did the database go down?
→ Because the primary database ran out of disk space

**Why 2**: Why did it run out of disk space?
→ Because PostgreSQL logs filled the entire disk (450GB)

**Why 3**: Why did logs grow to 450GB?
→ Because log rotation was disabled and logs accumulated for 6 months

**Why 4**: Why was log rotation disabled?
→ Because the `log_truncate_on_rotation` config was accidentally set to `off` during a migration 6 months ago

**Why 5**: Why was this config change not caught?
→ Because configuration changes are not code-reviewed and there was no disk monitoring alert for >90% usage

**ROOT CAUSE**: Missing disk monitoring alerts + configuration change without code review

### Contributing Factors

1. **No Disk Monitoring**: No alert for disk usage >90%
2. **Log Rotation Disabled**: Config change not reviewed
3. **No Log Size Limits**: PostgreSQL allowed unbounded log growth
4. **Slow Degradation**: Took 6 months to fill, no gradual alerts
5. **Manual Process**: Log cleanup not automated

---

## Mitigation & Resolution

### Immediate Actions (08:23:00 - 08:35:00)

**Decision**: Promote replica to new primary (faster than clearing disk)

**Replica Promotion**:
```bash
# Promote replica to primary (PlanetScale)
pscale db promote greyhaven-db replica-1

Promoting replica-1 to primary...
✓ Replica promoted successfully (5 minutes)
✓ New primary accepting connections
✓ Replication from old primary disabled

New primary: db-primary-new.greyhaven.io
```

**App Reconfiguration**:
```bash
# Update DATABASE_URL secret in Cloudflare Workers
wrangler secret put DATABASE_URL
# Enter new connection string: postgresql://...@db-primary-new.greyhaven.io/production

# Restart application pods to pick up new secret
kubectl rollout restart deployment/api-server

# Verify connections
kubectl logs -f deployment/api-server | grep "Database connected"
✓ Database connected to db-primary-new.greyhaven.io
```

**Verification** (08:35:00):
```
Health Checks: ✅ Passing
Error Rate: 0% (back to baseline)
Database Connections: 85/100 (healthy)
API Latency: p95 200ms (normal)
Customer Impact: Resolved
```

### Temporary Fix Applied

- Promoted replica to primary: 5 minutes
- Reconfigured applications: 7 minutes
- Total mitigation time: 12 minutes

---

### Permanent Fixes (08:45:00 - 09:00:00)

**Fix 1: Recover Old Primary as Replica**
```bash
# SSH to old primary
ssh ubuntu@db-primary-old.greyhaven.io

# Clear log directory
cd /var/lib/postgresql/14/main/pg_log
rm -rf *  # Freed 450GB

# Enable log rotation (permanent fix)
# postgresql.conf
log_truncate_on_rotation = on
log_rotation_age = 1d
log_rotation_size = 100MB

# Restart PostgreSQL
sudo systemctl restart postgresql@14-main

# Demote to replica and start replication from new primary
pscale db demote greyhaven-db old-primary
```

**Fix 2: Add Disk Monitoring**
```yaml
# prometheus/alerts/database.yml
- alert: DatabaseDiskUsageHigh
  expr: (node_filesystem_avail_bytes{mountpoint="/var/lib/postgresql"} / node_filesystem_size_bytes{mountpoint="/var/lib/postgresql"}) < 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Database disk >90% full"
    description: "{{ $labels.instance }} has only {{ $value | humanizePercentage }} disk space remaining"
    runbook: "https://docs.greyhaven.io/runbooks/database-disk-full"
```

---

## Communication

### Internal Updates (Slack #incident-001)

**08:16 - Incident Start**:
```
🚨 SEV1 INCIDENT DECLARED 🚨
Incident ID: INC-2024-1205-001
Impact: 100% service outage, database down
Incident Commander: @jane
Technical Lead: @mike
Status: Investigating

War room: Zoom link (https://zoom.us/j/incident001)
Next update: 08:30 (or when status changes)
```

**08:25 - Mitigation Started**:
```
📊 UPDATE #1 (T+10 minutes)
Root cause: Database primary disk full (450GB logs)
Mitigation: Promoting replica to primary (ETA: 5 min)
Impact: Still 100% down, waiting for replica promotion
Next update: 08:40
```

**08:35 - Services Recovering**:
```
✅ UPDATE #2 (T+20 minutes)
Replica promoted successfully
Applications reconfigured and restarted
Error rate: 0% (recovered)
Impact: Services coming back online
Next update: 08:50 or when fully resolved
```

**08:45 - Incident Resolved**:
```
🎉 INCIDENT RESOLVED (T+30 minutes)
All services operational
Error rate: 0%
Health checks: Passing
Customer impact: Mitigated
Old primary: Being recovered as replica

Postmortem: 11:00 UTC (2 hours)
Timeline: (link to internal doc)
```

### External Communications

**Status Page Update** (08:16):
```
🔴 INVESTIGATING - Major Service Disruption

We are currently experiencing a major service disruption affecting all users.
Our team is actively investigating and working to restore service as quickly as possible.

Started: 08:15 UTC
Next update: 08:30 UTC
```

**Status Page Update** (08:40):
```
🟡 IDENTIFIED - Database Issues Resolved, Services Recovering

We have identified and resolved the database issue causing the service disruption.
Services are currently recovering and should be fully operational within 5 minutes.

Started: 08:15 UTC
Identified: 08:25 UTC
Recovering: 08:35 UTC
Next update: When resolved
```

**Status Page Update** (08:45):
```
🟢 RESOLVED - All Services Operational

All services have been restored and are operating normally.
We apologize for the disruption and are conducting a full post-incident review.

Started: 08:15 UTC
Resolved: 08:45 UTC
Duration: 30 minutes
```

**Customer Email** (09:00):
```
Subject: Service Disruption Resolved - December 5, 2024

Dear Grey Haven Customers,

At 08:15 UTC today, we experienced a service disruption that affected all users for approximately 30 minutes. Our services are now fully restored and operating normally.

What happened: A database storage issue prevented our application from processing requests.

What we did: Our team immediately identified the issue and promoted a backup database to restore service within 30 minutes.

What we're doing next: We've implemented additional monitoring to prevent this from happening again and are conducting a full post-incident review.

We sincerely apologize for the inconvenience.

Grey Haven Engineering Team
```

---

## Prevention Measures

### Immediate Actions (Completed Same Day)

- [x] Added disk usage monitoring with 90% threshold alert (08:50)
- [x] Enabled PostgreSQL log rotation on all database instances (09:00)
- [x] Created runbook for disk-full scenario (09:30)
- [x] Updated replica promotion runbook with lessons learned (10:00)

### Short-Term Actions (Completed Within 1 Week)

- [x] Automated log cleanup cron job (every 6 hours, delete logs >7 days) - Day 2
- [x] Configuration change review process (all DB config changes require PR) - Day 3
- [x] Automated replica promotion script (reduce manual steps) - Day 5
- [x] Load testing for failover scenarios (verify replica can handle load) - Day 7

### Long-Term Actions (Completed Within 1 Month)

- [x] Database configuration management (Terraform/Ansible, version controlled) - Week 2
- [x] Automated failover (detect primary failure, auto-promote replica) - Week 3
- [x] Chaos engineering: monthly failover drills - Week 4
- [x] Disk space forecasting (predict when disk will fill) - Week 4

---

## Blameless Postmortem

### What Went Well ✅

1. **Fast Detection**: Alert fired within seconds of failure
2. **Clear Incident Command**: IC established roles immediately, no confusion
3. **Healthy Replica**: Replica was healthy and ready for promotion
4. **Quick Decision**: IC decided to promote replica vs trying to fix primary (saved time)
5. **Good Communication**: Regular updates every 15 minutes, status page updated
6. **Fast MTTR**: 45 minutes from detection to full recovery

### What Went Wrong ❌

1. **No Disk Monitoring**: Disk filled over 6 months without alert
2. **Config Change Not Reviewed**: Log rotation disabled 6 months ago, not caught
3. **No Gradual Alerts**: No warning at 80%, 90% disk usage
4. **Manual Failover**: Replica promotion was manual, took 5 minutes
5. **No Runbook**: Had to figure out steps during incident
6. **No Recent Failover Test**: Last tested failover 6 months ago

### Action Items (Tracked in Linear)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add disk usage alerts (>80%, >90%) | @mike | Dec 5 | ✅ Done |
| Enable log rotation on all DB instances | @mike | Dec 5 | ✅ Done |
| Create disk-full runbook | @sarah | Dec 6 | ✅ Done |
| Implement config change review (PR required) | @jane | Dec 8 | ✅ Done |
| Automate replica promotion | @mike | Dec 12 | ✅ Done |
| Monthly failover drills | @team | Ongoing | 🔄 Scheduled |
| Database config as code (Terraform) | @mike | Dec 20 | ✅ Done |
| Disk forecasting dashboard | @sarah | Dec 20 | ✅ Done |

### Metrics

**Before Incident**:
- Disk monitoring: None
- Failover automation: Manual
- Config management: Ad-hoc
- Runbooks: Incomplete

**After Incident**:
- Disk monitoring: ✅ Alerts at 80%, 90%
- Failover automation: ✅ Automated replica promotion
- Config management: ✅ Terraform, code-reviewed
- Runbooks: ✅ Complete for disk/failover scenarios

**MTTR Improvement**:
- Current incident: 45 minutes (manual)
- Future incidents: ~5 minutes (automated failover)
- **90% MTTR reduction**

---

## Related Documentation

- **Similar Incidents**: None (first database outage)
- **Runbooks Updated**: [Database Disk Full](../../reference/runbook-structure-guide.md), [Replica Promotion](../../reference/runbook-structure-guide.md)
- **Monitoring**: [Disk Usage Dashboard](https://grafana.greyhaven.io/d/disk-usage)
- **Postmortem Recording**: [Video](https://drive.google.com/postmortem-001) (internal only)

---

Return to [examples index](INDEX.md)
