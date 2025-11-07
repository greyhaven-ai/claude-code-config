# Garbage Collection Guide

Understanding and tuning garbage collectors in Node.js (V8) and Python for optimal memory management.

## V8 Garbage Collector (Node.js)

### Heap Structure

**Two Generations**:
```
┌─────────────────────────────────────────────────────────┐
│ V8 Heap                                                 │
├─────────────────────────────────────────────────────────┤
│ New Space (Young Generation) - 8MB-32MB                │
│ ┌─────────────┬─────────────┐                          │
│ │ From-Space  │ To-Space    │ ← Minor GC (Scavenge)   │
│ └─────────────┴─────────────┘                          │
│                                                         │
│ Old Space (Old Generation) - Remaining heap            │
│ ┌──────────────────────────────────────┐               │
│ │ Long-lived objects                   │ ← Major GC    │
│ │ (survived 2+ Minor GCs)              │   (Mark-Sweep)│
│ └──────────────────────────────────────┘               │
│                                                         │
│ Large Object Space - Objects >512KB                    │
└─────────────────────────────────────────────────────────┘
```

**GC Types**:
- **Scavenge (Minor GC)**: Fast (~1ms), clears new space, runs frequently
- **Mark-Sweep (Major GC)**: Slow (100-500ms), clears old space, runs when old space fills
- **Mark-Compact**: Like Mark-Sweep but also defragments memory

---

### Monitoring V8 GC

**Built-in GC Traces**:
```bash
# Enable GC logging
node --trace-gc server.js

# Output:
# [12345:0x104800000]       42 ms: Scavenge 8.5 (10.2) -> 7.8 (10.2) MB
# [12345:0x104800000]      123 ms: Mark-sweep 95.2 (100.5) -> 82.3 (100.5) MB
```

**Parse GC logs**:
```
[PID:address] time ms: GC-type before (heap) -> after (heap) MB

Scavenge = Minor GC (young generation)
Mark-sweep = Major GC (old generation)
```

**Prometheus Metrics**:
```typescript
import { Gauge } from 'prom-client';
import v8 from 'v8';

const heap_size = new Gauge({ name: 'nodejs_heap_size_total_bytes' });
const heap_used = new Gauge({ name: 'nodejs_heap_used_bytes' });
const gc_duration = new Histogram({
  name: 'nodejs_gc_duration_seconds',
  labelNames: ['kind']
});

// Track GC events
const PerformanceObserver = require('perf_hooks').PerformanceObserver;
const obs = new PerformanceObserver((list) => {
  const entry = list.getEntries()[0];
  gc_duration.labels(entry.kind).observe(entry.duration / 1000);
});
obs.observe({ entryTypes: ['gc'] });

// Update heap metrics every 10s
setInterval(() => {
  const stats = v8.getHeapStatistics();
  heap_size.set(stats.total_heap_size);
  heap_used.set(stats.used_heap_size);
}, 10000);
```

---

### V8 GC Tuning

**Heap Size Limits**:
```bash
# Default: ~1.4GB on 64-bit systems
# Increase max heap size
node --max-old-space-size=4096 server.js  # 4GB heap

# For containers (set to 75% of container memory)
# 8GB container → --max-old-space-size=6144
```

**GC Optimization Flags**:
```bash
# Aggressive GC (lower memory, more CPU)
node --optimize-for-size --gc-interval=100 server.js

# Optimize for throughput (higher memory, less CPU)
node --max-old-space-size=8192 server.js

# Expose GC to JavaScript
node --expose-gc server.js
# Then: global.gc() to force GC
```

**When to tune**:
- ✅ Container memory limits (set heap to 75% of limit)
- ✅ Frequent Major GC causing latency spikes
- ✅ OOM errors with available memory
- ❌ Don't tune as first step (fix leaks first!)

---

## Python Garbage Collector

### GC Mechanism

**Two Systems**:
1. **Reference Counting**: Primary mechanism, immediate cleanup when refcount = 0
2. **Generational GC**: Handles circular references

**Generational Structure**:
```
┌─────────────────────────────────────────────────────────┐
│ Python GC (Generational)                                │
├─────────────────────────────────────────────────────────┤
│ Generation 0 (Young) - Threshold: 700 objects          │
│ ├─ New objects                                          │
│ └─ Collected most frequently                            │
│                                                         │
│ Generation 1 (Middle) - Threshold: 10 collections      │
│ ├─ Survived 1 Gen0 collection                          │
│ └─ Collected less frequently                            │
│                                                         │
│ Generation 2 (Old) - Threshold: 10 collections         │
│ ├─ Survived Gen1 collection                            │
│ └─ Collected rarely                                     │
└─────────────────────────────────────────────────────────┘
```

---

### Monitoring Python GC

**GC Statistics**:
```python
import gc

# Get GC stats
print(gc.get_stats())
# [{'collections': 42, 'collected': 123, 'uncollectable': 0}, ...]

# Get object count by generation
print(gc.get_count())
# (45, 3, 1) = (gen0, gen1, gen2) object counts

# Get thresholds
print(gc.get_threshold())
# (700, 10, 10) = collect when gen0 has 700 objects, etc.
```

