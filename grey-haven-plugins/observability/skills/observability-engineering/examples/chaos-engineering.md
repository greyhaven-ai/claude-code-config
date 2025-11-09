# Chaos Engineering with Gremlin

Reliability testing and circuit breaker validation for Grey Haven microservices using Gremlin chaos experiments.

## Overview

**Before Chaos Engineering**:
- Untested failure scenarios (database outage, network latency)
- Unknown system behavior under stress
- Incident response procedures untested
- Circuit breakers never validated

**After Chaos Engineering**:
- 3 critical bugs found before production deployment
- Circuit breaker engages in 2 seconds (99.8% fallback success)
- Incident response time: 45 min → 8 min (82% reduction)
- Confidence in system resilience: 40% → 95%

**Technologies**: Gremlin Agent, Kubernetes attacks, Circuit breakers (resilience4j), Prometheus monitoring

**Cost**: $1,500/month (Gremlin Team plan)

## 1. Gremlin Setup

### Agent Deployment (Kubernetes)

```bash
# Add Gremlin Helm repository
helm repo add gremlin https://helm.gremlin.com
helm repo update

# Install Gremlin agent
helm install gremlin gremlin/gremlin \
  --namespace gremlin \
  --create-namespace \
  --set gremlin.secret.managed=true \
  --set gremlin.secret.type=secret \
  --set gremlin.secret.teamID=$GREMLIN_TEAM_ID \
  --set gremlin.secret.teamSecret=$GREMLIN_TEAM_SECRET
```

### Blast Radius Configuration

```yaml
# gremlin-config.yaml - Limit chaos to staging namespace
apiVersion: v1
kind: ConfigMap
metadata:
  name: gremlin-config
  namespace: gremlin
data:
  config.yaml: |
    blast_radius:
      # Only target staging environment
      namespaces: ["staging"]
      labels:
        environment: "staging"
        chaos-enabled: "true"

    # Protect production and critical services
    protected:
      namespaces: ["production", "kube-system"]
      labels:
        chaos-enabled: "false"
```

## 2. Circuit Breaker Implementation

### TypeScript (TanStack Start)

```typescript
// utils/circuit-breaker.ts
import CircuitBreaker from 'opossum';

const circuitBreakerOptions = {
  timeout: 3000,  // 3s timeout
  errorThresholdPercentage: 50,  // Open circuit if >50% errors
  resetTimeout: 30000,  // Retry after 30s
  rollingCountTimeout: 10000,  // 10s rolling window
  rollingCountBuckets: 10
};

// Circuit breaker for Stripe API calls
const stripeBreaker = new CircuitBreaker(
  async (amount: number) => {
    const response = await fetch('https://api.stripe.com/v1/payment_intents', {
      method: 'POST',
      headers: {'Authorization': `Bearer ${process.env.STRIPE_SECRET_KEY}`},
      body: JSON.stringify({amount, currency: 'usd'})
    });

    if (!response.ok) throw new Error('Stripe API error');
    return response.json();
  },
  circuitBreakerOptions
);

// Fallback when circuit opens
stripeBreaker.fallback(() => {
  logger.warn('Circuit breaker OPEN - using fallback');
  return {
    id: 'fallback-payment-intent',
    status: 'requires_payment_method',
    fallback: true
  };
});

// Monitor circuit breaker state
stripeBreaker.on('open', () => {
  logger.error('Circuit breaker OPEN');
  prometheusMetrics.circuitBreakerState.set({service: 'stripe'}, 1);
});

stripeBreaker.on('halfOpen', () => {
  logger.warn('Circuit breaker HALF-OPEN');
  prometheusMetrics.circuitBreakerState.set({service: 'stripe'}, 0.5);
});

stripeBreaker.on('close', () => {
  logger.info('Circuit breaker CLOSED');
  prometheusMetrics.circuitBreakerState.set({service: 'stripe'}, 0);
});

// Usage
export const createPayment = createServerFn({method: 'POST'})
  .handler(async ({data}) => {
    try {
      return await stripeBreaker.fire(data.amount);
    } catch (error) {
      if (stripeBreaker.opened) {
        // Circuit is open, use fallback
        return stripeBreaker.fallback();
      }
      throw error;
    }
  });
```

### Python (FastAPI)

