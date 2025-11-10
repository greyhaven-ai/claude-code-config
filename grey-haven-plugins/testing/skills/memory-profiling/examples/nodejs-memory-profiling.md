# Node.js Memory Profiling Example

Real-world example of identifying and fixing a memory leak in a Node.js/Bun application.

## Scenario

A TanStack Start application has a memory leak causing production crashes after 6 hours of uptime. Memory usage grows from 150MB to 2GB before the process restarts.

## Initial Investigation

### Step 1: Reproduce Locally

Run the application with memory profiling enabled:

```bash
# Node.js
node --inspect --max-old-space-size=512 dist/server.js

# Bun
bun --inspect run server.ts
```

Open Chrome DevTools: `chrome://inspect` → Click "inspect"

### Step 2: Take Heap Snapshots

**Before load:**
1. Take initial snapshot (Baseline)
2. Memory usage: 150MB

**After simulated user activity:**
```typescript
// simulate-load.ts - Create 1000 users logging in/out
import { test } from 'vitest';

test('simulate user activity', async () => {
  for (let i = 0; i < 1000; i++) {
    await fetch('http://localhost:3000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: `user${i}@example.com`,
        password: 'password123'
      })
    });

    await fetch('http://localhost:3000/api/dashboard');

    await fetch('http://localhost:3000/api/logout', {
      method: 'POST'
    });
  }
});
```

Run load: `bun test simulate-load.ts`

Take second snapshot (After Load):
- Memory usage: 850MB (should have been ~200MB)
- **Retained size growth: 700MB - THIS IS THE LEAK**

### Step 3: Compare Snapshots

In Chrome DevTools Memory tab:
1. Select "After Load" snapshot
2. Change dropdown from "Summary" to "Comparison"
3. Compare with "Baseline"
4. Sort by "Size Delta" (largest first)

**Findings:**
- `(array)` objects: +200MB
- `(closure)` objects: +300MB
- `QueryCache` objects: +200MB

Click on `(closure)` → Expand → See retention path:
```
(closure) in handleUserActivity
  → eventListeners array
    → WebSocket connection
      → global event emitter
        → (GC Root)
```

**Root Cause Identified:** Event listeners added but never removed.

## The Bug

**File:** `src/lib/realtime.ts`

