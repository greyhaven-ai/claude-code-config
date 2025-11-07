# Performance Optimization Examples

Real-world examples of performance bottlenecks and their optimizations across different layers.

## Examples Overview

### Algorithm Optimization
**File**: [algorithm-optimization.md](algorithm-optimization.md)

Fix algorithmic bottlenecks:
- Nested loops O(n²) → Map lookups O(n)
- Inefficient array operations
- Sorting and searching optimizations
- Data structure selection (Array vs Set vs Map)
- Before/after performance metrics

**Use when**: Profiling shows slow computational operations, CPU-intensive tasks.

---

### Database Optimization
**File**: [database-optimization.md](database-optimization.md)

Optimize database queries and patterns:
- N+1 query problem detection and fixes
- Eager loading vs lazy loading
- Query optimization with EXPLAIN ANALYZE
- Index strategy (single, composite, partial)
- Connection pooling
- Query result caching

**Use when**: Database queries are slow, high database CPU usage, query timeouts.

---

### Caching Optimization
**File**: [caching-optimization.md](caching-optimization.md)

Implement effective caching strategies:
- In-memory caching patterns
- Redis distributed caching
- HTTP caching headers
- Cache invalidation strategies
- Cache hit rate optimization
- TTL tuning

**Use when**: Repeated expensive computations, external API calls, static data queries.

---

### Frontend Optimization
**File**: [frontend-optimization.md](frontend-optimization.md)

Optimize React/frontend performance:
- Bundle size reduction (code splitting, tree shaking)
- React rendering optimization (memo, useMemo, useCallback)
- Virtual scrolling for long lists
- Image optimization (lazy loading, WebP, responsive images)
- Web Vitals improvement (LCP, FID, CLS)

**Use when**: Slow page load, large bundle sizes, poor Web Vitals scores.

---

### Backend Optimization
**File**: [backend-optimization.md](backend-optimization.md)

Optimize server-side performance:
- Async/parallel processing patterns
- Stream processing for large data
- Request batching and debouncing
- Worker threads for CPU-intensive tasks
- Memory leak prevention
- Connection pooling

**Use when**: High server response times, memory leaks, CPU bottlenecks.

---

## Quick Reference

| Optimization Type | Common Gains | Typical Fixes |
|-------------------|--------------|---------------|
| **Algorithm** | 50-90% faster | O(n²) → O(n), better data structures |
| **Database** | 60-95% faster | Indexes, eager loading, caching |
| **Caching** | 80-99% faster | Redis, in-memory, HTTP headers |
| **Frontend** | 40-70% faster | Code splitting, lazy loading, memoization |
| **Backend** | 50-80% faster | Async processing, streaming, pooling |

## Performance Impact Guide

### High Impact (>50% improvement)
- Fix N+1 queries
- Add missing indexes
- Implement caching layer
- Fix O(n²) algorithms
- Enable code splitting

### Medium Impact (20-50% improvement)
- Optimize React rendering
- Add connection pooling
- Implement lazy loading
- Batch API requests
- Optimize images

### Low Impact (<20% improvement)
- Minify assets
- Enable gzip compression
- Optimize CSS selectors
- Reduce HTTP headers

## Navigation

- **Reference**: [Reference Index](../reference/INDEX.md)
- **Templates**: [Templates Index](../templates/INDEX.md)
- **Main Agent**: [performance-optimizer.md](../performance-optimizer.md)

---

Return to [main agent](../performance-optimizer.md)
