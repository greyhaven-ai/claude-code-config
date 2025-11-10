# Performance Optimization Checklist

Systematic checklist for identifying and fixing performance bottlenecks across frontend, backend, and database.

## Pre-Optimization

- [ ] **Establish baseline metrics** (response times, load times, memory usage)
- [ ] **Identify user-facing issues** (slow pages, timeouts)
- [ ] **Set performance budgets** (< 3s load, < 100ms API response)
- [ ] **Prioritize optimization areas** (database, frontend, backend)
- [ ] **Set up profiling tools** (Chrome DevTools, Node.js inspector, APM)

## Frontend Performance (React/TypeScript)

### Bundle Size
- [ ] **Bundle analyzed** (use webpack-bundle-analyzer)
- [ ] **Code splitting implemented** (route-based, component-based)
- [ ] **Tree shaking working** (no unused code shipped)
- [ ] **Dependencies optimized** (no duplicate dependencies)
- [ ] **Total bundle < 200KB gzipped**

### React Optimization
- [ ] **useMemo** for expensive computations
- [ ] **useCallback** for functions passed as props
- [ ] **React.memo** for components that re-render unnecessarily
- [ ] **Virtual scrolling** for long lists (react-window, tanstack-virtual)
- [ ] **Lazy loading** for offscreen components

### Images & Assets
- [ ] **Images optimized** (WebP format, appropriate sizes)
- [ ] **Lazy loading** for below-fold images
- [ ] **Responsive images** (srcset, picture element)
- [ ] **SVG sprites** for icons
- [ ] **CDN used** for static assets

### Loading Performance
- [ ] **Critical CSS inlined**
- [ ] **Fonts preloaded** (font-display: swap)
- [ ] **Prefetch/preconnect** for critical resources
- [ ] **Service worker** for offline support (if applicable)
- [ ] **First Contentful Paint < 1.8s**
- [ ] **Largest Contentful Paint < 2.5s**
- [ ] **Time to Interactive < 3.8s**

### Runtime Performance
- [ ] **No layout thrashing** (batch DOM reads/writes)
- [ ] **RequestAnimationFrame** for animations
- [ ] **Debounce/throttle** for frequent events
- [ ] **Web Workers** for heavy computations
- [ ] **Frame rate stable** (60fps)

## Backend Performance (Node.js/Python)

### API Response Times
- [ ] **Endpoints respond < 100ms** (simple queries)
- [ ] **Endpoints respond < 500ms** (complex operations)
- [ ] **Timeout configured** (prevent hanging requests)
- [ ] **Connection pooling** enabled
- [ ] **Keep-alive** connections used

### Caching
- [ ] **HTTP caching headers** set (Cache-Control, ETag)
- [ ] **Redis caching** for expensive queries
- [ ] **Memory caching** for frequently accessed data
- [ ] **Cache invalidation** strategy defined
- [ ] **CDN caching** for static content

### Async Operations
- [ ] **Async/await** used instead of blocking operations
- [ ] **Promise.all** for parallel operations
- [ ] **Background jobs** for heavy tasks (queues)
- [ ] **Rate limiting** to prevent overload
- [ ] **Circuit breakers** for external services

### Node.js Specific
- [ ] **Cluster mode** for multi-core utilization
- [ ] **V8 heap size** optimized (--max-old-space-size)
- [ ] **GC tuning** if needed
- [ ] **No synchronous file operations**

### Python Specific
- [ ] **Async endpoints** (async def) for I/O operations
- [ ] **uvicorn workers** configured (multi-process)
- [ ] **Connection pooling** for database
- [ ] **Pydantic models** compiled (v2 for performance)

## Database Performance

### Query Optimization
- [ ] **No N+1 queries** (use joins, eager loading)
- [ ] **Indexes on frequently queried columns**
- [ ] **Indexes on foreign keys**
- [ ] **Composite indexes** for multi-column queries
- [ ] **Query execution plans analyzed** (EXPLAIN)
- [ ] **Slow query log reviewed**

### Data Structure
- [ ] **Appropriate data types** (INT vs BIGINT, VARCHAR length)
- [ ] **Normalization level appropriate** (balance between normalization and performance)
- [ ] **Denormalization** where read performance critical
- [ ] **Partitioning** for large tables

### Database Configuration
- [ ] **Connection pooling** configured
- [ ] **Max connections** tuned
- [ ] **Query cache** enabled (if applicable)
- [ ] **Shared buffers** optimized
- [ ] **Work memory** tuned

### PostgreSQL Specific
- [ ] **VACUUM** running regularly
- [ ] **ANALYZE** statistics up to date
- [ ] **Appropriate indexes** (B-tree, GiST, GIN)
- [ ] **RLS policies** not causing performance issues

## Algorithms & Data Structures

