---
name: grey-haven-performance
description: Optimize Grey Haven applications for performance - React rendering, TanStack Query caching, database queries (N+1 prevention), connection pooling, Cloudflare caching, lazy loading, and bundle size optimization. Use when performance issues detected.
---

# Grey Haven Performance Optimization

Optimize **frontend and backend performance** for Grey Haven Studio applications following proven patterns for React, TanStack Query, database queries, and Cloudflare Workers.

## Frontend Performance (React + TanStack)

### React Rendering Optimization

#### useMemo for Expensive Calculations
```typescript
// app/routes/dashboard.tsx
import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

function Dashboard() {
  const { data: users } = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
  });

  // [X] Bad - Recalculates on every render
  const activeUsers = users?.filter((u) => u.isActive);

  // [OK] Good - Memoize expensive calculation
  const activeUsers = useMemo(
    () => users?.filter((u) => u.isActive) ?? [],
    [users]
  );

  // [OK] Good - Memoize complex transformations
  const usersByDepartment = useMemo(() => {
    if (!users) return {};
    return users.reduce((acc, user) => {
      const dept = user.department || "Unknown";
      if (!acc[dept]) acc[dept] = [];
      acc[dept].push(user);
      return acc;
    }, {} as Record<string, typeof users>);
  }, [users]);

  return <div>{/* Render activeUsers */}</div>;
}
```

#### React.memo for Component Memoization
```typescript
// app/components/UserCard.tsx
import { memo } from "react";

// [X] Bad - Re-renders when parent re-renders (even if props unchanged)
function UserCard({ user }: { user: User }) {
  return (
    <div>
      <h3>{user.fullName}</h3>
      <p>{user.email}</p>
    </div>
  );
}

// [OK] Good - Only re-renders when user prop changes
export const UserCard = memo(function UserCard({ user }: { user: User }) {
  return (
    <div>
      <h3>{user.fullName}</h3>
      <p>{user.email}</p>
    </div>
  );
});

// [OK] Good - Custom comparison for complex props
export const UserCard = memo(
  function UserCard({ user }: { user: User }) {
    return (
      <div>
        <h3>{user.fullName}</h3>
        <p>{user.email}</p>
      </div>
    );
  },
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
);
```

#### useCallback for Stable Function References
```typescript
// app/routes/users.tsx
import { useCallback } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

function UserList() {
  const queryClient = useQueryClient();

  // [X] Bad - New function on every render (causes child re-renders)
  const handleDelete = (userId: string) => {
    deleteUser(userId);
  };

  // [OK] Good - Stable function reference
  const handleDelete = useCallback(
    (userId: string) => {
      deleteUser(userId);
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
    [queryClient]
  );

  return (
    <div>
      {users.map((user) => (
        <UserCard key={user.id} user={user} onDelete={handleDelete} />
      ))}
    </div>
  );
}
```

### TanStack Query Performance

#### Query Caching and Stale Time
```typescript
// app/utils/query-client.ts
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Cache data for 5 minutes
      staleTime: 1000 * 60 * 5,

      // Keep unused data in cache for 10 minutes
      gcTime: 1000 * 60 * 10,

      // Refetch on window focus (disable for better performance)
      refetchOnWindowFocus: false,

      // Retry failed requests (max 3 times)
      retry: 3,
    },
  },
});
```

#### Query Prefetching
```typescript
// app/routes/dashboard.tsx
import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

// Define query options
const usersQueryOptions = queryOptions({
  queryKey: ["users"],
  queryFn: fetchUsers,
  staleTime: 1000 * 60 * 5, // 5 minutes
});

// Prefetch in route loader
export const Route = createFileRoute("/dashboard")({
  loader: async ({ context }) => {
    // Prefetch users before rendering
    await context.queryClient.ensureQueryData(usersQueryOptions);
  },
  component: Dashboard,
});

function Dashboard() {
  // Data is already in cache from loader
  const { data: users } = useSuspenseQuery(usersQueryOptions);
  return <div>{/* Render users */}</div>;
}
```

