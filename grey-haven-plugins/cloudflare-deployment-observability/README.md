# Cloudflare Deployment Observability Plugin

Comprehensive observability for Cloudflare Workers and Pages deployments with GitHub Actions CI/CD integration. Monitor deployment pipelines, track metrics, analyze logs, and receive alerts.

## Overview

This plugin provides end-to-end observability for Cloudflare deployments, helping you:

- **Monitor deployments** in real-time across all environments
- **Track deployment metrics** including success rates, duration, and frequency
- **Analyze CI/CD pipelines** to identify bottlenecks and optimize performance
- **Monitor post-deployment performance** with detailed metrics and Core Web Vitals
- **Detect regressions** early with automated performance comparisons
- **Integrate with observability platforms** like Datadog, Sentry, and Grafana

## Features

### 🎯 Deployment Monitoring
- Real-time deployment status tracking
- Multi-environment support (production, staging, preview)
- Deployment success/failure tracking
- Rollback detection and tracking
- GitHub Actions workflow integration

### 📊 Performance Tracking
- Request latency monitoring (p50, p95, p99)
- Error rate tracking
- Cold start analysis
- Bundle size monitoring
- Geographic performance analysis
- Core Web Vitals tracking for Pages

### 🔍 Log Analysis
- Cloudflare Workers log streaming
- GitHub Actions log analysis
- Error pattern recognition
- Root cause analysis
- Automated fix suggestions

### 🚀 CI/CD Pipeline Optimization
- Workflow performance analysis
- Job-level duration tracking
- Cache effectiveness monitoring
- Parallelization opportunities
- Cost optimization recommendations

### 📈 Metrics Dashboard
- Comprehensive deployment metrics
- Performance trends
- CI/CD pipeline health
- SLO tracking
- Historical comparisons

## Installation

This plugin is part of the Grey Haven Claude Code plugin marketplace.

### 1. Add to Plugin Marketplace

Add to your `.claude/settings.json`:

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/path/to/grey-haven-plugins"
    }],
    "install": [
      "cloudflare-deployment-observability@grey-haven-plugins"
    ]
  }
}
```

### 2. Required Environment Variables

Set up the following environment variables:

```bash
# Cloudflare credentials
export CLOUDFLARE_API_TOKEN="your-api-token"
export CLOUDFLARE_ACCOUNT_ID="your-account-id"

# GitHub CLI (for workflow analysis)
gh auth login

# Optional: Observability platform integration
export DATADOG_API_KEY="your-datadog-api-key"
export SENTRY_AUTH_TOKEN="your-sentry-token"
export SENTRY_ORG="your-org"
export SENTRY_PROJECT="your-project"
```

### 3. Install Dependencies

```bash
# Cloudflare Wrangler
npm install -g wrangler

# GitHub CLI
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

## Usage

### Commands

#### `/cf-deployment-status`
Check deployment status across environments.

```bash
# Check all environments
/cf-deployment-status

# Check specific environment
/cf-deployment-status production

# Show failed deployments only
/cf-deployment-status --failed

# Check last N deployments
/cf-deployment-status --limit 20
```

**Example output:**
```markdown
## Deployment Status Report

**Generated**: 2025-01-15 10:30:00 UTC

### Summary
- Total deployments (24h): 15
- Success rate: 93% (14/15)
- Average duration: 2m 45s

### Environments
#### Production
- Status: ✓ Healthy
- Last deployment: 2 hours ago
- Health check: ✓ Passing
```

#### `/cf-logs-analyze`
Analyze Cloudflare Workers and GitHub Actions logs.

```bash
# Analyze recent logs
/cf-logs-analyze

# Filter for errors only
/cf-logs-analyze --errors-only

# Analyze specific deployment
/cf-logs-analyze <deployment-id>

# Analyze failed workflow
/cf-logs-analyze --run <run-id>
```

**Example output:**
```markdown
## Log Analysis

**Period**: Last 1 hour
**Errors**: 23 (0.15%)

### Top Errors
1. TypeError: Cannot read property 'id' of undefined
   - Count: 8 occurrences
   - Location: src/api/users.ts:42
   - Suggested fix: Add null check
```

#### `/cf-metrics-dashboard`
Display comprehensive metrics dashboard.

```bash
# Show all metrics
/cf-metrics-dashboard

# Specific time range
/cf-metrics-dashboard --range 7d

# Compare deployments
/cf-metrics-dashboard --compare abc123 xyz789

# Export to file
/cf-metrics-dashboard --export dashboard.json
```

