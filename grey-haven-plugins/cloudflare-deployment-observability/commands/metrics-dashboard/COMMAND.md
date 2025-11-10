---
name: cf-metrics-dashboard
description: Display comprehensive deployment and performance metrics dashboard for Cloudflare Workers and Pages with GitHub Actions CI/CD integration
---

Display a comprehensive metrics dashboard for Cloudflare Workers and Pages deployments, including deployment metrics, performance data, CI/CD pipeline health, and Core Web Vitals.

## What This Command Does

1. **Deployment Metrics**
   - Deployment frequency
   - Success/failure rate
   - Mean time to deployment (MTTD)
   - Rollback frequency
   - Deployment duration trends

2. **Performance Metrics**
   - Request latency (p50, p95, p99)
   - Error rates
   - Requests per second
   - Cold start metrics
   - Bundle size trends

3. **CI/CD Pipeline Metrics**
   - Workflow success rate
   - Pipeline duration
   - Job-level performance
   - GitHub Actions minutes usage
   - Queue time analysis

4. **Core Web Vitals**
   - LCP (Largest Contentful Paint)
   - FID (First Input Delay)
   - CLS (Cumulative Layout Shift)
   - TTFB (Time to First Byte)

## Usage

```bash
# Show all metrics
/cf-metrics-dashboard

# Specific time range
/cf-metrics-dashboard --range 7d
/cf-metrics-dashboard --range 24h
/cf-metrics-dashboard --range 30d

# Specific worker
/cf-metrics-dashboard --worker production-worker

# Specific environment
/cf-metrics-dashboard --env production

# Compare deployments
/cf-metrics-dashboard --compare abc123 xyz789

# Export to file
/cf-metrics-dashboard --export dashboard.json

# Specific metric groups
/cf-metrics-dashboard --metrics deployment,performance
/cf-metrics-dashboard --metrics cicd
/cf-metrics-dashboard --metrics web-vitals
```

## Dashboard Output

### Full Dashboard View

```markdown
# Cloudflare Deployment Metrics Dashboard

**Worker**: production-worker
**Environment**: production
**Period**: Last 7 days
**Generated**: 2025-01-15 10:30:00 UTC

---

## 📊 Executive Summary

| Metric | Value | Trend | Status |
|--------|-------|-------|--------|
| Deployment Success Rate | 96% | ↑ +2% | ✅ Good |
| Average Deployment Time | 2m 45s | ↓ -15s | ✅ Good |
| Error Rate | 0.08% | ↓ -0.02% | ✅ Good |
| P95 Latency | 125ms | ↑ +10ms | ⚠️ Warning |
| Core Web Vitals Score | 92/100 | → 0 | ✅ Good |

---

## 🚀 Deployment Metrics

### Deployment Frequency
```
Week view:
Mon ████████████ 12 deployments
Tue ██████ 6 deployments
Wed █████████ 9 deployments
Thu ███████████ 11 deployments
Fri ████████ 8 deployments
Sat ████ 4 deployments
Sun ██ 2 deployments

Total: 52 deployments
Average: 7.4 deployments/day
```

### Deployment Success Rate
```
Last 7 days: 96% (50/52 successful)
Last 30 days: 94% (198/210 successful)

Trend: ↑ Improving
```

### Deployment Duration
| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| Mean | 2m 45s | 3m 00s | ↓ -15s |
| P95 | 4m 30s | 5m 00s | ↓ -30s |
| P99 | 6m 15s | 7m 00s | ↓ -45s |
| Max | 8m 20s | 9m 30s | ↓ -1m 10s |

**Trend**: ✅ Improving (15% faster)

### Recent Deployments
| Time | Status | Duration | Commit | Environment |
|------|--------|----------|--------|-------------|
| 2h ago | ✅ Success | 2m 30s | abc123 | production |
| 4h ago | ✅ Success | 2m 45s | def456 | staging |
| 6h ago | ❌ Failed | 1m 20s | ghi789 | production |
| 8h ago | ✅ Success | 3m 10s | jkl012 | production |
| 10h ago | ✅ Success | 2m 55s | mno345 | staging |

### Rollback Activity
```
Total rollbacks (7d): 2
Rollback rate: 3.8%

Reasons:
- Build failure: 1
- Post-deployment errors: 1