#### Optimistic Updates
```typescript
// app/routes/users.tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function UserForm() {
  const queryClient = useQueryClient();

  const updateMutation = useMutation({
    mutationFn: updateUser,
    // Optimistic update (instant UI feedback)
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["users", newUser.id] });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(["users", newUser.id]);

      // Optimistically update cache
      queryClient.setQueryData(["users", newUser.id], newUser);

      return { previousUser };
    },
    // Rollback on error
    onError: (err, newUser, context) => {
      queryClient.setQueryData(["users", newUser.id], context?.previousUser);
    },
    // Refetch after mutation
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: ["users", variables.id] });
    },
  });

  return <form onSubmit={() => updateMutation.mutate(formData)} />;
}
```

#### Infinite Query for Large Datasets
```typescript
// app/routes/users.tsx
import { useInfiniteQuery } from "@tanstack/react-query";

function UserList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
    queryKey: ["users"],
    queryFn: ({ pageParam }) => fetchUsers({ cursor: pageParam, limit: 50 }),
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
    staleTime: 1000 * 60 * 5,
  });

  // Flatten pages
  const users = data?.pages.flatMap((page) => page.items) ?? [];

  return (
    <div>
      {users.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? "Loading..." : "Load More"}
        </button>
      )}
    </div>
  );
}
```

### Code Splitting and Lazy Loading

#### Route-Based Code Splitting
```typescript
// app/routes/index.tsx
import { createFileRoute } from "@tanstack/react-router";

// [OK] Automatic code splitting with TanStack Router
export const Route = createFileRoute("/dashboard")({
  component: Dashboard, // Automatically code-split
});

// Each route is a separate bundle
export const UsersRoute = createFileRoute("/users")({
  component: Users,
});
```

#### Component Lazy Loading
```typescript
// app/routes/dashboard.tsx
import { lazy, Suspense } from "react";

// [OK] Lazy load heavy components
const HeavyChart = lazy(() => import("~/components/HeavyChart"));
const LargeTable = lazy(() => import("~/components/LargeTable"));

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart data={chartData} />
      </Suspense>

      <Suspense fallback={<div>Loading table...</div>}>
        <LargeTable data={tableData} />
      </Suspense>
    </div>
  );
}
```

### Bundle Size Optimization

#### Analyze Bundle Size
```bash
# Build with analyzer
npm run build -- --analyze

# Check bundle size
ls -lh .output/public/_build/
```

#### Tree Shaking and Dead Code Elimination
```typescript
// [X] Bad - Imports entire library
import _ from "lodash";
const result = _.debounce(fn, 300);

// [OK] Good - Import only what you need
import debounce from "lodash/debounce";
const result = debounce(fn, 300);

// [X] Bad - Large date library
import moment from "moment";
const date = moment().format("YYYY-MM-DD");

// [OK] Good - Use native Date or smaller library
const date = new Date().toISOString().split("T")[0];

// OR use date-fns (tree-shakeable)
import { format } from "date-fns";
const date = format(new Date(), "yyyy-MM-dd");
```

#### Dynamic Imports for Heavy Libraries
```typescript
// app/routes/export.tsx
async function exportToExcel() {
  // [OK] Only load XLSX when needed
  const XLSX = await import("xlsx");
  const workbook = XLSX.utils.book_new();
  // ... generate Excel file
}

async function generatePDF() {
  // [OK] Only load jsPDF when needed
  const { jsPDF } = await import("jspdf");
  const doc = new jsPDF();
  // ... generate PDF
}
```

## Database Performance (PostgreSQL)

### N+1 Query Prevention

#### Select N+1 (Bad)
```python
# app/repositories/user_repository.py
from sqlmodel import Session, select
from app.models.user import User
from app.models.organization import Organization

# [X] Bad - N+1 query problem
async def get_users_with_orgs(db: Session) -> list[User]:
    # 1 query to fetch all users
    users = await db.execute(select(User))
    users = users.scalars().all()

    # N queries (one per user) to fetch organizations
    for user in users:
        org = await db.get(Organization, user.organization_id)  # N queries!
        user.organization = org

    return users
```

#### Eager Loading with Joins (Good)
```python
# [OK] Good - Single query with join
from sqlmodel import select
from sqlalchemy.orm import selectinload

async def get_users_with_orgs(db: Session) -> list[User]:
    # Single query with join
    statement = select(User).options(selectinload(User.organization))
    result = await db.execute(statement)
    users = result.scalars().all()
    return users
```

