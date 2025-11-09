# Observability Examples

Production-ready observability implementations for Grey Haven stack (Cloudflare Workers, TanStack Start, FastAPI, PostgreSQL).

## Examples Overview

### Prometheus + Grafana Setup

**File**: [prometheus-grafana-setup.md](prometheus-grafana-setup.md)

Complete monitoring stack for Kubernetes with Golden Signals:
- **Prometheus Deployment** - Helm charts, service discovery, scrape configs
- **Grafana Setup** - Dashboard-as-code, templating, alerting
- **Node Exporter** - System metrics collection (CPU, memory, disk)
- **kube-state-metrics** - Kubernetes resource metrics
- **Golden Signals** - Request rate, error rate, latency (p50/p95/p99), saturation
- **Recording Rules** - Pre-aggregated metrics for fast queries
- **Alert Manager** - PagerDuty integration, escalation policies
- **Before/After Metrics** - Response time improved 40%, MTTR reduced 60%

**Use when**: Setting up production monitoring, implementing SRE practices, cloud-native deployments

---

### OpenTelemetry Distributed Tracing

**File**: [opentelemetry-tracing.md](opentelemetry-tracing.md)

Distributed tracing for microservices with Jaeger:
- **OTel Collector** - Receiver/processor/exporter pipelines
- **Auto-Instrumentation** - Zero-code tracing for Node.js, Python, FastAPI
- **Context Propagation** - W3C Trace Context across services
- **Sampling Strategies** - Head-based (10%), tail-based (errors only)
- **Span Attributes** - HTTP method, status code, user ID, tenant ID
- **Trace Visualization** - Jaeger UI, dependency graphs, critical path
- **Performance Impact** - <5ms overhead, 2% CPU increase
- **Before/After** - MTTR 45min → 8min (82% reduction)

**Use when**: Debugging microservices, understanding latency, optimizing critical paths

---

### SLO & Error Budget Framework

**File**: [slo-error-budgets.md](slo-error-budgets.md)

Complete SLI/SLO/Error Budget implementation:
- **SLI Definition** - Availability (99.9%), latency (p95 < 200ms), error rate (< 0.5%)
- **SLO Targets** - Critical (99.95%), Essential (99.9%), Standard (99.5%)
- **Error Budget Calculation** - Monthly budget, burn rate monitoring (1h/6h/24h windows)
- **Prometheus Recording Rules** - Multi-window SLI calculations
- **Grafana SLO Dashboard** - Real-time status, budget remaining, burn rate graphs
- **Budget Policies** - Feature freeze at 25% remaining, postmortem required at depletion
- **Burn Rate Alerts** - PagerDuty escalation when burning too fast
- **Impact** - 99.95% availability achieved, 3 feature freezes prevented overspend

**Use when**: Implementing SRE practices, balancing reliability with velocity, production deployments

---

### DataDog APM Integration

**File**: [datadog-apm.md](datadog-apm.md)

Application Performance Monitoring for Grey Haven stack:
- **DataDog Agent** - Cloudflare Workers instrumentation, FastAPI tracing
- **Custom Metrics** - Business KPIs (checkout success rate, revenue per minute)
- **Real User Monitoring (RUM)** - Frontend performance, user sessions, error tracking
- **APM Traces** - Distributed tracing with Cloudflare Workers, database queries
- **Log Correlation** - Trace ID in logs, unified troubleshooting
- **Synthetic Monitoring** - API health checks every 1 minute from 10 locations
- **Anomaly Detection** - ML-powered alerts for unusual patterns
- **Cost** - $31/host/month, $40/million spans
- **Before/After** - 99.5% → 99.95% availability (10x fewer incidents)

**Use when**: Commercial APM needed, executive dashboards required, startup budget allows

---

### Centralized Logging with Fluentd + Elasticsearch

**File**: [centralized-logging.md](centralized-logging.md)

Production log aggregation for multi-region deployments:
- **Fluentd DaemonSet** - Kubernetes log collection from all pods
- **Structured Logging** - JSON format with trace ID, user ID, tenant ID
- **Elasticsearch Indexing** - Daily indices with rollover, ILM policies
- **Kibana Dashboards** - Error tracking, request patterns, audit logs
- **Log Parsing** - Grok patterns for FastAPI, TanStack Start, PostgreSQL
- **Retention** - Hot (7 days), Warm (30 days), Cold (90 days), Archive (1 year)
- **PII Redaction** - Automatic SSN, credit card, email masking
- **Volume** - 500GB/day ingested, 90% compression, $800/month cost
- **Before/After** - Log search 5min → 10sec, disk usage 10TB → 1TB

**Use when**: Debugging production issues, compliance requirements (SOC2/PCI), audit trails

---

### Chaos Engineering with Gremlin

**File**: [chaos-engineering.md](chaos-engineering.md)

Reliability testing and circuit breaker validation:
- **Gremlin Setup** - Agent deployment, blast radius configuration
- **Chaos Experiments** - Pod termination, network latency (100ms), CPU stress (80%)
- **Circuit Breaker** - Automatic fallback when error rate > 50%
- **Hypothesis** - "API handles 50% pod failures without user impact"
- **Validation** - Prometheus metrics, distributed traces, user session monitoring
- **Results** - Circuit breaker engaged in 2sec, fallback success rate 99.8%
- **Runbook** - Automatic rollback triggers, escalation procedures
- **Impact** - Found 3 critical bugs before production, confidence in resilience

**Use when**: Pre-production validation, testing disaster recovery, chaos engineering practice

---

## Quick Navigation

| Topic | File | Lines | Focus |
|-------|------|-------|-------|
| **Prometheus + Grafana** | [prometheus-grafana-setup.md](prometheus-grafana-setup.md) | ~480 | Golden Signals monitoring |
| **OpenTelemetry** | [opentelemetry-tracing.md](opentelemetry-tracing.md) | ~450 | Distributed tracing |
| **SLO Framework** | [slo-error-budgets.md](slo-error-budgets.md) | ~420 | Error budget management |
| **DataDog APM** | [datadog-apm.md](datadog-apm.md) | ~400 | Commercial APM |
| **Centralized Logging** | [centralized-logging.md](centralized-logging.md) | ~440 | Log aggregation |
| **Chaos Engineering** | [chaos-engineering.md](chaos-engineering.md) | ~350 | Reliability testing |

## Related Documentation

- **Reference**: [Reference Index](../reference/INDEX.md) - PromQL, Golden Signals, SLO best practices
- **Templates**: [Templates Index](../templates/INDEX.md) - Grafana dashboards, SLO definitions
- **Main Agent**: [observability-engineer.md](../observability-engineer.md) - Observability agent

---

Return to [main agent](../observability-engineer.md)
