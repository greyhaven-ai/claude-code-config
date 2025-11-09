# Distributed System Network Debugging

Investigating intermittent 504 Gateway Timeout errors between Cloudflare Workers and external APIs, resolved through DNS caching and timeout tuning.

## Overview

**Incident**: 5% of API requests failing with 504 timeouts
**Impact**: Intermittent failures, no clear pattern, user frustration
**Root Cause**: DNS resolution delays + worker timeout too aggressive
**Resolution**: DNS caching + timeout increase (5s→30s)
**Status**: Resolved

## Incident Timeline

| Time | Event | Action |
|------|-------|--------|
| 14:00 | 504 errors detected | Alerts triggered |
| 14:10 | Pattern analysis started | Check logs, no obvious cause |
| 14:30 | Network trace performed | Found DNS delays |
| 14:50 | Root cause identified | DNS + timeout combination |
| 15:10 | Fix deployed | DNS caching + timeout tuning |
| 15:40 | Monitoring confirmed | 504s eliminated |

---

## Symptoms and Detection

### Initial Alerts

**Error Pattern**:
```
[ERROR] Request to https://api.partner.com/data failed: 504 Gateway Timeout
[ERROR] Upstream timeout after 5000ms
[ERROR] DNS lookup took 3200ms (80% of timeout!)
```

**Characteristics**:
- ❌ Random occurrence (5% of requests)
- ❌ No pattern by time of day
- ❌ Affects all worker regions equally
- ❌ External API reports no issues
- ✅ Only affects specific external endpoints

---

## Diagnosis

### Step 1: Network Request Breakdown

**curl Timing Analysis**:
```bash
# Test external API with detailed timing
curl -w "\nDNS:     %{time_namelookup}s\nConnect: %{time_connect}s\nTLS:     %{time_appconnect}s\nStart:   %{time_starttransfer}s\nTotal:   %{time_total}s\n" \
  -o /dev/null -s https://api.partner.com/data

# Results (intermittent):
DNS:     3.201s  # ❌ Very slow!
Connect: 3.450s
TLS:     3.780s
Start:   4.120s
Total:   4.823s  # Close to 5s worker timeout
```

**Fast vs Slow Requests**:
```
FAST (95% of requests):
DNS: 0.050s → Connect: 0.120s → Total: 0.850s ✅

SLOW (5% of requests):
DNS: 3.200s → Connect: 3.450s → Total: 4.850s ❌ (near timeout)
```

**Root Cause**: DNS resolution delays causing total request time to exceed worker timeout.

---

### Step 2: DNS Investigation

**nslookup Testing**:
```bash
# Test DNS resolution
time nslookup api.partner.com

# Results (vary):
Run 1: 0.05s  ✅
Run 2: 3.10s  ❌
Run 3: 0.04s  ✅
Run 4: 2.95s  ❌

Pattern: DNS cache miss causes 3s delay
```

**dig Analysis**:
```bash
# Detailed DNS query
dig api.partner.com +stats

# Results:
;; Query time: 3021 msec          # Slow!
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Thu Dec 05 14:25:32 UTC 2024
;; MSG SIZE  rcvd: 84

# Root cause: No DNS caching in worker
```

---

### Step 3: Worker Timeout Configuration

**Current Worker Code**:
```typescript
// worker.ts (BEFORE - Too aggressive timeout)
export default {
  async fetch(request: Request, env: Env) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000); // 5s timeout

    try {
      const response = await fetch('https://api.partner.com/data', {
        signal: controller.signal
      });
      return response;
    } catch (error) {
      // 5% of requests timeout here
      return new Response('Gateway Timeout', { status: 504 });
    } finally {
      clearTimeout(timeout);
    }
  }
};
```

**Problem**: 5s timeout doesn't account for DNS delays (up to 3s).

---

### Step 4: CORS and Headers Check

**Test CORS Headers**:
```bash
# Check CORS preflight
curl -I -X OPTIONS https://api.greyhaven.io/proxy \
  -H "Origin: https://app.greyhaven.io" \
  -H "Access-Control-Request-Method: POST"

# Response:
HTTP/2 200
access-control-allow-origin: https://app.greyhaven.io ✅
access-control-allow-methods: GET, POST, PUT, DELETE ✅
access-control-max-age: 86400 ✅
```

**No CORS issues** - problem isolated to DNS + timeout.

---

## Resolution

### Fix 1: Implement DNS Caching

**Worker with DNS Cache**:
```typescript
// worker.ts (AFTER - With DNS caching)
interface DnsCache {
  ip: string;
  timestamp: number;
  ttl: number;
}

const DNS_CACHE = new Map<string, DnsCache>();
const DNS_TTL = 60 * 1000; // 60 seconds

async function resolveWithCache(hostname: string): Promise<string> {
  const cached = DNS_CACHE.get(hostname);

  if (cached && Date.now() - cached.timestamp < cached.ttl) {
    // Cache hit - return immediately
    return cached.ip;
  }

  // Cache miss - resolve DNS
  const dnsResponse = await fetch(`https://1.1.1.1/dns-query?name=${hostname}`, {
    headers: { 'accept': 'application/dns-json' }
  });
  const dnsData = await dnsResponse.json();
  const ip = dnsData.Answer[0].data;

  // Update cache
  DNS_CACHE.set(hostname, {
    ip,
    timestamp: Date.now(),
    ttl: DNS_TTL
  });

  return ip;
}

