# Cloudflare Workers Platform Guide

Comprehensive guide for deploying, monitoring, and troubleshooting Cloudflare Workers in Grey Haven's stack.

## Workers Architecture

**Execution Model**:
- V8 isolates (not containers)
- Deployed globally to 300+ datacenters
- Request routed to nearest location
- Cold start: ~1-5ms (vs 100-1000ms for containers)
- CPU time limit: 50ms (Free), 50ms-30s (Paid)

**Resource Limits**:
```
Free Plan:
- Bundle size: 1MB compressed
- CPU time: 50ms per request
- Requests: 100,000/day
- KV reads: 100,000/day

Paid Plan ($5/month):
- Bundle size: 10MB compressed
- CPU time: 50ms (standard), up to 30s (unbound)
- Requests: 10M included, $0.50/million after
- KV reads: 10M included
```

---

## Deployment Best Practices

### Bundle Optimization

**Size Reduction Strategies**:
```typescript
// 1. Tree shaking with named imports
import { uniq } from 'lodash-es';  // ✅ Only imports uniq
import _ from 'lodash';             // ❌ Imports entire library

// 2. Use native APIs instead of libraries
const date = new Date().toISOString();  // ✅ Native
import moment from 'moment';             // ❌ 300KB library

// 3. External API calls instead of SDKs
await fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: { 'x-api-key': env.API_KEY },
  body: JSON.stringify({ ... })
});  // ✅ 0KB vs @anthropic-ai/sdk (2.1MB)

// 4. Code splitting with dynamic imports
if (request.url.includes('/special')) {
  const { handler } = await import('./expensive-module');
  return handler(request);
}  // ✅ Lazy load
```

**webpack Configuration**:
```javascript
module.exports = {
  mode: 'production',
  target: 'webworker',
  optimization: {
    minimize: true,
    usedExports: true,  // Tree shaking
    sideEffects: false
  },
  resolve: {
    alias: {
      'lodash': 'lodash-es'  // Use ES modules version
    }
  }
};
```

---

### Environment Variables

**Using Secrets**:
```bash
# Add secret (never in code)
wrangler secret put DATABASE_URL

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete OLD_KEY
```

**Using Variables** (wrangler.toml):
```toml
[vars]
API_ENDPOINT = "https://api.partner.com"
MAX_RETRIES = "3"
CACHE_TTL = "300"

[env.staging.vars]
API_ENDPOINT = "https://staging-api.partner.com"

[env.production.vars]
API_ENDPOINT = "https://api.partner.com"
```

**Accessing in Code**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    const dbUrl = env.DATABASE_URL;  // Secret
    const endpoint = env.API_ENDPOINT;  // Var
    const maxRetries = parseInt(env.MAX_RETRIES);

    return new Response('OK');
  }
};
```

---

## Performance Optimization

### CPU Time Management

**Avoid CPU-Intensive Operations**:
```typescript
// ❌ BAD: CPU-intensive operation
function processLargeDataset(data) {
  const sorted = data.sort((a, b) => a.value - b.value);
  const filtered = sorted.filter(item => item.value > 1000);
  const mapped = filtered.map(item => ({ ...item, processed: true }));
  return mapped;  // Can exceed 50ms CPU limit
}

