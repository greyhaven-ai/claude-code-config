# Monitoring Setup Examples

Complete examples demonstrating production monitoring infrastructure setup with Prometheus, Grafana, OpenTelemetry, and structured logging.

## Available Examples

### [prometheus-setup-example.md](prometheus-setup-example.md)
Complete Prometheus setup with Kubernetes Operator.
- Prometheus Operator Helm deployment
- ServiceMonitor and PodMonitor configurations
- Recording rules for Golden Signals
- Alert rules with multi-window burn rates
- Persistent storage configuration
- Resource limits and requests
- High availability setup (2+ replicas)

### [grafana-dashboard-example.md](grafana-dashboard-example.md)
Complete Grafana dashboard JSON examples.
- Golden Signals dashboard (rate, errors, duration, saturation)
- Service overview dashboard per-service metrics
- Infrastructure dashboard (CPU, memory, disk, network)
- Business metrics dashboard (checkouts, signups, revenue)
- Alert panel configuration
- Dashboard variables and templating
- Time range controls

### [otel-tracing-example.md](otel-tracing-example.md)
OpenTelemetry distributed tracing setup.
- OpenTelemetry Collector deployment (Kubernetes DaemonSet)
- Receiver configuration (OTLP gRPC and HTTP)
- Processor configuration (batch, resource, sampling)
- Exporter configuration (Jaeger, DataDog, Zipkin)
- Auto-instrumentation for TypeScript/Node.js
- Manual span creation and attributes
- Context propagation across services
- Trace sampling strategies (head-based, tail-based)

### [alertmanager-config-example.md](alertmanager-config-example.md)
AlertManager routing and escalation configuration.
- Route hierarchy and matchers
- Receiver configuration (Slack, PagerDuty, email)
- Inhibition rules (prevent alert storms)
- Grouping and deduplication
- Time-based routing (business hours vs. off-hours)
- Escalation policies
- Silences and maintenance windows

## Quick Reference

**Need Prometheus setup?** → [prometheus-setup-example.md](prometheus-setup-example.md)
**Need Grafana dashboards?** → [grafana-dashboard-example.md](grafana-dashboard-example.md)
**Need tracing setup?** → [otel-tracing-example.md](otel-tracing-example.md)
**Need AlertManager config?** → [alertmanager-config-example.md](alertmanager-config-example.md)
