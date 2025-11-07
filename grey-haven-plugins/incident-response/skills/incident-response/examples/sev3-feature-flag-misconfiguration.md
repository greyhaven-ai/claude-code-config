# SEV3: Feature Flag Misconfiguration

Experimental feature accidentally enabled for 20% of production users, causing confusion and support tickets. Demonstrates SEV3 incident response, feature flag validation, and prevention measures.

## Incident Summary

**Incident ID**: INC-2024-1215-003
**Severity**: SEV3 (Minor Issue)
**Date**: December 15, 2024
**MTTR**: 30 minutes (10:00 → 10:30 UTC)
**Impact**: 20% of users saw experimental feature, user confusion
**Revenue Impact**: $0 (no revenue loss, no functional impact)
**Root Cause**: Feature flag percentage set to 20% instead of 0% in production
**Status**: Resolved, feature flag process improved

---

## Incident Timeline

| Time (UTC) | Event | Action | Owner |
|------------|-------|--------|-------|
| 10:00 | Support tickets spike: "What is this new dashboard?" | Support team notices pattern | @support |
| 10:05 | Engineering paged for feature flag issue | IC joins, declares SEV3 | @alex |
| 10:08 | Verified experimental feature visible to users | Checked production feature flags | @mike |
| 10:10 | Feature flag set to 20% (should be 0%) | Found misconfiguration in LaunchDarkly | @mike |
| 10:12 | Disabled feature flag immediately | Set to 0%, users no longer see feature | @mike |
| 10:15 | Verified feature hidden for all users | Checked production UI | @sarah |
| 10:20 | Customer communication drafted | Support response template created | @alex |
| 10:30 | Incident resolved | Monitoring for more tickets, postmortem scheduled | @alex |

**Total Duration**: 30 minutes from detection to resolution

---

## Severity Classification

### Why SEV3?

**SEV3 Criteria Met**:
- ✅ Isolated issue (only affected 20% of users)
- ✅ Low customer impact (confusion, no broken functionality)
- ✅ Workaround available (users could ignore new feature)
- ✅ No revenue impact (feature was informational only)
- ✅ SLO within budget (no latency or error rate impact)

**Why Not SEV2 or SEV1**:
- ❌ NOT major degradation (feature worked fine, just shown too early)
- ❌ NOT revenue-impacting (users could still use the product)
- ❌ NOT security issue (no data exposed)
- ❌ NOT functional bug (feature worked as designed)

**Business Impact**:
```
Revenue Impact: $0 (no loss)
Customers Affected: ~20% (~10,000 users saw unexpected feature)
Failed Requests: 0 (no errors)
User Confusion: 200 support tickets over 30 minutes
Brand Impact: Minor (some users concerned about "beta" feature)
SLA Breach: No
```

---

## Detection

### Support Ticket Pattern (10:00)

**Support Tickets** (sampled):
```
Ticket #1301 (09:55): "I see a new 'AI Recommendations' dashboard. Is this a beta feature?"
Ticket #1302 (09:57): "What is the AI dashboard for? I didn't enable anything."
Ticket #1303 (09:58): "Is my account part of a test? I see features my colleagues don't see."
Ticket #1304 (10:00): "The new AI dashboard looks buggy, should I use it?"
...
Total tickets: 200 in 30 minutes (vs baseline 5/hour)
```

**Support Team Alert**:
```
Hey @engineering, we're getting a lot of tickets about a new "AI Recommendations" dashboard.
This wasn't supposed to go live yet, right? Looks like 20% of users are seeing it.
```

---

## Investigation

### Step 1: Verify Feature Visibility (10:08)

```bash
# Check production feature flags
curl https://api.launchdarkly.com/flags/ai-recommendations \
  -H "Authorization: Bearer $LD_API_KEY"

{
  "key": "ai-recommendations",
  "name": "AI Recommendations Dashboard",
  "kind": "boolean",
  "environments": {
    "production": {
      "on": true,
      "fallthrough": {
        "rollout": {
          "variations": [
            {"variation": 0, "weight": 80000},  // 80% false
            {"variation": 1, "weight": 20000}   // 20% true ❌
          ]
        }
      }
    },
    "staging": {
      "on": true,
      "fallthrough": {
        "rollout": {
          "variations": [
            {"variation": 0, "weight": 0},      // 0% false
            {"variation": 1, "weight": 100000}  // 100% true ✅
          ]
        }
      }
    }
  }
}

# Production: 20% enabled ❌ (should be 0%)
# Staging: 100% enabled ✅ (correct for testing)
```

**Root Cause Found**: Production rollout set to 20% instead of 0%

### Step 2: Check Change History (10:12)

**LaunchDarkly Audit Log**:
```
2024-12-15 09:45 UTC - @jane updated flag "ai-recommendations" in production
Changed: rollout.variations[1].weight from 0 to 20000

Comment: "Testing gradual rollout"
```

**What Happened**:
- Engineer (@jane) intended to test gradual rollout in **staging**
- Accidentally modified **production** environment
- LaunchDarkly UI shows staging/production tabs side-by-side
- Easy to click wrong tab

---

## Root Cause Analysis (5 Whys)

**Why 1**: Why did users see the experimental feature?
→ Because feature flag was set to 20% rollout in production

**Why 2**: Why was the flag set to 20% in production?
→ Because engineer intended to set staging to 20% but clicked production tab instead

**Why 3**: Why did the engineer click the wrong tab?
→ Because LaunchDarkly UI has staging/production tabs side-by-side with minimal visual distinction

**Why 4**: Why wasn't this caught before users saw it?
→ Because:
- No code review for feature flag changes (done via UI)
- No approval required for production flag changes
- No notification when production flags change
- No automated testing of flag states

**Why 5**: Why don't we have safeguards for production flag changes?
→ Because feature flag governance process was never established

