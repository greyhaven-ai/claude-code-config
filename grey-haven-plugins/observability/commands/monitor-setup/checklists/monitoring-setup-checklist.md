# Monitoring Setup Checklist

**Use when setting up production monitoring and observability infrastructure.**

## Phase 1: Planning and Design

- [ ] Service inventory completed (all services identified)
- [ ] Service criticality tiers defined (Critical, Essential, Standard, Best Effort)
- [ ] Monitoring technology stack selected (Prometheus, Grafana, OpenTelemetry)
- [ ] Infrastructure requirements defined (Kubernetes, VMs, serverless)
- [ ] Retention policies defined (metrics: 15d hot, 90d cold; logs: 30d; traces: 7d)
- [ ] Cost budget allocated for monitoring infrastructure
- [ ] Team training plan created

## Phase 2: Infrastructure Setup

### Prometheus Deployment
- [ ] Prometheus Operator installed (or Prometheus standalone)
- [ ] Persistent storage configured (100GB+ for production)
- [ ] Retention period set (15 days minimum)
- [ ] Resource limits configured (CPU: 2 cores, Memory: 4GB minimum)
- [ ] High availability configured (2+ replicas for production)
- [ ] node-exporter deployed (host metrics)
- [ ] kube-state-metrics deployed (Kubernetes metrics)
- [ ] ServiceMonitor resources created for auto-discovery

### Grafana Deployment
- [ ] Grafana installed and accessible
- [ ] Persistent storage configured (10GB for dashboards)
- [ ] Admin password set securely (via Doppler or similar)
- [ ] Prometheus data source configured
- [ ] User authentication configured (OAuth, LDAP, or built-in)
- [ ] Dashboard permissions configured (viewer, editor, admin)
- [ ] Dashboard folders created (Services, Infrastructure, Business)

### AlertManager Deployment
- [ ] AlertManager deployed
- [ ] Persistent storage configured (for silences and notifications)
- [ ] Webhook receivers configured (Slack, PagerDuty, email)
- [ ] Routing rules defined
- [ ] Grouping configured (by alertname, cluster, service)
- [ ] Inhibition rules configured (prevent alert storms)
- [ ] Test alerts sent and received

## Phase 3: Application Instrumentation

### Metrics Instrumentation
- [ ] Prometheus client library installed (prom-client, prometheus_client)
- [ ] Metrics endpoint exposed (/metrics)
- [ ] HTTP request counter instrumented (http_requests_total)
- [ ] HTTP request duration histogram instrumented (http_request_duration_seconds)
- [ ] Business metrics instrumented (checkouts, signups, revenue)
- [ ] Resource metrics instrumented (active connections, queue depth)
- [ ] Metrics labeled appropriately (method, route, status_code)
- [ ] ServiceMonitor or scrape config created

### Structured Logging
- [ ] JSON logging format implemented
- [ ] Log levels configured (DEBUG, INFO, WARN, ERROR)
- [ ] Log fields standardized (timestamp, level, message, service, environment)
- [ ] Trace context added to logs (trace_id, span_id)
- [ ] Sensitive data redacted from logs (passwords, tokens, PII)
- [ ] Log shipping configured (Fluentd, Fluent Bit, or stdout)
- [ ] Log aggregation destination configured (Loki, Elasticsearch, CloudWatch)

### Distributed Tracing
- [ ] OpenTelemetry SDK installed
- [ ] Trace exporter configured (OTLP, Jaeger, Zipkin)
- [ ] Auto-instrumentation enabled (HTTP, database, Redis)
- [ ] Service name and version configured
- [ ] Sampling strategy defined (10% of requests, 100% of errors)
- [ ] Trace context propagation verified (across services)
- [ ] Custom spans added for critical operations

## Phase 4: Recording Rules

