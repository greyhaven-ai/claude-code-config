# Memory Profiling Examples

Production memory profiling implementations for Node.js and Python with leak detection, heap analysis, and optimization strategies.

## Examples Overview

### Node.js Memory Leak Detection

**File**: [nodejs-memory-leak.md](nodejs-memory-leak.md)

Identifying and fixing memory leaks in Node.js applications:
- **Memory leak detection**: Chrome DevTools, heapdump analysis
- **Common leak patterns**: Event listeners, closures, global variables
- **Heap snapshots**: Before/after comparison, retained object analysis
- **Real leak**: EventEmitter leak causing 2GB memory growth
- **Fix**: Proper cleanup with `removeListener()`, WeakMap for caching
- **Result**: Memory stabilized at 150MB (93% reduction)

**Use when**: Node.js memory growing over time, debugging production memory issues

---

### Python Memory Profiling with Scalene

**File**: [python-scalene-profiling.md](python-scalene-profiling.md)

Line-by-line memory profiling for Python applications:
- **Scalene setup**: Installation, pytest integration, CLI usage
- **Memory hotspots**: Line-by-line allocation tracking
- **CPU + Memory**: Combined profiling for performance bottlenecks
- **Real scenario**: 500MB dataset causing OOM, fixed with generators
- **Optimization**: List comprehension → generator (500MB → 5MB)
- **Result**: 99% memory reduction, no OOM errors

**Use when**: Python memory spikes, profiling pytest tests, finding allocation hotspots

---

### Database Connection Pool Leak

**File**: [database-connection-leak.md](database-connection-leak.md)

PostgreSQL connection pool exhaustion and memory leaks:
- **Symptom**: Connection pool maxed out, memory growing linearly
- **Root cause**: Unclosed connections in error paths, missing `finally` blocks
- **Detection**: Connection pool metrics, memory profiling
- **Fix**: Context managers (`with` statement), proper cleanup
- **Result**: Zero connection leaks, memory stable at 80MB

**Use when**: Database connection errors, "too many clients" errors, connection pool issues

---

### Large Dataset Memory Optimization

**File**: [large-dataset-optimization.md](large-dataset-optimization.md)

Memory-efficient data processing for large datasets:
- **Problem**: Loading 10GB CSV into memory (OOM killer)
- **Solutions**: Streaming with `pandas.read_csv(chunksize)`, generators, memory mapping
- **Techniques**: Lazy evaluation, columnar processing, batch processing
- **Before/After**: 10GB memory → 500MB (95% reduction)
- **Tools**: Pandas chunking, Dask for parallel processing

**Use when**: Processing large files, OOM errors, batch data processing

---

## Quick Navigation

| Topic | File | Lines | Focus |
|-------|------|-------|-------|
| **Node.js Leaks** | [nodejs-memory-leak.md](nodejs-memory-leak.md) | ~450 | EventEmitter, heap snapshots |
| **Python Scalene** | [python-scalene-profiling.md](python-scalene-profiling.md) | ~420 | Line-by-line profiling |
| **DB Connection Leaks** | [database-connection-leak.md](database-connection-leak.md) | ~380 | Connection pool management |
| **Large Datasets** | [large-dataset-optimization.md](large-dataset-optimization.md) | ~400 | Streaming, chunking |

## Related Documentation

- **Reference**: [Reference Index](../reference/INDEX.md) - Memory patterns, profiling tools
- **Templates**: [Templates Index](../templates/INDEX.md) - Profiling report template
- **Main Agent**: [memory-profiler.md](../memory-profiler.md) - Memory profiler agent

---

Return to [main agent](../memory-profiler.md)
