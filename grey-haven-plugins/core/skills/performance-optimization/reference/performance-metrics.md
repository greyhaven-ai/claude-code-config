# Performance Metrics Reference

Comprehensive guide to measuring and tracking performance across web, backend, and database layers.

## Web Vitals (Core)

### Largest Contentful Paint (LCP)
**Target**: <2.5s | **Poor**: >4.0s

Measures loading performance. Largest visible element in viewport.

```javascript
// Measure LCP
const observer = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
});
observer.observe({ entryTypes: ['largest-contentful-paint'] });
```

**Improvements**:
- Optimize images (WebP, lazy loading)
- Reduce server response time
- Eliminate render-blocking resources
- Use CDN for static assets

---

### First Input Delay (FID)
**Target**: <100ms | **Poor**: >300ms

Measures interactivity. Time from user interaction to browser response.

```javascript
// Measure FID
const observer = new PerformanceObserver((list) => {
  const entries = list.getEntries();
  entries.forEach((entry) => {
    console.log('FID:', entry.processingStart - entry.startTime);
  });
});
observer.observe({ entryTypes: ['first-input'] });
```

**Improvements**:
- Split long tasks
- Use web workers for heavy computation
- Optimize JavaScript execution
- Defer non-critical JavaScript

---

### Cumulative Layout Shift (CLS)
**Target**: <0.1 | **Poor**: >0.25

Measures visual stability. Unexpected layout shifts.

```javascript
// Measure CLS
let clsScore = 0;
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    if (!entry.hadRecentInput) {
      clsScore += entry.value;
    }
  });
  console.log('CLS:', clsScore);
});
observer.observe({ entryTypes: ['layout-shift'] });
```

**Improvements**:
- Set explicit dimensions for images/videos
- Avoid inserting content above existing content
- Use transform animations instead of layout properties
- Reserve space for ads/embeds

---

## Backend Metrics

### Response Time (Latency)
**Target**: p50 <100ms, p95 <200ms, p99 <500ms

```javascript
// Track with middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    metrics.histogram('http.response_time', duration, {
      method: req.method,
      route: req.route?.path,
      status: res.statusCode
    });
  });
  next();
});
```

---

### Throughput
**Target**: Varies by application (e.g., 1000 req/s)

```javascript
let requestCount = 0;
setInterval(() => {
  metrics.gauge('http.throughput', requestCount);
  requestCount = 0;
}, 1000);

app.use((req, res, next) => {
  requestCount++;
  next();
});
```

---

### Error Rate
**Target**: <0.1% (1 in 1000)

```javascript
let totalRequests = 0;
let errorRequests = 0;

app.use((req, res, next) => {
  totalRequests++;
  if (res.statusCode >= 500) {
    errorRequests++;
  }
  
  const errorRate = (errorRequests / totalRequests) * 100;
  metrics.gauge('http.error_rate', errorRate);
  next();
});
```

---

## Database Metrics

### Query Execution Time
**Target**: p95 <50ms, p99 <100ms

```sql
-- PostgreSQL: Enable query logging
ALTER DATABASE mydb SET log_min_duration_statement = 100;

-- View slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

### Connection Pool Usage
**Target**: <80% utilization

```javascript
pool.on('acquire', () => {
  const active = pool.totalCount - pool.idleCount;
  const utilization = (active / pool.max) * 100;
  metrics.gauge('db.pool.utilization', utilization);
});
```

---

## Memory Metrics

### Heap Usage
**Target**: <80% of max, stable over time

```javascript
setInterval(() => {
  const usage = process.memoryUsage();
  metrics.gauge('memory.heap_used', usage.heapUsed);
  metrics.gauge('memory.heap_total', usage.heapTotal);
  metrics.gauge('memory.external', usage.external);
}, 10000);
```

---

## Lighthouse Scores

| Score | Performance | Accessibility | Best Practices | SEO |
|-------|-------------|---------------|----------------|-----|
| **Good** | 90-100 | 90-100 | 90-100 | 90-100 |
| **Needs Improvement** | 50-89 | 50-89 | 50-89 | 50-89 |
| **Poor** | 0-49 | 0-49 | 0-49 | 0-49 |

---

## Summary

| Metric Category | Key Metrics | Tools |
|----------------|-------------|-------|
| **Web Vitals** | LCP, FID, CLS | Chrome DevTools, Lighthouse |
| **Backend** | Latency, Throughput, Error Rate | APM, Prometheus |
| **Database** | Query Time, Pool Usage | pg_stat_statements, APM |
| **Memory** | Heap Usage, GC Time | Node.js profiler |

---

**Next**: [Profiling Tools](profiling-tools.md) | **Index**: [Reference Index](INDEX.md)
