# Database Optimization Examples

Real-world database performance bottlenecks and their solutions with measurable query time improvements.

## Example 1: N+1 Query Problem

### Problem: Loading Users with Posts

```typescript
// ❌ BEFORE: N+1 queries - 3,500ms for 100 users
async function getUsersWithPosts() {
  // 1 query to get users
  const users = await db.user.findMany();
  
  // N queries (1 per user) to get posts
  for (const user of users) {
    user.posts = await db.post.findMany({
      where: { userId: user.id }
    });
  }
  
  return users;
}

// Total queries: 1 + 100 = 101 queries
// Time: ~3,500ms (35ms per query × 100)
```

### Solution 1: Eager Loading

```typescript
// ✅ AFTER: Eager loading - 80ms for 100 users (44x faster!)
async function getUsersWithPostsOptimized() {
  // Single query with JOIN
  const users = await db.user.findMany({
    include: {
      posts: true
    }
  });
  
  return users;
}

// Total queries: 1 query
// Time: ~80ms
// Performance gain: 44x faster (3,500ms → 80ms)
```

### Solution 2: DataLoader Pattern

```typescript
// ✅ ALTERNATIVE: Batched loading - 120ms for 100 users
import DataLoader from 'dataloader';

const postLoader = new DataLoader(async (userIds: string[]) => {
  const posts = await db.post.findMany({
    where: { userId: { in: userIds } }
  });
  
  // Group posts by userId
  const postsByUser = new Map<string, Post[]>();
  for (const post of posts) {
    if (!postsByUser.has(post.userId)) {
      postsByUser.set(post.userId, []);
    }
    postsByUser.get(post.userId)!.push(post);
  }
  
  // Return in same order as input
  return userIds.map(id => postsByUser.get(id) || []);
});

async function getUsersWithPostsBatched() {
  const users = await db.user.findMany();
  
  // Batches all user IDs into single query
  for (const user of users) {
    user.posts = await postLoader.load(user.id);
  }
  
  return users;
}

// Total queries: 2 queries (users + batched posts)
// Time: ~120ms
```

### Metrics

| Implementation | Queries | Time | Improvement |
|----------------|---------|------|-------------|
| **N+1 (Original)** | 101 | 3,500ms | baseline |
| **Eager Loading** | 1 | 80ms | **44x faster** |
| **DataLoader** | 2 | 120ms | **29x faster** |

---

## Example 2: Missing Index

### Problem: Slow Query on Large Table

```sql
-- ❌ BEFORE: Full table scan - 2,800ms for 1M rows
SELECT * FROM orders
WHERE customer_id = '123'
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;

-- EXPLAIN ANALYZE output:
-- Seq Scan on orders (cost=0.00..25000.00 rows=10 width=100) (actual time=2800.000)
--   Filter: (customer_id = '123' AND status = 'pending')
--   Rows Removed by Filter: 999,990
```

### Solution: Composite Index

```sql
-- ✅ AFTER: Index scan - 5ms for 1M rows (560x faster!)
CREATE INDEX idx_orders_customer_status_date 
ON orders(customer_id, status, created_at DESC);

-- Same query, now uses index:
SELECT * FROM orders
WHERE customer_id = '123'
  AND status = 'pending'
ORDER BY created_at DESC
LIMIT 10;

-- EXPLAIN ANALYZE output:
-- Index Scan using idx_orders_customer_status_date (cost=0.42..8.44 rows=10)
--   (actual time=5.000)
--   Index Cond: (customer_id = '123' AND status = 'pending')
```

### Metrics

| Implementation | Scan Type | Time | Rows Scanned |
|----------------|-----------|------|--------------|
| **No Index** | Sequential | 2,800ms | 1,000,000 |
| **With Index** | Index | 5ms | 10 |
| **Improvement** | - | **560x** | **99.999% less** |

### Index Strategy

```sql
-- Good: Covers WHERE + ORDER BY
CREATE INDEX idx_orders_customer_status_date 
ON orders(customer_id, status, created_at DESC);

-- Bad: Wrong column order (status first is less selective)
CREATE INDEX idx_orders_status_customer 
ON orders(status, customer_id);

-- Good: Partial index for common queries
CREATE INDEX idx_orders_pending 
ON orders(customer_id, created_at DESC)
WHERE status = 'pending';
```

---

## Example 3: SELECT * vs Specific Columns

### Problem: Fetching Unnecessary Data

```typescript
// ❌ BEFORE: Fetching all columns - 450ms for 10K rows
const products = await db.product.findMany({
  where: { category: 'electronics' }
  // Fetches all 30 columns including large JSONB fields
});

// Network transfer: 25 MB
// Time: 450ms (query) + 200ms (network) = 650ms total
```

### Solution: Select Only Needed Columns

```typescript
// ✅ AFTER: Fetch only required columns - 120ms for 10K rows
const products = await db.product.findMany({
  where: { category: 'electronics' },
  select: {
    id: true,
    name: true,
    price: true,
    inStock: true
  }
});

// Network transfer: 2 MB (88% reduction)
// Time: 120ms (query) + 25ms (network) = 145ms total
// Performance gain: 4.5x faster (650ms → 145ms)
```

### Metrics

| Implementation | Columns | Data Size | Total Time |
|----------------|---------|-----------|------------|
| **SELECT *** | 30 | 25 MB | 650ms |
| **Specific Columns** | 4 | 2 MB | 145ms |
| **Improvement** | **87% less** | **88% less** | **4.5x** |

