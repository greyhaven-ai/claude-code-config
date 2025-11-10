---
name: cf-logs-analyze
description: Analyze Cloudflare Workers logs and GitHub Actions deployment logs to identify errors, patterns, and performance issues
---

Analyze logs from Cloudflare Workers and GitHub Actions deployments to identify errors, patterns, and performance issues.

## What This Command Does

1. **Cloudflare Workers Logs**
   - Streams real-time Worker logs
   - Filters for errors and exceptions
   - Analyzes log patterns
   - Tracks error frequency

2. **GitHub Actions Logs**
   - Retrieves deployment workflow logs
   - Identifies build/deploy failures
   - Extracts error messages
   - Shows failed job steps

3. **Log Analysis**
   - Identifies common error patterns
   - Groups similar errors
   - Suggests fixes for common issues
   - Provides error context

## Usage

```bash
# Analyze recent Worker logs
/cf-logs-analyze

# Analyze specific deployment
/cf-logs-analyze <deployment-id>

# Analyze failed GitHub Actions run
/cf-logs-analyze --run <run-id>

# Filter for errors only
/cf-logs-analyze --errors-only

# Analyze last N minutes
/cf-logs-analyze --since 30m

# Specific worker
/cf-logs-analyze --worker production-worker

# Export logs to file
/cf-logs-analyze --export logs.json
```

## Implementation

When you use this command, Claude will:

1. **Stream Cloudflare Workers Logs**
```bash
# Tail Worker logs
wrangler tail <worker-name> --format=pretty

# Filter for errors
wrangler tail <worker-name> --format=json | jq 'select(.level=="error")'

# Get logs since timestamp
wrangler tail <worker-name> --since <timestamp>
```

2. **Analyze GitHub Actions Logs**
```bash
# Get workflow run logs
gh run view <run-id> --log

# Get failed job logs only
gh run view <run-id> --log-failed

# Get specific job logs
gh run view <run-id> --job <job-id> --log
```

3. **Parse and Analyze**
```javascript
// Log analysis structure
{
  "analysis_period": "last_1_hour",
  "total_logs": 15432,
  "errors": 23,
  "warnings": 145,
  "error_breakdown": {
    "TypeError": 12,
    "NetworkError": 6,
    "AuthenticationError": 3,
    "Other": 2
  },
  "top_errors": [
    {
      "type": "TypeError",
      "message": "Cannot read property 'id' of undefined",
      "count": 8,
      "first_seen": "2025-01-15T10:15:00Z",
      "last_seen": "2025-01-15T10:45:00Z",
      "locations": ["src/api/users.ts:42", "src/api/users.ts:67"],
      "suggested_fix": "Add null check before accessing user.id"
    }
  ]
}
```

4. **Generate Analysis Report**

## Output Format

### Example: Worker Logs Analysis

