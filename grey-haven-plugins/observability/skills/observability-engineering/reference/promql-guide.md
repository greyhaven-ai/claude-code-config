# PromQL Query Language Guide

Comprehensive reference for Prometheus Query Language (PromQL) with Grey Haven production patterns.

## Metric Types

### Counter (Always Increasing)

```promql
# Metric type: counter - Monotonically increasing value
http_requests_total{service="fastapi-backend"}

# WRONG: Don't query counters directly (value resets on restart)
http_requests_total

# RIGHT: Use rate() or increase()
rate(http_requests_total[5m])  # Per-second rate over 5 minutes
```

**Use for**: Request counts, error counts, bytes sent/received

### Gauge (Can Go Up or Down)

```promql
# Metric type: gauge - Current value (can increase or decrease)
memory_usage_bytes{instance="pod-123"}

# Use directly without rate()
memory_usage_bytes > 1000000000  # Alert if > 1GB
```

**Use for**: Memory usage, CPU usage, connection pool size, queue depth

### Histogram (Bucketed Observations)

```promql
# Metric type: histogram - Observations distributed across buckets
http_request_duration_seconds_bucket{le="0.5"}  # Requests ≤ 500ms

# Calculate percentiles
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))  # p95
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))  # p99

# Average duration
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

**Use for**: Request durations, response sizes

### Summary (Pre-calculated Percentiles)

```promql
# Metric type: summary - Pre-calculated quantiles (client-side)
http_request_duration_seconds{quantile="0.95"}  # p95 (calculated by client)

# Use directly (already calculated)
http_request_duration_seconds{quantile="0.95"} > 1  # Alert if p95 > 1s
```

**Use for**: Latency metrics where histogram overhead too high

## Core Functions

### rate() - Per-Second Rate

```promql
# Calculate per-second rate over time window
rate(http_requests_total[5m])

# Example: Requests per second for last 5 minutes
rate(http_requests_total{service="fastapi-backend"}[5m])

# Result: 45.2 (45.2 requests/second)
```

**Best practices**:
- Use `[5m]` for real-time dashboards
- Use `[1h]` for trending analysis
- Never use `[1m]` or less (unstable results)

### irate() - Instantaneous Rate

```promql
# Last two data points only (more sensitive to spikes)
irate(http_requests_total[5m])

# Use for: Detecting sudden traffic spikes
# Don't use for: Alerting (too sensitive to noise)
```

### increase() - Total Increase

```promql
# Total increase over time window
increase(http_requests_total[1h])

# Example: Total requests in last hour
increase(http_requests_total{service="fastapi-backend"}[1h])

# Result: 162,000 (162k total requests)
```

### sum() - Sum Across Series

```promql
# Sum all series
sum(http_requests_total)

# Sum by label (group by)
sum(rate(http_requests_total[5m])) by (service)

# Result:
# {service="fastapi-backend"} 45.2
# {service="tanstack-frontend"} 120.5
```

### avg() - Average Across Series

```promql
# Average memory usage across all pods
avg(memory_usage_bytes)

# Average by service
avg(memory_usage_bytes) by (service)
```

### max() / min() - Maximum / Minimum

```promql
# Maximum CPU usage across all pods
max(cpu_usage_percent)

# Minimum available memory
min(memory_available_bytes) by (node)
```

### histogram_quantile() - Calculate Percentiles

```promql
# p95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# p99 latency by service
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)
```

## Operators

### Arithmetic Operators

```promql
# Addition
http_requests_total + 100

# Subtraction
memory_total_bytes - memory_used_bytes

# Multiplication
cpu_usage_percent * 100

# Division (percentage calculation)
(http_requests_total{status="500"} / http_requests_total) * 100

# Modulo
http_requests_total % 1000
```

### Comparison Operators

```promql
# Greater than
memory_usage_bytes > 1000000000  # > 1GB

# Less than
http_request_duration_seconds < 0.1  # < 100ms

# Equal
http_requests_total{status="200"} == 1000

# Not equal
http_requests_total{status!="200"}

# Greater than or equal
cpu_usage_percent >= 80

# Less than or equal
error_rate <= 0.01
```

### Logical Operators

```promql
# AND
memory_usage_bytes > 1000000000 and cpu_usage_percent > 80

# OR
http_requests_total{status="500"} or http_requests_total{status="503"}

# UNLESS (exclude)
http_requests_total unless http_requests_total{status="200"}
```

## Label Matching

### Exact Match (=)

```promql
# Single label
http_requests_total{service="fastapi-backend"}

