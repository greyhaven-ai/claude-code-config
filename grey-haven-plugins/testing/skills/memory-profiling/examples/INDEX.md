# Memory Profiling Examples

Real-world examples of memory leak detection and optimization for JavaScript/TypeScript and Python applications.

## Available Examples

1. **[Memory Leak Detection](memory-leak-detection.md)** - Finding and fixing common leaks
   - Event listener leaks
   - Closure leaks
   - Cache leaks
   - Timer leaks

2. **[Heap Snapshot Analysis](heap-snapshot-analysis.md)** - Using Chrome DevTools
   - Taking heap snapshots
   - Comparing snapshots
   - Reading retention paths
   - Identifying leak sources

3. **[Node.js Memory Profiling](nodejs-memory-profiling.md)** - Server-side profiling
   - Using Node.js inspector
   - Analyzing V8 heap
   - Production profiling with --inspect
   - Memory leak in Express app

4. **[Python Memory Profiling](python-memory-profiling.md)** - Python-specific techniques
   - Using memory_profiler
   - tracemalloc for leak detection
   - pympler for detailed analysis
   - FastAPI memory leak example

## Recommended Path

**For memory leak investigations:**
1. Start with [memory-leak-detection.md](memory-leak-detection.md)
2. Learn [heap-snapshot-analysis.md](heap-snapshot-analysis.md) for your runtime
3. Apply techniques to your specific stack:
   - Node.js: [nodejs-memory-profiling.md](nodejs-memory-profiling.md)
   - Python: [python-memory-profiling.md](python-memory-profiling.md)

**For optimization:**
1. Profile current usage with [heap-snapshot-analysis.md](heap-snapshot-analysis.md)
2. Identify hotspots from [memory-leak-detection.md](memory-leak-detection.md)
3. Apply fixes and verify improvement

## Quick Reference by Issue Type

### Growing Memory Over Time
- See [memory-leak-detection.md](memory-leak-detection.md#continuous-growth)
- Check: Event listeners, timers, caches

### High Initial Memory
- See [heap-snapshot-analysis.md](heap-snapshot-analysis.md#large-objects)
- Check: Large data structures, inefficient data formats

### Garbage Collection Issues
- See [nodejs-memory-profiling.md](nodejs-memory-profiling.md#gc-analysis)
- See [python-memory-profiling.md](python-memory-profiling.md#gc-behavior)

### Production Out of Memory
- See [nodejs-memory-profiling.md](nodejs-memory-profiling.md#production-profiling)
- See [python-memory-profiling.md](python-memory-profiling.md#production-debugging)

## Example Usage

```bash
# View memory leak detection guide
cat examples/memory-leak-detection.md

# Learn heap snapshot analysis
cat examples/heap-snapshot-analysis.md

# Platform-specific guide
cat examples/nodejs-memory-profiling.md    # For Node.js/Bun
cat examples/python-memory-profiling.md    # For Python/FastAPI
```

## Related Materials

- **[Profiling Tools](../reference/profiling-tools.md)** - Complete tool reference
- **[Optimization Techniques](../reference/optimization-techniques.md)** - Memory reduction strategies
- **[Memory Leak Checklist](../checklists/memory-leak-checklist.md)** - Systematic detection process

---

**Total Examples**: 4 comprehensive guides
**Coverage**: JavaScript, TypeScript, Node.js, Bun, Python, FastAPI
**Last Updated**: 2025-11-09
