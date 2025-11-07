# Performance Investigation: [ISSUE TITLE]

**Date Started**: [YYYY-MM-DD]
**Investigator**: [Name]
**Status**: [Active / Resolved / Monitoring]
**Last Updated**: [YYYY-MM-DD HH:MM UTC]

---

## Performance Baseline

### Current State

**Observed Metrics**:
```
[FILL IN: Current performance metrics]
Example:
API Response Time:
- p50: 1800ms (baseline: 200ms) - 9x slower
- p95: 2500ms (baseline: 500ms) - 5x slower
- p99: 4000ms (baseline: 800ms) - 5x slower

Error Rate: 2.5% (baseline: 0.01%) - 250x higher
Throughput: 50 req/s (baseline: 200 req/s) - 75% reduction
```

**Affected Components**:
- [FILL IN: Component 1 - Performance degradation details]
- [FILL IN: Component 2 - Performance degradation details]
- [FILL IN: Component 3 - Performance degradation details]

**User Impact**:
```
[FILL IN: How users are affected]
Example:
- Page load times: 3-5 seconds (was 1 second)
- API timeouts: 2.5% of requests
- User complaints: 12 support tickets in 1 hour
```

### Expected Baseline

**Historical Performance**:
```
[FILL IN: Normal performance metrics from past 30 days]
Example:
p50: 200ms
p95: 500ms
p99: 800ms
Error rate: 0.01%
Throughput: 200 req/s
```

**Performance Budget**:
```
[FILL IN: Acceptable performance thresholds]
Example:
p95 latency: < 500ms
p99 latency: < 1000ms
Error rate: < 0.1%
Database queries per request: < 10
```

**SLA Requirements**:
```
[FILL IN: Service level agreements]
Example:
Uptime: 99.9% (43.2 minutes downtime/month)
p95 latency: < 500ms
Error budget: 0.1%
```

---

## Initial Observations

### When Did It Start?

**Timeline**:
```
[FILL IN: When was degradation first noticed?]
Example:
First detected: 2024-12-05 08:15 UTC
Alerted by: Grafana (p95 latency > 1000ms)
User reports started: 08:30 UTC
```

**Recent Changes**:
```
[FILL IN: Any deployments, configuration changes, traffic spikes?]
Example:
Last deployment: 2024-12-05 06:00 UTC (2 hours before)
Code changes: New feature added (user dashboard)
Traffic: 50% increase from marketing campaign
```

### Scope of Impact

**Affected Endpoints**:
```
[FILL IN: Which APIs/pages are slow?]
Example:
/api/orders - 2000ms (10x slower)
/api/users - 500ms (normal)
/api/products - 1500ms (7x slower)
```

**Geographic Distribution**:
```
[FILL IN: All regions or specific locations?]
Example:
All regions affected equally (global issue)
OR: Only US-East region slow (regional issue)
```

**Traffic Patterns**:
```
[FILL IN: Consistent or intermittent? Peak hours?]
Example:
Consistent slowness (not time-dependent)
OR: Only during peak hours (9am-5pm EST)
OR: Intermittent spikes every 15 minutes
```

---

## Hypothesis Generation

### Potential Root Causes

**Hypothesis 1: [FILL IN: Most likely cause]**
```
Why we think this: [FILL IN: Evidence supporting this hypothesis]
How to test: [FILL IN: Experiment to validate/invalidate]
Likelihood: [High / Medium / Low]
```

**Hypothesis 2: [FILL IN: Second most likely cause]**
```
Why we think this: [FILL IN: Evidence supporting this hypothesis]
How to test: [FILL IN: Experiment to validate/invalidate]
Likelihood: [High / Medium / Low]
```

**Hypothesis 3: [FILL IN: Third possibility]**
```
Why we think this: [FILL IN: Evidence supporting this hypothesis]
How to test: [FILL IN: Experiment to validate/invalidate]
Likelihood: [High / Medium / Low]
```

### Common Performance Issues Checklist

- [ ] **N+1 Query Problem**: Multiple database queries per request
- [ ] **Missing Database Indexes**: Full table scans instead of index lookups
- [ ] **Connection Pool Exhaustion**: Database connections maxed out
- [ ] **Memory Leak**: Heap growing unbounded
- [ ] **CPU Saturation**: Workers/processes at 100% CPU
- [ ] **Network Latency**: DNS delays, slow external API calls
- [ ] **Large Payloads**: Oversized responses, no pagination
- [ ] **Cache Miss Storm**: Cache invalidated, all requests hitting DB
- [ ] **Bundle Size**: Large JavaScript bundle slowing page loads
- [ ] **Blocking Operations**: Synchronous I/O blocking event loop

---

## Data Collection

### Application Performance Monitoring

