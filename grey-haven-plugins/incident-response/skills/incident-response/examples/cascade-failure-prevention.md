# Cascade Failure Prevention

Preventing cascade failures through circuit breakers, bulkhead isolation, and graceful degradation. Demonstrates how a single service failure (auth service down) can bring down an entire system without proper isolation, and how to architect for resilience.

## Incident Summary

**Incident**: Auth service down for 10 minutes, caused complete system outage
**Impact**: All services failed despite only auth being down
**Root Cause**: No circuit breakers, all services retrying auth indefinitely
**Resolution**: Implemented circuit breakers, bulkheads, and fallback logic
**Prevention**: Architectural changes to limit blast radius

---

## What is a Cascade Failure?

**Definition**: A failure in one component causes failures in dependent components, propagating through the system like falling dominoes.

**Example Cascade**:
```
Auth Service Down (1 service)
  ↓
API Gateway retries auth infinitely (blocks all requests)
  ↓
User Service can't authenticate (fails all user requests)
  ↓
Order Service can't validate users (fails all orders)
  ↓
Payment Service can't verify auth (fails all payments)
  ↓
Entire System Down (all services)
```

**Impact Amplification**: 1 service failure → 10 service failures

---

## The Incident

### Timeline

**Before Circuit Breakers**:

| Time | Event | Impact |
|------|-------|--------|
| 14:00 | Auth service goes down (database connection lost) | Auth service: 100% errors |
| 14:01 | API Gateway retries auth (exponential backoff) | API Gateway: Thread pool exhausted |
| 14:02 | User Service can't authenticate requests | User Service: 100% errors |
| 14:03 | Order Service times out waiting for auth | Order Service: 100% errors |
| 14:04 | Payment Service cascades fail | Payment Service: 100% errors |
| 14:05 | **Complete system outage** | **All services down** |
| 14:10 | Auth service recovers (database reconnects) | Auth service: Back online |
| 14:15 | Services gradually recover | All services: Slowly recovering |
| 14:20 | Full recovery | All services: Normal |

**Duration**: 20 minutes total outage (10 min auth down + 10 min recovery)
**Revenue Loss**: ~$16,667 (20 min × $50K/hour)

---

## Root Cause Analysis

### Why Did Everything Fail?

**Auth Service Failure** (Original Problem):
```
Auth Service
  ├─ Database connection lost
  ├─ Responding with HTTP 503
  └─ Expected recovery time: 10 minutes
```

**Cascade Effect** (Propagation):
```
1. API Gateway calls Auth Service
   ├─ Gets 503 error
   ├─ Retries with exponential backoff
   ├─ Retries exhaust thread pool (200 threads)
   └─ All incoming requests blocked waiting for threads

2. User Service calls API Gateway
   ├─ API Gateway not responding (threads exhausted)
   ├─ User Service retries infinitely
   ├─ User Service thread pool exhausted
   └─ User Service stops accepting requests

3. Order Service calls User Service
   ├─ User Service not responding
   ├─ Order Service retries infinitely
   ├─ Order Service thread pool exhausted
   └─ Order Service stops accepting requests

4. Payment Service calls Order Service
   ├─ Order Service not responding
   ├─ Payment Service retries infinitely
   └─ Payment Service fails

Result: Entire system down
```

**Why No Graceful Degradation?**
- ❌ No circuit breakers (kept retrying forever)
- ❌ No bulkhead isolation (exhausted all threads)
- ❌ No fallback logic (no graceful degradation)
- ❌ No timeout limits (waited indefinitely)

---

## Solution 1: Circuit Breaker Pattern

### What is a Circuit Breaker?

**Analogy**: Like an electrical circuit breaker in your home
- Detects failures (5 errors in 10 seconds)
- **Opens circuit** (stops calling failing service)
- Waits for recovery (60 seconds)
- **Half-open** (tries one request to test)
- **Closes circuit** (resumes normal operation if successful)

**Circuit Breaker States**:
```
┌─────────┐  5 errors   ┌──────┐  60s timeout  ┌───────────┐
│ CLOSED  │ ─────────→  │ OPEN │ ───────────→  │ HALF-OPEN │
│ (Normal)│              │(Fast │               │  (Testing)│
└─────────┘              │ Fail)│               └───────────┘
     ↑                   └──────┘                     │
     │                                                │
     └────────────────────────────────────────────────┘
              Success (circuit restored)
```

### Implementation

**Before** (No Circuit Breaker):
```typescript
// ❌ BAD: Retries forever, blocks threads
async function authenticateUser(token: string): Promise<User> {
  let retries = 0;
  while (true) {  // Infinite retries!
    try {
      const response = await fetch('https://auth.greyhaven.io/verify', {
        method: 'POST',
        body: JSON.stringify({ token })
      });
      return await response.json();
    } catch (error) {
      retries++;
      await sleep(Math.pow(2, retries) * 1000);  // Exponential backoff
      // Never gives up, keeps retrying forever
    }
  }
}
```

