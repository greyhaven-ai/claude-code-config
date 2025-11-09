# Security Review Report

**Project**: [Project Name]
**Version**: [Version/Commit Hash]
**Review Date**: [Date]
**Analyst**: [Analyst Name]
**Review Type**: Security Assessment
**Status**: [Draft | In Review | Final]

---

## Executive Summary

**Overall Security Score**: [X]/100

**Risk Level**: [🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low]

**Total Vulnerabilities Found**: [X]
- 🔴 Critical (P0): [X] - Fix immediately
- 🟠 High (P1): [X] - Fix before deployment
- 🟡 Medium (P2): [X] - Fix soon
- 🟢 Low (P3): [X] - Fix when convenient

**Recommendation**: [Do not deploy | Address critical issues | Ready for production]

**Key Findings**:
1. [Brief description of most critical vulnerability]
2. [Second most critical finding]
3. [Third most critical finding]

---

## Scope

**Files Reviewed**: [X] files, [Y] lines of code

**Components Analyzed**:
- [ ] Authentication and authorization
- [ ] Data validation and sanitization
- [ ] Cryptography implementation
- [ ] Session management
- [ ] API security
- [ ] Database security
- [ ] Third-party dependencies
- [ ] Configuration and secrets management

**Out of Scope**:
- [List items not covered in this review]

---

## OWASP Top 10 Assessment

### A01: Broken Access Control

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A02: Cryptographic Failures

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A03: Injection

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A04: Insecure Design

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A05: Security Misconfiguration

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A06: Vulnerable and Outdated Components

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A07: Identification and Authentication Failures

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A08: Software and Data Integrity Failures

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A09: Security Logging and Monitoring Failures

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

### A10: Server-Side Request Forgery (SSRF)

**Status**: [✅ Pass | ⚠️ Issues Found | 🔴 Critical Issues]

**Findings**:
- [List specific findings or "No issues found"]

---

## Detailed Findings

### 🔴 Critical (P0) - Fix Immediately

#### VULN-001: [Vulnerability Title]

**Severity**: 🔴 Critical
**CWE**: [CWE-XXX]
**CVSS Score**: [X.X]

**Location**:
- File: `[file path]`
- Lines: [X-Y]

**Description**:
[Detailed description of the vulnerability]

**Impact**:
[What could happen if exploited - data breach, unauthorized access, etc.]

**Proof of Concept**:
```python
# Example exploit code or attack vector
```

**Remediation**:
```python
# Before (vulnerable)
[vulnerable code]

# After (fixed)
[secure code]
```

**Estimated Fix Time**: [X hours/days]
**Status**: [⏳ To Do | 🔄 In Progress | ✅ Fixed]

---

#### VULN-002: [Next Critical Vulnerability]

[Repeat structure above]

---

### 🟠 High (P1) - Fix Before Deployment

#### VULN-003: [High Priority Vulnerability]

[Same structure as critical vulnerabilities]

---

### 🟡 Medium (P2) - Fix Soon

#### VULN-004: [Medium Priority Vulnerability]

[Same structure]

---

### 🟢 Low (P3) - Fix When Convenient

#### VULN-005: [Low Priority Vulnerability]

[Same structure]

---

## Security Scorecard

```
Category                        Score    Issues    Status
-----------------------------------------------------------
Input Validation                [X]/100  [X]       [✅/⚠️/🔴]
Authentication & Authorization  [X]/100  [X]       [✅/⚠️/🔴]
Cryptography                    [X]/100  [X]       [✅/⚠️/🔴]
Data Protection                 [X]/100  [X]       [✅/⚠️/🔴]
Session Management              [X]/100  [X]       [✅/⚠️/🔴]
API Security                    [X]/100  [X]       [✅/⚠️/🔴]
Dependency Security             [X]/100  [X]       [✅/⚠️/🔴]
Configuration                   [X]/100  [X]       [✅/⚠️/🔴]
-----------------------------------------------------------
Overall Security Score          [X]/100  [Total]   [Status]
```

**Scoring Criteria**:
- 90-100: Excellent security posture
- 75-89: Good, minor improvements needed
- 60-74: Fair, several issues to address
- 40-59: Poor, significant security gaps
- <40: Critical, major security overhaul required

---

## Automated Scan Results

### Bandit (Python Security Scanner)