---

## Example 4: Connection Pooling

### Problem: Creating New Connection Per Request

```typescript
// ❌ BEFORE: New connection each request - 150ms overhead
async function handleRequest() {
  // Opens new connection (150ms)
  const client = await pg.connect({
    host: 'db.example.com',
    database: 'myapp'
  });
  
  const result = await client.query('SELECT ...');
  await client.end(); // Closes connection
  
  return result;
}

// Per request: 150ms (connect) + 20ms (query) = 170ms
```

### Solution: Connection Pool

```typescript
// ✅ AFTER: Reuse pooled connections - 20ms per query
import { Pool } from 'pg';

const pool = new Pool({
  host: 'db.example.com',
  database: 'myapp',
  max: 20,              // Max 20 connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

async function handleRequestOptimized() {
  // Reuses existing connection (~0ms overhead)
  const client = await pool.connect();
  
  try {
    const result = await client.query('SELECT ...');
    return result;
  } finally {
    client.release(); // Return to pool
  }
}

// Per request: 0ms (pool) + 20ms (query) = 20ms
// Performance gain: 8.5x faster (170ms → 20ms)
```

### Metrics

| Implementation | Connection Time | Query Time | Total |
|----------------|-----------------|------------|-------|
| **New Connection** | 150ms | 20ms | 170ms |
| **Pooled** | ~0ms | 20ms | 20ms |
| **Improvement** | **∞** | - | **8.5x** |

---

## Example 5: Query Result Caching

### Problem: Repeated Expensive Queries

```typescript
// ❌ BEFORE: Query database every time - 80ms per call
async function getPopularProducts() {
  return await db.product.findMany({
    where: { 
      soldCount: { gte: 1000 }
    },
    orderBy: { soldCount: 'desc' },
    take: 20
  });
}

// Called 100 times/min = 8,000ms database load
```

### Solution: Redis Caching

```typescript
// ✅ AFTER: Cache results - 2ms per cache hit
import { Redis } from 'ioredis';
const redis = new Redis();

async function getPopularProductsCached() {
  const cacheKey = 'popular_products';
  
  // Check cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached); // 2ms cache hit
  }
  
  // Cache miss: query database
  const products = await db.product.findMany({
    where: { soldCount: { gte: 1000 } },
    orderBy: { soldCount: 'desc' },
    take: 20
  });
  
  // Cache for 5 minutes
  await redis.setex(cacheKey, 300, JSON.stringify(products));
  
  return products;
}

// First call: 80ms (database)
// Subsequent calls: 2ms (cache) × 99 = 198ms
// Total: 278ms vs 8,000ms
// Performance gain: 29x faster
```

### Metrics (100 calls)

| Implementation | Cache Hits | DB Queries | Total Time |
|----------------|------------|------------|------------|
| **No Cache** | 0 | 100 | 8,000ms |
| **With Cache** | 99 | 1 | 278ms |
| **Improvement** | - | **99% less** | **29x** |

---

## Example 6: Batch Operations

### Problem: Individual Inserts

```typescript
// ❌ BEFORE: Individual inserts - 5,000ms for 1000 records
async function importUsers(users: User[]) {
  for (const user of users) {
    await db.user.create({ data: user }); // 1000 queries
  }
}

// Time: 5ms per insert × 1000 = 5,000ms
```

### Solution: Batch Insert

```typescript
// ✅ AFTER: Single batch insert - 250ms for 1000 records
async function importUsersOptimized(users: User[]) {
  await db.user.createMany({
    data: users,
    skipDuplicates: true
  });
}

// Time: 250ms (single query with 1000 rows)
// Performance gain: 20x faster (5,000ms → 250ms)
```

### Metrics

| Implementation | Queries | Time | Network Roundtrips |
|----------------|---------|------|-------------------|
| **Individual** | 1,000 | 5,000ms | 1,000 |
| **Batch** | 1 | 250ms | 1 |
| **Improvement** | **1000x less** | **20x** | **1000x less** |

---

## Summary

| Optimization | Before | After | Gain | When to Use |
|--------------|--------|-------|------|-------------|
| **Eager Loading** | 101 queries | 1 query | 44x | N+1 problems |
| **Add Index** | 2,800ms | 5ms | 560x | Slow WHERE/ORDER BY |
| **Select Specific** | 25 MB | 2 MB | 4.5x | Large result sets |
| **Connection Pool** | 170ms/req | 20ms/req | 8.5x | High request volume |
| **Query Cache** | 100 queries | 1 query | 29x | Repeated queries |
| **Batch Operations** | 1000 queries | 1 query | 20x | Bulk inserts/updates |

## Best Practices

1. **Use EXPLAIN ANALYZE**: Always check query execution plans
2. **Index Wisely**: Cover WHERE, JOIN, ORDER BY columns
3. **Eager Load**: Avoid N+1 queries with includes/joins
4. **Connection Pools**: Never create connections per request
5. **Cache Strategically**: Cache expensive, frequently accessed queries
6. **Batch Operations**: Bulk insert/update when possible
7. **Monitor Slow Queries**: Log queries >100ms in production

---

**Previous**: [Algorithm Optimization](algorithm-optimization.md) | **Next**: [Caching Optimization](caching-optimization.md) | **Index**: [Examples Index](INDEX.md)