**After** (With Circuit Breaker):
```typescript
// ✅ GOOD: Circuit breaker stops calling failing service
import CircuitBreaker from 'opossum';

const breaker = new CircuitBreaker(authenticateUser, {
  timeout: 3000,           // 3s timeout per request
  errorThresholdPercentage: 50,  // Open circuit if >50% errors
  resetTimeout: 30000,     // Try again after 30s
  rollingCountTimeout: 10000,    // 10s error window
  volumeThreshold: 5       // Need 5 requests to trip
});

// Fallback when circuit is open
breaker.fallback(() => {
  return { id: 'guest', role: 'unauthenticated' };  // Graceful degradation
});

// Usage
async function authenticateUserWithCircuitBreaker(token: string): Promise<User> {
  try {
    return await breaker.fire(token);
  } catch (error) {
    if (error.message === 'Breaker is open') {
      // Circuit breaker is open, use fallback
      return { id: 'guest', role: 'unauthenticated' };
    }
    throw error;
  }
}

// Events
breaker.on('open', () => {
  console.log('Circuit breaker opened - auth service failing');
  metrics.increment('circuit_breaker.auth.open');
});

breaker.on('halfOpen', () => {
  console.log('Circuit breaker half-open - testing auth service');
});

breaker.on('close', () => {
  console.log('Circuit breaker closed - auth service recovered');
  metrics.increment('circuit_breaker.auth.close');
});
```

**Result**:
- Auth service down → Circuit opens after 5 failures
- Subsequent requests fail fast (< 1ms) instead of timing out (3s)
- Fallback to guest user (graceful degradation)
- System remains operational without auth

---

## Solution 2: Bulkhead Isolation

### What is a Bulkhead?

**Analogy**: Like compartments in a ship
- If one compartment floods, others stay dry
- Ship doesn't sink even with one failure

**Bulkhead in Services**:
- Separate thread pools for different dependencies
- Auth service failure doesn't exhaust all threads
- Other operations (database, cache) still work

### Implementation

**Before** (No Bulkheads):
```typescript
// ❌ BAD: Single thread pool for all operations
const threadPool = new ThreadPool(200);  // Shared by all operations

// All operations compete for the same 200 threads
await threadPool.execute(() => callAuthService());
await threadPool.execute(() => callDatabase());
await threadPool.execute(() => callCache());

// If auth service hangs, all 200 threads stuck waiting
// Database and cache operations blocked
```

**After** (With Bulkheads):
```typescript
// ✅ GOOD: Separate thread pools for each dependency
const authThreadPool = new ThreadPool(50);       // Auth: 50 threads max
const databaseThreadPool = new ThreadPool(100);  // Database: 100 threads
const cacheThreadPool = new ThreadPool(50);      // Cache: 50 threads

// Auth failure only affects auth thread pool
await authThreadPool.execute(() => callAuthService());
await databaseThreadPool.execute(() => callDatabase());
await cacheThreadPool.execute(() => callCache());

// If auth hangs, only 50 threads blocked
// Database and cache still have 150 threads available
```

**Bulkhead with Limits**:
```typescript
import pLimit from 'p-limit';

// Limit concurrent auth calls to 10
const authLimit = pLimit(10);

async function callAuthService(token: string) {
  return authLimit(async () => {
    // Only 10 concurrent auth calls allowed
    // If limit reached, queues instead of exhausting threads
    const response = await fetch('https://auth.greyhaven.io/verify', {
      method: 'POST',
      body: JSON.stringify({ token }),
      timeout: 3000  // Fail fast if slow
    });
    return response.json();
  });
}
```

---

## Solution 3: Graceful Degradation

### What is Graceful Degradation?

**Definition**: System continues operating with reduced functionality when dependencies fail

**Example**: Auth service down → Allow guest access instead of total failure

### Implementation

**Before** (Hard Failure):
```typescript
// ❌ BAD: Entire request fails if auth fails
async function handleRequest(req: Request): Promise<Response> {
  const user = await authenticateUser(req.headers.get('Authorization'));
  const orders = await getOrders(user.id);
  return Response.json(orders);
}

// If auth fails: 500 error (user sees nothing)
```

**After** (Graceful Degradation):
```typescript
// ✅ GOOD: Degrade to guest user, show limited data
async function handleRequest(req: Request): Promise<Response> {
  let user: User;

  try {
    user = await authenticateUserWithCircuitBreaker(req.headers.get('Authorization'));
  } catch (error) {
    // Auth failed → use guest user
    user = { id: 'guest', role: 'unauthenticated' };
  }

  if (user.role === 'unauthenticated') {
    // Show public data only
    const publicOrders = await getPublicOrders();
    return Response.json({
      orders: publicOrders,
      notice: 'Authentication unavailable, showing limited data'
    });
  }

  // Authenticated → show full data
  const orders = await getOrders(user.id);
  return Response.json(orders);
}
```

