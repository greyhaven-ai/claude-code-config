# CVSS v3.1 Vulnerability Scoring Reference

Complete guide to Common Vulnerability Scoring System (CVSS) v3.1 for accurate vulnerability assessment and prioritization.

## Overview

**CVSS v3.1**: Industry-standard vulnerability severity scoring
**Range**: 0.0 (None) to 10.0 (Critical)
**Purpose**: Consistent vulnerability risk communication across organizations

## Severity Ratings

| Score Range | Rating | Example |
|-------------|--------|---------|
| **9.0 - 10.0** | Critical | Remote code execution without authentication |
| **7.0 - 8.9** | High | Authentication bypass, SQL injection |
| **4.0 - 6.9** | Medium | XSS, information disclosure |
| **0.1 - 3.9** | Low | Timing attacks, minor information leaks |
| **0.0** | None | No security impact |

## Base Metrics

### Attack Vector (AV)

**Question**: How is the vulnerability exploited?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **Network** | N | Remotely exploitable | Public API vulnerable to SQL injection |
| **Adjacent** | A | Local network required | WiFi attack, ARP spoofing |
| **Local** | L | Local access required | Privilege escalation on same machine |
| **Physical** | P | Physical access required | USB attack, hardware tampering |

**Impact on Score**: N (worst) > A > L > P (best)

### Attack Complexity (AC)

**Question**: How difficult is exploitation?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **Low** | L | Minimal skill, automated exploit | Public exploit code available |
| **High** | H | Requires expertise, specific conditions | Race condition, timing-dependent |

**Impact on Score**: L (worst) > H (best)

### Privileges Required (PR)

**Question**: What privileges does attacker need?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **None** | N | No authentication required | Anonymous access to vulnerable endpoint |
| **Low** | L | Basic user account needed | Authenticated user exploits privilege escalation |
| **High** | H | Admin/privileged account needed | Admin-only feature with vulnerability |

**Impact on Score**: N (worst) > L > H (best)

### User Interaction (UI)

**Question**: Does attack require victim action?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **None** | N | Fully automated | Server-side vulnerability exploited remotely |
| **Required** | R | Victim must take action | Phishing, XSS requiring user to click link |

**Impact on Score**: N (worst) > R (best)

### Scope (S)

**Question**: Does vulnerability affect other components?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **Unchanged** | U | Affects only vulnerable component | SQL injection in application database |
| **Changed** | C | Affects other components/systems | SSRF accessing cloud metadata, container escape |

**Impact on Score**: C (worst) > U (best)

### Confidentiality Impact (C)

**Question**: How much data is disclosed?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **High** | H | Total data disclosure | Database dump, all user records exposed |
| **Low** | L | Limited data disclosure | Single record exposed |
| **None** | N | No data disclosure | DoS attack with no data leak |

**Impact on Score**: H (worst) > L > N (best)

### Integrity Impact (I)

**Question**: Can attacker modify data?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **High** | H | Arbitrary data modification | SQL injection with UPDATE/DELETE |
| **Low** | L | Limited data modification | Modify own user profile |
| **None** | N | No data modification | Read-only vulnerability |

**Impact on Score**: H (worst) > L > N (best)

### Availability Impact (A)

**Question**: Can attacker cause service disruption?

| Value | Code | Description | Example |
|-------|------|-------------|---------|
| **High** | H | Complete service denial | DROP TABLE, crash application |
| **Low** | L | Degraded performance | Resource exhaustion, slowdown |
| **None** | N | No availability impact | Information disclosure only |

**Impact on Score**: H (worst) > L > N (best)

## CVSS Vector Strings

### Format

```
CVSS:3.1/AV:X/AC:X/PR:X/UI:X/S:X/C:X/I:X/A:X
```

### Real-World Examples

#### SQL Injection (Critical 9.8)

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```

**Breakdown**:
- AV:N - Network exploitable (remote API)
- AC:L - Simple to exploit (union-based SQL injection)
- PR:N - No authentication required
- UI:N - No user interaction
- S:U - Affects only database
- C:H - Full database disclosure
- I:H - Database modification (UPDATE/DELETE)
- A:H - Can DROP tables

#### XSS - Stored (High 7.1)

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N
```

**Breakdown**:
- AV:N - Network exploitable (public website)
- AC:L - Easy to inject payload
- PR:N - No authentication
- UI:R - Victim must view page
- S:C - Affects other users (changed scope)
- C:H - Session cookie theft
- I:L - Limited modification (user actions only)
- A:N - No availability impact

#### Authentication Bypass (High 8.1)

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```

**Breakdown**:
- AV:N - Network exploitable
- AC:L - Simple bypass (JWT algorithm confusion)
- PR:N - No credentials needed
- UI:N - Automated
- S:U - Unchanged scope
- C:H - Full account access
- I:H - Account modification
- A:H - Account lockout possible

#### Secrets in Git (Critical 9.1)

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N
```

**Breakdown**:
- AV:N - Public GitHub repository
- AC:L - Simple grep/trufflehog scan
- PR:N - Public access
- UI:N - Automated scanning
- S:U - Affects single application
- C:H - All secrets exposed
- I:H - Database/API modification
- A:N - Doesn't affect availability

#### SSRF to AWS Metadata (Medium 6.5)

