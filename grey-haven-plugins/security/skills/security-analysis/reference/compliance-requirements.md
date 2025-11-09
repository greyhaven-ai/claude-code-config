# Security Compliance Requirements Reference

Comprehensive guide to security compliance frameworks for Grey Haven SaaS applications (PCI DSS, GDPR, SOC 2, HIPAA).

## Overview

**Grey Haven Compliance Posture**: Multi-tenant SaaS with payment processing
**Required Frameworks**: PCI DSS 4.0 (Stripe), GDPR (EU users), SOC 2 Type II
**Optional**: HIPAA (if healthcare data), ISO 27001 (enterprise sales)

## PCI DSS 4.0 - Payment Card Industry Data Security Standard

**Applies to**: Applications processing credit card payments via Stripe

### Requirements Mapping to Grey Haven

#### Requirement 1: Install and Maintain Network Security Controls

```typescript
// ✅ Cloudflare Workers enforces HTTPS
export default {
  async fetch(request: Request) {
    // Automatic HTTPS enforcement via Cloudflare
    if (request.url.startsWith('http://')) {
      return Response.redirect(request.url.replace('http://', 'https://'), 301);
    }
  }
};

// ✅ Firewall rules via Cloudflare WAF
// Block common attacks, rate limiting, DDoS protection
```

**Controls**:
- HTTPS only (TLS 1.3)
- Cloudflare WAF enabled
- No direct database access from internet

#### Requirement 2: Apply Secure Configurations

```typescript
// ✅ Security headers
response.headers.set('Strict-Transport-Security', 'max-age=31536000');
response.headers.set('X-Content-Type-Options', 'nosniff');
response.headers.set('X-Frame-Options', 'DENY');
```

**Controls**:
- Default deny security model
- Remove default accounts (no test/admin)
- Security headers on all responses

#### Requirement 3: Protect Stored Account Data

**Grey Haven Approach**: **Never store card data** (Stripe handles all PCI data)

```typescript
// ✅ SECURE: Use Stripe Payment Intents
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export const createPayment = createServerFn({ method: 'POST' })
  .handler(async ({ data }) => {
    // ✅ Create payment intent (card data stays at Stripe)
    const paymentIntent = await stripe.paymentIntents.create({
      amount: data.amount,
      currency: 'usd',
      customer: data.stripeCustomerId,
      // ❌ NEVER: cardNumber, cvv, expiry (PCI scope reduction)
    });

    // Store only Stripe IDs, not card data
    await db.insert(payments).values({
      id: crypto.randomUUID(),
      stripe_payment_intent_id: paymentIntent.id,  // ✅ Reference only
      amount: data.amount,
      tenant_id: data.tenantId
    });
  });
```

**Controls**:
- Zero card data storage (PCI SAQ A-EP)
- Store only Stripe customer/payment IDs
- Masked display (last 4 digits from Stripe)

#### Requirement 4: Protect Cardholder Data with Strong Cryptography

**N/A** - No card data storage (handled by Stripe)

#### Requirement 5: Protect All Systems and Networks from Malicious Software

```bash
# ✅ Snyk vulnerability scanning
snyk test
snyk monitor

# ✅ Dependabot security updates
# .github/dependabot.yml enabled
```

**Controls**:
- bun audit weekly
- Snyk monitoring
- Cloudflare virus scanning (for file uploads)

#### Requirement 6: Develop and Maintain Secure Systems and Software

```typescript
// ✅ Secure SDLC
// 1. Code review required (GitHub branch protection)
// 2. Security testing in CI/CD
// 3. SAST/DAST scanning

// .github/workflows/security.yml
- name: Security Scan
  run: |
    bun audit
    gitleaks detect
    eslint --plugin security
```

**Controls**:
- Mandatory code review
- CI/CD security gates
- Penetration testing annually

#### Requirement 7: Restrict Access to System Components

```typescript
// ✅ Least privilege access
CREATE POLICY user_access ON sensitive_data
  USING (
    user_id = current_setting('app.user_id')::uuid
    AND tenant_id = current_setting('app.tenant_id')::uuid
  );
```

**Controls**:
- PostgreSQL RLS on all tables
- Role-based access control (RBAC)
- Multi-tenant isolation

#### Requirement 8: Identify Users and Authenticate Access