### Golden Signals Recording Rules
- [ ] Request rate rule created (service:request_rate:5m)
- [ ] Success rate rule created (service:success_rate:5m)
- [ ] Error rate rule created (service:error_rate:5m)
- [ ] Latency p50 rule created (service:latency_p50:5m)
- [ ] Latency p95 rule created (service:latency_p95:5m)
- [ ] Latency p99 rule created (service:latency_p99:5m)
- [ ] Recording rules validated (no syntax errors)
- [ ] Recording rules applied to Prometheus

### Resource Utilization Rules
- [ ] CPU usage rules created
- [ ] Memory usage rules created
- [ ] Disk usage rules created
- [ ] Network I/O rules created
- [ ] Database connection pool rules created (if applicable)

## Phase 5: Alert Rules

### High-Severity Alerts (Critical)
- [ ] High error rate alert created (> 5% for 5 minutes)
- [ ] High memory usage alert created (> 90% for 10 minutes)
- [ ] Service down alert created (no metrics for 2 minutes)
- [ ] Database connection failure alert created
- [ ] Certificate expiration alert created (< 7 days)

### Medium-Severity Alerts (Warning)
- [ ] Slow response time alert created (p95 > 1s for 10 minutes)
- [ ] High CPU usage alert created (> 80% for 15 minutes)
- [ ] Disk space low alert created (< 20% for 30 minutes)
- [ ] High request rate alert created (> 2x normal for 5 minutes)

### Alert Configuration
- [ ] Alert thresholds validated (not too sensitive)
- [ ] Alert for durations configured (prevent flapping)
- [ ] Alert severity labels set (critical, warning, info)
- [ ] Team labels set (backend, frontend, platform)
- [ ] Alert annotations added (summary, description, runbook_url)
- [ ] Alerts validated (no syntax errors)
- [ ] Test alerts triggered and verified

## Phase 6: Grafana Dashboards

### Golden Signals Dashboard
- [ ] Request rate panel created
- [ ] Error rate panel created
- [ ] Latency panel created (p50, p95, p99)
- [ ] Saturation panel created (CPU, memory, connections)
- [ ] Alert annotations overlayed on panels
- [ ] Dashboard variables created (service, environment)
- [ ] Time range controls configured

### Service Overview Dashboard
- [ ] Per-service health panel created
- [ ] Request rate breakdown by route/endpoint
- [ ] Error rate breakdown by error type
- [ ] Latency distribution histogram
- [ ] Active connections/users panel
- [ ] Business metrics panel (checkouts, signups)

### Infrastructure Dashboard
- [ ] CPU usage panel (per node/pod)
- [ ] Memory usage panel (per node/pod)
- [ ] Disk I/O panel
- [ ] Network I/O panel
- [ ] Pod status panel (Running, Pending, Failed)
- [ ] Node status panel (Ready, NotReady)

### Dashboard Quality
- [ ] Dashboards tested with real data
- [ ] Dashboards accessible to team (correct permissions)
- [ ] Dashboard links added (drill-down to other dashboards)
- [ ] Dashboard descriptions added
- [ ] Dashboards organized in folders
- [ ] Dashboards exported as JSON (version control)

## Phase 7: Runbooks

### Runbook Creation
- [ ] Runbook for high error rate alert
- [ ] Runbook for slow response time alert
- [ ] Runbook for high CPU usage alert
- [ ] Runbook for high memory usage alert
- [ ] Runbook for service down alert
- [ ] Runbook URLs linked from alerts

### Runbook Quality
- [ ] Diagnostic steps documented
- [ ] Common causes identified
- [ ] Remediation steps documented
- [ ] Escalation procedures defined
- [ ] Contact information added
- [ ] Runbooks tested during incident simulations

## Phase 8: Testing and Validation

### Metrics Testing
- [ ] Metrics endpoint accessible (/metrics)
- [ ] Metrics scraped by Prometheus (verify targets)
- [ ] Recording rules producing data (verify in Prometheus)
- [ ] Metrics visible in Grafana dashboards
- [ ] Metric cardinality acceptable (< 10k per metric)

