# Backend Optimization Examples

Server-side performance optimizations for Node.js/FastAPI applications with measurable throughput improvements.

## Example 1: Async/Parallel Processing

### Problem: Sequential Operations

```typescript
// ❌ BEFORE: Sequential - 1,500ms total
async function getUserProfile(userId: string) {
  const user = await db.user.findUnique({ where: { id: userId } });
  const orders = await db.order.findMany({ where: { userId } });
  const reviews = await db.review.findMany({ where: { userId } });
  
  return { user, orders, reviews };
}

// Total time: 500ms + 600ms + 400ms = 1,500ms
```

### Solution: Parallel with Promise.all

```typescript
// ✅ AFTER: Parallel - 600ms total (2.5x faster)
async function getUserProfileOptimized(userId: string) {
  const [user, orders, reviews] = await Promise.all([
    db.user.findUnique({ where: { id: userId } }),     // 500ms
    db.order.findMany({ where: { userId } }),           // 600ms
    db.review.findMany({ where: { userId } })           // 400ms
  ]);
  
  return { user, orders, reviews };
}

// Total time: max(500, 600, 400) = 600ms
// Performance gain: 2.5x faster
```

---

## Example 2: Streaming Large Files

### Problem: Loading Entire File

```typescript
// ❌ BEFORE: Load 1GB file into memory
import fs from 'fs';

async function processLargeFile(path: string) {
  const data = fs.readFileSync(path); // Loads entire file
  const lines = data.toString().split('\n');
  
  for (const line of lines) {
    await processLine(line);
  }
}

// Memory: 1GB
// Time: 5,000ms
```

### Solution: Stream Processing

```typescript
// ✅ AFTER: Stream with readline
import fs from 'fs';
import readline from 'readline';

async function processLargeFileOptimized(path: string) {
  const stream = fs.createReadStream(path);
  const rl = readline.createInterface({ input: stream });
  
  for await (const line of rl) {
    await processLine(line);
  }
}

// Memory: 15MB (constant)
// Time: 4,800ms
// Memory gain: 67x less
```

---

## Example 3: Worker Threads for CPU-Intensive Tasks

### Problem: Blocking Event Loop

```typescript
// ❌ BEFORE: CPU-intensive task blocks server
function generateReport(data: any[]) {
  // Heavy computation blocks event loop for 3 seconds
  const result = complexCalculation(data);
  return result;
}

app.get('/report', (req, res) => {
  const report = generateReport(largeDataset);
  res.json(report);
});

// While generating: All requests blocked for 3s
// Throughput: 0 req/s during computation
```

### Solution: Worker Threads

```typescript
// ✅ AFTER: Worker thread doesn't block event loop
import { Worker } from 'worker_threads';

function generateReportAsync(data: any[]): Promise<any> {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./report-worker.js');
    worker.postMessage(data);
    worker.on('message', resolve);
    worker.on('error', reject);
  });
}

app.get('/report', async (req, res) => {
  const report = await generateReportAsync(largeDataset);
  res.json(report);
});

// Other requests: Continue processing normally
// Throughput: 200 req/s maintained
```

---

## Example 4: Request Batching

### Problem: Many Small Requests

```typescript
// ❌ BEFORE: Individual requests to external API
async function enrichUsers(users: User[]) {
  for (const user of users) {
    user.details = await externalAPI.getDetails(user.id);
  }
  return users;
}

// 1000 users = 1000 API calls = 50,000ms
```

### Solution: Batch Requests

```typescript
// ✅ AFTER: Batch requests
async function enrichUsersOptimized(users: User[]) {
  const batchSize = 100;
  const results: any[] = [];
  
  for (let i = 0; i < users.length; i += batchSize) {
    const batch = users.slice(i, i + batchSize);
    const batchResults = await externalAPI.getBatch(
      batch.map(u => u.id)
    );
    results.push(...batchResults);
  }
  
  users.forEach((user, i) => {
    user.details = results[i];
  });
  
  return users;
}

// 1000 users = 10 batch calls = 2,500ms (20x faster)
```

---

## Example 5: Connection Pooling

### Problem: New Connection Per Request

```python
# ❌ BEFORE: New connection each time (Python/FastAPI)
from sqlalchemy import create_engine

def get_user(user_id: int):
    engine = create_engine("postgresql://...")  # New connection
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM users WHERE id = %s", user_id)
        return result.fetchone()

# Per request: 150ms (connect) + 20ms (query) = 170ms
```

### Solution: Connection Pool

```python
# ✅ AFTER: Reuse pooled connections
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://...",
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10
)

def get_user_optimized(user_id: int):
    with engine.connect() as conn:  # Reuses connection
        result = conn.execute("SELECT * FROM users WHERE id = %s", user_id)
        return result.fetchone()

# Per request: 0ms (pool) + 20ms (query) = 20ms (8.5x faster)
```

---

## Summary

| Optimization | Before | After | Gain | Use Case |
|--------------|--------|-------|------|----------|
| **Parallel Processing** | 1,500ms | 600ms | 2.5x | Independent operations |
| **Streaming** | 1GB mem | 15MB | 67x | Large files |
| **Worker Threads** | 0 req/s | 200 req/s | ∞ | CPU-intensive |
| **Request Batching** | 1000 calls | 10 calls | 100x | External APIs |
| **Connection Pool** | 170ms | 20ms | 8.5x | Database queries |

---

**Previous**: [Frontend Optimization](frontend-optimization.md) | **Index**: [Examples Index](INDEX.md)
