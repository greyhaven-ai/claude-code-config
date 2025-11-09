# PlanetScale Connection Pool Exhaustion

Complete investigation of database connection pool exhaustion causing 503 errors, resolved through connection pool tuning and leak fixes.

## Overview

**Incident**: Database connection timeouts causing 15% request failure rate
**Impact**: Customer-facing 503 errors, support tickets increasing
**Root Cause**: Connection pool too small + unclosed connections in error paths
**Resolution**: Pool tuning (20→50) + connection leak fixes
**Status**: Resolved

## Incident Timeline

| Time | Event | Action |
|------|-------|--------|
| 09:30 | Alerts: High 503 error rate | Oncall paged |
| 09:35 | Investigation started | Check logs, metrics |
| 09:45 | Database connections at 100% | Identified pool exhaustion |
| 10:00 | Temporary fix: restart service | Bought time for root cause |
| 10:30 | Code analysis complete | Found connection leaks |
| 11:00 | Fix deployed (pool + leaks) | Production deployment |
| 11:30 | Monitoring confirmed stable | Incident resolved |

---

## Symptoms and Detection

### Initial Alerts

**Prometheus Alert**:
```yaml
# Alert: HighErrorRate
expr: rate(http_requests_total{status="503"}[5m]) > 0.05
for: 5m
annotations:
  summary: "503 error rate >5% for 5 minutes"
  description: "Current rate: {{ $value | humanizePercentage }}"
```

**Error Logs**:
```
[ERROR] Database query failed: connection timeout
[ERROR] Pool exhausted, waiting for available connection
[ERROR] Request timeout after 30s waiting for DB connection
```

**Impact Metrics**:
```
Error rate: 15% (150 failures per 1000 requests)
User complaints: 23 support tickets in 30 minutes
Failed transactions: ~$15,000 in abandoned carts
```

---

## Diagnosis

### Step 1: Check Connection Pool Status

**Query PlanetScale**:
```bash
# Connect to database
pscale shell greyhaven-db main

# Check active connections
SELECT
  COUNT(*) as active_connections,
  MAX(pg_stat_activity.query_start) as oldest_query
FROM pg_stat_activity
WHERE state = 'active';

# Result:
# active_connections: 98
# oldest_query: 2024-12-05 09:15:23 (15 minutes ago!)
```

**Check Application Pool**:
```python
# In FastAPI app - add diagnostic endpoint
from sqlmodel import Session
from database import engine

@app.get("/pool-status")
def pool_status():
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "timeout": pool._timeout,
        "max_overflow": pool._max_overflow
    }

# Response:
{
  "size": 20,
  "checked_out": 20,  # Pool exhausted!
  "overflow": 0,
  "timeout": 30,
  "max_overflow": 10
}
```

**Red Flags**:
- ✅ Pool at 100% capacity (20/20 connections checked out)
- ✅ No overflow connections being used (0/10)
- ✅ Connections held for >15 minutes
- ✅ New requests timing out waiting for connections

---

### Step 2: Identify Connection Leaks

**Code Review - Found Vulnerable Pattern**:
```python
# api/orders.py (BEFORE - LEAK)
from fastapi import APIRouter
from sqlmodel import Session, select
from database import engine

router = APIRouter()

@router.post("/orders")
async def create_order(order_data: OrderCreate):
    # ❌ LEAK: Session never closed on exception
    session = Session(engine)

    # Create order
    order = Order(**order_data.dict())
    session.add(order)
    session.commit()

    # If exception here, session never closed!
    if order.total > 10000:
        raise ValueError("Order exceeds limit")

    # session.close() never reached
    return order
```

**How Leak Occurs**:
1. Request creates session (acquires connection from pool)
2. Exception raised after commit
3. Function exits without calling `session.close()`
4. Connection remains "checked out" from pool
5. After 20 such exceptions, pool exhausted

---

### Step 3: Load Testing to Reproduce

