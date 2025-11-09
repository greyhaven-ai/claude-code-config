---
name: monitor-setup
description: Set up comprehensive monitoring and observability infrastructure with Prometheus, Grafana, OpenTelemetry, and structured logging. Configure metrics collection, distributed tracing, and alerting for production systems.
---

# Monitor Setup - Production Observability Infrastructure

Comprehensive monitoring and observability setup implementing the three pillars (metrics, logs, traces) with best practices for production systems.

## What This Command Does

Guides you through setting up complete observability infrastructure:
- **Prometheus** - Metrics collection, recording rules, and alerting
- **Grafana** - Visualization dashboards for Golden Signals
- **OpenTelemetry** - Distributed tracing across services
- **Structured Logging** - JSON-formatted logs with trace correlation
- **AlertManager** - Alert routing and escalation

## When to Use

- Setting up monitoring for new production services
- Implementing SRE observability best practices
- Replacing ad-hoc monitoring with structured approach
- Establishing baseline metrics before SLO implementation
- After deploying services to production

## Prerequisites

- Production service deployed (Cloudflare Workers, Kubernetes, or traditional infrastructure)
- Basic understanding of observability concepts (metrics, logs, traces)
- Access to deploy infrastructure components
- (Optional) Kubernetes cluster for Prometheus Operator

## Core Capabilities

### 1. Prometheus Metrics Setup

**Golden Signals** (The Four Key Metrics):
- **Rate** - Requests per second
- **Errors** - Error rate percentage
- **Duration** - Latency (p50, p95, p99)
- **Saturation** - Resource utilization (CPU, memory, connections)

**Application Instrumentation (TypeScript/Cloudflare Workers)**:
```typescript
// metrics.ts - Prometheus-style metrics for Cloudflare
import { Registry, Counter, Histogram } from 'prom-client';

const register = new Registry();

// HTTP Request Counter
const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

// HTTP Request Duration
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5],
  registers: [register]
});

// Business Metrics
const checkoutCompletedTotal = new Counter({
  name: 'checkout_completed_total',
  help: 'Total completed checkouts',
  labelNames: ['payment_method', 'currency'],
  registers: [register]
});

// Middleware for automatic tracking
export function metricsMiddleware(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const labels = {
      method: req.method,
      route: req.route?.path || 'unknown',
      status_code: res.statusCode
    };

    httpRequestsTotal.inc(labels);
    httpRequestDuration.observe(labels, duration);
  });

  next();
}

// Metrics endpoint
export function metricsHandler(req, res) {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
}
```

**Recording Rules** (Prometheus):
```yaml
# prometheus-recording-rules.yaml
groups:
  - name: service_metrics
    interval: 30s
    rules:
    # Request Rate (per second)
    - record: service:request_rate:5m
      expr: rate(http_requests_total[5m])

    # Success Rate (percentage)
    - record: service:success_rate:5m
      expr: |
        sum(rate(http_requests_total{status_code=~"2.."}[5m]))
        /
        sum(rate(http_requests_total[5m])) * 100

    # Error Rate (percentage)
    - record: service:error_rate:5m
      expr: |
        sum(rate(http_requests_total{status_code=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m])) * 100

    # Latency Percentiles
    - record: service:latency_p50:5m
      expr: histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))

    - record: service:latency_p95:5m
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

    - record: service:latency_p99:5m
      expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

### 2. Alert Rules Configuration

**Key Pattern** (Multi-Window Burn Rate Alerts):
```yaml
# prometheus-alert-rules.yaml
groups:
  - name: service_alerts
    rules:
    # High Error Rate (Critical)
    - alert: HighErrorRate
      expr: service:error_rate:5m > 5
      for: 5m
      labels:
        severity: critical
        team: backend
      annotations:
        summary: "High error rate detected"
        description: "Service {{ $labels.service }} has error rate of {{ $value }}% (threshold: 5%)"
        runbook_url: "https://runbooks.greyhaven.com/high-error-rate"

    # Slow Response Time (Warning)
    - alert: SlowResponseTime
      expr: service:latency_p95:5m > 1
      for: 10m
      labels:
        severity: warning
        team: backend
      annotations:
        summary: "Slow API response time"
        description: "Service {{ $labels.service }} p95 latency is {{ $value }}s (threshold: 1s)"
        runbook_url: "https://runbooks.greyhaven.com/slow-response"

    # High CPU Usage
    - alert: HighCPUUsage
      expr: rate(process_cpu_seconds_total[5m]) > 0.8
      for: 15m
      labels:
        severity: warning
        team: platform
      annotations:
        summary: "High CPU usage detected"
        description: "Pod {{ $labels.pod }} CPU usage is {{ $value | humanizePercentage }}"

    # High Memory Usage
    - alert: HighMemoryUsage
      expr: process_resident_memory_bytes / node_memory_MemTotal_bytes > 0.9
      for: 10m
      labels:
        severity: critical
        team: platform
      annotations:
        summary: "High memory usage detected"
        description: "Pod {{ $labels.pod }} memory usage is {{ $value | humanizePercentage }}"
