# Heap Snapshot Analysis Guide

Detailed guide for analyzing heap snapshots in Chrome DevTools to identify memory leaks.

## Overview

Heap snapshots capture the memory state of your JavaScript application at a specific moment. By comparing snapshots, you can identify objects that are growing unexpectedly - indicating a memory leak.

## Taking Snapshots

### Chrome DevTools (Browser or Node.js)

1. Open DevTools (`F12` or `Cmd+Option+I`)
2. Go to **Memory** tab
3. Select **Heap snapshot**
4. Click **Take snapshot**

### Node.js with --inspect

```bash
node --inspect server.js
```

Open `chrome://inspect` → Click "inspect" → Memory tab

### Programmatic Snapshots

```javascript
// Using v8 (Node.js)
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
  const snapshot = v8.writeHeapSnapshot(filename);
  console.log(`Heap snapshot written to ${snapshot}`);
}

takeHeapSnapshot('./heap-before.heapsnapshot');
// ... perform actions ...
takeHeapSnapshot('./heap-after.heapsnapshot');
```

## Snapshot Views

### Summary View

Shows objects grouped by constructor name.

**Key columns:**
- **Constructor**: Object type (Array, Object, String, etc.)
- **Distance**: Steps from GC root (smaller = harder to GC)
- **Objects Count**: Number of instances
- **Shallow Size**: Memory used by object itself
- **Retained Size**: Memory freed if object is GCed (includes references)

**What to look for:**
- High **Retained Size** (objects holding lots of references)
- High **Objects Count** (many instances created)
- Custom classes with growing counts (potential leaks)

### Comparison View

Compares two snapshots to show what grew.

**Key columns:**
- **Constructor**: Object type
- **# New**: New objects created
- **# Deleted**: Objects garbage collected
- **# Delta**: Net change (New - Deleted)
- **Alloc. Size**: Memory allocated to new objects
- **Freed Size**: Memory freed from deleted objects
- **Size Delta**: Net memory change

**What to look for:**
- Positive **# Delta** (more created than deleted)
- Large **Size Delta** (significant memory growth)
- Custom classes that shouldn't persist (detached DOM, closures)

### Containment View

Shows objects organized by GC roots (Window, GC roots, closures).

**What to look for:**
- Objects unexpectedly reachable from global scope
- Closures holding references to large objects
- Detached DOM trees

### Statistics View

Pie chart showing memory distribution by object type.

**What to look for:**
- Unexpectedly large slices (e.g., 40% strings)
- Growing slices over time

## Real-World Example: React Component Leak

### Scenario

Dashboard component leaks memory on every re-render.

### Step 1: Take Baseline Snapshot

**Actions:**
1. Open application
2. Navigate to dashboard
3. Take snapshot: "Baseline"

**Results:**
- Total size: 45MB
- Objects: 250,000
- Strings: 150,000
- Arrays: 50,000

### Step 2: Reproduce Leak

**Actions:**
1. Trigger re-render 10 times (toggle settings on/off)
2. Take snapshot: "After 10 Renders"

**Results:**
- Total size: 180MB (grew 135MB!)
- Objects: 750,000 (grew 500,000!)
- Strings: 450,000 (grew 300,000!)

### Step 3: Compare Snapshots

Switch to **Comparison** view, compare "After 10 Renders" to "Baseline".

**Top growers:**

| Constructor | # Delta | Size Delta |
|-------------|---------|------------|
| (closure)   | +10,000 | +50 MB     |
| Array       | +8,000  | +40 MB     |
| Object      | +12,000 | +35 MB     |
| FiberNode   | +2,000  | +10 MB     |

