# Performance Degradation Analysis

Investigating API response time increase from 200ms to 2000ms, resolved through N+1 query elimination, caching, and index optimization.

## Overview

**Incident**: API response times degraded 10x (200ms → 2000ms)
**Impact**: User-facing slowness, timeout errors, poor UX
**Root Cause**: N+1 query problem + missing indexes + no caching
**Resolution**: Query optimization + indexes + Redis caching
**Status**: Resolved

## Incident Timeline

| Time | Event | Action |
|------|-------|--------|
| 08:00 | Slowness reports from users | Support tickets opened |
| 08:15 | Monitoring confirms degradation | p95 latency 2000ms |
| 08:30 | Database profiling started | Slow query log analysis |
| 09:00 | N+1 query identified | Found 100+ queries per request |
| 09:30 | Fix implemented | Eager loading + indexes |
| 10:00 | Caching added | Redis for frequently accessed data |
| 10:30 | Deployment complete | Latency back to 200ms |

---

## Symptoms and Detection

### Initial Metrics

**Latency Increase**:
```
p50: 180ms → 1800ms (+900% slower)
p95: 220ms → 2100ms (+854% slower)
p99: 450ms → 3500ms (+677% slower)

Requests timing out: 5% (>3s timeout)
```

**User Impact**:
- Page load times: 5-10 seconds
- API timeouts: 5% of requests
- Support tickets: 47 in 1 hour
- User complaints: "App is unusable"

---

## Diagnosis

### Step 1: Application Performance Monitoring

**Wrangler Tail Analysis**:
```bash
# Monitor worker requests in real-time
wrangler tail --format pretty

# Output shows slow requests:
[2024-12-05 08:20:15] GET /api/orders - 2145ms
  └─ database_query: 1950ms (90% of total time!)
  └─ json_serialization: 150ms
  └─ response_headers: 45ms

# Red flag: Database taking 90% of request time
```

---

### Step 2: Database Query Analysis

**PlanetScale Slow Query Log**:
```bash
# Enable and check slow queries
pscale database insights greyhaven-db main --slow-queries

# Results:
Query: SELECT * FROM order_items WHERE order_id = ?
Calls: 157 times per request  # ❌ N+1 query problem!
Avg time: 12ms per query
Total: 1884ms per request (12ms × 157)
```

**N+1 Query Pattern Identified**:
```python
# api/orders.py (BEFORE - N+1 Problem)
@router.get("/orders/{user_id}")
async def get_user_orders(user_id: int, session: Session = Depends(get_session)):
    # Query 1: Get all orders for user
    orders = session.exec(
        select(Order).where(Order.user_id == user_id)
    ).all()  # Returns 157 orders

    # Query 2-158: Get items for EACH order (N+1!)
    for order in orders:
        order.items = session.exec(
            select(OrderItem).where(OrderItem.order_id == order.id)
        ).all()  # 157 additional queries!

    return orders

# Total queries: 1 + 157 = 158 queries per request
# Total time: 10ms + (157 × 12ms) = 1894ms
```

---

### Step 3: Database Index Analysis

**Missing Indexes**:
```sql
-- Check existing indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'order_items';

-- Results:
-- Primary key on id (exists) ✅
-- NO index on order_id ❌ (needed for WHERE clause)
-- NO index on user_id ❌ (needed for joins)

-- Explain plan shows full table scan
EXPLAIN ANALYZE
SELECT * FROM order_items WHERE order_id = 123;

-- Result:
Seq Scan on order_items  (cost=0.00..1500.00 rows=1 width=100) (actual time=12.345..12.345 rows=5 loops=157)
  Filter: (order_id = 123)
  Rows Removed by Filter: 10000

-- Full table scan on 10K rows, 157 times = extremely slow!
```

---

## Resolution

### Fix 1: Eliminate N+1 with Eager Loading

**After - Single Query with Join**:
```python
# api/orders.py (AFTER - Eager Loading)
from sqlmodel import select
from sqlalchemy.orm import selectinload

@router.get("/orders/{user_id}")
async def get_user_orders(user_id: int, session: Session = Depends(get_session)):
    # ✅ Single query with eager loading
    statement = (
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.items))  # Eager load items
    )

    orders = session.exec(statement).all()

    return orders

# Total queries: 2 (1 for orders, 1 for all items)
# Total time: 10ms + 25ms = 35ms (98% faster!)
```

**Query Comparison**:
```
BEFORE (N+1):
- Query 1: SELECT * FROM orders WHERE user_id = 1 (10ms)
- Query 2-158: SELECT * FROM order_items WHERE order_id = ? (×157, 12ms each)
- Total: 1894ms

AFTER (Eager Loading):
- Query 1: SELECT * FROM orders WHERE user_id = 1 (10ms)
- Query 2: SELECT * FROM order_items WHERE order_id IN (?, ?, ..., ?) (25ms)
- Total: 35ms (54x faster!)
```

---

### Fix 2: Add Database Indexes

**Create Indexes**:
```sql
-- Index on order_id for faster lookups
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- Index on user_id for user queries
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Index on created_at for time-based queries
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- Composite index for common filters
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
```

**Before/After EXPLAIN**:
```sql
-- BEFORE (no index):
EXPLAIN ANALYZE SELECT * FROM order_items WHERE order_id = 123;
Seq Scan (cost=0.00..1500.00) (actual time=12.345ms)

-- AFTER (with index):
Index Scan using idx_order_items_order_id (cost=0.00..8.50) (actual time=0.045ms)

-- 270x faster (12.345ms → 0.045ms)
```

