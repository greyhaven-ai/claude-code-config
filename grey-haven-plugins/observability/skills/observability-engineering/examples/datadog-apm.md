# DataDog APM Integration

Commercial Application Performance Monitoring (APM) for Grey Haven stack with Real User Monitoring (RUM), custom metrics, and synthetic monitoring.

## Overview

**Before Implementation**:
- No production visibility into user experience
- Incident detection via user complaints (30+ min delay)
- No business metrics tracking (conversion rates, revenue)
- Manual log analysis (45 min MTTR)

**After Implementation**:
- Real User Monitoring (RUM) for frontend performance
- Automatic error tracking with stack traces
- Business KPIs on exec dashboard (revenue/minute, checkout funnel)
- MTTR reduced from 45 min → 5 min (89% improvement)
- 99.5% → 99.95% availability (10x fewer incidents)

**Technologies**: DataDog Agent, APM traces, RUM, Synthetic Monitoring, Custom Metrics

**Cost**: $31/host/month + $40/million spans (~$150/month for startup)

## 1. DataDog Agent Deployment

### Cloudflare Workers Integration

```typescript
// worker.ts - DataDog metrics for Cloudflare Workers
import { Hono } from 'hono';

const app = new Hono();

// DataDog endpoint
const DD_API_URL = 'https://http-intake.logs.datadoghq.com/api/v2/logs';
const DD_API_KEY = process.env.DD_API_KEY!;

async function sendMetric(metric: {
  metric: string;
  value: number;
  tags?: string[];
}) {
  const payload = {
    ddsource: 'cloudflare-workers',
    service: 'tanstack-frontend',
    hostname: 'cloudflare-worker',
    message: JSON.stringify(metric),
    ddtags: metric.tags?.join(',')
  };

  await fetch(DD_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'DD-API-KEY': DD_API_KEY
    },
    body: JSON.stringify(payload)
  });
}

app.use('*', async (c, next) => {
  const start = Date.now();

  try {
    await next();

    const duration = Date.now() - start;

    // Send metrics to DataDog
    await sendMetric({
      metric: 'cloudflare.request.duration',
      value: duration,
      tags: [
        `route:${c.req.path}`,
        `method:${c.req.method}`,
        `status:${c.res.status}`
      ]
    });
  } catch (error) {
    // Track errors
    await sendMetric({
      metric: 'cloudflare.request.error',
      value: 1,
      tags: [`error:${error.message}`]
    });
    throw error;
  }
});

export default app;
```

### FastAPI Backend Agent

```python
# main.py - DataDog APM for FastAPI
from ddtrace import tracer, patch_all
import ddtrace

patch_all()  # Auto-instrument all libraries
ddtrace.config.env = 'production'
ddtrace.config.service = 'fastapi-backend'

app = FastAPI()

@app.post("/orders")
async def create_order(order: OrderCreate):
    with tracer.trace("create_order") as span:
        span.set_tag("order.amount", order.amount)
        span.set_tag("user.id", order.user_id)
        span.set_tag("tenant.id", order.tenant_id)
        span.set_metric("order.revenue", order.amount / 100)

        db_order = await create_order_in_db(order)  # Auto-traced
        payment = await stripe.PaymentIntent.create(amount=order.amount)

        return {"order_id": db_order.id}
```

## 2. Real User Monitoring (RUM)

### Frontend Integration (TanStack Start)

```typescript
// app/root.tsx - DataDog RUM initialization
import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
  applicationId: 'YOUR_APP_ID',
  clientToken: 'YOUR_CLIENT_TOKEN',
  site: 'datadoghq.com',
  service: 'tanstack-frontend',
  env: 'production',
  version: '1.0.0',
  sessionSampleRate: 100,  // 100% of sessions
  sessionReplaySampleRate: 20,  // 20% session replays
  trackUserInteractions: true,
  trackResources: true,
  trackLongTasks: true,
  defaultPrivacyLevel: 'mask-user-input'  // GDPR compliance
});

// Track user context
datadogRum.setUser({
  id: user.id,
  email: user.email,  // ❌ Remove if PII concern
  tenant_id: user.tenantId
});

// Custom RUM events
function trackCheckoutStep(step: string) {
  datadogRum.addAction('checkout_step', {
    step,
    cart_value: cartTotal,
    items_count: cartItems.length
  });
}

// Error tracking with context
try {
  await createOrder(orderData);
} catch (error) {
  datadogRum.addError(error, {
    order_amount: orderData.amount,
    user_id: user.id,
    tenant_id: user.tenantId
  });
  throw error;
}
```

