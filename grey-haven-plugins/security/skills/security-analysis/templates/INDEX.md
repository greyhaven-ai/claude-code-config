# Security Templates

Copy-paste ready templates for security documentation and reporting.

## Templates Overview

### Security Vulnerability Report

**File**: [security-report.md](security-report.md)

Complete vulnerability report template for documenting security findings:
- **Executive Summary** - Non-technical overview for stakeholders
- **Vulnerability Details** - Technical description, CVSS scoring, affected systems
- **Proof of Concept** - Exploitation steps and evidence
- **Business Impact** - Risk assessment and potential damage
- **Remediation Steps** - Step-by-step fixes with code examples
- **Timeline** - Discovery, notification, patch, verification
- **References** - CVEs, OWASP, compliance mapping

**Use when**: Documenting security findings from audits, pentests, or internal discovery

---

### Penetration Testing Report

**File**: [penetration-test.md](penetration-test.md)

Comprehensive penetration testing documentation template:
- **Scope & Methodology** - Testing boundaries, rules of engagement
- **Executive Summary** - High-level findings for management
- **Testing Methodology** - OWASP Testing Guide, tools used
- **Findings Summary** - Critical/High/Medium/Low vulnerability counts
- **Detailed Findings** - Each vulnerability with PoC and remediation
- **Risk Assessment** - CVSS scoring and business impact
- **Remediation Roadmap** - Prioritized action plan with deadlines
- **Appendix** - Tool outputs, screenshots, raw scan data

**Use when**: Conducting penetration tests, security audits, or compliance assessments

---

## Quick Usage

```bash
# Copy template to project
cp templates/security-report.md ../reports/vuln-2025-001.md

# Fill in sections
vim ../reports/vuln-2025-001.md

# Submit for review
git add ../reports/vuln-2025-001.md
git commit -m "docs: add SQL injection vulnerability report"
```

## Template Conventions

**Date Format**: YYYY-MM-DD (ISO 8601)
**CVSS Format**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
**Severity Ratings**: Critical (9.0-10.0), High (7.0-8.9), Medium (4.0-6.9), Low (0.1-3.9)
**Code Blocks**: Use triple backticks with language specifier (```typescript, ```python)

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Real vulnerability examples
- **Reference**: [Reference Index](../reference/INDEX.md) - OWASP, CVSS, compliance guides
- **Main Agent**: [security-analyzer.md](../security-analyzer.md) - Security analyzer agent

---

Return to [main agent](../security-analyzer.md)
