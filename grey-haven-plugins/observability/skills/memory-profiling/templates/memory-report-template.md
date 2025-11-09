# Memory Leak Investigation Report

**Service**: [Service Name]
**Date**: [YYYY-MM-DD]
**Investigator**: [Your Name]
**Severity**: [Critical/High/Medium/Low]

---

## Executive Summary

**TL;DR**: [One sentence summary of the leak, cause, and fix]

**Impact**:
- Memory growth: [X MB/hour or X% increase]
- OOM incidents: [Number of crashes]
- Affected users: [Number or percentage]
- Duration: [How long the leak existed]

**Resolution**:
- Root cause: [Leak pattern - e.g., "EventEmitter listeners not removed"]
- Fix deployed: [Date/time]
- Status: [Resolved/Monitoring/In Progress]

---

## Incident Timeline

| Time | Event | Details |
|------|-------|---------|
| [HH:MM] | Detection | [How was leak detected? Alert, manual observation, etc.] |
| [HH:MM] | Investigation started | [Initial actions taken] |
| [HH:MM] | Root cause identified | [What was found] |
| [HH:MM] | Fix implemented | [Code changes made] |
| [HH:MM] | Fix deployed | [Deployment details] |
| [HH:MM] | Validation complete | [Confirmation that leak is fixed] |

---

## Symptoms and Detection

### Initial Symptoms

- [ ] Linear memory growth (X MB/hour)
- [ ] OOM crashes (frequency: ___)
- [ ] GC pressure (frequent/long pauses)
- [ ] Connection pool exhaustion
- [ ] Service degradation (slow responses)
- [ ] Other: ___

### Detection Method

**How Discovered**: [Alert, monitoring dashboard, user report, etc.]

**Monitoring Data**:
```
Prometheus query: [Query used to detect the leak]
Alert rule: [Alert name/threshold]
Dashboard: [Link to Grafana dashboard]
```

**Example Metrics**:
```
Before:
- Heap usage baseline: X MB
- After 6 hours: Y MB
- Growth rate: Z MB/hour

Current:
- Heap usage: [Current value]
- Active connections: [Number]
- GC pause duration: [p95 value]
```

---

## Investigation Steps

### 1. Initial Data Collection

**Tools Used**:
- [ ] Chrome DevTools heap snapshots
- [ ] Node.js `--trace-gc` logs
- [ ] Python Scalene profiling
- [ ] Prometheus metrics
- [ ] Application logs
- [ ] Other: ___

**Heap Snapshots Collected**:
```
Snapshot 1: [timestamp] - [size] MB - [location/filename]
Snapshot 2: [timestamp] - [size] MB - [location/filename]
Snapshot 3: [timestamp] - [size] MB - [location/filename]
```

### 2. Snapshot Comparison Analysis

**Method**: [Comparison view in Chrome DevTools, diff analysis, etc.]

**Findings**:
```
Objects growing between snapshots:
- [Object type 1]: +X instances (+Y MB)
- [Object type 2]: +X instances (+Y MB)
- [Object type 3]: +X instances (+Y MB)

Top 3 memory consumers:
1. [Object type] - X MB - [Retainer path]
2. [Object type] - X MB - [Retainer path]
3. [Object type] - X MB - [Retainer path]
```

### 3. Retainer Path Analysis

**Leaked Object**: [Type of object that's leaking]

**Retainer Path**:
```
Window / Global
  → [Variable name]
    → [Object/function]
      → [Property]
        → [Leaked object]
```

**Why Not GC'd**: [Explanation of what's keeping object alive]

---

## Root Cause Analysis

### Leak Pattern Identified

**Pattern**: [e.g., EventEmitter leak, closure trap, unclosed connection, etc.]

**Vulnerable Code** (before fix):
```typescript
// File: [filepath]:[line]
// [Brief explanation of why this leaks]

[Paste vulnerable code here]
```

**Why This Leaks**:
1. [Step 1 of how the leak occurs]
2. [Step 2]
3. [Result: memory accumulates]

### Reproduction Steps

