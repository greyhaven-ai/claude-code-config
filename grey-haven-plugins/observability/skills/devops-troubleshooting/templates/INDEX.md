# DevOps Troubleshooter Templates

Ready-to-use templates for infrastructure incident response, deployment checklists, and performance investigations.

## Available Templates

### Incident Report Template

**File**: [incident-report-template.md](incident-report-template.md)

Comprehensive template for documenting infrastructure incidents:
- **Incident Overview**: Summary, impact, timeline
- **Root Cause Analysis**: What happened, why it happened
- **Resolution Steps**: What was done to fix it
- **Prevention Measures**: How to prevent recurrence
- **Lessons Learned**: What went well, what could improve

**Use when**: Documenting production outages, degradations, or significant infrastructure issues

**Copy and fill in** all sections for your specific incident.

---

### Deployment Checklist

**File**: [deployment-checklist.md](deployment-checklist.md)

Pre-deployment and post-deployment verification checklist:
- **Pre-Deployment Verification**: Code review, tests, dependencies, configuration
- **Deployment Steps**: Backup, deploy, verify, rollback plan
- **Post-Deployment Monitoring**: Health checks, metrics, logs, alerts
- **Rollback Procedures**: When and how to rollback

**Use when**: Deploying Cloudflare Workers, database migrations, infrastructure changes

**Check off** each item before and after deployment.

---

### Performance Investigation Template

**File**: [performance-investigation-template.md](performance-investigation-template.md)

Systematic template for investigating performance issues:
- **Performance Baseline**: Current metrics vs expected
- **Hypothesis Generation**: Potential root causes
- **Data Collection**: Profiling, metrics, logs
- **Analysis**: What the data reveals
- **Optimization Plan**: Prioritized fixes with impact estimates
- **Validation**: Before/after metrics

**Use when**: API latency increases, database slow queries, high CPU/memory usage

**Follow systematically** to diagnose and resolve performance problems.

---

## Template Usage

**How to use these templates**:
1. Copy the template file to your project documentation
2. Fill in all sections marked with `[FILL IN]` placeholders
3. Remove sections that don't apply (optional)
4. Share with your team for review

**When to create reports**:
- **Incident Report**: After any production incident (SEV1-SEV3)
- **Deployment Checklist**: Before every production deployment
- **Performance Investigation**: When performance degrades >20%

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Real-world troubleshooting walkthroughs
- **Reference**: [Reference Index](../reference/INDEX.md) - Runbooks and diagnostic commands
- **Main Agent**: [devops-troubleshooter.md](../devops-troubleshooter.md) - DevOps troubleshooter agent

---

Return to [main agent](../devops-troubleshooter.md)
