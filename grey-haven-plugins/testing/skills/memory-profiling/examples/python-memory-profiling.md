# Python Memory Profiling Example

Real-world example of identifying and fixing a memory leak in a FastAPI application.

## Scenario

A FastAPI background job processes user data exports. After processing 100 exports, memory usage grows from 200MB to 3GB, eventually causing OOM (Out of Memory) crashes.

## Initial Investigation

### Step 1: Install Profiling Tools

```bash
pip install memory-profiler tracemalloc-ng objgraph pympler
```

### Step 2: Enable tracemalloc

**File:** `app/main.py`

```python
import tracemalloc

# Start tracing at application startup
tracemalloc.start()

@app.on_event("startup")
async def startup_event():
    print("Memory tracking started")
    snapshot1 = tracemalloc.take_snapshot()
    app.state.initial_snapshot = snapshot1

@app.get("/api/memory-stats")
async def memory_stats():
    """Debug endpoint to check memory usage"""
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.compare_to(app.state.initial_snapshot, 'lineno')

    stats = []
    for stat in top_stats[:10]:
        stats.append({
            "file": stat.traceback.format()[0],
            "size_mb": stat.size_diff / 1024 / 1024,
            "count": stat.count_diff
        })

    return {"top_allocations": stats}
```

### Step 3: Profile the Export Job

**File:** `app/jobs/export_job.py`

```python
# ❌ BUGGY CODE
from memory_profiler import profile

@profile  # Add this decorator to see line-by-line memory usage
async def export_user_data(user_id: str, tenant_id: str):
    """Export all user data to CSV"""

    # Fetch all user records (could be millions)
    query = select(UserActivity).where(
        UserActivity.user_id == user_id,
        UserActivity.tenant_id == tenant_id
    )
    activities = await session.execute(query)
    all_activities = activities.scalars().all()  # ❌ PROBLEM: Loads ALL into memory

    # Build CSV in memory
    csv_data = []
    csv_data.append(['timestamp', 'action', 'details'])  # Header

    for activity in all_activities:
        csv_data.append([
            activity.timestamp.isoformat(),
            activity.action,
            json.dumps(activity.details)  # ❌ PROBLEM: details can be large JSON
        ])

    # ❌ PROBLEM: Entire CSV built in memory before writing
    csv_content = '\n'.join([','.join(row) for row in csv_data])

    # Write to file
    with open(f'/tmp/export_{user_id}.csv', 'w') as f:
        f.write(csv_content)

    # ❌ PROBLEM: all_activities and csv_data never explicitly cleared
    # They stay in memory until GC runs (which may not be soon)

    return f'/tmp/export_{user_id}.csv'
```

### Step 4: Run with Memory Profiler

```bash
python -m memory_profiler app/jobs/export_job.py
```

**Output:**
```
Line #    Mem usage    Increment  Occurrences   Line Contents
================================================================
    10     50.0 MiB     50.0 MiB           1   async def export_user_data(...):
    15    250.0 MiB    200.0 MiB           1       all_activities = activities.scalars().all()
    18    250.5 MiB      0.5 MiB           1       csv_data = []
    23   1500.0 MiB   1250.0 MiB      100000       for activity in all_activities:
    28   2800.0 MiB   1300.0 MiB           1       csv_content = '\n'.join(...)
    32   2800.0 MiB      0.0 MiB           1       f.write(csv_content)
```

**Analysis:**
- Line 15: 200MB - Loading all activities into memory
- Line 23-27: 1250MB - Building CSV list in memory
- Line 28: 1300MB - Joining entire CSV into string
- **Total: 2750MB for one export!**

### Step 5: Identify Object Retention

```python
import objgraph
import gc

# After export job completes
gc.collect()  # Force garbage collection

# Show most common types
objgraph.show_most_common_types(limit=10)
```

**Output:**
```
dict                      125000
list                       75000
str                       250000
UserActivity              100000  # ❌ Should be 0 after job completes!
```

**Problem:** UserActivity objects not being garbage collected.

### Step 6: Find References

```python
import objgraph

# Find what's holding references to UserActivity
activities = objgraph.by_type('UserActivity')
if activities:
    objgraph.show_backrefs(
        activities[:3],  # Show references for first 3 objects
        filename='backrefs.png',
        max_depth=5
    )
```

