# Prometheus + Grafana Monitoring Setup

Production-ready monitoring stack for Grey Haven applications with Golden Signals, recording rules, and PagerDuty alerting.

## Overview

**Before Implementation**:
- No visibility into production performance
- Mean Time to Resolution (MTTR): 45 minutes
- Incident detection: User reports only
- No SLO tracking

**After Implementation**:
- Golden Signals monitoring (request rate, errors, latency, saturation)
- MTTR: 18 minutes (60% reduction)
- Incident detection: Automated alerts (2-5 minute detection)
- 99.9% availability SLO tracking

**Technologies**: Prometheus, Grafana, kube-state-metrics, Node Exporter, Alert Manager, PagerDuty

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Grafana (Port 3000)                  │
│              Dashboards, Alerts, Annotations            │
└────────────────────┬────────────────────────────────────┘
                     │ PromQL Queries
┌────────────────────▼────────────────────────────────────┐
│              Prometheus (Port 9090)                     │
│    TSDB, Recording Rules, Alert Rules, Targets         │
└─┬──────────────┬─────────────────┬─────────────────────┘
  │              │                 │
  │ Scrape       │ Scrape          │ Scrape
  │ :9100        │ :8080           │ :8081
  ▼              ▼                 ▼
┌──────────┐  ┌──────────────┐  ┌───────────────────────┐
│   Node   │  │ kube-state-  │  │  Application Metrics  │
│ Exporter │  │   metrics    │  │   (Cloudflare, API)   │
└──────────┘  └──────────────┘  └───────────────────────┘
```

## 1. Prometheus Deployment (Helm)

### Install Prometheus with Helm

```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Create namespace
kubectl create namespace monitoring

# Install Prometheus stack (includes Grafana, Alert Manager, exporters)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=100Gi \
  --set grafana.adminPassword=changeme
```

### Custom values.yaml for Grey Haven

```yaml
# values.yaml - Key settings (30d retention, 100GB storage, PagerDuty alerts)
prometheus:
  prometheusSpec:
    retention: 30d
    scrapeInterval: 15s
    storageSpec:
      volumeClaimTemplate:
        spec:
          resources:
            requests:
              storage: 100Gi
    additionalScrapeConfigs:
      - job_name: 'cloudflare-workers'
        static_configs:
          - targets: ['api.greyhaven.io:443']
        metrics_path: /metrics
        scheme: https

grafana:
  adminPassword: "changeme"
  persistence: {enabled: true, size: 10Gi}

alertmanager:
  config:
    route:
      receiver: 'pagerduty'
    receivers:
      - name: 'pagerduty'
        pagerduty_configs:
          - service_key: 'YOUR_PAGERDUTY_KEY'
```

## 2. Golden Signals Implementation

### Request Rate (Traffic)

```yaml
# prometheus-recording-rules.yaml
groups:
  - name: golden_signals_request_rate
    interval: 15s
    rules:
      # Total request rate across all services
      - record: greyhaven:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m]))

      # Per-service request rate
      - record: greyhaven:http_requests:rate5m:by_service
        expr: sum(rate(http_requests_total[5m])) by (service, method, status)

      # Requests per second (RPS)
      - record: greyhaven:http_rps
        expr: sum(rate(http_requests_total[1m]))
```

**Grafana Dashboard Panel** (Request Rate):
```json
{
  "title": "Request Rate (RPS)",
  "targets": [{
    "expr": "greyhaven:http_rps",
    "legendFormat": "Requests/sec"
  }],
  "yaxes": [{"format": "reqps"}]
}
```

### Error Rate

```yaml
# Recording rule for error rate
- record: greyhaven:http_errors:rate5m
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m]))

# Error rate by service
- record: greyhaven:http_errors:rate5m:by_service
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
    /
    sum(rate(http_requests_total[5m])) by (service)
```

**Grafana Dashboard Panel** (Error Rate):
```json
{
  "title": "Error Rate (%)",
  "targets": [{
    "expr": "greyhaven:http_errors:rate5m * 100",
    "legendFormat": "Error %"
  }],
  "yaxes": [{"format": "percent"}],
  "alert": {
    "conditions": [{
      "evaluator": {"params": [1], "type": "gt"},
      "operator": {"type": "and"},
      "query": {"params": ["A", "5m", "now"]},
      "type": "query"
    }]
  }
}
```

### Latency (Duration)

```yaml
# Latency recording rules (p50, p95, p99)
- record: greyhaven:http_request_duration:p50
  expr: histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

- record: greyhaven:http_request_duration:p95
  expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

- record: greyhaven:http_request_duration:p99
  expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# Average latency
- record: greyhaven:http_request_duration:avg
  expr: sum(rate(http_request_duration_seconds_sum[5m])) / sum(rate(http_request_duration_seconds_count[5m]))
```

**Grafana Dashboard Panel** (Latency Percentiles):
```json
{
  "title": "Request Latency (ms)",
  "targets": [
    {"expr": "greyhaven:http_request_duration:p50 * 1000", "legendFormat": "p50"},
    {"expr": "greyhaven:http_request_duration:p95 * 1000", "legendFormat": "p95"},
    {"expr": "greyhaven:http_request_duration:p99 * 1000", "legendFormat": "p99"}
  ],
  "yaxes": [{"format": "ms"}],
  "thresholds": [
    {"value": 200, "colorMode": "critical", "op": "gt"}
  ]
}
```

### Saturation (Resource Usage)

```yaml
# CPU saturation (Node Exporter)
- record: greyhaven:cpu_usage:percent
  expr: 100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory saturation