**Track GC Pauses**:
```python
import gc
import time

class GCMonitor:
    def __init__(self):
        self.start_time = None

    def on_gc_start(self, phase, info):
        self.start_time = time.time()

    def on_gc_finish(self, phase, info):
        duration = time.time() - self.start_time
        print(f"GC {phase}: {duration*1000:.1f}ms, collected {info['collected']}")

# Install callbacks
gc.callbacks.append(GCMonitor().on_gc_start)
```

**Prometheus Metrics**:
```python
from prometheus_client import Gauge, Histogram
import gc

gc_collections = Gauge('python_gc_collections_total', 'GC collections', ['generation'])
gc_collected = Gauge('python_gc_objects_collected_total', 'Objects collected', ['generation'])
gc_duration = Histogram('python_gc_duration_seconds', 'GC duration', ['generation'])

def record_gc_metrics():
    stats = gc.get_stats()
    for gen, stat in enumerate(stats):
        gc_collections.labels(generation=gen).set(stat['collections'])
        gc_collected.labels(generation=gen).set(stat['collected'])
```

---

### Python GC Tuning

**Disable GC (for batch jobs)**:
```python
import gc

# Disable automatic GC
gc.disable()

# Process large dataset without GC pauses
for chunk in large_dataset:
    process(chunk)

# Manual GC at end
gc.collect()
```

**Adjust Thresholds**:
```python
import gc

# Default: (700, 10, 10)
# More aggressive: collect more often, lower memory
gc.set_threshold(400, 5, 5)

# Less aggressive: collect less often, higher memory but faster
gc.set_threshold(1000, 15, 15)
```

**Debug Circular References**:
```python
import gc

# Find objects that can't be collected
gc.set_debug(gc.DEBUG_SAVEALL)
gc.collect()

print(f"Uncollectable: {len(gc.garbage)}")
for obj in gc.garbage:
    print(type(obj), obj)
```

**When to tune**:
- ✅ Batch jobs: disable GC, manual collect at end
- ✅ Real-time systems: adjust thresholds to avoid long pauses
- ✅ Debugging: use `DEBUG_SAVEALL` to find leaks
- ❌ Don't disable GC in long-running services (memory will grow!)

---

## GC-Related Memory Issues

### Issue 1: Long GC Pauses

**Symptom**: Request latency spikes every few minutes

**V8 Fix**:
```bash
# Monitor GC pauses
node --trace-gc server.js 2>&1 | grep "Mark-sweep"

# If Major GC >500ms, increase heap size
node --max-old-space-size=4096 server.js
```

**Python Fix**:
```python
# Disable GC during request handling
import gc
gc.disable()

# Periodic manual GC (in background thread)
import threading
def periodic_gc():
    while True:
        time.sleep(60)
        gc.collect()
threading.Thread(target=periodic_gc, daemon=True).start()
```

---

### Issue 2: Frequent Minor GC

**Symptom**: High CPU from constant minor GC

**Cause**: Too many short-lived objects

**Fix**: Reduce allocations
```python
# ❌ BAD: Creates many temporary objects
def process_data(items):
    return [str(i) for i in items]  # New list + strings

# ✅ BETTER: Generator (no intermediate list)
def process_data(items):
    return (str(i) for i in items)
```

---

### Issue 3: Memory Not Released After GC

**Symptom**: Heap usage high even after GC

**V8 Cause**: Objects in old generation (major GC needed)
```bash
# Force full GC to reclaim memory
node --expose-gc server.js

# In code:
if (global.gc) global.gc();
```

**Python Cause**: Reference cycles
```python
# Debug reference cycles
import gc
import sys

# Find what's keeping object alive
obj = my_object
print(sys.getrefcount(obj))  # Should be low

# Get referrers
print(gc.get_referrers(obj))
```

---

## GC Alerts (Prometheus)

```yaml
# Prometheus alert rules
groups:
  - name: gc_alerts
    rules:
      # V8: Major GC taking too long
      - alert: SlowMajorGC
        expr: nodejs_gc_duration_seconds{kind="major"} > 0.5
        for: 5m
        annotations:
          summary: "Major GC >500ms ({{ $value }}s)"

      # V8: High GC frequency
      - alert: FrequentGC
        expr: rate(nodejs_gc_duration_seconds_count[5m]) > 10
        for: 10m
        annotations:
          summary: "GC running >10x/min"

      # Python: High Gen2 collections
      - alert: FrequentFullGC
        expr: rate(python_gc_collections_total{generation="2"}[1h]) > 1
        for: 1h
        annotations:
          summary: "Full GC >1x/hour (potential leak)"
```

---

## Best Practices

### V8 (Node.js)

1. **Set heap size**: `--max-old-space-size` to 75% of container memory
2. **Monitor GC**: Track duration and frequency with Prometheus
3. **Alert on slow GC**: Major GC >500ms indicates heap too small or memory leak
4. **Don't force GC**: Let V8 manage (except for tests/debugging)

### Python

1. **Use reference counting**: Most cleanup is automatic (refcount = 0)
2. **Avoid circular refs**: Use `weakref` for back-references
3. **Batch jobs**: Disable GC, manual `gc.collect()` at end
4. **Monitor Gen2**: Frequent Gen2 collections = potential leak

---

## Related Documentation

- **Patterns**: [memory-optimization-patterns.md](memory-optimization-patterns.md)
- **Tools**: [profiling-tools.md](profiling-tools.md)
- **Examples**: [Examples Index](../examples/INDEX.md)

---

Return to [reference index](INDEX.md)
