# Database Connection Pool Memory Leaks

Detecting and fixing PostgreSQL connection pool leaks in FastAPI applications using connection monitoring and proper cleanup patterns.

## Overview

**Before Optimization**:
- Active connections: 95/100 (pool exhausted)
- Connection timeouts: 15-20/min during peak
- Memory growth: 100MB/hour (unclosed connections)
- Service restarts: 3-4x/day

**After Optimization**:
- Active connections: 8-12/100 (healthy pool)
- Connection timeouts: 0/day
- Memory growth: 0MB/hour (stable)
- Service restarts: 0/month

**Tools**: asyncpg, SQLModel, psycopg3, pg_stat_activity, Prometheus

## 1. Connection Pool Architecture

### Grey Haven Stack: PostgreSQL + SQLModel

**Connection Pool Configuration**:
```python
# database.py
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

# ❌ VULNERABLE: No max_overflow, no timeout
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=20,
    echo=True
)

# ✅ SECURE: Proper pool configuration
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=20,              # Core connections
    max_overflow=10,           # Max additional connections
    pool_timeout=30,           # Wait timeout (seconds)
    pool_recycle=3600,         # Recycle after 1 hour
    pool_pre_ping=True,        # Verify connection before use
    echo=False
)
```

**Pool Health Monitoring**:
```python
# monitoring.py
from prometheus_client import Gauge

# Prometheus metrics
db_pool_size = Gauge('db_pool_connections_total', 'Total pool size')
db_pool_active = Gauge('db_pool_connections_active', 'Active connections')
db_pool_idle = Gauge('db_pool_connections_idle', 'Idle connections')
db_pool_overflow = Gauge('db_pool_connections_overflow', 'Overflow connections')

def record_pool_metrics(engine):
    pool = engine.pool
    db_pool_size.set(pool.size())
    db_pool_active.set(pool.checkedout())
    db_pool_idle.set(pool.size() - pool.checkedout())
    db_pool_overflow.set(pool.overflow())
```

## 2. Common Leak Pattern: Unclosed Connections

### Vulnerable Code (Connection Leak)

```python
# api/orders.py (BEFORE)
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import engine

router = APIRouter()

@router.get("/orders")
async def get_orders():
    # ❌ LEAK: Connection never closed
    session = Session(engine)

    # If exception occurs here, session never closed
    orders = session.exec(select(Order)).all()

    # If return happens here, session never closed
    return orders

    # session.close() never reached if early return/exception
    session.close()
```

**What Happens**:
1. Every request acquires connection from pool
2. Exception/early return prevents `session.close()`
3. Connection remains in "active" state
4. Pool exhausts after 100 requests (pool_size=100)
5. New requests timeout waiting for connection

**Memory Impact**:
```
Initial pool: 20 connections (40MB)
After 1 hour: 95 leaked connections (190MB)
After 6 hours: Pool exhausted + 100MB leaked memory
```

### Fixed Code (Context Manager)

```python
# api/orders.py (AFTER)
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import engine, get_session
from contextlib import contextmanager

router = APIRouter()

# ✅ Option 1: FastAPI dependency injection (recommended)
def get_session():
    """Session dependency with automatic cleanup"""
    with Session(engine) as session:
        yield session

@router.get("/orders")
async def get_orders(session: Session = Depends(get_session)):
    # Session automatically closed after request
    orders = session.exec(select(Order)).all()
    return orders


# ✅ Option 2: Explicit context manager
@router.get("/orders-alt")
async def get_orders_alt():
    with Session(engine) as session:
        orders = session.exec(select(Order)).all()
        return orders
    # Session guaranteed to close (even on exception)
```

**Why This Works**:
- Context manager ensures `session.close()` called in `__exit__`
- Works even if exception raised
- Works even if early return
- FastAPI `Depends()` handles async cleanup

## 3. Async Connection Leaks (asyncpg)

### Vulnerable Async Pattern

