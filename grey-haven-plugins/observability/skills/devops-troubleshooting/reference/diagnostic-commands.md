# Diagnostic Commands Reference

Quick command reference for Grey Haven infrastructure troubleshooting. Copy-paste ready commands for rapid diagnosis.

## Cloudflare Workers Commands

### Deployment Management

```bash
# List recent deployments
wrangler deployments list

# View specific deployment
wrangler deployments view <deployment-id>

# Rollback to previous version
wrangler rollback --message "Reverting due to errors"

# Deploy to production
wrangler deploy

# Deploy to staging
wrangler deploy --env staging
```

### Logs and Monitoring

```bash
# Real-time logs (pretty format)
wrangler tail --format pretty

# JSON logs for parsing
wrangler tail --format json

# Filter by status code
wrangler tail --format json | grep "\"status\":500"

# Show only errors
wrangler tail --format json | grep -i "error"

# Save logs to file
wrangler tail --format json > worker-logs.json

# Monitor specific worker
wrangler tail --name my-worker
```

### Local Development

```bash
# Start local dev server
wrangler dev

# Dev with specific port
wrangler dev --port 8788

# Dev with remote mode (use production bindings)
wrangler dev --remote

# Test locally
curl http://localhost:8787/api/health
```

### Configuration

```bash
# Show account info
wrangler whoami

# List KV namespaces
wrangler kv:namespace list

# List secrets
wrangler secret list

# Add secret
wrangler secret put API_KEY

# Delete secret
wrangler secret delete API_KEY
```

---

## PlanetScale Commands

### Database Management

```bash
# Connect to database shell
pscale shell greyhaven-db main

# Connect and execute query
pscale shell greyhaven-db main --execute "SELECT COUNT(*) FROM users"

# Show database info
pscale database show greyhaven-db

# List all databases
pscale database list

# Create new branch
pscale branch create greyhaven-db feature-branch

# List branches
pscale branch list greyhaven-db
```

### Connection Monitoring

```sql
-- Active connections
SELECT COUNT(*) as active_connections
FROM pg_stat_activity
WHERE state = 'active';

-- Long-running queries
SELECT
  pid,
  now() - query_start as duration,
  query
FROM pg_stat_activity
WHERE state = 'active'
  AND query_start < now() - interval '10 seconds'
ORDER BY duration DESC;

-- Connection by state
SELECT state, COUNT(*)
FROM pg_stat_activity
GROUP BY state;

-- Blocked queries
SELECT
  blocked.pid AS blocked_pid,
  blocking.pid AS blocking_pid,
  blocked.query AS blocked_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid));
```

### Performance Analysis

```bash
# Slow query insights
pscale database insights greyhaven-db main --slow-queries

# Database size
pscale database show greyhaven-db --web

# Enable slow query log
pscale database settings update greyhaven-db --enable-slow-query-log
```

```sql
-- Table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Cache hit ratio
SELECT
  'cache hit rate' AS metric,
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS ratio
FROM pg_statio_user_tables;
```

### Schema Migrations

```bash
# Create deploy request
pscale deploy-request create greyhaven-db <branch-name>

# List deploy requests
pscale deploy-request list greyhaven-db

# View deploy request diff
pscale deploy-request diff greyhaven-db <number>

# Deploy schema changes
pscale deploy-request deploy greyhaven-db <number>

# Close deploy request
pscale deploy-request close greyhaven-db <number>
```

---

## Network Diagnostic Commands

### DNS Resolution

```bash
# Basic DNS lookup
nslookup api.partner.com

# Detailed DNS query
dig api.partner.com

# Measure DNS time
time nslookup api.partner.com

# Check DNS propagation
dig api.partner.com @8.8.8.8
dig api.partner.com @1.1.1.1

# Reverse DNS lookup
dig -x 203.0.113.42
```

### Connectivity Testing

```bash
# Ping test
ping -c 10 api.partner.com

# Trace network route
traceroute api.partner.com

# TCP connection test
nc -zv api.partner.com 443

# Test specific port
telnet api.partner.com 443
```

### HTTP Request Timing

```bash
# Full timing breakdown
curl -w "\nDNS Lookup:    %{time_namelookup}s\nTCP Connect:   %{time_connect}s\nTLS Handshake: %{time_appconnect}s\nStart Transfer:%{time_starttransfer}s\nTotal:         %{time_total}s\n" \
  -o /dev/null -s https://api.partner.com/data

# Test with specific method
curl -X POST https://api.example.com/api \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Follow redirects
curl -L https://example.com

# Show response headers
curl -I https://api.example.com

# Test CORS
curl -I -X OPTIONS https://api.example.com \
  -H "Origin: https://app.example.com" \
  -H "Access-Control-Request-Method: POST"
```