**Worker Tail Logs**:
```bash
[FILL IN: Command and output]
Example:
wrangler tail --format pretty

[2024-12-05 08:20:15] GET /api/orders - 2145ms
  └─ database_query: 1950ms (90% of total time!)
  └─ json_serialization: 150ms
  └─ response_headers: 45ms

Red flag: Database taking 90% of request time
```

**Profiling Data**:
```
[FILL IN: CPU/memory profiling results]
Example:
Chrome DevTools Performance:
- Scripting: 1200ms (60%)
- Rendering: 300ms (15%)
- System: 500ms (25%)

Top 3 functions by CPU time:
1. processOrders(): 800ms
2. validateData(): 300ms
3. formatResponse(): 100ms
```

### Database Analysis

**Query Performance**:
```bash
[FILL IN: Slow query log analysis]
Example:
pscale database insights greyhaven-db main --slow-queries

Query: SELECT * FROM order_items WHERE order_id = ?
Calls: 157 times per request  # N+1 query problem!
Avg time: 12ms per query
Total: 1884ms per request (12ms × 157)
```

**Connection Pool Status**:
```
[FILL IN: Pool utilization]
Example:
{
  "size": 20,
  "checked_out": 20,  # Pool exhausted!
  "overflow": 0,
  "idle": 0
}
```

**Missing Indexes**:
```sql
[FILL IN: EXPLAIN ANALYZE results]
Example:
EXPLAIN ANALYZE SELECT * FROM order_items WHERE order_id = 123;

Result:
Seq Scan on order_items  (cost=0.00..1500.00)
  Filter: (order_id = 123)
  Rows Removed by Filter: 10000

Full table scan! Need index on order_id.
```

### Network Diagnostics

**DNS Resolution**:
```bash
[FILL IN: DNS timing]
Example:
time nslookup api.partner.com

real    0m3.201s  # 3 second DNS delay!
```

**Request Timing**:
```bash
[FILL IN: curl timing breakdown]
Example:
curl -w "\nDNS:     %{time_namelookup}s\nConnect: %{time_connect}s\nTLS:     %{time_appconnect}s\nStart:   %{time_starttransfer}s\nTotal:   %{time_total}s\n" \
  -o /dev/null -s https://api.partner.com/data

DNS:     3.201s  # Very slow!
Connect: 3.450s
TLS:     3.780s
Start:   4.120s
Total:   4.823s
```

### Metrics and Graphs

**Grafana Dashboard Links**:
```
[FILL IN: Links to dashboards showing the issue]
Example:
CPU Usage: https://grafana.com/d/xyz/cpu
Memory Usage: https://grafana.com/d/abc/memory
Database Queries: https://grafana.com/d/def/database
```

---

## Analysis

### Data Reveals

**Finding 1**: [FILL IN: Key discovery from data]
```
[FILL IN: Evidence]
Example:
Database queries per request: 158 (1 initial + 157 N+1)
This accounts for 1884ms out of 2000ms total latency
N+1 query pattern confirmed
```

**Finding 2**: [FILL IN: Second key discovery]
```
[FILL IN: Evidence]
Example:
No index on order_items.order_id
EXPLAIN shows full table scan (10,000 rows)
Each query takes 12ms instead of <1ms with index
```

**Finding 3**: [FILL IN: Third key discovery]
```
[FILL IN: Evidence]
Example:
Connection pool at 100% capacity (20/20)
New requests waiting up to 30 seconds for connection
Pool too small for current load (16 workers × 2 = 32 needed)
```

### Root Cause Identified

**Primary Cause**:
[FILL IN: The main root cause]

**Contributing Factors**:
1. [FILL IN: Factor 1]
2. [FILL IN: Factor 2]
3. [FILL IN: Factor 3]

**Why This Causes Slowness**:
[FILL IN: Explain the technical mechanism of how this causes performance degradation]

---

## Optimization Plan

### Priority 1: Critical Fixes (Immediate Impact)

**Fix 1**: [FILL IN: Most impactful fix]
```
Implementation: [FILL IN: Code or config change]
Expected impact: [FILL IN: Estimated improvement]
Risk: [Low / Medium / High]
Rollback plan: [FILL IN: How to undo]
```

**Fix 2**: [FILL IN: Second most impactful fix]
```
Implementation: [FILL IN: Code or config change]
Expected impact: [FILL IN: Estimated improvement]
Risk: [Low / Medium / High]
Rollback plan: [FILL IN: How to undo]
```

### Priority 2: Important Improvements (Short-Term)

**Improvement 1**: [FILL IN: Important but not urgent]
```
Implementation: [FILL IN: Code or config change]
Expected impact: [FILL IN: Estimated improvement]
Timeline: [FILL IN: When this can be done]
```

**Improvement 2**: [FILL IN: Second improvement]
```
Implementation: [FILL IN: Code or config change]
Expected impact: [FILL IN: Estimated improvement]
Timeline: [FILL IN: When this can be done]
```

