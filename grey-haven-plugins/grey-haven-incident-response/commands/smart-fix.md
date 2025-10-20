---
name: smart-fix
description: Intelligent debugging command that automatically analyzes issues, routes to appropriate specialists, and implements fixes. Uses multi-agent orchestration for rapid problem resolution with testing and verification.
---

# Smart Fix - Intelligent Automated Debugging

AI-powered debugging that analyzes issues, delegates to specialists, implements fixes, and validates solutions automatically.

## Overview

Smart Fix uses multi-agent orchestration to intelligently debug production issues by:
- Analyzing symptoms to identify root cause category
- Routing to appropriate domain specialists
- Implementing fixes with automated testing
- Verifying solutions with monitoring validation

## Usage

```bash
/smart-fix <issue description>
```

**Examples:**
```bash
/smart-fix High memory usage causing OOM kills in production
/smart-fix Intermittent database connection timeouts
/smart-fix API returning 500 errors for /checkout endpoint
/smart-fix Slow query performance on orders table
```

## Intelligent Routing Logic

### 1. Issue Analysis Phase
```
Use Task tool with subagent_type="error-detective"
→ Analyze error logs and patterns
→ Classify issue category (performance, database, network, security, application)
→ Identify affected components
→ Estimate severity and urgency
```

### 2. Specialist Routing

**Performance Issues** → performance-engineer
- High CPU/memory usage
- Slow response times
- Resource exhaustion
- Cache inefficiency

**Database Issues** → database-admin
- Connection pool exhaustion
- Slow queries
- Replication lag
- Deadlocks

**Network Issues** → network-engineer
- Connectivity failures
- Timeout errors
- DNS problems
- Load balancer issues

**Security Issues** → security-analyzer
- Authentication failures
- Suspicious access patterns
- Injection attempts
- Credential issues

**Application Bugs** → backend-architect / debugger
- Logic errors
- Null pointer exceptions
- State management issues
- Integration failures

### 3. Fix Implementation
```
Use Task tool with identified specialist
→ Deep dive into root cause
→ Implement fix (code, config, infrastructure)
→ Create automated tests
→ Deploy with verification
```

### 4. Validation Phase
```
Use Task tool with subagent_type="observability-engineer"
→ Monitor metrics post-fix
→ Validate error rate reduction
→ Confirm performance improvement
→ Check SLO compliance
```

## Output Format

1. **Analysis Summary**
   - Issue classification
   - Root cause hypothesis
   - Affected services/components
   - Severity assessment

2. **Specialist Recommendation**
   - Routed specialist agent
   - Rationale for selection
   - Expected resolution approach

3. **Fix Implementation**
   - Changes made (code, config, infra)
   - Testing performed
   - Deployment steps

4. **Verification Results**
   - Metrics before/after
   - Error rate improvement
   - Performance impact
   - SLO status

## Advanced Features

### Multi-Issue Detection
If multiple issues detected, prioritizes by severity and resolves sequentially.

### Cascading Failure Handling
Identifies root cause vs symptoms, fixes underlying issue first.

### Rollback Safety
Creates checkpoint before changes, automatic rollback if validation fails.

### Knowledge Capture
Documents fix in runbook, updates troubleshooting guides, shares with team.

## Integration

- **Observability:** Uses Prometheus, Grafana, traces for analysis
- **Testing:** Runs regression tests, integration tests post-fix
- **Documentation:** Auto-updates runbooks with new procedures
- **Communication:** Posts updates to incident channel if active

## References

- [Google SRE - Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)
- [Debugging Production Systems](https://www.brendangregg.com/blog/)
