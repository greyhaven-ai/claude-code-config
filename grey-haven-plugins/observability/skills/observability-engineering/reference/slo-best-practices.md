# SLO Best Practices

Google SRE Service Level Objective (SLO) framework implementation guide with error budgets and multi-window burn rate alerting.

## SLI/SLO/SLA Definitions

### SLI (Service Level Indicator)

**Definition**: Quantitative measure of a service's behavior.

**Examples**:
- Availability: % of successful HTTP requests
- Latency: % of requests faster than threshold
- Throughput: Requests processed per second

### SLO (Service Level Objective)

**Definition**: Target value or range for an SLI over a time period.

**Examples**:
- Availability SLO: 99.9% of requests succeed (30-day window)
- Latency SLO: 95% of requests complete in <200ms
- Error Rate SLO: <0.5% error rate

### SLA (Service Level Agreement)

**Definition**: Business contract with consequences for missing SLO.

**Examples**:
- If availability <99.9%, customer receives 10% credit
- If p95 latency >500ms, customer receives 5% credit

**Key difference**: SLO = internal target, SLA = external contract

## SLO Tiers

### Critical Services (99.95% Availability)

**Use for**: Payment processing, authentication, data consistency

**Error budget**: 0.05% = 21.6 minutes downtime/month

**Example**:
```yaml
slo:
  tier: critical
  availability: 99.95%
  latency_p95: 200ms
  error_budget: 21.6min/month
```

**Incident response**: Page on-call immediately, postmortem required

### Essential Services (99.9% Availability)

**Use for**: Core user-facing features (orders, checkout, profiles)

**Error budget**: 0.1% = 43.2 minutes downtime/month

**Example**:
```yaml
slo:
  tier: essential
  availability: 99.9%
  latency_p95: 500ms
  error_budget: 43.2min/month
```

**Incident response**: Page during business hours, postmortem recommended

### Standard Services (99.5% Availability)

**Use for**: Analytics, reporting, admin features

**Error budget**: 0.5% = 3.6 hours downtime/month

**Example**:
```yaml
slo:
  tier: standard
  availability: 99.5%
  latency_p95: 1000ms
  error_budget: 3.6hours/month
```

**Incident response**: Ticket created, fix in next sprint

## SLI Selection

### Good SLIs

**Characteristics**:
- Directly impacts user experience
- Measurable and objective
- Actionable (can be improved)

**Availability SLI**:
```promql
# Good: HTTP success rate (user-facing)
sum(rate(http_requests_total{status=~"2..|3.."}[30d]))
/
sum(rate(http_requests_total[30d]))
```

**Latency SLI**:
```promql
# Good: Percentage of requests under threshold
sum(rate(http_request_duration_seconds_bucket{le="0.2"}[30d]))
/
sum(rate(http_request_duration_seconds_count[30d]))
```

### Bad SLIs

**Avoid**:
- Internal metrics (cache hit rate, database connections)
- Vanity metrics (page views, user signups)
- Metrics not tied to user experience

## Multi-Window Burn Rate Alerts

### Burn Rate Definition

**Burn rate**: How fast you're consuming your error budget.

```
Burn rate = 1.0 → Budget lasts 30 days (expected)
Burn rate = 2.0 → Budget lasts 15 days (consuming 2x faster)
Burn rate = 14.4 → Budget lasts 2 hours (critical)
```

### Alert Windows

**Principle**: Use multiple time windows to balance sensitivity vs noise.

**Fast burn (1h + 6h windows)**:
- Detects severe incidents quickly
- Budget exhausted in 2 hours at current rate
- Page immediately

**Slow burn (6h + 24h windows)**:
- Detects moderate issues
- Budget exhausted in 5 days at current rate
- Page during business hours

### Implementation

```yaml
# Multi-window burn rate alerts
groups:
  - name: slo_burn_rate
    rules:
      # Critical: 14.4x burn rate (budget exhausted in 2h)
      - alert: ErrorBudgetBurnRateCritical
        expr: |
          (1 - http_request_success_rate_1h) / (1 - 0.999) > 14.4
          and
          (1 - http_request_success_rate_6h) / (1 - 0.999) > 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Critical burn rate - budget exhausted in 2 hours"

      # High: 6x burn rate (budget exhausted in 5 days)
      - alert: ErrorBudgetBurnRateHigh
        expr: |
          (1 - http_request_success_rate_6h) / (1 - 0.999) > 6
          and
          (1 - http_request_success_rate_24h) / (1 - 0.999) > 6
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "High burn rate - budget exhausted in 5 days"

      # Medium: 3x burn rate (budget exhausted in 10 days)
      - alert: ErrorBudgetBurnRateMedium
        expr: |
          (1 - http_request_success_rate_24h) / (1 - 0.999) > 3
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Medium burn rate - budget exhausted in 10 days"
```

### Alert Thresholds (99.9% SLO)

| Window | Burn Rate | Budget Exhausted In | Severity | Action |
|--------|-----------|---------------------|----------|--------|
| 1h + 6h | 14.4x | 2 hours | Critical | Page immediately |
| 6h + 24h | 6x | 5 days | Warning | Page business hours |
| 24h | 3x | 10 days | Warning | Ticket created |

## Error Budget Policy

### Budget Allocation

**100% budget remaining** (0 downtime):
- Full speed feature development
- Take calculated risks
- Approval: Engineering team

**75-100% budget remaining**:
- Normal development pace
- Monitor closely
- Approval: Engineering team

