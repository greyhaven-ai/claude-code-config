# Incident Response Reference

Quick reference guides for incident severity classification, communication templates, root cause analysis techniques, and runbook structure.

## Available References

### Incident Severity Matrix

**File**: [incident-severity-matrix.md](incident-severity-matrix.md)

Complete severity classification guide with examples:
- **SEV1 (Critical)**: Complete outage, all customers affected, revenue stopped
- **SEV2 (Major)**: Partial degradation, significant customer impact
- **SEV3 (Minor)**: Isolated issues, workarounds available
- **SEV4 (Cosmetic)**: UI issues, no functional impact

**Use when**: Classifying incident severity, determining escalation path

---

### Communication Templates

**File**: [communication-templates.md](communication-templates.md)

Ready-to-use templates for all incident communications:
- Internal updates (Slack, email)
- External communications (status page, customer emails)
- Executive briefings
- Post-incident summaries
- Postmortem distribution

**Use when**: Communicating during or after incidents

---

### Root Cause Analysis Techniques

**File**: [rca-techniques.md](rca-techniques.md)

Comprehensive RCA methodology guide:
- **5 Whys**: Iterative questioning to find root cause
- **Fishbone Diagrams**: Category-based analysis
- **Timeline Reconstruction**: Event sequencing and correlation
- **Contributing Factors Analysis**: Immediate vs underlying vs latent causes
- **Hypothesis Testing**: Data-driven validation

**Use when**: Conducting root cause analysis, writing postmortems

---

### Runbook Structure Guide

**File**: [runbook-structure-guide.md](runbook-structure-guide.md)

Best practices for writing effective runbooks:
- Standard runbook template
- Diagnostic procedures
- Remediation steps
- Escalation paths
- Success criteria
- Runbook maintenance

**Use when**: Creating or updating runbooks, automating diagnostics

---

## Quick Links

**By Use Case**:
- Need to classify incident severity → [Severity Matrix](incident-severity-matrix.md)
- Need to communicate during incident → [Communication Templates](communication-templates.md)
- Need to find root cause → [RCA Techniques](rca-techniques.md)
- Need to write a runbook → [Runbook Structure Guide](runbook-structure-guide.md)

**Related Documentation**:
- **Examples**: [Examples Index](../examples/INDEX.md) - Real-world incident examples
- **Templates**: [Templates Index](../templates/INDEX.md) - Incident timeline, postmortem templates
- **Main Agent**: [incident-responder.md](../incident-responder.md) - Incident responder agent

---

Return to [main agent](../incident-responder.md)