```typescript
// ❌ BUGGY CODE
export function setupRealtimeUpdates(userId: string) {
  const ws = new WebSocket(`wss://api.example.com/realtime?user=${userId}`);

  ws.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    // Update query cache
    queryClient.setQueryData(['notifications', userId], data);
  });

  ws.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
  });

  // ❌ PROBLEM: No cleanup! Event listeners persist forever
  return ws;
}
```

**Usage:** `src/routes/_authenticated/dashboard.tsx`

```typescript
// ❌ BUGGY CODE
export default function Dashboard() {
  const { user } = useAuth();

  useEffect(() => {
    // Called on every render when user data changes
    const ws = setupRealtimeUpdates(user.id);

    // ❌ PROBLEM: No cleanup function
    // WebSocket and event listeners leak on re-render or unmount
  }, [user.id]);

  return <div>Dashboard Content</div>;
}
```

**Why This Leaks:**
1. Every time `user.id` changes (or component re-renders), `setupRealtimeUpdates` is called
2. New WebSocket connection created
3. New event listeners attached
4. Old WebSocket and listeners never cleaned up
5. After 1000 users, 1000 WebSocket connections and 2000 event listeners exist

## The Fix

### Fixed Code

**File:** `src/lib/realtime.ts`

```typescript
// ✅ FIXED CODE
export function setupRealtimeUpdates(userId: string) {
  const ws = new WebSocket(`wss://api.example.com/realtime?user=${userId}`);

  const handleMessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);
    queryClient.setQueryData(['notifications', userId], data);
  };

  const handleError = (error: Event) => {
    console.error('WebSocket error:', error);
  };

  ws.addEventListener('message', handleMessage);
  ws.addEventListener('error', handleError);

  // ✅ FIX: Return cleanup function
  return () => {
    ws.removeEventListener('message', handleMessage);
    ws.removeEventListener('error', handleError);
    ws.close();
  };
}
```

**Usage:** `src/routes/_authenticated/dashboard.tsx`

```typescript
// ✅ FIXED CODE
export default function Dashboard() {
  const { user } = useAuth();

  useEffect(() => {
    const cleanup = setupRealtimeUpdates(user.id);

    // ✅ FIX: Cleanup on unmount or user change
    return cleanup;
  }, [user.id]);

  return <div>Dashboard Content</div>;
}
```

## Verification

### Re-run Load Test

```bash
bun test simulate-load.ts
```

**Results:**
- Before fix: Memory growth 150MB → 850MB (leak)
- After fix: Memory stabilizes at 200MB ✅

### Heap Snapshot Comparison

Take new "After Fix" snapshot:
- `(array)` objects: +10MB (normal)
- `(closure)` objects: +5MB (normal)
- `QueryCache` objects: +15MB (normal)
- **Total growth: 30MB (expected for cache) ✅**

### Extended Test

Run for 6 hours in production:
```bash
# Monitor memory every minute
watch -n 60 'ps aux | grep node'
```

**Results:**
- Memory stable at 180-220MB throughout 6 hours ✅
- No crashes ✅
- Leak fixed! 🎉

## Key Takeaways

### Common Node.js Leak Patterns

1. **Event Listeners Not Removed**
   ```typescript
   // ❌ Leaks
   window.addEventListener('resize', handler);

   // ✅ Fixed
   window.addEventListener('resize', handler);
   return () => window.removeEventListener('resize', handler);
   ```

2. **Timers Not Cleared**
   ```typescript
   // ❌ Leaks
   const interval = setInterval(() => { ... }, 1000);

   // ✅ Fixed
   const interval = setInterval(() => { ... }, 1000);
   return () => clearInterval(interval);
   ```

3. **Closures Capturing Large Objects**
   ```typescript
   // ❌ Leaks
   const largeData = await fetchLargeDataset();
   const handler = () => {
     // Closure captures entire largeData
     console.log(largeData[0]);
   };

   // ✅ Fixed
   const largeData = await fetchLargeDataset();
   const firstItem = largeData[0];
   const handler = () => {
     // Closure only captures firstItem
     console.log(firstItem);
   };
   ```

4. **Unbounded Caches**
   ```typescript
   // ❌ Leaks
   const cache = new Map();
   function getUser(id) {
     if (!cache.has(id)) {
       cache.set(id, fetchUser(id));
     }
     return cache.get(id);
   }

   // ✅ Fixed (with size limit)
   const cache = new Map();
   const MAX_SIZE = 1000;
   function getUser(id) {
     if (!cache.has(id)) {
       if (cache.size >= MAX_SIZE) {
         const firstKey = cache.keys().next().value;
         cache.delete(firstKey);
       }
       cache.set(id, fetchUser(id));
     }
     return cache.get(id);
   }
   ```

### Debugging Tools

**Chrome DevTools:**
- Heap snapshots (compare before/after)
- Allocation timeline (see allocations over time)
- Allocation sampling (profile with less overhead)

**Node.js --inspect:**
```bash
node --inspect --max-old-space-size=512 server.js
```

**Bun.inspect():**
```typescript
Bun.inspect(process.memoryUsage());
```

**Heap Dump:**
```bash
npm install -g heapdump
node -r heapdump server.js

# In code:
const heapdump = require('heapdump');
heapdump.writeSnapshot('/tmp/heap-' + Date.now() + '.heapsnapshot');
```

### Prevention

1. **Always clean up in useEffect:**
   ```typescript
   useEffect(() => {
     // Setup
     return () => {
       // ✅ Cleanup
     };
   }, [deps]);
   ```

2. **Use WeakMap/WeakSet for caches:**
   ```typescript
   const cache = new WeakMap(); // ✅ Automatically GC'd
   ```

3. **Profile regularly:**
   - Add memory profiling to CI/CD
   - Monitor production memory metrics
   - Alert on memory growth

4. **Test for leaks:**
   ```typescript
   test('no memory leak on mount/unmount', async () => {
     const before = process.memoryUsage().heapUsed;

     for (let i = 0; i < 100; i++) {
       const { unmount } = render(<Dashboard />);
       unmount();
     }

     global.gc(); // Force GC (node --expose-gc)
     const after = process.memoryUsage().heapUsed;

     const growth = after - before;
     expect(growth).toBeLessThan(10 * 1024 * 1024); // < 10MB
   });
   ```

## Related Resources

- [Memory Leak Checklist](../checklists/memory-leak-checklist.md)
- [Heap Snapshot Analysis](./heap-snapshot-analysis.md)
- [Chrome DevTools Memory Profiling](https://developer.chrome.com/docs/devtools/memory-problems/)
- [Node.js --inspect](https://nodejs.org/en/docs/guides/debugging-getting-started/)

---

**Leak Pattern**: Event listeners + closures
**Time to Fix**: 2 hours (investigation + fix + verification)
**Memory Saved**: 700MB per 1000 users
**Impact**: Production stability restored ✅
