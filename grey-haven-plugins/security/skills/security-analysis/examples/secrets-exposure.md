# Secrets Exposure Vulnerability Examples

Real-world hardcoded credentials and secret management vulnerabilities with exploitation details, CVSS scoring, and complete remediation using Grey Haven stack (Doppler, FastAPI, Cloudflare Workers).

## Overview

**OWASP Category**: A02:2021 - Cryptographic Failures
**CVSS v3.1 Score**: 9.1 (Critical)
**Impact**: Complete infrastructure compromise, database access, API abuse, financial loss

## Vulnerability Pattern 1: Hardcoded API Keys

### Vulnerable Code

```python
# app/config.py - VULNERABLE
DATABASE_URL = "postgresql://admin:SuperSecret123@db.greyhaven.io:5432/prod"
STRIPE_SECRET_KEY = "sk_live_51HqR2wKX9vZ3yN8cP4hT5"  # ❌ Production key in code
OPENAI_API_KEY = "sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
JWT_SECRET = "my-secret-key-12345"  # ❌ Weak and hardcoded
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# app/lib/email.py - VULNERABLE
from sendgrid import SendGridAPIClient

sg = SendGridAPIClient(api_key='SG.abc123xyz')  # ❌ Hardcoded in source
```

### Exploitation

```bash
# Step 1: Find secrets in public GitHub repo
git clone https://github.com/company/app
grep -r "sk_live" .
grep -r "postgresql://" .
grep -r "AKIA" .  # AWS access key pattern

# Step 2: Use exposed credentials
export STRIPE_SECRET_KEY="sk_live_51HqR2wKX9vZ3yN8cP4hT5"
stripe charges create --amount=100000 --currency=usd  # Charge $1000

psql "postgresql://admin:SuperSecret123@db.greyhaven.io:5432/prod"
# DROP TABLE users;  # Complete database access

# Step 3: Automated scanning
trufflehog git https://github.com/company/app --only-verified
# Finds: 14 verified secrets (Stripe, AWS, DB, OpenAI)
```

**Impact Metrics**:
- **Financial Loss**: $50K+ in fraudulent Stripe charges
- **Data Breach**: Complete database dump (500K user records)
- **API Abuse**: $10K OpenAI API charges in 24 hours
- **AWS Takeover**: Attacker spins up 100 EC2 instances
- **Total Damage**: $500K+ (fraud + remediation + fines)

### Secure Implementation (Doppler)

```typescript
// app/lib/config.ts - SECURE
import { Redis } from '@upstash/redis';

// ✅ All secrets from Doppler (never in code)
export const config = {
  database: {
    url: process.env.DATABASE_URL!,  // From Doppler
    // postgres://user:REDACTED@host:5432/db
  },

  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY!,
    publishableKey: process.env.STRIPE_PUBLISHABLE_KEY!
  },

  openai: {
    apiKey: process.env.OPENAI_API_KEY!
  },

  jwt: {
    secret: process.env.JWT_SECRET!,  // 256-bit from Doppler
    expiresIn: '15m'
  },

  aws: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
    region: process.env.AWS_REGION!
  },

  redis: {
    url: process.env.REDIS_URL!,
    token: process.env.REDIS_TOKEN!
  }
};

// ✅ Validate all required secrets at startup
const requiredSecrets = [
  'DATABASE_URL',
  'STRIPE_SECRET_KEY',
  'OPENAI_API_KEY',
  'JWT_SECRET',
  'REDIS_URL'
];

for (const secret of requiredSecrets) {
  if (!process.env[secret]) {
    throw new Error(`Missing required secret: ${secret}`);
  }
}
```

**Doppler Setup**:
```bash
# Install Doppler CLI
brew install dopplerhq/cli/doppler

# Login and setup
doppler login
doppler setup

# Inject secrets into environment
doppler run -- bun dev  # Development
doppler run --config prd -- bun start  # Production

# Cloudflare Workers deployment
doppler secrets download --config prd --format env > .env
wrangler secret bulk .env
rm .env  # Never commit
```

