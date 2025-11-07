# Root Cause Analysis Techniques

Comprehensive methods for identifying root causes through 5 Whys, Fishbone Diagrams, Timeline Reconstruction, and data-driven hypothesis testing.

## 5 Whys Technique

### Method

Ask "Why?" iteratively until you reach the root cause (typically 5 levels deep, but can be 3-7).

**Rules**:
1. Start with the problem statement
2. Ask "Why did this happen?"
3. Answer based on facts/data (not assumptions)
4. Repeat for each answer until root cause found
5. Root cause = **systemic issue** (not human error)

### Example

**Problem**: Database went down

```
Why 1: Why did the database go down?
→ Because the primary database ran out of disk space

Why 2: Why did it run out of disk space?
→ Because PostgreSQL logs filled the entire disk (450GB)

Why 3: Why did logs grow to 450GB?
→ Because log rotation was disabled

Why 4: Why was log rotation disabled?
→ Because the `log_truncate_on_rotation` config was set to `off` during a migration

Why 5: Why was this config change not caught?
→ Because configuration changes are not code-reviewed and there was no disk monitoring alert

ROOT CAUSE: Missing disk monitoring alerts + configuration change without code review
```

**Action Items**:
- Add disk usage monitoring (>90% alert)
- Require code review for all config changes
- Enable log rotation on all databases

---

## Fishbone Diagram (Ishikawa)

### Method

Categorize contributing factors into major categories to identify root cause systematically.

**Categories** (6M's):
1. **Method** (Process)
2. **Machine** (Technology)
3. **Material** (Inputs/Data)
4. **Measurement** (Monitoring)
5. **Mother Nature** (Environment)
6. **Manpower** (People/Skills)

### Example

**Problem**: API performance degraded (p95: 200ms → 2000ms)

```
                              API Performance Degraded
                                        │
        ┌───────────────────┬───────────┴───────────┬───────────────────┐
        │                   │                       │                   │
    METHOD              MACHINE                 MATERIAL          MEASUREMENT
  (Process)          (Technology)               (Data)            (Monitoring)
        │                   │                       │                   │
   No memory          EventEmitter              Large dataset       No heap
   profiling in       listeners leak            processing          snapshots
   code review        (not removed)             (100K orders)       in CI/CD
        │                   │                       │                   │
   No long-running    Node.js v14               High traffic        No gradual
   load tests         (old GC)                  spike (2x)          alerts
   (only 5min)                                                      (1h → 2h)
```

**Root Causes Identified**:
- **Machine**: EventEmitter leak (technical)
- **Measurement**: No heap monitoring (monitoring gap)
- **Method**: No memory profiling in code review (process gap)

---

## Timeline Reconstruction

### Method

Build chronological timeline of events to identify causation and correlation.

**Steps**:
1. Gather logs from all systems (with timestamps)
2. Normalize to UTC
3. Plot events chronologically
4. Identify cause-and-effect relationships
5. Find the triggering event

### Example

```
12:00:00 - Normal operation (p95: 200ms, memory: 400MB)
12:15:00 - Code deployment (v2.15.4)
12:30:00 - Memory: 720MB (+80% in 15min) ⚠️
12:45:00 - Memory: 1.2GB (+67% in 15min) ⚠️
13:00:00 - Memory: 1.8GB (+50% in 15min) 🚨
13:00:00 - p95 latency: 800ms (4x slower)
13:15:00 - Memory: 2.3GB (limit reached)
13:15:00 - Workers start OOMing
13:20:00 - p95 latency: 2000ms (10x slower)
13:30:00 - Alert fired: High latency
14:00:00 - Alert fired: High memory

CORRELATION:
- Deployment at 12:15 → Memory growth starts at 12:30
- Memory growth → Latency increase (correlated)
- TRIGGER: Code deployment v2.15.4

ACTION: Review code changes in v2.15.4
```

---

## Contributing Factors Analysis

### Levels of Causation

**Immediate Cause** (What happened):
- Direct technical failure
- Example: EventEmitter listeners not removed

**Underlying Conditions** (Why it was possible):
- Missing safeguards
- Example: No memory profiling in code review

**Latent Failures** (Systemic weaknesses):
- Organizational/process gaps
- Example: No developer training on memory management

### Example

**Incident**: Memory leak in production

```
Immediate Cause:
└─ Code: EventEmitter .on() used without .removeListener()

Underlying Conditions:
├─ No code review caught the issue
├─ No memory profiling in CI/CD
└─ Short load tests (5min) didn't reveal gradual leak

Latent Failures:
├─ Team lacks memory management training
├─ No documentation on EventEmitter best practices
└─ Culture of "ship fast, fix later"
```

---

## Hypothesis Testing

### Method

Generate hypotheses, test with data, validate or reject.

**Process**:
1. Observe symptoms
2. Generate hypotheses (educated guesses)
3. Design experiments to test each hypothesis
4. Collect data
5. Accept or reject hypothesis
6. Repeat until root cause found

### Example

**Symptom**: Checkout API slow (p95: 3000ms)

**Hypothesis 1**: Database slow queries
```
Test: Check slow query log
Data: All queries < 50ms ✅
Result: REJECTED - database is fast
```

**Hypothesis 2**: External API slow
```
Test: Distributed tracing (Jaeger)
Data: Fraud check API: 2750ms (91% of total time) 🚨
Result: ACCEPTED - external API is bottleneck
```

**Hypothesis 3**: Network latency
```
Test: curl timing breakdown
Data: DNS: 50ms, Connect: 30ms, Transfer: 2750ms
Result: PARTIAL - transfer is slow (not DNS/connect)
```

**Root Cause**: External fraud check API slow (blocking checkout)

---

## Blameless RCA Principles

### Core Tenets

1. **Focus on Systems, Not People**
   - ❌ "Engineer made a mistake"
   - ✅ "Process didn't catch config error"

2. **Assume Good Intent**
   - Everyone did the best they could with information available
   - Blame discourages honesty and learning

3. **Multiple Contributing Factors**
   - Never a single cause
   - Usually 3-5 factors contribute

4. **Actionable Improvements**
   - Fix the system, not the person
   - Concrete action items with owners

### Example (Blameless vs Blame)

**Blamefu (BAD)**:
```
Root Cause: Engineer Jane deployed code without testing
Action Item: Remind Jane to test before deploying
```

**Blameless (GOOD)**:
```
Root Cause: Deployment process allowed untested code to reach production
Contributing Factors:
1. No automated tests in CI/CD
2. Manual deployment process (prone to human error)
3. No staging environment validation

Action Items:
1. Add automated tests to CI/CD (Owner: Mike, Due: Dec 20)
2. Require staging deployment + validation before production (Owner: Sarah, Due: Dec 22)
3. Implement deployment checklist (Owner: Alex, Due: Dec 18)
```

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - RCA examples from real incidents
- **Severity Matrix**: [incident-severity-matrix.md](incident-severity-matrix.md) - When to perform RCA
- **Templates**: [Postmortem Template](../templates/postmortem-template.md) - Structured RCA format

---

Return to [reference index](INDEX.md)