**Example output:**
```markdown
# Cloudflare Deployment Metrics Dashboard

## Executive Summary
| Metric | Value | Trend | Status |
|--------|-------|-------|--------|
| Success Rate | 96% | ↑ +2% | ✅ Good |
| Avg Duration | 2m 45s | ↓ -15s | ✅ Good |
| Error Rate | 0.08% | ↓ -0.02% | ✅ Good |
| P95 Latency | 125ms | ↑ +10ms | ⚠️ Warning |
```

### Agents

#### `cloudflare-deployment-monitor`
Expert agent for monitoring deployments.

**Use when:**
- Setting up deployment monitoring
- Investigating deployment failures
- Tracking deployment metrics
- Implementing deployment alerts

**Example usage:**
```
Claude, use the cloudflare-deployment-monitor agent to help me
investigate why our staging deployments are failing.
```

#### `cloudflare-cicd-analyzer`
Expert agent for CI/CD pipeline analysis and optimization.

**Use when:**
- Optimizing GitHub Actions workflows
- Reducing workflow execution time
- Implementing CI/CD best practices
- Troubleshooting pipeline issues

**Example usage:**
```
Claude, use the cloudflare-cicd-analyzer agent to analyze our
deployment workflow and suggest optimizations.
```

#### `cloudflare-performance-tracker`
Expert agent for post-deployment performance monitoring.

**Use when:**
- Tracking deployment performance
- Detecting performance regressions
- Monitoring Core Web Vitals
- Analyzing Worker execution metrics

**Example usage:**
```
Claude, use the cloudflare-performance-tracker agent to check if
the latest deployment introduced any performance regressions.
```

## GitHub Actions Integration

### Quick Start

Use the provided workflow template for comprehensive observability:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare with Observability

on:
  push:
    branches: [main, develop]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        check: [lint, test, type-check]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run ${{ matrix.check }}

  deploy:
    needs: quality-checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}

      - name: Health Check
        run: curl -f https://your-worker.workers.dev/health

      - name: Report to Datadog
        if: always()
        run: |
          curl -X POST "https://api.datadoghq.com/api/v1/events" \
            -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
            -d '{
              "title": "Deployment ${{ job.status }}",
              "text": "Deployed ${{ github.sha }}",
              "tags": ["env:production", "status:${{ job.status }}"]
            }'
```

See `workflows/deployment-with-observability.yml` for a complete example with:
- Parallel quality checks
- Multi-environment deployment
- Health checks and smoke tests
- Automatic rollback on failure
- Integration with Datadog and Sentry
- Slack notifications
- Preview deployments for PRs

## Monitoring Setup

### 1. Local Monitoring

Use the provided monitoring script:

```bash
# Make script executable
chmod +x scripts/monitor-deployment.sh

# Monitor production worker for 5 minutes
./scripts/monitor-deployment.sh production-worker production 300
```

The script provides:
- Real-time metrics dashboard
- Error rate tracking
- Latency monitoring
- Health checks
- Log analysis
- Automated reporting

### 2. Continuous Monitoring

Set up automated monitoring in CI/CD:

```yaml
- name: Monitor Deployment
  run: |
    ./scripts/monitor-deployment.sh production-worker production 300
    if [ $? -ne 0 ]; then
      echo "Deployment monitoring detected issues"
      exit 1
    fi
```

### 3. Observability Platform Integration

#### Datadog

```bash
# In your deployment workflow
- name: Send Metrics to Datadog
  run: |
    curl -X POST "https://api.datadoghq.com/api/v1/series" \
      -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
      -d '{
        "series": [{
          "metric": "cloudflare.deployment.duration",
          "points": [['$(date +%s)', '165']],
          "type": "gauge",
          "tags": ["env:production"]
        }]
      }'
```

#### Sentry

```bash
# Track releases and deployments
- name: Create Sentry Release
  run: |
    npx @sentry/cli releases new "${{ github.sha }}"
    npx @sentry/cli releases set-commits "${{ github.sha }}" --auto
    npx @sentry/cli releases finalize "${{ github.sha }}"
    npx @sentry/cli releases deploys "${{ github.sha }}" new -e production
