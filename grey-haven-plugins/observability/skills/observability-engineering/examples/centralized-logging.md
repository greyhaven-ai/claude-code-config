# Centralized Logging with Fluentd + Elasticsearch

Production log aggregation for multi-region Grey Haven deployments with structured logging, PII redaction, and Kibana dashboards.

## Overview

**Before Implementation**:
- Logs scattered across pods (kubectl logs pod-xyz)
- Log search time: 5+ minutes per query
- No log retention policy (disk full incidents)
- PII exposed in logs (GDPR violation risk)

**After Implementation**:
- Centralized log storage (500GB/day ingested)
- Log search time: <10 seconds via Kibana
- 90% compression (10TB → 1TB storage)
- Automatic PII redaction (SSN, credit cards, emails)
- 1-year retention with tiered storage (Hot/Warm/Cold/Archive)

**Technologies**: Fluentd DaemonSet, Elasticsearch, Kibana, Log4j/Winston, Grok patterns

**Cost**: $800/month (AWS ElasticSearch managed service)

## 1. Fluentd DaemonSet Deployment

### Kubernetes Deployment

```yaml
# fluentd-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd
      containers:
        - name: fluentd
          image: fluent/fluentd-kubernetes-daemonset:v1.16-debian-elasticsearch7-1
          env:
            - name: FLUENT_ELASTICSEARCH_HOST
              value: "elasticsearch.logging.svc.cluster.local"
            - name: FLUENT_ELASTICSEARCH_PORT
              value: "9200"
            - name: FLUENT_ELASTICSEARCH_SCHEME
              value: "http"
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: config
              mountPath: /fluentd/etc/fluent.conf
              subPath: fluent.conf
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: config
          configMap:
            name: fluentd-config
```

### Fluentd Configuration

```ruby
# fluentd.conf
<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/fluentd-containers.log.pos
  tag kubernetes.*
  read_from_head true
  <parse>
    @type json
    time_key time
    time_format %Y-%m-%dT%H:%M:%S.%NZ
  </parse>
</source>

# Parse TanStack Start logs (Winston JSON format)
<filter kubernetes.**tanstack**>
  @type parser
  key_name log
  <parse>
    @type json
    time_key timestamp
  </parse>
</filter>

# Parse FastAPI logs (Python logging JSON format)
<filter kubernetes.**fastapi**>
  @type parser
  key_name log
  <parse>
    @type json
  </parse>
</filter>

# Add Kubernetes metadata
<filter kubernetes.**>
  @type kubernetes_metadata
  @id kubernetes_metadata
</filter>

# PII redaction (SSN, credit card, email)
<filter **>
  @type record_transformer
  enable_ruby true
  <record>
    log ${record["log"].to_s.gsub(/\b\d{3}-\d{2}-\d{4}\b/, "***-**-****")}  # SSN
    log ${record["log"].to_s.gsub(/\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b/, "****-****-****-****")}  # Credit card
    log ${record["log"].to_s.gsub(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/, "***@***.***")}  # Email
  </record>
</filter>

# Route to Elasticsearch
<match **>
  @type elasticsearch
  host elasticsearch.logging.svc.cluster.local
  port 9200
  logstash_format true
  logstash_prefix greyhaven
  include_timestamp true
  <buffer>
    @type file
    path /var/log/fluentd-buffers/kubernetes.system.buffer
    flush_mode interval
    retry_type exponential_backoff
    flush_interval 5s
    retry_forever false
    retry_max_interval 30
    chunk_limit_size 2M
    queue_limit_length 8
    overflow_action block
  </buffer>
</match>
```

## 2. Structured Logging

### TypeScript (TanStack Start with Winston)

```typescript
// utils/logger.ts
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'tanstack-frontend',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({filename: 'app.log'})
  ]
});

// Usage in server functions
export const createOrder = createServerFn({method: 'POST'})
  .handler(async ({data}) => {
    const session = await auth.api.getSession({headers: request.headers});

    logger.info('Order creation started', {
      user_id: session.user.id,
      tenant_id: session.user.tenantId,
      order_amount: data.amount,
      trace_id: request.headers.get('x-trace-id')  // Distributed tracing
    });

    try {
      const order = await db.insert(orders).values({...data});

      logger.info('Order created successfully', {
        order_id: order.id,
        user_id: session.user.id,
        tenant_id: session.user.tenantId
      });

      return order;
    } catch (error) {
      logger.error('Order creation failed', {
        error: error.message,
        stack: error.stack,
        user_id: session.user.id,
        tenant_id: session.user.tenantId,
        trace_id: request.headers.get('x-trace-id')
      });
      throw error;
    }
  });
```

### Python (FastAPI with Python logging)

```python
# logging_config.py
import logging
import json
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['timestamp'] = record.created
        log_record['level'] = record.levelname
        log_record['service'] = 'fastapi-backend'

logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Usage in FastAPI endpoints
@app.post("/orders")
async def create_order(order: OrderCreate, request: Request):
    logger.info("Order creation started", extra={
        "user_id": order.user_id,
        "tenant_id": order.tenant_id,
        "order_amount": order.amount,
        "trace_id": request.headers.get("x-trace-id")
    })

    try:
        db_order = await create_order_in_db(order)

        logger.info("Order created", extra={
            "order_id": db_order.id,
            "user_id": order.user_id,
            "tenant_id": order.tenant_id
        })

        return db_order
    except Exception as e:
        logger.error("Order creation failed", extra={
            "error": str(e),
            "user_id": order.user_id,
            "tenant_id": order.tenant_id,
            "trace_id": request.headers.get("x-trace-id")
        }, exc_info=True)
        raise
```

