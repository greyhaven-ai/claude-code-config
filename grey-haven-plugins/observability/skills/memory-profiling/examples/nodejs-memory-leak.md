# Node.js Memory Leak Detection

Identifying and fixing memory leaks in Node.js applications using Chrome DevTools, heapdump, and memory profiling techniques.

## Overview

**Symptoms Before Fix**:
- Memory usage: 150MB → 2GB over 6 hours
- Heap size growing linearly (5MB/minute)
- V8 garbage collection ineffective
- Production outages (OOM killer)

**After Fix**:
- Memory stable at 150MB (93% reduction)
- Heap size constant over time
- Zero OOM errors in 30 days
- Proper resource cleanup

**Tools**: Chrome DevTools, heapdump, memwatch-next, Prometheus monitoring

## 1. Memory Leak Symptoms

### Linear Memory Growth

```bash
# Monitor Node.js memory usage
node --expose-gc --inspect app.js

# Connect Chrome DevTools: chrome://inspect
# Memory tab → Take heap snapshot every 5 minutes
```

**Heap growth pattern**:
```
Time  | Heap Size | External | Total
------|-----------|----------|-------
0 min | 50MB      | 10MB     | 60MB
5 min | 75MB      | 15MB     | 90MB
10min | 100MB     | 20MB     | 120MB
15min | 125MB     | 25MB     | 150MB
...   | ...       | ...      | ...
6 hrs | 1.8GB     | 200MB    | 2GB
```

**Diagnosis**: Linear growth indicates memory leak (not normal sawtooth GC pattern)

### High GC Activity

```javascript
// Monitor GC events
const v8 = require('v8');
const memoryUsage = process.memoryUsage();

setInterval(() => {
  const usage = process.memoryUsage();
  console.log({
    heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
    heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)}MB`,
    external: `${Math.round(usage.external / 1024 / 1024)}MB`,
    rss: `${Math.round(usage.rss / 1024 / 1024)}MB`
  });
}, 60000);  // Every minute
```

**Output showing leak**:
```
{heapUsed: '75MB', heapTotal: '100MB', external: '15MB', rss: '120MB'}
{heapUsed: '100MB', heapTotal: '130MB', external: '20MB', rss: '150MB'}
{heapUsed: '125MB', heapTotal: '160MB', external: '25MB', rss: '185MB'}
```

## 2. Heap Snapshot Analysis

### Taking Heap Snapshots

```javascript
// Generate heap snapshot programmatically
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
  const heapSnapshot = v8.writeHeapSnapshot(filename);
  console.log(`Heap snapshot written to ${heapSnapshot}`);
}

// Take snapshot every hour
setInterval(() => {
  const timestamp = new Date().toISOString().replace(/:/g, '-');
  takeHeapSnapshot(`heap-${timestamp}.heapsnapshot`);
}, 3600000);
```

### Analyzing Snapshots in Chrome DevTools

**Steps**:
1. Load two snapshots (before and after 1 hour)
2. Compare snapshots (Comparison view)
3. Sort by "Size Delta" (descending)
4. Look for objects growing significantly

**Example Analysis**:
```
Object Type           | Count  | Size Delta | Retained Size
----------------------|--------|------------|---------------
(array)               | +5,000 | +50MB      | +60MB
EventEmitter          | +1,200 | +12MB      | +15MB
Closure (anonymous)   | +800   | +8MB       | +10MB
```

**Diagnosis**: EventEmitter count growing = likely event listener leak

### Retained Objects Analysis

```javascript
// Chrome DevTools → Heap Snapshot → Summary → sort by "Retained Size"
// Click object → view Retainer tree
```

**Retainer tree example** (EventEmitter leak):
```
EventEmitter @123456
  ← listeners: Array[50]
    ← _events.data: Array
      ← EventEmitter @123456 (self-reference leak!)
```

## 3. Common Memory Leak Patterns

### Pattern 1: Event Listener Leak

**Vulnerable Code**:
```typescript
// ❌ LEAK: EventEmitter listeners never removed
import {EventEmitter} from 'events';

class DataProcessor {
  private emitter = new EventEmitter();

  async processOrders() {
    // Add listener every time function called
    this.emitter.on('data', (data) => {
      console.log('Processing:', data);
    });

    // Emit 1000 events
    for (let i = 0; i < 1000; i++) {
      this.emitter.emit('data', {id: i});
    }
  }
}

