# SLO & Error Budget Framework

Complete Service Level Objective (SLO) and error budget implementation using Google SRE best practices with Prometheus and Grafana.

## Overview

**Before Implementation**:
- No reliability targets or accountability
- Unclear when to prioritize reliability vs features
- Incidents without context of customer impact
- "Move fast and break things" culture

**After Implementation**:
- Clear SLO targets: Critical (99.95%), Essential (99.9%), Standard (99.5%)
- Error budget policy: Feature freeze at 25% remaining
- Data-driven reliability decisions
- 3 feature freezes prevented budget exhaustion (saved 99.95% SLO)

**Technologies**: Prometheus recording rules, Grafana SLO dashboards, PagerDuty burn rate alerts

## SLO Framework

### SLI (Service Level Indicators)

**Definition**: Quantitative measures of service quality.

```yaml
# SLI Categories
availability:
  - description: Percentage of successful requests
  - formula: successful_requests / total_requests
  - measurement: HTTP status codes (2xx, 3xx = success)

latency:
  - description: Percentage of requests faster than threshold
  - formula: requests_under_threshold / total_requests
  - measurement: p95 latency < 200ms

error_rate:
  - description: Percentage of requests without errors
  - formula: (total_requests - error_requests) / total_requests
  - measurement: HTTP 5xx errors
```

### SLO (Service Level Objectives)

**Definition**: Target values for SLIs over a time window (usually 30 days).

```yaml
# Grey Haven SLO Tiers
critical_services:  # Payment processing, authentication
  availability: 99.95%  # 21.6 minutes downtime/month
  latency_p95: 200ms
  error_rate: 0.05%

essential_services:  # User-facing features
  availability: 99.9%  # 43.2 minutes downtime/month
  latency_p95: 500ms
  error_rate: 0.1%

standard_services:  # Analytics, reporting
  availability: 99.5%  # 3.6 hours downtime/month
  latency_p95: 1000ms
  error_rate: 0.5%
```

### Error Budget

**Definition**: Allowed downtime = 100% - SLO target.

```
99.95% SLO → 0.05% error budget → 21.6 min/month
99.9%  SLO → 0.1%  error budget → 43.2 min/month
99.5%  SLO → 0.5%  error budget → 3.6 hours/month
```

**Error Budget Calculation**:
```python
# 30-day window
total_minutes = 30 * 24 * 60 = 43,200 minutes

# For 99.95% SLO
error_budget_minutes = 43,200 * (1 - 0.9995) = 21.6 minutes

# For 99.9% SLO
error_budget_minutes = 43,200 * (1 - 0.999) = 43.2 minutes
```

## 1. Prometheus Recording Rules

### Multi-Window SLI Calculations

```yaml
# prometheus-slo-rules.yaml
groups:
  - name: slo_availability
    interval: 30s
    rules:
      # 1-hour window availability
      - record: greyhaven:sli:availability:1h
        expr: |
          sum(rate(http_requests_total{status=~"2..|3.."}[1h]))
          /
          sum(rate(http_requests_total[1h]))

      # 6-hour window availability
      - record: greyhaven:sli:availability:6h
        expr: |
          sum(rate(http_requests_total{status=~"2..|3.."}[6h]))
          /
          sum(rate(http_requests_total[6h]))

      # 24-hour window availability
      - record: greyhaven:sli:availability:24h
        expr: |
          sum(rate(http_requests_total{status=~"2..|3.."}[24h]))
          /
          sum(rate(http_requests_total[24h]))

      # 30-day window availability
      - record: greyhaven:sli:availability:30d
        expr: |
          sum(rate(http_requests_total{status=~"2..|3.."}[30d]))
          /
          sum(rate(http_requests_total[30d]))

  - name: slo_latency
    interval: 30s
    rules:
      # Latency SLI (p95 < 200ms)
      - record: greyhaven:sli:latency:1h
        expr: |
          sum(rate(http_request_duration_seconds_bucket{le="0.2"}[1h]))
          /
          sum(rate(http_request_duration_seconds_count[1h]))

      - record: greyhaven:sli:latency:6h
        expr: |
          sum(rate(http_request_duration_seconds_bucket{le="0.2"}[6h]))
          /
          sum(rate(http_request_duration_seconds_count[6h]))

      - record: greyhaven:sli:latency:30d
        expr: |
          sum(rate(http_request_duration_seconds_bucket{le="0.2"}[30d]))
          /
          sum(rate(http_request_duration_seconds_count[30d]))

  - name: slo_error_budget
    interval: 30s
    rules:
      # Error budget remaining (30-day window)
      - record: greyhaven:error_budget:remaining:30d
        expr: |
          1 - (
            (1 - greyhaven:sli:availability:30d)
            /
            (1 - 0.9995)  # 99.95% SLO target
          )

      # Error budget burn rate (1h window)
      - record: greyhaven:error_budget:burn_rate:1h
        expr: |
          (1 - greyhaven:sli:availability:1h)
          /
          (1 - 0.9995)

      # Error budget burn rate (6h window)
      - record: greyhaven:error_budget:burn_rate:6h
        expr: |
          (1 - greyhaven:sli:availability:6h)
          /
          (1 - 0.9995)
```