```python
# circuit_breaker.py
from pybreaker import CircuitBreaker
import prometheus_client

stripe_breaker = CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    timeout_duration=30,  # Reset after 30s
    expected_exception=Exception
)

circuit_breaker_state = prometheus_client.Gauge(
    'circuit_breaker_state',
    'Circuit breaker state (0=closed, 0.5=half-open, 1=open)',
    ['service']
)

@stripe_breaker
async def create_stripe_payment(amount: int):
    response = await stripe.PaymentIntent.create(amount=amount, currency='usd')
    return response

@app.post("/payments")
async def create_payment(payment: PaymentCreate):
    try:
        result = await create_stripe_payment(payment.amount)
        return result
    except CircuitOpenException:
        logger.warning("Circuit breaker OPEN - using fallback")
        circuit_breaker_state.labels(service='stripe').set(1)

        # Fallback: Queue payment for later processing
        await queue_payment(payment)
        return {"status": "queued", "message": "Payment queued for processing"}
```

## 3. Chaos Experiments

### Experiment 1: Pod Termination (50% Failure)

**Hypothesis**: "API handles 50% pod failures without user impact"

```json
{
  "name": "Pod Termination - 50% Failure",
  "description": "Kill 50% of FastAPI pods to test resilience",
  "type": "attack",
  "target": {
    "type": "kubernetes",
    "namespace": "staging",
    "labels": {"app": "fastapi-backend"},
    "percentage": 50
  },
  "attack": {
    "type": "shutdown",
    "args": {
      "delay": 5
    }
  }
}
```

**Validation Metrics**:
```promql
# HTTP error rate during experiment
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))

# Expected: <1% error rate (requests routed to healthy pods)
```

**Result**:
- ✅ Error rate: 0.2% (within SLO)
- ✅ Kubernetes automatically routed traffic to healthy pods
- ✅ No user-facing impact

### Experiment 2: Network Latency (100ms → 500ms)

**Hypothesis**: "System maintains p95 latency < 1s with 500ms network delay"

```json
{
  "name": "Network Latency - 500ms delay",
  "type": "attack",
  "target": {
    "type": "kubernetes",
    "namespace": "staging",
    "labels": {"app": "fastapi-backend"}
  },
  "attack": {
    "type": "latency",
    "args": {
      "delay": 500,
      "protocol": "tcp",
      "port": 8000
    }
  }
}
```

**Result**:
- ❌ p95 latency: 1.2s (exceeded 1s threshold)
- **Issue found**: Synchronous Stripe API calls (300ms baseline + 500ms delay = 800ms)
- **Fix**: Moved Stripe calls to background job with webhooks
- **Retest**: p95 latency: 600ms ✅

### Experiment 3: CPU Stress (80% Utilization)

**Hypothesis**: "Application remains responsive at 80% CPU"

```json
{
  "name": "CPU Stress - 80% utilization",
  "type": "attack",
  "target": {
    "type": "kubernetes",
    "namespace": "staging",
    "labels": {"app": "fastapi-backend"}
  },
  "attack": {
    "type": "cpu",
    "args": {
      "cores": 0,
      "percent": 80,
      "length": 300
    }
  }
}
```

**Result**:
- ✅ p95 latency increased from 200ms → 350ms (within threshold)
- ✅ Horizontal Pod Autoscaler (HPA) scaled from 3 → 5 pods
- ✅ No errors or timeouts

### Experiment 4: Database Connection Pool Exhaustion

**Hypothesis**: "Circuit breaker engages when database connection pool full"

```json
{
  "name": "Database Connection Exhaustion",
  "type": "attack",
  "target": {
    "type": "container",
    "namespace": "staging",
    "labels": {"app": "fastapi-backend"}
  },
  "attack": {
    "type": "process_killer",
    "args": {
      "process": "postgres",
      "interval": 1,
      "length": 60
    }
  }
}
```

**Result**:
- ✅ Circuit breaker opened after 5 failed connections
- ✅ Fallback: Return cached data (99.8% success rate)
- ✅ Circuit closed automatically after 30s when database recovered

## 4. Monitoring During Chaos

### Prometheus Queries

```promql
# Circuit breaker state (0=closed, 1=open)
circuit_breaker_state{service="stripe"}

# Error rate during experiment
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))

# p95 latency during experiment
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))

# Pod count (verify autoscaling)
count(kube_pod_status_phase{namespace="staging", pod=~"fastapi.*", phase="Running"})
```

