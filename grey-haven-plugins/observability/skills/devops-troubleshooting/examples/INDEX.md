# DevOps Troubleshooter Examples

Real-world infrastructure troubleshooting scenarios for Grey Haven's Cloudflare Workers + PlanetScale PostgreSQL stack.

## Examples Overview

### 1. Cloudflare Worker Deployment Failure

**File**: [cloudflare-worker-deployment-failure.md](cloudflare-worker-deployment-failure.md)
**Scenario**: Worker deployment fails with "Script exceeds size limit" error
**Stack**: Cloudflare Workers, wrangler, webpack bundling
**Impact**: Production deployment blocked, 2-hour downtime
**Resolution**: Bundle size reduction (5.2MB → 1.8MB), code splitting, tree shaking
**Lines**: ~450 lines

### 2. PlanetScale Connection Pool Exhaustion

**File**: [planetscale-connection-issues.md](planetscale-connection-issues.md)
**Scenario**: Database connection timeouts causing 503 errors
**Stack**: PlanetScale PostgreSQL, connection pooling, FastAPI
**Impact**: 15% of requests failing, customer complaints
**Resolution**: Connection pool tuning, connection leak fixes
**Lines**: ~430 lines

### 3. Distributed System Network Debugging

**File**: [distributed-system-debugging.md](distributed-system-debugging.md)
**Scenario**: Intermittent 504 Gateway Timeout errors between services
**Stack**: Cloudflare Workers, external APIs, DNS, CORS
**Impact**: 5% of API calls failing, no clear pattern
**Resolution**: DNS caching issue, worker timeout configuration
**Lines**: ~420 lines

### 4. Performance Degradation Analysis

**File**: [performance-degradation-analysis.md](performance-degradation-analysis.md)
**Scenario**: API response times increased from 200ms to 2000ms
**Stack**: Cloudflare Workers, PlanetScale, caching layer
**Impact**: User-facing slowness, poor UX
**Resolution**: N+1 query elimination, caching strategy, index optimization
**Lines**: ~410 lines

---

## Quick Navigation

**By Issue Type**:
- Deployment failures → [cloudflare-worker-deployment-failure.md](cloudflare-worker-deployment-failure.md)
- Database issues → [planetscale-connection-issues.md](planetscale-connection-issues.md)
- Network problems → [distributed-system-debugging.md](distributed-system-debugging.md)
- Performance issues → [performance-degradation-analysis.md](performance-degradation-analysis.md)

**By Stack Component**:
- Cloudflare Workers → Examples 1, 3, 4
- PlanetScale PostgreSQL → Examples 2, 4
- Distributed Systems → Example 3

---

## Related Documentation

- **Reference**: [Reference Index](../reference/INDEX.md) - Runbooks and diagnostic commands
- **Templates**: [Templates Index](../templates/INDEX.md) - Incident templates
- **Main Agent**: [devops-troubleshooter.md](../devops-troubleshooter.md) - DevOps troubleshooter agent

---

Return to [main agent](../devops-troubleshooter.md)
