# Profiling Tools Reference

Tools and techniques for identifying performance bottlenecks across the stack.

## Chrome DevTools

### Performance Panel
```javascript
// Mark performance measurements
performance.mark('start-expensive-operation');
// ... expensive operation ...
performance.mark('end-expensive-operation');
performance.measure(
  'expensive-operation',
  'start-expensive-operation',
  'end-expensive-operation'
);
```

**Use for**: FPS analysis, JavaScript profiling, paint events, network waterfall

---

### Memory Panel
- **Heap Snapshot**: Take snapshot, compare for memory leaks
- **Allocation Timeline**: See memory allocation over time
- **Allocation Sampling**: Low-overhead profiling

**Use for**: Memory leak detection, heap size analysis

---

## Node.js Profiling

### Built-in Inspector
```bash
# Start with inspector
node --inspect server.js

# Open chrome://inspect in Chrome
# Click "inspect" to open DevTools
```

### clinic.js
```bash
# Install
npm install -g clinic

# Doctor: Overall health check
clinic doctor -- node server.js

# Flame: CPU profiling
clinic flame -- node server.js

# Bubbleprof: Async operations
clinic bubbleprof -- node server.js
```

---

## React DevTools Profiler

```jsx
import { Profiler } from 'react';

function onRenderCallback(
  id, phase, actualDuration, baseDuration, startTime, commitTime
) {
  console.log(`${id} took ${actualDuration}ms to render`);
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

**Metrics**:
- **Actual Duration**: Time to render committed update
- **Base Duration**: Estimated time without memoization
- **Start Time**: When React began rendering
- **Commit Time**: When React committed the update

---

## Database Profiling

### PostgreSQL EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = '123'
  AND status = 'pending';

-- Output shows:
-- - Execution time
-- - Rows scanned
-- - Index usage
-- - Cost estimates
```

### pg_stat_statements
```sql
-- Enable extension
CREATE EXTENSION pg_stat_statements;

-- View top slow queries
SELECT 
  query,
  mean_exec_time,
  calls,
  total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## APM Tools

### DataDog
```javascript
const tracer = require('dd-trace').init();

tracer.trace('expensive-operation', () => {
  // Your code here
});
```

### Sentry Performance
```javascript
import * as Sentry from '@sentry/node';

const transaction = Sentry.startTransaction({
  op: 'task',
  name: 'Process Order'
});

// ... do work ...

transaction.finish();
```

---

## Summary

| Tool | Use Case | Best For |
|------|----------|----------|
| **Chrome DevTools** | Frontend profiling | JavaScript, rendering, network |
| **clinic.js** | Node.js profiling | CPU, async, I/O |
| **React Profiler** | Component profiling | React performance |
| **EXPLAIN ANALYZE** | Query profiling | Database optimization |
| **APM Tools** | Production monitoring | Distributed tracing |

---

**Previous**: [Performance Metrics](performance-metrics.md) | **Next**: [Optimization Patterns](optimization-patterns.md) | **Index**: [Reference Index](INDEX.md)
