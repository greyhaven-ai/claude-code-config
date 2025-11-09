# Observability Templates

Copy-paste ready configuration templates for Prometheus, Grafana, and OpenTelemetry.

## Templates Overview

### Grafana Dashboard Template

**File**: [grafana-dashboard.json](grafana-dashboard.json)

Production-ready Golden Signals dashboard:
- **Request Rate**: Total RPS with 5-minute averages
- **Error Rate**: Percentage of 5xx errors with alert thresholds
- **Latency**: p50/p95/p99 percentiles in milliseconds
- **Saturation**: CPU and memory usage percentages

**Use when**: Creating new service dashboards, standardizing monitoring

---

### SLO Definition Template

**File**: [slo-definition.yaml](slo-definition.yaml)

Service Level Objective configuration:
- **SLO tiers**: Critical (99.95%), Essential (99.9%), Standard (99.5%)
- **SLI definitions**: Availability, latency, error rate
- **Error budget policy**: Feature freeze thresholds
- **Multi-window burn rate alerts**: 1h, 6h, 24h windows

**Use when**: Implementing SLO framework for new services

---

### Prometheus Recording Rules

**File**: [prometheus-recording-rules.yaml](prometheus-recording-rules.yaml)

Pre-aggregated metrics for fast dashboards:
- **Request rates**: Per-service, per-endpoint RPS
- **Error rates**: Percentage calculations (5xx / total)
- **Latency percentiles**: p50/p95/p99 pre-computed
- **Error budget**: Remaining budget and burn rate

**Use when**: Optimizing slow dashboard queries, implementing SLOs

---

## Quick Usage

```bash
# Copy template to your monitoring directory
cp templates/grafana-dashboard.json ../monitoring/dashboards/

# Edit service name and thresholds
vim ../monitoring/dashboards/grafana-dashboard.json

# Import to Grafana
curl -X POST http://admin:password@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @../monitoring/dashboards/grafana-dashboard.json
```

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Full implementations
- **Reference**: [Reference Index](../reference/INDEX.md) - PromQL, SLO guides
- **Main Agent**: [observability-engineer.md](../observability-engineer.md) - Observability agent

---

Return to [main agent](../observability-engineer.md)
