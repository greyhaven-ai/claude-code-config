---
name: grey-haven-performance
description: Optimize Grey Haven applications for performance - React rendering, TanStack Query caching, database queries (N+1 prevention), connection pooling, Cloudflare caching, lazy loading, and bundle size optimization. Use when performance issues detected.
---

# Grey Haven Performance Optimization

Optimize **frontend and backend performance** for Grey Haven Studio applications following proven patterns for React, TanStack Query, database queries, and Cloudflare Workers.

## Performance Categories

### Frontend Performance
- **React rendering**: useMemo, React.memo, useCallback
- **TanStack Query**: Caching, prefetching, staleTime optimization
- **Bundle size**: Code splitting, lazy loading, tree shaking
- **Asset optimization**: Image optimization, font loading

### Backend Performance
- **Database queries**: N+1 prevention, connection pooling, indexes
- **API response time**: Caching, pagination, parallel queries
- **FastAPI optimization**: Async/await, dependency caching
- **Cloudflare Workers**: Edge caching, KV storage, R2

## Critical Patterns

### 1. React Rendering Optimization

**useMemo for Expensive Calculations**:
```typescript
// ❌ Bad - Recalculates on every render
const filtered = data?.filter(item => item.active);

// ✅ Good - Memoize expensive calculation
const filtered = useMemo(
  () => data?.filter(item => item.active) ?? [],
  [data]
);
```

**React.memo for Component Memoization**:
```typescript
// ✅ Only re-renders when props change
export const UserCard = memo(function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>;
});
```

### 2. TanStack Query Caching

**Optimal staleTime Configuration**:
```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,  // 5 minutes
      gcTime: 1000 * 60 * 10,     // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});
```

**Query Prefetching**:
```typescript
// Prefetch on hover for instant navigation
queryClient.prefetchQuery({
  queryKey: ["user", userId],
  queryFn: () => fetchUser(userId),
});
```

### 3. Database Query Optimization

**N+1 Prevention**:
```python
# ❌ Bad - N+1 query problem
users = await session.execute(select(User))
for user in users:
    # Additional query for each user!
    posts = await session.execute(
        select(Post).where(Post.user_id == user.id)
    )

# ✅ Good - Single query with join
users = await session.execute(
    select(User).options(selectinload(User.posts))
)
```

**Connection Pooling**:
```python
# Database engine with connection pool
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Max connections
    max_overflow=10,       # Additional connections
    pool_pre_ping=True,    # Verify connections
    pool_recycle=3600,     # Recycle after 1 hour
)
```

### 4. Cloudflare Workers Caching

**Edge Caching**:
```typescript
// Cache at Cloudflare edge
const response = await fetch(request);
return new Response(response.body, {
  headers: {
    "Cache-Control": "public, max-age=300", // 5 minutes
  },
});
```

**KV Storage**:
```typescript
// Use KV for frequently accessed data
const cachedData = await env.KV.get("key");
if (cachedData) return JSON.parse(cachedData);

const data = await fetchData();
await env.KV.put("key", JSON.stringify(data), {
  expirationTtl: 300, // 5 minutes
});
```

### 5. Bundle Size Optimization

**Code Splitting**:
```typescript
// Lazy load heavy components
const HeavyChart = lazy(() => import("./HeavyChart"));

function Dashboard() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyChart data={data} />
    </Suspense>
  );
}
```

**Tree Shaking**:
```typescript
// ❌ Bad - Imports entire library
import _ from "lodash";

// ✅ Good - Import only what you need
import { debounce } from "lodash-es";
```

## Performance Metrics

Track these key metrics:

| Metric | Target | Tool |
|--------|--------|------|
| First Contentful Paint (FCP) | < 1.8s | Lighthouse |
| Largest Contentful Paint (LCP) | < 2.5s | Lighthouse |
| Time to Interactive (TTI) | < 3.8s | Lighthouse |
| Cumulative Layout Shift (CLS) | < 0.1 | Lighthouse |
| API Response Time | < 200ms | Application logs |
| Database Query Time | < 50ms | Query profiler |
| Bundle Size | < 200KB | Webpack analyzer |

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete optimization examples
  - [react-optimization.md](examples/react-optimization.md) - React rendering patterns
  - [tanstack-query-optimization.md](examples/tanstack-query-optimization.md) - Query caching
  - [database-optimization.md](examples/database-optimization.md) - N+1 prevention
  - [cloudflare-optimization.md](examples/cloudflare-optimization.md) - Edge caching
  - [bundle-optimization.md](examples/bundle-optimization.md) - Code splitting
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Performance references
  - [metrics.md](reference/metrics.md) - Performance metrics and targets
  - [profiling.md](reference/profiling.md) - Profiling tools and techniques
  - [caching-strategies.md](reference/caching-strategies.md) - Caching patterns
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[checklists/](checklists/)** - Performance checklists
  - [performance-checklist.md](checklists/performance-checklist.md) - Pre-deployment checklist

## When to Apply This Skill

Use this skill when:
- Page load times exceed 3 seconds
- API response times exceed 200ms
- Database queries take longer than 50ms
- Bundle size exceeds 200KB
- Users report slow performance
- Lighthouse scores below 90
- Preparing for production deployment
- Optimizing for mobile devices

## Template Reference

These patterns are from Grey Haven's production templates:
- **cvi-template**: TanStack Start + React 19 (optimized for performance)
- **cvi-backend-template**: FastAPI + SQLModel (with connection pooling)

## Critical Reminders

1. **useMemo**: Memoize expensive calculations
2. **React.memo**: Memoize components that render frequently
3. **useCallback**: Stable function references for callbacks
4. **staleTime**: Set appropriate cache duration (5 minutes default)
5. **Prefetch**: Prefetch on hover for instant navigation
6. **N+1 prevention**: Use joins or selectinload
7. **Connection pooling**: Configure pool_size and max_overflow
8. **Edge caching**: Use Cache-Control headers
9. **Code splitting**: Lazy load heavy components
10. **Monitor metrics**: Track FCP, LCP, TTI, CLS, API times