// ✅ GOOD: Offload to external service
async function processLargeDataset(data, env) {
  const response = await fetch(`${env.PROCESSING_API}/process`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return response.json();  // External service handles heavy lifting
}

// ✅ BETTER: Use Durable Objects for stateful computation
const id = env.PROCESSOR.idFromName('processor');
const stub = env.PROCESSOR.get(id);
return stub.fetch(request);  // Durable Object has more CPU time
```

**Monitor CPU Usage**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    const start = Date.now();

    try {
      const response = await handleRequest(request, env);
      const duration = Date.now() - start;

      if (duration > 40) {
        console.warn(`CPU time approaching limit: ${duration}ms`);
      }

      return response;
    } catch (error) {
      const duration = Date.now() - start;
      console.error(`Request failed after ${duration}ms:`, error);
      throw error;
    }
  }
};
```

---

### Caching Strategies

**Cache API**:
```typescript
export default {
  async fetch(request: Request) {
    const cache = caches.default;

    // Check cache
    let response = await cache.match(request);
    if (response) return response;

    // Cache miss - fetch and cache
    response = await fetch(request);

    // Cache for 5 minutes
    const cacheResponse = new Response(response.body, response);
    cacheResponse.headers.set('Cache-Control', 'max-age=300');
    await cache.put(request, cacheResponse.clone());

    return response;
  }
};
```

**KV for Data Caching**:
```typescript
export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    const cacheKey = `data:${url.pathname}`;

    // Check KV
    const cached = await env.CACHE.get(cacheKey, 'json');
    if (cached) return Response.json(cached);

    // Fetch data
    const data = await fetchExpensiveData();

    // Store in KV with 5min TTL
    await env.CACHE.put(cacheKey, JSON.stringify(data), {
      expirationTtl: 300
    });

    return Response.json(data);
  }
};
```

---

## Common Errors and Solutions

### Error 1101: Worker Threw Exception

**Cause**: Unhandled JavaScript exception

**Example**:
```typescript
// ❌ BAD: Unhandled error
export default {
  async fetch(request: Request) {
    const data = JSON.parse(request.body);  // Throws if invalid JSON
    return Response.json(data);
  }
};
```

**Solution**:
```typescript
// ✅ GOOD: Proper error handling
export default {
  async fetch(request: Request) {
    try {
      const body = await request.text();
      const data = JSON.parse(body);
      return Response.json(data);
    } catch (error) {
      console.error('JSON parse error:', error);
      return new Response('Invalid JSON', { status: 400 });
    }
  }
};
```

---

### Error 1015: Rate Limited

**Cause**: Too many requests to origin

**Solution**: Implement caching and rate limiting
```typescript
const RATE_LIMIT = 100;  // requests per minute
const rateLimits = new Map();

export default {
  async fetch(request: Request) {
    const ip = request.headers.get('CF-Connecting-IP');
    const key = `ratelimit:${ip}`;

    const count = rateLimits.get(key) || 0;
    if (count >= RATE_LIMIT) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    rateLimits.set(key, count + 1);
    setTimeout(() => rateLimits.delete(key), 60000);

    return new Response('OK');
  }
};
```

---

### Error: Script Exceeds Size Limit

**Diagnosis**:
```bash
# Check bundle size
npm run build
ls -lh dist/worker.js

# Analyze bundle
npm install --save-dev webpack-bundle-analyzer
npm run build -- --analyze
```

**Solutions**: See [bundle optimization](#bundle-optimization) above

---

## Monitoring and Logging

### Structured Logging

```typescript
interface LogEntry {
  level: 'info' | 'warn' | 'error';
  message: string;
  timestamp: string;
  requestId?: string;
  duration?: number;
  metadata?: Record<string, any>;
}

function log(entry: LogEntry) {
  console.log(JSON.stringify({
    ...entry,
    timestamp: new Date().toISOString()
  }));
}

export default {
  async fetch(request: Request, env: Env) {
    const requestId = crypto.randomUUID();
    const start = Date.now();

    try {
      log({
        level: 'info',
        message: 'Request started',
        requestId,
        metadata: {
          method: request.method,
          url: request.url
        }
      });

      const response = await handleRequest(request, env);

      log({
        level: 'info',
        message: 'Request completed',
        requestId,
        duration: Date.now() - start,
        metadata: {
          status: response.status
        }
      });

      return response;
    } catch (error) {
      log({
        level: 'error',
        message: 'Request failed',
        requestId,
        duration: Date.now() - start,
        metadata: {
          error: error.message,
          stack: error.stack
        }
      });

      return new Response('Internal Server Error', { status: 500 });
    }
  }
};
```

---

### Health Check Endpoint

```typescript
export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);

    if (url.pathname === '/health') {
      return Response.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: env.VERSION || 'unknown'
      });
    }

    // Regular request handling
    return handleRequest(request, env);
  }
};
```

---

## Testing Workers

```bash
# Local testing
wrangler dev
curl http://localhost:8787/api/users
curl -X POST http://localhost:8787/api/users -H "Content-Type: application/json" -d '{"name": "Test User"}'

# Unit testing (Vitest)
import { describe, it, expect } from 'vitest';
import worker from './worker';

describe('Worker', () => {
  it('returns 200 for health check', async () => {
    const request = new Request('https://example.com/health');
    const response = await worker.fetch(request, getMockEnv());
    expect(response.status).toBe(200);
  });
});
```

---

## Security Best Practices

```typescript
// 1. Validate inputs
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// 2. Set security headers
function addSecurityHeaders(response: Response): Response {
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Strict-Transport-Security', 'max-age=31536000');
  return response;
}

// 3. CORS configuration
const ALLOWED_ORIGINS = ['https://app.greyhaven.io', 'https://staging.greyhaven.io'];
function handleCors(request: Request): Response | null {
  const origin = request.headers.get('Origin');
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE',
        'Access-Control-Max-Age': '86400'
      }
    });
  }
  if (origin && !ALLOWED_ORIGINS.includes(origin)) {
    return new Response('Forbidden', { status: 403 });
  }
  return null;
}
```

---

## Related Documentation

- **Runbooks**: [troubleshooting-runbooks.md](troubleshooting-runbooks.md) - Step-by-step procedures
- **Commands**: [diagnostic-commands.md](diagnostic-commands.md) - Command reference
- **Examples**: [Examples Index](../examples/INDEX.md) - Full examples

---

Return to [reference index](INDEX.md)
