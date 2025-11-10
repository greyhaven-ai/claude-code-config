# Observability Engineering Setup Checklist

Comprehensive checklist for implementing production-grade observability with logs, metrics, traces, and alerts.

## Pre-Implementation Planning

- [ ] **Define observability goals** (debug production issues, monitor SLAs, detect anomalies)
- [ ] **Choose observability stack**:
  - [ ] Logging: Pino (Node.js), structlog (Python), CloudWatch, Datadog
  - [ ] Metrics: Prometheus, Datadog, CloudWatch
  - [ ] Tracing: OpenTelemetry, Datadog APM, Jaeger
  - [ ] Visualization: Grafana, Datadog, Honeycomb

- [ ] **Set up observability infrastructure** (collectors, storage, dashboards)
- [ ] **Define data retention** policies (logs: 30 days, metrics: 1 year, traces: 7 days)
- [ ] **Plan for scale** (log volume, metric cardinality, trace sampling)

## Structured Logging

### Logger Configuration

- [ ] **Structured logger installed**:
  - Node.js: `pino` with `pino-pretty` for dev
  - Python: `structlog` with JSON formatter
  - Browser: Custom JSON logger or service integration

- [ ] **Log levels defined**:
  - [ ] TRACE: Very detailed debugging
  - [ ] DEBUG: Detailed debugging info
  - [ ] INFO: General informational messages
  - [ ] WARN: Warning messages (recoverable issues)
  - [ ] ERROR: Error messages (failures)
  - [ ] FATAL: Critical failures (application crash)

- [ ] **Environment-based configuration**:
  - [ ] Development: Pretty-printed logs, DEBUG level
  - [ ] Production: JSON logs, INFO level
  - [ ] Test: Silent or minimal logs

### Log Structure

- [ ] **Standard log format** across services:
  ```json
  {
    "level": "info",
    "timestamp": "2025-11-10T10:30:00.000Z",
    "service": "api-server",
    "environment": "production",
    "tenant_id": "uuid",
    "user_id": "uuid",
    "request_id": "uuid",
    "message": "User logged in",
    "duration_ms": 150,
    "http": {
      "method": "POST",
      "path": "/api/login",
      "status": 200,
      "user_agent": "Mozilla/5.0..."
    }
  }
  ```

- [ ] **Correlation IDs** added:
  - [ ] request_id: Unique per request
  - [ ] session_id: Unique per session
  - [ ] trace_id: Unique per distributed trace
  - [ ] tenant_id: Multi-tenant context

- [ ] **Context propagation** through request lifecycle
- [ ] **Sensitive data redacted** (passwords, tokens, credit cards)

### What to Log

- [ ] **Request/response logging**:
  - [ ] HTTP method, path, status code
  - [ ] Request duration
  - [ ] User agent, IP address (hashed or anonymized)
  - [ ] Query parameters (non-sensitive)

- [ ] **Authentication events**:
  - [ ] Login success/failure
  - [ ] Logout
  - [ ] Token refresh
  - [ ] Permission checks

- [ ] **Business events**:
  - [ ] User registration
  - [ ] Payment processing
  - [ ] Data exports
  - [ ] Admin actions

- [ ] **Errors and exceptions**:
  - [ ] Error message
  - [ ] Stack trace
  - [ ] Error context (what user was doing)
  - [ ] Affected resources (user_id, tenant_id, entity_id)

- [ ] **Performance metrics**:
  - [ ] Database query times
  - [ ] External API call times
  - [ ] Cache hit/miss rates
  - [ ] Background job durations

### Log Aggregation

- [ ] **Logs shipped** to central location:
  - [ ] CloudWatch Logs
  - [ ] Datadog Logs
  - [ ] Elasticsearch (ELK stack)
  - [ ] Splunk

- [ ] **Log retention** configured (30-90 days typical)
- [ ] **Log volume** monitored (cost management)
- [ ] **Log sampling** for high-volume services (if needed)

## Application Metrics

### Metric Types

- [ ] **Counters** for events that only increase:
  - [ ] Total requests
  - [ ] Total errors
  - [ ] Total registrations

- [ ] **Gauges** for values that go up and down:
  - [ ] Active connections
  - [ ] Memory usage
  - [ ] Queue depth

- [ ] **Histograms** for distributions:
  - [ ] Request duration
  - [ ] Response size
  - [ ] Database query time

- [ ] **Summaries** for quantiles (p50, p95, p99)

### Standard Metrics

#### HTTP Metrics

- [ ] **http_requests_total** (counter):
  - Labels: method, path, status, tenant_id
  - Track total requests per endpoint

- [ ] **http_request_duration_seconds** (histogram):
  - Labels: method, path, status
  - Buckets: 0.1, 0.5, 1, 2, 5, 10 seconds