export default {
  async fetch(request: Request, env: Env) {
    // Pre-resolve DNS (cached)
    const ip = await resolveWithCache('api.partner.com');

    // Use IP directly (bypass DNS)
    const response = await fetch(`https://${ip}/data`, {
      headers: {
        'Host': 'api.partner.com' // Required for SNI
      }
    });

    return response;
  }
};
```

**Result**: DNS resolution <5ms (cache hit) vs 3000ms (cache miss).

---

### Fix 2: Increase Worker Timeout

**Updated Timeout**:
```typescript
// worker.ts - Increased timeout to account for DNS
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 30000); // 30s timeout

try {
  const response = await fetch('https://api.partner.com/data', {
    signal: controller.signal
  });
  return response;
} finally {
  clearTimeout(timeout);
}
```

**Timeout Breakdown**:
```
Old: 5s total
- DNS: 3s (worst case)
- Connect: 1s
- Request: 1s
= Frequent timeouts

New: 30s total
- DNS: <0.01s (cached)
- Connect: 1s
- Request: 2s
- Buffer: 27s (ample)
= No timeouts
```

---

### Fix 3: Add Retry Logic with Exponential Backoff

**Retry Implementation**:
```typescript
// utils/retry.ts
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries: number = 3
): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(url, options);

      // Retry on 5xx errors
      if (response.status >= 500 && attempt < maxRetries - 1) {
        const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      return response;
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      // Exponential backoff: 1s, 2s, 4s
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Max retries exceeded');
}

// Usage:
const response = await fetchWithRetry('https://api.partner.com/data', {
  signal: controller.signal
});
```

---

### Fix 4: Circuit Breaker Pattern

**Prevent Cascading Failures**:
```typescript
// utils/circuit-breaker.ts
class CircuitBreaker {
  private failures: number = 0;
  private lastFailureTime: number = 0;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      // Check if enough time passed to try again
      if (Date.now() - this.lastFailureTime > 60000) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();

    if (this.failures >= 5) {
      this.state = 'OPEN'; // Trip circuit after 5 failures
    }
  }
}

// Usage:
const breaker = new CircuitBreaker();
const response = await breaker.execute(() =>
  fetch('https://api.partner.com/data')
);
```

---

## Results

### Before vs After Metrics

| Metric | Before Fix | After Fix | Improvement |
|--------|-----------|-----------|-------------|
| **504 Error Rate** | 5% | 0.01% | **99.8% reduction** |
| **DNS Resolution** | 3000ms (worst) | <5ms (cached) | **99.8% faster** |
| **Total Request Time** | 4800ms (p95) | 850ms (p95) | **82% faster** |
| **Timeout Threshold** | 5s (too low) | 30s (appropriate) | +500% headroom |

---

### Network Diagnostics

**traceroute Analysis**:
```bash
# Check network path to external API
traceroute api.partner.com

# Results show no packet loss
 1  gateway (10.0.0.1)  1.234 ms
 2  isp-router (100.64.0.1)  5.678 ms
...
15  api.partner.com (203.0.113.42)  45.234 ms
```

**No packet loss** - confirms DNS was the issue, not network.

---

## Prevention Measures

### 1. Network Monitoring Dashboard

**Metrics to Track**:
```typescript
// Track network timing metrics
const network_dns_duration = new Histogram({
  name: 'network_dns_duration_seconds',
  help: 'DNS resolution time'
});

const network_connect_duration = new Histogram({
  name: 'network_connect_duration_seconds',
  help: 'TCP connection time'
});

const network_total_duration = new Histogram({
  name: 'network_total_duration_seconds',
  help: 'Total request time'
});
```

### 2. Alert Rules

```yaml
# Alert on high DNS resolution time
- alert: SlowDnsResolution
  expr: histogram_quantile(0.95, network_dns_duration_seconds) > 1
  for: 5m
  annotations:
    summary: "DNS resolution p95 >1s"

# Alert on gateway timeouts
- alert: HighGatewayTimeouts
  expr: rate(http_requests_total{status="504"}[5m]) > 0.01
  for: 5m
  annotations:
    summary: "504 error rate >1%"
```

### 3. Health Check Endpoints

```typescript
@app.get("/health/network")
async function networkHealth() {
  const checks = await Promise.all([
    checkDns('api.partner.com'),
    checkConnectivity('https://api.partner.com/health'),
    checkLatency('https://api.partner.com/ping')
  ]);

  return {
    status: checks.every(c => c.healthy) ? 'healthy' : 'degraded',
    checks
  };
}
```

---

## Lessons Learned

### What Went Well

✅ Detailed network timing analysis pinpointed DNS
✅ DNS caching eliminated 99.8% of timeouts
✅ Circuit breaker prevents cascading failures

### What Could Be Improved

❌ No DNS monitoring before incident
❌ Timeout too aggressive without considering DNS
❌ No retry logic for transient failures

### Key Takeaways

1. **Always cache DNS** in workers (60s TTL minimum)
2. **Account for DNS time** when setting timeouts
3. **Add retry logic** with exponential backoff
4. **Implement circuit breakers** for external dependencies
5. **Monitor network timing** (DNS, connect, TLS, transfer)

---

## Related Documentation

- **Worker Deployment**: [cloudflare-worker-deployment-failure.md](cloudflare-worker-deployment-failure.md)
- **Database Issues**: [planetscale-connection-issues.md](planetscale-connection-issues.md)
- **Performance**: [performance-degradation-analysis.md](performance-degradation-analysis.md)
- **Runbooks**: [../reference/troubleshooting-runbooks.md](../reference/troubleshooting-runbooks.md)

---

Return to [examples index](INDEX.md)
