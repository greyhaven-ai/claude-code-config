# Incident Severity Matrix

Comprehensive guide for classifying incident severity levels (SEV1-SEV4) with clear criteria, examples, escalation paths, and communication frequencies.

## Severity Levels Overview

| Severity | Impact | Response Time | Update Frequency | Escalation | Example |
|----------|--------|---------------|------------------|------------|---------|
| **SEV1** | Critical - Total outage | Immediate | Every 15 min | CTO, CEO | Database down, 100% error rate |
| **SEV2** | Major - Partial degradation | < 30 min | Every 30 min | VP Eng | API slow, 30% users affected |
| **SEV3** | Minor - Isolated issues | < 2 hours | Hourly | Team Lead | Feature flag misconfigured |
| **SEV4** | Cosmetic - No functional impact | < 1 week | As needed | None | Button color wrong |

---

## SEV1: Critical

### Definition

**Total or near-total service outage with severe customer impact and revenue loss**

### Criteria (ANY of these qualifies as SEV1)

- ✅ **Complete outage**: 100% of users unable to use core functionality
- ✅ **Revenue stopped**: E-commerce checkout down, payment processing offline
- ✅ **Data loss**: Customer data deleted, database corruption
- ✅ **Security breach**: Active security incident, data exposure
- ✅ **SLO violation >50%**: Error rate >50%, p95 latency >10x baseline
- ✅ **Regulatory exposure**: GDPR violation, compliance breach

### Examples

**SEV1 Examples**:
```
✅ Database primary failure (100% error rate)
✅ Payment gateway down (revenue stopped)
✅ Security breach (customer data exposed)
✅ DDoS attack (all users unable to access site)
✅ Data center outage (entire region down)
✅ Critical bug causing data corruption
✅ API returning 500 errors for 100% of requests
```

**NOT SEV1** (would be SEV2):
```
❌ Slow performance (users can still use, just slow)
❌ Partial outage (80% of users working fine)
❌ Feature disabled (core functionality still works)
❌ Dashboard down (main product still accessible)
```

### Response Protocol

