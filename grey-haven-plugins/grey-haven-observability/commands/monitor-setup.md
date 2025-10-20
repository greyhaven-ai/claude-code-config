---
name: monitor-setup
description: Set up comprehensive monitoring and observability infrastructure with Prometheus, Grafana, OpenTelemetry, and Fluentd. Configure metrics collection, distributed tracing, log aggregation, and alerting for production systems.
---

# Monitor Setup - Production Observability Infrastructure

Comprehensive monitoring and observability setup implementing the three pillars (metrics, logs, traces) with best practices for production systems.

## Overview

This command guides you through setting up a complete observability stack including:
- **Prometheus** for metrics collection and alerting
- **Grafana** for visualization and dashboards
- **OpenTelemetry** for distributed tracing
- **Fluentd** for log aggregation
- **AlertManager** for alert routing and escalation

## Prerequisites

- Kubernetes cluster (or Docker Compose for local development)
- Basic understanding of observability concepts
- Access to deploy infrastructure components
- (Optional) DataDog or Sentry accounts for SaaS integration

## Output Format

When implementing monitoring setup, provide:

1. **Infrastructure Assessment**
   - Current monitoring state
   - Identified gaps and risks
   - Service inventory with criticality

2. **Monitoring Architecture**
   - Component diagram (Mermaid)
   - Data flow and retention policies
   - Technology stack selections

3. **Implementation Plan**
   - Phased rollout strategy
   - Timeline and resource requirements
   - Risk mitigation approaches

4. **Metric Definitions**
   - Golden Signals (rate, errors, latency)
   - Custom business metrics
   - Resource utilization metrics

5. **Dashboard Templates**
   - Service overview dashboards
   - Infrastructure dashboards
   - Executive/business dashboards

6. **Alert Runbooks**
   - Alert rule definitions
   - Diagnostic procedures
   - Escalation policies

7. **SLO Definitions**
   - Service-level indicators
   - Target percentiles and thresholds
   - Error budget calculations

8. **Integration Guide**
   - CI/CD integration
   - Incident management tools
   - Documentation and training

## Technology Stack

### Option 1: Open Source Stack (Recommended for Cost Control)

```yaml
# Prometheus Stack
- Prometheus Server (metrics storage + querying)
- Prometheus Operator (Kubernetes-native deployment)
- node-exporter (host metrics)
- kube-state-metrics (Kubernetes metrics)
- AlertManager (alert routing)

# Visualization
- Grafana (dashboards + alerting)
- Grafana Loki (log aggregation)

# Tracing
- Jaeger (distributed tracing)
- OpenTelemetry Collector (telemetry pipeline)

# Logging
- Fluentd or Fluent Bit (log shipping)
- Elasticsearch (optional, log storage)
```

### Option 2: Hybrid Stack (SaaS + Open Source)

```yaml
# Metrics & APM
- DataDog (SaaS metrics + APM)
- Prometheus (supplemental, cost optimization)

# Error Tracking
- Sentry (application errors + performance)

# Logs
- DataDog Logs or ELK Stack

# Distributed Tracing
- DataDog APM or Jaeger
```

## Implementation Guide

### Phase 1: Prometheus Metrics Setup

#### 1.1 Deploy Prometheus Operator (Kubernetes)

```yaml
# prometheus-operator.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring

---
apiVersion: helm.sh/v1
kind: HelmRelease
metadata:
  name: kube-prometheus-stack
  namespace: monitoring
spec:
  chart:
    repository: https://prometheus-community.github.io/helm-charts
    name: kube-prometheus-stack
    version: 45.x.x
  values:
    prometheus:
      prometheusSpec:
        retention: 15d
        retentionSize: "50GB"
        storageSpec:
          volumeClaimTemplate:
            spec:
              accessModes: ["ReadWriteOnce"]
              resources:
                requests:
                  storage: 100Gi
        resources:
          requests:
            memory: 2Gi
            cpu: 1000m
          limits:
            memory: 4Gi
            cpu: 2000m
    
    grafana:
      adminPassword: <SET_SECURE_PASSWORD>
      persistence:
        enabled: true
        size: 10Gi
      
    alertmanager:
      config:
        route:
          group_by: ['alertname', 'cluster', 'service']
          group_wait: 10s
          group_interval: 10s
          repeat_interval: 12h
          receiver: 'slack-notifications'
        receivers:
        - name: 'slack-notifications'
          slack_configs:
          - api_url: <SLACK_WEBHOOK_URL>
            channel: '#alerts'
            title: 'Alert: {{ .GroupLabels.alertname }}'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

#### 1.2 Application Instrumentation (TypeScript/Node.js)

```typescript
// metrics.ts - Custom Prometheus Metrics
import { Registry, Counter, Histogram, Gauge } from 'prom-client';

// Create registry
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

// Active Connections
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
  registers: [register]
});

// Business Metrics
const checkoutCompletedTotal = new Counter({
  name: 'checkout_completed_total',
  help: 'Total number of completed checkouts',
  labelNames: ['payment_method', 'currency'],
  registers: [register]
});

// Express Middleware
export function metricsMiddleware(req, res, next) {
  const start = Date.now();
  
  // Track active connections
  activeConnections.inc();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || 'unknown';
    const labels = {
      method: req.method,
      route: route,
      status_code: res.statusCode
    };
    
    httpRequestsTotal.inc(labels);
    httpRequestDuration.observe(labels, duration);
    activeConnections.dec();
  });
  
  next();
}

// Metrics Endpoint
export function metricsHandler(req, res) {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
}
```

#### 1.3 Recording Rules (Prometheus)

```yaml
# prometheus-recording-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-recording-rules
  namespace: monitoring
spec:
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

#### 1.4 Alert Rules