```typescript
// ✅ Strong authentication with better-auth
export const auth = betterAuth({
  emailAndPassword: {
    minPasswordLength: 12,  // ✅ PCI requires 12+ chars
  },
  plugins: [
    twoFactor({  // ✅ MFA for admin access
      issuer: "Grey Haven"
    })
  ],
  session: {
    expiresIn: 60 * 60 * 8  // ✅ 8 hour session timeout
  }
});
```

**Controls**:
- Unique user IDs
- MFA for administrative access
- Password complexity (12+ chars)
- Session timeout (8 hours)

#### Requirement 9: Restrict Physical Access

**N/A** - Cloudflare Workers (no physical servers)

#### Requirement 10: Log and Monitor All Access

```typescript
// ✅ Security event logging
logger.security({
  event: 'payment_created',
  user_id: session.user.id,
  tenant_id: session.user.tenantId,
  amount: payment.amount,
  stripe_payment_id: paymentIntent.id,
  ip: request.headers.get('CF-Connecting-IP'),
  timestamp: new Date().toISOString()
});
```

**Controls**:
- DataDog centralized logging
- 90-day log retention
- Daily log reviews (automated alerts)
- Tamper-evident logs

#### Requirement 11: Test Security of Systems

```bash
# ✅ Annual penetration testing
- External penetration test (Cobalt.io)
- Internal vulnerability scanning (Snyk)
- Quarterly ASV scans (if applicable)
```

**Controls**:
- Annual penetration test
- Quarterly vulnerability scans
- bun audit weekly

#### Requirement 12: Support Information Security

```markdown
# Grey Haven Security Policy

## Incident Response Plan
1. Detect: DataDog alerts
2. Contain: Revoke compromised keys, isolate affected tenants
3. Eradicate: Patch vulnerability
4. Recover: Restore from backups
5. Post-mortem: Document lessons learned

## Acceptable Use Policy
- Developers must use Doppler for secrets
- Never commit .env files
- Code review required for all changes
```

**Controls**:
- Documented security policies
- Incident response plan
- Security awareness training (annually)

### PCI DSS Compliance Checklist

- [ ] HTTPS enforced (Requirement 1, 4)
- [ ] No card data storage (Requirement 3)
- [ ] Strong authentication + MFA (Requirement 8)
- [ ] Security logging (Requirement 10)
- [ ] Annual penetration test (Requirement 11)
- [ ] bun audit weekly (Requirement 5, 6)
- [ ] Code review mandatory (Requirement 6)
- [ ] PostgreSQL RLS (Requirement 7)

## GDPR - General Data Protection Regulation

**Applies to**: EU/EEA users (includes UK post-Brexit)

### Article 25: Data Protection by Design

```typescript
// ✅ Minimal data collection
class UserCreateSchema(BaseModel):
    email: EmailStr  # ✅ Required for service
    username: str    # ✅ Required for service
    # ❌ DON'T collect: SSN, passport, unnecessary PII
```

**Controls**:
- Collect only necessary data
- Purpose limitation (state why data collected)
- Data minimization

### Article 32: Security of Processing

```typescript
// ✅ Encryption at rest (PostgreSQL)
ALTER DATABASE greyhaven SET ssl = on;

// ✅ Encryption in transit (HTTPS only)
// ✅ Argon2id password hashing
// ✅ Multi-tenant data isolation (RLS)
```

**Controls**:
- TLS 1.3 in transit
- AES-256 encryption at rest
- Argon2id password hashing
- PostgreSQL RLS for tenant isolation

### Article 15: Right of Access

```typescript
// ✅ Data export endpoint
export const exportUserData = createServerFn({ method: 'GET' })
  .handler(async ({ data }) => {
    const user = await getAuthenticatedUser();

    // Export all user data in JSON
    const userData = {
      profile: await getUserProfile(user.id),
      orders: await getUserOrders(user.id),
      payments: await getUserPayments(user.id)
    };

    return new Response(JSON.stringify(userData, null, 2), {
      headers: {
        'Content-Type': 'application/json',
        'Content-Disposition': 'attachment; filename="user-data.json"'
      }
    });
  });
```

**Controls**:
- User data export within 30 days
- Machine-readable format (JSON)
- Free of charge

### Article 17: Right to Erasure