```python
# api/analytics.py (BEFORE)
import asyncpg
from fastapi import APIRouter

router = APIRouter()

@router.get("/analytics")
async def get_analytics():
    # ❌ LEAK: Connection never closed
    conn = await asyncpg.connect(
        user='postgres',
        password='secret',
        database='analytics'
    )

    # Exception here = connection leaked
    result = await conn.fetch('SELECT * FROM metrics WHERE date > $1', date)

    # Early return = connection leaked
    if not result:
        return []

    await conn.close()  # Never reached
    return result
```

### Fixed Async Pattern

```python
# api/analytics.py (AFTER)
import asyncpg
from fastapi import APIRouter
from contextlib import asynccontextmanager

router = APIRouter()

# ✅ Connection pool (shared across requests)
pool: asyncpg.Pool = None

@asynccontextmanager
async def get_db_connection():
    """Async context manager for connections"""
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)

@router.get("/analytics")
async def get_analytics():
    async with get_db_connection() as conn:
        result = await conn.fetch(
            'SELECT * FROM metrics WHERE date > $1',
            date
        )
        return result
    # Connection automatically released to pool
```

**Pool Setup** (application startup):
```python
# main.py
from fastapi import FastAPI
import asyncpg

app = FastAPI()

@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(
        user='postgres',
        password='secret',
        database='analytics',
        min_size=10,        # Minimum connections
        max_size=20,        # Maximum connections
        max_inactive_connection_lifetime=300  # Recycle after 5 min
    )

@app.on_event("shutdown")
async def shutdown():
    await pool.close()
```

## 4. Transaction Leak Detection

### Monitoring Active Connections

**PostgreSQL Query**:
```sql
-- Show active connections with details
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query,
    state_change,
    NOW() - state_change AS duration
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;
```

**Prometheus Metrics**:
```python
# monitoring.py
from prometheus_client import Gauge
import asyncpg

db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections',
    ['state']
)

async def monitor_connections(pool: asyncpg.Pool):
    """Monitor PostgreSQL connections every 30 seconds"""
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT state, COUNT(*) as count
            FROM pg_stat_activity
            WHERE datname = current_database()
            GROUP BY state
        """)

        for row in rows:
            db_connections_active.labels(state=row['state']).set(row['count'])
```

**Grafana Alert** (connection leak):
```yaml
alert: DatabaseConnectionLeak
expr: db_connections_active{state="active"} > 80
for: 5m
annotations:
  summary: "Potential connection leak ({{ $value }} active connections)"
  description: "Active connections have been above 80 for 5+ minutes"
```

## 5. Real-World Fix: FastAPI Order Service

### Before (Connection Pool Exhaustion)

```python
# services/order_processor.py (BEFORE)
from sqlmodel import Session, select
from database import engine
from models import Order, OrderItem

class OrderProcessor:
    async def process_order(self, order_id: int):
        # ❌ LEAK: Multiple sessions, some never closed
        session1 = Session(engine)
        order = session1.get(Order, order_id)

        if not order:
            # Early return = session1 leaked
            return None

        # ❌ LEAK: Second session
        session2 = Session(engine)
        items = session2.exec(
            select(OrderItem).where(OrderItem.order_id == order_id)
        ).all()

        # Exception here = both sessions leaked
        total = sum(item.price * item.quantity for item in items)

        order.total = total
        session1.commit()

        # Only session1 closed, session2 leaked
        session1.close()
        return order
```

**Metrics (Before)**:
```
Connection pool: 100 connections
Active connections after 1 hour: 95/100
Leaked connections: ~12/min
Memory growth: 100MB/hour
Pool exhaustion: Every 6-8 hours
```

### After (Proper Resource Management)