### SSL/TLS Verification

```bash
# Check SSL certificate
openssl s_client -connect api.example.com:443

# Show certificate expiry
echo | openssl s_client -connect api.example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Verify certificate chain
openssl s_client -connect api.example.com:443 -showcerts
```

---

## Application Performance Commands

### Resource Monitoring

```bash
# CPU usage
top -o cpu

# Memory usage
free -h  # Linux
vm_stat  # macOS

# Disk usage
df -h

# Process list
ps aux | grep node

# Port usage
lsof -i :8000
netstat -an | grep 8000
```

### Log Analysis

```bash
# Tail logs
tail -f /var/log/app.log

# Search logs
grep -i "error" /var/log/app.log

# Count errors
grep -c "ERROR" /var/log/app.log

# Show recent errors with context
grep -B 5 -A 5 "error" /var/log/app.log

# Parse JSON logs
cat app.log | jq 'select(.level=="error")'

# Error frequency
grep "ERROR" /var/log/app.log | cut -d' ' -f1 | uniq -c
```

### Worker Performance

```bash
# Monitor CPU time
wrangler tail --format json | jq '.outcome.cpuTime'

# Monitor duration
wrangler tail --format json | jq '.outcome.duration'

# Requests per second
wrangler tail --format json | wc -l

# Average response time
wrangler tail --format json | \
  jq -r '.outcome.duration' | \
  awk '{sum+=$1; count++} END {print sum/count}'
```

---

## Health Check Scripts

### Worker Health Check

```bash
#!/bin/bash
# health-check-worker.sh

echo "=== Worker Health Check ==="

# Test endpoint
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.greyhaven.io/health)

if [ "$STATUS" -eq 200 ]; then
  echo "✅ Worker responding (HTTP $STATUS)"
else
  echo "❌ Worker error (HTTP $STATUS)"
  exit 1
fi

# Check response time
TIME=$(curl -w "%{time_total}" -o /dev/null -s https://api.greyhaven.io/health)
echo "Response time: ${TIME}s"

if (( $(echo "$TIME > 1.0" | bc -l) )); then
  echo "⚠️  Slow response (>${TIME}s)"
fi
```

### Database Health Check

```bash
#!/bin/bash
# health-check-db.sh

echo "=== Database Health Check ==="

# Test connection
pscale shell greyhaven-db main --execute "SELECT 1" > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo "✅ Database connection OK"
else
  echo "❌ Database connection failed"
  exit 1
fi

# Check active connections
ACTIVE=$(pscale shell greyhaven-db main --execute \
  "SELECT COUNT(*) FROM pg_stat_activity WHERE state='active'" | tail -1)

echo "Active connections: $ACTIVE"

if [ "$ACTIVE" -gt 80 ]; then
  echo "⚠️  High connection count (>80)"
fi
```

### Complete System Health

```bash
#!/bin/bash
# health-check-all.sh

echo "=== Complete System Health Check ==="

# Worker
echo "\n1. Cloudflare Worker"
./health-check-worker.sh

# Database
echo "\n2. PlanetScale Database"
./health-check-db.sh

# External APIs
echo "\n3. External Dependencies"
for API in "https://api.partner1.com/health" "https://api.partner2.com/health"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API")
  if [ "$STATUS" -eq 200 ]; then
    echo "✅ $API (HTTP $STATUS)"
  else
    echo "❌ $API (HTTP $STATUS)"
  fi
done

echo "\n=== Health Check Complete ==="
```

---

## Troubleshooting One-Liners

```bash
# Find memory hogs
ps aux --sort=-%mem | head -10

# Find CPU hogs
ps aux --sort=-%cpu | head -10

# Disk space by directory
du -sh /* | sort -h

# Network connections
netstat -ant | awk '{print $6}' | sort | uniq -c

# Failed login attempts
grep "Failed password" /var/log/auth.log | wc -l

# Top error codes
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# Requests per minute
awk '{print $4}' access.log | cut -d: -f1-2 | uniq -c

# Average response size
awk '{sum+=$10; count++} END {print sum/count}' access.log
```

---

## Related Documentation

- **Runbooks**: [troubleshooting-runbooks.md](troubleshooting-runbooks.md) - Step-by-step procedures
- **Cloudflare Guide**: [cloudflare-workers-guide.md](cloudflare-workers-guide.md) - Platform-specific
- **Examples**: [Examples Index](../examples/INDEX.md) - Full troubleshooting examples

---

Return to [reference index](INDEX.md)
