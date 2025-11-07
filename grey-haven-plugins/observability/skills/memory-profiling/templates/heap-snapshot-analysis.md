# Heap Snapshot Analysis Checklist

Step-by-step guide for analyzing V8 heap snapshots in Chrome DevTools to identify memory leaks.

## Prerequisites

- [ ] Node.js service running with `--inspect` flag
- [ ] Chrome DevTools connected (chrome://inspect)
- [ ] Baseline snapshot captured (before leak appears)
- [ ] Leak snapshot captured (after memory growth)

---

## Phase 1: Snapshot Collection

### When to Capture Snapshots

**Baseline Snapshot**:
- [ ] Capture immediately after service starts
- [ ] After warm-up period (first 100 requests)
- [ ] Before leak appears (memory stable)

**Leak Snapshot**:
- [ ] After observing memory growth (e.g., +100MB)
- [ ] After specific number of requests (e.g., 10,000)
- [ ] After time period (e.g., 1 hour)

**Optional: Multiple Leak Snapshots**:
- [ ] Snapshot 2: After 2x memory growth
- [ ] Snapshot 3: After 3x memory growth
- [ ] Helps identify linear vs exponential growth

### How to Capture

**Method 1: Chrome DevTools UI**:
1. Open Chrome DevTools → Memory tab
2. Select "Heap snapshot"
3. Click "Take snapshot"
4. Wait for snapshot to complete
5. Snapshot appears in left sidebar

**Method 2: heapdump package**:
```bash
# Send SIGUSR2 signal to Node.js process
kill -USR2 <pid>

# Snapshot saved to ./heapdump-<timestamp>.heapsnapshot
# Load in DevTools: Memory → Load → select file
```

---

## Phase 2: Snapshot Comparison

### Load and Compare

- [ ] Load baseline snapshot in DevTools
- [ ] Load leak snapshot in DevTools
- [ ] Click "Comparison" view
- [ ] Select "Compare with baseline"

### Interpretation

**Comparison Table Columns**:
```
Constructor   | # New | # Deleted | # Delta | Size Delta
--------------|-------|-----------|---------|------------
EventEmitter  | +500  | -0        | +500    | +2.5 MB
Closure       | +100  | -0        | +100    | +1.2 MB
Array         | +50   | -10       | +40     | +800 KB
```

**Red Flags**:
- [ ] Large positive # Delta (objects not being GC'd)
- [ ] Size Delta in MB range (significant memory)
- [ ] System objects growing (Array, String, Object)
- [ ] Application objects accumulating (User, Order, etc.)

### Top Candidates for Investigation

**Sort by**:
1. [ ] Size Delta (descending) - biggest memory impact
2. [ ] # Delta (descending) - most objects leaked

**Focus on**:
- Top 5 constructors by size
- Application-specific objects (not native types)
- Objects with +100 or more instances

---

## Phase 3: Retainer Analysis

### Select Leaked Object

- [ ] Click on constructor with large delta
- [ ] Select individual object instance
- [ ] View "Retainers" panel (bottom of DevTools)

### Understand Retainer Path

**Example Retainer Path**:
```
Window / Global
  → global_handlers (Array)
    → EventEmitter@12345
      → _events (Object)
        → data (Array[500])
          → [handler function]
            → [leaked object]
```

**Interpretation**:
- Root: What's keeping object alive (Window, Global, Module)
- Path: Chain of references preventing GC
- Leaf: The leaked object

### Common Leak Patterns in Retainer Paths

**EventEmitter Leak**:
```
EventEmitter → _events → [event name] → Array → handler → [captured variables]
```
- [ ] Check if event listeners are removed
- [ ] Verify `removeListener()` or `once()` usage

**Closure Leak**:
```
Global → function → [[Scopes]] → Closure → [large object]
```
- [ ] Check what variables closure captures
- [ ] Verify if all captured variables are needed

**Timer Leak**:
```
Global → Timeout → [timer callback] → [captured variables]
```
- [ ] Check if `clearTimeout()` or `clearInterval()` called
- [ ] Verify timer lifecycle management

**Connection Leak**:
```
Global → connection_pool → active_connections → Connection → [query results]
```
- [ ] Check if connections are closed
- [ ] Verify `try/finally` or context manager usage

---

## Phase 4: Code Mapping

### Find Source Code

**From Retainer Path**:
- [ ] Note function names in retainer path
- [ ] Note variable names
- [ ] Look for file names (if source maps available)

**Search Codebase**:
```bash
# Search for function name
grep -r "functionName" src/

# Search for event name
grep -r "emitter.on('eventName')" src/

# Search for variable name
grep -r "variableName" src/
```

### Identify Vulnerable Code

**Checklist**:
- [ ] Find where object is created
- [ ] Find where object should be cleaned up
- [ ] Verify cleanup happens in all code paths
- [ ] Check exception handling (try/catch/finally)

**Example**:
```typescript
// Found in retainer path: "DataProcessor.process"
// File: src/services/data-processor.ts:42

class DataProcessor {
  process() {
    this.emitter.on('data', handler);  // ← No removeListener!
    // ...
  }
}
```

---

## Phase 5: Verification

### Reproduce Locally

- [ ] Reproduce leak in dev environment
- [ ] Capture heap snapshots locally
- [ ] Verify same leak pattern appears

### Test Fix

**Before Fix**:
- [ ] Capture baseline snapshot
- [ ] Run 1000 operations
- [ ] Capture leak snapshot
- [ ] Verify leak appears in comparison

**After Fix**:
- [ ] Apply fix
- [ ] Capture new baseline
- [ ] Run 1000 operations
- [ ] Capture new snapshot
- [ ] Verify leak eliminated (# Delta ≈ 0)

### Automated Test

```typescript
// Memory leak test
describe('DataProcessor', () => {
  it('should not leak listeners', () => {
    const processor = new DataProcessor();
    const before = processor.emitter.listenerCount('data');

    for (let i = 0; i < 1000; i++) {
      processor.process();
    }

    const after = processor.emitter.listenerCount('data');
    expect(after).toBe(before); // No leak
  });
});
```

---

## Phase 6: Documentation

### Record Findings

**Leak Summary**:
- Constructor leaking: [Name]
- Size leaked: [X MB]
- Number of instances: [Count]
- Growth rate: [MB/hour or instances/request]

**Root Cause**:
- Pattern: [EventEmitter leak, closure trap, etc.]
- File: [filepath:line]
- Function: [function name]

**Fix**:
- Strategy: [removeListener, close connection, clear timer, etc.]
- Code change: [Brief description]
- PR link: [URL]

### Save Artifacts

- [ ] Save heap snapshots (.heapsnapshot files)
- [ ] Screenshot comparison view
- [ ] Screenshot retainer path
- [ ] Copy retainer path text
- [ ] Save to incident report or wiki

---

## Quick Reference: DevTools Navigation

### Memory Tab Views

**Summary View** (default):
- Shows all objects by constructor
- Sortable by size, count

**Comparison View**:
- Shows delta between snapshots
- Sortable by size delta, # delta

**Containment View**:
- Shows object graph from roots
- Useful for understanding structure

**Statistics View**:
- Pie chart of memory by type
- Quick overview of distribution

### Filtering

**Filter by Constructor**:
```
Type in filter box: "EventEmitter"
Shows only EventEmitter objects
```

**Filter by Size**:
```
Objects: size > 1000000  (objects >1MB)
```

**Filter by Retainer**:
```
Objects retained by: "global_handlers"
```

---

## Common Leak Patterns and Retainer Paths

### 1. EventEmitter Leak

**Retainer Path**:
```
EventEmitter → _events → [event_name] → Array[500] → handler
```

**Code Pattern**:
```typescript
// ❌ Leak: Listener added but never removed
emitter.on('data', handler);
```

**Fix**:
```typescript
// ✅ Fix: Remove listener or use once()
emitter.once('data', handler);
// or
emitter.on('data', handler);
emitter.removeListener('data', handler);
```

---

### 2. Closure Leak

**Retainer Path**:
```
Global → function → [[Scopes]] → Closure → largeObject
```

**Code Pattern**:
```typescript
// ❌ Leak: Closure captures large object
function createHandler(largeBuffer) {
  return () => console.log(largeBuffer.length);
}
```

**Fix**:
```typescript
// ✅ Fix: Extract only needed value
function createHandler(largeBuffer) {
  const length = largeBuffer.length;
  return () => console.log(length);
}
```

---

### 3. Timer Leak

**Retainer Path**:
```
Global → Timeout → callback → capturedVariables
```

**Code Pattern**:
```typescript
// ❌ Leak: Timer never cleared
setInterval(() => {
  process();
}, 1000);
```

**Fix**:
```typescript
// ✅ Fix: Clear timer on cleanup
const id = setInterval(() => process(), 1000);
// Later:
clearInterval(id);
```

---

### 4. Connection Leak

**Retainer Path**:
```
Global → connection_pool → active_connections → Connection
```

**Code Pattern**:
```python
# ❌ Leak: Connection never closed
conn = pool.acquire()
result = conn.execute(query)
return result  # Conn never released
```

**Fix**:
```python
# ✅ Fix: Use context manager
with pool.acquire() as conn:
    result = conn.execute(query)
    return result  # Conn auto-released
```

---

## Related Documentation

- **Memory Report Template**: [memory-report-template.md](memory-report-template.md)
- **Pattern Catalog**: [../reference/memory-optimization-patterns.md](../reference/memory-optimization-patterns.md)
- **Examples**: [../examples/nodejs-memory-leak.md](../examples/nodejs-memory-leak.md)

---

Return to [templates index](INDEX.md)