```python
# services/order_processor.py (AFTER)
from sqlmodel import Session, select
from database import engine, get_session
from models import Order, OrderItem
from contextlib import contextmanager

class OrderProcessor:
    async def process_order(self, order_id: int):
        # ✅ Single session, guaranteed cleanup
        with Session(engine) as session:
            # Query order
            order = session.get(Order, order_id)
            if not order:
                return None

            # Query items (same session)
            items = session.exec(
                select(OrderItem).where(OrderItem.order_id == order_id)
            ).all()

            # Calculate total
            total = sum(item.price * item.quantity for item in items)

            # Update order
            order.total = total
            session.add(order)
            session.commit()
            session.refresh(order)

            return order
        # Session automatically closed (even on exception)
```

**Metrics (After)**:
```
Connection pool: 100 connections
Active connections: 8-12/100 (stable)
Leaked connections: 0/day
Memory growth: 0MB/hour
Pool exhaustion: Never (0 incidents/month)
```

## 6. Connection Pool Configuration Best Practices

### Recommended Settings (Grey Haven Stack)

```python
# database.py - Production settings
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=20,          # (workers * connections/worker) + buffer
    max_overflow=10,       # 50% of pool_size
    pool_timeout=30,       # Wait timeout
    pool_recycle=3600,     # Recycle after 1h
    pool_pre_ping=True     # Health check
)
```

**Pool Size Formula**: `pool_size = (workers * conn_per_worker) + buffer`
Example: `(4 workers * 3 conn) + 8 buffer = 20`

## 7. Testing Connection Cleanup

### Pytest Fixture for Connection Tracking

```python
# tests/conftest.py
import pytest
from sqlmodel import Session, create_engine

@pytest.fixture
def engine():
    """Test engine with connection tracking"""
    test_engine = create_engine("postgresql://test:test@localhost/test_db", pool_size=5)
    initial_active = test_engine.pool.checkedout()
    yield test_engine
    final_active = test_engine.pool.checkedout()
    assert final_active == initial_active, f"Leaked {final_active - initial_active} connections"

@pytest.mark.asyncio
async def test_no_connection_leak_under_load(engine):
    """Simulate 1000 concurrent requests"""
    initial = engine.pool.checkedout()
    tasks = [get_orders() for _ in range(1000)]
    await asyncio.gather(*tasks)
    await asyncio.sleep(1)
    assert engine.pool.checkedout() == initial, "Connection leak detected"
```

## 8. CI/CD Integration

```yaml
# .github/workflows/connection-leak-test.yml
name: Connection Leak Detection
on: [pull_request]
jobs:
  leak-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env: {POSTGRES_PASSWORD: test, POSTGRES_DB: test_db}
        ports: [5432:5432]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt pytest pytest-asyncio
      - run: pytest tests/test_connection_leaks.py -v
```

## 9. Results and Impact

### Before vs After Metrics

| Metric | Before | After | Impact |
|--------|--------|-------|--------|
| **Active Connections** | 95/100 (95%) | 8-12/100 (10%) | **85% reduction** |
| **Connection Timeouts** | 15-20/min | 0/day | **100% eliminated** |
| **Memory Growth** | 100MB/hour | 0MB/hour | **100% eliminated** |
| **Service Restarts** | 3-4x/day | 0/month | **100% eliminated** |
| **Pool Wait Time (p95)** | 5.2s | 0.01s | **99.8% faster** |

### Key Optimizations Applied

1. **Context Managers**: Guaranteed connection cleanup (even on exceptions)
2. **FastAPI Dependencies**: Automatic session lifecycle management
3. **Connection Pooling**: Proper pool_size, max_overflow, pool_timeout
4. **Prometheus Monitoring**: Real-time pool saturation metrics
5. **Load Testing**: CI/CD checks for connection leaks

## Related Documentation

- **Node.js Leaks**: [nodejs-memory-leak.md](nodejs-memory-leak.md)
- **Python Profiling**: [python-scalene-profiling.md](python-scalene-profiling.md)
- **Large Datasets**: [large-dataset-optimization.md](large-dataset-optimization.md)
- **Reference**: [../reference/profiling-tools.md](../reference/profiling-tools.md)

---

Return to [examples index](INDEX.md)