```

### 3. Grafana Dashboards

**Golden Signals Dashboard Structure**:
```json
{
  "dashboard": {
    "title": "Service Golden Signals",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{
          "expr": "sum(rate(http_requests_total[5m])) by (service)",
          "legendFormat": "{{service}}"
        }],
        "type": "graph"
      },
      {
        "title": "Error Rate %",
        "targets": [{
          "expr": "service:error_rate:5m",
          "legendFormat": "{{service}}"
        }],
        "type": "graph",
        "alert": {
          "conditions": [{
            "evaluator": { "type": "gt", "params": [5] }
          }]
        }
      },
      {
        "title": "Latency (p50, p95, p99)",
        "targets": [
          { "expr": "service:latency_p50:5m", "legendFormat": "p50" },
          { "expr": "service:latency_p95:5m", "legendFormat": "p95" },
          { "expr": "service:latency_p99:5m", "legendFormat": "p99" }
        ],
        "type": "graph"
      }
    ]
  }
}
```

**Dashboard Categories**:
- **Golden Signals** - Rate, errors, duration, saturation
- **Service Overview** - Per-service health and performance
- **Infrastructure** - CPU, memory, disk, network
- **Business Metrics** - Checkouts, signups, revenue

### 4. OpenTelemetry Distributed Tracing

**OpenTelemetry Collector Configuration**:
```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024

  resource:
    attributes:
    - key: environment
      value: production
      action: upsert

  probabilistic_sampler:
    sampling_percentage: 10  # Sample 10% of traces, 100% of errors

exporters:
  jaeger:
    endpoint: jaeger-collector:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource, probabilistic_sampler]
      exporters: [jaeger]
```

**Application Tracing (TypeScript)**:
```typescript
// tracing.ts - OpenTelemetry Setup
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  resource: {
    'service.name': 'my-service',
    'service.version': '1.0.0',
    'deployment.environment': process.env.NODE_ENV || 'development'
  },
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector:4318/v1/traces',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingPaths: ['/health', '/metrics']
      }
    })
  ]
});

sdk.start();
```

### 5. Structured Logging

**JSON Logging with Trace Correlation (Python)**:
```python
# logging_config.py
import logging
import json
from datetime import datetime
from opentelemetry import trace

class JSONFormatter(logging.Formatter):
    """Format logs as JSON with trace context"""

    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'service': 'my-service',
            'environment': os.getenv('ENVIRONMENT', 'development')
        }

        # Add trace context
        span = trace.get_current_span()
        if span:
            span_context = span.get_span_context()
            log_data['trace_id'] = format(span_context.trace_id, '032x')
            log_data['span_id'] = format(span_context.span_id, '016x')

        # Add exception info
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1])
            }

        return json.dumps(log_data)
```

### 6. Alert Runbook Template

**Runbook Example** (High Error Rate):
```markdown
# Runbook: High Error Rate

**Alert:** HighErrorRate
**Severity:** Critical
**Threshold:** Error rate > 5% for 5 minutes

## Diagnostic Steps