---

### Fix 3: Implement Redis Caching

**Cache Frequent Queries**:
```typescript
// cache.ts - Redis caching layer
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: env.UPSTASH_REDIS_URL,
  token: env.UPSTASH_REDIS_TOKEN
});

async function getCachedOrders(userId: number) {
  const cacheKey = `orders:user:${userId}`;

  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);  // Cache hit
  }

  // Cache miss - query database
  const orders = await fetchOrdersFromDb(userId);

  // Store in cache (5 minute TTL)
  await redis.setex(cacheKey, 300, JSON.stringify(orders));

  return orders;
}
```

**Cache Hit Rates**:
```
Requests: 10,000
Cache hits: 8,500 (85%)
Cache misses: 1,500 (15%)

Avg latency with cache:
- Cache hit: 5ms (Redis)
- Cache miss: 35ms (database)
- Overall: (0.85 × 5) + (0.15 × 35) = 9.5ms
```

---

### Fix 4: Database Connection Pooling

**Optimize Pool Settings**:
```python
# database.py - Tuned for performance
engine = create_engine(
    database_url,
    pool_size=50,           # Increased from 20
    max_overflow=20,
    pool_recycle=1800,      # 30 minutes
    pool_pre_ping=True,     # Health check
    echo=False,
    connect_args={
        "server_settings": {
            "statement_timeout": "30000",  # 30s query timeout
            "idle_in_transaction_session_timeout": "60000"  # 60s idle
        }
    }
)
```

---

## Results

### Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **p50 Latency** | 1800ms | 180ms | **90% faster** |
| **p95 Latency** | 2100ms | 220ms | **90% faster** |
| **p99 Latency** | 3500ms | 450ms | **87% faster** |
| **Database Queries** | 158/request | 2/request | **99% reduction** |
| **Cache Hit Rate** | 0% | 85% | **85% hits** |
| **Timeout Errors** | 5% | 0% | **100% eliminated** |

### Cost Impact

**Database Query Reduction**:
```
Before: 158 queries × 100 req/s = 15,800 queries/s
After: 2 queries × 100 req/s = 200 queries/s

Reduction: 98.7% fewer queries
Cost savings: $450/month (reduced database tier)
```

---

## Prevention Measures

### 1. Query Performance Monitoring

**Slow Query Alert**:
```yaml
# Alert on slow database queries
- alert: SlowDatabaseQueries
  expr: histogram_quantile(0.95, rate(database_query_duration_seconds[5m])) > 0.1
  for: 5m
  annotations:
    summary: "Database queries p95 >100ms"
```

### 2. N+1 Query Detection

**Test for N+1 Patterns**:
```python
# tests/test_n_plus_one.py
import pytest
from sqlalchemy import event
from database import engine

@pytest.fixture
def query_counter():
    """Count SQL queries during test"""
    queries = []

    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        queries.append(statement)

    event.listen(engine, "before_cursor_execute", before_cursor_execute)
    yield queries
    event.remove(engine, "before_cursor_execute", before_cursor_execute)

def test_get_user_orders_no_n_plus_one(query_counter):
    """Verify endpoint doesn't have N+1 queries"""
    get_user_orders(user_id=1)

    # Should be 2 queries max (orders + items)
    assert len(query_counter) <= 2, f"N+1 detected: {len(query_counter)} queries"
```

### 3. Database Index Coverage

```sql
-- Check for missing indexes
SELECT
  schemaname,
  tablename,
  attname,
  n_distinct,
  correlation
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct > 100  -- Cardinality suggests index needed
ORDER BY tablename, attname;
```

### 4. Performance Budget

```typescript
// Set performance budgets
const PERFORMANCE_BUDGETS = {
  api_latency_p95: 500,  // ms
  database_queries_per_request: 5,
  cache_hit_rate_min: 0.70,  // 70%
};

// CI/CD check
if (metrics.api_latency_p95 > PERFORMANCE_BUDGETS.api_latency_p95) {
  throw new Error(`Performance budget exceeded: ${metrics.api_latency_p95}ms > 500ms`);
}
```

---

## Lessons Learned

### What Went Well

✅ Slow query log pinpointed N+1 problem
✅ Eager loading eliminated 99% of queries
✅ Indexes provided 270x speedup
✅ Caching reduced load by 85%

### What Could Be Improved

❌ No N+1 query detection before production
❌ Missing indexes not caught in code review
❌ No caching layer initially
❌ No query performance monitoring

### Key Takeaways

1. **Always use eager loading** for associations
2. **Add indexes** for all foreign keys and WHERE clauses
3. **Implement caching** for frequently accessed data
4. **Monitor query counts** per request (alert on >10)
5. **Test for N+1** in CI/CD pipeline

---

## Related Documentation

- **Worker Deployment**: [cloudflare-worker-deployment-failure.md](cloudflare-worker-deployment-failure.md)
- **Database Issues**: [planetscale-connection-issues.md](planetscale-connection-issues.md)
- **Network Debugging**: [distributed-system-debugging.md](distributed-system-debugging.md)
- **Runbooks**: [../reference/troubleshooting-runbooks.md](../reference/troubleshooting-runbooks.md)

---

Return to [examples index](INDEX.md)