# Multiple labels (AND)
http_requests_total{service="fastapi-backend", method="POST", status="200"}
```

### Negative Match (!=)

```promql
# Exclude label value
http_requests_total{status!="200"}

# Exclude multiple
http_requests_total{status!="200", status!="201"}
```

### Regex Match (=~)

```promql
# Regex: Match 5xx status codes
http_requests_total{status=~"5.."}

# Regex: Match multiple services
http_requests_total{service=~"fastapi.*|tanstack.*"}

# Regex: Match endpoints
http_requests_total{path=~"/api/orders/.*"}
```

### Negative Regex (!~)

```promql
# Exclude health check endpoints
http_requests_total{path!~"/health|/metrics"}

# Exclude test environments
http_requests_total{environment!~"test.*|dev.*"}
```

## Aggregation

### by (Group By)

```promql
# Group by service
sum(rate(http_requests_total[5m])) by (service)

# Group by multiple labels
sum(rate(http_requests_total[5m])) by (service, status)

# Result:
# {service="fastapi", status="200"} 45.2
# {service="fastapi", status="500"} 0.5
```

### without (Exclude Labels)

```promql
# Remove instance label (aggregate across all instances)
sum(rate(http_requests_total[5m])) without (instance)

# Remove multiple labels
sum(rate(http_requests_total[5m])) without (instance, pod, node)
```

## Recording Rules

### Pre-Aggregated Metrics

```yaml
# prometheus-recording-rules.yaml
groups:
  - name: http_request_rates
    interval: 15s
    rules:
      # Request rate (per-second)
      - record: greyhaven:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m]))

      # Request rate by service
      - record: greyhaven:http_requests:rate5m:by_service
        expr: sum(rate(http_requests_total[5m])) by (service)

      # Error rate (percentage)
      - record: greyhaven:http_errors:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))

      # p95 latency
      - record: greyhaven:http_latency:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

**Benefits**:
- Faster dashboard queries (pre-computed)
- Consistent naming convention
- Lower cardinality

**Usage**:
```promql
# Use recording rule instead of raw metric
greyhaven:http_requests:rate5m  # Fast ⚡

# Instead of:
sum(rate(http_requests_total[5m]))  # Slow 🐌
```

## Common Patterns

### Availability SLI

```promql
# Availability = successful requests / total requests
sum(rate(http_requests_total{status=~"2..|3.."}[30d]))
/
sum(rate(http_requests_total[30d]))
```

### Latency SLI (p95 < 200ms)

```promql
# Percentage of requests under 200ms threshold
sum(rate(http_request_duration_seconds_bucket{le="0.2"}[30d]))
/
sum(rate(http_request_duration_seconds_count[30d]))
```

### Error Budget Remaining

```promql
# Error budget remaining (for 99.9% SLO)
1 - (
  (1 - greyhaven:sli:availability:30d)
  /
  (1 - 0.999)
)
```

### Burn Rate (1h window)

```promql
# How fast error budget is being consumed
(1 - greyhaven:sli:availability:1h)
/
(1 - 0.999)  # 99.9% SLO
```

### Top N Slowest Endpoints

```promql
# Top 10 slowest endpoints by p95 latency
topk(10,
  histogram_quantile(0.95,
    sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path)
  )
)
```

### Request Rate Growth

```promql
# Request rate compared to 1 week ago
(
  sum(rate(http_requests_total[5m]))
  /
  sum(rate(http_requests_total[5m] offset 7d))
) - 1

# Result: 0.15 (15% growth)
```

## Performance Optimization

### Avoid High Cardinality

```promql
# BAD: User ID in labels (millions of unique series)
http_requests_total{user_id="12345"}  # ❌ High cardinality

# GOOD: Aggregate first, then filter
sum(rate(http_requests_total[5m])) by (service)  # ✅ Low cardinality
```

### Use Recording Rules

```promql
# BAD: Complex query in dashboard (slow)
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket{service="fastapi"}[5m])) by (le)
)

# GOOD: Pre-calculated recording rule (fast)
greyhaven:http_latency:p95{service="fastapi"}
```

### Limit Time Range

```promql
# BAD: 90-day query (very slow)
sum(rate(http_requests_total[90d]))

# GOOD: Use recording rules for long ranges
greyhaven:http_requests:rate30d  # Pre-aggregated daily
```

## Related Documentation

- **Examples**: [Prometheus + Grafana Setup](../examples/prometheus-grafana-setup.md)
- **Reference**: [Golden Signals](golden-signals.md), [SLO Best Practices](slo-best-practices.md)
- **Templates**: [Recording Rules](../templates/prometheus-recording-rules.yaml)

---

Return to [reference index](INDEX.md)
