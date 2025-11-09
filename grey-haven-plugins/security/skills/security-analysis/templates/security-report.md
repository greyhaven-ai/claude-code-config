# Security Vulnerability Report

**Report ID**: VULN-YYYY-###
**Date**: YYYY-MM-DD
**Severity**: [Critical | High | Medium | Low]
**CVSS Score**: X.X
**Status**: [Open | In Progress | Resolved | Verified]
**Reporter**: [Name or Team]

---

## Executive Summary

**For non-technical stakeholders**

_Brief description of the vulnerability in business terms (2-3 sentences). Focus on impact to users, data, or business operations._

**Example**:
> A critical SQL injection vulnerability was discovered in the user search endpoint that allows attackers to extract all customer data from the database, including names, emails, and payment information. This vulnerability affects all users of the application and could result in a significant data breach if exploited.

---

## Vulnerability Details

### Description

_Technical description of the vulnerability. What is broken and why?_

**Affected Systems**:
- Component: [API endpoint, database, authentication system, etc.]
- Version: [Software version number]
- URL/Location: [https://api.greyhaven.io/users/search]
- Environment: [Production | Staging | Development]

**Attack Vector**: [Network | Adjacent | Local | Physical]

**OWASP Category**: [A03:2021 - Injection]

### CVSS v3.1 Scoring

**Vector String**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`

| Metric | Value | Justification |
|--------|-------|---------------|
| Attack Vector (AV) | [N/A/L/P] | _How is it exploited?_ |
| Attack Complexity (AC) | [L/H] | _Difficulty of exploitation_ |
| Privileges Required (PR) | [N/L/H] | _Authentication needed?_ |
| User Interaction (UI) | [N/R] | _Victim must act?_ |
| Scope (S) | [U/C] | _Affects other components?_ |
| Confidentiality (C) | [H/L/N] | _Data disclosure?_ |
| Integrity (I) | [H/L/N] | _Data modification?_ |
| Availability (A) | [H/L/N] | _Service disruption?_ |

**Base Score**: X.X ([Critical | High | Medium | Low])

---

## Proof of Concept

### Exploitation Steps

1. **Step 1**: _Description_
   ```bash
   # Command or code
   ```

2. **Step 2**: _Description_
   ```bash
   # Command or code
   ```

3. **Step 3**: _Description_
   ```bash
   # Expected result
   ```

### Evidence

_Screenshots, logs, or output demonstrating successful exploitation_

```
[Paste actual output or attach screenshot]
```

### Affected Code

**File**: `path/to/vulnerable/file.ts`
**Lines**: 42-58

```typescript
// Vulnerable code snippet
export async function searchUsers(query: string) {
  // ❌ VULNERABLE: String concatenation in SQL query
  const sql = `SELECT * FROM users WHERE username LIKE '%${query}%'`;
  return await db.query(sql);
}
```

---

## Business Impact

### Risk Assessment

**Likelihood**: [High | Medium | Low]
- _How likely is exploitation in the wild?_

**Impact**: [Critical | High | Medium | Low]
- _What is the worst-case outcome?_

**Overall Risk**: [Critical | High | Medium | Low]
- _Likelihood × Impact_

### Potential Consequences

- **Data Breach**: _Description of data exposure (e.g., 500K user records)_
- **Financial Loss**: _Estimated monetary impact (e.g., $500K in GDPR fines)_
- **Reputational Damage**: _Impact on brand trust_
- **Regulatory Compliance**: _Which regulations violated (GDPR, PCI DSS)_

### Affected Users

- **User Count**: [X users affected]
- **User Types**: [All users | Admin users | Specific tenant]
- **Geographic Scope**: [Global | EU | US only]

---

## Remediation

### Immediate Mitigation (Temporary Fix)

**Timeline**: Implement within [X hours]

_Quick workaround to reduce risk while developing permanent fix_

**Steps**:
1. _Temporary mitigation step 1_
2. _Temporary mitigation step 2_

**Code Example** (if applicable):
```typescript
// Temporary workaround
export async function searchUsers(query: string) {
  // ✅ TEMPORARY: Input validation regex
  if (!/^[a-zA-Z0-9_-]+$/.test(query)) {
    throw new Error('Invalid query');
  }
  const sql = `SELECT * FROM users WHERE username LIKE '%${query}%'`;
  return await db.query(sql);
}
```

### Permanent Fix

**Timeline**: Deploy within [X days]

_Complete solution that eliminates the vulnerability_

**Steps**:
1. _Implementation step 1_
2. _Implementation step 2_
3. _Testing step_
4. _Deployment step_

**Code Example**:
```typescript
// ✅ SECURE: Parameterized query with Drizzle ORM
import { eq, like } from 'drizzle-orm';

export async function searchUsers(query: string) {
  // ✅ Input validation
  if (query.length > 100) {
    throw new Error('Query too long');
  }

  // ✅ Parameterized query (SQL injection safe)
  return await db.query.users.findMany({
    where: like(users.username, `%${query}%`)
  });
}
```

### Testing & Verification

**Test Cases**:
- [ ] Normal input: `alice` → Returns matching users
- [ ] Malicious input: `'; DROP TABLE users--` → Rejected/escaped
- [ ] SQL injection attempt: `' OR '1'='1` → No unauthorized access
- [ ] Automated test: `bun test security/sql-injection.test.ts`

**Verification Steps**:
1. Deploy fix to staging
2. Run penetration test suite
3. Verify vulnerability no longer exploitable
4. Code review by security team
5. Deploy to production
6. Monitor for 48 hours

---

## Timeline

| Date | Event | Responsible |
|------|-------|-------------|
| YYYY-MM-DD | Vulnerability discovered | [Name] |
| YYYY-MM-DD | Security team notified | [Name] |
| YYYY-MM-DD | Initial assessment completed | Security Team |
| YYYY-MM-DD | Temporary mitigation deployed | DevOps |
| YYYY-MM-DD | Permanent fix developed | Engineering |
| YYYY-MM-DD | Fix deployed to production | DevOps |
| YYYY-MM-DD | Vulnerability verified fixed | Security Team |
| YYYY-MM-DD | Report published (if public) | Security Team |

---

## References

### CVE/CWE

- **CVE**: [CVE-YYYY-XXXXX] (if assigned)
- **CWE**: [CWE-89: SQL Injection]
- **OWASP**: [A03:2021 - Injection]

### Documentation

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Drizzle ORM Security Documentation](https://orm.drizzle.team/)
- Internal: [Security Best Practices](../reference/owasp-top-10.md)

### Similar Incidents

- _Link to similar vulnerabilities in your organization_
- _External references to similar attacks (if applicable)_

---

## Compliance Mapping

**Affected Compliance Requirements**:
- [ ] **PCI DSS 4.0**: Requirement 6.2 (Secure Development)
- [ ] **GDPR**: Article 32 (Security of Processing)
- [ ] **SOC 2**: CC6.1 (Logical Access Controls)

---

## Lessons Learned

### Root Cause Analysis

_What caused this vulnerability to exist?_

**Example**:
> The vulnerability was introduced in commit abc123 when developers implemented user search without using the ORM. Code review did not catch the SQL injection vulnerability because security review was not part of the PR checklist.

### Prevention Measures

_How can we prevent this class of vulnerabilities in the future?_

- [ ] Add SQL injection test cases to CI/CD
- [ ] Enforce Drizzle ORM usage (eslint rule)
- [ ] Security training on parameterized queries
- [ ] Mandatory security review for database changes
- [ ] Run `bun audit` and `bandit` in CI/CD

---

## Sign-Off

**Reported by**: _______________________ Date: ___________

**Verified by**: _______________________ Date: ___________

**Approved for Closure**: _______________________ Date: ___________

---

**Template Version**: 1.0.0
**Last Updated**: 2025-01-06
