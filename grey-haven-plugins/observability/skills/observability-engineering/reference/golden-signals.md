# Golden Signals Reference

Google SRE Golden Signals implementation guide for Grey Haven microservices: Request Rate, Error Rate, Latency, and Saturation.

## Overview

**The Four Golden Signals** (from Google SRE Workbook):

1. **Traffic (Request Rate)** - How much demand is being placed on your system
2. **Errors (Error Rate)** - Rate of requests that fail
3. **Latency (Duration)** - Time it takes to service a request
4. **Saturation** - How "full" your service is (CPU, memory, disk, connections)

**Why Golden Signals?**
- Focus on what matters most to users
- Detect issues before they become outages
- Consistent monitoring across all services
- SLO-driven (availability, latency, error rate)

## 1. Traffic (Request Rate)

### Definition

**What**: Number of requests per second (RPS) your system is handling.

**Why measure**: Understand load patterns, capacity planning, detect traffic anomalies.

### Implementation

**Prometheus Counter**:
```python
# Python (FastAPI)
from prometheus_client import Counter

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    return response
```

**PromQL Queries**:
```promql
# Total request rate (RPS)
sum(rate(http_requests_total[5m]))

# Request rate by service
sum(rate(http_requests_total[5m])) by (service)

# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Request rate by HTTP method
sum(rate(http_requests_total[5m])) by (method)
```

**Alert Thresholds**:
- **Sudden drop**: RPS drops >50% in 5 minutes (possible outage)
- **Sudden spike**: RPS increases >200% in 5 minutes (DDoS or traffic spike)

```promql
# Alert: Traffic drop >50%
(
  sum(rate(http_requests_total[5m]))
  /
  sum(rate(http_requests_total[5m] offset 10m))
) < 0.5
```

## 2. Errors (Error Rate)

### Definition

**What**: Percentage of requests that fail (5xx errors, exceptions, timeouts).

**Why measure**: Direct measure of service health, SLO tracking, user-facing impact.

### Implementation

**Error Types**:
- **HTTP 5xx**: Server errors (500, 502, 503, 504)
- **HTTP 4xx**: Client errors (400, 401, 403, 404) - usually not counted as errors for SLO
- **Exceptions**: Unhandled exceptions (Python, TypeScript)
- **Timeouts**: Requests exceeding timeout threshold

**Prometheus Metric** (Counter):
```typescript
// TypeScript (TanStack Start)
import { Counter } from 'prom-client';

const httpErrorsTotal = new Counter({
  name: 'http_errors_total',
  help: 'Total HTTP errors',
  labelNames: ['service', 'status', 'error_type']
});

app.use(async (req, res, next) => {
  try {
    await next();
  } catch (error) {
    httpErrorsTotal.inc({
      service: 'tanstack-frontend',
      status: '500',
      error_type: error.constructor.name
    });
    throw error;
  }
});
```

**PromQL Queries**:
```promql
# Error rate (percentage)
(
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
) * 100

# Error rate by service
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
/
sum(rate(http_requests_total[5m])) by (service)

# Error count (absolute)
sum(rate(http_errors_total[5m]))
```

**Alert Thresholds**:
- **Critical**: Error rate >1% for 5 minutes
- **Warning**: Error rate >0.5% for 10 minutes

```promql
# Alert: High error rate
(
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
) > 0.01  # 1%
```

## 3. Latency (Duration)

### Definition

**What**: Time taken to service a request (response time).

**Why measure**: User experience, SLO compliance, performance regression detection.

### Percentiles

**Why percentiles?** Average latency hides outliers. Use p50, p95, p99 instead.

- **p50 (Median)**: 50% of requests faster than this
- **p95**: 95% of requests faster than this (common SLO target)
- **p99**: 99% of requests faster than this (tail latency)

**Example**:
```
p50: 100ms  ← Half of users see <100ms
p95: 200ms  ← 95% of users see <200ms
p99: 500ms  ← 1% of users see >500ms (tail latency)
```

### Implementation

**Prometheus Histogram**:
```python
# Python (FastAPI)
from prometheus_client import Histogram
import time

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]  # 10ms to 5s
)

@app.middleware("http")
async def measure_latency(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response
```

