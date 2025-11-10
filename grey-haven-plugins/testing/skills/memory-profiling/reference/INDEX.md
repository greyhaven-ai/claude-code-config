# Memory Profiling Reference

Technical reference for memory profiling tools, concepts, and optimization techniques.

## Reference Materials

1. **[Profiling Tools](profiling-tools.md)** - Complete tool reference
   - Chrome DevTools Memory Profiler
   - Node.js Inspector
   - Bun memory profiling
   - Python memory_profiler
   - tracemalloc
   - pympler
   - Tool comparison and selection

2. **[Memory Concepts](memory-concepts.md)** - Understanding memory management
   - Heap vs Stack
   - Garbage collection algorithms (Mark-and-Sweep, Generational GC)
   - Retention paths
   - Shallow vs Retained size
   - Memory lifecycle

3. **[Optimization Techniques](optimization-techniques.md)** - Memory reduction strategies
   - Object pooling
   - Weak references (WeakMap, WeakSet)
   - Lazy loading
   - Data structure optimization
   - Caching strategies
   - Resource cleanup patterns

4. **[Common Leak Patterns](common-leak-patterns.md)** - Identifying typical leaks
   - Event listener leaks
   - Closure leaks
   - Cache leaks
   - Timer leaks (setInterval, setTimeout)
   - DOM leaks
   - Circular references
   - Detection and prevention

## Quick Links

- For examples: See [examples/](../examples/INDEX.md)
- For checklists: See [checklists/](../checklists/)
- For templates: See [templates/](../templates/)

---

**Coverage**: Tools, Concepts, Techniques, Patterns
**Platforms**: JavaScript, TypeScript, Node.js, Bun, Python
**Last Updated**: 2025-11-09