Mean time to rollback: 5m 30s
```

---

## ⚡ Performance Metrics

### Request Latency
```
Current (last hour):
p50: 45ms  ████████████░░░░░░░░
p75: 82ms  ████████████████░░░░
p95: 125ms █████████████████░░░
p99: 245ms ███████████████████░

Target thresholds:
p50: <50ms  ✅ Met
p95: <200ms ✅ Met
p99: <500ms ✅ Met
```

**7-day trend**:
```
Day 1: p95=115ms ████████████░
Day 2: p95=118ms █████████████░
Day 3: p95=120ms █████████████░
Day 4: p95=125ms ██████████████
Day 5: p95=122ms █████████████░
Day 6: p95=125ms ██████████████
Day 7: p95=125ms ██████████████

Trend: ↑ Slight increase (+10ms)
```

### Request Volume
```
Requests/second (current): 1,245 rps
Requests/day (average): 107M requests

Peak: 2,180 rps (09:00 UTC)
Trough: 340 rps (03:00 UTC)
```

### Error Rates
| Error Type | Count | Rate | Trend |
|------------|-------|------|-------|
| 5xx errors | 850 | 0.08% | ↓ Good |
| 4xx errors | 12,400 | 1.16% | → Stable |
| Timeouts | 120 | 0.01% | ↓ Good |
| Total | 13,370 | 1.25% | ↓ Good |

**Target**: <1% error rate for 5xx errors ✅ Met

### Cold Start Analysis
```
Cold starts (7d): 3,420
Cold start rate: 0.32% of requests

Duration distribution:
p50: 180ms ████████████████░░░░
p95: 350ms ███████████████████░
p99: 520ms ████████████████████

Impact: Minimal (<0.5% of requests)
```

### Bundle Size
```
Current: 512 KB ████████████████░░░░
Maximum: 750 KB ████████████████████
Percentage: 68% of limit

7-day trend:
Day 1: 505 KB ████████████████░░░░
Day 2: 508 KB ████████████████░░░░
Day 3: 510 KB ████████████████░░░░
Day 4: 512 KB ████████████████░░░░
Day 5: 512 KB ████████████████░░░░
Day 6: 512 KB ████████████████░░░░
Day 7: 512 KB ████████████████░░░░

Change: +7 KB (+1.4%)
Status: ✅ Under control
```

---

## 🔄 CI/CD Pipeline Metrics

### GitHub Actions Performance
```
Workflow: Deploy to Cloudflare
Total runs (7d): 52
Success rate: 96% (50/52)

Duration breakdown:
├─ Build job: 2m 15s (50%)
├─ Test job: 1m 30s (33%)
└─ Deploy job: 45s (17%)

Total average: 4m 30s
```

### Job-Level Performance
| Job | Avg Duration | Success Rate | Trend |
|-----|--------------|--------------|-------|
| Build | 2m 15s | 98% | ↓ -10s |
| Test | 1m 30s | 96% | → 0s |
| Deploy | 45s | 100% | ↓ -5s |

### Cache Effectiveness
```
npm cache hit rate: 87%
Build cache hit rate: 72%

Time saved by caching:
- npm install: 1m 20s → 15s (saved 1m 05s)
- Build: 2m 30s → 45s (saved 1m 45s)

Total time saved per run: 2m 50s
```

### GitHub Actions Minutes Usage
```
Total minutes (7d): 234 minutes
Average per run: 4.5 minutes
Projected monthly: ~1,000 minutes

Cost (estimated): $0.00 (within free tier)
```

### Failure Analysis
```
Failed runs (7d): 2

Failure breakdown:
- Build failures: 1 (50%)
- Test failures: 0 (0%)
- Deployment failures: 1 (50%)

Mean time to fix: 15 minutes
```

---

## 🌐 Core Web Vitals

### Overall Score: 92/100 ✅

| Metric | Value | Target | Status | Trend |
|--------|-------|--------|--------|-------|
| LCP (p75) | 1.8s | <2.5s | ✅ Good | → Stable |
| FID (p75) | 45ms | <100ms | ✅ Good | ↓ Better |
| CLS (p75) | 0.05 | <0.1 | ✅ Good | → Stable |
| FCP (p75) | 1.2s | <1.8s | ✅ Good | → Stable |
| TTFB (p75) | 420ms | <600ms | ✅ Good | ↑ +20ms |

### LCP (Largest Contentful Paint)
```
Distribution:
Good (<2.5s):    ████████████████████ 89% ✅
Needs work (2.5-4s): ███ 8% ⚠️
Poor (>4s):      █ 3% ❌