**Findings:** UserActivity objects referenced by:
- SQLAlchemy session (not closed)
- csv_data list (not cleared)
- Circular references in activity.details (JSON with nested objects)

## The Fix

### Fixed Code - Streaming Approach

**File:** `app/jobs/export_job.py`

```python
# ✅ FIXED CODE
import csv
from sqlalchemy import select
from sqlalchemy.orm import load_only

async def export_user_data(user_id: str, tenant_id: str):
    """Export user data using streaming to minimize memory usage"""

    output_path = f'/tmp/export_{user_id}.csv'

    # ✅ FIX 1: Use server-side cursor (yield_per)
    # Fetches in batches instead of all at once
    query = (
        select(UserActivity)
        .where(
            UserActivity.user_id == user_id,
            UserActivity.tenant_id == tenant_id
        )
        .execution_options(yield_per=1000)  # Fetch 1000 at a time
        .options(load_only(  # ✅ FIX 2: Only load needed columns
            UserActivity.timestamp,
            UserActivity.action,
            UserActivity.details
        ))
    )

    # ✅ FIX 3: Write directly to file (streaming)
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'action', 'details'])  # Header

        result = await session.execute(query)

        # ✅ FIX 4: Process in batches, clear after each batch
        batch = []
        for activity in result.scalars():
            batch.append([
                activity.timestamp.isoformat(),
                activity.action,
                json.dumps(activity.details)
            ])

            if len(batch) >= 1000:
                writer.writerows(batch)
                batch.clear()  # ✅ FIX 5: Explicitly clear batch
                await session.flush()  # Clear SQLAlchemy cache

        # Write remaining rows
        if batch:
            writer.writerows(batch)
            batch.clear()

    # ✅ FIX 6: Explicitly close session and run GC
    await session.close()
    import gc
    gc.collect()

    return output_path
```

### Additional Fix - Connection Management

**File:** `app/db/session.py`

```python
# ❌ BUGGY CODE
async def get_session():
    session = AsyncSession(engine)
    yield session
    # ❌ PROBLEM: Session not closed on exception

# ✅ FIXED CODE
async def get_session():
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()  # ✅ Always close session
```

### Additional Fix - Background Task Isolation

**File:** `app/api/v1/exports.py`

```python
from fastapi import BackgroundTasks

# ❌ BUGGY CODE
@router.post("/export")
async def create_export(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    # ❌ PROBLEM: Session shared between request and background task
    background_tasks.add_task(export_user_data, user_id, session)
    return {"status": "started"}

# ✅ FIXED CODE
@router.post("/export")
async def create_export(
    user_id: str,
    tenant_id: str,
    background_tasks: BackgroundTasks
):
    # ✅ FIX: Background task creates its own session
    background_tasks.add_task(export_job_wrapper, user_id, tenant_id)
    return {"status": "started"}

async def export_job_wrapper(user_id: str, tenant_id: str):
    """Wrapper that creates isolated session for background job"""
    async with AsyncSession(engine) as session:
        try:
            await export_user_data(user_id, tenant_id, session)
        except Exception as e:
            logger.error(f"Export failed: {e}")
        finally:
            await session.close()
            gc.collect()  # Force cleanup
```

## Verification

### Re-profile with Memory Profiler

```bash
python -m memory_profiler app/jobs/export_job.py
```

**Output (After Fix):**
```
Line #    Mem usage    Increment  Occurrences   Line Contents
================================================================
    10     50.0 MiB     50.0 MiB           1   async def export_user_data(...):
    20     50.5 MiB      0.5 MiB           1       with open(output_path, 'w') as f:
    25     55.0 MiB      4.5 MiB           1           for activity in result.scalars():
    32     75.0 MiB     20.0 MiB         100           if len(batch) >= 1000:
    45     75.0 MiB      0.0 MiB           1       await session.close()
```

**Results:**
- Before fix: 2750MB peak memory
- After fix: 75MB peak memory ✅
- **Memory savings: 97% reduction!**

### Test with 100 Exports

