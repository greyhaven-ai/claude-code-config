# Security Tools Reference

Comprehensive security tooling guide for Grey Haven stack (TanStack Start, FastAPI, Cloudflare Workers, PostgreSQL).

## Static Application Security Testing (SAST)

### ESLint Security Plugin (TypeScript/JavaScript)

```bash
# Install
bun add -D eslint-plugin-security

# .eslintrc.js
module.exports = {
  plugins: ['security'],
  extends: ['plugin:security/recommended'],
  rules: {
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-regexp': 'error',
    'security/detect-unsafe-regex': 'error',
    'security/detect-eval-with-expression': 'error',
    'security/detect-no-csrf-before-method-override': 'error'
  }
};

# Run in CI/CD
bun run eslint . --ext .ts,.tsx
```

**Detects**:
- eval() usage
- Unsafe regex (ReDoS)
- Object injection vulnerabilities
- Non-literal require()

### Bandit (Python)

```bash
# Install
pip install bandit

# Run on FastAPI code
bandit -r app/ -f json -o bandit-report.json

# Configuration: .bandit
[bandit]
exclude_dirs = ['/tests', '/migrations']
tests = ['B201', 'B301', 'B302', 'B303', 'B304', 'B305', 'B306']
```

**Detects**:
- SQL injection (raw queries)
- Hardcoded passwords
- assert used for security checks
- Unsafe YAML/pickle loading

## Dependency Scanning

### bun audit (JavaScript/TypeScript)

```bash
# Scan dependencies
bun audit

# Fix automatically
bun update --latest

# CI/CD integration
bun audit --audit-level=moderate  # Fail on moderate+

# Output JSON for parsing
bun audit --json > audit-report.json
```

**Scans**:
- npm packages
- Transitive dependencies
- Known CVEs from npm advisory database

### pip-audit (Python)

```bash
# Install
pip install pip-audit

# Scan requirements.txt
pip-audit

# Fix automatically
pip-audit --fix

# CI/CD integration
pip-audit --requirement requirements.txt --format json
```

**Scans**:
- PyPI packages
- CVEs from OSV and PyPI databases

### Snyk (Comprehensive)

```bash
# Install
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor project continuously
snyk monitor

# Fix vulnerabilities automatically
snyk fix

# Container scanning (if applicable)
snyk container test grey-haven:latest

# Infrastructure as Code scanning
snyk iac test
```

**Features**:
- Real-time vulnerability database
- Automated PR fixes (Snyk Bot)
- License compliance checking
- Container vulnerability scanning

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
    commit-message:
      prefix: "chore"
      include: "scope"

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Features**:
- Automated security updates
- Version bump PRs
- Grouped dependency updates
- Custom PR reviewers

## Secret Scanning

### gitleaks

```bash
# Install
brew install gitleaks

# Scan entire repository
gitleaks detect --source . --verbose

# Scan specific commit
gitleaks detect --log-opts="HEAD~1..HEAD"

# Pre-commit hook
gitleaks protect --staged

# CI/CD integration
gitleaks detect --source . --report-format json --report-path gitleaks-report.json
```

**Configuration**: `.gitleaks.toml`
```toml
[extend]
useDefault = true

[[rules]]
id = "doppler-token"
description = "Doppler API token"
regex = '''dp\.pt\.[a-zA-Z0-9]{40}'''
```

**Detects**:
- AWS keys (AKIA...)
- Stripe keys (sk_live_...)
- Database connection strings
- JWT tokens
- API keys

### trufflehog

```bash
# Install
brew install trufflehog

# Scan git history
trufflehog git file://. --only-verified

# Scan GitHub repo
trufflehog github --repo https://github.com/greyhaven/app

# Scan S3 bucket
trufflehog s3 --bucket greyhaven-backups

# CI/CD integration
trufflehog filesystem . --json --fail
```

**Features**:
- Verified secrets (actually valid)
- S3, GitHub, filesystem scanning
- Entropy analysis for unknown secrets

### Doppler Secret Audit

```bash
# View audit logs
doppler audit

# Filter by action
doppler audit --action=secret.read

# Export for SIEM
doppler audit --json > doppler-audit.json
```

**Tracks**:
- Secret access
- Secret modifications
- Team member changes
- Failed authentication attempts

## Penetration Testing Tools

### OWASP ZAP (Dynamic Scanning)

```bash
# Docker-based scan
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://app.greyhaven.io \
  -r zap-report.html

# API scanning
zap-api-scan.py -t https://api.greyhaven.io/openapi.json -f openapi

# Authenticated scan
zap-full-scan.py -t https://app.greyhaven.io \
  -U admin@greyhaven.io \
  -P $PASSWORD
```

**Tests**:
- SQL injection
- XSS vulnerabilities
- CSRF
- Insecure authentication
- Security headers

### Burp Suite

**Setup**:
1. Configure browser proxy → localhost:8080
2. Import Burp CA certificate
3. Browse application to build sitemap
4. Run active/passive scans

**Features**:
- Intercepting proxy
- Active scanner
- Repeater (manual testing)
- Intruder (brute force)
- Extensions (JSON Web Tokens, SQLMap)