**ROOT CAUSE**: Missing feature flag governance + easy to accidentally modify production in UI

---

## Mitigation & Resolution

### Immediate Fix (10:12 - 10:15)

```bash
# Disable feature flag in production (via LaunchDarkly UI)
# Set rollout to 0% for production

# Verify flag state
curl https://api.launchdarkly.com/flags/ai-recommendations/production

{
  "on": true,
  "fallthrough": {
    "rollout": {
      "variations": [
        {"variation": 0, "weight": 100000},  // 100% false ✅
        {"variation": 1, "weight": 0}        // 0% true ✅
      ]
    }
  }
}

# Production: 0% enabled ✅ (corrected)
```

**Verification**:
```bash
# Test as user in production
curl https://app.greyhaven.io/api/feature-flags \
  -H "Authorization: Bearer $USER_TOKEN"

{
  "ai-recommendations": false  ✅
}

# Feature no longer visible in UI ✅
```

### Customer Communication (10:20)

**Support Response Template**:
```
Subject: About the "AI Recommendations" Dashboard

Hi [Customer Name],

You may have briefly seen a new "AI Recommendations" dashboard in your account.
This was an experimental feature that was accidentally enabled for a small group of users.

We've disabled it and you should no longer see it in your account.
This feature is still in development and will be officially announced when it's ready.

We apologize for any confusion this may have caused.

Best,
Grey Haven Support Team
```

**Sent to**: 200 users who opened support tickets

---

## Prevention Measures

### Immediate Actions (Completed Same Day)

- [x] Disabled AI recommendations flag (10:12)
- [x] Documented incident in Slack (10:20)
- [x] Created support response template (10:20)
- [x] Reviewed all production feature flags for similar issues (10:45)

### Short-Term Actions (Completed Within 1 Week)

- [x] Feature flag change approval process (require peer approval for prod) - Day 1
- [x] LaunchDarkly production environment protected (require confirmation modal) - Day 2
- [x] Slack notifications for all production flag changes - Day 2
- [x] Feature flag documentation (owner, purpose, rollout plan) - Day 3
- [x] Staging validation checklist before production rollout - Day 5

### Long-Term Actions (Completed Within 1 Month)

- [x] Feature flag as code (Terraform/configuration files, code-reviewed) - Week 2
- [x] Automated testing of flag states in CI/CD - Week 3
- [x] Feature flag lifecycle policy (flags deleted after 90 days) - Week 3
- [x] Gradual rollout automation (5% → 10% → 25% → 50% → 100%) - Week 4

---

## Blameless Postmortem

### What Went Well ✅

1. **Fast Detection**: Support team noticed pattern within 5 minutes
2. **Clear Communication**: Support pinged engineering immediately
3. **Quick Resolution**: Fixed within 10 minutes of engineering notification
4. **Customer Care**: Sent personalized responses to all affected users
5. **No Revenue Impact**: Feature was informational only, no broken functionality

### What Went Wrong ❌

1. **No Safeguards**: No approval required for production flag changes
2. **UI Confusion**: Easy to accidentally click production instead of staging
3. **No Validation**: No staging validation checklist before production
4. **No Notifications**: Team not notified when production flags change
5. **No Review**: Feature flag changes not code-reviewed

### Key Learnings

1. **Feature Flags Are Code**: Treat them with same rigor as code changes
2. **Production Protection**: Require approval for production changes
3. **Clear UI Distinction**: Visual cues needed for production vs staging
4. **Validation Checklists**: Test in staging before production rollout
5. **Notifications**: Team should know when production changes

### Action Items (Tracked in Linear)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Feature flag approval process | @alex | Dec 15 | ✅ Done |
| LaunchDarkly production protection | @mike | Dec 16 | ✅ Done |
| Slack notifications for flag changes | @sarah | Dec 16 | ✅ Done |
| Flag documentation template | @alex | Dec 17 | ✅ Done |
| Staging validation checklist | @team | Dec 20 | ✅ Done |
| Feature flags as code (Terraform) | @mike | Dec 28 | ✅ Done |
| Automated flag testing | @sarah | Jan 5 | ✅ Done |
| Flag lifecycle policy (90 days) | @alex | Jan 10 | ✅ Done |

---

## Feature Flag Governance (New Process)

### Before This Incident

```
❌ Anyone can change production flags
❌ No approval required
❌ No notifications
❌ No validation checklist
❌ Manual rollouts (error-prone)
```

### After This Incident

```
✅ Production flags require approval (peer review)
✅ Slack notification on any prod flag change
✅ Staging validation checklist before production
✅ Gradual rollout automation (5% → 100%)
✅ Flags as code (Terraform, version controlled)
✅ Automated testing of flag states
✅ Flags auto-expire after 90 days (cleanup)
```

### Example: New Flag Rollout

1. **Create flag in staging** (via Terraform)
2. **Test with 100% in staging** (validation checklist)
3. **Submit PR** for production rollout (code review)
4. **Merge PR** (Terraform applies changes)
5. **Gradual rollout** (automated: 5% → 10% → 25% → 50% → 100%)
6. **Monitor metrics** at each step (automated rollback if issues)
7. **Remove flag** after 90 days (lifecycle policy)

---

## Related Documentation

- **Feature Flag Best Practices**: [LaunchDarkly Documentation](https://docs.launchdarkly.com/)
- **Terraform LaunchDarkly Provider**: [terraform-provider-launchdarkly](https://registry.terraform.io/providers/launchdarkly/launchdarkly/latest/docs)
- **Gradual Rollout Strategy**: [Progressive Delivery](https://martinfowler.com/bliki/ProgressiveDelivery.html)
- **Similar Incidents**: None (first feature flag incident)

---

Return to [examples index](INDEX.md)