**Immediate Actions** (within 5 minutes):
1. Page oncall engineer via PagerDuty
2. Incident Commander joins immediately
3. Create war room (Slack #incident-XXX, Zoom bridge)
4. Declare SEV1 in Slack
5. Update status page: "Investigating major outage"

**Communication Frequency**:
- Internal: Every 15 minutes (or on status change)
- External: Status page update within 5 minutes, then every 15 minutes
- Executive: Immediate notification (CTO, CEO)

**Escalation Path**:
```
0-5 min:   Oncall Engineer
5-10 min:  IC + Technical Lead
10-15 min: Engineering Manager
15-30 min: VP Engineering
30+ min:   CTO, CEO (if unresolved)
```

**Example Communication**:
```
🚨 SEV1 INCIDENT DECLARED 🚨
Impact: 100% outage, database down
Incident ID: INC-2024-1205-001
IC: @jane
War room: #incident-001
Next update: 15 minutes
```

---

## SEV2: Major

### Definition

**Significant degradation affecting substantial number of users, but core functionality remains available**

### Criteria (2 or more of these)

- ⚠️ **Partial degradation**: 20-50% of users affected
- ⚠️ **Performance issues**: p95 latency >5x baseline
- ⚠️ **Elevated errors**: Error rate 1-10% (vs <0.1% baseline)
- ⚠️ **Feature outage**: Non-critical feature completely down
- ⚠️ **SLO violation >10%**: Breaking SLA but not catastrophic

### Examples

**SEV2 Examples**:
```
⚠️ API p95 latency 200ms → 2000ms (10x slower)
⚠️ Memory leak causing gradual degradation
⚠️ 30% of workers failing health checks
⚠️ Search feature down (rest of site works)
⚠️ External API timeout affecting 20% of requests
⚠️ Cache cluster failure (database handling increased load)
⚠️ Mobile app crashing for 40% of users
```

**NOT SEV2** (would be SEV3):
```
❌ Minor feature flag misconfiguration (< 20% users)
❌ Slight performance degradation (< 2x slower)
❌ Dashboard metrics missing (functionality unaffected)
❌ Error rate 0.5% (close to baseline 0.1%)
```

### Response Protocol

**Initial Actions** (within 30 minutes):
1. Oncall engineer investigates
2. IC joins if issue persists > 15 minutes
3. Create incident channel (Slack #incident-XXX)
4. Declare SEV2
5. Status page update: "Investigating performance issues"

**Communication Frequency**:
- Internal: Every 30 minutes
- External: Status page update within 15 minutes, then hourly
- Executive: Notify VP Engineering (not CEO unless prolonged)

**Escalation Path**:
```
0-30 min:  Oncall Engineer
30-60 min: IC + Team Lead
60+ min:   Engineering Manager → VP Engineering
```

**Example Communication**:
```
⚠️ SEV2 INCIDENT
Impact: API performance degraded, 30% of users slow
Incident ID: INC-2024-1210-002
IC: @mike
Status: Investigating memory leak
Next update: 30 minutes
```

---

## SEV3: Minor

### Definition

**Isolated issues with low customer impact, workarounds available**

### Criteria

- ⚡ **Limited scope**: < 20% of users affected
- ⚡ **Low impact**: Confusion or inconvenience, not functional failure
- ⚡ **Workaround available**: Users can complete tasks via alternate path
- ⚡ **Non-critical feature**: Feature affected is not core product
- ⚡ **SLO within budget**: No SLA violations

### Examples

**SEV3 Examples**:
```
⚡ Feature flag enabled for 20% of users (should be 0%)
⚡ UI button misaligned (cosmetic but noticed)
⚡ Email notifications delayed by 1 hour
⚡ Export feature broken (data accessible via UI)
⚡ Dashboard chart not loading (data available elsewhere)
⚡ Error message unclear (doesn't prevent completion)
⚡ Mobile app force-close on rare edge case
```

**NOT SEV3** (would be SEV4):
```
❌ Button color slightly off (no user confusion)
❌ Tooltip text outdated (doesn't mislead)
❌ Console warning in browser DevTools (no user impact)
```

### Response Protocol

**Initial Actions** (within 2 hours):
1. Oncall engineer investigates during business hours
2. No IC needed (unless escalates)
3. Document in Slack (no dedicated channel unless needed)
4. Status page update: Optional (if user-facing)

**Communication Frequency**:
- Internal: Hourly or as needed
- External: Status page optional (if many users report)
- Executive: Team lead informed, no VP/CTO escalation

**Escalation Path**:
```
0-2 hours:  Oncall Engineer
2+ hours:   Team Lead (if unresolved)
No automatic escalation beyond team level
```

**Example Communication**:
```
ℹ️ SEV3 INCIDENT
Impact: Feature flag misconfigured, 20% users see experimental feature
Status: Disabled flag, sending customer communication
Resolution: 30 minutes
```

---

## SEV4: Cosmetic

### Definition

**Minor UI/UX issues with no functional impact**

### Criteria

- 🎨 **Visual only**: No functional impact
- 🎨 **No user confusion**: Users understand how to proceed
- 🎨 **Deferred fix**: Can be addressed in regular sprint
- 🎨 **No business impact**: No revenue or reputation impact

### Examples

**SEV4 Examples**:
```
🎨 Button color slightly wrong (users can still click)
🎨 Spacing issue in UI (minor visual defect)
🎨 Tooltip spelling error (doesn't affect functionality)
🎨 Icon misaligned by 2px (barely noticeable)
🎨 Footer text outdated (non-critical information)
🎨 DevTools console warning (developers only)
```

### Response Protocol

**Actions**:
1. Create ticket in backlog (Linear, Jira)
2. Prioritize in next sprint planning
3. No incident response needed
4. No status page update

**Communication**:
- Document in ticket
- Fix in regular development cycle
- No incident declared

---

## Decision Tree

### Use this flowchart to classify incidents:

```
START: Issue detected
  │
  ├─ Is the entire service down?
  │    ├─ YES → SEV1 (Critical)
  │    └─ NO ↓
  │
  ├─ Are >50% of users affected?
  │    ├─ YES → SEV1 (Critical)
  │    └─ NO ↓
  │
  ├─ Is revenue stopped?
  │    ├─ YES → SEV1 (Critical)
  │    └─ NO ↓
  │
  ├─ Is there a security breach or data loss?
  │    ├─ YES → SEV1 (Critical)
  │    └─ NO ↓
  │
  ├─ Are 20-50% of users affected OR is performance >5x degraded?
  │    ├─ YES → SEV2 (Major)
  │    └─ NO ↓
  │
  ├─ Is a non-critical feature broken?
  │    ├─ YES → SEV2 (Major)
  │    └─ NO ↓
  │
  ├─ Are <20% of users affected AND workaround available?
  │    ├─ YES → SEV3 (Minor)
  │    └─ NO ↓
  │
  ├─ Is this a visual/UX issue only?
  │    ├─ YES → SEV4 (Cosmetic)
  │    └─ NO → Reassess, likely SEV3
```

---

## Severity Upgrade/Downgrade

### When to Upgrade Severity

**SEV3 → SEV2**:
- Issue affects more users than initially thought (10% → 30%)
- Workaround stops working
- Impact duration extends beyond 4 hours

**SEV2 → SEV1**:
- Degradation becomes complete outage
- Affects all users instead of partial
- Data corruption discovered
- Security implications identified

**Example Upgrade**:
```
10:00 - SEV3 declared (feature flag issue, 10% users)
10:30 - Scope increased to 40% of users → Upgrade to SEV2
11:00 - All users affected, feature completely broken → Upgrade to SEV1
```

### When to Downgrade Severity

**SEV1 → SEV2**:
- Partial mitigation in place (50% of users recovered)
- Workaround available for remaining users
- Revenue partially restored

**SEV2 → SEV3**:
- Issue affects fewer users than initially thought (30% → 15%)
- Performance degradation minor (3x → 1.5x)
- Workaround discovered

**Example Downgrade**:
```
14:00 - SEV1 declared (database down, 100% outage)
14:30 - Replica promoted, 80% of users recovered → Downgrade to SEV2
15:00 - All users recovered, monitoring for recurrence → Downgrade to SEV3
```

---

## Severity-Specific Metrics

### SEV1 Metrics

```
MTTR Target: < 1 hour (mean time to recovery)
MTTD Target: < 5 minutes (mean time to detect)
Acceptable Frequency: < 1 per quarter
SLO Impact: Counts against error budget (99.9% uptime = 43.2 min/month)
```

### SEV2 Metrics

```
MTTR Target: < 4 hours
MTTD Target: < 15 minutes
Acceptable Frequency: < 1 per month
SLO Impact: Partial error budget consumption
```

### SEV3 Metrics

```
MTTR Target: < 1 day
MTTD Target: < 1 hour
Acceptable Frequency: < 4 per month
SLO Impact: Minimal or no error budget impact
```

### SEV4 Metrics

```
Resolution Target: Next sprint
Detection: User reports or internal QA
Frequency: Unlimited (tracked as tech debt)
SLO Impact: None
```

---

## Examples from Real Incidents

### SEV1 Examples (from incident-responder examples)

1. **Database Outage** ([sev1-critical-database-outage.md](../examples/sev1-critical-database-outage.md))
   - Impact: 100% outage, all users affected
   - MTTR: 45 minutes
   - Revenue loss: $37,500

### SEV2 Examples

2. **API Performance Degradation** ([sev2-api-performance-degradation.md](../examples/sev2-api-performance-degradation.md))
   - Impact: 30% users affected, 10x slower
   - MTTR: 3 hours
   - Revenue impact: $15,000

### SEV3 Examples

3. **Feature Flag Misconfiguration** ([sev3-feature-flag-misconfiguration.md](../examples/sev3-feature-flag-misconfiguration.md))
   - Impact: 20% users saw experimental feature
   - MTTR: 30 minutes
   - Revenue impact: $0

---

## Related Documentation

- **Communication Templates**: [communication-templates.md](communication-templates.md) - Templates for each severity level
- **Examples**: [Examples Index](../examples/INDEX.md) - Real-world incidents
- **RCA Techniques**: [rca-techniques.md](rca-techniques.md) - Root cause analysis methods

---

Return to [reference index](INDEX.md)
