# Memory Profiling Tools Comparison

Quick reference for choosing and using memory profiling tools across Node.js, Python, and production monitoring.

## Node.js Tools

### Chrome DevTools (Built-in)

**Best for**: Interactive heap snapshot analysis, timeline profiling
**Cost**: Free (built into Node.js)

**Usage**:
```bash
# Start Node.js with inspector
node --inspect server.js

# Open chrome://inspect
# Click "Open dedicated DevTools for Node"
```

**Features**:
- Heap snapshots (memory state at point in time)
- Timeline recording (allocations over time)
- Comparison view (find leaks by comparing snapshots)
- Retainer paths (why object not GC'd)

**When to use**:
- Development/staging environments
- Interactive debugging sessions
- Visual leak analysis

---

### heapdump (npm package)

**Best for**: Production heap snapshots without restarts
**Cost**: Free (npm package)

**Usage**:
```typescript
import heapdump from 'heapdump';

// Trigger snapshot on signal
process.on('SIGUSR2', () => {
  heapdump.writeSnapshot((err, filename) => {
    console.log('Heap dump written to', filename);
  });
});

// Auto-snapshot on OOM
heapdump.writeSnapshot('./oom-' + Date.now() + '.heapsnapshot');
```

**When to use**:
- Production memory leak diagnosis
- Scheduled snapshots (daily/weekly)
- OOM analysis (capture before crash)

---

### clinic.js (Comprehensive Suite)

**Best for**: All-in-one performance profiling
**Cost**: Free (open source)

**Usage**:
```bash
# Install
npm install -g clinic

# Memory profiling
clinic heapprofiler -- node server.js

# Generates interactive HTML report
```

**Features**:
- Heap profiler (memory allocations)
- Flame graphs (CPU + memory)
- Timeline visualization
- Automatic leak detection

**When to use**:
- Initial performance investigation
- Comprehensive profiling (CPU + memory)
- Team-friendly reports (HTML)

---

### memwatch-next

**Best for**: Real-time leak detection in production
**Cost**: Free (npm package)

**Usage**:
```typescript
import memwatch from '@airbnb/node-memwatch';

memwatch.on('leak', (info) => {
  console.error('Memory leak detected:', info);
  // Alert, log, snapshot, etc.
});

memwatch.on('stats', (stats) => {
  console.log('GC stats:', stats);
});
```

**When to use**:
- Production leak monitoring
- Automatic alerting
- GC pressure tracking

---

## Python Tools

### Scalene (Line-by-Line Profiler)

**Best for**: Fastest, most detailed Python profiler
**Cost**: Free (pip package)

**Usage**:
```bash
# Install
pip install scalene

# Profile script
scalene script.py

# Profile with pytest
scalene --cli --memory -m pytest tests/

# HTML report
scalene --html --outfile profile.html script.py
```

**Features**:
- Line-by-line memory allocation
- CPU profiling
- GPU profiling
- Native code vs Python time
- Memory timeline

**When to use**:
- Python memory optimization
- Line-level bottleneck identification
- pytest integration

---

### memory_profiler

**Best for**: Simple decorator-based profiling
**Cost**: Free (pip package)

**Usage**:
```python
from memory_profiler import profile

@profile
def my_function():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    return a + b

# Run with: python -m memory_profiler script.py
```

**When to use**:
- Quick function-level profiling
- Simple memory debugging
- Educational/learning

---

### tracemalloc (Built-in)

**Best for**: Production memory tracking without dependencies
**Cost**: Free (Python standard library)

**Usage**:
```python
import tracemalloc

tracemalloc.start()

# Your code here

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.1f} MB")
print(f"Peak: {peak / 1024 / 1024:.1f} MB")

# Top allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)

tracemalloc.stop()
```

**When to use**:
- Production environments (no external dependencies)
- Allocation tracking
- Top allocators identification

---

### py-spy (Sampling Profiler)

**Best for**: Zero-overhead production profiling
**Cost**: Free (cargo/pip package)

**Usage**:
```bash
# Install
pip install py-spy

# Attach to running process (no code changes!)
py-spy top --pid 12345

# Flame graph
py-spy record --pid 12345 --output profile.svg
```

**When to use**:
- Production profiling (minimal overhead)
- No code modification required
- Running process analysis

---

## Monitoring Tools

### Prometheus + Grafana

**Best for**: Production metrics and alerting
**Cost**: Free (open source)

**Metrics to track**:
```typescript
import { Gauge, Histogram } from 'prom-client';

// Heap usage
const heap_used = new Gauge({
  name: 'nodejs_heap_used_bytes',
  help: 'V8 heap used bytes'
});

// Memory allocation rate
const allocation_rate = new Gauge({
  name: 'memory_allocation_bytes_per_second',
  help: 'Memory allocation rate'
});

// Connection pool
const pool_active = new Gauge({
  name: 'db_pool_connections_active',
  help: 'Active database connections'
});
```

**Alerts**:
```yaml
# Prometheus alert rules
groups:
  - name: memory_alerts
    rules:
      - alert: MemoryLeak
        expr: increase(nodejs_heap_used_bytes[1h]) > 100000000  # +100MB/hour
        for: 6h
        annotations:
          summary: "Potential memory leak ({{ $value | humanize }} growth)"

      - alert: HeapNearLimit
        expr: nodejs_heap_used_bytes / nodejs_heap_size_bytes > 0.9
        for: 5m
        annotations:
          summary: "Heap usage >90%"
```

**When to use**:
- Production monitoring (all environments)
- Long-term trend analysis
- Automatic alerting

---

### DataDog APM

**Best for**: Comprehensive observability platform
**Cost**: Paid (starts $15/host/month)

**Features**:
- Automatic heap tracking
- Memory leak detection
- Distributed tracing
- Alert management
- Dashboards

**When to use**:
- Enterprise environments
- Multi-service tracing
- Managed solution preferred

---

## Tool Selection Matrix

| Scenario | Node.js Tool | Python Tool | Monitoring |
|----------|-------------|-------------|------------|
| **Development debugging** | Chrome DevTools | Scalene | - |
| **Production leak** | heapdump | py-spy | Prometheus |
| **Line-level analysis** | clinic.js | Scalene | - |
| **Real-time monitoring** | memwatch-next | tracemalloc | Grafana |
| **Zero overhead** | - | py-spy | DataDog |
| **No dependencies** | Chrome DevTools | tracemalloc | - |
| **Team reports** | clinic.js | Scalene HTML | Grafana |

---

## Quick Start Commands

### Node.js

```bash
# Development: Chrome DevTools
node --inspect server.js

# Production: Heap snapshot
kill -USR2 <pid>  # If heapdump configured

# Comprehensive: clinic.js
clinic heapprofiler -- node server.js
```

### Python

```bash
# Line-by-line: Scalene
scalene --cli --memory script.py

# Quick profile: memory_profiler
python -m memory_profiler script.py

# Production: py-spy
py-spy top --pid <pid>
```

### Monitoring

```bash
# Prometheus metrics
curl http://localhost:9090/metrics | grep memory

# Grafana dashboard
# Import dashboard ID: 11159 (Node.js)
# Import dashboard ID: 7362 (Python)
```

---

## Tool Comparison Table

| Tool | Language | Type | Overhead | Production-Safe | Interactive |
|------|----------|------|----------|----------------|-------------|
| **Chrome DevTools** | Node.js | Heap snapshot | Low | No | Yes |
| **heapdump** | Node.js | Heap snapshot | Low | Yes | No |
| **clinic.js** | Node.js | Profiler | Medium | No | Yes |
| **memwatch-next** | Node.js | Real-time | Low | Yes | No |
| **Scalene** | Python | Profiler | Low | Staging | Yes |
| **memory_profiler** | Python | Decorator | Medium | No | No |
| **tracemalloc** | Python | Built-in | Low | Yes | No |
| **py-spy** | Python | Sampling | Very Low | Yes | No |
| **Prometheus** | Both | Metrics | Very Low | Yes | Yes (Grafana) |
| **DataDog** | Both | APM | Very Low | Yes | Yes |

---

## Best Practices

### Development Workflow

1. **Initial investigation**: Chrome DevTools (Node.js) or Scalene (Python)
2. **Line-level analysis**: clinic.js or Scalene with `--html`
3. **Root cause**: Heap snapshot comparison (DevTools)
4. **Validation**: Load testing with monitoring

### Production Workflow

1. **Detection**: Prometheus alerts (heap growth, pool exhaustion)
2. **Diagnosis**: heapdump snapshot or py-spy sampling
3. **Analysis**: Chrome DevTools (load snapshot) or Scalene (if reproducible in staging)
4. **Monitoring**: Grafana dashboards for trends

---

## Related Documentation

- **Patterns**: [memory-optimization-patterns.md](memory-optimization-patterns.md)
- **GC**: [garbage-collection-guide.md](garbage-collection-guide.md)
- **Examples**: [Examples Index](../examples/INDEX.md)

---

Return to [reference index](INDEX.md)
