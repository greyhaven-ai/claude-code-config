# Incident Report: [INCIDENT TITLE]

**Date**: [YYYY-MM-DD]
**Incident ID**: [INC-XXXXX]
**Severity**: [SEV1 / SEV2 / SEV3]
**Status**: [Investigating / Mitigated / Resolved]
**Report Author**: [Name]
**Last Updated**: [YYYY-MM-DD HH:MM UTC]

---

## Executive Summary

**TL;DR** (1-2 sentences):
[FILL IN: Brief description of what happened and the impact]

**Impact**:
- **Users Affected**: [Number or percentage]
- **Duration**: [HH:MM from start to resolution]
- **Business Impact**: [Revenue loss, SLA breach, customer complaints, etc.]

**Root Cause**:
[FILL IN: One sentence explaining the root cause]

**Resolution**:
[FILL IN: One sentence explaining how it was resolved]

---

## Incident Timeline

| Time (UTC) | Event | Action Taken |
|------------|-------|--------------|
| [HH:MM] | [FILL IN: First symptom detected] | [FILL IN: What was done] |
| [HH:MM] | [FILL IN: Incident declared] | [FILL IN: Who was paged] |
| [HH:MM] | [FILL IN: Investigation started] | [FILL IN: What was checked] |
| [HH:MM] | [FILL IN: Root cause identified] | [FILL IN: How it was found] |
| [HH:MM] | [FILL IN: Fix deployed] | [FILL IN: What was deployed] |
| [HH:MM] | [FILL IN: Incident mitigated] | [FILL IN: Impact reduced] |
| [HH:MM] | [FILL IN: Full resolution] | [FILL IN: All systems normal] |

---

## Symptoms and Detection

### Initial Alert

**How we detected the issue**:
[FILL IN: Monitoring alert, customer report, internal detection, etc.]

**Alert Details**:
```
[FILL IN: Paste alert details, error messages, or logs]
```

**Affected Systems**:
- [FILL IN: System 1 - Description of impact]
- [FILL IN: System 2 - Description of impact]
- [FILL IN: System 3 - Description of impact]

### Metrics and Observations

**Error Rates**:
```
[FILL IN: Baseline vs incident error rates]
Example:
Baseline: 0.01% errors
Incident: 15% errors (1500x increase)
```

**Performance Degradation**:
```
[FILL IN: Latency, throughput, or other performance metrics]
Example:
p50 latency: 200ms → 2000ms (10x slower)
p95 latency: 500ms → 5000ms (10x slower)
```

**Infrastructure Metrics**:
```
[FILL IN: CPU, memory, disk, network, database connections, etc.]
Example:
Database connections: 20/100 → 100/100 (exhausted)
Worker CPU: 20% → 95% (saturated)
```

---

## Impact Assessment

### User Impact

**Number of Users Affected**:
[FILL IN: Exact number, percentage, or "All users"]

**Affected Functionality**:
- [FILL IN: Feature 1 - Completely unavailable / Degraded / Slow]
- [FILL IN: Feature 2 - Completely unavailable / Degraded / Slow]

**User Experience**:
```
[FILL IN: Describe what users experienced]
Example:
- API requests timing out (3000ms → 30000ms)
- Page load failures (HTTP 503)
- Data not loading, infinite spinners
```

### Business Impact

**Revenue Impact**:
```
[FILL IN: Estimated revenue loss]
Example:
- Failed transactions: ~$15,000
- Abandoned carts: ~$8,000
- Total estimated loss: ~$23,000
```

**SLA Breach**:
```
[FILL IN: Any SLA violations]
Example:
99.9% uptime SLA breached (99.2% actual)
p95 latency SLA: 500ms (actual: 5000ms)
```

**Customer Support**:
```
[FILL IN: Support ticket volume, complaints]
Example:
- Support tickets: 47 (vs baseline 5)
- Social media mentions: 12 complaints
- Escalations: 3 enterprise customers
```

---

## Root Cause Analysis

### What Happened

**Trigger Event**:
[FILL IN: What initiated the incident?]

**Failure Mode**:
[FILL IN: How did the system fail?]

**Propagation**:
[FILL IN: How did the failure spread through the system?]

### Why It Happened

**Immediate Cause**:
[FILL IN: Direct technical cause of the incident]

**Contributing Factors**:
1. [FILL IN: Factor 1 - Why this made it worse]
2. [FILL IN: Factor 2 - Why this made it worse]
3. [FILL IN: Factor 3 - Why this made it worse]

**Root Cause** (5 Whys):
```
Why 1: [FILL IN: First why]
↓
Why 2: [FILL IN: Second why]
↓
Why 3: [FILL IN: Third why]
↓
Why 4: [FILL IN: Fourth why]
↓
Why 5: [FILL IN: Fifth why - ROOT CAUSE]
```

### Evidence

**Logs**:
```
[FILL IN: Relevant log entries showing the problem]
```

**Metrics/Graphs**:
```
[FILL IN: Link to Grafana dashboards, screenshots, or paste metrics]
```

**Code or Configuration**:
```
[FILL IN: Problematic code snippet or configuration]
```

---

## Diagnosis Process

### Investigation Steps

**Step 1**: [FILL IN: First thing checked]
```
[FILL IN: What was found]
```

**Step 2**: [FILL IN: Second thing checked]
```
[FILL IN: What was found]
```

