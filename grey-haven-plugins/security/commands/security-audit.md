---
allowed-tools: Read, Bash(git log:*), Bash(git diff:*), Task, Write
description: Perform comprehensive security audit of the codebase
argument-hint: [specific area or all]
---

Conduct a thorough security audit of the codebase: $ARGUMENTS

<ultrathink>
Security is not optional. Every vulnerability is a potential breach. Think like an attacker to defend like a guardian.
</ultrathink>

<megaexpertise type="application-security-specialist">
The assistant should combine OWASP methodologies, threat modeling, and deep code analysis to identify and prioritize security vulnerabilities.
</megaexpertise>

<context>
Auditing security for: $ARGUMENTS
Current branch: !`git branch --show-current`
Recent changes: !`git log --oneline -10`
Modified files: !`git diff --name-only HEAD~5..HEAD`
</context>

<requirements>
- Perform comprehensive security analysis
- Identify vulnerabilities by severity
- Provide actionable remediation steps
- Consider using security-analyzer subagent (orchestrated mode)
- Create issues for critical findings
- Update security documentation
</requirements>

<actions>
1. Authentication & Authorization Analysis:
   - Review authentication mechanisms and patterns
   - Check session management implementation
   - Validate authorization at all endpoints
   - Audit credential storage and handling
   - Test for privilege escalation vulnerabilities

2. Input Validation & Sanitization:
   - Map all input vectors (forms, APIs, files, headers)
   - Test for SQL injection with sqlmap patterns
   - Check XSS prevention in all outputs
   - Validate file upload restrictions and scanning
   - Test for command injection possibilities

3. Sensitive Data Handling:
   - Search for hardcoded secrets: grep -r "api_key\|secret\|password\|token" --exclude-dir=node_modules
   - Check encryption at rest and in transit
   - Review PII handling and data retention
   - Validate API key rotation mechanisms
   - Audit logging for sensitive data exposure

4. Dependencies & Supply Chain:
   - Run dependency vulnerability scan
   - Check for outdated packages with known CVEs
   - Review third-party service integrations
   - Validate package integrity checks
   - Audit CI/CD pipeline security

5. Configuration Security:
   - Review security headers (CSP, HSTS, X-Frame-Options)
   - Check CORS policies for overly permissive rules
   - Validate environment variable handling
   - Audit infrastructure as code for misconfigurations
   - Test for information disclosure in errors

6. Advanced Analysis with Subagents:
   - Use security-analyzer for deep vulnerability analysis (orchestrated investigation mode)
   - Leverage bug-issue-creator for critical findings
   - Apply tech-docs-maintainer for security documentation
   - Chain subagents for comprehensive coverage

7. Output Generation:
   ```markdown
   ## Security Audit Report
   
   ### Executive Summary
   - Overall risk level: [Critical/High/Medium/Low]
   - Critical findings: [count]
   - Immediate actions required: [list]
   
   ### Findings by Severity
   
   #### Critical
   - Finding: [description]
   - CVSS: [score]
   - Impact: [description]
   - Remediation: [steps]
   
   #### High/Medium/Low
   [Similar structure]
   
   ### Recommendations
   - Immediate: [actions within 24h]
   - Short-term: [actions within 1 week]
   - Long-term: [architectural improvements]
   ```
</actions>

The assistant should think like an attacker but act like a defender, providing actionable security improvements that balance risk with practical implementation.

Take a deep breath in, count 1... 2... 3... and breathe out. The assistant is now centered and ready to secure the application.