### Performance Metrics

```typescript
// Track Web Vitals
import { onCLS, onFID, onLCP } from 'web-vitals';

onCLS((metric) => {
  datadogRum.addAction('web_vital_cls', {value: metric.value});
});

onFID((metric) => {
  datadogRum.addAction('web_vital_fid', {value: metric.value});
});

onLCP((metric) => {
  datadogRum.addAction('web_vital_lcp', {value: metric.value});
});
```

## 3. Custom Business Metrics

### Revenue Per Minute

```python
# metrics.py
from datadog import statsd

@app.post("/orders")
async def create_order(order: OrderCreate):
    # Increment order count
    statsd.increment('orders.created', tags=[
        f'tenant_id:{order.tenant_id}',
        'payment_method:stripe'
    ])

    # Track revenue
    statsd.histogram('orders.revenue', order.amount / 100, tags=[
        f'tenant_id:{order.tenant_id}'
    ])

    # Track checkout funnel
    statsd.increment('checkout.funnel.completed', tags=[
        f'step:payment',
        f'tenant_id:{order.tenant_id}'
    ])
```

### Checkout Funnel Tracking

```typescript
// Track multi-step funnel
const funnel = ['cart', 'shipping', 'payment', 'confirmation'];

funnel.forEach((step, index) => {
  datadogRum.addAction('checkout_funnel', {
    step,
    step_number: index + 1,
    cart_value: cartTotal
  });
});

// Calculate conversion rate in DataDog
// Query: sum:checkout.funnel.completed{step:confirmation} / sum:checkout.funnel.completed{step:cart}
```

## 4. APM Traces with Distributed Context

### Trace Correlation (Frontend → Backend)

```typescript
// TanStack Start server function
export const createOrder = createServerFn({method: 'POST'})
  .handler(async ({data}) => {
    // DataDog automatically injects trace context
    const response = await fetch('http://fastapi-backend/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // x-datadog-trace-id, x-datadog-parent-id automatically injected
      },
      body: JSON.stringify(data)
    });

    return response.json();
  });
```

**Headers injected**:
```
x-datadog-trace-id: 1234567890123456789
x-datadog-parent-id: 9876543210987654321
x-datadog-sampling-priority: 1
```

### Log Correlation

```python
# logging_config.py - Correlate logs with traces
import logging
from ddtrace import tracer

logger = logging.getLogger(__name__)

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    # Get current trace context
    span = tracer.current_span()

    logger.info(
        f"Fetching order {order_id}",
        extra={
            'dd.trace_id': span.trace_id,
            'dd.span_id': span.span_id,
            'order_id': order_id
        }
    )
```

## 5. Synthetic Monitoring

### API Health Checks

```json
{
  "name": "API Health Check - Production",
  "type": "api",
  "config": {
    "request": {"method": "GET", "url": "https://api.greyhaven.io/health"},
    "assertions": [
      {"type": "statusCode", "target": 200},
      {"type": "responseTime", "operator": "lessThan", "target": 500}
    ]
  },
  "locations": ["aws:us-east-1", "aws:eu-west-1"],
  "options": {"tick_every": 60}
}
```

### Critical User Journey Test

```javascript
// synthetic-checkout-test.js - Browser test
describe('Checkout Flow', () => {
  it('completes order successfully', async () => {
    await browser.get('https://app.greyhaven.io/products/123');
    await browser.findElement(By.id('add-to-cart')).click();
    await browser.findElement(By.id('checkout')).click();
    await browser.findElement(By.id('email')).sendKeys('test@example.com');
    await browser.findElement(By.id('card-number')).sendKeys('4242424242424242');
    await browser.findElement(By.id('submit-payment')).click();

    const confirmation = await browser.findElement(By.id('order-confirmation')).getText();
    assert.include(confirmation, 'Order successful');
  });
});
```

**Run**: Every 5 min from 3 locations. **Alert**: 2 consecutive failures or >2s response time.

## 6. Anomaly Detection

### ML-Powered Alerts

