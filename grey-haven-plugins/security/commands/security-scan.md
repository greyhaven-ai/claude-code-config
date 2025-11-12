---
allowed-tools: Read, Grep, Bash, Write, Task, TodoWrite
description: Deep security scan following OWASP Top 10 with automated remediation
argument-hint: [directory or specific area to scan]
---
Perform security scan on: $ARGUMENTS
<ultrathink>
Security vulnerabilities are doors left open. Every line must be scrutinized. OWASP Top 10 guides our vigilance.
</ultrathink>
<megaexpertise type="security-specialist">
The assistant should leverage the security-analyzer subagent (in direct or orchestrated mode) to perform comprehensive vulnerability analysis with automated fixes where safe.
</megaexpertise>
<context>
Security scanning: $ARGUMENTS
Following OWASP Top 10 guidelines
Hooks will enhance detection and validation
</context>
<requirements>
- OWASP Top 10 vulnerability check
- Dependency vulnerability scan
- Secret/credential detection
- Security header validation
- Input validation audit
- Authentication/authorization review
- Automated safe remediations
- Detailed security report
</requirements>
<actions>
1. **Quick Security Sweep**:
 ```bash
# Scan for exposed secrets
 grep -r -E "(api[_-]?key|secret|password|token|private[_-]?key)" \
 --exclude-dir=node_modules --exclude-dir=.git \
 --exclude="*.md" $ARGUMENTS | head -20
# Check for hardcoded credentials
 grep -r -E "(postgres|redis)://[^/]*:[^@]*@" \
 --exclude-dir=node_modules $ARGUMENTS
# Find dangerous functions
 grep -r -E "(eval|exec|system|shell_exec|os\.system|subprocess\.call)" \
 --exclude-dir=node_modules $ARGUMENTS
 ```
2. **Dependency Vulnerability Check**:
 ```bash
# JavaScript/Node.js with bun
# Note: bun doesn't have built-in audit yet, use npm audit as fallback
 npm audit --audit-level=moderate 2>/dev/null || echo "Run 'npm audit' manually for security check"
# Python
 pip-audit 2>/dev/null || safety check 2>/dev/null
# Ruby
 bundle audit 2>/dev/null
# Check for outdated dependencies
 bun outdated 2>/dev/null || bunx npm-check-updates
 ```
3. **Invoke Security Subagents**:
 - Primary: security-analyzer subagent (direct analysis mode for quick scans)
 - Optional: security-analyzer subagent (orchestrated mode for comprehensive review)
 - Hook: security-validator provides real-time feedback
4. **OWASP Top 10 Systematic Check**:
 **A01:2021 - Broken Access Control**:
 - Check all routes for authentication
 - Verify authorization on data access
 - Look for IDOR vulnerabilities
 **A02:2021 - Cryptographic Failures**:
 - Identify weak hashing (MD5, SHA1)
 - Check for unencrypted sensitive data
 - Verify proper key management
 **A03:2021 - Injection**:
 - SQL injection patterns
 - NoSQL injection risks
 - Command injection points
 - XSS vulnerabilities
 **A04:2021 - Insecure Design**:
 - Review threat model
 - Check rate limiting
 - Validate business logic
 **A05:2021 - Security Misconfiguration**:
 - Check security headers
 - Review error handling
 - Validate CORS settings
5. **Automated Remediation**:
 ```javascript
 // Auto-fix: Add security headers
 if (!hasSecurityHeaders) {
 addHelmetMiddleware();
 }
 // Auto-fix: Parameterize queries
 // Before: "SELECT * FROM users WHERE id = " + userId
 // After: "SELECT * FROM users WHERE id = ?", [userId]
 // Auto-fix: Hash passwords properly
 // Before: MD5(password)
 // After: bcrypt.hash(password, 10)
 ```
6. **Security Score Calculation**:
 ```
 Score = 100 - (
 Critical * 20 +
 High * 10 +
 Medium * 5 +
 Low * 2
 )
 Minimum acceptable score: 70
 ```
7. **Generate Security Report**:
 ```markdown
## Security Scan Report
### Critical Vulnerabilities (Must Fix Immediately)
 1. **SQL Injection in auth.js:45**
 - Risk: Database compromise
 - Fix: Use parameterized queries
 - Status: SUCCESS: Auto-fixed
### WARNING: High Priority Issues
 1. **Weak Password Hashing**
 - Location: user-model.js:23
 - Current: MD5
 - Recommended: bcrypt/argon2
 - Status: WARNING: Manual review needed
### OWASP Top 10 Compliance
 - A01 Access Control: SUCCESS: Pass
 - A02 Cryptography: WARNING: Issues found
 - A03 Injection: ERROR: Critical issues
 - A04 Design: SUCCESS: Pass
 - A05 Misconfiguration: WARNING: Issues found
 - A06 Vulnerable Components: SUCCESS: Pass
 - A07 Authentication: SUCCESS: Pass
 - A08 Data Integrity: SUCCESS: Pass
 - A09 Logging: WARNING: Improvements needed
 - A10 SSRF: SUCCESS: Pass
### Security Score: 75/100
### Dependency Vulnerabilities
 - Critical: 0
 - High: 2 (lodash@4.17.15, axios@0.21.0)
 - Medium: 5
 - Low: 12
### Remediation Priority
 1. Update vulnerable dependencies
 2. Fix SQL injection vulnerabilities
 3. Implement proper password hashing
 4. Add security headers
 5. Enable audit logging
### Automated Fixes Applied
 - SUCCESS: Added Helmet.js security headers
 - SUCCESS: Parameterized 3 SQL queries
 - SUCCESS: Added input validation to 5 endpoints
 - SUCCESS: Enabled CSRF protection
### Manual Actions Required
 - [ ] Review and merge security fixes
 - [ ] Update password hashing algorithm
 - [ ] Implement rate limiting
 - [ ] Add security monitoring
 ```
8. **Hook Integration Benefits**:
 - **security-validator hook**: Real-time vulnerability detection
 - **dependency-checker hook**: Continuous dependency monitoring
 - **secret-scanner hook**: Prevents credential commits
 - **post-edit-validator hook**: Ensures security standards
9. **Create Security Checklist**:
 ```bash
# Generate security checklist
 cat > SECURITY_CHECKLIST.md << 'EOF'
## Pre-Deployment Security Checklist
 - [ ] All critical vulnerabilities fixed
 - [ ] Dependencies updated
 - [ ] Security headers configured
 - [ ] Authentication tested
 - [ ] Authorization verified
 - [ ] Input validation complete
 - [ ] Secrets removed from code
 - [ ] Security scan score > 80
 EOF
 ```
</actions>
The assistant should treat security as non-negotiable, leveraging subagents and hooks to create multiple layers of defense against vulnerabilities.