### Priority 3: Long-Term Optimizations

**Optimization 1**: [FILL IN: Architectural improvement]
```
Implementation: [FILL IN: What needs to change]
Expected impact: [FILL IN: Estimated improvement]
Timeline: [FILL IN: Quarters, not weeks]
```

---

## Implementation

### Fix 1: [FILL IN: Fix title]

**Before (Problem)**:
```
[FILL IN: Problematic code or configuration]
```

**After (Solution)**:
```
[FILL IN: Fixed code or configuration]
```

**Deployment**:
```bash
[FILL IN: Commands to deploy]
```

**Verification**:
```
[FILL IN: How to verify the fix worked]
```

### Fix 2: [FILL IN: Fix title]

**Before (Problem)**:
```
[FILL IN: Problematic code or configuration]
```

**After (Solution)**:
```
[FILL IN: Fixed code or configuration]
```

**Deployment**:
```bash
[FILL IN: Commands to deploy]
```

**Verification**:
```
[FILL IN: How to verify the fix worked]
```

---

## Validation

### Before vs After Metrics

| Metric | Before Fix | After Fix | Improvement |
|--------|-----------|-----------|-------------|
| **p50 Latency** | [FILL IN] | [FILL IN] | [FILL IN]% faster |
| **p95 Latency** | [FILL IN] | [FILL IN] | [FILL IN]% faster |
| **p99 Latency** | [FILL IN] | [FILL IN] | [FILL IN]% faster |
| **Error Rate** | [FILL IN] | [FILL IN] | [FILL IN]% reduction |
| **Throughput** | [FILL IN] | [FILL IN] | [FILL IN]% increase |
| **Database Queries** | [FILL IN] | [FILL IN] | [FILL IN]% reduction |

### User Impact Resolved

```
[FILL IN: How user experience improved]
Example:
Before: Page load 3-5 seconds, 2.5% timeouts
After: Page load 1 second, 0.01% timeouts
User complaints: 0 (vs 12/hour during incident)
```

### Cost Impact

```
[FILL IN: Infrastructure cost changes]
Example:
Database query reduction: 98.7% fewer queries
Cost savings: $450/month (reduced database tier)
Worker CPU reduction: 50% less CPU time
```

---

## Prevention Measures

### Monitoring Improvements

**New Alerts**:
```yaml
[FILL IN: Alert rules to detect this earlier]
Example:
- alert: SlowDatabaseQueries
  expr: histogram_quantile(0.95, database_query_duration_seconds) > 0.1
  for: 5m
  annotations:
    summary: "Database queries p95 >100ms"
```

**Dashboard Updates**:
- [FILL IN: Dashboard 1 - What was added]
- [FILL IN: Dashboard 2 - What was added]

### Testing Improvements

**Performance Tests**:
```
[FILL IN: New performance tests added to CI/CD]
Example:
- test_query_count_per_request() - Fail if >10 queries
- test_response_time_budget() - Fail if p95 >500ms
- test_n_plus_one_detection() - Detect N+1 patterns
```

**Load Testing**:
```bash
[FILL IN: Load testing added to release process]
Example:
npm run load-test -- --rps 200 --duration 5m
# Verify p95 <500ms under load before production deploy
```

### Code Quality

**Linting Rules**:
```
[FILL IN: New linting or code review requirements]
Example:
- Require .options(selectinload()) for associations
- Flag queries in loops (potential N+1)
- Require indexes for new foreign keys
```

---

## Lessons Learned

### What Worked Well ✅

1. [FILL IN: Good thing 1]
2. [FILL IN: Good thing 2]
3. [FILL IN: Good thing 3]

### What Could Improve ❌

1. [FILL IN: Area for improvement 1]
2. [FILL IN: Area for improvement 2]
3. [FILL IN: Area for improvement 3]

### Key Takeaways

1. [FILL IN: Lesson 1]
2. [FILL IN: Lesson 2]
3. [FILL IN: Lesson 3]

---

## Related Documentation

**Similar Investigations**:
- [FILL IN: Link to similar performance issue]
- [FILL IN: Link to related runbook]

**Updated Runbooks**:
- [FILL IN: Runbook updated based on this investigation]

---

## Template Notes

**How to use this template**:
1. Copy to your documentation when performance degrades >20%
2. Fill in sections systematically (don't skip data collection!)
3. Follow scientific method: hypothesis → test → analyze → fix
4. Measure before/after to validate improvements
5. Share findings with team in retrospective

**Performance Investigation Workflow**:
1. Establish baseline (what's normal?)
2. Collect data (logs, metrics, profiles)
3. Generate hypotheses (educated guesses)
4. Test hypotheses (run experiments)
5. Implement fixes (prioritized by impact)
6. Validate results (measure improvement)
7. Prevent recurrence (monitoring, testing)

---

Return to [templates index](INDEX.md)
