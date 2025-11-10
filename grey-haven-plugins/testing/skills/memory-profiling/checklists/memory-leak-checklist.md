# Memory Leak Detection Checklist

Systematic process for identifying and fixing memory leaks in JavaScript/TypeScript and Python applications.

## Pre-Investigation Setup

- [ ] Confirm memory leak symptoms (growing memory over time)
- [ ] Identify runtime environment (Node.js, Bun, Browser, Python)
- [ ] Install profiling tools for your platform
- [ ] Set up test environment that reproduces the issue
- [ ] Document baseline memory usage

## Initial Profiling

- [ ] **Take initial heap snapshot** (before operations)
- [ ] **Perform leak-inducing operations** (user actions, API calls, etc.)
- [ ] **Take second heap snapshot** (after operations)
- [ ] **Compare snapshots** to identify growing objects
- [ ] **Document object types with largest growth**

## Common Leak Patterns Check

### Event Listeners
- [ ] Check for event listeners added but not removed
- [ ] Verify `removeEventListener` called when components unmount
- [ ] Check for `once: true` option where applicable
- [ ] Audit global event listeners (window, document)

### Timers
- [ ] Check for `setInterval` without corresponding `clearInterval`
- [ ] Check for `setTimeout` in loops without cleanup
- [ ] Verify timers cleared when components unmount
- [ ] Check for recursive `setTimeout` patterns

### Closures
- [ ] Identify closures capturing large objects
- [ ] Check for closures in event handlers holding references
- [ ] Verify closures don't prevent GC of parent scopes
- [ ] Look for closures in long-lived callbacks

### Caches
- [ ] Check for unbounded caches (no size limit)
- [ ] Verify cache eviction policies exist
- [ ] Check for caches using WeakMap where appropriate
- [ ] Audit memory caches vs persistent storage

### DOM (Browser only)
- [ ] Check for detached DOM nodes
- [ ] Verify elements removed from DOM are nullified
- [ ] Check for event listeners on removed elements
- [ ] Audit third-party library cleanup

### Circular References
- [ ] Identify circular object references
- [ ] Check if objects properly break cycles
- [ ] Verify objects are nullified when done
- [ ] Use weak references where cycles unavoidable

## Retention Path Analysis

- [ ] **Select suspect objects** from heap snapshot
- [ ] **Trace retention paths** to GC roots
- [ ] **Identify what's holding references**
- [ ] **Document source of each leak**

## Fix Implementation

- [ ] **Implement cleanup logic** for identified leaks
- [ ] **Add cleanup to component unmount** (React useEffect cleanup)
- [ ] **Clear timers and intervals** when done
- [ ] **Remove event listeners** when no longer needed
- [ ] **Nullify references** to large objects
- [ ] **Implement cache eviction** if using unbounded caches

## Verification

- [ ] **Re-run profiling** with fixes applied
- [ ] **Compare new snapshots** - memory should stabilize
- [ ] **Run extended test** (hours if needed)
- [ ] **Monitor production** after deployment
- [ ] **Document baseline** for future comparison

## Node.js/Bun Specific

- [ ] Check for large buffers not released
- [ ] Verify streams properly ended
- [ ] Check for unclosed database connections
- [ ] Audit HTTP keep-alive connections
- [ ] Verify worker threads properly terminated

## Python Specific

- [ ] Check for circular references in custom classes
- [ ] Verify `__del__` not preventing GC
- [ ] Check for global variables holding references
- [ ] Audit large collections (lists, dicts) not cleared
- [ ] Verify generators properly closed

## Production Deployment

- [ ] **Set memory limits** (NODE_OPTIONS=--max-old-space-size, ulimit)
- [ ] **Configure monitoring** (memory usage alerts)
- [ ] **Set up profiling** in production (--inspect flag, memory_profiler)
- [ ] **Document fix** in changelog
- [ ] **Monitor metrics** post-deployment

## Scoring

- **All checks passed**: Excellent - Leak likely fixed ✅
- **35+ items checked**: Good - Most leaks addressed ⚠️
- **25-34 items**: Fair - More investigation needed 🔴
- **<25 items**: Poor - Leak likely still present ❌

## Common Mistakes to Avoid

❌ **Don't:**
- Profile in development mode (enables leak checks that impact performance)
- Assume small leaks don't matter (they compound)
- Only test for short durations (some leaks take time to manifest)
- Ignore memory spikes (may indicate allocation issues)
- Profile without reproducing the leak first

✅ **Do:**
- Profile in production mode
- Test for extended periods (hours)
- Monitor real user patterns
- Fix root causes, not symptoms
- Document findings and fixes

## Tools by Platform

**JavaScript/TypeScript:**
- Chrome DevTools Memory Profiler
- Node.js --inspect flag
- Bun.inspect()

**Python:**
- memory_profiler
- tracemalloc
- pympler
- objgraph

## Next Steps If Leak Persists

1. Review [common-leak-patterns.md](../reference/common-leak-patterns.md)
2. Deep dive with [heap-snapshot-analysis.md](../examples/heap-snapshot-analysis.md)
3. Check platform-specific guides:
   - [nodejs-memory-profiling.md](../examples/nodejs-memory-profiling.md)
   - [python-memory-profiling.md](../examples/python-memory-profiling.md)
4. Consider consulting memory-profiler agent

## Related Resources

- [Examples](../examples/INDEX.md)
- [Profiling Tools](../reference/profiling-tools.md)
- [Optimization Techniques](../reference/optimization-techniques.md)

---

**Total Checks**: 50+ items
**Coverage**: JavaScript, TypeScript, Node.js, Bun, Python
**Critical Checks**: Event listeners, Timers, Closures, Caches
**Last Updated**: 2025-11-09