**Test Script**:
```python
# test_connection_leak.py
import asyncio
import httpx

async def create_order(client, amount):
    """Create order that will trigger exception"""
    try:
        response = await client.post(
            "https://api.greyhaven.io/orders",
            json={"total": amount}
        )
        return response.status_code
    except Exception:
        return 503

async def load_test():
    """Simulate 100 orders with high amounts (triggers leak)"""
    async with httpx.AsyncClient() as client:
        # Trigger 100 exceptions (leak 100 connections)
        tasks = [create_order(client, 15000) for _ in range(100)]
        results = await asyncio.gather(*tasks)

        success = sum(1 for r in results if r == 201)
        errors = sum(1 for r in results if r == 503)

        print(f"Success: {success}, Errors: {errors}")

asyncio.run(load_test())
```

**Results**:
```
Success: 20  (first 20 use all connections)
Errors: 80   (remaining 80 timeout waiting for pool)

Proves: Connection leak exhausts pool
```

---

## Resolution

### Fix 1: Use Context Manager (Guaranteed Cleanup)

**After - With Context Manager**:
```python
# api/orders.py (AFTER - FIXED)
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session

router = APIRouter()

# ✅ Dependency injection with automatic cleanup
def get_session():
    with Session(engine) as session:
        yield session
    # Session always closed (even on exception)

@router.post("/orders")
async def create_order(
    order_data: OrderCreate,
    session: Session = Depends(get_session)
):
    # Session managed by FastAPI dependency
    order = Order(**order_data.dict())
    session.add(order)
    session.commit()

    # Exception here? No problem - session still closed by context manager
    if order.total > 10000:
        raise ValueError("Order exceeds limit")

    return order
```

**Why This Works**:
- Context manager (`with` statement) guarantees `session.close()` in `__exit__`
- Works even if exception raised
- FastAPI `Depends()` handles async cleanup automatically

---

### Fix 2: Increase Connection Pool Size

**Before** (pool too small):
```python
# database.py (BEFORE)
from sqlmodel import create_engine

engine = create_engine(
    database_url,
    pool_size=20,        # Too small for load
    max_overflow=10,
    pool_timeout=30
)
```

**After** (tuned for load):
```python
# database.py (AFTER)
from sqlmodel import create_engine
import os

# Calculate pool size based on workers
# Formula: (workers * 2) + buffer
# 16 workers * 2 + 20 buffer = 52
workers = int(os.getenv("WEB_CONCURRENCY", 16))
pool_size = (workers * 2) + 20

engine = create_engine(
    database_url,
    pool_size=pool_size,      # 52 connections
    max_overflow=20,          # Burst to 72 total
    pool_timeout=30,
    pool_recycle=3600,        # Recycle after 1 hour
    pool_pre_ping=True,       # Verify connection health
    echo=False
)
```

**Pool Size Calculation**:
```
Workers: 16 (Uvicorn workers)
Connections per worker: 2 (normal peak)
Buffer: 20 (for spikes)

pool_size = (16 * 2) + 20 = 52
max_overflow = 20 (total 72 for extreme spikes)
```

---

### Fix 3: Add Connection Pool Monitoring

**Prometheus Metrics**:
```python
# monitoring.py
from prometheus_client import Gauge
from database import engine

# Pool metrics
db_pool_size = Gauge('db_pool_size_total', 'Total pool size')
db_pool_checked_out = Gauge('db_pool_checked_out', 'Connections in use')
db_pool_idle = Gauge('db_pool_idle', 'Idle connections')
db_pool_overflow = Gauge('db_pool_overflow', 'Overflow connections')

def update_pool_metrics():
    """Update pool metrics every 10 seconds"""
    pool = engine.pool
    db_pool_size.set(pool.size())
    db_pool_checked_out.set(pool.checkedout())
    db_pool_idle.set(pool.size() - pool.checkedout())
    db_pool_overflow.set(pool.overflow())

# Schedule in background task
import asyncio
async def pool_monitor():
    while True:
        update_pool_metrics()
        await asyncio.sleep(10)
```

**Grafana Alert**:
```yaml
# Alert: Connection pool near exhaustion
expr: db_pool_checked_out / db_pool_size_total > 0.8
for: 5m
annotations:
  summary: "Connection pool >80% utilized"
  description: "{{ $value | humanizePercentage }} of pool in use"
```

