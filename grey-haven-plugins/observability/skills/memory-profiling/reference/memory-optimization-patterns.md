# Memory Optimization Patterns Reference

Quick reference catalog of common memory leak patterns and their fixes.

## Event Listener Leaks

### Pattern: EventEmitter Accumulation

**Symptom**: Memory grows linearly with time/requests
**Cause**: Event listeners added but never removed

**Vulnerable**:
```typescript
// ❌ LEAK: listener added every call
class DataProcessor {
  private emitter = new EventEmitter();

  async process() {
    this.emitter.on('data', handler);  // Never removed
  }
}
```

**Fixed**:
```typescript
// ✅ FIX 1: Remove listener
this.emitter.on('data', handler);
try { /* work */ } finally {
  this.emitter.removeListener('data', handler);
}

// ✅ FIX 2: Use once()
this.emitter.once('data', handler);  // Auto-removed

// ✅ FIX 3: Use AbortController
const controller = new AbortController();
this.emitter.on('data', handler, { signal: controller.signal });
controller.abort();  // Removes listener
```

**Detection**:
```typescript
// Check listener count
console.log(emitter.listenerCount('data'));  // Should be constant

// Monitor in production
process.on('warning', (warning) => {
  if (warning.name === 'MaxListenersExceededWarning') {
    console.error('Listener leak detected:', warning);
  }
});
```

---

## Closure Memory Traps

### Pattern: Captured Variables in Closures

**Symptom**: Memory not released after scope exits
**Cause**: Closure captures large variables

**Vulnerable**:
```typescript
// ❌ LEAK: Closure captures entire 1GB buffer
function createHandler(largeBuffer: Buffer) {
  return function handler() {
    // Only uses buffer.length, but captures entire buffer
    console.log(largeBuffer.length);
  };
}
```

**Fixed**:
```typescript
// ✅ FIX: Extract only what's needed
function createHandler(largeBuffer: Buffer) {
  const length = largeBuffer.length;  // Extract value
  return function handler() {
    console.log(length);  // Only captures number, not Buffer
  };
}
```

---

## Connection Pool Leaks

### Pattern: Unclosed Database Connections

**Symptom**: Pool exhaustion, connection timeouts
**Cause**: Connections acquired but not released

**Vulnerable**:
```python
# ❌ LEAK: Connection never closed on exception
def get_orders():
    conn = pool.acquire()
    orders = conn.execute("SELECT * FROM orders")
    return orders  # conn never released
```

**Fixed**:
```python
# ✅ FIX: Context manager guarantees cleanup
def get_orders():
    with pool.acquire() as conn:
        orders = conn.execute("SELECT * FROM orders")
        return orders  # conn auto-released
```

---

## Large Dataset Patterns

### Pattern 1: Loading Entire File into Memory

**Vulnerable**:
```python
# ❌ LEAK: 10GB file → 20GB RAM
df = pd.read_csv("large.csv")
```

**Fixed**:
```python
# ✅ FIX: Chunking
for chunk in pd.read_csv("large.csv", chunksize=10000):
    process(chunk)  # Constant memory

# ✅ BETTER: Polars streaming
df = pl.scan_csv("large.csv").collect(streaming=True)
```

### Pattern 2: List Comprehension vs Generator

**Vulnerable**:
```python
# ❌ LEAK: Entire list in memory
result = [process(item) for item in huge_list]
```

**Fixed**:
```python
# ✅ FIX: Generator (lazy evaluation)
result = (process(item) for item in huge_list)
for item in result:
    use(item)  # Processes one at a time
```

---

## Cache Management

### Pattern: Unbounded Cache Growth

**Vulnerable**:
```typescript
// ❌ LEAK: Cache grows forever
const cache = new Map<string, Data>();

function getData(key: string) {
  if (!cache.has(key)) {
    cache.set(key, fetchData(key));  // Never evicted
  }
  return cache.get(key);
}
```

