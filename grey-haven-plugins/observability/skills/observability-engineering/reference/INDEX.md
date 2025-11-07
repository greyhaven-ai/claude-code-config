# Observability Reference Documentation

Comprehensive reference guides for production observability patterns, PromQL queries, and SRE best practices.

## Reference Overview

### PromQL Query Language Guide

**File**: [promql-guide.md](promql-guide.md)

Complete PromQL reference for Prometheus queries:
- **Metric types**: Counter, Gauge, Histogram, Summary
- **PromQL functions**: rate(), irate(), increase(), sum(), avg(), histogram_quantile()
- **Recording rules**: Pre-aggregated metrics for performance
- **Alerting queries**: Burn rate calculations, threshold alerts
- **Performance tips**: Query optimization, avoiding cardinality explosions

**Use when**: Writing Prometheus queries, creating recording rules, debugging slow queries

---

### Golden Signals Reference

**File**: [golden-signals.md](golden-signals.md)

Google SRE Golden Signals implementation guide:
- **Request Rate (Traffic)**: RPS calculations, per-service breakdowns
- **Error Rate**: 5xx errors, client vs server errors, error budget impact
- **Latency (Duration)**: p50/p95/p99 percentiles, latency SLOs
- **Saturation**: CPU, memory, disk, connection pools

**Use when**: Designing monitoring dashboards, implementing SLIs, understanding system health

---

### SLO Best Practices

**File**: [slo-best-practices.md](slo-best-practices.md)

Google SRE SLO/SLI/Error Budget framework:
- **SLI selection**: Choosing meaningful indicators (availability, latency, throughput)
- **SLO targets**: Critical (99.95%), Essential (99.9%), Standard (99.5%)
- **Error budget policies**: Feature freeze thresholds, postmortem requirements
- **Multi-window burn rate alerts**: 1h, 6h, 24h windows
- **SLO review cadence**: Weekly reviews, quarterly adjustments

**Use when**: Implementing SLO framework, setting reliability targets, balancing velocity with reliability

---

## Quick Navigation

| Topic | File | Lines | Focus |
|-------|------|-------|-------|
| **PromQL** | [promql-guide.md](promql-guide.md) | ~450 | Query language reference |
| **Golden Signals** | [golden-signals.md](golden-signals.md) | ~380 | Four signals implementation |
| **SLO Practices** | [slo-best-practices.md](slo-best-practices.md) | ~420 | Google SRE framework |

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Production implementations
- **Templates**: [Templates Index](../templates/INDEX.md) - Copy-paste configurations
- **Main Agent**: [observability-engineer.md](../observability-engineer.md) - Observability agent

---

Return to [main agent](../observability-engineer.md)
