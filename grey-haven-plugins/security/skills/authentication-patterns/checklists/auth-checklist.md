# Authentication Security Checklist

**Use before deploying authentication features.**

## Configuration Security

- [ ] BETTER_AUTH_SECRET stored in Doppler (never committed)
- [ ] OAuth secrets in Doppler (Google, GitHub, etc.)
- [ ] BETTER_AUTH_URL matches production domain
- [ ] trustedOrigins configured correctly
- [ ] Session expiry configured (7 days default)

## Database Security

- [ ] tenant_id included in users table
- [ ] tenant_id included in sessions table
- [ ] RLS policies created for users table
- [ ] RLS policies created for sessions table
- [ ] Email addresses unique constraint
- [ ] Passwords never stored in plain text (better-auth handles)

## Multi-Tenant Isolation

- [ ] tenant_id extracted from JWT claims
- [ ] All auth queries filter by tenant_id
- [ ] Session data includes tenant context
- [ ] Test cases verify tenant isolation

## Email Verification

- [ ] Email verification required for signup
- [ ] Verification tokens expire (15 minutes)
- [ ] Verification tokens single-use
- [ ] Email templates styled (Resend/SendGrid)

## OAuth Configuration

- [ ] OAuth redirect URLs whitelisted
- [ ] OAuth scopes minimal (email, profile only)
- [ ] OAuth secrets in Doppler
- [ ] OAuth callback URLs HTTPS only

## Session Management

- [ ] Redis/Upstash configured for sessions
- [ ] Session tokens stored securely (httpOnly cookies)
- [ ] Session refresh configured (1 day)
- [ ] Session expiry configured (7 days)

## Protected Routes

- [ ] beforeLoad checks authentication
- [ ] Redirects to login with return URL
- [ ] Session data available in route context
- [ ] Logout clears session completely

## Testing

- [ ] Signup flow tested
- [ ] Login flow tested
- [ ] Logout tested
- [ ] Email verification tested
- [ ] OAuth flow tested (if enabled)
- [ ] Magic link tested (if enabled)
- [ ] Passkey tested (if enabled)
- [ ] Multi-tenant isolation tested