**Security Improvements**:
1. **Doppler Secrets Manager**: Centralized secret storage
2. **Environment Variables**: No secrets in code
3. **Secret Rotation**: Rotate via Doppler dashboard
4. **Access Control**: Team-based permissions
5. **Audit Logging**: Track all secret access

## Vulnerability Pattern 2: Secrets in Git History

### Vulnerable Scenario

```bash
# Developer accidentally commits .env file
git add .env
git commit -m "Add environment configuration"
git push origin main

# Later removes it
git rm .env
git commit -m "Remove .env file"
git push origin main

# ❌ Secret still in git history
git log --all --full-history -- .env
git show abc123:.env
# Reveals: DATABASE_URL, API_KEYS, etc.
```

**Impact**: Secrets remain in git history forever, public GitHub repos expose to millions

### Secure Implementation

```bash
# .gitignore - ALWAYS ignore secrets
.env
.env.*
!.env.example
*.key
*.pem
secrets/
credentials.json

# Pre-commit hook for secret detection
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached --name-only | grep -E '\.env$|\.key$|credentials'; then
  echo "ERROR: Attempting to commit secret files"
  exit 1
fi

# Scan for patterns
if git diff --cached | grep -E 'sk_live_|AKIA|password.*=.*["\']'; then
  echo "ERROR: Potential secret in commit"
  exit 1
fi

# Use gitleaks for comprehensive scanning
gitleaks protect --staged

# If secrets already committed, rewrite history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: destructive)
git push origin --force --all
git push origin --force --tags

# Rotate all exposed secrets immediately
```

## Vulnerability Pattern 3: Client-Side Secret Exposure

### Vulnerable Code (React/TanStack)

```tsx
// app/routes/api-test.tsx - VULNERABLE
export function ApiTestPage() {
  const [result, setResult] = useState('');

  async function testAPI() {
    // ❌ CRITICAL: API key exposed in browser
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      headers: {
        'Authorization': `Bearer sk-proj-AbCdEf123456`,  // ❌ Visible in DevTools
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ model: 'gpt-4', messages: [...] })
    });
  }

  return <button onClick={testAPI}>Test API</button>;
}

// ❌ Built JavaScript contains secret
// bundle.js: ...Authorization: "Bearer sk-proj-AbCdEf123456"...
```

**Exploitation**:
```bash
# View page source
curl https://app.greyhaven.io/api-test | grep -o 'sk-proj-[^"]*'

# Or inspect Network tab in DevTools
# Result: OpenAI API key visible to all users
```

**Impact**: Any visitor can extract API key, $10K+ API abuse

### Secure Implementation

```tsx
// app/routes/api-test.tsx - SECURE
import { createServerFn } from '@tanstack/start';

// ✅ Server-side function with Doppler secrets
export const callOpenAI = createServerFn({ method: 'POST' })
  .handler(async ({ data }: { data: { prompt: string } }) => {
    // ✅ API key only accessible on server
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,  // ✅ Server-side only
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [{ role: 'user', content: data.prompt }]
      })
    });

    return await response.json();
  });

// ✅ Client-side component (no secrets)
export function ApiTestPage() {
  const [result, setResult] = useState('');

  async function testAPI() {
    // ✅ Calls server function (secrets never leave server)
    const data = await callOpenAI({ data: { prompt: 'Hello' } });
    setResult(data.content);
  }

  return <button onClick={testAPI}>Test API</button>;
}
```

## Vulnerability Pattern 4: Secrets in Logs

### Vulnerable Code

```python
# app/api/users.py - VULNERABLE
import logging

@router.post("/login")
async def login(username: str, password: str):
    # ❌ CRITICAL: Password logged
    logging.info(f"Login attempt: {username} with password {password}")

    user = verify_credentials(username, password)
    if user:
        token = create_token(user.id)
        # ❌ Token logged
        logging.info(f"Generated token: {token}")
        return {"token": token}
```