## 2. Burn Rate Alerts

### Multi-Burn-Rate Alerting

**Burn Rate Definition**: How fast you're consuming your error budget.

```
Burn rate = 1.0 → Consuming at expected rate (budget lasts 30 days)
Burn rate = 2.0 → Consuming 2x faster (budget lasts 15 days)
Burn rate = 14.4 → Consuming 14.4x faster (budget lasts 2 hours)
```

```yaml
# prometheus-slo-alerts.yaml
groups:
  - name: slo_alerts
    rules:
      # Critical: 14.4x burn rate over 1h (budget exhausted in 2 hours)
      - alert: ErrorBudgetBurnRateCritical
        expr: |
          greyhaven:error_budget:burn_rate:1h > 14.4
          and
          greyhaven:error_budget:burn_rate:6h > 14.4
        for: 2m
        labels:
          severity: critical
          slo_tier: critical
        annotations:
          summary: "Critical burn rate - budget exhausted in 2 hours"
          description: "Burn rate: {{ $value | humanize }}x (1h: {{ $labels.burn_rate_1h }}, 6h: {{ $labels.burn_rate_6h }})"
          runbook: "https://runbooks.greyhaven.io/slo-burn-rate"

      # High: 6x burn rate over 6h (budget exhausted in 5 days)
      - alert: ErrorBudgetBurnRateHigh
        expr: |
          greyhaven:error_budget:burn_rate:6h > 6
          and
          greyhaven:error_budget:burn_rate:24h > 6
        for: 15m
        labels:
          severity: warning
          slo_tier: critical
        annotations:
          summary: "High burn rate - budget exhausted in 5 days"
          description: "Burn rate: {{ $value | humanize }}x"

      # Medium: 3x burn rate over 24h (budget exhausted in 10 days)
      - alert: ErrorBudgetBurnRateMedium
        expr: |
          greyhaven:error_budget:burn_rate:24h > 3
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Medium burn rate - budget exhausted in 10 days"

      # Budget exhaustion warning (25% remaining)
      - alert: ErrorBudgetLow
        expr: greyhaven:error_budget:remaining:30d < 0.25
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Error budget low ({{ $value | humanizePercentage }} remaining)"
          description: "Consider feature freeze per error budget policy"

      # Budget depleted (0% remaining)
      - alert: ErrorBudgetDepleted
        expr: greyhaven:error_budget:remaining:30d <= 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error budget depleted - feature freeze required"
          description: "SLO violated. Postmortem required."
```

## 3. Grafana SLO Dashboard

```json
{
  "dashboard": {
    "title": "SLO & Error Budget - Grey Haven",
    "tags": ["slo", "reliability"],
    "panels": [
      {
        "id": 1,
        "title": "SLO Status (30d)",
        "type": "stat",
        "targets": [{"expr": "greyhaven:sli:availability:30d * 100", "legendFormat": "Availability %"}],
        "thresholds": {"mode": "absolute", "steps": [
          {"value": 0, "color": "red"},
          {"value": 99.5, "color": "yellow"},
          {"value": 99.95, "color": "green"}
        ]}
      },
      {
        "id": 2,
        "title": "Error Budget Remaining",
        "type": "gauge",
        "targets": [{"expr": "greyhaven:error_budget:remaining:30d * 100"}],
        "thresholds": [
          {"value": 0, "color": "red"},
          {"value": 25, "color": "yellow"},
          {"value": 50, "color": "green"}
        ]
      },
      {
        "id": 3,
        "title": "Burn Rate (Multi-Window)",
        "type": "graph",
        "targets": [
          {"expr": "greyhaven:error_budget:burn_rate:1h", "legendFormat": "1h"},
          {"expr": "greyhaven:error_budget:burn_rate:6h", "legendFormat": "6h"},
          {"expr": "greyhaven:error_budget:burn_rate:24h", "legendFormat": "24h"}
        ],
        "thresholds": [
          {"value": 1, "colorMode": "ok"},
          {"value": 3, "colorMode": "warning"},
          {"value": 6, "colorMode": "critical"}
        ]
      },
      {
        "id": 4,
        "title": "SLI Trends (7 days)",
        "type": "graph",
        "targets": [
          {"expr": "greyhaven:sli:availability:24h * 100", "legendFormat": "Availability"},
          {"expr": "greyhaven:sli:latency:24h * 100", "legendFormat": "Latency"}
        ]
      }
    ]
  }
}
```

## 4. Error Budget Policy

### Decision Framework