#### Relationship Loading Strategies
```python
# app/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    organization_id: str = Field(foreign_key="organization.id")

    # Lazy loading (default) - queries on access
    organization: Optional["Organization"] = Relationship(lazy="select")

    # Eager loading - always fetches related data
    organization: Optional["Organization"] = Relationship(lazy="joined")

# Usage with selectinload (recommended)
from sqlalchemy.orm import selectinload

statement = select(User).options(selectinload(User.organization))
```

### Query Optimization

#### Index Usage
```python
# app/db/migrations/add_indexes.py
from alembic import op
from sqlalchemy import Index

# [OK] Add index on frequently queried columns
op.create_index("idx_users_email", "users", ["email"])
op.create_index("idx_users_tenant_id", "users", ["tenant_id"])

# [OK] Composite index for multi-column queries
op.create_index("idx_users_tenant_email", "users", ["tenant_id", "email"])

# [OK] Partial index for filtered queries
op.execute("""
    CREATE INDEX idx_users_active
    ON users (tenant_id, created_at)
    WHERE is_active = true;
""")
```

#### Query Pagination
```python
# [X] Bad - Loads all records into memory
async def list_users(db: Session) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()  # Could be millions of rows!

# [OK] Good - Cursor-based pagination
async def list_users(
    db: Session,
    cursor: Optional[str] = None,
    limit: int = 100,
) -> dict:
    statement = select(User).limit(limit)

    if cursor:
        statement = statement.where(User.id > cursor)

    result = await db.execute(statement)
    users = result.scalars().all()

    next_cursor = users[-1].id if len(users) == limit else None

    return {
        "items": users,
        "next_cursor": next_cursor,
        "has_more": next_cursor is not None,
    }
```

#### Select Only Required Fields
```python
# [X] Bad - Fetches all columns (including large text fields)
async def list_users(db: Session) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()

# [OK] Good - Select only needed columns
from sqlalchemy import select

async def list_users(db: Session) -> list[dict]:
    statement = select(User.id, User.email, User.full_name)  # Only 3 columns
    result = await db.execute(statement)
    return [
        {"id": row.id, "email": row.email, "full_name": row.full_name}
        for row in result
    ]
```

### Connection Pooling

#### PostgreSQL Connection Pool (asyncpg)
```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Doppler provides DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# [OK] Configure connection pool
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL logging in production
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections when pool is full
    pool_timeout=30,  # Wait 30 seconds for available connection
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Check connection health before using
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    """Dependency for database sessions."""
    async with AsyncSessionLocal() as session:
        yield session
```

#### Connection Pool Monitoring
```python
# app/utils/db_monitor.py
from app.core.database import engine

async def check_pool_status():
    """Monitor connection pool health."""
    pool = engine.pool

    print(f"Pool size: {pool.size()}")
    print(f"Checked out connections: {pool.checkedout()}")
    print(f"Overflow: {pool.overflow()}")
    print(f"Total connections: {pool.size() + pool.overflow()}")
```

### Database Query Caching (Redis)

#### Cache Frequent Queries
```python
# app/repositories/user_repository.py
from upstash_redis import Redis
import json
import os

# Doppler provides REDIS_URL
redis = Redis.from_url(os.getenv("REDIS_URL"))

class UserRepository:
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    async def get_by_id(self, user_id: str) -> User | None:
        # Check Redis cache first
        cache_key = f"user:{self.tenant_id}:{user_id}"
        cached = redis.get(cache_key)

        if cached:
            # Cache hit - return from Redis
            return User(**json.loads(cached))

        # Cache miss - query database
        statement = select(User).where(
            User.id == user_id,
            User.tenant_id == self.tenant_id,
        )
        result = await self.db.execute(statement)
        user = result.scalar_one_or_none()

        if user:
            # Store in Redis (5 minute TTL)
            redis.setex(
                cache_key,
                300,  # 5 minutes
                json.dumps(user.model_dump()),
            )

        return user

    async def invalidate_cache(self, user_id: str):
        """Invalidate cache after update/delete."""
        cache_key = f"user:{self.tenant_id}:{user_id}"
        redis.delete(cache_key)
```

