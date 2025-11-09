# Troubleshooting Runbooks

Step-by-step runbooks for resolving common Grey Haven infrastructure issues. Follow procedures systematically for fastest resolution.

## Runbook 1: Worker Not Responding

### Symptoms
- API returning 500/502/503 errors
- Workers timing out or not processing requests
- Cloudflare error pages showing

### Diagnosis Steps

**1. Check Cloudflare Status**
```bash
# Visit: https://www.cloudflarestatus.com
# Or query status API
curl -s https://www.cloudflarestatus.com/api/v2/status.json | jq '.status.indicator'
```

**2. View Worker Logs**
```bash
# Real-time logs
wrangler tail --format pretty

# Look for errors:
# - "Script exceeded CPU time limit"
# - "Worker threw exception"
# - "Uncaught TypeError"
```

**3. Check Recent Deployments**
```bash
wrangler deployments list

# If recent deployment suspicious, rollback:
wrangler rollback --message "Reverting to stable version"
```

**4. Test Worker Locally**
```bash
# Run worker in dev mode
wrangler dev

# Test endpoint
curl http://localhost:8787/api/health
```

### Resolution Paths

**Path A: Platform Issue** - Wait for Cloudflare, monitor status, communicate ETA
**Path B: Code Error** - Rollback deployment, fix in dev, test before redeploy
**Path C: Resource Limit** - Check CPU logs, optimize operations, upgrade if needed
**Path D: Binding Issue** - Verify wrangler.toml, check bindings, redeploy

### Prevention
- Health check endpoint: `GET /health`
- Monitor error rate with alerts (>1% = alert)
- Test deployments in staging first
- Implement circuit breakers for external calls

---

## Runbook 2: Database Connection Failures

### Symptoms
- "connection refused" errors
- "too many connections" errors
- Application timing out on database queries
- 503 errors from API

### Diagnosis Steps

**1. Test Database Connection**
```bash
# Direct connection test
pscale shell greyhaven-db main

# If fails, check:
# - Database status
# - Credentials
# - Network connectivity
```

**2. Check Connection Pool**
```bash
# Query pool status
curl http://localhost:8000/pool-status

# Expected healthy response:
{
  "size": 50,
  "checked_out": 25,  # <80% is healthy
  "overflow": 0,
  "available": 25
}
```

**3. Check Active Connections**
```sql
-- In pscale shell
SELECT
  COUNT(*) as active,
  MAX(query_start) as oldest_query
FROM pg_stat_activity
WHERE state = 'active';

-- If active = pool size, pool exhausted
-- If oldest_query >10min, leaked connection
```

**4. Review Application Logs**
```bash
# Search for connection errors
grep -i "connection" logs/app.log | tail -50

# Common errors:
# - "Pool timeout"
# - "Connection refused"
# - "Max connections reached"
```

### Resolution Paths

**Path A: Invalid Credentials**
```bash
# Rotate credentials
pscale password create greyhaven-db main app-password

# Update environment variable
# Restart application
```

**Path B: Pool Exhausted**
```python
# Increase pool size in database.py
engine = create_engine(
    database_url,
    pool_size=50,      # Increase from 20
    max_overflow=20
)
```

**Path C: Connection Leaks**
```python
# Fix: Use context managers
with Session(engine) as session:
    # Work with session
    pass  # Automatically closed
```

**Path D: Database Paused/Down**
```bash
# Resume database if paused
pscale database resume greyhaven-db

# Check database status
pscale database show greyhaven-db
```

### Prevention
- Use connection pooling with proper limits
- Implement retry logic with exponential backoff
- Monitor pool utilization (alert >80%)
- Test for connection leaks in CI/CD

---

## Runbook 3: Deployment Failures

### Symptoms
- `wrangler deploy` fails
- CI/CD pipeline fails at deployment step
- New code not reflecting in production

### Diagnosis Steps

**1. Check Deployment Error**
```bash
wrangler deploy --verbose

# Common errors:
# - "Script exceeds size limit"
# - "Syntax error in worker"
# - "Environment variable missing"
# - "Binding not found"
```

**2. Verify Build Output**
```bash
# Check built file
ls -lh dist/
npm run build

# Ensure build succeeds locally
```

**3. Check Environment Variables**
```bash
# List secrets
wrangler secret list

# Verify wrangler.toml vars
cat wrangler.toml | grep -A 10 "\[vars\]"
```

**4. Test Locally**
```bash
# Start dev server
wrangler dev

# If works locally but not production:
# - Environment variable mismatch
# - Binding configuration issue
```

### Resolution Paths

**Path A: Bundle Too Large**
```bash
# Check bundle size
ls -lh dist/worker.js

# Solutions:
# - Tree shake unused code
# - Code split large modules
# - Use fetch instead of SDK
```

**Path B: Syntax Error**
```bash
# Run TypeScript check
npm run type-check

# Run linter
npm run lint

# Fix errors before deploying
```

**Path C: Missing Variables**
```bash
# Add missing secret
wrangler secret put API_KEY

# Or add to wrangler.toml vars
[vars]
API_ENDPOINT = "https://api.example.com"
```

**Path D: Binding Not Found**
```toml
# wrangler.toml - Add binding
[[kv_namespaces]]
binding = "CACHE"
id = "abc123"

[[d1_databases]]
binding = "DB"
database_name = "greyhaven-db"
database_id = "xyz789"
```