### sqlmap (SQL Injection)

```bash
# Test for SQL injection
sqlmap -u "https://api.greyhaven.io/users?search=test" \
  --cookie="session=abc123" \
  --batch \
  --level=3

# Dump database
sqlmap -u "https://api.greyhaven.io/users?search=test" \
  --cookie="session=abc123" \
  --dump-all

# Specify DBMS
sqlmap -u "https://api.greyhaven.io/users" \
  --dbms=postgresql \
  --technique=BEUSTQ
```

**Techniques**:
- Boolean-based blind
- Time-based blind
- Error-based
- UNION query-based
- Stacked queries

## Cloud Security

### Cloudflare WAF

**Configuration**: wrangler.toml with firewall rules (block geographic regions, rate limiting, WAF rules)

**Features**: DDoS protection, rate limiting (5 req/sec), bot protection, custom WAF rules

### Cloudflare Zero Trust

**Features**: Zero Trust access, identity-based rules, audit logging, device posture checks

## Database Security

### PostgreSQL Audit Logging

```sql
-- Enable audit logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;

-- Reload configuration
SELECT pg_reload_conf();

-- Query audit logs
SELECT * FROM pg_stat_statements
WHERE query LIKE '%users%'
ORDER BY total_exec_time DESC;
```

**Logs**:
- All SQL statements
- Connection attempts
- Failed authentication
- Query execution time

### pgAudit Extension

```sql
-- Install
CREATE EXTENSION pgaudit;

-- Configure
ALTER SYSTEM SET pgaudit.log = 'write, ddl';
ALTER SYSTEM SET pgaudit.log_catalog = off;

-- Audit specific role
ALTER ROLE app_user SET pgaudit.log = 'all';
```

## Monitoring & Alerting

### DataDog Security Monitoring

```typescript
// app/lib/logger.ts
import { datadogLogs } from '@datadog/browser-logs';

datadogLogs.init({
  clientToken: process.env.DATADOG_CLIENT_TOKEN!,
  site: 'datadoghq.com',
  forwardErrorsToLogs: true,
  sessionSampleRate: 100
});

// Log security events
datadogLogs.logger.info('login_attempt', {
  user_id: userId,
  success: true,
  ip: ipAddress,
  user_agent: userAgent
});

// Alert on suspicious activity
if (failedLogins > 5) {
  datadogLogs.logger.error('brute_force_attempt', {
    user_id: userId,
    ip: ipAddress,
    failed_count: failedLogins
  });
}
```

**Alerts**:
- Failed login spikes
- Privilege escalation attempts
- SQL injection patterns in logs
- Unusual API access patterns

### Sentry Error Tracking

```typescript
// app/lib/sentry.ts
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,

  // Filter sensitive data
  beforeSend(event) {
    // Remove passwords from breadcrumbs
    if (event.breadcrumbs) {
      event.breadcrumbs = event.breadcrumbs.filter(
        crumb => !crumb.message?.includes('password')
      );
    }
    return event;
  }
});
```

## CI/CD Security Gates

### GitHub Actions Security Pipeline

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [pull_request, push]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency audit
        run: bun audit --audit-level=moderate && pip-audit
      - name: Secret scanning
        run: gitleaks detect --source . --verbose
      - name: SAST
        run: bun run eslint . --ext .ts,.tsx && bandit -r app/
```

## Tool Comparison

| Category | Tool | Language | Integration | Cost |
|----------|------|----------|-------------|------|
| **SAST** | ESLint Security | TypeScript | GitHub Actions | Free |
| **SAST** | Bandit | Python | GitHub Actions | Free |
| **Dependency** | bun audit | JavaScript | Built-in | Free |
| **Dependency** | pip-audit | Python | CLI | Free |
| **Dependency** | Snyk | All | GitHub, CLI | Paid ($) |
| **Secret** | gitleaks | All | Pre-commit, CI | Free |
| **Secret** | trufflehog | All | CI/CD | Free |
| **DAST** | OWASP ZAP | Web | Docker | Free |
| **DAST** | Burp Suite | Web | Manual | Paid ($$) |
| **Monitoring** | DataDog | All | SDK | Paid ($$) |

## Recommended Security Stack

### Minimum (Free Tier)

```yaml
SAST: ESLint Security + Bandit
Dependency: bun audit + pip-audit
Secret: gitleaks pre-commit hook
DAST: OWASP ZAP baseline scan
Monitoring: Cloudflare Analytics + Sentry (free tier)
```

### Production (Enterprise)

```yaml
SAST: ESLint Security + Bandit
Dependency: Snyk (paid)
Secret: gitleaks + trufflehog + Doppler audit
DAST: Burp Suite Professional + OWASP ZAP
Penetration: Annual external pentest (Cobalt.io)
Monitoring: DataDog Security + Sentry Business
Compliance: Vanta (SOC 2 automation)
```

---

**Related**: [OWASP Top 10](owasp-top-10.md) | [CVSS Scoring](cvss-scoring.md) | [Compliance](compliance-requirements.md) | **Index**: [Reference Index](INDEX.md)