```markdown
## Cloudflare Worker Logs Analysis

**Worker**: production-worker
**Period**: Last 1 hour
**Total Logs**: 15,432

### Summary
- Total requests: 15,000
- Errors: 23 (0.15%)
- Warnings: 145 (0.97%)
- Average response time: 45ms

### Error Breakdown
| Type | Count | % of Errors | First Seen | Status |
|------|-------|-------------|------------|--------|
| TypeError | 12 | 52% | 10:15 UTC | 🔴 Active |
| NetworkError | 6 | 26% | 10:30 UTC | 🔴 Active |
| AuthenticationError | 3 | 13% | 10:25 UTC | ✅ Resolved |
| Other | 2 | 9% | 10:40 UTC | 🔴 Active |

### Top Errors

#### 1. TypeError: Cannot read property 'id' of undefined
- **Count**: 8 occurrences
- **First seen**: 10:15 UTC
- **Last seen**: 10:45 UTC
- **Location**: src/api/users.ts:42, src/api/users.ts:67
- **Impact**: 0.05% of requests
- **Suggested fix**:
  ```typescript
  // Before
  const userId = user.id;

  // After
  const userId = user?.id;
  if (!userId) {
    throw new Error('User ID not found');
  }
  ```

#### 2. NetworkError: Failed to fetch user data
- **Count**: 6 occurrences
- **First seen**: 10:30 UTC
- **Last seen**: 10:50 UTC
- **Location**: src/services/api.ts:123
- **Impact**: 0.04% of requests
- **Pattern**: All errors from same external API
- **Suggested fix**: Add retry logic with exponential backoff

#### 3. AuthenticationError: Invalid token
- **Count**: 3 occurrences
- **First seen**: 10:25 UTC
- **Last seen**: 10:35 UTC
- **Location**: src/middleware/auth.ts:45
- **Status**: ✅ Resolved at 10:36 UTC
- **Resolution**: Token refresh implemented

### Performance Issues

#### Slow Requests (>1s)
- **Count**: 45 (0.3% of requests)
- **Average duration**: 1.8s
- **Max duration**: 3.2s
- **Common pattern**: Database queries without indexes

### Log Patterns

#### Pattern 1: Rate Limiting
```
[10:15:32] WARNING: Rate limit approaching for user 12345
[10:15:45] WARNING: Rate limit approaching for user 12345
[10:15:58] ERROR: Rate limit exceeded for user 12345
```
**Analysis**: User hitting rate limits
**Recommendation**: Implement client-side throttling

#### Pattern 2: External API Timeouts
```
[10:30:12] INFO: Fetching user data from external API
[10:30:42] ERROR: Request timeout after 30s
```
**Analysis**: External API slow/unreachable
**Recommendation**: Add circuit breaker, reduce timeout

### Geographic Distribution
| Region | Requests | Errors | Error Rate |
|--------|----------|--------|------------|
| US-East | 8,000 | 5 | 0.06% |
| EU-West | 4,500 | 12 | 0.27% |
| APAC | 2,500 | 6 | 0.24% |

**Note**: Higher error rate in EU-West region

### Recommendations
1. **Critical**: Fix TypeError in user API (8 occurrences)
2. **High**: Add retry logic for external API calls
3. **Medium**: Optimize database queries causing slow requests
4. **Low**: Investigate higher error rate in EU-West region

### Next Steps
1. Deploy fix for TypeError in src/api/users.ts
2. Monitor error rate for next hour
3. Set up alert if error rate exceeds 0.5%
```

### Example: GitHub Actions Logs Analysis

```markdown
## GitHub Actions Deployment Logs Analysis

**Workflow**: Deploy to Cloudflare
**Run ID**: 12345678
**Status**: ✗ Failed
**Duration**: 3m 45s
**Triggered**: 2 hours ago by @developer

### Job Summary
| Job | Status | Duration | Error |
|-----|--------|----------|-------|
| Build | ✓ Success | 2m 15s | - |
| Test | ✓ Success | 1m 30s | - |
| Deploy | ✗ Failed | 0m 45s | Deployment rejected |

### Failed Job: Deploy

**Error**:
```
Error: Failed to publish your Function. Got error: Uncaught SyntaxError:
Unexpected token 'export' in dist/worker.js:1234
  at worker.js:1234:5
```

**Failed Step**: Deploy to Cloudflare Workers
**Time**: Step 4 of 5
**Exit Code**: 1

**Log Context**:
```
[2025-01-15 10:30:15] Installing dependencies...
[2025-01-15 10:30:45] Dependencies installed successfully
[2025-01-15 10:30:50] Building worker...
[2025-01-15 10:31:30] Build completed successfully
[2025-01-15 10:31:35] Deploying to Cloudflare...
[2025-01-15 10:31:40] ERROR: Failed to publish your Function
[2025-01-15 10:31:40] ERROR: Got error: Uncaught SyntaxError
```

### Root Cause Analysis

**Issue**: SyntaxError in deployed worker
**Cause**: Build output contains ES6 modules but Cloudflare Worker expects bundled code
**Location**: dist/worker.js:1234

**Code Context**:
```javascript
// Line 1234 in dist/worker.js
export { handler }; // ❌ This is the problem
```

**Why it failed**:
- Build process didn't bundle the code properly
- Export statement not compatible with Worker runtime
- Missing bundler configuration

### Suggested Fix

**Option 1**: Update build configuration
```json
// package.json
{
  "scripts": {
    "build": "esbuild src/index.ts --bundle --format=esm --outfile=dist/worker.js"
  }
}
```

**Option 2**: Update wrangler.toml
```toml
[build]
command = "npm run build"
watch_dirs = ["src"]