## Cloudflare Workers Performance

### Cloudflare Cache API

#### Cache Static Assets
```typescript
// app/entry.server.tsx
export async function handleFetch(request: Request, env: Env) {
  const url = new URL(request.url);

  // [OK] Cache static assets at edge
  if (url.pathname.startsWith("/assets/")) {
    const cache = caches.default;
    let response = await cache.match(request);

    if (!response) {
      response = await fetch(request);

      // Cache for 1 year (immutable assets)
      const headers = new Headers(response.headers);
      headers.set("Cache-Control", "public, max-age=31536000, immutable");

      response = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });

      await cache.put(request, response.clone());
    }

    return response;
  }

  // Handle dynamic requests
  return getLoadContext(request, env);
}
```

#### Cache API Responses
```typescript
// app/routes/api/users.ts
import { createServerFn } from "@tanstack/start";

export const listUsers = createServerFn({ method: "GET" }).handler(
  async ({ request, context }) => {
    const cache = caches.default;
    const cacheKey = new Request(request.url);

    // Check cache
    let response = await cache.match(cacheKey);
    if (response) {
      return response; // Cache hit
    }

    // Fetch from database
    const users = await db.select().from(usersTable);

    // Create response with cache headers
    response = new Response(JSON.stringify(users), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300", // 5 minutes
      },
    });

    // Store in edge cache
    await cache.put(cacheKey, response.clone());

    return response;
  }
);
```

### Workers KV for Session Storage

#### Session Caching
```typescript
// app/utils/session.server.ts
export async function getSession(
  sessionId: string,
  env: Env
): Promise<Session | null> {
  // [OK] Fast read from KV (edge cache)
  const cached = await env.SESSIONS.get(sessionId, "json");

  if (cached) {
    return cached as Session;
  }

  // Fallback to database
  const session = await db.query.sessionsTable.findFirst({
    where: eq(sessionsTable.id, sessionId),
  });

  if (session) {
    // Cache in KV for 1 hour
    await env.SESSIONS.put(sessionId, JSON.stringify(session), {
      expirationTtl: 3600,
    });
  }

  return session;
}
```

### Durable Objects for Stateful Operations

#### Rate Limiting with Durable Objects
```typescript
// app/durable-objects/RateLimiter.ts
export class RateLimiter {
  state: DurableObjectState;
  requests: Map<string, number[]>;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.requests = new Map();
  }

  async fetch(request: Request) {
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const now = Date.now();
    const windowMs = 60000; // 1 minute
    const maxRequests = 100;

    // Get request timestamps for this IP
    const timestamps = this.requests.get(ip) || [];

    // Filter timestamps within window
    const recent = timestamps.filter((t) => now - t < windowMs);

    // Check rate limit
    if (recent.length >= maxRequests) {
      return new Response("Rate limit exceeded", { status: 429 });
    }

    // Add current request
    recent.push(now);
    this.requests.set(ip, recent);

    return new Response("OK", { status: 200 });
  }
}
```

## Image Optimization

### Cloudflare Images

#### Image Resizing
```typescript
// app/routes/api/images.ts
export async function GET({ request, context }: { request: Request; context: any }) {
  const url = new URL(request.url);
  const imageUrl = url.searchParams.get("url");
  const width = url.searchParams.get("width") || "800";
  const quality = url.searchParams.get("quality") || "85";

  // [OK] Use Cloudflare Image Resizing
  const resizedUrl = `https://imagedelivery.net/${context.env.CLOUDFLARE_ACCOUNT_ID}/${imageUrl}/width=${width},quality=${quality}`;

  return fetch(resizedUrl);
}
```

#### Lazy Loading Images
```typescript
// app/components/LazyImage.tsx
import { useState, useEffect, useRef } from "react";

export function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setIsLoaded(true);
          observer.disconnect();
        }
      });
    });

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <img
      ref={imgRef}
      src={isLoaded ? src : "data:image/gif;base64,R0lGODlhAQABAAAAACw="}
      alt={alt}
      loading="lazy"
      decoding="async"
    />
  );
}
```

## Performance Monitoring

### Web Vitals Tracking

#### Measure Core Web Vitals
```typescript
// app/utils/web-vitals.ts
import { onCLS, onFID, onLCP, onTTFB } from "web-vitals";