**Fixed**:
```typescript
// ✅ FIX 1: LRU cache with max size
import { LRUCache } from 'lru-cache';

const cache = new LRUCache<string, Data>({
  max: 1000,  // Max 1000 entries
  ttl: 1000 * 60 * 5  // 5 minute TTL
});

// ✅ FIX 2: WeakMap (auto-cleanup when key GC'd)
const cache = new WeakMap<object, Data>();
cache.set(key, data);  // Auto-removed when key is GC'd
```

---

## Timer and Interval Leaks

### Pattern: Forgotten Timers

**Vulnerable**:
```typescript
// ❌ LEAK: Timer never cleared
class Component {
  startPolling() {
    setInterval(() => {
      this.fetchData();  // Keeps Component alive forever
    }, 1000);
  }
}
```

**Fixed**:
```typescript
// ✅ FIX: Clear timer on cleanup
class Component {
  private intervalId?: NodeJS.Timeout;

  startPolling() {
    this.intervalId = setInterval(() => {
      this.fetchData();
    }, 1000);
  }

  cleanup() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
}
```

---

## Global Variable Accumulation

### Pattern: Growing Global Arrays

**Vulnerable**:
```typescript
// ❌ LEAK: Array grows forever
const logs: string[] = [];

function log(message: string) {
  logs.push(message);  // Never cleared
}
```

**Fixed**:
```typescript
// ✅ FIX 1: Bounded array
const MAX_LOGS = 1000;
const logs: string[] = [];

function log(message: string) {
  logs.push(message);
  if (logs.length > MAX_LOGS) {
    logs.shift();  // Remove oldest
  }
}

// ✅ FIX 2: Circular buffer
import { CircularBuffer } from 'circular-buffer';
const logs = new CircularBuffer<string>(1000);
```

---

## String Concatenation

### Pattern: Repeated String Concatenation

**Vulnerable**:
```python
# ❌ LEAK: Creates new string each iteration (O(n²))
result = ""
for item in items:
    result += str(item)  # New string allocation
```

**Fixed**:
```python
# ✅ FIX 1: Join
result = "".join(str(item) for item in items)

# ✅ FIX 2: StringIO
from io import StringIO
buffer = StringIO()
for item in items:
    buffer.write(str(item))
result = buffer.getvalue()
```

---

## React Component Leaks

### Pattern: setState After Unmount

**Vulnerable**:
```typescript
// ❌ LEAK: setState called after unmount
function Component() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData);  // If unmounted, causes leak
  }, []);
}
```

**Fixed**:
```typescript
// ✅ FIX: Cleanup with AbortController
function Component() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    fetchData(controller.signal).then(setData);

    return () => controller.abort();  // Cleanup
  }, []);
}
```

---

## Detection Patterns

### Memory Leak Indicators

1. **Linear growth**: Memory usage increases linearly with time/requests
2. **Pool exhaustion**: Connection pool hits max size
3. **EventEmitter warnings**: "MaxListenersExceededWarning"
4. **GC pressure**: Frequent/long GC pauses
5. **OOM errors**: Process crashes with "JavaScript heap out of memory"

### Monitoring Metrics

```typescript
// Prometheus metrics for leak detection
const heap_used = new Gauge({
  name: 'nodejs_heap_used_bytes',
  help: 'V8 heap used bytes'
});

const event_listeners = new Gauge({
  name: 'event_listeners_total',
  help: 'Total event listeners',
  labelNames: ['event']
});

// Alert if heap grows >10% per hour
// Alert if listener count >100 for single event
```

---

## Quick Fixes Checklist

- [ ] **Event listeners**: Use `once()` or `removeListener()`
- [ ] **Database connections**: Use context managers or `try/finally`
- [ ] **Large datasets**: Use chunking or streaming
- [ ] **Caches**: Implement LRU or WeakMap
- [ ] **Timers**: Clear with `clearInterval()` or `clearTimeout()`
- [ ] **Closures**: Extract values, avoid capturing large objects
- [ ] **React**: Cleanup in `useEffect()` return
- [ ] **Strings**: Use `join()` or `StringIO`, not `+=`

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md)
- **Tools**: [profiling-tools.md](profiling-tools.md)
- **GC**: [garbage-collection-guide.md](garbage-collection-guide.md)

---

Return to [reference index](INDEX.md)
