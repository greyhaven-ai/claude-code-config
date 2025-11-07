# Security Vulnerability Examples

Real-world vulnerability examples with exploitation scenarios, CVSS scores, and complete remediations.

## Examples Overview

### SQL Injection (A03)
**File**: [sql-injection.md](sql-injection.md)

Critical database security vulnerabilities:
- SQL injection attack scenarios
- Blind SQL injection techniques
- Parameterized query solutions
- ORM best practices
- Input validation patterns
- CVSS 9.8 (Critical) examples

**Use when**: Building database queries, API endpoints with user input, search functionality.

---

### Cross-Site Scripting - XSS (A03)
**File**: [xss-vulnerabilities.md](xss-vulnerabilities.md)

XSS attack vectors and prevention:
- Reflected XSS exploitation
- Stored XSS persistence attacks
- DOM-based XSS scenarios
- Output encoding solutions
- Content Security Policy (CSP)
- CVSS 7.1 (High) examples

**Use when**: Rendering user-generated content, building search features, dynamic HTML generation.

---

### Authentication Bypass (A07)
**File**: [authentication-bypass.md](authentication-bypass.md)

Authentication and session security flaws:
- JWT algorithm confusion attacks
- Session fixation exploitation
- Weak password policies
- Missing MFA vulnerabilities
- Secure authentication implementation
- CVSS 8.1 (High) examples

**Use when**: Implementing login systems, session management, API authentication, OAuth flows.

---

### Secrets Exposure (A02)
**File**: [secrets-exposure.md](secrets-exposure.md)

Hardcoded credentials and secret management:
- API key exposure detection
- Hardcoded password patterns
- Environment variable best practices
- Doppler/Vault integration
- Git secret scanning
- CVSS 9.1 (Critical) examples

**Use when**: Managing configuration, deploying applications, working with third-party APIs.

---

### Dependency Vulnerabilities (A06)
**File**: [dependency-vulnerabilities.md](dependency-vulnerabilities.md)

Supply chain and dependency security:
- Known CVE exploitation
- Outdated package detection
- npm audit / pip-audit usage
- Dependency update strategies
- Lock file security
- CVSS varies by CVE

**Use when**: Adding dependencies, updating packages, conducting security audits.

---

## OWASP Top 10 Coverage

| Vulnerability | Example File | CVSS Range | Frequency |
|---------------|--------------|------------|-----------|
| **A01: Broken Access Control** | (Covered in auth-bypass) | 6.5-8.8 | Very High |
| **A02: Cryptographic Failures** | secrets-exposure.md | 7.5-9.8 | High |
| **A03: Injection** | sql-injection.md, xss-vulnerabilities.md | 7.3-9.8 | High |
| **A04: Insecure Design** | (Threat modeling reference) | Varies | Medium |
| **A05: Security Misconfiguration** | (Reference docs) | 5.3-7.5 | High |
| **A06: Vulnerable Components** | dependency-vulnerabilities.md | 4.0-10.0 | Very High |
| **A07: Auth Failures** | authentication-bypass.md | 6.5-9.1 | High |
| **A08: Data Integrity** | (Reference docs) | 7.5-8.8 | Medium |
| **A09: Logging Failures** | (Reference docs) | 5.3-6.5 | Medium |
| **A10: SSRF** | (Reference docs) | 6.4-9.6 | Medium |

## Severity Guide

- **Critical (9.0-10.0)**: Immediate exploitation, severe impact
- **High (7.0-8.9)**: Easy exploitation, significant impact
- **Medium (4.0-6.9)**: Moderate difficulty, limited impact
- **Low (0.1-3.9)**: Difficult exploitation, minimal impact

## Navigation

- **Reference**: [Reference Index](../reference/INDEX.md)
- **Templates**: [Templates Index](../templates/INDEX.md)
- **Main Agent**: [security-analyzer.md](../security-analyzer.md)

---

Return to [main agent](../security-analyzer.md)