1. [Step to reproduce leak in dev/staging]
2. [Step 2]
3. [Observed result: memory growth]

**Reproduction Time**: [How long to observe leak? Minutes/hours]

---

## Fix Implementation

### Code Changes

**Pull Request**: [Link to PR]

**Files Modified**:
- [file1.ts] - [Brief description of change]
- [file2.ts] - [Brief description of change]

**Fixed Code**:
```typescript
// File: [filepath]:[line]
// [Brief explanation of fix]

[Paste fixed code here]
```

**Fix Strategy**:
- [ ] Remove event listeners (use `removeListener()` or `once()`)
- [ ] Close connections (use context managers or `try/finally`)
- [ ] Clear timers (use `clearInterval()`/`clearTimeout()`)
- [ ] Use WeakMap/WeakSet (for cache)
- [ ] Implement generator/streaming (for large datasets)
- [ ] Other: ___

### Testing and Validation

**Tests Added**:
```typescript
// Test that verifies no leak
describe('Memory leak fix', () => {
  it('should not leak listeners', () => {
    const before = emitter.listenerCount('event');
    // ... execute code
    const after = emitter.listenerCount('event');
    expect(after).toBe(before); // No leak
  });
});
```

**Load Test Results**:
```
Before fix:
- Memory after 1000 requests: X MB
- Memory after 10000 requests: Y MB (growth)

After fix:
- Memory after 1000 requests: X MB
- Memory after 10000 requests: X MB (stable)
```

---

## Deployment and Results

### Deployment Details

**Environment**: [staging/production]
**Deployment Time**: [YYYY-MM-DD HH:MM UTC]
**Rollout Strategy**: [Canary, blue-green, rolling, etc.]

### Post-Deployment Metrics

**Before Fix**:
```
Memory baseline: X MB
Memory after 6h: Y MB
Growth rate: Z MB/hour
OOM incidents: N/week
```

**After Fix**:
```
Memory baseline: X MB
Memory after 6h: X MB (stable!)
Growth rate: 0 MB/hour
OOM incidents: 0/month
```

**Improvement**:
- Memory reduction: [X% or Y MB]
- OOM elimination: [100%]
- GC pressure: [Reduced by X%]

### Grafana Dashboard

**Link**: [Dashboard URL]

**Key Panels**:
- Heap usage trend: [Shows memory stable after fix]
- GC pause duration: [Shows improved GC behavior]
- Error rate: [Shows OOM errors eliminated]

---

## Lessons Learned

### What Went Well

- [Positive aspect 1]
- [Positive aspect 2]

### What Could Be Improved

- [Improvement area 1]
- [Improvement area 2]

### Preventive Measures

**Monitoring Added**:
- [ ] Alert: Memory growth >X MB/hour for >Y hours
- [ ] Alert: Heap usage >Z% of limit
- [ ] Dashboard: Memory trend visualization
- [ ] Alert: Connection pool saturation >X%

**Code Review Checklist Updated**:
- [ ] Event listeners properly cleaned up
- [ ] Database connections closed
- [ ] Timers/intervals cleared
- [ ] Large datasets processed with streaming/chunking

**Testing Standards**:
- [ ] Memory leak tests for event listeners
- [ ] Load tests with memory monitoring
- [ ] CI/CD checks for connection cleanup

---

## Related Documentation

- **Pattern Catalog**: [Link to memory-optimization-patterns.md]
- **Similar Incidents**: [Links to previous memory leak reports]
- **Runbook**: [Link to memory leak runbook]

---

## Appendix

### Heap Snapshot Files

- [snapshot1.heapsnapshot] - [Location/S3 URL]
- [snapshot2.heapsnapshot] - [Location/S3 URL]

### GC Logs

```
[Relevant GC log excerpts showing the leak]
```

### Prometheus Queries

```promql
# Memory growth rate
rate(nodejs_heap_used_bytes[1h])

# GC pause duration
histogram_quantile(0.95, rate(nodejs_gc_duration_seconds_bucket[5m]))
```

---

**Report Completed**: [YYYY-MM-DD]
**Next Review**: [Date for follow-up validation]
