# Data Quality Monitoring

Monitor data validation in production to detect quality issues, track metrics, and ensure reliability.

## Core Metrics

### Validation Error Rate

```python
# app/middleware/validation_metrics.py
from prometheus_client import Counter, Histogram
from fastapi import Request, Response
from pydantic import ValidationError
import time

validation_errors = Counter(
    'validation_errors_total',
    'Total validation errors',
    ['endpoint', 'error_type', 'field']
)

validation_duration = Histogram(
    'validation_duration_seconds',
    'Time spent in validation',
    ['endpoint']
)

async def track_validation_middleware(request: Request, call_next):
    """Track validation metrics."""
    start_time = time.time()
    endpoint = request.url.path

    try:
        response = await call_next(request)
        duration = time.time() - start_time
        validation_duration.labels(endpoint=endpoint).observe(duration)
        return response

    except ValidationError as e:
        for error in e.errors():
            validation_errors.labels(
                endpoint=endpoint,
                error_type=error['type'],
                field='.'.join(str(loc) for loc in error['loc'])
            ).inc()
        raise
```

### Data Profile Metrics

```python
# app/monitoring/data_profiler.py
from prometheus_client import Gauge, Info

# Track data distribution
field_value_distribution = Gauge(
    'field_value_distribution',
    'Distribution of field values',
    ['model', 'field', 'value_range']
)

# Track data completeness
field_completeness = Gauge(
    'field_completeness_ratio',
    'Ratio of non-null values',
    ['model', 'field']
)

def profile_model_data(model_name: str, instances: list):
    """Profile model data distribution."""
    for field_name in instances[0].__fields__:
        values = [getattr(inst, field_name) for inst in instances]

        # Completeness
        non_null = sum(1 for v in values if v is not None)
        completeness = non_null / len(values)
        field_completeness.labels(
            model=model_name,
            field=field_name
        ).set(completeness)

        # Distribution (for numeric fields)
        if all(isinstance(v, (int, float)) for v in values if v is not None):
            numeric_values = [v for v in values if v is not None]
            if numeric_values:
                _track_distribution(model_name, field_name, numeric_values)
```

## Error Tracking

### Structured Error Logging

```python
# app/logging/validation_logger.py
import structlog
from pydantic import ValidationError
from typing import Any

logger = structlog.get_logger()

def log_validation_error(
    error: ValidationError,
    context: dict[str, Any]
):
    """Log validation error with context."""
    for err in error.errors():
        logger.warning(
            "validation_error",
            error_type=err['type'],
            field='.'.join(str(loc) for loc in err['loc']),
            message=err['msg'],
            input_value=err.get('input'),
            context=context,
            user_id=context.get('user_id'),
            tenant_id=context.get('tenant_id'),
            endpoint=context.get('endpoint')
        )
```

### Error Aggregation

```python
# app/monitoring/error_aggregator.py
from collections import defaultdict
from datetime import datetime, timedelta

class ValidationErrorAggregator:
    """Aggregate validation errors for analysis."""

    def __init__(self):
        self.errors = defaultdict(lambda: defaultdict(int))
        self.time_window = timedelta(minutes=5)

    def record_error(
        self,
        endpoint: str,
        field: str,
        error_type: str
    ):
        """Record validation error."""
        key = (endpoint, field, error_type)
        self.errors[datetime.utcnow()][key] += 1

    def get_top_errors(self, limit: int = 10) -> list:
        """Get most frequent errors in time window."""
        cutoff = datetime.utcnow() - self.time_window
        recent_errors = defaultdict(int)

        for timestamp, errors in self.errors.items():
            if timestamp >= cutoff:
                for key, count in errors.items():
                    recent_errors[key] += count

        return sorted(
            recent_errors.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

    def get_error_rate(self, endpoint: str) -> float:
        """Calculate error rate for endpoint."""
        cutoff = datetime.utcnow() - self.time_window
        errors = sum(
            sum(counts.values())
            for ts, counts in self.errors.items()
            if ts >= cutoff
        )
        return errors / self.time_window.total_seconds()
```

## Alerting

### Prometheus Alerts

```yaml
# prometheus/alerts/validation.yml
groups:
  - name: data_validation
    interval: 30s
    rules:
      # High error rate
      - alert: HighValidationErrorRate
        expr: |
          rate(validation_errors_total[5m]) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High validation error rate on {{ $labels.endpoint }}"
          description: "Validation errors on {{ $labels.endpoint }} exceed 10/sec"

      # Specific field errors
      - alert: FrequentFieldValidationErrors
        expr: |
          sum by (field) (rate(validation_errors_total[10m])) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Frequent errors on field {{ $labels.field }}"
          description: "Field {{ $labels.field }} has >5 errors/sec"

      # Data completeness drop
      - alert: DataCompletenessDropped
        expr: |
          field_completeness_ratio < 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Data completeness dropped for {{ $labels.field }}"
          description: "Field {{ $labels.field }} completeness < 80%"
```

### Custom Alerting

