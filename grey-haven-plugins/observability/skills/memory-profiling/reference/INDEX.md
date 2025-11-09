# Memory Profiler Reference

Quick reference guides for memory optimization patterns, profiling tools, and garbage collection.

## Reference Guides

### Memory Optimization Patterns

**File**: [memory-optimization-patterns.md](memory-optimization-patterns.md)

Comprehensive catalog of memory leak patterns and their fixes:
- **Event Listener Leaks**: EventEmitter cleanup, closure traps
- **Connection Pool Leaks**: Database connection management
- **Large Dataset Patterns**: Streaming, chunking, lazy evaluation
- **Cache Management**: LRU caches, WeakMap/WeakSet
- **Closure Memory Traps**: Variable capture, scope management

**Use when**: Quick lookup for specific memory leak pattern

---

### Profiling Tools Comparison

**File**: [profiling-tools.md](profiling-tools.md)

Comparison matrix and usage guide for memory profiling tools:
- **Node.js**: Chrome DevTools, heapdump, memwatch-next, clinic.js
- **Python**: Scalene, memory_profiler, tracemalloc, py-spy
- **Monitoring**: Prometheus, Grafana, DataDog APM
- **Tool Selection**: When to use which tool

**Use when**: Choosing the right profiling tool for your stack

---

### Garbage Collection Guide

**File**: [garbage-collection-guide.md](garbage-collection-guide.md)

Understanding and tuning garbage collectors:
- **V8 (Node.js)**: Generational GC, heap structure, --max-old-space-size
- **Python**: Reference counting, generational GC, gc.collect()
- **GC Monitoring**: Metrics, alerts, optimization
- **GC Tuning**: When and how to tune

**Use when**: GC issues, tuning performance, understanding memory behavior

---

## Quick Lookup

**Common Patterns**:
- EventEmitter leak → [memory-optimization-patterns.md#event-listener-leaks](memory-optimization-patterns.md#event-listener-leaks)
- Connection leak → [memory-optimization-patterns.md#connection-pool-leaks](memory-optimization-patterns.md#connection-pool-leaks)
- Large dataset → [memory-optimization-patterns.md#large-dataset-patterns](memory-optimization-patterns.md#large-dataset-patterns)

**Tool Selection**:
- Node.js profiling → [profiling-tools.md#nodejs-tools](profiling-tools.md#nodejs-tools)
- Python profiling → [profiling-tools.md#python-tools](profiling-tools.md#python-tools)
- Production monitoring → [profiling-tools.md#monitoring-tools](profiling-tools.md#monitoring-tools)

**GC Issues**:
- Node.js heap → [garbage-collection-guide.md#v8-heap](garbage-collection-guide.md#v8-heap)
- Python GC → [garbage-collection-guide.md#python-gc](garbage-collection-guide.md#python-gc)
- GC metrics → [garbage-collection-guide.md#gc-monitoring](garbage-collection-guide.md#gc-monitoring)

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Full walkthroughs
- **Templates**: [Templates Index](../templates/INDEX.md) - Memory report templates
- **Main Agent**: [memory-profiler.md](../memory-profiler.md) - Memory profiler agent

---

Return to [main agent](../memory-profiler.md)