// Called 1000 times = 1000 listeners accumulate!
setInterval(() => new DataProcessor().processOrders(), 1000);
```

**Result**: 1000 listeners/second = 3.6M listeners/hour → 2GB memory leak

**Fixed Code**:
```typescript
// ✅ FIXED: Remove listener after use
class DataProcessor {
  private emitter = new EventEmitter();

  async processOrders() {
    const handler = (data) => {
      console.log('Processing:', data);
    };

    this.emitter.on('data', handler);

    try {
      for (let i = 0; i < 1000; i++) {
        this.emitter.emit('data', {id: i});
      }
    } finally {
      // ✅ Clean up listener
      this.emitter.removeListener('data', handler);
    }
  }
}
```

**Better**: Use `once()` for one-time listeners:
```typescript
this.emitter.once('data', handler);  // Auto-removed after first emit
```

### Pattern 2: Closure Leak

**Vulnerable Code**:
```typescript
// ❌ LEAK: Closure captures large object
const cache = new Map();

function processRequest(userId: string) {
  const largeData = fetchLargeDataset(userId);  // 10MB object

  // Closure captures entire largeData
  cache.set(userId, () => {
    return largeData.summary;  // Only need summary (1KB)
  });
}

// Called for 1000 users = 10GB in cache!
```

**Fixed Code**:
```typescript
// ✅ FIXED: Only store what you need
const cache = new Map();

function processRequest(userId: string) {
  const largeData = fetchLargeDataset(userId);
  const summary = largeData.summary;  // Extract only 1KB

  // Store minimal data
  cache.set(userId, () => summary);
}

// 1000 users = 1MB in cache ✅
```

### Pattern 3: Global Variable Accumulation

**Vulnerable Code**:
```typescript
// ❌ LEAK: Global array keeps growing
const requestLog: Request[] = [];

app.post('/api/orders', (req, res) => {
  requestLog.push(req);  // Never removed!
  // ... process order
});

// 1M requests = 1M objects in memory permanently
```

**Fixed Code**:
```typescript
// ✅ FIXED: Use LRU cache with size limit
import LRU from 'lru-cache';

const requestLog = new LRU({
  max: 1000,  // Maximum 1000 items
  ttl: 1000 * 60 * 5  // 5-minute TTL
});

app.post('/api/orders', (req, res) => {
  requestLog.set(req.id, req);  // Auto-evicts old items
});
```

### Pattern 4: Forgotten Timers/Intervals

**Vulnerable Code**:
```typescript
// ❌ LEAK: setInterval never cleared
class ReportGenerator {
  private data: any[] = [];

  start() {
    setInterval(() => {
      this.data.push(generateReport());  // Accumulates forever
    }, 60000);
  }
}

// Each instance leaks!
const generator = new ReportGenerator();
generator.start();
```

**Fixed Code**:
```typescript
// ✅ FIXED: Clear interval on cleanup
class ReportGenerator {
  private data: any[] = [];
  private intervalId?: NodeJS.Timeout;

  start() {
    this.intervalId = setInterval(() => {
      this.data.push(generateReport());
    }, 60000);
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = undefined;
      this.data = [];  // Clear accumulated data
    }
  }
}
```

## 4. Memory Profiling with memwatch-next

### Installation

```bash
bun add memwatch-next
```

### Leak Detection

```typescript
// memory-monitor.ts
import memwatch from 'memwatch-next';

// Detect memory leaks
memwatch.on('leak', (info) => {
  console.error('Memory leak detected:', {
    growth: info.growth,
    reason: info.reason,
    current_base: `${Math.round(info.current_base / 1024 / 1024)}MB`,
    leaked: `${Math.round((info.current_base - info.start) / 1024 / 1024)}MB`
  });

  // Alert to PagerDuty/Slack
  alertOps('Memory leak detected', info);
});

// Monitor GC stats
memwatch.on('stats', (stats) => {
  console.log('GC stats:', {
    used_heap_size: `${Math.round(stats.used_heap_size / 1024 / 1024)}MB`,
    heap_size_limit: `${Math.round(stats.heap_size_limit / 1024 / 1024)}MB`,
    num_full_gc: stats.num_full_gc,
    num_inc_gc: stats.num_inc_gc
  });
});
```

### HeapDiff for Leak Analysis

```typescript
import memwatch from 'memwatch-next';

const hd = new memwatch.HeapDiff();

