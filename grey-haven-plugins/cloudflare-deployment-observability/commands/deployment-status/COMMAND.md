---
name: cf-deployment-status
description: Check Cloudflare deployment status across environments, view recent deployments, and monitor CI/CD pipeline health
---

Check the status of Cloudflare Workers and Pages deployments. This command provides a comprehensive view of deployment health across all environments.

## What This Command Does

1. **List Recent Deployments**
   - Shows last 10 deployments
   - Displays status (success/failure/in-progress)
   - Shows deployment duration
   - Includes commit SHA and message

2. **GitHub Actions Status**
   - Lists recent workflow runs
   - Shows current deployment pipeline status
   - Identifies failed or stuck workflows
   - Displays workflow execution time

3. **Environment Health Check**
   - Checks production deployment status
   - Verifies staging environment
   - Tests preview deployments
   - Shows environment-specific metrics

## Usage

```bash
# Basic usage - check all environments
/cf-deployment-status

# Check specific environment
/cf-deployment-status production

# Show last N deployments
/cf-deployment-status --limit 20

# Show failed deployments only
/cf-deployment-status --failed

# Check specific worker
/cf-deployment-status --worker my-worker-name
```

## Implementation

When you use this command, Claude will:

1. **Check Cloudflare Deployments**
```bash
# List deployments via Wrangler
wrangler deployments list --name <worker-name>

# Get deployment details
wrangler deployments view <deployment-id>
```

2. **Check GitHub Actions**
```bash
# List recent workflow runs
gh run list --workflow=deploy.yml --limit=10 --json status,conclusion,createdAt,updatedAt,headSha,headBranch

# Check for failures
gh run list --workflow=deploy.yml --status=failure --limit=5
```

3. **Environment Health**
```bash
# Test production endpoint
curl -f https://production.example.com/health

# Test staging endpoint
curl -f https://staging.example.com/health
```

4. **Generate Report**
```markdown
## Deployment Status Report

**Generated**: 2025-01-15 10:30:00 UTC

### Summary
- Total deployments (24h): 15
- Success rate: 93% (14/15)
- Active failures: 1
- Average duration: 2m 45s

### Environments

#### Production
- Status: ✓ Healthy
- Last deployment: 2 hours ago (abc123)
- Version: v1.2.3
- Health check: ✓ Passing

#### Staging
- Status: ✓ Healthy
- Last deployment: 30 minutes ago (def456)
- Version: v1.2.4-rc.1
- Health check: ✓ Passing

### Recent Deployments
| Time | Environment | Status | Duration | Commit | Triggered By |
|------|-------------|--------|----------|--------|--------------|
| 10:15 | production | ✓ Success | 2m 30s | abc123 | GitHub Actions |
| 10:00 | staging | ✓ Success | 2m 15s | def456 | GitHub Actions |
| 09:45 | staging | ✗ Failed | 1m 05s | ghi789 | Manual |

### Active Issues
1. Staging deployment failed (ghi789)
   - Error: Build failed - missing environment variable
   - Time: 09:45 UTC
   - Duration: 1m 05s
   - Recommendation: Check GitHub secrets configuration

### GitHub Actions Status
- Workflow: Deploy to Cloudflare
- Last run: ✓ Success (2 hours ago)
- Average duration: 2m 45s
- Success rate (7 days): 95%

### Recommendations
✓ All systems operational
- No action required
```

## Output Format

The command provides structured output with:

- **Executive summary** - Quick overview of deployment health
- **Environment status** - Status of each environment (production, staging, preview)
- **Recent deployments** - Table of recent deployments with status
- **Active issues** - Any current deployment problems
- **CI/CD health** - GitHub Actions workflow status
- **Recommendations** - Suggested actions

## Error Handling

If the command encounters issues:

1. **No Cloudflare credentials**
```
⚠ Warning: Cloudflare API token not found
Set CLOUDFLARE_API_TOKEN environment variable or configure wrangler.toml
```

2. **GitHub CLI not authenticated**
```
⚠ Warning: GitHub CLI not authenticated
Run: gh auth login
```

3. **Worker not found**
```
✗ Error: Worker 'my-worker' not found
Available workers:
  - production-worker
  - staging-worker
```

4. **API rate limit**
```
⚠ Warning: Cloudflare API rate limit reached
Retry in 60 seconds or use cached data
```

## Best Practices

1. **Regular Monitoring**
   - Run daily to track deployment health
   - Set up automated checks in CI/CD
   - Monitor success rate trends

2. **Quick Debugging**
   - Use `--failed` flag to focus on issues
   - Check specific environments during incidents
   - Compare deployment durations

3. **Integration**
   - Add to deployment pipeline for validation
   - Include in monitoring dashboards
   - Use in incident response runbooks

## Related Commands

- `/cf-logs-analyze` - Analyze deployment logs
- `/cf-metrics-dashboard` - View detailed metrics
- Use `cloudflare-deployment-monitor` agent for active monitoring

## Examples

### Example 1: Check Production Status
```bash
/cf-deployment-status production
```

Output:
```markdown
## Production Deployment Status

**Status**: ✓ Healthy
**Last Deployment**: 2 hours ago
**Version**: v1.2.3 (abc123)
**Health Check**: ✓ Passing
**Response Time**: 45ms (p95)
**Error Rate**: 0.01%

**Recent Deployments**:
1. ✓ abc123 - 2 hours ago - "Fix authentication bug" (2m 30s)
2. ✓ xyz789 - 1 day ago - "Add new feature" (2m 45s)
3. ✓ def456 - 2 days ago - "Update dependencies" (3m 10s)
```

### Example 2: Check Failed Deployments
```bash
/cf-deployment-status --failed
```

Output:
```markdown
## Failed Deployments

**Last 24 Hours**: 2 failures

### Failure 1: ghi789
- **Time**: 2 hours ago
- **Environment**: staging
- **Duration**: 1m 05s
- **Error**: Build failed - Type error in src/api/handler.ts
- **Triggered By**: GitHub Actions (PR #123)
- **Logs**: Available via `gh run view 12345678`

### Failure 2: jkl012
- **Time**: 5 hours ago
- **Environment**: preview
- **Duration**: 45s
- **Error**: Missing CLOUDFLARE_ACCOUNT_ID secret
- **Triggered By**: GitHub Actions (PR #122)
- **Fixed**: Yes (redeployed successfully)
```

### Example 3: Check All Workers
```bash
/cf-deployment-status
```

Output shows status for all workers and environments with summary metrics.

## Configuration

The command uses these configuration sources:

1. **wrangler.toml** - Worker configuration
2. **GitHub Actions workflows** - CI/CD configuration
3. **Environment variables**:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
   - `GITHUB_TOKEN` (for gh CLI)

## Troubleshooting

**Command returns no deployments**:
- Check wrangler.toml configuration
- Verify worker name
- Ensure API token has correct permissions

**GitHub Actions status unavailable**:
- Authenticate with `gh auth login`
- Check repository permissions
- Verify workflow file exists

**Health checks fail**:
- Verify endpoint URLs
- Check network connectivity
- Ensure health endpoint is implemented
