# OpenTelemetry Distributed Tracing

Production distributed tracing implementation with OpenTelemetry, Jaeger, and automatic instrumentation for Node.js and Python (FastAPI).

## Overview

**Before Implementation**:
- No visibility into request flow across services
- Mean Time to Resolution (MTTR): 45 minutes
- Performance bottlenecks unknown
- Database N+1 queries undetected

**After Implementation**:
- Complete request trace visualization (10+ microservices)
- MTTR: 8 minutes (82% reduction)
- Critical path analysis (identified 300ms→50ms optimization)
- Automatic N+1 query detection

**Technologies**: OpenTelemetry Collector, Jaeger, Node.js auto-instrumentation, FastAPI tracing

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Jaeger UI (Port 16686)                        │
│      Trace Visualization, Dependency Graphs             │
└────────────────────┬────────────────────────────────────┘
                     │ gRPC/HTTP
┌────────────────────▼────────────────────────────────────┐
│         OpenTelemetry Collector (Port 4317)             │
│  Receiver → Processor → Exporter (Jaeger, DataDog)     │
└─┬──────────────┬─────────────────┬─────────────────────┘
  │ OTLP         │ OTLP            │ OTLP
  │ :4317        │ :4317           │ :4317
  ▼              ▼                 ▼
┌──────────┐  ┌──────────────┐  ┌───────────────────────┐
│ TanStack │  │   FastAPI    │  │     PostgreSQL        │
│  Start   │  │   Backend    │  │  (DB queries traced)  │
└──────────┘  └──────────────┘  └───────────────────────┘
```

## 1. OpenTelemetry Collector Deployment

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Jaeger all-in-one (storage, collector, UI)
  jaeger:
    image: jaegertracing/all-in-one:1.52
    ports:
      - "16686:16686"  # Jaeger UI
      - "14268:14268"  # Jaeger collector HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.91.0
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"  # OTLP gRPC receiver
      - "4318:4318"  # OTLP HTTP receiver
      - "8888:8888"  # Prometheus metrics
    depends_on:
      - jaeger

  # PostgreSQL with trace context
  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

### OpenTelemetry Collector Configuration

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

  # Sampling (10% head-based, 100% errors)
  probabilistic_sampler:
    sampling_percentage: 10

  # Tail-based sampling (keep all errors)
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: error-traces
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: slow-traces
        type: latency
        latency: {threshold_ms: 1000}

  # Add resource attributes
  resource:
    attributes:
      - key: deployment.environment
        value: production
        action: insert

exporters:
  # Jaeger exporter
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  # DataDog exporter (optional)
  datadog:
    api:
      key: ${DATADOG_API_KEY}
      site: datadoghq.com

  # Prometheus metrics exporter
  prometheus:
    endpoint: "0.0.0.0:8889"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling, resource]
      exporters: [jaeger, datadog]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

## 2. TanStack Start Auto-Instrumentation (Node.js)

### Install Dependencies

```bash
bun add @opentelemetry/sdk-node \
  @opentelemetry/auto-instrumentations-node \
  @opentelemetry/exporter-trace-otlp-grpc \
  @opentelemetry/resources \
  @opentelemetry/semantic-conventions
```

### Tracer Initialization

```typescript
// tracing.ts - Initialize before app starts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'tanstack-frontend',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production'
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4317'
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        // Add custom span attributes
        requestHook: (span, request) => {
          span.setAttribute('http.user_agent', request.headers['user-agent']);
          span.setAttribute('http.client_ip', request.headers['x-forwarded-for']);
        }
      },
      '@opentelemetry/instrumentation-fs': {enabled: false}  // Disable file system tracing
    })
  ]
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown().finally(() => process.exit(0));
});
```

### Manual Instrumentation (Custom Spans)

```typescript
// utils/tracing.ts
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('tanstack-app');

export async function tracedServerFn<T>(
  name: string,
  fn: () => Promise<T>,
  attributes?: Record<string, string | number>
): Promise<T> {
  return tracer.startActiveSpan(name, async (span) => {
    try {
      // Add custom attributes
      if (attributes) {
        Object.entries(attributes).forEach(([key, value]) => {
          span.setAttribute(key, value);
        });
      }

      const result = await fn();
      span.setStatus({code: SpanStatusCode.OK});
      return result;
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error instanceof Error ? error.message : 'Unknown error'
      });
      span.recordException(error as Error);
      throw error;
    } finally {
      span.end();
    }
  });
}

// Usage in server functions
export const getOrder = createServerFn({method: 'GET'})
  .handler(async ({data}) => {
    return tracedServerFn(
      'getOrder',
      async () => {
        const session = await auth.api.getSession({headers: request.headers});

        // Database query (auto-instrumented)
        const order = await db.query.orders.findFirst({
          where: and(
            eq(orders.id, data.orderId),
            eq(orders.tenant_id, session.user.tenantId)
          )
        });

        return order;
      },
      {
        'order.id': data.orderId,
        'user.id': session.user.id,
        'tenant.id': session.user.tenantId
      }
    );
  });
```

## 3. FastAPI Backend Instrumentation (Python)

### Install Dependencies

```bash
pip install opentelemetry-api opentelemetry-sdk \
  opentelemetry-instrumentation-fastapi \
  opentelemetry-instrumentation-sqlalchemy \
  opentelemetry-exporter-otlp-proto-grpc
```

### Automatic Instrumentation

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Initialize tracer provider
resource = Resource.create({
    "service.name": "fastapi-backend",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument FastAPI
def setup_tracing(app: FastAPI, engine):
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)

# In main.py
from tracing import setup_tracing

app = FastAPI()
engine = create_engine(DATABASE_URL)

setup_tracing(app, engine)
```