**Analysis:**
- 10,000 new closures (suspicious!)
- 2,000 new FiberNodes (React internals - might indicate unmounted components not GC'd)

### Step 4: Investigate Closures

Click on **(closure)** → Sort by **Retained Size** → Expand largest closure

**Retention path:**
```
(closure) in handleDataUpdate
  size: 5 MB
  distance: 7

Retained by:
  → eventHandlers (Array)
    → WebSocketManager.listeners
      → WebSocketManager instance
        → window.wsManager (global)
          → Window (GC Root)
```

**Findings:**
1. Closure `handleDataUpdate` retains 5MB
2. Held in `eventHandlers` array
3. Array held by global `window.wsManager`
4. Never cleaned up!

### Step 5: Examine Closure Content

Click **Closure** → Expand **Scopes**

**Captured variables:**
```
[[Scopes]]:
  Closure (handleDataUpdate):
    data: Array(10000)        // 4 MB - large array captured!
    userId: "uuid-123"
    tenantId: "uuid-456"
    queryClient: Object       // 1 MB - React Query client
```

**Root Cause:**
- Closure captures large `data` array
- Closure added to event listeners on every render
- Old closures never removed
- After 10 renders: 10 closures × 5MB = 50MB leak

### Step 6: Find the Buggy Code

Use DevTools **Sources** tab → Click filename in retention path

**Buggy code:**

```typescript
// ❌ LEAKS
function Dashboard() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    // Fetch large dataset
    const fetchData = async () => {
      const result = await api.get('/data');
      setData(result);
    };
    fetchData();
  }, []);

  useEffect(() => {
    // ❌ PROBLEM: Closure captures large 'data' array
    const handleDataUpdate = (event: MessageEvent) => {
      const newItem = JSON.parse(event.data);
      // Closure needs access to 'data' to merge
      setData([...data, newItem]);
    };

    // ❌ PROBLEM: Event listener added on every render (when data changes)
    window.wsManager.on('update', handleDataUpdate);

    // ❌ PROBLEM: No cleanup!
  }, [data]); // Re-runs every time data changes

  return <div>Dashboard with {data.length} items</div>;
}
```

### The Fix

```typescript
// ✅ FIXED
function Dashboard() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await api.get('/data');
      setData(result);
    };
    fetchData();
  }, []);

  useEffect(() => {
    // ✅ FIX 1: Use functional update (doesn't capture 'data')
    const handleDataUpdate = (event: MessageEvent) => {
      const newItem = JSON.parse(event.data);
      setData(prevData => [...prevData, newItem]); // Uses previous state
    };

    window.wsManager.on('update', handleDataUpdate);

    // ✅ FIX 2: Cleanup function removes listener
    return () => {
      window.wsManager.off('update', handleDataUpdate);
    };
  }, []); // ✅ FIX 3: Empty deps - only runs once

  return <div>Dashboard with {data.length} items</div>;
}
```

### Step 7: Verify Fix

Take new snapshot: "After Fix - 10 Renders"

**Results:**
- Total size: 47MB (only 2MB growth)
- Objects: 255,000 (only 5,000 growth)
- No closure accumulation ✅

Compare "After Fix" to "Baseline":

| Constructor | # Delta | Size Delta |
|-------------|---------|------------|
| (closure)   | +1      | +0.5 MB    | ✅ Only 1 closure (correct)
| Array       | +50     | +1 MB      | ✅ Normal growth
| Object      | +100    | +0.5 MB    | ✅ Normal growth

**Leak fixed!** 🎉

## Common Retention Paths

### Global Variables

```
YourClass instance
  → window.myGlobal
    → Window (GC Root)
```

**Fix:** Remove from global scope when done
```javascript
delete window.myGlobal;
```

### Event Listeners

```
(closure) in handleClick
  → eventListeners
    → HTMLButtonElement
      → Detached HTMLDivElement
        → (No path to GC Root - but still retained!)
```

**Fix:** Remove event listeners before removing element
```javascript
button.removeEventListener('click', handleClick);
button.remove();
```

### Closures in Timers

```
(closure) in intervalCallback
  → setInterval timer
    → timers list
      → (GC Root)
```

**Fix:** Clear timers
```javascript
const id = setInterval(callback, 1000);
// Later:
clearInterval(id);
```

### React Component State

```
YourComponent (unmounted)
  → FiberNode
    → FiberNode (parent)
      → ReactDOM root
        → (GC Root)
```

**Fix:** Ensure cleanup in useEffect
```javascript
useEffect(() => {
  // Setup
  return () => {
    // Cleanup
  };
}, []);
```

### Cache/Store

```
CachedData
  → Map.entries
    → GlobalCache
      → window.cache
        → (GC Root)
```

**Fix:** Use WeakMap or implement eviction
```javascript
const cache = new WeakMap(); // Automatically GC'd
// or
const cache = new Map();
if (cache.size > 1000) {
  const firstKey = cache.keys().next().value;
  cache.delete(firstKey);
}
```

## Analysis Checklist

When analyzing heap snapshots:

- [ ] **Take baseline** before reproducing issue
- [ ] **Reproduce leak** (repeat action 10-100 times)
- [ ] **Take second snapshot** after reproduction
- [ ] **Use Comparison view** (not Summary)
- [ ] **Sort by Size Delta** (largest growth first)
- [ ] **Click on growing objects** to see retention path
- [ ] **Trace to GC root** (why is it retained?)
- [ ] **Examine Scopes** (what does closure capture?)
- [ ] **Identify buggy code** from retention path
- [ ] **Fix and verify** with new snapshot

## Advanced Techniques

### Allocation Timeline

Shows memory allocations over time.

**How to use:**
1. Memory tab → **Allocation instrumentation on timeline**
2. Click **Start**
3. Perform actions
4. Click **Stop**

**What to see:**
- Blue bars: Allocations
- Gray bars: Garbage collected
- Blue bars that don't turn gray: **Potential leaks!**

### Allocation Sampling

Low-overhead profiling of allocations.

**How to use:**
1. Memory tab → **Allocation sampling**
2. Click **Start**
3. Perform actions (can run for minutes)
4. Click **Stop**

**What to see:**
- Flame graph of allocation call stacks
- Identify which functions allocate the most memory

### Detached DOM Trees

Special view for detached DOM elements.

**How to find:**
1. Comparison view
2. Filter: `Detached`
3. Look for **HTMLElement** types with no path to document

**Example retention path:**
```
HTMLDivElement (detached)
  → closure in component
    → React FiberNode
      → (GC Root)
```

**Fix:** Nullify references to removed elements
```javascript
let myDiv = document.createElement('div');
document.body.appendChild(myDiv);
myDiv.remove();
myDiv = null; // ✅ Allow GC
```

## Tips & Tricks

1. **Force GC before snapshot:**
   - DevTools: Click trash icon before taking snapshot
   - Code: `global.gc()` (requires `--expose-gc` flag)

2. **Use descriptive constructor names:**
   ```javascript
   // ❌ Anonymous
   const obj = { data: [] };

   // ✅ Named (easier to find in snapshots)
   class DataCache {
     constructor() {
       this.data = [];
     }
   }
   const obj = new DataCache();
   ```

3. **Add custom properties for debugging:**
   ```javascript
   const cache = new Map();
   cache.__DEBUG_NAME = 'UserCache'; // Shows up in snapshots
   ```

4. **Compare multiple snapshots:**
   - Baseline (startup)
   - After action (1x)
   - After action (10x)
   - After action (100x)
   - See if growth is linear (leak) or stabilizes (normal)

5. **Export/import snapshots:**
   - Right-click snapshot → **Save as...**
   - Share with team or analyze later
   - Load in any Chrome DevTools instance

## Related Resources

- [Node.js Memory Profiling](./nodejs-memory-profiling.md)
- [Python Memory Profiling](./python-memory-profiling.md)
- [Memory Leak Checklist](../checklists/memory-leak-checklist.md)
- [Chrome DevTools Memory Docs](https://developer.chrome.com/docs/devtools/memory-problems/)

---

**Key Skill**: Reading retention paths to find leak source
**Best Practice**: Always compare snapshots (not just one snapshot)
**Pro Tip**: Sort by Retained Size (not Shallow Size) to find biggest impact