**Step 3**: [FILL IN: Third thing checked]
```
[FILL IN: What was found]
```

**Key Discovery**:
[FILL IN: The "aha!" moment - what revealed the root cause]

### Tools Used

- [FILL IN: Tool 1 - What it revealed]
- [FILL IN: Tool 2 - What it revealed]
- [FILL IN: Tool 3 - What it revealed]

---

## Resolution

### Immediate Fix (Mitigation)

**What we did**:
[FILL IN: Quick fix to stop the bleeding]

**Code/Configuration Change**:
```
[FILL IN: Paste the emergency fix]
```

**Deployment**:
```
[FILL IN: How the fix was deployed]
Example:
wrangler deploy --env production
Deployed to 300+ edge locations in 45 seconds
```

**Verification**:
```
[FILL IN: How we verified the fix worked]
Example:
Error rate: 15% → 0.01% (back to baseline)
p95 latency: 5000ms → 500ms (back to normal)
```

### Permanent Fix

**What we changed**:
[FILL IN: Long-term solution to prevent recurrence]

**Code Changes**:
```
[FILL IN: Permanent code or configuration changes]
```

**Infrastructure Changes**:
```
[FILL IN: Any infrastructure modifications]
Example:
- Increased database connection pool: 20 → 50
- Added Redis caching layer
- Enabled auto-scaling: 4-16 workers
```

---

## Prevention Measures

### Immediate Actions (Completed)

- [x] [FILL IN: Action 1 - Status: Completed on YYYY-MM-DD]
- [x] [FILL IN: Action 2 - Status: Completed on YYYY-MM-DD]
- [x] [FILL IN: Action 3 - Status: Completed on YYYY-MM-DD]

### Short-Term Actions (1-2 weeks)

- [ ] [FILL IN: Action 1 - Owner: Name, Due: YYYY-MM-DD]
- [ ] [FILL IN: Action 2 - Owner: Name, Due: YYYY-MM-DD]
- [ ] [FILL IN: Action 3 - Owner: Name, Due: YYYY-MM-DD]

### Long-Term Actions (1-3 months)

- [ ] [FILL IN: Action 1 - Owner: Name, Due: YYYY-MM-DD]
- [ ] [FILL IN: Action 2 - Owner: Name, Due: YYYY-MM-DD]
- [ ] [FILL IN: Action 3 - Owner: Name, Due: YYYY-MM-DD]

### Monitoring Improvements

**New Alerts**:
```yaml
[FILL IN: New alert rules to detect this earlier]
Example:
- alert: HighDatabaseConnectionUsage
  expr: db_pool_utilization > 0.8
  for: 5m
  annotations:
    summary: "Database pool >80% utilized"
```

**Dashboard Updates**:
- [FILL IN: Dashboard 1 - What was added]
- [FILL IN: Dashboard 2 - What was added]

**Runbook Updates**:
- [FILL IN: Runbook 1 - What was updated]
- [FILL IN: Runbook 2 - What was created]

---

## Lessons Learned

### What Went Well ✅

1. [FILL IN: Good thing 1]
2. [FILL IN: Good thing 2]
3. [FILL IN: Good thing 3]

### What Went Wrong ❌

1. [FILL IN: Problem 1]
2. [FILL IN: Problem 2]
3. [FILL IN: Problem 3]

### What We'll Do Differently

1. [FILL IN: Change 1]
2. [FILL IN: Change 2]
3. [FILL IN: Change 3]

### Questions for Follow-Up

1. [FILL IN: Question 1 - Needs investigation]
2. [FILL IN: Question 2 - Needs discussion]
3. [FILL IN: Question 3 - Needs research]

---

## Related Incidents

**Similar Past Incidents**:
- [FILL IN: INC-XXXX - Brief description - Date]
- [FILL IN: INC-YYYY - Brief description - Date]

**Related Issues**:
- [FILL IN: GitHub/Linear issue link - Description]
- [FILL IN: GitHub/Linear issue link - Description]

---

## Appendix

### Full Error Logs

```
[FILL IN: Complete error logs for reference]
```

### Performance Graphs

```
[FILL IN: Links to Grafana dashboards or screenshots]
```

### Database Queries

```sql
[FILL IN: Slow queries or problematic SQL]
```

### Configuration Files

```
[FILL IN: Relevant configuration that contributed to the incident]
```

---

## Sign-Off

**Incident Commander**: [Name] - [Date]
**Technical Lead**: [Name] - [Date]
**Engineering Manager**: [Name] - [Date]

**Post-Incident Review Scheduled**: [YYYY-MM-DD at HH:MM]

---

## Template Notes

**How to use this template**:
1. Copy this template to your documentation system
2. Fill in all `[FILL IN]` sections
3. Remove sections that don't apply
4. Share with team for review within 24 hours of incident resolution
5. Schedule post-incident review meeting

**Severity Definitions**:
- **SEV1**: Complete outage, all users affected, revenue impact
- **SEV2**: Partial outage, some users affected, degraded experience
- **SEV3**: Minor issue, few users affected, workaround available

**Required Sections** (do not skip):
- Executive Summary
- Incident Timeline
- Root Cause Analysis
- Resolution
- Prevention Measures
- Lessons Learned

---

Return to [templates index](INDEX.md)
