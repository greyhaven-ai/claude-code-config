# Caching Optimization Examples

Real-world caching strategies to eliminate redundant computations and reduce latency with measurable cache hit rates.

## Example 1: In-Memory Function Cache

### Problem: Expensive Computation

```typescript
// ❌ BEFORE: Recalculates every time - 250ms per call
function calculateComplexMetrics(userId: string) {
  // Expensive calculation: database queries + computation
  const userData = db.user.findUnique({ where: { id: userId } });
  const posts = db.post.findMany({ where: { userId } });
  const comments = db.comment.findMany({ where: { userId } });
  
  // Complex aggregations
  return {
    totalEngagement: calculateEngagement(posts, comments),
    averageScore: calculateScores(posts),
    trendingTopics: analyzeTrends(posts, comments)
  };
}

// Called 100 times/minute = 25,000ms computation time
```

### Solution: LRU Cache with TTL

```typescript
// ✅ AFTER: Cache results - 2ms per cache hit
import LRU from 'lru-cache';

const cache = new LRU<string, MetricsResult>({
  max: 500,              // Max 500 entries
  ttl: 1000 * 60 * 5,   // 5 minute TTL
  updateAgeOnGet: true   // Reset TTL on access
});

function calculateComplexMetricsCached(userId: string) {
  // Check cache first
  const cached = cache.get(userId);
  if (cached) {
    return cached; // 2ms cache hit
  }
  
  // Cache miss: calculate and store
  const result = calculateComplexMetrics(userId);
  cache.set(userId, result);
  
  return result;
}

// First call: 250ms (calculation)
// Subsequent calls (within 5 min): 2ms (cache) × 99 = 198ms
// Total: 448ms vs 25,000ms
// Performance gain: 56x faster
```

### Metrics (100 calls, 90% cache hit rate)

| Implementation | Calculations | Total Time | Avg Response |
|----------------|--------------|------------|--------------|
| **No Cache** | 100 | 25,000ms | 250ms |
| **With Cache** | 10 | 2,680ms | 27ms |
| **Improvement** | **90% less** | **9.3x** | **9.3x** |

---

## Example 2: Redis Distributed Cache

### Problem: API Rate Limits

```typescript
// ❌ BEFORE: External API call every time - 450ms per call
async function getGitHubUserData(username: string) {
  const response = await fetch(`https://api.github.com/users/${username}`);
  return response.json();
}

// API limit: 60 requests/hour
// Average response: 450ms
// Risk: Rate limit errors
```

### Solution: Redis Caching Layer

```typescript
// ✅ AFTER: Cache in Redis - 15ms per cache hit
import { createClient } from 'redis';

const redis = createClient();
await redis.connect();

async function getGitHubUserDataCached(username: string) {
  const cacheKey = `github:user:${username}`;
  
  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached); // 15ms cache hit
  }
  
  // Cache miss: call API
  const response = await fetch(`https://api.github.com/users/${username}`);
  const data = await response.json();
  
  // Cache for 1 hour
  await redis.setex(cacheKey, 3600, JSON.stringify(data));
  
  return data;
}

// First call: 450ms (API) + 5ms (cache write) = 455ms
// Subsequent calls: 15ms (cache read)
// Performance gain: 30x faster
```

### Metrics (1000 calls, 95% cache hit rate)

| Implementation | API Calls | Redis Hits | Total Time | Cost |
|----------------|-----------|------------|------------|------|
| **No Cache** | 1000 | 0 | 450,000ms | High |
| **With Cache** | 50 | 950 | 36,750ms | Low |
| **Improvement** | **95% less** | - | **12.2x** | **95% less** |

### Cache Invalidation Strategy

```typescript
// Update cache when data changes
async function updateGitHubUserCache(username: string) {
  const cacheKey = `github:user:${username}`;
  const response = await fetch(`https://api.github.com/users/${username}`);
  const data = await response.json();
  
  // Update cache
  await redis.setex(cacheKey, 3600, JSON.stringify(data));
  
  return data;
}

// Invalidate on webhook
app.post('/webhook/github', async (req, res) => {
  const { username } = req.body;
  await redis.del(`github:user:${username}`); // Clear cache
  res.send('OK');
});
```

---

## Example 3: HTTP Caching Headers

### Problem: Static Assets Re-downloaded

```typescript
// ❌ BEFORE: No caching headers - 2MB download every request
app.get('/assets/bundle.js', (req, res) => {
  res.sendFile('dist/bundle.js');
});

// Every page load: 2MB download × 1000 users/hour = 2GB bandwidth
// Load time: 800ms on slow connection
```

### Solution: Aggressive HTTP Caching

```typescript
// ✅ AFTER: Cache with hash-based filename - 0ms after first load
app.get('/assets/:filename', (req, res) => {
  const file = `dist/${req.params.filename}`;
  
  // Immutable files (with hash in filename)
  if (req.params.filename.match(/\.[a-f0-9]{8}\./)) {
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  } else {
    // Regular files
    res.setHeader('Cache-Control', 'public, max-age=3600');
  }
  
  res.setHeader('ETag', generateETag(file));
  res.sendFile(file);
});

// First load: 800ms (download)
// Subsequent loads: 0ms (browser cache)
// Bandwidth saved: 99% (conditional requests return 304)
```

### Metrics (1000 page loads)

| Implementation | Downloads | Bandwidth | Avg Load Time |
|----------------|-----------|-----------|---------------|
| **No Cache** | 1000 | 2 GB | 800ms |
| **With Cache** | 10 | 20 MB | 8ms |
| **Improvement** | **99% less** | **99% less** | **100x** |

---

## Example 4: Cache-Aside Pattern

### Problem: Database Under Load

```typescript
// ❌ BEFORE: Every request hits database - 150ms per query
async function getProductById(id: string) {
  return await db.product.findUnique({
    where: { id },
    include: { category: true, reviews: true }
  });
}