### Prevention
- Bundle size check in CI/CD
- Pre-commit hooks for validation
- Staging environment for testing
- Automated deployment tests

---

## Runbook 4: Performance Degradation

### Symptoms
- API response times increased (>2x normal)
- Slow page loads
- User complaints about slowness
- Timeout errors

### Diagnosis Steps

**1. Check Current Latency**
```bash
# Test endpoint
curl -w "\nTotal: %{time_total}s\n" -o /dev/null -s https://api.greyhaven.io/orders

# p95 should be <500ms
# If >1s, investigate
```

**2. Analyze Worker Logs**
```bash
wrangler tail --format json | jq '{duration: .outcome.duration, event: .event}'

# Identify slow requests
# Check what's taking time
```

**3. Check Database Queries**
```bash
# Slow query log
pscale database insights greyhaven-db main --slow-queries

# Look for:
# - N+1 queries (many small queries)
# - Missing indexes (full table scans)
# - Long-running queries (>100ms)
```

**4. Profile Application**
```bash
# Add timing middleware
# Log slow operations
# Identify bottleneck (DB, API, compute)
```

### Resolution Paths

**Path A: N+1 Queries**
```python
# Use eager loading
statement = (
    select(Order)
    .options(selectinload(Order.items))
)
```

**Path B: Missing Indexes**
```sql
-- Add indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_items_order_id ON order_items(order_id);
```

**Path C: No Caching**
```typescript
// Add Redis caching
const cached = await redis.get(cacheKey);
if (cached) return cached;

const result = await expensiveOperation();
await redis.setex(cacheKey, 300, result);
```

**Path D: Worker CPU Limit**
```typescript
// Optimize expensive operations
// Use async operations
// Offload to external service
```

### Prevention
- Monitor p95 latency (alert >500ms)
- Test for N+1 queries in CI/CD
- Add indexes for foreign keys
- Implement caching layer
- Performance budgets in tests

---

## Runbook 5: Network Connectivity Issues

### Symptoms
- Intermittent failures
- DNS resolution errors
- Connection timeouts
- CORS errors

### Diagnosis Steps

**1. Test DNS Resolution**
```bash
# Check DNS
nslookup api.partner.com
dig api.partner.com

# Measure DNS time
time nslookup api.partner.com

# If >1s, DNS is slow
```

**2. Test Connectivity**
```bash
# Basic connectivity
ping api.partner.com

# Trace route
traceroute api.partner.com

# Full timing breakdown
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTotal: %{time_total}s\n" \
  -o /dev/null -s https://api.partner.com
```

**3. Check CORS**
```bash
# Preflight request
curl -I -X OPTIONS https://api.greyhaven.io/api/users \
  -H "Origin: https://app.greyhaven.io" \
  -H "Access-Control-Request-Method: POST"

# Verify headers:
# - Access-Control-Allow-Origin
# - Access-Control-Allow-Methods
```

**4. Check Firewall/Security**
```bash
# Test from different location
# Check IP whitelist
# Verify SSL certificate
```

### Resolution Paths

**Path A: Slow DNS**
```typescript
// Implement DNS caching
const DNS_CACHE = new Map();
// Cache DNS for 60s
```

**Path B: Connection Timeout**
```typescript
// Increase timeout
const controller = new AbortController();
setTimeout(() => controller.abort(), 30000); // 30s
```

**Path C: CORS Error**
```typescript
// Add CORS headers
response.headers.set('Access-Control-Allow-Origin', origin);
response.headers.set('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE');
```

**Path D: SSL/TLS Issue**
```bash
# Check certificate
openssl s_client -connect api.partner.com:443

# Verify not expired
# Check certificate chain
```

### Prevention
- DNS caching (60s TTL)
- Appropriate timeouts (30s for external APIs)
- Health checks for external dependencies
- Circuit breakers for failures
- Monitor external API latency

---

## Emergency Procedures (SEV1)

**Immediate Actions**:
1. **Assess**: Users affected? Functionality broken? Data loss risk?
2. **Communicate**: Alert team, update status page
3. **Stop Bleeding**: `wrangler rollback` or disable feature
4. **Diagnose**: Logs, recent changes, metrics
5. **Fix**: Hotfix or workaround, test first
6. **Verify**: Monitor metrics, test functionality
7. **Postmortem**: Document, root cause, prevention

---

## Escalation Matrix

| Issue Type | First Response | Escalate To | Escalation Trigger |
|------------|---------------|-------------|-------------------|
| Worker errors | DevOps troubleshooter | incident-responder | SEV1/SEV2 |
| Performance | DevOps troubleshooter | performance-optimizer | >30min unresolved |
| Database | DevOps troubleshooter | data-validator | Schema issues |
| Security | DevOps troubleshooter | security-analyzer | Breach suspected |
| Application bugs | DevOps troubleshooter | smart-debug | Infrastructure ruled out |

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Full troubleshooting examples
- **Diagnostic Commands**: [diagnostic-commands.md](diagnostic-commands.md) - Command reference
- **Cloudflare Guide**: [cloudflare-workers-guide.md](cloudflare-workers-guide.md) - Platform-specific

---

Return to [reference index](INDEX.md)