p75 value: 1.8s ✅ Good
Target: <2.5s
```

### FID (First Input Delay)
```
Distribution:
Good (<100ms):   ████████████████████ 95% ✅
Needs work (100-300ms): █ 4% ⚠️
Poor (>300ms):   ░ 1% ❌

p75 value: 45ms ✅ Good
Target: <100ms
```

### CLS (Cumulative Layout Shift)
```
Distribution:
Good (<0.1):     ████████████████████ 92% ✅
Needs work (0.1-0.25): ██ 6% ⚠️
Poor (>0.25):    ░ 2% ❌

p75 value: 0.05 ✅ Good
Target: <0.1
```

### Geographic Performance
| Region | LCP | FID | CLS | Score |
|--------|-----|-----|-----|-------|
| US-East | 1.6s | 42ms | 0.04 | 95/100 ✅ |
| US-West | 1.7s | 44ms | 0.05 | 94/100 ✅ |
| EU-West | 1.9s | 48ms | 0.06 | 91/100 ✅ |
| APAC | 2.2s | 55ms | 0.07 | 88/100 ⚠️ |

**Note**: APAC region slightly slower, still meeting targets

---

## 📈 Trends & Insights

### Key Findings
1. ✅ Deployment speed improved 15% over last week
2. ⚠️ P95 latency increased by 10ms (monitoring)
3. ✅ Error rate decreased by 0.02%
4. ✅ Core Web Vitals stable and meeting targets
5. ✅ CI/CD pipeline optimized with caching

### Performance Regressions Detected
None. All metrics within acceptable thresholds.

### Recommendations
1. **Medium Priority**: Investigate P95 latency increase
   - Started: 3 days ago
   - Impact: +10ms (still within target)
   - Action: Review recent code changes

2. **Low Priority**: Optimize APAC region performance
   - LCP slightly higher (2.2s vs 1.8s average)
   - Still meeting targets (<2.5s)
   - Action: Consider regional caching strategy

### Upcoming Alerts
⚠️ Bundle size approaching 70% of limit
- Current: 512 KB / 750 KB
- Action: Plan bundle size optimization

---

## 📊 Historical Comparison

### vs. Last Week
| Metric | Current | Last Week | Change |
|--------|---------|-----------|--------|
| Deployment frequency | 52 | 48 | +4 (+8%) |
| Success rate | 96% | 94% | +2% |
| Avg deployment time | 2m 45s | 3m 00s | -15s (-8%) |
| Error rate | 0.08% | 0.10% | -0.02% |
| P95 latency | 125ms | 115ms | +10ms (+9%) |

### vs. Last Month
| Metric | Current | Last Month | Change |
|--------|---------|------------|--------|
| Deployment frequency | 52/wk | 45/wk | +7 (+16%) |
| Success rate | 96% | 92% | +4% |
| Avg deployment time | 2m 45s | 3m 30s | -45s (-21%) |
| Error rate | 0.08% | 0.12% | -0.04% |
| P95 latency | 125ms | 130ms | -5ms (-4%) |

---

## 🎯 SLO Status

### Service Level Objectives
| SLO | Target | Current | Status | Remaining Error Budget |
|-----|--------|---------|--------|------------------------|
| Availability | 99.9% | 99.92% | ✅ Met | 80% remaining |
| P95 Latency | <200ms | 125ms | ✅ Met | 37% used |
| Error Rate | <1% | 0.08% | ✅ Met | 92% remaining |
| Deployment Success | >95% | 96% | ✅ Met | 20% buffer |

**Error Budget Status**: ✅ Healthy
- 80% error budget remaining
- Current burn rate: Low
- Projected to meet SLOs for next 30 days

---

## 🔔 Active Alerts

No active alerts. All systems operational. ✅

---

## 💡 Next Actions

1. Continue monitoring P95 latency trend
2. Review code changes from last 3 days
3. Plan bundle size optimization for next sprint
4. Consider APAC region caching improvements

---

**Report Generated**: 2025-01-15 10:30:00 UTC
**Next Update**: Automatic (every hour) or run `/cf-metrics-dashboard` anytime
```

## Metric Categories