[build.upload]
format = "modules"
main = "./dist/worker.js"
```

### Prevention

To prevent this in the future:
1. Add build validation step before deployment
2. Test worker locally with `wrangler dev`
3. Add syntax validation in CI
4. Use TypeScript strict mode

**Recommended CI step**:
```yaml
- name: Validate Worker
  run: |
    wrangler deploy --dry-run
    node -c dist/worker.js  # Check syntax
```

### Related Issues
- Similar failure in run #12345600 (3 days ago)
- Pattern: Occurs after dependency updates
- Recommendation: Add pre-deployment validation

### Quick Fix Command
```bash
# Update build configuration
npm install --save-dev esbuild
# Update build script in package.json
# Redeploy
```
```

## Log Analysis Capabilities

### 1. Error Pattern Recognition

Identifies common error patterns:
- **Null pointer exceptions** → Add null checks
- **Authentication failures** → Check token/credentials
- **Network timeouts** → Add retry logic
- **Rate limiting** → Implement backoff
- **Build failures** → Check dependencies/configuration

### 2. Performance Analysis

Tracks performance metrics from logs:
- Request duration distribution
- Slow endpoint identification
- Cold start frequency
- Resource usage patterns

### 3. Security Issue Detection

Identifies security-related log entries:
- Authentication failures
- Unauthorized access attempts
- Suspicious request patterns
- Potential DDoS indicators

### 4. Deployment Issue Analysis

Analyzes deployment-specific problems:
- Build failures
- Test failures
- Configuration errors
- Dependency issues
- API quota/rate limits

## Advanced Features

### Log Aggregation

Combine logs from multiple sources:
```bash
# Analyze both Worker and CI logs
/cf-logs-analyze --deployment abc123 --include-ci
```

Output combines:
- Worker execution logs
- GitHub Actions deployment logs
- Build process logs
- Test execution logs

### Time-Series Analysis

Track errors over time:
```bash
# Analyze last 24 hours
/cf-logs-analyze --since 24h --group-by hour
```

Output:
```markdown
### Error Rate Over Time
| Hour | Requests | Errors | Error Rate |
|------|----------|--------|------------|
| 09:00 | 5,000 | 12 | 0.24% |
| 10:00 | 5,200 | 23 | 0.44% | 📈 Spike
| 11:00 | 5,100 | 8 | 0.16% |
```

### Error Correlation

Find correlated errors:
```markdown
### Correlated Errors
**Primary**: TypeError in user API
**Correlated with**:
- AuthenticationError (80% correlation)
- NetworkError to external API (60% correlation)

**Analysis**: TypeError occurs after auth token expiry
**Fix**: Refresh token before API call
```

## Integration

### With Monitoring Tools

Export to monitoring platforms:
```bash
# Export to Datadog
/cf-logs-analyze --export datadog

# Export to Sentry
/cf-logs-analyze --export sentry

# Export to JSON
/cf-logs-analyze --export logs.json
```

### With Incident Response

Use during incidents:
```bash
# Quick error analysis
/cf-logs-analyze --errors-only --since 30m

# Find specific error
/cf-logs-analyze --search "database timeout"

# Compare with previous deployment
/cf-logs-analyze --deployment abc123 --compare-to xyz789
```

## Best Practices

1. **Regular Analysis**
   - Analyze logs after each deployment
   - Review error patterns weekly
   - Track error rate trends

2. **Proactive Monitoring**
   - Set up log-based alerts
   - Monitor error rate thresholds
   - Track performance degradation

3. **Incident Response**
   - Use during outages for quick diagnosis
   - Compare with baseline logs
   - Track error resolution

## Related Commands

- `/cf-deployment-status` - Check deployment status
- `/cf-metrics-dashboard` - View metrics dashboard
- Use `cloudflare-deployment-monitor` agent for active monitoring
- Use `cloudflare-cicd-analyzer` agent for CI/CD optimization

## Configuration

Configure log analysis behavior:

```json
// .claude/settings.json
{
  "cloudflare-logs": {
    "default_worker": "production-worker",
    "analysis_window": "1h",
    "error_threshold": 0.01,
    "include_warnings": true,
    "export_format": "json"
  }
}
```

## Troubleshooting

**No logs available**:
- Check worker name
- Verify API token permissions
- Ensure worker is receiving traffic

**GitHub Actions logs not found**:
- Authenticate with `gh auth login`
- Check run ID is correct
- Verify repository access

**Analysis too slow**:
- Reduce time window
- Use `--errors-only` flag
- Filter by specific log level