- [ ] **http_request_size_bytes** (histogram)
- [ ] **http_response_size_bytes** (histogram)

#### Database Metrics

- [ ] **db_queries_total** (counter):
  - Labels: operation (SELECT, INSERT, UPDATE, DELETE), table

- [ ] **db_query_duration_seconds** (histogram):
  - Labels: operation, table
  - Track slow queries (p95, p99)

- [ ] **db_connection_pool_size** (gauge)
- [ ] **db_connection_pool_available** (gauge)

#### Application Metrics

- [ ] **active_sessions** (gauge)
- [ ] **background_jobs_total** (counter):
  - Labels: job_name, status (success, failure)

- [ ] **background_job_duration_seconds** (histogram):
  - Labels: job_name

- [ ] **cache_operations_total** (counter):
  - Labels: operation (hit, miss, set, delete)

- [ ] **external_api_calls_total** (counter):
  - Labels: service, status

- [ ] **external_api_duration_seconds** (histogram):
  - Labels: service

#### System Metrics

- [ ] **process_cpu_usage_percent** (gauge)
- [ ] **process_memory_usage_bytes** (gauge)
- [ ] **process_heap_usage_bytes** (gauge) - JavaScript specific
- [ ] **process_open_file_descriptors** (gauge)

### Metric Collection

- [ ] **Prometheus client library** installed:
  - Node.js: `prom-client`
  - Python: `prometheus-client`
  - Custom: OpenTelemetry SDK

- [ ] **Metrics endpoint** exposed (`/metrics`)
- [ ] **Prometheus scrapes** endpoint (or push to gateway)
- [ ] **Metric naming** follows conventions:
  - Lowercase with underscores
  - Unit suffixes (_seconds, _bytes, _total)
  - Namespace prefix (myapp_http_requests_total)

### Multi-Tenant Metrics

- [ ] **tenant_id label** on all relevant metrics
- [ ] **Per-tenant dashboards** (filter by tenant_id)
- [ ] **Tenant resource usage** tracked:
  - [ ] API calls per tenant
  - [ ] Database storage per tenant
  - [ ] Data transfer per tenant

- [ ] **Tenant quotas** monitored (alert on approaching limit)

## Distributed Tracing

### Tracing Setup

- [ ] **OpenTelemetry SDK** installed:
  - Node.js: `@opentelemetry/sdk-node`
  - Python: `opentelemetry-sdk`

- [ ] **Tracing backend** configured:
  - [ ] Jaeger (self-hosted)
  - [ ] Datadog APM
  - [ ] Honeycomb
  - [ ] AWS X-Ray

- [ ] **Auto-instrumentation** enabled:
  - [ ] HTTP client/server
  - [ ] Database queries
  - [ ] Redis operations
  - [ ] Message queues

### Span Creation

- [ ] **Custom spans** for business logic:
  ```typescript
  const span = tracer.startSpan('process-payment');
  span.setAttribute('tenant_id', tenantId);
  span.setAttribute('amount', amount);
  try {
    await processPayment();
    span.setStatus({ code: SpanStatusCode.OK });
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR });
    throw error;
  } finally {
    span.end();
  }
  ```

- [ ] **Span attributes** include context:
  - [ ] tenant_id, user_id, request_id
  - [ ] Input parameters (non-sensitive)
  - [ ] Result status

- [ ] **Span events** for key moments:
  - [ ] "Payment started"
  - [ ] "Database query executed"
  - [ ] "External API called"

### Trace Context Propagation

- [ ] **W3C Trace Context** headers propagated:
  - traceparent: trace-id, parent-span-id, flags
  - tracestate: vendor-specific data

- [ ] **Context propagated** across:
  - [ ] HTTP requests (frontend ↔ backend)
  - [ ] Background jobs
  - [ ] Message queues
  - [ ] Microservices

- [ ] **Trace ID** included in logs (correlate logs + traces)

### Sampling

- [ ] **Sampling strategy** defined:
  - [ ] Head-based: Sample at trace start (1%, 10%, 100%)
  - [ ] Tail-based: Sample after trace completes (error traces, slow traces)
  - [ ] Adaptive: Sample based on load

- [ ] **Always sample** errors and slow requests
- [ ] **Sample rate** appropriate for volume (start high, reduce if needed)

## Alerting

### Alert Definitions

- [ ] **Error rate alerts**:
  - [ ] Condition: Error rate > 5% for 5 minutes
  - [ ] Severity: Critical
  - [ ] Action: Page on-call engineer

- [ ] **Latency alerts**:
  - [ ] Condition: p95 latency > 1s for 10 minutes
  - [ ] Severity: Warning
  - [ ] Action: Slack notification