// Simulate leak
const leak: any[] = [];
for (let i = 0; i < 10000; i++) {
  leak.push({data: new Array(1000).fill('x')});
}

// Compare heaps
const diff = hd.end();
console.log('Heap diff:', JSON.stringify(diff, null, 2));

// Output:
// {
//   "before": {"nodes": 12345, "size": 50000000},
//   "after": {"nodes": 22345, "size": 150000000},
//   "change": {
//     "size_bytes": 100000000,  // 100MB leak!
//     "size": "100.00MB",
//     "freed_nodes": 100,
//     "allocated_nodes": 10100  // Net increase
//   }
// }
```

## 5. Production Memory Monitoring

### Prometheus Metrics

```typescript
// metrics.ts
import {Gauge} from 'prom-client';

const memoryUsageGauge = new Gauge({
  name: 'nodejs_memory_usage_bytes',
  help: 'Node.js memory usage in bytes',
  labelNames: ['type']
});

setInterval(() => {
  const usage = process.memoryUsage();
  memoryUsageGauge.set({type: 'heap_used'}, usage.heapUsed);
  memoryUsageGauge.set({type: 'heap_total'}, usage.heapTotal);
  memoryUsageGauge.set({type: 'external'}, usage.external);
  memoryUsageGauge.set({type: 'rss'}, usage.rss);
}, 15000);
```

**Grafana Alert**:
```promql
# Alert if heap usage growing linearly
increase(nodejs_memory_usage_bytes{type="heap_used"}[1h]) > 100000000  # 100MB/hour
```

## 6. Real-World Fix: EventEmitter Leak

### Before (Leaking)

```typescript
// order-processor.ts (BEFORE FIX)
class OrderProcessor {
  private emitter = new EventEmitter();

  async processOrders() {
    // ❌ LEAK: Listener added every call
    this.emitter.on('order:created', async (order) => {
      await this.sendConfirmationEmail(order);
      await this.updateInventory(order);
    });

    const orders = await db.query.orders.findMany({status: 'pending'});
    for (const order of orders) {
      this.emitter.emit('order:created', order);
    }
  }
}

// Called every minute
setInterval(() => new OrderProcessor().processOrders(), 60000);
```

**Result**: 1,440 listeners/day → 2GB memory leak in production

### After (Fixed)

```typescript
// order-processor.ts (AFTER FIX)
class OrderProcessor {
  private emitter = new EventEmitter();
  private listeners = new WeakMap();  // Track listeners for cleanup

  async processOrders() {
    const handler = async (order) => {
      await this.sendConfirmationEmail(order);
      await this.updateInventory(order);
    };

    // ✅ Use once() for one-time processing
    this.emitter.once('order:created', handler);

    const orders = await db.query.orders.findMany({status: 'pending'});
    for (const order of orders) {
      this.emitter.emit('order:created', order);
    }

    // ✅ Cleanup (if using on() instead of once())
    this.emitter.removeAllListeners('order:created');
  }
}
```

**Result**: Memory stable at 150MB, zero leaks

## 7. Results and Impact

### Before vs After Metrics

| Metric | Before Fix | After Fix | Impact |
|--------|-----------|-----------|---------|
| **Memory Usage** | 2GB (after 6h) | 150MB (stable) | **93% reduction** |
| **Heap Size** | Linear growth (5MB/min) | Stable | **Zero growth** |
| **OOM Incidents** | 12/month | 0/month | **100% eliminated** |
| **GC Pause Time** | 200ms avg | 50ms avg | **75% faster** |
| **Uptime** | 6 hours avg | 30+ days | **120x improvement** |

### Lessons Learned

**1. Always remove event listeners**
- Use `once()` for one-time events
- Use `removeListener()` in finally blocks
- Track listeners with WeakMap for debugging

**2. Avoid closures capturing large objects**
- Extract only needed data before closure
- Use WeakMap/WeakSet for object references
- Profile with heap snapshots regularly

**3. Monitor memory in production**
- Prometheus metrics for heap usage
- Alert on linear growth patterns
- Weekly heap snapshot analysis

## Related Documentation

- **Python Profiling**: [python-scalene-profiling.md](python-scalene-profiling.md)
- **DB Leaks**: [database-connection-leak.md](database-connection-leak.md)
- **Reference**: [../reference/memory-patterns.md](../reference/memory-patterns.md)
- **Templates**: [../templates/memory-report.md](../templates/memory-report.md)

---

Return to [examples index](INDEX.md)