```yaml
# prometheus-alert-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-alert-rules
  namespace: monitoring
spec:
  groups:
  - name: service_alerts
    rules:
    # High Error Rate
    - alert: HighErrorRate
      expr: service:error_rate:5m > 5
      for: 5m
      labels:
        severity: critical
        team: backend
      annotations:
        summary: "High error rate detected"
        description: "Service {{ $labels.service }} has error rate of {{ $value }}% (threshold: 5%)"
        runbook_url: "https://runbooks.example.com/high-error-rate"
    
    # Slow Response Time
    - alert: SlowResponseTime
      expr: service:latency_p95:5m > 1
      for: 10m
      labels:
        severity: warning
        team: backend
      annotations:
        summary: "Slow API response time"
        description: "Service {{ $labels.service }} p95 latency is {{ $value }}s (threshold: 1s)"
        runbook_url: "https://runbooks.example.com/slow-response"
    
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

### Phase 2: Grafana Dashboards

#### 2.1 Golden Signals Dashboard (JSON)

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
            "evaluator": { "type": "gt", "params": [5] },
            "query": { "params": ["A", "5m", "now"] }
          }]
        }
      },
      {
        "title": "Latency (p50, p95, p99)",
        "targets": [
          {
            "expr": "service:latency_p50:5m",
            "legendFormat": "p50"
          },
          {
            "expr": "service:latency_p95:5m",
            "legendFormat": "p95"
          },
          {
            "expr": "service:latency_p99:5m",
            "legendFormat": "p99"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

### Phase 3: OpenTelemetry Distributed Tracing

#### 3.1 OpenTelemetry Collector Configuration

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
    sampling_percentage: 10  # Sample 10% of traces

exporters:
  jaeger:
    endpoint: jaeger-collector:14250
    tls:
      insecure: true
  
  datadog:
    api:
      key: ${DD_API_KEY}
    hostname: ${HOSTNAME}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource, probabilistic_sampler]
      exporters: [jaeger, datadog]
```

#### 3.2 Application Tracing (TypeScript)

```typescript
// tracing.ts - OpenTelemetry Setup
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development'
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector:4318/v1/traces',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        enabled: true,
        ignoreIncomingPaths: ['/health', '/metrics']
      },
      '@opentelemetry/instrumentation-express': { enabled: true },
      '@opentelemetry/instrumentation-pg': { enabled: true },
      '@opentelemetry/instrumentation-redis': { enabled: true }
    })
  ]
});

sdk.start();

// Graceful shutdown
process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('Tracing terminated'))
    .catch((error) => console.log('Error terminating tracing', error));
});
```

### Phase 4: Log Aggregation with Fluentd

#### 4.1 Fluentd Configuration (Kubernetes)

```yaml
# fluentd-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluentd-config
          mountPath: /fluentd/etc/fluent.conf
          subPath: fluent.conf
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluentd-config
        configMap:
          name: fluentd-config
```

#### 4.2 Structured Logging (Python)

```python
# logging_config.py - Structured JSON Logging
import logging
import json
import traceback
from datetime import datetime
from opentelemetry import trace

class JSONFormatter(logging.Formatter):
    """Format logs as JSON with trace context"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'service': 'my-service',
            'version': '1.0.0',
            'environment': os.getenv('ENVIRONMENT', 'development')
        }
        
        # Add trace context if available
        span = trace.get_current_span()
        if span:
            span_context = span.get_span_context()
            log_data['trace_id'] = format(span_context.trace_id, '032x')
            log_data['span_id'] = format(span_context.span_id, '016x')
        
        # Add exception info
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'stacktrace': traceback.format_exception(*record.exc_info)
            }
        
        # Add custom fields
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        
        return json.dumps(log_data)

# Configure logger
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger
```

## Runbook Templates

### High Error Rate Runbook

```markdown
# Runbook: High Error Rate

**Alert:** HighErrorRate
**Severity:** Critical
**Threshold:** Error rate > 5% for 5 minutes

## Diagnostic Steps

1. Check Grafana dashboard for affected services
2. Query recent errors in logs:
   ```
   kubectl logs -l app=my-service --tail=100 | grep -i error
   ```
3. Check Jaeger for failed traces
4. Verify database connectivity and health
5. Check external API status (status pages)

## Common Causes

- Database connection pool exhaustion
- Third-party API failures
- Recent deployment introducing bugs
- Infrastructure issues (network, disk, memory)

## Remediation

1. **Immediate:** Rollback recent deployment if correlation exists
2. **Short-term:** Scale up service if resource constrained
3. **Investigation:** Analyze error logs and traces for root cause

## Escalation

- **After 15 minutes:** Page on-call engineer
- **After 30 minutes:** Escalate to senior engineer
- **After 1 hour:** Incident commander + engineering manager
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
  
  - name: checkout-success-rate
    service: checkout-service
    sli_type: success_rate
    target: 99.5
    window: 30d
    calculation: |
      (sum(checkout_completed_total) / sum(checkout_attempted_total)) * 100
```

## Cost Optimization Tips

1. **Metric Retention:** Use tiered storage (hot: 15d, cold: 90d+)
2. **Sampling:** Trace 10% of requests, 100% of errors
3. **Cardinality:** Limit label values, avoid user IDs in metrics
4. **Aggregation:** Use recording rules to pre-aggregate expensive queries
5. **Open Source:** Prefer Prometheus + Grafana over DataDog for cost savings (10-50x cheaper)

## Next Steps

After completing this monitoring setup:

1. Run `/slo-implement` to define service-level objectives
2. Implement chaos engineering experiments to validate observability
3. Create team-specific dashboards for different stakeholders
4. Set up automated reporting (daily/weekly summaries)
5. Train team on dashboard usage and alert response

## References

- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