- [ ] **Availability alerts**:
  - [ ] Condition: Health check fails 3 consecutive times
  - [ ] Severity: Critical
  - [ ] Action: Page on-call + auto-restart

- [ ] **Resource alerts**:
  - [ ] Memory usage > 80%
  - [ ] CPU usage > 80%
  - [ ] Disk usage > 85%
  - [ ] Database connections > 90% of pool

- [ ] **Business metric alerts**:
  - [ ] Registration rate drops > 50%
  - [ ] Payment failures increase > 10%
  - [ ] Active users drop significantly

### Alert Channels

- [ ] **PagerDuty** (or equivalent) for critical alerts
- [ ] **Slack** for warnings and notifications
- [ ] **Email** for non-urgent alerts
- [ ] **SMS** for highest priority (only use sparingly)

### Alert Management

- [ ] **Alert fatigue** prevented:
  - [ ] Appropriate thresholds (not too sensitive)
  - [ ] Proper severity levels (not everything is critical)
  - [ ] Alert aggregation (deduplicate similar alerts)

- [ ] **Runbooks** for each alert:
  - [ ] What the alert means
  - [ ] How to investigate
  - [ ] How to resolve
  - [ ] Escalation path

- [ ] **Alert suppression** during deployments (planned downtime)
- [ ] **Alert escalation** if not acknowledged

## Dashboards & Visualization

### Standard Dashboards

- [ ] **Service Overview** dashboard:
  - [ ] Request rate (requests/sec)
  - [ ] Error rate (errors/sec, %)
  - [ ] Latency (p50, p95, p99)
  - [ ] Availability (uptime %)

- [ ] **Database** dashboard:
  - [ ] Query rate
  - [ ] Slow queries (p95, p99)
  - [ ] Connection pool usage
  - [ ] Table sizes

- [ ] **System Resources** dashboard:
  - [ ] CPU usage
  - [ ] Memory usage
  - [ ] Disk I/O
  - [ ] Network I/O

- [ ] **Business Metrics** dashboard:
  - [ ] Active users
  - [ ] Registrations
  - [ ] Revenue
  - [ ] Feature usage

### Dashboard Best Practices

- [ ] **Auto-refresh** enabled (every 30-60 seconds)
- [ ] **Time range** configurable (last hour, 24h, 7 days)
- [ ] **Drill-down** to detailed views
- [ ] **Annotations** for deployments/incidents
- [ ] **Shared dashboards** accessible to team

### Per-Tenant Dashboards

- [ ] **Tenant filter** on all relevant dashboards
- [ ] **Tenant resource usage** visualized
- [ ] **Tenant-specific alerts** (if large customer)
- [ ] **Tenant comparison** view (compare usage across tenants)

## Health Checks

### Endpoint Implementation

- [ ] **Health check endpoint** (`/health` or `/healthz`):
  - [ ] Returns 200 OK when healthy
  - [ ] Returns 503 Service Unavailable when unhealthy
  - [ ] Includes subsystem status

```json
{
  "status": "healthy",
  "version": "1.2.3",
  "uptime_seconds": 86400,
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "external_api": "degraded"
  }
}
```

- [ ] **Liveness probe** (`/health/live`):
  - [ ] Checks if application is running
  - [ ] Fails → restart container

- [ ] **Readiness probe** (`/health/ready`):
  - [ ] Checks if application is ready to serve traffic
  - [ ] Fails → remove from load balancer

### Health Check Coverage

- [ ] **Database connectivity** checked
- [ ] **Cache connectivity** checked (Redis, Memcached)
- [ ] **External APIs** checked (optional, can cause false positives)
- [ ] **Disk space** checked
- [ ] **Critical dependencies** checked

### Monitoring Health Checks

- [ ] **Uptime monitoring** service (Pingdom, UptimeRobot, Datadog Synthetics)
- [ ] **Check frequency** appropriate (every 1-5 minutes)
- [ ] **Alerting** on failed health checks
- [ ] **Geographic monitoring** (check from multiple regions)

## Error Tracking

### Error Capture

- [ ] **Error tracking service** integrated:
  - [ ] Sentry
  - [ ] Datadog Error Tracking
  - [ ] Rollbar
  - [ ] Custom solution

- [ ] **Unhandled exceptions** captured automatically
- [ ] **Handled errors** reported when appropriate
- [ ] **Error context** included:
  - [ ] User ID, tenant ID
  - [ ] Request ID, trace ID
  - [ ] User actions (breadcrumbs)
  - [ ] Environment variables (non-sensitive)

### Error Grouping

- [ ] **Errors grouped** by fingerprint (same error, different occurrences)
- [ ] **Error rate** tracked per group
- [ ] **Alerting** on new error types or spike in existing
- [ ] **Error assignment** to team members
- [ ] **Resolution tracking** (mark errors as resolved)