export function trackWebVitals() {
  onCLS((metric) => {
    console.log("CLS:", metric.value);
    sendToAnalytics("CLS", metric.value);
  });

  onFID((metric) => {
    console.log("FID:", metric.value);
    sendToAnalytics("FID", metric.value);
  });

  onLCP((metric) => {
    console.log("LCP:", metric.value);
    sendToAnalytics("LCP", metric.value);
  });

  onTTFB((metric) => {
    console.log("TTFB:", metric.value);
    sendToAnalytics("TTFB", metric.value);
  });
}

async function sendToAnalytics(metric: string, value: number) {
  // Send to Axiom or other analytics
  await fetch("/api/analytics", {
    method: "POST",
    body: JSON.stringify({ metric, value }),
  });
}
```

#### React DevTools Profiler
```typescript
// app/routes/dashboard.tsx
import { Profiler, ProfilerOnRenderCallback } from "react";

const onRender: ProfilerOnRenderCallback = (
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) => {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
};

function Dashboard() {
  return (
    <Profiler id="Dashboard" onRender={onRender}>
      {/* Dashboard content */}
    </Profiler>
  );
}
```

### Database Query Performance

#### Log Slow Queries
```python
# app/core/database.py
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logger = logging.getLogger(__name__)

# Log queries taking > 100ms
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop()
    if total > 0.1:  # 100ms threshold
        logger.warning(f"Slow query ({total:.2f}s): {statement}")
```

## Performance Benchmarking

### pytest Benchmark
```python
# tests/benchmarks/test_user_repository.py
import pytest
from app.repositories.user_repository import UserRepository

@pytest.mark.benchmark
def test_list_users_performance(benchmark, db_session, tenant_id):
    """Benchmark user listing performance."""
    repository = UserRepository(db_session, tenant_id=tenant_id)

    # Run benchmark
    result = benchmark(repository.list, skip=0, limit=100)

    # Assert performance
    assert len(result) <= 100
    assert benchmark.stats["mean"] < 0.1  # Average < 100ms
```

**Run benchmarks with Doppler**:
```bash
doppler run --config test -- pytest tests/benchmarks/ --benchmark-only
```

## When to Apply This Skill

Use this performance optimization skill when:
- Frontend rendering feels sluggish or components re-render unnecessarily
- TanStack Query refetches data too frequently
- Database queries are slow (N+1 problems, missing indexes)
- Bundle size exceeds 500KB (analyze with `npm run build -- --analyze`)
- Cloudflare Workers timeout or CPU time is high
- Connection pool is exhausted (monitor with pool status checks)
- Images load slowly (use lazy loading, Cloudflare Images)
- Web Vitals scores are poor (LCP > 2.5s, CLS > 0.1, FID > 100ms)
- API responses are slow (add caching, optimize queries)
- Performance regressions detected in benchmarks

## Template References

These performance patterns come from Grey Haven's actual templates:
- **Frontend**: `cvi-template` (TanStack Start + React 19 + Query)
- **Backend**: `cvi-backend-template` (FastAPI + SQLModel + connection pooling)
- **Cloudflare**: Wrangler configuration with KV/R2/DO bindings

## Critical Reminders

1. **useMemo/useCallback** - Memoize expensive calculations and functions
2. **React.memo** - Prevent unnecessary component re-renders
3. **TanStack Query staleTime** - Configure appropriate cache duration (5+ minutes)
4. **Query prefetching** - Prefetch data in route loaders
5. **N+1 prevention** - Use selectinload() for relationships
6. **Database indexes** - Index tenant_id, email, frequently queried columns
7. **Connection pooling** - Configure pool size, max overflow, timeouts
8. **Cloudflare Cache API** - Cache static assets and API responses at edge
9. **Code splitting** - Lazy load heavy components and libraries
10. **Bundle size** - Analyze with `npm run build -- --analyze`, tree-shake imports
11. **Web Vitals** - Monitor LCP, CLS, FID, TTFB with web-vitals library
12. **Benchmarking** - Run pytest benchmarks with `--benchmark-only`