- record: greyhaven:memory_usage:percent
  expr: |
    100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Database connection pool saturation
- record: greyhaven:db_pool:saturation
  expr: |
    db_pool_connections_active / db_pool_connections_max
```

## 3. Application Instrumentation

### TypeScript (TanStack Start + Cloudflare Workers)

```typescript
// middleware/metrics.ts
import { Histogram, Counter, Gauge } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]  // 10ms to 5s
});

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status']
});

const activeConnections = new Gauge({
  name: 'http_active_connections',
  help: 'Number of active HTTP connections'
});

export function metricsMiddleware() {
  return async (request: Request, next: () => Promise<Response>) => {
    const start = Date.now();
    activeConnections.inc();

    try {
      const response = await next();
      const duration = (Date.now() - start) / 1000;

      httpRequestDuration.observe({
        method: request.method,
        route: new URL(request.url).pathname,
        status: response.status.toString()
      }, duration);

      httpRequestsTotal.inc({
        method: request.method,
        route: new URL(request.url).pathname,
        status: response.status.toString()
      });

      return response;
    } finally {
      activeConnections.dec();
    }
  };
}

// Metrics endpoint for Prometheus scraping
export async function GET() {
  const { register } = await import('prom-client');
  return new Response(await register.metrics(), {
    headers: { 'Content-Type': register.contentType }
  });
}
```

### Python (FastAPI Backend)

```python
# middleware/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request
import time

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

db_pool_connections = Gauge(
    'db_pool_connections_active',
    'Active database connections'
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 4. Alert Rules

```yaml
# prometheus-alerts.yaml
groups:
  - name: golden_signals_alerts
    rules:
      # High error rate alert
      - alert: HighErrorRate
        expr: greyhaven:http_errors:rate5m > 0.01  # 1% error rate
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected ({{ $value | humanizePercentage }})"
          description: "Error rate is {{ $value | humanizePercentage }} for 5 minutes"

      # High latency alert (p95 > 500ms)
      - alert: HighLatencyP95
        expr: greyhaven:http_request_duration:p95 > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p95 latency ({{ $value | humanizeDuration }})"

      # Critical latency alert (p99 > 1s)
      - alert: CriticalLatencyP99
        expr: greyhaven:http_request_duration:p99 > 1.0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Critical p99 latency ({{ $value | humanizeDuration }})"

      # CPU saturation
      - alert: HighCPUUsage
        expr: greyhaven:cpu_usage:percent > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage ({{ $value }}%)"

      # Memory saturation
      - alert: HighMemoryUsage
        expr: greyhaven:memory_usage:percent > 85
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage ({{ $value }}%)"
```

## 5. Grafana Dashboard as Code

```json
{
  "dashboard": {
    "title": "Grey Haven Golden Signals",
    "tags": ["golden-signals", "production"],
    "panels": [
      {"id": 1, "title": "Request Rate (RPS)", "type": "graph", "targets": [{"expr": "greyhaven:http_rps"}], "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}},
      {"id": 2, "title": "Error Rate (%)", "type": "graph", "targets": [{"expr": "greyhaven:http_errors:rate5m * 100"}], "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}, "alert": {"conditions": [{"evaluator": {"params": [1], "type": "gt"}}]}},
      {"id": 3, "title": "Request Latency", "type": "graph", "targets": [{"expr": "greyhaven:http_request_duration:p50 * 1000", "legendFormat": "p50"}, {"expr": "greyhaven:http_request_duration:p95 * 1000", "legendFormat": "p95"}, {"expr": "greyhaven:http_request_duration:p99 * 1000", "legendFormat": "p99"}], "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}},
      {"id": 4, "title": "Resource Saturation", "type": "graph", "targets": [{"expr": "greyhaven:cpu_usage:percent", "legendFormat": "CPU %"}, {"expr": "greyhaven:memory_usage:percent", "legendFormat": "Memory %"}], "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}}
    ]
  }
}
```

**Deploy**: `curl -X POST http://admin:changeme@localhost:3000/api/dashboards/db -H "Content-Type: application/json" -d @grafana-golden-signals.json`

## 6. Results and Impact

### Before vs After Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **MTTR** | 45 min | 18 min | **60% reduction** |
| **Incident Detection** | User reports | 2-5 min (automated) | **90% faster** |
| **P95 Latency Visibility** | None | Real-time | **100% coverage** |
| **Error Rate Tracking** | Manual logs | Automated alerts | **Real-time** |
| **Availability** | Unknown | 99.9% tracked | **SLO compliance** |
| **Alert False Positives** | N/A | <5% | **High precision** |

### Key Improvements

**1. Response Time Optimization** (40% improvement)
- Identified N+1 database queries via latency spikes in p95
- Fixed: Reduced p95 from 350ms → 210ms

**2. Error Detection** (82% faster resolution)
- Alert fired 2 minutes after error rate spike (previously 45 min via user reports)
- Root cause identified via correlated metrics (CPU + error rate)

**3. Capacity Planning**
- Identified memory saturation at 85% during peak hours
- Scaled horizontally: 3 → 5 pods, saturation dropped to 60%

## Related Documentation

- **OpenTelemetry**: [opentelemetry-tracing.md](opentelemetry-tracing.md) - Distributed tracing
- **SLO Framework**: [slo-error-budgets.md](slo-error-budgets.md) - Error budget tracking
- **Reference**: [../reference/promql-guide.md](../reference/promql-guide.md) - PromQL queries
- **Templates**: [../templates/grafana-dashboard.json](../templates/grafana-dashboard.json) - Dashboard template

---

Return to [examples index](INDEX.md)