**Impact**: Credentials in CloudWatch/DataDog logs, accessible to all developers

### Secure Implementation

```python
# app/api/users.py - SECURE
import logging
import re

def sanitize_log(message: str) -> str:
    """Remove sensitive data from logs."""
    # Redact JWT tokens
    message = re.sub(r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*', '[REDACTED_TOKEN]', message)
    # Redact API keys
    message = re.sub(r'sk-[a-zA-Z0-9]{20,}', '[REDACTED_API_KEY]', message)
    # Redact passwords
    message = re.sub(r'password["\s:=]+[^\s"]+', 'password=[REDACTED]', message, flags=re.IGNORECASE)
    return message

@router.post("/login")
async def login(credentials: LoginRequest):
    # ✅ Never log passwords
    logging.info(f"Login attempt: {credentials.username}")

    user = verify_credentials(credentials.username, credentials.password)
    if user:
        token = create_token(user.id)
        # ✅ Log token prefix only
        logging.info(f"Token generated: {token[:10]}...")
        return {"token": token}
```

## CVSS v3.1 Scoring

**Base Score: 9.1 (Critical)** - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`

| Metric | Value | Reasoning |
|--------|-------|-----------|
| Attack Vector | Network | GitHub public repos accessible globally |
| Attack Complexity | Low | Simple grep/trufflehog scans |
| Privileges Required | None | Public repositories |
| User Interaction | None | Automated scanning |
| Confidentiality | High | All secrets exposed |
| Integrity | High | Database/API modification |
| Availability | None | Doesn't affect availability |

## Prevention Checklist

- [ ] **Use Doppler** for all secrets management
- [ ] **Never commit .env files** to git
- [ ] **Add .env to .gitignore** immediately
- [ ] **Use pre-commit hooks** (gitleaks)
- [ ] **Server-side API calls** only (TanStack server functions)
- [ ] **Sanitize logs** (no passwords, tokens, keys)
- [ ] **Rotate secrets** quarterly
- [ ] **Monitor secret access** with Doppler audit logs
- [ ] **Scan git history** with trufflehog
- [ ] **Use .env.example** for documentation

## Testing for Secret Exposure

```bash
# Scan codebase for hardcoded secrets
gitleaks detect --source . --verbose

# Scan git history
trufflehog git file://. --only-verified

# Check for common patterns
grep -r "password.*=" . --include="*.py" --include="*.ts"
grep -r "api_key.*=" . --include="*.py" --include="*.ts"
grep -r "sk_live_" .
grep -r "AKIA" .

# Verify .env in .gitignore
git check-ignore .env || echo "WARNING: .env not ignored"

# Check if secrets in environment (not code)
grep -r "process.env" . --include="*.ts" | wc -l  # Should be > 0
grep -r "sk_live" . --include="*.ts" | wc -l      # Should be 0
```

## Real-World Impact

**Case Study: 2023 Uber Breach**
- **Vulnerability**: Hardcoded credentials in GitHub
- **Attack**: Attacker found AWS keys in public repo
- **Impact**: 57M user records stolen, $148M FTC fine
- **Remediation**: 6 months, complete credential rotation
- **Prevention**: Doppler + gitleaks pre-commit hooks

## Summary

| Secret Type | Risk | Detection | Prevention |
|-------------|------|-----------|------------|
| **Hardcoded API Keys** | Critical | gitleaks | Doppler |
| **Git History Secrets** | Critical | trufflehog | .gitignore + hooks |
| **Client-Side Secrets** | High | Code review | Server functions |
| **Secrets in Logs** | Medium | Log analysis | Sanitization |

**Key Takeaway**: Use Doppler for ALL secrets, add .env to .gitignore, scan with gitleaks/trufflehog, and NEVER put secrets in client-side code.

---

**Next**: [Dependency Vulnerabilities](dependency-vulnerabilities.md) | **Previous**: [Authentication Bypass](authentication-bypass.md) | **Index**: [Examples Index](INDEX.md)