```

## Best Practices

### 1. Deployment Monitoring

- ✅ Monitor all environments (production, staging, preview)
- ✅ Set up health checks for all deployments
- ✅ Track deployment frequency and success rate
- ✅ Implement automatic rollback on failures
- ✅ Monitor post-deployment metrics for 5-10 minutes

### 2. Performance Tracking

- ✅ Track Core Web Vitals for Pages
- ✅ Monitor cold start frequency and duration
- ✅ Set up alerts for performance regressions
- ✅ Compare performance across deployments
- ✅ Monitor bundle size growth

### 3. CI/CD Optimization

- ✅ Parallelize independent jobs
- ✅ Implement effective caching
- ✅ Use conditional execution
- ✅ Right-size GitHub Actions runners
- ✅ Monitor workflow costs

### 4. Alerting

- ✅ Set up tiered alerts (critical, warning, info)
- ✅ Configure alerts for SLO violations
- ✅ Route alerts to appropriate channels
- ✅ Include actionable information in alerts
- ✅ Avoid alert fatigue

## Metrics Reference

### Deployment Metrics
- **Deployment Frequency**: Deployments per day/week
- **Deployment Success Rate**: % of successful deployments
- **Mean Time to Deployment (MTTD)**: Average deployment duration
- **Rollback Rate**: Frequency of rollbacks
- **Change Failure Rate**: % of deployments causing issues

### Performance Metrics
- **Request Latency**: p50, p95, p99 response times
- **Error Rate**: % of failed requests
- **Throughput**: Requests per second
- **Cold Start Rate**: % of requests with cold starts
- **Bundle Size**: Worker bundle size in KB

### CI/CD Metrics
- **Workflow Success Rate**: % of successful workflow runs
- **Pipeline Duration**: Total workflow execution time
- **Job Performance**: Duration of individual jobs
- **Cache Hit Rate**: Effectiveness of caching
- **GitHub Actions Minutes**: Usage tracking

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: Loading performance (<2.5s)
- **FID (First Input Delay)**: Interactivity (<100ms)
- **CLS (Cumulative Layout Shift)**: Visual stability (<0.1)
- **TTFB (Time to First Byte)**: Server responsiveness (<600ms)

## Troubleshooting

### Common Issues

#### No deployment data available
**Solution:**
- Verify `CLOUDFLARE_API_TOKEN` is set
- Check worker name is correct
- Ensure API token has correct permissions

#### GitHub Actions logs unavailable
**Solution:**
- Run `gh auth login` to authenticate
- Verify repository access
- Check workflow file exists

#### Health checks fail
**Solution:**
- Verify endpoint URL is correct
- Check network connectivity
- Ensure health endpoint is implemented

#### High error rates after deployment
**Solution:**
1. Check deployment logs with `/cf-logs-analyze`
2. Review recent code changes
3. Check for configuration issues
4. Consider rolling back if critical

## Examples

### Example 1: Monitor Deployment Success

```bash
# After deploying to production
/cf-deployment-status production

# Check for any errors
/cf-logs-analyze --errors-only --since 10m

# View performance metrics
/cf-metrics-dashboard --range 1h
```

### Example 2: Investigate Deployment Failure

```bash
# Check what failed
/cf-deployment-status --failed

# Analyze logs for the failed deployment
/cf-logs-analyze --run <run-id>

# Get detailed analysis from agent
Claude, use the cloudflare-deployment-monitor agent to
investigate the deployment failure in run <run-id>.
```

### Example 3: Optimize CI/CD Pipeline

```bash
# Analyze current workflow performance
Claude, use the cloudflare-cicd-analyzer agent to analyze
our .github/workflows/deploy.yml and suggest optimizations.

# Check metrics after optimization
/cf-metrics-dashboard --metrics cicd --range 7d
```

### Example 4: Detect Performance Regression

```bash
# Compare performance between deployments
/cf-metrics-dashboard --compare <old-deploy> <new-deploy>

# Get detailed performance analysis
Claude, use the cloudflare-performance-tracker agent to
check if deployment <new-deploy> introduced any regressions.
```

## Contributing

This plugin is part of the Grey Haven Studio Claude Code plugin collection. Contributions are welcome!

### Plugin Structure

```
cloudflare-deployment-observability/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── agents/
│   ├── deployment-monitor.md # Deployment monitoring agent
│   ├── ci-cd-analyzer.md     # CI/CD analysis agent
│   └── performance-tracker.md # Performance tracking agent
├── commands/
│   ├── deployment-status/    # Deployment status command
│   ├── logs-analyze/         # Log analysis command
│   └── metrics-dashboard/    # Metrics dashboard command
├── workflows/
│   └── deployment-with-observability.yml # Example workflow
├── scripts/
│   └── monitor-deployment.sh # Monitoring script
└── README.md                 # This file
```

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/greyhaven-ai/claude-code-config
- Documentation: See individual agent and command files

## Changelog

### v1.0.0 (2025-01-15)
- Initial release
- Deployment monitoring agent
- CI/CD analyzer agent
- Performance tracker agent
- Three slash commands: deployment-status, logs-analyze, metrics-dashboard
- GitHub Actions workflow template
- Monitoring scripts
- Comprehensive documentation

## Related Plugins

- **deployment**: Cloudflare Workers and Pages deployment
- **observability**: General production observability tools
- **developer-experience**: Development workflow enhancements
- **incident-response**: Incident management and response

## Acknowledgments

Built for the Claude Code community by Grey Haven Studio.
