# Security Reference Documentation

Comprehensive security reference materials for the Grey Haven security analyzer agent.

## Reference Guides Overview

### OWASP Top 10 2021

**File**: [owasp-top-10.md](owasp-top-10.md)

Complete OWASP Top 10 coverage for Grey Haven stack:
- **A01: Broken Access Control** - Multi-tenant RLS, authorization patterns
- **A02: Cryptographic Failures** - Secrets management, encryption, hashing
- **A03: Injection** - SQL injection, XSS, command injection prevention
- **A04: Insecure Design** - Threat modeling, secure architecture patterns
- **A05: Security Misconfiguration** - Cloudflare Workers, environment hardening
- **A06: Vulnerable Components** - Dependency scanning, update strategies
- **A07: Authentication Failures** - better-auth, MFA, session management
- **A08: Software & Data Integrity** - Checksum validation, CI/CD security
- **A09: Logging & Monitoring Failures** - Security event logging, SIEM integration
- **A10: Server-Side Request Forgery** - SSRF prevention, URL validation

**Use when**: Understanding OWASP categories, mapping vulnerabilities to standards

---

### CVSS v3.1 Scoring Reference

**File**: [cvss-scoring.md](cvss-scoring.md)

Complete CVSS vulnerability scoring methodology:
- **Base Metrics**: AV, AC, PR, UI, S, C, I, A
- **Temporal Metrics**: Exploit Code Maturity, Remediation Level, Report Confidence
- **Environmental Metrics**: Modified Base Metrics for specific environments
- **Severity Ranges**: Critical (9.0-10.0), High (7.0-8.9), Medium (4.0-6.9), Low (0.1-3.9)
- **Vector Strings**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- **Calculator**: Step-by-step scoring examples
- **Real CVEs**: Mapping actual vulnerabilities to CVSS scores

**Use when**: Scoring vulnerabilities, prioritizing remediation, reporting severity

---

### Compliance Requirements

**File**: [compliance-requirements.md](compliance-requirements.md)

Security compliance frameworks for SaaS:
- **PCI DSS 4.0**: Payment card data security (Stripe integration)
- **GDPR**: EU data privacy requirements (multi-tenant data isolation)
- **HIPAA**: Healthcare data protection (if applicable)
- **SOC 2 Type II**: Trust services criteria (security, availability, confidentiality)
- **ISO 27001**: Information security management
- **NIST Cybersecurity Framework**: Security controls mapping
- **Grey Haven Specific**: Cloudflare Workers compliance, PostgreSQL encryption

**Use when**: Preparing for audits, implementing compliance controls, documenting security posture

---

### Security Tools Reference

**File**: [security-tools.md](security-tools.md)

Complete tooling guide for Grey Haven stack:
- **SAST**: Bandit (Python), ESLint security plugins (TypeScript)
- **Dependency Scanning**: bun audit, pip-audit, Snyk, Dependabot
- **Secret Scanning**: gitleaks, trufflehog, Doppler audit logs
- **Container Security**: (if using Docker)
- **Cloud Security**: Cloudflare WAF, rate limiting, DDoS protection
- **Database Security**: PostgreSQL RLS, query auditing, encryption at rest
- **Penetration Testing**: Burp Suite, OWASP ZAP, SQLMap
- **Monitoring**: DataDog Security Monitoring, Sentry error tracking

**Use when**: Selecting security tools, configuring CI/CD security gates, penetration testing

---

## Quick Navigation

| Topic | File | Lines | Purpose |
|-------|------|-------|---------|
| **OWASP Top 10** | [owasp-top-10.md](owasp-top-10.md) | ~450 | Security categories |
| **CVSS Scoring** | [cvss-scoring.md](cvss-scoring.md) | ~380 | Vulnerability scoring |
| **Compliance** | [compliance-requirements.md](compliance-requirements.md) | ~420 | Audit requirements |
| **Security Tools** | [security-tools.md](security-tools.md) | ~350 | Tool configuration |

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Vulnerability examples with exploitation
- **Templates**: [Templates Index](../templates/INDEX.md) - Security report templates
- **Main Agent**: [security-analyzer.md](../security-analyzer.md) - Agent documentation

---

Return to [main agent](../security-analyzer.md)