### Logging Testing
- [ ] Logs formatted as JSON
- [ ] Logs contain required fields (timestamp, level, message)
- [ ] Trace context present in logs (trace_id, span_id)
- [ ] Logs aggregated in destination system
- [ ] Logs searchable and filterable

### Tracing Testing
- [ ] Traces visible in tracing UI (Jaeger, Zipkin)
- [ ] Spans contain correct attributes (service, operation, duration)
- [ ] Trace context propagates across services
- [ ] Sampling rate validated (10% of traces visible)
- [ ] Error traces captured (100% of errors)

### Alerting Testing
- [ ] Test alerts triggered manually (change threshold temporarily)
- [ ] Alerts routed to correct receivers (Slack, PagerDuty, email)
- [ ] Alert grouping working as expected
- [ ] Alert inhibition working (no alert storms)
- [ ] Silence functionality tested
- [ ] Escalation tested (after repeat_interval)

## Phase 9: Documentation

- [ ] Architecture diagram created (Mermaid or similar)
- [ ] Metrics catalog documented (all custom metrics)
- [ ] Dashboard guide created (how to use dashboards)
- [ ] Alert runbooks linked from alerts
- [ ] Incident response procedures documented
- [ ] On-call rotation documented
- [ ] Postmortem template created
- [ ] Training materials created

## Phase 10: Training and Rollout

### Team Training
- [ ] Grafana dashboard training conducted
- [ ] Alert response training conducted
- [ ] Runbook walkthrough completed
- [ ] Incident simulation performed (test on-call procedures)
- [ ] Q&A session held

### Rollout
- [ ] Monitoring enabled for non-production environments first
- [ ] Monitoring validated in staging
- [ ] Monitoring rolled out to production
- [ ] Monitoring announced to team (documentation links)
- [ ] Feedback collected after 1 week
- [ ] Adjustments made based on feedback

## Phase 11: Continuous Improvement

### Weekly Tasks
- [ ] Review fired alerts (identify false positives)
- [ ] Adjust alert thresholds (reduce noise)
- [ ] Review new services (add monitoring)
- [ ] Review dashboard usage (identify unused dashboards)

### Monthly Tasks
- [ ] Review recording rules (identify slow queries)
- [ ] Review cardinality (identify high-cardinality metrics)
- [ ] Review retention policies (adjust based on cost)
- [ ] Review runbooks (update based on incidents)
- [ ] Conduct incident retrospectives

### Quarterly Tasks
- [ ] Comprehensive monitoring audit
- [ ] Review SLO adherence (run /slo-implement if needed)
- [ ] Review monitoring costs (optimize if needed)
- [ ] Review team training needs (conduct refreshers)
- [ ] Update monitoring strategy based on lessons learned

## Critical Validations

- [ ] All production services instrumented (metrics, logs, traces)
- [ ] Golden Signals monitored for all critical services
- [ ] Alerts configured for all critical issues
- [ ] Runbooks exist for all alerts
- [ ] Dashboards accessible and useful to team
- [ ] Monitoring infrastructure highly available (2+ replicas)
- [ ] Metrics retention ≥ 15 days
- [ ] Logs retention ≥ 30 days
- [ ] Traces retention ≥ 7 days
- [ ] Cost within budget
- [ ] Team trained on monitoring tools
- [ ] Incident response procedures tested

## Cost Optimization

- [ ] Metric cardinality controlled (< 10k per metric)
- [ ] Trace sampling configured (10% of requests)
- [ ] Log retention optimized (30d vs. 90d)
- [ ] Recording rules used to pre-aggregate expensive queries
- [ ] Open source stack used where possible (vs. SaaS)
- [ ] Resource limits configured (prevent runaway costs)

## Security

- [ ] Grafana authentication configured (not anonymous)
- [ ] Prometheus endpoints protected (not public)
- [ ] Sensitive data redacted from logs
- [ ] Secrets managed via Doppler or similar
- [ ] Alert webhooks secured (HTTPS, authentication)
- [ ] Dashboard permissions configured (viewer, editor, admin)