1. Check Grafana dashboard for affected services
2. Query recent errors: `kubectl logs -l app=my-service --tail=100 | grep -i error`
3. Check Jaeger for failed traces
4. Verify database connectivity
5. Check external API status

## Common Causes

- Database connection pool exhaustion
- Third-party API failures
- Recent deployment introducing bugs
- Infrastructure issues (network, disk, memory)

## Remediation

1. **Immediate:** Rollback recent deployment if correlated
2. **Short-term:** Scale up if resource constrained
3. **Investigation:** Analyze logs and traces for root cause

## Escalation

- After 15 min: Page on-call engineer
- After 30 min: Escalate to senior engineer
- After 1 hour: Incident commander + engineering manager
```

## Technology Stack Options

### Option 1: Open Source Stack (Recommended)
```yaml
Metrics & Alerting:
  - Prometheus (metrics storage + querying)
  - Grafana (dashboards)
  - AlertManager (alert routing)

Tracing:
  - Jaeger (distributed tracing)
  - OpenTelemetry Collector

Logging:
  - Structured JSON logs to stdout
  - Fluentd/Fluent Bit (log shipping)
```

### Option 2: Cloudflare-Native Stack
```yaml
Metrics:
  - Cloudflare Workers Analytics
  - Custom Analytics Engine

Logging:
  - Console logging (JSON.stringify)
  - Wrangler tail for real-time logs

Tracing:
  - OpenTelemetry with custom exporter
```

## SLO Definitions

```yaml
# slo-definitions.yaml
slos:
  - name: api-availability
    service: api-gateway
    sli_type: availability
    target: 99.9
    window: 30d
    calculation: |
      (sum(http_requests_total{status_code!~"5.."}) / sum(http_requests_total)) * 100

  - name: api-latency
    service: api-gateway
    sli_type: latency
    target_percentile: 95
    target_value: 500ms
    window: 30d
    calculation: |
      histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

## Cost Optimization

1. **Metric Retention** - Hot: 15d, Cold: 90d+
2. **Trace Sampling** - 10% of requests, 100% of errors
3. **Cardinality Control** - Limit label values, avoid high-cardinality IDs
4. **Recording Rules** - Pre-aggregate expensive queries
5. **Open Source** - Prometheus + Grafana is 10-50x cheaper than DataDog

## Best Practices

1. **Start with Golden Signals** - Rate, errors, duration, saturation
2. **Alert on Symptoms, Not Causes** - User-facing issues, not server metrics
3. **Multi-Window Burn Rates** - Fast (1h) and slow (6h) burn alerts
4. **Runbooks for Every Alert** - Document diagnostic steps
5. **Test Alerts** - Verify alert routing and escalation

## Next Steps

After completing monitoring setup:

1. Run `/slo-implement` to define service-level objectives
2. Implement chaos engineering to validate observability
3. Create team-specific dashboards
4. Set up automated reporting (daily/weekly summaries)
5. Train team on dashboard usage and alert response

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete monitoring examples
  - [prometheus-setup-example.md](examples/prometheus-setup-example.md) - Full Prometheus deployment
  - [grafana-dashboard-example.md](examples/grafana-dashboard-example.md) - Complete dashboard JSON
  - [otel-tracing-example.md](examples/otel-tracing-example.md) - OpenTelemetry tracing setup
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Configuration references
  - [prometheus-operators.md](reference/prometheus-operators.md) - PromQL operators and functions
  - [alertmanager-routing.md](reference/alertmanager-routing.md) - Alert routing patterns
  - [grafana-variables.md](reference/grafana-variables.md) - Dashboard variables and templating
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [recording-rules-template.yaml](templates/recording-rules-template.yaml) - Recording rules template
  - [alert-rules-template.yaml](templates/alert-rules-template.yaml) - Alert rules template
  - [dashboard-template.json](templates/dashboard-template.json) - Grafana dashboard template

- **[checklists/](checklists/)** - Monitoring setup checklists
  - [monitoring-setup-checklist.md](checklists/monitoring-setup-checklist.md) - Complete setup checklist

## References

- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