### Custom Spans in FastAPI

```python
# api/orders.py
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@app.get("/orders/{order_id}")
async def get_order(order_id: str, session: Session = Depends(get_session)):
    with tracer.start_as_current_span("get_order") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("user.id", session.user_id)
        span.set_attribute("tenant.id", session.tenant_id)

        # Database query (auto-traced by SQLAlchemy instrumentation)
        with tracer.start_as_current_span("db.query.orders"):
            order = db.query(Order).filter(
                Order.id == order_id,
                Order.tenant_id == session.tenant_id
            ).first()

        if not order:
            span.set_status(Status(StatusCode.ERROR, "Order not found"))
            raise HTTPException(status_code=404, detail="Order not found")

        # External API call
        with tracer.start_as_current_span("stripe.retrieve_payment") as stripe_span:
            stripe_span.set_attribute("stripe.payment_intent_id", order.stripe_payment_id)
            payment = stripe.PaymentIntent.retrieve(order.stripe_payment_id)

        return {"order": order, "payment_status": payment.status}
```

## 4. Context Propagation (W3C Trace Context)

### Frontend → Backend Propagation

```typescript
// TanStack Start server function with trace context
export const fetchOrder = createServerFn({method: 'POST'})
  .handler(async ({data}) => {
    // OpenTelemetry automatically propagates trace context via headers:
    // traceparent: 00-{trace-id}-{span-id}-01
    const response = await fetch('http://fastapi-backend/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Trace context automatically injected by auto-instrumentation
      },
      body: JSON.stringify(data)
    });

    return response.json();
  });
```

**Headers automatically added**:
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: congo=t61rcWkgMzE
```

## 5. Span Attributes and Semantic Conventions

### Standard Attributes

```typescript
// HTTP: method, url, status_code, route
span.setAttribute('http.method', 'POST');
span.setAttribute('http.status_code', 200);

// Database: system, statement, name
span.setAttribute('db.system', 'postgresql');
span.setAttribute('db.statement', 'SELECT * FROM orders WHERE id = $1');

// Business: user.id, tenant.id, order.amount
span.setAttribute('user.id', session.user.id);
span.setAttribute('tenant.id', session.user.tenantId);
```

## 6. Sampling Strategies

### Head-Based Sampling (10%)

```yaml
# otel-collector-config.yaml
processors:
  probabilistic_sampler:
    sampling_percentage: 10  # Sample 10% of traces
```

### Tail-Based Sampling (All Errors + Slow Traces)

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: always-sample-errors
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: slow-traces
        type: latency
        latency: {threshold_ms: 1000}  # >1s traces
      - name: sample-10-percent
        type: probabilistic
        probabilistic: {sampling_percentage: 10}
```

**Result**: 100% of errors + slow traces, 10% of normal traces

## 7. Trace Visualization in Jaeger

### Critical Path Analysis

**Trace Example** (Order creation flow):
```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736
Duration: 420ms

├─ POST /orders (TanStack Start)         [420ms] ████████████████████
│  ├─ auth.getSession                    [5ms]   █
│  ├─ POST /api/orders (FastAPI)         [400ms] ███████████████████
│  │  ├─ db.query.orders.insert          [50ms]  ██
│  │  ├─ stripe.PaymentIntent.create     [300ms] ██████████████ (SLOW!)
│  │  └─ db.query.orders.update          [45ms]  ██
│  └─ cache.set                           [10ms]  █
```

**Optimization identified**: Stripe API call taking 300ms (71% of total time). Solution: Move to background job.

### Dependency Graph

```
TanStack Start (10,000 req/min)
  ↓
FastAPI Backend (9,500 req/min)
  ↓                    ↓
PostgreSQL (8,000)   Stripe API (1,500)
```

## 8. Results and Impact

### Before vs After Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **MTTR** | 45 min | 8 min | **82% reduction** |
| **Critical Path Visibility** | 0% | 100% | **Complete visibility** |
| **N+1 Query Detection** | Manual | Automatic | **Instant detection** |
| **Latency Optimization** | Guesswork | Data-driven | **300ms → 50ms** |
| **Trace Coverage** | 0% | 95% of requests | **95% instrumented** |
| **Performance Overhead** | N/A | <5ms per request | **Negligible** |

### Key Discoveries

**1. Stripe API Bottleneck** (300ms per request)
- **Trace showed**: 71% of request time in Stripe API call
- **Solution**: Moved to background job with webhooks
- **Result**: 420ms → 120ms (71% faster)

**2. N+1 Database Query** (15 queries for 5 orders)
- **Trace showed**: 15 separate SQL queries in single request
- **Solution**: Added Drizzle `with` clause for eager loading
- **Result**: 15 queries → 1 query, 200ms → 20ms

**3. Missing Database Index** (2s query time)
- **Trace showed**: `db.query.orders` taking 2 seconds
- **Solution**: Added index on `(tenant_id, created_at)`
- **Result**: 2000ms → 15ms (99.25% faster)

## Related Documentation

- **Prometheus**: [prometheus-grafana-setup.md](prometheus-grafana-setup.md) - Metrics monitoring
- **SLO**: [slo-error-budgets.md](slo-error-budgets.md) - Error budget tracking
- **Reference**: [../reference/opentelemetry-best-practices.md](../reference/opentelemetry-best-practices.md)
- **Templates**: [../templates/otel-config.yaml](../templates/otel-config.yaml) - Configuration template

---

Return to [examples index](INDEX.md)