```
CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N
```

**Breakdown**:
- AV:N - Network exploitable
- AC:L - Simple URL manipulation
- PR:L - Authenticated user required
- UI:N - No interaction
- S:U - Unchanged
- C:H - AWS credentials exposed
- I:N - Read-only
- A:N - No availability impact

## Calculating CVSS Scores

### Step 1: Assess Base Metrics

Answer each question for the vulnerability:
1. Attack Vector: How is it exploited? (N/A/L/P)
2. Attack Complexity: How difficult? (L/H)
3. Privileges Required: What access needed? (N/L/H)
4. User Interaction: Does victim act? (N/R)
5. Scope: Affects other components? (U/C)
6. Confidentiality Impact: Data disclosed? (H/L/N)
7. Integrity Impact: Data modified? (H/L/N)
8. Availability Impact: Service disrupted? (H/L/N)

### Step 2: Use CVSS Calculator

**Online Calculator**: https://www.first.org/cvss/calculator/3.1

**Manual Calculation** (complex formulas):
```
BaseScore = RoundUp(
  if (Impact == 0) then 0
  else if (Scope == Unchanged) then min(10, (Impact + Exploitability))
  else min(10, 1.08 × (Impact + Exploitability))
)
```

### Step 3: Interpret Score

- **Critical (9.0-10.0)**: Patch immediately, emergency deployment
- **High (7.0-8.9)**: Patch within 7 days
- **Medium (4.0-6.9)**: Patch within 30 days
- **Low (0.1-3.9)**: Patch in next release cycle

## Real CVE Examples

### CVE-2021-44228 (Log4Shell) - CVSS 10.0

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
```

**Why Critical**:
- Remote code execution
- No authentication
- Scope changed (affects entire infrastructure)
- Full impact (C:H, I:H, A:H)

### CVE-2021-3749 (axios SSRF) - CVSS 7.5

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N
```

**Why High**:
- Network exploitable SSRF
- No authentication
- High confidentiality impact (AWS metadata)
- No integrity/availability impact

### CVE-2020-28500 (lodash Prototype Pollution) - CVSS 5.3

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N
```

**Why Medium**:
- Low integrity impact
- Requires specific exploitation conditions
- Limited practical impact

## Temporal Metrics (Optional)

### Exploit Code Maturity (E)

| Value | Code | Description |
|-------|------|-------------|
| Not Defined | X | Skip temporal metrics |
| High | H | Public exploit code widely available |
| Functional | F | Exploit code exists but not reliable |
| Proof-of-Concept | P | PoC only, not weaponized |
| Unproven | U | No public exploit |

### Remediation Level (RL)

| Value | Code | Description |
|-------|------|-------------|
| Not Defined | X | Skip |
| Official Fix | O | Vendor patch available |
| Temporary Fix | T | Workaround available |
| Workaround | W | Unofficial mitigation |
| Unavailable | U | No fix available |

### Report Confidence (RC)

| Value | Code | Description |
|-------|------|-------------|
| Not Defined | X | Skip |
| Confirmed | C | Vendor confirmed |
| Reasonable | R | Independently verified |
| Unknown | U | Unconfirmed |

## Grey Haven Severity Thresholds

### Deployment Gates

```yaml
# CI/CD security gate
security-scan:
  thresholds:
    critical: 0    # Block deployment if any critical
    high: 2        # Allow max 2 high severity
    medium: 10     # Allow max 10 medium severity
    low: unlimited # No limit on low severity
```

### SLA Response Times

| Severity | Response Time | Patch Deadline |
|----------|---------------|----------------|
| **Critical** | 4 hours | 24 hours |
| **High** | 24 hours | 7 days |
| **Medium** | 3 days | 30 days |
| **Low** | 7 days | Next release |

## Prioritization Matrix

### Vulnerability Priority

```
Priority = CVSS Score × Exposure Factor × Business Impact

Exposure Factor:
- Internet-facing: 1.5x
- Internal-only: 1.0x
- Admin-only: 0.7x

Business Impact:
- Payment processing: 2.0x
- User data: 1.5x
- Public website: 1.0x
- Internal tools: 0.8x
```

### Example Calculation

```
SQL Injection in payment API:
- CVSS: 9.8
- Exposure: Internet-facing (1.5x)
- Impact: Payment processing (2.0x)
- Priority = 9.8 × 1.5 × 2.0 = 29.4 (CRITICAL)

XSS in admin panel:
- CVSS: 7.1
- Exposure: Admin-only (0.7x)
- Impact: Internal tools (0.8x)
- Priority = 7.1 × 0.7 × 0.8 = 3.98 (MEDIUM)
```

## Summary

**CVSS v3.1 Components**:
1. **Base Metrics** (required): AV, AC, PR, UI, S, C, I, A
2. **Temporal Metrics** (optional): E, RL, RC
3. **Environmental Metrics** (optional): Modified Base Metrics

**Grey Haven Practice**:
- Use CVSS for all vulnerability reports
- Include vector string in security documentation
- Block deployments with Critical (9.0+) vulnerabilities
- Prioritize based on CVSS × Exposure × Impact

---

**Related**: [OWASP Top 10](owasp-top-10.md) | [Compliance Requirements](compliance-requirements.md) | **Index**: [Reference Index](INDEX.md)