**50-75% budget remaining**:
- Reduce risky changes
- Increase testing
- Approval: Engineering team

**25-50% budget remaining**:
- Prioritize reliability work
- Code freeze on risky features
- Approval: Engineering manager

**0-25% budget remaining**:
- Feature freeze (all hands on reliability)
- Daily reliability standup
- No new features until budget >50%
- Approval: VP Engineering

**Budget depleted (0% remaining)**:
- SLO violation
- Mandatory postmortem within 48 hours
- Exec team presentation
- Approval: VP Engineering + CTO

### Example Policy

```yaml
# error-budget-policy.yaml
policy:
  name: "Grey Haven Error Budget Policy"
  slo_target: 99.9%
  time_window: 30d

  actions:
    - budget_range: [75%, 100%]
      action: "Normal development"
      approval: "Team"

    - budget_range: [50%, 75%]
      action: "Reduce risky changes"
      approval: "Team"

    - budget_range: [25%, 50%]
      action: "Prioritize reliability"
      approval: "Manager"

    - budget_range: [0%, 25%]
      action: "Feature freeze"
      approval: "VP Engineering"
      requirements:
        - "Daily reliability standup"
        - "Postmortem all incidents"
        - "No features until >50%"

    - budget_range: [0%, 0%]
      action: "SLO violation"
      approval: "VP + CTO"
      requirements:
        - "Postmortem within 48h"
        - "Exec presentation"
        - "Action items with owners"
```

## SLO Review Cadence

### Weekly SLO Review

**Participants**: Engineering, Product, SRE

**Agenda**:
1. Current error budget status (all services)
2. Burn rate trends (increasing/decreasing?)
3. Recent incidents and impact on budget
4. Upcoming risky changes (deployments, migrations)
5. Action items from previous week

**Duration**: 30 minutes

### Quarterly SLO Adjustment

**Evaluate**:
- Are SLO targets too aggressive? (budget always depleted)
- Are SLO targets too relaxed? (budget never consumed)
- Are SLIs measuring the right thing?
- Should we add/remove services from SLO tracking?

**Outcome**: Adjust SLO targets, SLI definitions, or alert thresholds

## SLO Dashboard

### Grafana Dashboard

```json
{
  "title": "SLO & Error Budget Dashboard",
  "panels": [
    {
      "title": "SLO Status (30d)",
      "type": "stat",
      "targets": [{"expr": "http_request_success_rate_30d * 100"}],
      "thresholds": [
        {"value": 0, "color": "red"},
        {"value": 99.5, "color": "yellow"},
        {"value": 99.9, "color": "green"}
      ]
    },
    {
      "title": "Error Budget Remaining",
      "type": "gauge",
      "targets": [{"expr": "1 - ((1 - http_request_success_rate_30d) / (1 - 0.999))"}],
      "thresholds": [
        {"value": 0, "color": "red"},
        {"value": 0.25, "color": "yellow"},
        {"value": 0.5, "color": "green"}
      ]
    },
    {
      "title": "Burn Rate (Multi-Window)",
      "type": "graph",
      "targets": [
        {"expr": "(1 - http_request_success_rate_1h) / (1 - 0.999)", "legendFormat": "1h"},
        {"expr": "(1 - http_request_success_rate_6h) / (1 - 0.999)", "legendFormat": "6h"},
        {"expr": "(1 - http_request_success_rate_24h) / (1 - 0.999)", "legendFormat": "24h"}
      ]
    }
  ]
}
```

## Common Pitfalls

### Pitfall 1: Too Many SLOs

**Problem**: Tracking SLOs for every service dilutes focus.

**Solution**: Start with 3-5 critical services. Expand gradually.

### Pitfall 2: Unrealistic SLOs

**Problem**: 99.99% SLO (52 minutes downtime/year) is very expensive.

**Solution**: Set SLOs based on customer needs, not aspirational goals. 99.9% is often sufficient.

### Pitfall 3: Ignoring Error Budget

**Problem**: SLO defined but no error budget policy.

**Solution**: Create clear policy: what happens when budget is consumed?

### Pitfall 4: No SLI Validation

**Problem**: SLI doesn't reflect actual user experience.

**Solution**: Validate SLIs with Real User Monitoring (RUM). Do users experience outages when SLO violated?

### Pitfall 5: Alert Fatigue

**Problem**: Too many burn rate alerts (false positives).

**Solution**: Tune alert thresholds based on historical data. Use multi-window alerts.

## SLO Checklist

**Before implementing SLOs**:
- [ ] Identify 3-5 critical services
- [ ] Define SLIs (availability, latency, error rate)
- [ ] Set realistic SLO targets (99.5%, 99.9%, or 99.95%)
- [ ] Calculate error budgets (downtime allowed per month)
- [ ] Create error budget policy (feature freeze thresholds)
- [ ] Implement multi-window burn rate alerts
- [ ] Create SLO dashboard in Grafana
- [ ] Schedule weekly SLO review meetings
- [ ] Document postmortem process
- [ ] Get exec buy-in on error budget policy

## Related Documentation

- **Examples**: [SLO Framework](../examples/slo-error-budgets.md), [Prometheus + Grafana](../examples/prometheus-grafana-setup.md)
- **Reference**: [PromQL Guide](promql-guide.md), [Golden Signals](golden-signals.md)
- **Templates**: [SLO Definition](../templates/slo-definition.yaml)

---

Return to [reference index](INDEX.md)
