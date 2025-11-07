# Performance Optimization Reference

Reference materials for performance metrics, profiling tools, and optimization patterns.

## Reference Materials

### Performance Metrics
**File**: [performance-metrics.md](performance-metrics.md)

Complete guide to measuring and tracking performance:
- Web Vitals (LCP, FID, CLS, TTFB)
- Backend metrics (latency, throughput, error rate)
- Database metrics (query time, connection pool)
- Memory metrics (heap size, garbage collection)
- Lighthouse scores and interpretation

**Use when**: Setting up monitoring, establishing performance budgets, tracking improvements.

---

### Profiling Tools
**File**: [profiling-tools.md](profiling-tools.md)

Tools for identifying performance bottlenecks:
- Chrome DevTools (Performance, Memory, Network panels)
- Node.js profiling (--inspect, clinic.js, 0x)
- React DevTools Profiler
- Database query analyzers (EXPLAIN, pg_stat_statements)
- APM tools (DataDog, New Relic, Sentry)

**Use when**: Investigating slow performance, finding bottlenecks, profiling before optimization.

---

### Optimization Patterns
**File**: [optimization-patterns.md](optimization-patterns.md)

Catalog of common optimization patterns:
- Algorithm patterns (Map lookup, binary search, memoization)
- Database patterns (eager loading, indexing, caching)
- Caching patterns (LRU, cache-aside, write-through)
- Frontend patterns (lazy loading, code splitting, virtualization)
- Backend patterns (pooling, batching, streaming)

**Use when**: Looking for proven solutions, learning optimization techniques.

---

## Quick Reference

| Resource | Focus | Primary Use |
|----------|-------|-------------|
| **Performance Metrics** | Measurement | Tracking performance |
| **Profiling Tools** | Analysis | Finding bottlenecks |
| **Optimization Patterns** | Solutions | Implementing fixes |

## Navigation

- **Examples**: [Examples Index](../examples/INDEX.md)
- **Templates**: [Templates Index](../templates/INDEX.md)
- **Main Agent**: [performance-optimizer.md](../performance-optimizer.md)

---

Return to [main agent](../performance-optimizer.md)