```python
# app/monitoring/alerting.py
from enum import Enum
import httpx

class AlertSeverity(Enum):
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'

async def send_alert(
    title: str,
    message: str,
    severity: AlertSeverity,
    context: dict
):
    """Send alert to monitoring system."""
    # Slack webhook
    slack_payload = {
        'text': f'*{severity.value.upper()}*: {title}',
        'attachments': [{
            'text': message,
            'fields': [
                {'title': k, 'value': str(v), 'short': True}
                for k, v in context.items()
            ]
        }]
    }

    async with httpx.AsyncClient() as client:
        await client.post(
            'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
            json=slack_payload
        )

# Usage
await send_alert(
    title='High Validation Error Rate',
    message='Validation errors exceed threshold on /api/orders endpoint',
    severity=AlertSeverity.WARNING,
    context={
        'endpoint': '/api/orders',
        'error_rate': '15/sec',
        'time_window': '5 minutes'
    }
)
```

## Dashboards

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Data Validation Monitoring",
    "panels": [
      {
        "title": "Validation Error Rate",
        "targets": [{
          "expr": "rate(validation_errors_total[5m])"
        }],
        "type": "graph"
      },
      {
        "title": "Top Error Fields",
        "targets": [{
          "expr": "topk(10, sum by (field) (validation_errors_total))"
        }],
        "type": "table"
      },
      {
        "title": "Data Completeness",
        "targets": [{
          "expr": "field_completeness_ratio"
        }],
        "type": "heatmap"
      },
      {
        "title": "Validation Duration",
        "targets": [{
          "expr": "histogram_quantile(0.95, validation_duration_seconds)"
        }],
        "type": "graph"
      }
    ]
  }
}
```

### Custom Dashboard

```python
# app/dashboard/validation_dashboard.py
from fastapi import APIRouter
from app.monitoring.error_aggregator import ValidationErrorAggregator

router = APIRouter(prefix="/dashboard")
aggregator = ValidationErrorAggregator()

@router.get("/validation-metrics")
async def get_validation_metrics():
    """Get validation dashboard metrics."""
    return {
        'top_errors': aggregator.get_top_errors(limit=10),
        'error_rate': aggregator.get_error_rate('all'),
        'endpoints': [
            {
                'name': endpoint,
                'error_rate': aggregator.get_error_rate(endpoint)
            }
            for endpoint in ['/api/users', '/api/orders', '/api/products']
        ]
    }
```

## Integration Patterns

### Sentry Integration

```python
# app/monitoring/sentry_integration.py
import sentry_sdk
from pydantic import ValidationError

def track_validation_error_sentry(
    error: ValidationError,
    context: dict
):
    """Send validation errors to Sentry."""
    with sentry_sdk.push_scope() as scope:
        scope.set_tag('error_type', 'validation')
        scope.set_context('validation', {
            'errors': error.errors(),
            'model': error.model.__name__
        })
        scope.set_context('request', context)

        sentry_sdk.capture_exception(error)
```

### DataDog Integration

```python
# app/monitoring/datadog_integration.py
from datadog import statsd

def track_validation_metrics_datadog(
    endpoint: str,
    field: str,
    error_type: str
):
    """Send metrics to DataDog."""
    statsd.increment(
        'validation.errors',
        tags=[
            f'endpoint:{endpoint}',
            f'field:{field}',
            f'error_type:{error_type}'
        ]
    )

def track_validation_duration_datadog(
    endpoint: str,
    duration_ms: float
):
    """Track validation duration."""
    statsd.histogram(
        'validation.duration',
        duration_ms,
        tags=[f'endpoint:{endpoint}']
    )
```

## Quality Rules Engine

### Define Quality Rules

```python
# app/quality/rules.py
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class QualityRule:
    """Data quality rule definition."""
    name: str
    field: str
    check: Callable[[Any], bool]
    severity: str
    message: str

# Example rules
email_domain_rule = QualityRule(
    name='corporate_email_domain',
    field='email',
    check=lambda v: v.endswith('@company.com'),
    severity='warning',
    message='Non-corporate email domain detected'
)

age_range_rule = QualityRule(
    name='reasonable_age',
    field='age',
    check=lambda v: 13 <= v <= 100,
    severity='error',
    message='Age outside reasonable range'
)

class QualityEngine:
    """Execute quality rules on data."""

    def __init__(self, rules: list[QualityRule]):
        self.rules = rules

    def check(self, data: dict) -> list[dict]:
        """Run all rules against data."""
        violations = []

        for rule in self.rules:
            if rule.field in data:
                value = data[rule.field]
                if not rule.check(value):
                    violations.append({
                        'rule': rule.name,
                        'field': rule.field,
                        'severity': rule.severity,
                        'message': rule.message,
                        'value': value
                    })

        return violations
```

## Best Practices

1. **Track Everything**: Log all validation errors with context
2. **Set Thresholds**: Define acceptable error rates per endpoint
3. **Alert Proactively**: Alert before users notice issues
4. **Dashboard Visibility**: Make metrics visible to entire team
5. **Regular Review**: Weekly review of top validation errors
6. **Trend Analysis**: Monitor error trends over time
7. **Root Cause**: Investigate spikes immediately

## Summary

| Aspect | Tools | Purpose |
|--------|-------|---------|
| **Metrics** | Prometheus, DataDog | Track error rates, duration |
| **Logging** | Structlog, Sentry | Detailed error context |
| **Alerting** | Prometheus Alerts, Slack | Proactive notifications |
| **Dashboards** | Grafana, Custom | Visualize data quality |
| **Quality Rules** | Custom Engine | Enforce business rules |

---

**Previous**: [SQLModel Alignment](sqlmodel-alignment.md) | **Index**: [Reference Index](INDEX.md)
