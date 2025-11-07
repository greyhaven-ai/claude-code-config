# Distributed Tracing Investigation

Using Jaeger distributed tracing to identify a microservice bottleneck in checkout flow. Demonstrates how to trace requests across 7 microservices, identify the critical path, and resolve synchronous external API calls causing 3-second delays.

## Investigation Summary

**Issue**: Checkout API p95 latency degraded from 150ms to 3000ms
**Investigation Method**: Jaeger distributed tracing
**Root Cause**: Payment service calling external fraud check API synchronously
**Resolution**: Moved fraud check to async background job
**Impact**: p95 latency 3000ms → 150ms (95% faster)
**Services Involved**: 7 microservices in checkout flow

---

## Problem Statement

### Symptoms

**Performance Degradation**:
```
Checkout API p95 latency:
- Expected: 150ms
- Actual: 3000ms (20x slower)
- When: Last 2 days
- Impact: 15% cart abandonment (vs 8% baseline)
```

**User Impact**:
- Checkout takes 3-5 seconds (was <1 second)
- Users abandoning carts due to slowness
- Support tickets: "Is my payment processing?"
- Conversion rate: 2.5% (vs 4.2% baseline) - 40% drop

**Revenue Impact**:
```
Lost Revenue: ~$25,000 per day
Abandoned Carts: +7% (doubled)
Completion Time: 3-5 seconds (vs <1 second)
```

---

## Microservices Architecture

```
┌──────────────┐
│   Frontend   │ (TanStack Start)
└──────┬───────┘
       │
       v
┌──────────────┐
│  API Gateway │ (Cloudflare Worker)
└──────┬───────┘
       │
       v
┌──────────────┐
│   Checkout   │ ← Main API (3000ms p95)
│   Service    │
└──────┬───────┘
       │
       ├─→ Cart Service (50ms)
       ├─→ Inventory Service (30ms)
       ├─→ Payment Service (2800ms) ← BOTTLENECK
       ├─→ Shipping Service (40ms)
       ├─→ Tax Service (25ms)
       └─→ Notification Service (20ms)

Total: 50 + 30 + 2800 + 40 + 25 + 20 = 2965ms
```

**Question**: Which service is slow? (not obvious from metrics alone)

---

## Investigation with Jaeger

### Step 1: Generate Trace

**Trigger Checkout Request**:
```bash
# Make checkout API call with trace enabled
curl -X POST https://api.greyhaven.io/checkout \
  -H "Content-Type: application/json" \
  -H "X-Trace-ID: trace-$(uuidgen)" \
  -d '{
    "cart_id": "cart-123",
    "payment_method": "card",
    "shipping_address": {...}
  }'

Response:
{
  "order_id": "order-456",
  "total": 149.99,
  "status": "processing"
}

Response Time: 3021ms
Trace ID: trace-550e8400-e29b-41d4-a716-446655440000
```

### Step 2: View Trace in Jaeger

**Open Jaeger UI**:
```
URL: https://jaeger.greyhaven.io
Search: trace-550e8400-e29b-41d4-a716-446655440000
```

**Trace Visualization** (Waterfall View):
```
┌────────────────────────────────────────────────────────────────────┐
│ POST /checkout (3021ms total)                                       │
├────────────────────────────────────────────────────────────────────┤
│  ├─ api-gateway (10ms)                                              │
│  │  ├─ checkout-service (2985ms)                                    │
│  │  │  ├─ cart-service:get-cart (50ms)                              │
│  │  │  ├─ inventory-service:check-stock (30ms)                      │
│  │  │  ├─ payment-service:process-payment (2800ms) ← SLOW!          │
│  │  │  │  ├─ internal:validate-card (15ms)                          │
│  │  │  │  ├─ external:fraud-check-api (2750ms) ← BOTTLENECK!       │
│  │  │  │  └─ internal:charge-card (35ms)                            │
│  │  │  ├─ shipping-service:calculate (40ms)                         │
│  │  │  ├─ tax-service:calculate (25ms)                              │
│  │  │  └─ notification-service:send-email (20ms)                    │
└────────────────────────────────────────────────────────────────────┘

Critical Path: checkout → payment → fraud-check (2750ms of 3021ms = 91%)
```

**Bottleneck Identified**: External fraud check API taking 2750ms (91% of total time)

### Step 3: Analyze Span Details

**Payment Service Span**:
```json
{
  "traceID": "550e8400-e29b-41d4-a716-446655440000",
  "spanID": "1234567890abcdef",
  "operationName": "payment-service:process-payment",
  "startTime": 1702900000000,
  "duration": 2800000,  // 2800ms
  "tags": {
    "span.kind": "server",
    "http.method": "POST",
    "http.url": "/api/payment/process",
    "http.status_code": 200,
    "service": "payment-service"
  },
  "logs": [
    {"timestamp": 1702900000015, "message": "Validating card"},
    {"timestamp": 1702900000030, "message": "Calling fraud check API"},
    {"timestamp": 1702900002780, "message": "Fraud check complete"},  // 2750ms later!
    {"timestamp": 1702900002815, "message": "Charging card"}
  ]
}
```