---

## Solution 4: Timeout and Retry Configuration

### Proper Timeout Configuration

```typescript
// ✅ GOOD: Aggressive timeouts with exponential backoff
const fetchWithTimeout = async (url: string, timeout: number = 3000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: { 'Connection': 'keep-alive' }
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
};

// Retry with exponential backoff (max 3 attempts)
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      const delay = Math.pow(2, attempt) * 1000;  // 1s, 2s, 4s
      await sleep(delay);
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## Results

### Before vs After Architecture

**Before** (Cascade Failures):
```
Auth Service Down (1 failure)
  ↓ No circuit breakers
API Gateway exhausts threads (2 failures)
  ↓ No bulkheads
User Service exhausts threads (3 failures)
  ↓ No fallback
Order Service fails (4 failures)
  ↓ No graceful degradation
Payment Service fails (5 failures)
  ↓
TOTAL OUTAGE (all services down)
```

**After** (Isolated Failures):
```
Auth Service Down (1 failure)
  ↓ Circuit breaker opens
API Gateway fails fast (< 1ms)
  ↓ Bulkhead isolation (auth thread pool only)
User Service uses guest fallback (continues working)
  ↓ Graceful degradation
Order Service shows public orders (reduced functionality)
  ↓ Timeout limits
Payment Service disabled for guests (expected behavior)
  ↓
LIMITED FUNCTIONALITY (core services still work)
```

### Metrics

| Metric | Before (No Resilience) | After (With Resilience) | Improvement |
|--------|----------------------|------------------------|-------------|
| **System Uptime** | 99.0% (20 min outage/month) | 99.9% (2 min outage/month) | **10x better** |
| **Cascade Failures** | 5 services down | 1 service down | **80% reduction** |
| **Recovery Time** | 20 minutes | 2 minutes | **90% faster** |
| **Revenue Loss** | $16,667 per incident | $1,667 per incident | **90% reduction** |
| **User Impact** | 100% (total outage) | 20% (reduced features) | **80% reduction** |

---

## Key Patterns

### Pattern 1: Circuit Breaker

**When to Use**:
- External dependencies (APIs, databases, caches)
- Services with variable latency
- Prevent retry storms

**Configuration**:
```javascript
{
  timeout: 3000,              // Max request time
  errorThresholdPercentage: 50,  // Open at 50% errors
  resetTimeout: 30000,        // Retry after 30s
  volumeThreshold: 5          // Min requests to trip
}
```

### Pattern 2: Bulkhead Isolation

**When to Use**:
- Multiple dependencies
- Prevent thread pool exhaustion
- Limit blast radius

**Configuration**:
```javascript
{
  authThreads: 50,      // Auth operations
  dbThreads: 100,       // Database operations
  cacheThreads: 50      // Cache operations
}
```

### Pattern 3: Graceful Degradation

**When to Use**:
- Non-critical features
- User-facing operations
- Maintain partial functionality

**Fallback Strategy**:
- Auth down → Guest user
- Database down → Cache
- Cache down → Empty results

### Pattern 4: Timeout & Retry

**When to Use**:
- All external calls
- Prevent indefinite waits

**Configuration**:
```javascript
{
  timeout: 3000,        // 3s max
  maxRetries: 3,        // 3 attempts
  backoff: 'exponential'  // 1s, 2s, 4s
}
```

---

## Prevention Measures

### Immediate Actions

- [x] Implemented circuit breakers for all external dependencies
- [x] Added bulkhead isolation (separate thread pools)
- [x] Graceful degradation for auth failures
- [x] Timeout configuration (3s max for all external calls)

### Short-Term Actions

- [x] Chaos engineering: randomly kill services to test resilience
- [x] Load testing with dependency failures
- [x] Metrics dashboard for circuit breaker states
- [x] Automated alerts when circuit breakers open

### Long-Term Actions

- [x] Service mesh (Istio) for automatic circuit breakers
- [x] Resilience patterns for all microservices
- [x] Monthly resilience drills (simulate failures)
- [x] Architectural decision record: resilience requirements

---

## Related Documentation

- **Circuit Breaker Pattern**: [Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html)
- **Bulkhead Pattern**: [Resilience4j](https://resilience4j.readme.io/docs/bulkhead)
- **Chaos Engineering**: [Principles of Chaos](https://principlesofchaos.org/)
- **Istio Service Mesh**: [istio.io](https://istio.io/)
- **Opossum (Circuit Breaker Library)**: [nodeshift.dev/opossum](https://nodeshift.dev/opossum/)

---

Return to [examples index](INDEX.md)