```yaml
# error-budget-policy.yaml
policy:
  tiers:
    critical: {slo_target: 99.95%, error_budget: 0.05%, window: 30d}
    essential: {slo_target: 99.9%, error_budget: 0.1%, window: 30d}

  actions:
    - budget_range: [75%, 100%]
      action: "Normal feature development"

    - budget_range: [50%, 75%]
      action: "Continue with caution, increase monitoring"

    - budget_range: [25%, 50%]
      action: "Prioritize reliability work, reduce risky changes"
      approval: "Engineering manager"

    - budget_range: [0%, 25%]
      action: "Feature freeze, all hands on reliability"
      approval: "VP Engineering"
      requirements: ["Daily reliability standup", "Postmortem all incidents", "No features until >50%"]

    - budget_range: [0%, 0%]
      action: "SLO violation - mandatory postmortem"
      approval: "VP Engineering + CTO"
      requirements: ["Postmortem within 48h", "Action items with owners", "Present to exec team"]

  review: {frequency: "Weekly", participants: ["Engineering", "Product", "SRE"]}
```

## 5. Implementation Example

### TypeScript Server Function with SLO Tracking

```typescript
// middleware/slo-tracking.ts
import { Counter, Histogram } from 'prom-client';

const httpRequests = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status']
});

const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route'],
  buckets: [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]  # SLO: p95 < 200ms
});

export function sloMiddleware() {
  return async (request: Request, next: () => Promise<Response>) => {
    const start = Date.now();
    const route = new URL(request.url).pathname;

    try {
      const response = await next();

      // Track request for SLO calculation
      httpRequests.inc({
        method: request.method,
        route,
        status: response.status.toString()
      });

      httpDuration.observe({
        method: request.method,
        route
      }, (Date.now() - start) / 1000);

      return response;
    } catch (error) {
      // Track errors for SLO
      httpRequests.inc({
        method: request.method,
        route,
        status: '500'
      });
      throw error;
    }
  };
}
```

## 6. Real-World Example: Feature Freeze

### Scenario

**Date**: 2024-12-15
**Service**: Payment processing API
**SLO**: 99.95% availability (21.6 min downtime/month)

**Incident Timeline**:
```
Dec 10: Database connection pool exhaustion → 15 min outage
Dec 12: Redis cache failure → 8 min outage
Dec 14: 5xx errors from Stripe integration → 3 min partial outage

Total downtime: 26 minutes (exceeded 21.6 min budget)
Error budget: -20% (depleted)
```

**Error Budget Policy Triggered**:
1. ✅ Feature freeze enacted immediately
2. ✅ All hands on reliability (3 engineers pulled from feature work)
3. ✅ Daily standups on reliability work
4. ✅ Postmortem scheduled within 48 hours

**Actions Taken**:
1. **Database connection pool**: Increased from 20 → 50 connections
2. **Redis**: Implemented circuit breaker with fallback
3. **Stripe**: Added retry logic with exponential backoff
4. **Monitoring**: Added connection pool saturation alerts

**Results**:
- No outages for next 15 days
- Error budget recovered to 80% remaining
- Feature freeze lifted on Dec 30
- SLO achieved: 99.96% (exceeded 99.95% target)

## 7. Results and Impact

### Before vs After Metrics

| Metric | Before SLO | After SLO | Impact |
|--------|-----------|-----------|---------|
| **Availability** | Unknown | 99.95% tracked | **SLO compliance** |
| **Feature Freezes** | Arbitrary | 3 data-driven | **Clear policy** |
| **Incident Response** | Reactive | Proactive (burn rate alerts) | **2-5 min detection** |
| **Reliability Investment** | Ad-hoc | Budget-driven | **Balanced with features** |
| **Customer Impact** | Unknown | Quantified (21.6 min/month) | **Transparency** |

### Key Learnings

**1. Error Budget as Currency**
- Product team understands: "We have 21.6 minutes of downtime to spend"
- Engineering can say "no" to risky features: "We don't have the error budget"
- Data-driven decisions replace gut feelings

**2. Burn Rate Alerts Prevent Exhaustion**
- 3 incidents detected via burn rate alerts before budget exhaustion
- Feature freezes enacted proactively, preventing SLO violations

**3. Shared Responsibility**
- Product and engineering aligned on reliability targets
- Weekly SLO reviews create accountability

## Related Documentation

- **Prometheus**: [prometheus-grafana-setup.md](prometheus-grafana-setup.md) - Metrics collection
- **Tracing**: [opentelemetry-tracing.md](opentelemetry-tracing.md) - Distributed tracing
- **Reference**: [../reference/slo-best-practices.md](../reference/slo-best-practices.md) - Google SRE patterns
- **Templates**: [../templates/slo-definition.yaml](../templates/slo-definition.yaml) - SLO config template

---

Return to [examples index](INDEX.md)