**Child Span - External API Call**:
```json
{
  "spanID": "fedcba0987654321",
  "parentSpanID": "1234567890abcdef",
  "operationName": "http:POST:fraud-check-api",
  "startTime": 1702900000030,
  "duration": 2750000,  // 2750ms!
  "tags": {
    "span.kind": "client",
    "http.method": "POST",
    "http.url": "https://api.fraudcheck.com/v1/verify",
    "http.status_code": 200,
    "peer.service": "fraud-check-api",
    "external": "true"
  }
}
```

**Root Cause**: Payment service calling external fraud check API **synchronously**, blocking checkout for 2750ms

---

## Root Cause Analysis

### Why Is This Slow?

**Current Flow** (Synchronous):
```
User clicks "Place Order"
  ↓
Checkout validates cart, inventory, etc. (130ms)
  ↓
Payment service START (0ms)
  ├─ Validate card (15ms)
  ├─ Call fraud check API (2750ms) ← BLOCKING!
  │  └─ Wait for external API response
  ├─ Charge card (35ms)
  └─ Return success (2800ms total)
  ↓
Checkout completes remaining steps (55ms)
  ↓
User sees "Order Placed" (3021ms total)
```

**Problem**: Fraud check is synchronous
- Blocks the entire checkout flow
- External API (fraud-check.com) is slow (p95: 2.5 seconds)
- User waits 3+ seconds for order confirmation
- Cart abandonment increases

### Is Fraud Check Critical for Checkout?

**Fraud Check Requirements**:
- Must complete before charging card? **YES** ✅
- Must complete before user sees "Order Placed"? **NO** ❌
- Can be done asynchronously? **YES** ✅

**Better Flow**: Charge card immediately, fraud check in background

---

## Resolution

### Solution: Async Fraud Check

**New Flow** (Asynchronous):
```
User clicks "Place Order"
  ↓
Checkout validates cart, inventory, etc. (130ms)
  ↓
Payment service START (0ms)
  ├─ Validate card (15ms)
  ├─ Charge card (35ms) ← No blocking
  ├─ Queue fraud check job (5ms) ← Background
  └─ Return success (55ms total) ← Fast!
  ↓
Checkout completes remaining steps (55ms)
  ↓
User sees "Order Placed" (240ms total) ← 12x faster!

MEANWHILE (background):
Fraud check worker picks up job
  ↓
Call fraud check API (2750ms)
  ↓
If fraud detected:
  ├─ Void transaction
  ├─ Email customer
  └─ Cancel order
Else:
  └─ Mark order as verified
```

**Benefits**:
- User sees "Order Placed" in 240ms (vs 3021ms)
- Fraud check still happens (just asynchronously)
- If fraud detected, we void transaction and notify customer
- p95 latency: 3000ms → 150ms (95% faster)

### Code Changes

**Before** (Synchronous):
```typescript
// payment-service/src/process-payment.ts
export async function processPayment(order: Order): Promise<PaymentResult> {
  // Validate card
  await validateCard(order.payment_method);

  // ❌ BLOCKING: Wait for fraud check
  const fraudCheck = await callFraudCheckAPI(order);
  if (fraudCheck.isFraud) {
    throw new Error('Fraud detected');
  }

  // Charge card
  const charge = await chargeCard(order);

  return { success: true, charge_id: charge.id };
}
```

**After** (Asynchronous):
```typescript
// payment-service/src/process-payment.ts
export async function processPayment(order: Order): Promise<PaymentResult> {
  // Validate card
  await validateCard(order.payment_method);

  // ✅ NON-BLOCKING: Charge card immediately
  const charge = await chargeCard(order);

  // ✅ Queue fraud check for background processing
  await queueFraudCheckJob({
    order_id: order.id,
    charge_id: charge.id,
    payment_method: order.payment_method
  });

  return { success: true, charge_id: charge.id };
}

// Background worker processes fraud checks
// fraud-worker/src/process-fraud-check.ts
export async function processFraudCheck(job: FraudCheckJob) {
  const fraudCheck = await callFraudCheckAPI(job);

  if (fraudCheck.isFraud) {
    // Void the charge
    await voidCharge(job.charge_id);

    // Cancel the order
    await cancelOrder(job.order_id, 'Fraud detected');

    // Notify customer
    await sendEmail(job.order_id, 'order-cancelled-fraud');
  } else {
    // Mark order as verified
    await markOrderVerified(job.order_id);
  }
}
```

### Deployment

**Background Worker**:
```bash
# Deploy fraud check worker (BullMQ worker)
docker build -t fraud-worker:v1.0.0 .
docker push ghcr.io/greyhaven/fraud-worker:v1.0.0

kubectl apply -f k8s/fraud-worker-deployment.yaml

# Worker config
replicas: 3
queue: fraud-checks
concurrency: 10
retry: 3 times with exponential backoff
```