### 1. Deployment Metrics
- **Frequency**: Deployments per day/week
- **Success Rate**: % of successful deployments
- **Duration**: Time to complete deployment
- **Rollback Rate**: Frequency of rollbacks
- **MTTD**: Mean Time To Deployment

### 2. Performance Metrics
- **Latency**: p50, p95, p99 response times
- **Error Rates**: 4xx, 5xx, timeout errors
- **Throughput**: Requests per second
- **Cold Starts**: Frequency and duration
- **Bundle Size**: Size trends

### 3. CI/CD Metrics
- **Workflow Success Rate**: GitHub Actions success %
- **Pipeline Duration**: Total workflow time
- **Job Performance**: Individual job times
- **Cache Hit Rate**: Effectiveness of caching
- **GitHub Actions Minutes**: Usage tracking

### 4. User Experience Metrics
- **Core Web Vitals**: LCP, FID, CLS
- **TTFB**: Time to First Byte
- **FCP**: First Contentful Paint
- **Geographic Performance**: Regional metrics

## Advanced Features

### Metric Comparison

Compare different deployments:
```bash
/cf-metrics-dashboard --compare abc123 xyz789
```

Output shows side-by-side comparison with deltas.

### Custom Time Ranges

```bash
# Last 24 hours
/cf-metrics-dashboard --range 24h

# Last 7 days (default)
/cf-metrics-dashboard --range 7d

# Last 30 days
/cf-metrics-dashboard --range 30d

# Custom range
/cf-metrics-dashboard --from 2025-01-01 --to 2025-01-15
```

### Filtered Views

Show specific metric categories:
```bash
# Only deployment metrics
/cf-metrics-dashboard --metrics deployment

# Only performance metrics
/cf-metrics-dashboard --metrics performance

# Multiple categories
/cf-metrics-dashboard --metrics deployment,performance,cicd
```

### Export Options

```bash
# Export to JSON
/cf-metrics-dashboard --export dashboard.json

# Export to CSV
/cf-metrics-dashboard --export metrics.csv

# Send to monitoring platform
/cf-metrics-dashboard --export datadog
```

## Integration

### With Monitoring Tools

Send metrics to external platforms:
- **Datadog**: Send metrics and events
- **Sentry**: Performance monitoring
- **Grafana**: Custom dashboards
- **CloudWatch**: AWS integration

### With Alerting

Set up alerts based on thresholds:
```javascript
{
  "alerts": [
    {
      "metric": "deployment_success_rate",
      "threshold": 0.95,
      "operator": "<",
      "action": "notify_slack"
    },
    {
      "metric": "p95_latency_ms",
      "threshold": 200,
      "operator": ">",
      "action": "create_incident"
    }
  ]
}
```

## Best Practices

1. **Regular Review**
   - Check dashboard daily
   - Review weekly trends
   - Monthly deep dives

2. **Threshold Monitoring**
   - Set up alerts for SLO violations
   - Track error budget consumption
   - Monitor trend changes

3. **Historical Analysis**
   - Compare with previous periods
   - Identify seasonal patterns
   - Track long-term improvements

4. **Actionable Insights**
   - Focus on trends, not just absolute values
   - Investigate significant changes
   - Correlate metrics with deployments

## Related Commands

- `/cf-deployment-status` - Check current deployment status
- `/cf-logs-analyze` - Analyze logs for errors
- Use `cloudflare-performance-tracker` agent for detailed performance analysis
- Use `cloudflare-deployment-monitor` agent for active monitoring

## Configuration

Customize dashboard settings:

```json
// .claude/settings.json
{
  "cloudflare-metrics": {
    "default_range": "7d",
    "default_worker": "production-worker",
    "refresh_interval": "1h",
    "thresholds": {
      "p95_latency_ms": 200,
      "error_rate": 0.01,
      "deployment_success_rate": 0.95
    },
    "web_vitals_targets": {
      "lcp": 2.5,
      "fid": 100,
      "cls": 0.1
    }
  }
}
```

## Troubleshooting

**No metrics available**:
- Check Cloudflare API access
- Verify worker name
- Ensure analytics are enabled

**Incomplete data**:
- Analytics may have delay (up to 5 minutes)
- Check date range
- Verify data retention settings

**Metrics don't match other tools**:
- Check time zone differences
- Verify aggregation methods
- Compare data sources
