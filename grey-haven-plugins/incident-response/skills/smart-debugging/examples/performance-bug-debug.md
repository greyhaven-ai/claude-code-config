# Performance Bug Debug Example

Debugging slow database queries and N+1 problems.

## Symptom

API endpoint taking 4.5 seconds to respond (target: < 200ms).

## Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

response = await get_users_with_posts()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Profile Output

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      100    4.321    0.043    4.321    0.043 database.py:42(execute_query)
        1    0.089    0.089    4.410    4.410 users.py:15(get_users_with_posts)
```

**Issue**: Database query called 100 times! (N+1 problem)

## Code Analysis

```python
# BAD: N+1 Query Problem
async def get_users_with_posts():
    users = await db.users.find_all()  # 1 query

    result = []
    for user in users:  # 100 iterations
        posts = await db.posts.find({"user_id": user.id})  # N queries!
        result.append({"user": user, "posts": posts})

    return result  # Total: 101 queries (1 + 100)
```

## Fix: Use Join/Eager Loading

```python
# GOOD: Single Query with Join
async def get_users_with_posts():
    query = """
        SELECT
            users.*,
            json_agg(posts.*) as posts
        FROM users
        LEFT JOIN posts ON posts.user_id = users.id
        GROUP BY users.id
    """
    result = await db.execute(query)  # 1 query total!
    return result
```

## Performance Comparison

| Approach | Queries | Time |
|----------|---------|------|
| **Before (N+1)** | 101 | 4.5s ❌ |
| **After (Join)** | 1 | 85ms ✅ |

**Improvement**: 53x faster!

## Prevention

1. **Query logging**: Log all database queries in development
2. **Performance tests**: Assert query count < threshold
3. **APM monitoring**: Track query patterns in production (Datadog, New Relic)

```python
# Performance test
def test_get_users_with_posts_query_count(query_counter):
    get_users_with_posts()
    assert query_counter.count <= 1, f"Expected 1 query, got {query_counter.count}"
```

---

**Result**: N+1 detected and fixed. Performance SLA met (< 200ms).