// 1000 requests/min = 150,000ms database load
```

### Solution: Cache-Aside with Stale-While-Revalidate

```typescript
// ✅ AFTER: Cache with background refresh - 5ms typical response
interface CachedData<T> {
  data: T;
  cachedAt: number;
  staleAt: number;
}

class CacheAside<T> {
  private cache = new Map<string, CachedData<T>>();
  
  constructor(
    private fetchFn: (key: string) => Promise<T>,
    private ttl = 60000,      // 1 minute fresh
    private staleTtl = 300000 // 5 minutes stale
  ) {}
  
  async get(key: string): Promise<T> {
    const cached = this.cache.get(key);
    const now = Date.now();
    
    if (cached) {
      // Fresh: return immediately
      if (now < cached.staleAt) {
        return cached.data;
      }
      
      // Stale: return old data, refresh in background
      this.refreshInBackground(key);
      return cached.data;
    }
    
    // Miss: fetch and cache
    const data = await this.fetchFn(key);
    this.cache.set(key, {
      data,
      cachedAt: now,
      staleAt: now + this.ttl
    });
    
    return data;
  }
  
  private async refreshInBackground(key: string) {
    try {
      const data = await this.fetchFn(key);
      const now = Date.now();
      this.cache.set(key, {
        data,
        cachedAt: now,
        staleAt: now + this.ttl
      });
    } catch (error) {
      console.error('Background refresh failed:', error);
    }
  }
}

const productCache = new CacheAside(
  (id) => db.product.findUnique({ where: { id }, include: {...} }),
  60000,   // Fresh for 1 minute
  300000   // Serve stale for 5 minutes
);

async function getProductByIdCached(id: string) {
  return await productCache.get(id);
}

// Fresh data: 5ms (cache)
// Stale data: 5ms (cache) + background refresh
// Cache miss: 150ms (database)
// Average: ~10ms (95% cache hit rate)
```

### Metrics (1000 requests/min)

| Implementation | DB Queries | Avg Response | P95 Response |
|----------------|------------|--------------|--------------|
| **No Cache** | 1000 | 150ms | 200ms |
| **Cache-Aside** | 50 | 10ms | 15ms |
| **Improvement** | **95% less** | **15x** | **13x** |

---

## Example 5: Query Result Cache

### Problem: Expensive Aggregation

```typescript
// ❌ BEFORE: Aggregation on every request - 1,200ms
async function getDashboardStats() {
  const [
    totalUsers,
    activeUsers,
    totalOrders,
    revenue
  ] = await Promise.all([
    db.user.count(),
    db.user.count({ where: { lastActiveAt: { gte: new Date(Date.now() - 86400000) } } }),
    db.order.count(),
    db.order.aggregate({ _sum: { total: true } })
  ]);
  
  return { totalUsers, activeUsers, totalOrders, revenue: revenue._sum.total };
}

// Called every dashboard load: 1,200ms
```

### Solution: Materialized View with Periodic Refresh

```typescript
// ✅ AFTER: Pre-computed stats - 2ms per read
interface DashboardStats {
  totalUsers: number;
  activeUsers: number;
  totalOrders: number;
  revenue: number;
  lastUpdated: Date;
}

let cachedStats: DashboardStats | null = null;

// Background job: Update every 5 minutes
setInterval(async () => {
  const stats = await calculateDashboardStats();
  cachedStats = {
    ...stats,
    lastUpdated: new Date()
  };
}, 300000); // 5 minutes

async function getDashboardStatsCached(): Promise<DashboardStats> {
  if (!cachedStats) {
    // First run: calculate immediately
    const stats = await calculateDashboardStats();
    cachedStats = {
      ...stats,
      lastUpdated: new Date()
    };
  }
  
  return cachedStats; // 2ms read from memory
}

// Read time: 2ms (vs 1,200ms)
// Performance gain: 600x faster
```

### Metrics

| Implementation | Computation | Read Time | Freshness |
|----------------|-------------|-----------|-----------|
| **Real-time** | Every request | 1,200ms | Live |
| **Cached** | Every 5 min | 2ms | 5 min stale |
| **Improvement** | **Scheduled** | **600x** | Acceptable |

---

## Summary

| Strategy | Use Case | Cache Hit Response | Best For |
|----------|----------|-------------------|----------|
| **In-Memory LRU** | Function results | 2ms | Single-server apps |
| **Redis** | Distributed caching | 15ms | Multi-server apps |
| **HTTP Cache** | Static assets | 0ms | CDN-cacheable content |
| **Cache-Aside** | Database queries | 5ms | Frequently accessed data |
| **Materialized View** | Aggregations | 2ms | Expensive computations |

## Cache Hit Rate Targets

- **Excellent**: >90% hit rate
- **Good**: 70-90% hit rate
- **Poor**: <70% hit rate

## Best Practices

1. **Set Appropriate TTL**: Balance freshness vs performance
2. **Cache Invalidation**: Clear cache when data changes
3. **Monitor Hit Rates**: Track cache effectiveness
4. **Handle Cache Stampede**: Use locks for simultaneous cache misses
5. **Size Limits**: Use LRU eviction for memory-bounded caches
6. **Fallback**: Always handle cache failures gracefully

---

**Previous**: [Database Optimization](database-optimization.md) | **Next**: [Frontend Optimization](frontend-optimization.md) | **Index**: [Examples Index](INDEX.md)