### Complexity Analysis
- [ ] **Time complexity acceptable** (avoid O(n²) for large n)
- [ ] **Space complexity acceptable** (no exponential memory usage)
- [ ] **Appropriate data structures** (Map vs Array, Set vs Array)
- [ ] **No unnecessary iterations**

### Common Optimizations
- [ ] **Hash maps** for O(1) lookups instead of arrays
- [ ] **Early termination** in loops when result found
- [ ] **Binary search** instead of linear search
- [ ] **Memoization** for recursive functions
- [ ] **Dynamic programming** for overlapping subproblems

## Memory Optimization

### Memory Leaks
- [ ] **No memory leaks** (event listeners removed)
- [ ] **Timers cleared** (setInterval, setTimeout)
- [ ] **Weak references** used where appropriate (WeakMap)
- [ ] **Large objects released** when done
- [ ] **Memory profiling done** (heap snapshots)

### Memory Usage
- [ ] **Streams used** for large files
- [ ] **Pagination** for large datasets
- [ ] **Object pooling** for frequently created objects
- [ ] **Lazy loading** for large data structures

## Network Performance

### API Design
- [ ] **GraphQL/REST batching** for multiple queries
- [ ] **Compression enabled** (gzip, brotli)
- [ ] **HTTP/2** or HTTP/3 used
- [ ] **Payload size minimized** (no over-fetching)
- [ ] **WebSockets** for real-time updates (not polling)

### Third-Party Services
- [ ] **Timeout configured** for external APIs
- [ ] **Retry logic** for transient failures
- [ ] **Circuit breaker** for failing services
- [ ] **Fallback data** when service unavailable

## Monitoring & Metrics

### Application Monitoring
- [ ] **APM installed** (New Relic, DataDog, Sentry Performance)
- [ ] **Response time tracked** per endpoint
- [ ] **Error rates monitored**
- [ ] **Custom metrics** for business logic
- [ ] **Alerts configured** for degradation

### User Monitoring
- [ ] **Real User Monitoring** (RUM) enabled
- [ ] **Core Web Vitals tracked**
- [ ] **Lighthouse CI** in pipeline
- [ ] **Performance budget enforced**

## Testing Performance

### Load Testing
- [ ] **Load tests written** (k6, Artillery, Locust)
- [ ] **Baseline established** (requests/second)
- [ ] **Tested under load** (50%, 100%, 150% capacity)
- [ ] **Stress tested** (find breaking point)
- [ ] **Results documented**

### Continuous Performance Testing
- [ ] **Performance tests in CI**
- [ ] **Regression detection** (alert if slower)
- [ ] **Budget enforcement** (fail build if budget exceeded)

## Scoring

- **90+ items checked**: Excellent - Well optimized ✅
- **75-89 items**: Good - Most optimizations in place ⚠️
- **60-74 items**: Fair - Significant optimization needed 🔴
- **<60 items**: Poor - Performance issues likely ❌

## Priority Optimizations

Start with these high-impact items:
1. **Database N+1 queries** - Biggest performance killer
2. **Missing indexes** - Immediate improvement
3. **Bundle size** - Major impact on load time
4. **API caching** - Reduce server load
5. **Image optimization** - Faster page loads

## Performance Budgets

### Frontend
- Total bundle size: < 200KB gzipped
- FCP (First Contentful Paint): < 1.8s
- LCP (Largest Contentful Paint): < 2.5s
- TTI (Time to Interactive): < 3.8s
- CLS (Cumulative Layout Shift): < 0.1

### Backend
- Simple API endpoints: < 100ms
- Complex API endpoints: < 500ms
- Database queries: < 50ms (simple), < 200ms (complex)

### Database
- Query execution time: < 50ms for 95th percentile
- Connection pool utilization: < 80%
- Slow queries: 0 queries > 1s

## Tools Reference

**Frontend:**
- Chrome DevTools Performance panel
- Lighthouse
- WebPageTest
- Webpack Bundle Analyzer

**Backend:**
- Node.js Inspector
- clinic.js (Doctor, Flame, Bubbleprof)
- Python cProfile
- FastAPI profiling middleware

**Database:**
- EXPLAIN/EXPLAIN ANALYZE
- pg_stat_statements (PostgreSQL)
- Slow query log

**Load Testing:**
- k6
- Artillery
- Apache JMeter
- Locust (Python)

## Related Resources

- [Algorithm Optimization Examples](../examples/algorithm-optimization.md)
- [Database Optimization Guide](../examples/database-optimization.md)
- [Frontend Optimization](../examples/frontend-optimization.md)
- [Memory Profiling](../../memory-profiling/SKILL.md)

---

**Total Items**: 120+ performance checks
**Critical Items**: N+1 queries, Indexes, Bundle size, Caching
**Last Updated**: 2025-11-09