```yaml
# DataDog Monitor - Anomaly Detection
name: "Anomaly: Elevated Error Rate"
type: "metric alert"
query: "anomalies(sum:trace.web.request.errors{service:fastapi-backend}.as_count(), 'agile', 2)"
message: |
  **Anomaly detected**: Error rate is {{value}} ({{value_percent}}% above baseline)

  **Baseline**: {{threshold}} errors/min
  **Current**: {{value}} errors/min

  **Potential causes**:
  - Database connection issues
  - Stripe API degradation
  - Recent deployment

  @pagerduty-critical
```

### Forecasting

```python
# DataDog API - Query forecast
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

config = Configuration()
api = MetricsApi(ApiClient(config))

response = api.query_metrics(
    from_=int(time.time()) - 86400,  # Last 24 hours
    to=int(time.time()),
    query='forecast(sum:orders.revenue{*}.rollup(sum, 3600), "linear", 1)'  # Forecast next hour
)

print(f"Predicted revenue next hour: ${response['series'][0]['pointlist'][-1][1]}")
```

## 7. DataDog Dashboard

```json
{
  "title": "Grey Haven - Executive Dashboard",
  "widgets": [
    {"definition": {"type": "timeseries", "requests": [{"q": "sum:orders.revenue{*}.rollup(sum, 60)"}], "title": "Revenue per Minute"}},
    {"definition": {"type": "query_value", "requests": [{"q": "sum:checkout.funnel.completed{step:confirmation}.as_count() / sum:checkout.funnel.completed{step:cart}.as_count()"}], "title": "Checkout Conversion Rate"}},
    {"definition": {"type": "toplist", "requests": [{"q": "top(avg:trace.web.request.duration{service:fastapi-backend} by {resource_name}, 10, 'mean', 'desc')"}], "title": "Slowest Endpoints"}},
    {"definition": {"type": "heatmap", "requests": [{"q": "avg:rum.view.loading_time{*}"}], "title": "Page Load Time Distribution"}}
  ]
}
```

## 8. Cost Optimization

### Sampling Strategy

```python
# Sample 25% of traces, 100% of errors
from ddtrace.sampler import RateSampler, RateByServiceSampler

# Default: 25% sampling
tracer.configure(sampler=RateSampler(sample_rate=0.25))

# Always sample errors
@app.middleware("http")
async def sample_errors(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception:
        # Force sampling for errors
        span = tracer.current_span()
        span.set_tag('manual.keep', 'true')
        raise
```

**Result**: $40/million spans → $10/million spans (75% cost reduction)

## 9. Results and Impact

### Before vs After Metrics

| Metric | Before DataDog | After DataDog | Impact |
|--------|---------------|---------------|--------|
| **MTTR** | 45 min | 5 min | **89% reduction** |
| **Incident Detection** | User reports (30+ min) | Automatic (2 min) | **93% faster** |
| **Availability** | 99.5% | 99.95% | **10x fewer incidents** |
| **Business Visibility** | None | Real-time revenue/min | **Executive dashboards** |
| **User Experience** | Unknown | LCP p75: 1.2s | **Web Vitals tracked** |
| **Cost** | $0 | $150/month | **ROI: 10x (saved 40h/month)** |

### Key Discoveries

**1. Session Replay Identified UX Bug**
- RUM session replay showed users clicking submit button 5+ times
- Root cause: No loading state on button
- Fix: Added spinner + disabled state
- Result: Checkout completion rate 68% → 82%

**2. Anomaly Detection Prevented Outage**
- ML alert: "Error rate 3x above baseline" at 2 AM
- Investigation: Database connection pool exhaustion
- Fix: Increased pool size before business hours
- Result: Prevented 99.95% SLO violation

**3. Revenue Dashboard Drove Product Decisions**
- Real-time revenue tracking showed 30% drop on Sundays
- Product decision: Sunday-only promotions
- Result: 30% → 10% drop in Sunday revenue

## Related Documentation

- **Prometheus**: [prometheus-grafana-setup.md](prometheus-grafana-setup.md) - Open-source alternative
- **OpenTelemetry**: [opentelemetry-tracing.md](opentelemetry-tracing.md) - Vendor-neutral tracing
- **SLO**: [slo-error-budgets.md](slo-error-budgets.md) - Error budget tracking
- **Reference**: [../reference/apm-comparison.md](../reference/apm-comparison.md) - APM vendor comparison

---

Return to [examples index](INDEX.md)