## 3. Elasticsearch Index Lifecycle Management (ILM)

### ILM Policy

```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "1d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "forcemerge": {"max_num_segments": 1},
          "shrink": {"number_of_shards": 1}
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

**Retention Strategy**:
- **Hot** (0-7 days): Fast SSD storage, all logs searchable
- **Warm** (7-30 days): Slower storage, merged indices
- **Cold** (30-365 days): Archive storage, frozen indices (read-only)
- **Delete** (>365 days): Permanently deleted

## 4. Kibana Dashboards

### Error Tracking Dashboard

**Saved Search** (KQL Query):
```
level: ERROR AND service: fastapi-backend
```

**Visualizations**:
```json
{
  "title": "Error Rate Over Time",
  "type": "line",
  "params": {
    "aggs": [
      {
        "id": "1",
        "type": "count",
        "schema": "metric"
      },
      {
        "id": "2",
        "type": "date_histogram",
        "schema": "segment",
        "params": {"field": "timestamp", "interval": "5m"}
      }
    ],
    "filters": [{"query": "level: ERROR"}]
  }
}
```

### Audit Log Dashboard

```
KQL: event_type: ("order_created" OR "payment_processed" OR "user_deleted")

Columns: timestamp, user_id, tenant_id, event_type, order_id, amount
```

## 5. Log Parsing (Grok Patterns)

### PostgreSQL Logs

```ruby
# PostgreSQL query log parsing
<filter **postgres**>
  @type parser
  key_name log
  <parse>
    @type grok
    grok_pattern %{TIMESTAMP_ISO8601:timestamp} \[%{NUMBER:pid}\] %{WORD:user}@%{WORD:database} %{WORD:level}:  duration: %{NUMBER:duration} ms  statement: %{GREEDYDATA:query}
  </parse>
</filter>
```

### Nginx Access Logs

```ruby
<filter **nginx**>
  @type parser
  key_name log
  <parse>
    @type grok
    grok_pattern %{COMBINEDAPACHELOG}
  </parse>
</filter>
```

## 6. Alerting with ElastAlert

```yaml
# elastalert-rules/high-error-rate.yaml
name: High Error Rate Alert
type: frequency
index: greyhaven-*
num_events: 50
timeframe:
  minutes: 5

filter:
  - term:
      level: ERROR

alert:
  - slack:
      slack_webhook_url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL

alert_text: |
  **High Error Rate Detected**
  50+ errors in last 5 minutes

  Service: {service}
  Error: {error}

  [View in Kibana](https://kibana.greyhaven.io/app/discover)
```

## 7. Log Volume Optimization

### Before Optimization (10TB/month)

```
DEBUG logs: 70% (7TB)  ← Unnecessary in production
INFO logs: 20% (2TB)
WARN logs: 5% (500GB)
ERROR logs: 5% (500GB)
```

### After Optimization (1TB/month - 90% reduction)

```python
# Only log INFO+ in production
if os.getenv("ENVIRONMENT") == "production":
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)

# Sample verbose logs (1 in 100)
if random.random() < 0.01:
    logger.debug("Verbose debug info", extra={...})
```

**Result**: $8,000/month → $800/month (90% cost reduction)

## 8. PII Redaction Validation

### Test Cases

```ruby
# fluentd-test.rb - PII redaction validation
class TestPIIRedaction < Test::Unit::TestCase
  def test_ssn_redaction
    assert_equal "User SSN: ***-**-****", redact_pii("User SSN: 123-45-6789")
  end

  def test_credit_card_redaction
    assert_equal "Card: ****-****-****-****", redact_pii("Card: 4242-4242-4242-4242")
  end

  def test_email_redaction
    assert_equal "User email: ***@***.***", redact_pii("User email: user@example.com")
  end
end
```

## 9. Results and Impact

### Before vs After Metrics

| Metric | Before | After | Impact |
|--------|--------|-------|--------|
| **Log Search Time** | 5+ min | <10 sec | **97% faster** |
| **Storage Cost** | $8,000/month | $800/month | **90% reduction** |
| **Disk Usage** | 10TB | 1TB (90% compression) | **10x reduction** |
| **Retention** | 7 days (disk limit) | 365 days | **52x longer** |
| **PII Compliance** | At risk | GDPR compliant | **Risk eliminated** |
| **MTTR** | 45 min | 8 min | **82% faster** |

### Key Discoveries

**1. N+1 Query Detection via Logs**
- Kibana query: `query: "*SELECT * FROM orders*" AND duration > 100`
- Found 15 queries per request (should be 1)
- Fix: Added Drizzle `with` clause for eager loading
- Result: 15 queries → 1 query, 200ms → 20ms

**2. Unauthorized Access Attempt**
- Audit log showed 500+ failed login attempts from single IP
- Investigation: Brute force attack on admin accounts
- Response: IP blocked via Cloudflare WAF, MFA enforced
- Result: Attack mitigated in 5 minutes

**3. Memory Leak Detection**
- Log pattern: "Out of memory" errors every 6 hours
- Root cause: Unclosed database connections
- Fix: Implemented connection pooling with proper cleanup
- Result: Zero OOM errors after fix

## Related Documentation

- **Prometheus**: [prometheus-grafana-setup.md](prometheus-grafana-setup.md) - Metrics monitoring
- **OpenTelemetry**: [opentelemetry-tracing.md](opentelemetry-tracing.md) - Distributed tracing
- **Reference**: [../reference/logging-best-practices.md](../reference/logging-best-practices.md)
- **Templates**: [../templates/fluentd-config.rb](../templates/fluentd-config.rb)

---

Return to [examples index](INDEX.md)
