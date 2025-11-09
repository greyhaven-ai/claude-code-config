# Runbook: [PROBLEM TITLE]

**Alert**: [Alert name that triggers this runbook]
**Severity**: [SEV1 / SEV2 / SEV3]
**Owner**: [Team name]
**Last Updated**: [YYYY-MM-DD]
**Last Tested**: [YYYY-MM-DD]

---

## Problem Description

[2-3 sentence description of what this problem is]

**Symptoms**:
- [Observable symptom 1 - what users/operators see]
- [Observable symptom 2]
- [Observable symptom 3]

**Impact**:
- **Customer Impact**: [What users experience]
- **Business Impact**: [Revenue, SLA, compliance]
- **Affected Services**: [List of services]

---

## Prerequisites

**Required Access**:
- [ ] Kubernetes cluster access (`kubectl` configured)
- [ ] Database access (PlanetScale/PostgreSQL)
- [ ] Cloudflare Workers access (`wrangler` configured)
- [ ] Monitoring access (Grafana, Datadog)

**Required Tools**:
- [ ] `kubectl` v1.28+
- [ ] `wrangler` v3+
- [ ] `pscale` CLI
- [ ] `curl`, `jq`

---

## Diagnosis

### Step 1: [Check Initial Symptom]

**What to check**: [Describe what this step verifies]

```bash
# Command to run
[command]

# Expected output (healthy):
[what you should see if everything is fine]

# Problem indicator:
[what you see if there's an issue]
```

**Interpretation**:
- If [condition], then [conclusion]
- If [condition], then go to Step 2

---

### Step 2: [Verify Root Cause]

```bash
# Command to run
[command]

# Look for:
[what to look for in the output]
```

**Possible Causes**:
1. **[Cause 1]**: [How to identify] → Go to [Mitigation Option A](#option-a-cause-1)
2. **[Cause 2]**: [How to identify] → Go to [Mitigation Option B](#option-b-cause-2)
3. **[Cause 3]**: [How to identify] → Escalate to [team]

---

### Step 3: [Additional Verification]

[Only if needed for complex scenarios]

```bash
# Commands
[commands]
```

---

## Mitigation

### Option A: [Cause 1]

**When to use**: [Conditions when this mitigation applies]

**Steps**:
1. [Action 1]
   ```bash
   [command]
   ```

2. [Action 2]
   ```bash
   [command]
   ```

3. [Action 3]
   ```bash
   [command]
   ```

**Verification**:
```bash
# Check that mitigation worked
[verification command]

# Expected result:
[what you should see]
```

**If mitigation fails**: [What to do next - usually escalate]

---

### Option B: [Cause 2]

[Same format as Option A]

---

## Rollback

**If mitigation makes things worse:**

```bash
# Rollback command 1
[command to undo action 1]

# Rollback command 2
[command to undo action 2]
```

---

## Verification & Monitoring

### Health Checks

After mitigation, verify these metrics return to normal:

```bash
# Check 1: Service health
curl https://api.greyhaven.io/health
# Expected: HTTP 200, {"status": "healthy"}

# Check 2: Error rate
# Grafana: Error Rate dashboard
# Expected: <0.1%

# Check 3: Latency
# Grafana: API Latency dashboard
# Expected: p95 <500ms
```

### Monitoring Period

Monitor for **[time period]** after mitigation:
- [ ] Error rate stable (<0.1%)
- [ ] Latency normal (p95 <500ms)
- [ ] No new alerts
- [ ] User reports resolved

---

## Escalation

**Escalate if**:
- Mitigation doesn't work after [X] minutes
- Root cause unclear after diagnosis
- Issue is [severity] and unresolved after [X] minutes
- Multiple services affected

**Escalation Path**:
```
0-15 min:  @oncall-engineer
15-30 min: @team-lead
30-60 min: @engineering-manager
60+ min:   @vp-engineering (SEV1 only)
```

**Escalation Contact**:
- Team Slack: #[team-channel]
- PagerDuty: [escalation policy]
- Oncall: @[oncall-alias]

---

## Common Mistakes

### Mistake 1: [Common Error]

**Wrong**:
```bash
[incorrect command or approach]
```

**Correct**:
```bash
[correct command or approach]
```

### Mistake 2: [Common Error]

[Description and correction]

---

## Related Documentation

- **Alert Definition**: [Link to alert config]
- **Monitoring Dashboard**: [Link to Grafana]
- **Architecture Doc**: [Link to system architecture]
- **Past Incidents**: [Links to similar incidents]
- **Postmortems**: [Links to related postmortems]

---

## Changelog

| Date | Author | Changes |
|------|--------|---------|
| [YYYY-MM-DD] | @[name] | Initial creation |
| [YYYY-MM-DD] | @[name] | Updated [what changed] |

---

## Testing Notes

**Last Test Date**: [YYYY-MM-DD]
**Test Result**: [Pass / Fail]
**Notes**: [What was learned from testing]

**How to Test**:
1. [Step to simulate failure in staging]
2. [Follow runbook]
3. [Verify recovery]
4. [Document time taken and any issues]

---

Return to [templates index](INDEX.md)