**Payment Service Update**:
```bash
# Deploy updated payment service (async fraud check)
git checkout feature/async-fraud-check
npm run build
docker build -t payment-service:v2.5.0 .

# Canary deployment (10% → 100%)
kubectl set image deployment/payment-service payment=ghcr.io/greyhaven/payment:v2.5.0
kubectl rollout status deployment/payment-service
```

---

## Results

### Before vs After Metrics

| Metric | Before (Sync) | After (Async) | Improvement |
|--------|--------------|---------------|-------------|
| **p50 Latency** | 2500ms | 120ms | **95% faster** |
| **p95 Latency** | 3000ms | 150ms | **95% faster** |
| **p99 Latency** | 3500ms | 200ms | **94% faster** |
| **Fraud Detection** | 100% (before charge) | 99.9% (after charge) | -0.1% (acceptable) |
| **Cart Abandonment** | 15% | 8% | **47% reduction** |
| **Conversion Rate** | 2.5% | 4.1% | **64% increase** |
| **Revenue Impact** | -$25K/day | +$0 | **$25K/day saved** |

### Jaeger Trace After Fix

**New Trace Visualization**:
```
┌────────────────────────────────────────────────────────────────────┐
│ POST /checkout (240ms total) ← 12x faster!                         │
├────────────────────────────────────────────────────────────────────┤
│  ├─ api-gateway (10ms)                                              │
│  │  ├─ checkout-service (205ms)                                     │
│  │  │  ├─ cart-service:get-cart (50ms)                              │
│  │  │  ├─ inventory-service:check-stock (30ms)                      │
│  │  │  ├─ payment-service:process-payment (55ms) ← Fast!            │
│  │  │  │  ├─ internal:validate-card (15ms)                          │
│  │  │  │  ├─ internal:charge-card (35ms)                            │
│  │  │  │  └─ queue:fraud-check-job (5ms) ← Async!                   │
│  │  │  ├─ shipping-service:calculate (40ms)                         │
│  │  │  ├─ tax-service:calculate (25ms)                              │
│  │  │  └─ notification-service:send-email (20ms)                    │
└────────────────────────────────────────────────────────────────────┘

BACKGROUND (not in critical path):
┌────────────────────────────────────────────────────────────────────┐
│ fraud-worker:process-fraud-check (2780ms) ← Async!                 │
├────────────────────────────────────────────────────────────────────┤
│  ├─ queue:dequeue (5ms)                                             │
│  ├─ external:fraud-check-api (2750ms) ← Still slow, but not blocking│
│  └─ internal:mark-verified (25ms)                                   │
└────────────────────────────────────────────────────────────────────┘
```

---

## Key Learnings

### Distributed Tracing Benefits

1. **Critical Path Identification**: Instantly see which service is slow
2. **Span-Level Details**: Exact operation and duration
3. **External Dependencies**: Easy to spot slow external APIs
4. **Async Opportunities**: Identify blocking calls that could be async
5. **Before/After Comparison**: Verify improvements with new traces

### When to Use Async Processing

**Good candidates for async**:
- ✅ Non-critical path operations (fraud check after charge)
- ✅ External API calls (especially slow ones)
- ✅ Batch processing (email notifications, analytics)
- ✅ Background tasks (image resizing, report generation)

**Keep synchronous**:
- ❌ Critical validations (card validation before charge)
- ❌ User-facing errors (payment declined)
- ❌ Data consistency requirements (inventory check before purchase)

### Jaeger Best Practices

1. **Instrument All Services**: Include all microservices in trace
2. **Tag External Calls**: Mark external APIs with `external: true`
3. **Log Key Events**: Add logs to spans for debugging
4. **Sampling Strategy**: 100% for errors, 1% for success (reduce overhead)
5. **Trace ID Propagation**: Pass trace ID through all services

---

## Prevention Measures

### Immediate Actions

- [x] Moved fraud check to async background job
- [x] Deployed fraud worker with BullMQ
- [x] Added Jaeger tracing to all microservices

### Short-Term Actions

- [x] Performance budget: p95 < 500ms for checkout
- [x] Automated alerts for critical path latency >1s
- [x] Async-first architecture review (identify more opportunities)

### Long-Term Actions

- [x] Service mesh (Istio) for automatic distributed tracing
- [x] Chaos engineering: inject latency to test async resilience
- [x] Architectural decision record: synchronous vs asynchronous guidelines

---

## Related Documentation

- **Jaeger Documentation**: [jaegertracing.io/docs](https://www.jaegertracing.io/docs/)
- **OpenTelemetry**: [opentelemetry.io](https://opentelemetry.io/)
- **Async Processing Patterns**: [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
- **BullMQ (Background Jobs)**: [docs.bullmq.io](https://docs.bullmq.io/)

---

Return to [examples index](INDEX.md)
