# Optimization Patterns Catalog

Proven patterns for common performance bottlenecks.

## Algorithm Patterns

### 1. Map Lookup
**Problem**: O(n²) nested loops  
**Solution**: O(n) with Map  
**Gain**: 100-1000x faster

```typescript
// Before: O(n²)
items.forEach(item => {
  const related = items.find(i => i.id === item.relatedId);
});

// After: O(n)
const map = new Map(items.map(i => [i.id, i]));
items.forEach(item => {
  const related = map.get(item.relatedId);
});
```

### 2. Memoization
**Problem**: Repeated expensive calculations  
**Solution**: Cache results  
**Gain**: 10-100x faster

```typescript
const memo = new Map();
function fibonacci(n) {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n);
  const result = fibonacci(n - 1) + fibonacci(n - 2);
  memo.set(n, result);
  return result;
}
```

---

## Database Patterns

### 1. Eager Loading
**Problem**: N+1 queries  
**Solution**: JOIN or include relations  
**Gain**: 10-100x fewer queries

```typescript
// Before: N+1
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// After: 1 query
const users = await User.findAll({ include: ['posts'] });
```

### 2. Composite Index
**Problem**: Slow WHERE + ORDER BY  
**Solution**: Multi-column index  
**Gain**: 100-1000x faster

```sql
CREATE INDEX idx_orders_customer_status_date 
ON orders(customer_id, status, created_at DESC);
```

---

## Caching Patterns

### 1. Cache-Aside
**Problem**: Database load  
**Solution**: Check cache, fallback to DB  
**Gain**: 5-50x faster

```typescript
async function get(key) {
  let value = cache.get(key);
  if (!value) {
    value = await db.get(key);
    cache.set(key, value);
  }
  return value;
}
```

### 2. Write-Through
**Problem**: Cache staleness  
**Solution**: Write to cache and DB  
**Gain**: Always fresh cache

```typescript
async function set(key, value) {
  await db.set(key, value);
  cache.set(key, value);
}
```

---

## Frontend Patterns

### 1. Code Splitting
**Problem**: Large bundle  
**Solution**: Dynamic imports  
**Gain**: 2-10x faster initial load

```typescript
const Component = lazy(() => import('./Component'));
```

### 2. Virtual Scrolling
**Problem**: Large lists  
**Solution**: Render only visible items  
**Gain**: 10-100x less DOM

```typescript
<FixedSizeList itemCount={10000} itemSize={50} height={600} />
```

---

## Backend Patterns

### 1. Connection Pooling
**Problem**: Connection overhead  
**Solution**: Reuse connections  
**Gain**: 5-10x faster

```typescript
const pool = new Pool({ max: 20 });
```

### 2. Request Batching
**Problem**: Too many small requests  
**Solution**: Batch multiple requests  
**Gain**: 10-100x fewer calls

```typescript
const batch = users.map(u => u.id);
const results = await api.getBatch(batch);
```

---

**Previous**: [Profiling Tools](profiling-tools.md) | **Index**: [Reference Index](INDEX.md)