```python
# test_export_memory.py
import pytest
import tracemalloc
import gc

@pytest.mark.asyncio
async def test_export_memory_usage():
    """Verify exports don't leak memory"""

    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()

    # Run 100 exports
    for i in range(100):
        await export_user_data(f"user_{i}", "tenant_123")

    gc.collect()
    snapshot2 = tracemalloc.take_snapshot()

    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    total_growth = sum(stat.size_diff for stat in top_stats)

    # Memory growth should be minimal (<50MB for 100 exports)
    assert total_growth < 50 * 1024 * 1024, \
        f"Memory leak detected: {total_growth / 1024 / 1024:.2f}MB growth"
```

**Results:**
- Before fix: 27GB growth (27MB per export × 100)
- After fix: 15MB growth (150KB per export × 100) ✅

## Key Takeaways

### Common Python Leak Patterns

1. **Loading Too Much Data at Once**
   ```python
   # ❌ Leaks
   all_records = session.query(Model).all()

   # ✅ Fixed (streaming)
   for batch in session.query(Model).yield_per(1000):
       process(batch)
   ```

2. **Not Closing Database Sessions**
   ```python
   # ❌ Leaks
   session = Session()
   # ... do work ...
   # Session never closed!

   # ✅ Fixed
   async with AsyncSession(engine) as session:
       # ... do work ...
       # Automatically closed
   ```

3. **Circular References**
   ```python
   # ❌ Leaks (circular reference prevents GC)
   class Node:
       def __init__(self):
           self.parent = None
           self.children = []

   parent = Node()
   child = Node()
   child.parent = parent
   parent.children.append(child)
   # Circular reference: parent → child → parent

   # ✅ Fixed (use weakref)
   import weakref

   class Node:
       def __init__(self):
           self.parent = None  # Will be weak reference
           self.children = []

   parent = Node()
   child = Node()
   child.parent = weakref.ref(parent)  # Weak reference
   parent.children.append(child)
   ```

4. **Global Caches Without Eviction**
   ```python
   # ❌ Leaks
   CACHE = {}
   def get_data(key):
       if key not in CACHE:
           CACHE[key] = fetch(key)
       return CACHE[key]

   # ✅ Fixed (with LRU cache)
   from functools import lru_cache

   @lru_cache(maxsize=1000)
   def get_data(key):
       return fetch(key)
   ```

### Debugging Tools

**tracemalloc (Built-in):**
```python
import tracemalloc

tracemalloc.start()
# ... code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(f"{stat.traceback}: {stat.size / 1024 / 1024:.2f} MB")
```

**memory_profiler:**
```python
from memory_profiler import profile

@profile
def my_function():
    # Line-by-line memory usage
    pass
```

**objgraph:**
```python
import objgraph

# Show most common objects
objgraph.show_most_common_types()

# Show references to specific object
objgraph.show_backrefs(obj, filename='refs.png')

# Track object growth
objgraph.show_growth()
```

**pympler:**
```python
from pympler import tracker, muppy, summary

# Track memory over time
tr = tracker.SummaryTracker()
# ... code ...
tr.print_diff()

# Detailed memory snapshot
all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)
summary.print_(sum1)
```

### Prevention

1. **Use streaming for large datasets:**
   - `yield_per()` in SQLAlchemy
   - Generators instead of lists
   - Write to file instead of building in memory

2. **Close resources explicitly:**
   - Database sessions
   - File handles
   - Network connections

3. **Use context managers:**
   ```python
   async with AsyncSession(engine) as session:
       # Automatically closed
   ```

4. **Profile regularly:**
   - Add memory tests to CI/CD
   - Monitor production memory
   - Alert on memory growth

5. **Force garbage collection in long-running jobs:**
   ```python
   import gc
   gc.collect()  # Force cleanup
   ```

## Related Resources

- [Memory Leak Checklist](../checklists/memory-leak-checklist.md)
- [Node.js Memory Profiling](./nodejs-memory-profiling.md)
- [Python tracemalloc docs](https://docs.python.org/3/library/tracemalloc.html)
- [memory_profiler](https://pypi.org/project/memory-profiler/)
- [objgraph](https://mg.pov.lt/objgraph/)

---

**Leak Pattern**: Loading too much data + unclosed sessions
**Time to Fix**: 3 hours (investigation + fix + verification)
**Memory Saved**: 2.7GB per export → 75MB per export (97% reduction)
**Impact**: OOM crashes eliminated ✅
