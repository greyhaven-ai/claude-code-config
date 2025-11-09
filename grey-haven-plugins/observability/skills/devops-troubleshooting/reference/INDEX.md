# DevOps Troubleshooter Reference

Quick reference guides for Grey Haven infrastructure troubleshooting - runbooks, diagnostic commands, and platform-specific guides.

## Reference Guides

### Troubleshooting Runbooks

**File**: [troubleshooting-runbooks.md](troubleshooting-runbooks.md)

Step-by-step runbooks for common infrastructure issues:
- **Worker Not Responding**: 500/502/503 errors from Cloudflare Workers
- **Database Connection Failures**: Connection refused, pool exhaustion
- **Deployment Failures**: Failed deployments, rollback procedures
- **Performance Degradation**: Slow responses, high latency
- **Network Issues**: DNS failures, connectivity problems

**Use when**: Following structured resolution for known issues

---

### Diagnostic Commands Reference

**File**: [diagnostic-commands.md](diagnostic-commands.md)

Command reference for quick troubleshooting:
- **Cloudflare Workers**: wrangler commands, log analysis
- **PlanetScale**: Database queries, connection checks
- **Network**: curl timing, DNS resolution, traceroute
- **Performance**: Profiling, metrics collection

**Use when**: Need quick command syntax for diagnostics

---

### Cloudflare Workers Platform Guide

**File**: [cloudflare-workers-guide.md](cloudflare-workers-guide.md)

Cloudflare Workers-specific guidance:
- **Deployment Best Practices**: Bundle size, environment variables
- **Performance Optimization**: CPU limits, memory management
- **Error Handling**: Common errors and solutions
- **Monitoring**: Logs, metrics, analytics

**Use when**: Cloudflare Workers-specific issues

---

## Quick Navigation

**By Issue Type**:
- Worker errors → [troubleshooting-runbooks.md#worker-not-responding](troubleshooting-runbooks.md#worker-not-responding)
- Database issues → [troubleshooting-runbooks.md#database-connection-failures](troubleshooting-runbooks.md#database-connection-failures)
- Performance → [troubleshooting-runbooks.md#performance-degradation](troubleshooting-runbooks.md#performance-degradation)

**By Platform**:
- Cloudflare Workers → [cloudflare-workers-guide.md](cloudflare-workers-guide.md)
- PlanetScale → [diagnostic-commands.md#planetscale-commands](diagnostic-commands.md#planetscale-commands)
- Network → [diagnostic-commands.md#network-commands](diagnostic-commands.md#network-commands)

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Full troubleshooting walkthroughs
- **Templates**: [Templates Index](../templates/INDEX.md) - Incident report templates
- **Main Agent**: [devops-troubleshooter.md](../devops-troubleshooter.md) - DevOps troubleshooter agent

---

Return to [main agent](../devops-troubleshooter.md)
