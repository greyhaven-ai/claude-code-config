# SEV2: API Performance Degradation

Gradual API performance degradation due to memory leak in Node.js worker, resolved through heap snapshot analysis and code fix. Demonstrates SEV2 incident response, temporary mitigation vs permanent fix, and gradual alert patterns.

## Incident Summary

**Incident ID**: INC-2024-1210-002
**Severity**: SEV2 (Major Degradation)
**Date**: December 10, 2024
**MTTR**: 3 hours (14:00 → 17:00 UTC)
**Impact**: 30% of users affected, slow page loads
**Revenue Impact**: ~$15,000 (reduced conversion rate)
**Root Cause**: Memory leak in EventEmitter listeners (worker process)
**Status**: Resolved, memory profiling added to CI/CD

---

## Incident Timeline

| Time (UTC) | Event | Action | Owner |
|------------|-------|--------|-------|
| 14:00 | Gradual p95 latency alert (500ms → 2000ms) | Monitoring detected degradation | Auto |
| 14:05 | IC joins, declares SEV2 | War room created (#incident-002) | @sarah |
| 14:10 | Verified gradual degradation over 2 hours | Grafana shows steady climb | @mike |
| 14:15 | Checked recent deployments | No deployments in last 6 hours | @alex |
| 14:20 | Heap snapshot taken from slow worker | heapdump captured (2.3GB) | @mike |
| 14:30 | Heap analysis started (Chrome DevTools) | Loading snapshot... | @mike |
| 14:45 | Memory leak identified | EventEmitter listeners accumulating | @mike |
| 15:00 | Temporary fix: restart workers | kubectl rollout restart | @alex |
| 15:05 | Latency improved immediately | p95: 2000ms → 250ms | @sarah |
| 15:15 | Code review for EventEmitter usage | Found leak in data-processor.ts | @mike |
| 15:45 | Fix implemented and tested | Used .once() instead of .on() | @mike |
| 16:15 | Fix deployed to production | Canary deployment (10% → 100%) | @alex |
| 16:30 | Memory stabilized | No more growth, leak eliminated | @mike |
| 17:00 | Incident resolved | All metrics normal, monitoring continues | @sarah |

**Total Duration**: 3 hours from detection to permanent fix

---

## Severity Classification

### Why SEV2?

**SEV2 Criteria Met**:
- ✅ Partial degradation (30% of users affected)
- ✅ Elevated errors (timeout rate 2% vs baseline 0.01%)
- ✅ Performance impact (p95 latency 10x slower)
- ✅ SLO violation >10% (p95 latency SLA: 500ms, actual: 2000ms)
- ❌ NOT total outage (70% of users unaffected)

**Why Not SEV1**:
- ❌ NOT 100% outage (still serving most traffic)
- ❌ NOT all customers affected (only slow workers)
- ❌ Revenue still flowing (reduced but not stopped)
- ❌ Workaround available (users could retry)

**Business Impact**:
```
Revenue Impact: ~$15,000 (reduced conversion rate over 3 hours)
Customers Affected: ~30% (~15,000 users on slow workers)
Failed Requests: 2% timeout rate (vs 0.01% baseline)
Page Load Time: 3-8 seconds (vs 1-2 seconds normal)
Support Tickets: 34 (vs baseline 2/hour)
Conversion Rate: 2.5% (vs 3.8% baseline) - 34% drop
```

---

## Detection

### Initial Alert

**Grafana Alert** (14:00 UTC):
```
ALERT: [P2] API Latency High
Service: api-server
Metric: http_request_duration_p95
Threshold: >1000ms for 5 minutes
Current: 2000ms (vs baseline 200ms)
Trend: Increasing gradually over 2 hours
Dashboard: https://grafana.greyhaven.io/d/api-latency
```

**Gradual Degradation Pattern**:
```
12:00 UTC: p95 latency 200ms  ✅ Normal
12:30 UTC: p95 latency 400ms  ⚠️  Slow
13:00 UTC: p95 latency 800ms  ⚠️  Slow
13:30 UTC: p95 latency 1500ms 🚨 Very slow
14:00 UTC: p95 latency 2000ms 🔴 Alert fired
```

**User Reports** (via support tickets):
```
Ticket #1247 (13:45): "Dashboard is very slow to load"
Ticket #1248 (13:50): "Getting timeout errors when saving data"
Ticket #1249 (13:55): "Page takes 10+ seconds to load"
```

---

## Investigation

### Step 1: Check Recent Changes (14:15)

```bash
# Check recent deployments
kubectl rollout history deployment/api-server

REVISION  CHANGE-CAUSE
12        Deploy v2.15.3 (6 hours ago)
13        Deploy v2.15.4 (12 hours ago)

# No recent deployments - not a bad deploy
# Degradation started 2 hours ago, last deploy was 6 hours ago
```

**Hypothesis 1 Rejected**: Not caused by recent deployment

### Step 2: Check Infrastructure (14:20)

```bash
# Check worker CPU/memory
kubectl top pods -l app=api-server

NAME                CPU    MEMORY
api-server-abc123   45%    2.3Gi / 4Gi   # High memory!
api-server-def456   42%    2.1Gi / 4Gi   # High memory!
api-server-ghi789   15%    450Mi / 4Gi   # Normal (recently restarted)

# Memory leak suspected - workers with high uptime have high memory
```

**Pattern**: Workers with longer uptime have higher memory usage

### Step 3: Heap Snapshot Analysis (14:20-14:45)

**Capture Heap Snapshot**:
```bash
# Send SIGUSR2 to trigger heapdump
kubectl exec api-server-abc123 -- kill -USR2 1

# Download heap snapshot
kubectl cp api-server-abc123:/tmp/heapdump-*.heapsnapshot ./heap.heapsnapshot

# File size: 2.3GB (very large!)
```

**Chrome DevTools Analysis**:
```
1. Open Chrome DevTools → Memory → Load Profile
2. Load heap.heapsnapshot
3. View by Constructor:
   - Array: 1.8GB (78% of heap!)
   - Object: 350MB
   - String: 150MB

4. View Retainers for large Array:
   - EventEmitter listeners array
   - data-processor.ts:45 (processOrders function)
   - Never removed, accumulating indefinitely
```

**Memory Leak Identified**:
- EventEmitter listeners accumulating in Array
- Source: `data-processor.ts` line 45
- Pattern: `.on('data', handler)` without `.removeListener()`

### Step 4: Code Review (14:45-15:15)

**Problematic Code**:
```typescript
// ❌ BAD: src/data-processor.ts (BEFORE)
import { EventEmitter } from 'events';

class DataProcessor {
  private emitter = new EventEmitter();

  async processOrders(orders: Order[]) {
    for (const order of orders) {
      // Memory leak: listener never removed!
      this.emitter.on('data', (data) => {
        console.log('Processing order:', data);
        this.handleOrder(order);
      });

      this.emitter.emit('data', order);
    }
  }
}

// Called 1000x per minute
// Each call adds 1 listener
// After 2 hours: 120,000 listeners accumulated
// Memory: ~2GB of listener closures
```

**Memory Growth Pattern**:
```
12:00 - 10,000 listeners - 180MB
12:30 - 40,000 listeners - 720MB
13:00 - 70,000 listeners - 1.26GB
13:30 - 100,000 listeners - 1.80GB
14:00 - 120,000 listeners - 2.16GB (threshold)
```

---

## Mitigation

### Temporary Fix (15:00 - 15:05)

**Decision**: Restart workers to clear memory (buy time for permanent fix)

```bash
# Rolling restart of all worker pods
kubectl rollout restart deployment/api-server

# Watch pods restart
kubectl rollout status deployment/api-server

Waiting for deployment "api-server" rollout to finish: 1 old replicas pending termination...
Waiting for deployment "api-server" rollout to finish: 1 old replicas pending termination...
deployment "api-server" successfully rolled out

# Verify memory
kubectl top pods -l app=api-server

NAME                CPU    MEMORY
api-server-new123   12%    380Mi / 4Gi  ✅ Normal
api-server-new456   14%    420Mi / 4Gi  ✅ Normal
api-server-new789   11%    350Mi / 4Gi  ✅ Normal
```

**Result**:
- p95 latency: 2000ms → 250ms (immediately)
- Error rate: 2% → 0.01% (back to baseline)
- Memory: ~2GB → ~400MB per worker
- **Symptom resolved, but leak still exists in code**

### Permanent Fix (15:15 - 16:15)

**Fixed Code**:
```typescript
// ✅ GOOD: src/data-processor.ts (AFTER)
import { EventEmitter } from 'events';

class DataProcessor {
  private emitter = new EventEmitter();

  async processOrders(orders: Order[]) {
    for (const order of orders) {
      // Fix 1: Use .once() instead of .on() (auto-removes after first emit)
      this.emitter.once('data', (data) => {
        console.log('Processing order:', data);
        this.handleOrder(order);
      });

      this.emitter.emit('data', order);
    }
  }

  // Fix 2: Alternative - remove listener explicitly
  async processOrdersAlt(orders: Order[]) {
    for (const order of orders) {
      const handler = (data: any) => {
        console.log('Processing order:', data);
        this.handleOrder(order);
      };

      this.emitter.on('data', handler);
      this.emitter.emit('data', order);
      this.emitter.removeListener('data', handler);  // Explicit cleanup
    }
  }
}
```

**Testing**:
```bash
# Local testing with heap profiling
NODE_OPTIONS="--max-old-space-size=512" npm run test:memory

# Run for 10 minutes, process 10,000 orders
# Memory: 350MB (stable, no growth) ✅

# Old code would have grown to 1.8GB in same timeframe ❌
```

**Deployment** (16:15):
```bash
# Canary deployment (gradual rollout)
kubectl set image deployment/api-server api-server=ghcr.io/greyhaven/api:v2.15.5

# 10% traffic to new version
kubectl patch deployment/api-server -p '{"spec":{"strategy":{"rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'

# Monitor for 5 minutes (memory stable)
# Promote to 100%
kubectl rollout status deployment/api-server
```

---

## Root Cause Analysis (5 Whys)

**Why 1**: Why did the API become slow?
→ Because worker processes ran out of memory and became unresponsive

**Why 2**: Why did workers run out of memory?
→ Because EventEmitter listeners accumulated without being removed

**Why 3**: Why were listeners not removed?
→ Because `.on()` was used instead of `.once()`, and no explicit `.removeListener()` call

**Why 4**: Why was `.on()` used incorrectly?
→ Because the developer didn't understand that `.on()` creates a persistent listener

**Why 5**: Why wasn't this caught before production?
→ Because:
- No memory profiling in code review
- No memory leak detection in CI/CD
- No heap snapshot analysis for PRs
- No long-running load tests (only tested 5-minute runs)

**ROOT CAUSE**: Missing memory profiling in development process + developer education gap on EventEmitter lifecycle

---

## Communication

### Internal Updates (Slack #incident-002)

**14:05 - Incident Start**:
```
⚠️ SEV2 INCIDENT DECLARED
Incident ID: INC-2024-1210-002
Impact: API performance degraded, 30% of users slow
Symptoms: p95 latency 2000ms (vs 200ms baseline)
IC: @sarah
Technical Lead: @mike
Status: Investigating gradual degradation

Next update: 14:30 (or status change)
```

**15:00 - Temporary Fix Applied**:
```
📊 UPDATE #1 (T+55 minutes)
Root cause: Memory leak in EventEmitter listeners
Temporary fix: Restarting workers (in progress)
Permanent fix: Code change being developed
Impact: Still degraded, mitigation in progress
Next update: 15:30
```

**15:05 - Performance Restored**:
```
✅ UPDATE #2 (T+60 minutes)
Workers restarted successfully
p95 latency: Back to 250ms (normal)
Error rate: 0.01% (normal)
Impact: Performance restored
Status: Developing permanent fix to prevent recurrence
Next update: 16:00
```

**17:00 - Permanent Fix Deployed**:
```
🎉 INCIDENT RESOLVED (T+3 hours)
Permanent fix deployed (v2.15.5)
Memory leak eliminated (tested with heap profiling)
Memory: Stable at ~400MB per worker
Next steps: Postmortem tomorrow at 10:00
```

### External Communications

**Status Page** (14:10):
```
🟡 IDENTIFIED - Performance Degradation

We are experiencing performance degradation affecting some users.
Pages may load slowly, but all functionality remains available.
Our team is actively working on a fix.

Impact: 30% of users
Started: 14:00 UTC
Next update: 15:00 UTC
```

**Status Page** (15:05):
```
🟢 RESOLVED - Performance Restored

We have restored normal performance by restarting affected services.
We are deploying a permanent fix to prevent recurrence.

Impact: Resolved
Started: 14:00 UTC
Mitigated: 15:05 UTC
Permanent fix: Deploying
```

---

## Prevention Measures

### Immediate Actions (Completed Same Day)

- [x] Memory profiling added to CI/CD (fail build if memory grows >20% in 10min test)
- [x] Heap snapshot automation (weekly snapshots of production workers)
- [x] EventEmitter usage linter rule (warn on .on() without .removeListener())
- [x] Developer training: EventEmitter lifecycle best practices

### Short-Term Actions (Completed Within 1 Week)

- [x] Long-running load tests (4-hour tests vs 5-minute) - Day 2
- [x] Memory leak detection tool (automated heap snapshot comparison) - Day 3
- [x] Code review checklist: "Are EventEmitter listeners cleaned up?" - Day 4
- [x] Refactor all EventEmitter usage across codebase - Day 7

### Long-Term Actions (Completed Within 1 Month)

- [x] Memory budgets (per-route memory limits, fail CI if exceeded) - Week 2
- [x] Production memory monitoring (alert if worker memory >80% of limit) - Week 2
- [x] Chaos engineering: memory pressure testing (monthly) - Week 3
- [x] Developer education: memory management workshop - Week 4

---

## Blameless Postmortem

### What Went Well ✅

1. **Gradual Alert**: Alert fired before total outage, gave time to mitigate
2. **Heap Snapshot Analysis**: Quickly identified exact source of leak
3. **Temporary Mitigation**: Worker restart bought time for proper fix
4. **Canary Deployment**: Gradual rollout verified fix before full deployment
5. **Communication**: Clear updates, status page kept customers informed

### What Went Wrong ❌

1. **No Memory Profiling**: Leak not caught in development or code review
2. **Short Load Tests**: 5-minute tests didn't reveal gradual leak
3. **No Heap Monitoring**: No production heap snapshot automation
4. **Developer Gap**: Team didn't know `.once()` vs `.on()` difference
5. **Late Detection**: Took 2 hours to alert (should alert at 1 hour)

### Key Learnings

1. **Memory Leaks Are Gradual**: Short tests don't catch slow leaks
2. **Heap Snapshots Are Essential**: Only way to definitively find memory leaks
3. **EventEmitter Lifecycle**: `.once()` for single-use, `.on()` requires `.removeListener()`
4. **Temporary vs Permanent**: Worker restart bought time but didn't fix root cause
5. **Gradual Alerts**: Alert thresholds should catch degradation early

### Action Items (Tracked in Linear)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add memory profiling to CI/CD | @mike | Dec 10 | ✅ Done |
| Heap snapshot automation | @sarah | Dec 11 | ✅ Done |
| EventEmitter linter rule | @alex | Dec 11 | ✅ Done |
| Long-running load tests (4hr) | @mike | Dec 12 | ✅ Done |
| Refactor all EventEmitter usage | @team | Dec 17 | ✅ Done |
| Memory budgets per route | @sarah | Dec 20 | ✅ Done |
| Production heap monitoring | @mike | Dec 20 | ✅ Done |
| Memory management workshop | @sarah | Dec 22 | ✅ Done |

---

## Related Documentation

- **Similar Incidents**: [Memory Profiler Examples](../../../observability/agents/memory-profiler/examples/nodejs-memory-leak.md)
- **Runbooks**: [Memory Leak Investigation](../../reference/rca-techniques.md)
- **Heap Analysis Guide**: [Chrome DevTools Memory Profiling](https://developer.chrome.com/docs/devtools/memory-problems/)
- **EventEmitter Best Practices**: [Node.js Events Documentation](https://nodejs.org/api/events.html)

---

Return to [examples index](INDEX.md)