---

### Fix 4: Add Timeout and Retry Logic

**Connection Timeout Handling**:
```python
# database.py - Add connection retry
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def get_session_with_retry():
    """Get session with automatic retry on pool timeout"""
    try:
        with Session(engine) as session:
            yield session
    except TimeoutError:
        # Pool exhausted - retry after exponential backoff
        raise

@router.post("/orders")
async def create_order(
    order_data: OrderCreate,
    session: Session = Depends(get_session_with_retry)
):
    # Will retry up to 3 times if pool exhausted
    ...
```

---

## Results

### Before vs After Metrics

| Metric | Before Fix | After Fix | Improvement |
|--------|-----------|-----------|-------------|
| **Connection Pool Size** | 20 | 52 | +160% capacity |
| **Pool Utilization** | 100% (exhausted) | 40-60% (healthy) | -40% utilization |
| **503 Error Rate** | 15% | 0.01% | **99.9% reduction** |
| **Request Timeout** | 30s (waiting) | <100ms | **99.7% faster** |
| **Leaked Connections** | 12/hour | 0/day | **100% eliminated** |

---

### Deployment Verification

**Load Test After Fix**:
```bash
# Simulate 1000 concurrent orders
ab -n 1000 -c 50 -p order.json https://api.greyhaven.io/orders

# Results:
Requests per second: 250 [#/sec]
Time per request: 200ms [mean]
Failed requests: 0 (0%)
Successful requests: 1000 (100%)

# Pool status during test:
{
  "size": 52,
  "checked_out": 28,     # 54% utilization (healthy)
  "overflow": 0,
  "idle": 24
}
```

---

## Prevention Measures

### 1. Connection Leak Tests

```python
# tests/test_connection_leaks.py
@pytest.fixture
def track_connections():
    before = engine.pool.checkedout()
    yield
    after = engine.pool.checkedout()
    assert after == before, f"Leaked {after - before} connections"
```

### 2. Pool Alerts

```yaml
# Alert if pool >80% for 5 minutes
expr: db_pool_checked_out / db_pool_size_total > 0.8
```

### 3. Health Check

```python
@app.get("/health/database")
async def database_health():
    with Session(engine) as session:
        session.execute("SELECT 1")
        return {"status": "healthy", "pool_utilization": pool.checkedout() / pool.size()}
```

### 4. Monitoring Commands

```bash
# Active connections
pscale shell db main --execute "SELECT COUNT(*) FROM pg_stat_activity WHERE state='active'"

# Slow queries
pscale database insights db main --slow-queries
```

---

## Lessons Learned

### What Went Well

✅ Quick identification of pool exhaustion (Prometheus alerts)
✅ Context manager pattern eliminated leaks
✅ Pool tuning based on formula (workers * 2 + buffer)
✅ Comprehensive monitoring added

### What Could Be Improved

❌ No pool monitoring before incident
❌ Pool size not calculated based on load
❌ Missing connection leak tests

### Key Takeaways

1. **Always use context managers** for database sessions
2. **Calculate pool size** based on workers and load
3. **Monitor pool utilization** with alerts at 80%
4. **Test for connection leaks** in CI/CD
5. **Add retry logic** for transient pool timeouts

---

## PlanetScale Best Practices

```bash
# Connection string with SSL
DATABASE_URL="postgresql://user:pass@aws.connect.psdb.cloud/db?sslmode=require"

# Schema changes via deploy requests
pscale deploy-request create db schema-update

# Test in branch
pscale branch create db test-feature
```

```sql
-- Index frequently queried columns
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Analyze slow queries
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

---

## Related Documentation

- **Worker Deployment**: [cloudflare-worker-deployment-failure.md](cloudflare-worker-deployment-failure.md)
- **Network Debugging**: [distributed-system-debugging.md](distributed-system-debugging.md)
- **Performance**: [performance-degradation-analysis.md](performance-degradation-analysis.md)
- **Runbooks**: [../reference/troubleshooting-runbooks.md](../reference/troubleshooting-runbooks.md)

---

Return to [examples index](INDEX.md)