```bash
# Command run
bandit -r app/ -f json -o bandit-report.json

# Summary
Total Issues: [X]
- High Severity: [X]
- Medium Severity: [X]
- Low Severity: [X]
```

### npm audit (JavaScript Dependency Scanner)

```bash
# Command run
npm audit --json

# Summary
Total Vulnerabilities: [X]
- Critical: [X]
- High: [X]
- Moderate: [X]
- Low: [X]
```

### Semgrep (Multi-language Security Scanner)

```bash
# Command run
semgrep --config auto app/

# Summary
Total Findings: [X]
- By Severity: Critical [X], High [X], Medium [X]
- By Category: Injection [X], XSS [X], Auth [X]
```

---

## Dependencies Analysis

**Total Dependencies**: [X]
**Known Vulnerabilities**: [X]

**Critical Dependency Issues**:
| Package | Version | Vulnerability | CVSS | Fix Version | Status |
|---------|---------|---------------|------|-------------|--------|
| [pkg]   | [ver]   | [CVE-XXXX]    | [X.X]| [ver]       | [status]|
| ...     | ...     | ...           | ...  | ...         | ...     |

---

## Recommendations

### Immediate Actions (P0)
1. [Critical fix #1]
2. [Critical fix #2]
3. [Critical fix #3]

### Short-term (P1)
1. [High priority improvement #1]
2. [High priority improvement #2]

### Medium-term (P2)
1. [Medium priority improvement #1]
2. [Medium priority improvement #2]

### Long-term Improvements
1. [Architectural security improvement]
2. [Process improvement]
3. [Training recommendation]

---

## Prevention Measures

### Pre-commit Hooks
```bash
# Install security hooks
pip install pre-commit bandit
pre-commit install

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    hooks:
      - id: bandit
        args: ['-ll']  # Only show high/medium severity
```

### CI/CD Security Gates
```yaml
# .github/workflows/security.yml
- name: Security scan
  run: |
    bandit -r app/ -ll --exit-zero
    safety check --json
    # Fail if critical vulnerabilities found
```

### Regular Security Reviews
- [ ] Monthly automated dependency scans
- [ ] Quarterly manual security reviews
- [ ] Annual penetration testing
- [ ] Security training for developers

---

## Compliance

**Standards Assessed**:
- [ ] OWASP Top 10 (2021)
- [ ] CWE Top 25
- [ ] PCI DSS (if applicable)
- [ ] GDPR (if applicable)
- [ ] HIPAA (if applicable)

**Compliance Status**: [Compliant | Non-compliant | Partially compliant]

**Non-compliance Items**:
1. [Standard requirement not met]
2. [Another requirement not met]

---

## Remediation Plan

### Week 1 (Critical Fixes)
- [ ] VULN-001: [Description] - Assigned to: [Name] - Due: [Date]
- [ ] VULN-002: [Description] - Assigned to: [Name] - Due: [Date]
- [ ] VULN-003: [Description] - Assigned to: [Name] - Due: [Date]

### Week 2 (High Priority)
- [ ] VULN-004: [Description] - Assigned to: [Name] - Due: [Date]
- [ ] VULN-005: [Description] - Assigned to: [Name] - Due: [Date]

### Week 3-4 (Medium Priority)
- [ ] VULN-006: [Description] - Assigned to: [Name] - Due: [Date]
- [ ] VULN-007: [Description] - Assigned to: [Name] - Due: [Date]

**Re-assessment Date**: [Date - 2 weeks after fixes complete]

---

## Appendix

### Testing Methodology
[Describe how testing was conducted]

### Tools Used
- Bandit v[X.X.X] - Python security scanner
- Safety v[X.X.X] - Python dependency checker
- npm audit v[X.X.X] - JavaScript dependency checker
- Semgrep v[X.X.X] - Multi-language security scanner
- Manual code review

### References
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE Database: https://cwe.mitre.org/
- CVSS Calculator: https://www.first.org/cvss/calculator/

### Reviewer Information
**Name**: [Analyst Name]
**Role**: [Security Engineer/Consultant]
**Contact**: [Email]
**Date**: [Date]

---

**Approval**:
- [ ] Security Team: ________________ Date: ________
- [ ] Engineering Lead: ________________ Date: ________
- [ ] Product Owner: ________________ Date: ________

---

Related: [Clarity Report Template](clarity-report-template.md) | [Synthesis Report Template](synthesis-report-template.md) | [Complete Audit Template](complete-audit-report-template.md)