```typescript
// ✅ Account deletion endpoint
export const deleteAccount = createServerFn({ method: 'DELETE' })
  .handler(async () => {
    const user = await getAuthenticatedUser();

    // ✅ Delete or anonymize all user data
    await db.transaction(async (tx) => {
      // Delete user account
      await tx.delete(users).where(eq(users.id, user.id));

      // Anonymize orders (retain for financial records)
      await tx.update(orders)
        .set({ user_email: 'deleted@example.com' })
        .where(eq(orders.user_id, user.id));

      // Delete sessions
      await redis.del(`session:${user.id}`);
    });
  });
```

**Controls**:
- Account deletion within 30 days
- Anonymize financial records (7-year retention)
- Cascade deletions (all related data)

### Article 33: Breach Notification

```typescript
// ✅ Breach notification procedure
async function notifyDataBreach(breach: {
  affectedUsers: number;
  dataTypes: string[];
  severity: 'low' | 'medium' | 'high';
}) {
  if (breach.severity === 'high') {
    // ✅ Notify supervisory authority within 72 hours
    await notifySupervisoryAuthority(breach);

    // ✅ Notify affected users
    await notifyAffectedUsers(breach);
  }

  // ✅ Document breach
  await logBreachIncident(breach);
}
```

**Controls**:
- Breach detection (DataDog alerts)
- 72-hour notification to supervisory authority
- User notification if high risk
- Breach register maintained

### GDPR Compliance Checklist

- [ ] Privacy policy published (Article 13)
- [ ] Consent for data collection (Article 6)
- [ ] Data export endpoint (Article 15)
- [ ] Account deletion endpoint (Article 17)
- [ ] Encryption at rest + in transit (Article 32)
- [ ] Breach notification process (Article 33)
- [ ] DPA with subprocessors (Article 28) - Stripe, Cloudflare, DataDog
- [ ] Multi-tenant isolation (Article 32)

## SOC 2 Type II - Trust Services Criteria

**Applies to**: B2B SaaS (enterprise customers)

### CC6.1: Logical Access Controls

```typescript
// ✅ RBAC implementation
enum UserRole {
  USER = 'user',
  ADMIN = 'admin',
  OWNER = 'owner'
}

function requireRole(role: UserRole) {
  return async (request: Request) => {
    const session = await auth.api.getSession({ headers: request.headers });

    if (!session || session.user.role < role) {
      throw new Error('Insufficient permissions');
    }
  };
}
```

**Controls**:
- Role-based access control
- Principle of least privilege
- Access reviews quarterly

### CC7.2: System Monitoring

```typescript
// ✅ Continuous monitoring
logger.monitor({
  metric: 'failed_logins',
  user_id: userId,
  ip: ipAddress,
  count: failedLoginCount
});

// Alert if > 5 failed logins
if (failedLoginCount > 5) {
  await alertSecurityTeam({
    type: 'brute_force_attempt',
    user_id: userId
  });
}
```

**Controls**:
- DataDog monitoring
- Security alerts (Slack, PagerDuty)
- Weekly log reviews

### CC8.1: Change Management

```yaml
# ✅ GitHub branch protection
branches:
  main:
    protection:
      required_pull_request_reviews: 2
      required_status_checks:
        - security-scan
        - tests
      enforce_admins: true
```

**Controls**:
- Code review mandatory
- CI/CD security gates
- Change log maintained

### SOC 2 Compliance Checklist

- [ ] Access controls (CC6.1)
- [ ] System monitoring (CC7.2)
- [ ] Change management (CC8.1)
- [ ] Encryption (CC6.7)
- [ ] Annual penetration test
- [ ] Vendor risk assessment (Stripe, Cloudflare)
- [ ] Business continuity plan

## Summary Table

| Framework | Scope | Key Requirements | Grey Haven Implementation |
|-----------|-------|------------------|---------------------------|
| **PCI DSS 4.0** | Payment processing | No card storage, encryption, logging | Stripe integration, Doppler secrets |
| **GDPR** | EU users | Data export, deletion, consent | Export/delete endpoints, RLS |
| **SOC 2** | B2B SaaS | Access controls, monitoring, change mgmt | RBAC, DataDog, GitHub protection |
| **HIPAA** | Healthcare data (optional) | BAA, encryption, audit logs | N/A unless handling PHI |

---

**Related**: [OWASP Top 10](owasp-top-10.md) | [CVSS Scoring](cvss-scoring.md) | **Index**: [Reference Index](INDEX.md)