### Privacy & Security

- [ ] **PII redacted** from error reports:
  - [ ] Passwords, tokens, API keys
  - [ ] Credit card numbers
  - [ ] Email addresses (unless necessary)
  - [ ] SSNs, tax IDs

- [ ] **Source maps** uploaded for frontend (de-minify stack traces)
- [ ] **Release tagging** (associate errors with deployments)

## Performance Monitoring

### Real User Monitoring (RUM)

- [ ] **RUM tool integrated** (Datadog RUM, New Relic Browser, Google Analytics):
  - [ ] Page load times
  - [ ] Core Web Vitals (LCP, FID, CLS)
  - [ ] JavaScript errors
  - [ ] User sessions

- [ ] **Performance budgets** defined:
  - [ ] First Contentful Paint < 1.8s
  - [ ] Largest Contentful Paint < 2.5s
  - [ ] Time to Interactive < 3.8s
  - [ ] Cumulative Layout Shift < 0.1

- [ ] **Alerting** on performance regressions

### Application Performance Monitoring (APM)

- [ ] **APM tool** integrated (Datadog APM, New Relic APM):
  - [ ] Trace every request
  - [ ] Identify slow endpoints
  - [ ] Database query analysis
  - [ ] External API profiling

- [ ] **Performance profiling** for critical paths:
  - [ ] Authentication flow
  - [ ] Payment processing
  - [ ] Data exports
  - [ ] Complex queries

## Cost Management

- [ ] **Observability costs** tracked:
  - [ ] Log ingestion costs
  - [ ] Metric cardinality costs
  - [ ] Trace sampling costs
  - [ ] Dashboard/seat costs

- [ ] **Cost optimization**:
  - [ ] Log sampling for high-volume services
  - [ ] Metric aggregation (reduce cardinality)
  - [ ] Trace sampling (not 100% in production)
  - [ ] Data retention policies

- [ ] **Budget alerts** configured

## Security & Compliance

- [ ] **Access control** on observability tools (role-based)
- [ ] **Audit logging** for observability access
- [ ] **Data retention** complies with regulations (GDPR, HIPAA)
- [ ] **Data encryption** in transit and at rest
- [ ] **PII handling** compliant (redaction, anonymization)

## Testing Observability

- [ ] **Log output** tested in unit tests:
  ```typescript
  test('logs user login', () => {
    const logs = captureLogs();
    await loginUser();
    expect(logs).toContainEqual(
      expect.objectContaining({
        level: 'info',
        message: 'User logged in',
        user_id: expect.any(String)
      })
    );
  });
  ```

- [ ] **Metrics** incremented in tests
- [ ] **Traces** created in integration tests
- [ ] **Health checks** tested
- [ ] **Alert thresholds** tested (inject failures, verify alert fires)

## Documentation

- [ ] **Observability runbook** created:
  - [ ] How to access logs, metrics, traces
  - [ ] How to create dashboards
  - [ ] How to set up alerts
  - [ ] Common troubleshooting queries

- [ ] **Alert runbooks** for each alert
- [ ] **Dashboard documentation** (what each panel shows)
- [ ] **Metric dictionary** (what each metric means)
- [ ] **On-call procedures** documented

## Scoring

- **85+ items checked**: Excellent - Production-grade observability ✅
- **65-84 items**: Good - Most observability covered ⚠️
- **45-64 items**: Fair - Significant gaps exist 🔴
- **<45 items**: Poor - Not ready for production ❌

## Priority Items

Address these first:
1. **Structured logging** - Foundation for debugging
2. **Error tracking** - Catch and fix bugs quickly
3. **Health checks** - Know when service is down
4. **Alerting** - Get notified of issues
5. **Key metrics** - Request rate, error rate, latency

## Common Pitfalls

❌ **Don't:**
- Log sensitive data (passwords, tokens, PII)
- Create high-cardinality metrics (user_id as label)
- Trace 100% of requests in production (sample instead)
- Alert on every anomaly (alert fatigue)
- Ignore observability until there's a problem

✅ **Do:**
- Log at appropriate levels (use DEBUG for verbose)
- Use correlation IDs throughout request lifecycle
- Set up alerts with clear runbooks
- Review dashboards regularly (detect issues early)
- Iterate on observability (improve over time)

## Related Resources

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Pino Logger](https://getpino.io)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [observability-engineering skill](../SKILL.md)

---

**Total Items**: 140+ observability checks
**Critical Items**: Logging, Metrics, Alerting, Health checks
**Coverage**: Logs, Metrics, Traces, Alerts, Dashboards
**Last Updated**: 2025-11-10