**PromQL Queries**:
```promql
# p95 latency (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# p99 latency (99th percentile)
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# p50 latency (median)
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))

# Average latency
rate(http_request_duration_seconds_sum[5m])
/
rate(http_request_duration_seconds_count[5m])

# Latency by endpoint (p95)
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
)
```

**Alert Thresholds**:
- **Critical**: p95 > 500ms for 5 minutes
- **Warning**: p95 > 200ms for 10 minutes

```promql
# Alert: High latency (p95)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
```

## 4. Saturation

### Definition

**What**: How "full" your service is (utilization of constrained resources).

**Why measure**: Prevent resource exhaustion, capacity planning, autoscaling triggers.

### Resource Types

**CPU Saturation**:
```promql
# CPU usage percentage
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# CPU saturation by pod
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)
/
sum(container_spec_cpu_quota / container_spec_cpu_period) by (pod)
```

**Memory Saturation**:
```promql
# Memory usage percentage
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Memory by pod
container_memory_usage_bytes{pod=~"fastapi.*"} / container_spec_memory_limit_bytes
```

**Disk Saturation**:
```promql
# Disk usage percentage
100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100

# Disk I/O wait
rate(node_disk_io_time_seconds_total[5m])
```

**Connection Pool Saturation**:
```python
# PostgreSQL connection pool
from prometheus_client import Gauge

db_pool_connections_active = Gauge(
    'db_pool_connections_active',
    'Active database connections'
)

db_pool_connections_max = Gauge(
    'db_pool_connections_max',
    'Maximum database connections'
)

# Update metrics
db_pool_connections_active.set(pool.size)
db_pool_connections_max.set(pool.maxsize)
```

```promql
# Connection pool saturation
db_pool_connections_active / db_pool_connections_max

# Alert if >80% saturated
(db_pool_connections_active / db_pool_connections_max) > 0.8
```

**Queue Depth Saturation**:
```promql
# Queue depth (e.g., Redis)
redis_queue_length

# Alert if queue backing up
redis_queue_length > 1000
```

**Alert Thresholds**:
- **Critical**: CPU >90%, Memory >90%, Disk >90%
- **Warning**: CPU >80%, Memory >85%, Disk >85%

## Golden Signals Dashboard

### Grafana Dashboard (JSON)

```json
{
  "dashboard": {
    "title": "Golden Signals - Grey Haven",
    "panels": [
      {
        "id": 1,
        "title": "Traffic (Request Rate)",
        "type": "graph",
        "targets": [{"expr": "sum(rate(http_requests_total[5m]))"}]
      },
      {
        "id": 2,
        "title": "Errors (Error Rate %)",
        "type": "graph",
        "targets": [{"expr": "(sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))) * 100"}],
        "alert": {"threshold": 1.0}
      },
      {
        "id": 3,
        "title": "Latency (p50/p95/p99)",
        "type": "graph",
        "targets": [
          {"expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))", "legendFormat": "p50"},
          {"expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))", "legendFormat": "p95"},
          {"expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))", "legendFormat": "p99"}
        ]
      },
      {
        "id": 4,
        "title": "Saturation (CPU/Memory %)",
        "type": "graph",
        "targets": [
          {"expr": "100 - (avg(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)", "legendFormat": "CPU"},
          {"expr": "100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))", "legendFormat": "Memory"}
        ]
      }
    ]
  }
}
```

## Golden Signals Checklist

**For each service, ensure**:
- [ ] **Traffic**: Request rate tracked (`http_requests_total` counter)
- [ ] **Errors**: Error rate tracked (5xx status codes, exceptions)
- [ ] **Latency**: p50/p95/p99 tracked (`http_request_duration_seconds` histogram)
- [ ] **Saturation**: CPU, memory, connection pools tracked
- [ ] **Alerts**: Critical thresholds defined for each signal
- [ ] **Dashboard**: Golden Signals dashboard created in Grafana
- [ ] **SLO**: SLOs defined based on error rate and latency

## Related Documentation

- **Examples**: [Prometheus + Grafana](../examples/prometheus-grafana-setup.md)
- **Reference**: [PromQL Guide](promql-guide.md), [SLO Best Practices](slo-best-practices.md)
- **Templates**: [Grafana Dashboard](../templates/grafana-dashboard.json)

---

Return to [reference index](INDEX.md)