### Grafana Dashboard

```json
{
  "title": "Chaos Engineering Dashboard",
  "panels": [
    {"title": "Error Rate", "targets": [{"expr": "sum(rate(http_requests_total{status=~\"5..\"}[1m])) / sum(rate(http_requests_total[1m]))"}], "alert": {"threshold": 0.01}},
    {"title": "p95 Latency", "targets": [{"expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))"}], "alert": {"threshold": 1.0}},
    {"title": "Circuit Breaker State", "targets": [{"expr": "circuit_breaker_state{service=\"stripe\"}"}]},
    {"title": "Active Pods", "targets": [{"expr": "count(kube_pod_status_phase{namespace=\"staging\", phase=\"Running\"})"}]}
  ]
}
```

## 5. Runbook Automation

### Automatic Rollback

```yaml
# rollback-on-high-error-rate.yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: fastapi-backend
spec:
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: {duration: 2m}
        - setWeight: 50
        - pause: {duration: 5m}
        - setWeight: 100

      analysis:
        templates:
          - templateName: error-rate-analysis
        args:
          - name: error-rate-threshold
            value: "0.01"  # 1% error rate

---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-analysis
spec:
  args:
    - name: error-rate-threshold
  metrics:
    - name: error-rate
      interval: 1m
      successCondition: result < {{args.error-rate-threshold}}
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{status=~"5.."}[1m]))
            /
            sum(rate(http_requests_total[1m]))
```

**Behavior**: Automatically rollback deployment if error rate > 1% during chaos experiment

## 6. GameDay Exercises

### Quarterly GameDay (4-hour exercise)

**Agenda**:
```
09:00 - Kickoff: Review objectives and rules
09:15 - Experiment 1: Database failure (30 min)
09:45 - Debrief and fixes
10:00 - Experiment 2: Network partition (30 min)
10:30 - Debrief and fixes
10:45 - Break
11:00 - Experiment 3: Dependency failure (Stripe API down)
11:30 - Debrief and fixes
11:45 - Retro: Lessons learned, action items
```

**Metrics Tracked**:
- Mean Time to Detection (MTTD)
- Mean Time to Resolution (MTTR)
- Error rate during incident
- Circuit breaker effectiveness

## 7. Results and Impact

### Before vs After Chaos Engineering

| Metric | Before | After | Impact |
|--------|--------|-------|--------|
| **Critical Bugs Found** | 0 (in production) | 3 (before deployment) | **3 P0 incidents prevented** |
| **Circuit Breaker Validation** | Untested | Validated (2s engagement, 99.8% success) | **High confidence** |
| **MTTR** | 45 min | 8 min | **82% reduction** |
| **Incident Response Confidence** | 40% | 95% | **Trained via GameDays** |
| **Runbook Coverage** | 20% | 85% | **Automated procedures** |

### Critical Bugs Found

**Bug 1: Database Connection Pool Leak**
- **Discovery**: Pod termination experiment revealed OOM errors
- **Root cause**: Unclosed connections in error paths
- **Fix**: Implemented connection pooling with proper cleanup
- **Impact**: Prevented production outage (99.95% SLO violation)

**Bug 2: Infinite Retry Loop**
- **Discovery**: Network latency experiment caused retry storms
- **Root cause**: No exponential backoff in retry logic
- **Fix**: Implemented jitter + exponential backoff (1s, 2s, 4s, 8s)
- **Impact**: Prevented cascading failures

**Bug 3: Missing Circuit Breaker**
- **Discovery**: Stripe API failure experiment caused 100% error rate
- **Root cause**: No circuit breaker on Stripe calls
- **Fix**: Implemented circuit breaker with fallback (queue payments)
- **Impact**: 100% error rate → 0.2% error rate

## Related Documentation

- **Prometheus**: [prometheus-grafana-setup.md](prometheus-grafana-setup.md) - Monitoring
- **SLO**: [slo-error-budgets.md](slo-error-budgets.md) - Error budget tracking
- **Tracing**: [opentelemetry-tracing.md](opentelemetry-tracing.md) - Distributed tracing
- **Reference**: [../reference/chaos-best-practices.md](../reference/chaos-best-practices.md)

---

Return to [examples index](INDEX.md)
