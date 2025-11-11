# Prompt-Based Hooks: Implementation Examples

**Related Document**: `PROMPT_BASED_HOOKS_ANALYSIS.md`

This document provides ready-to-use configuration examples for implementing prompt-based hooks in the Grey Haven plugin ecosystem.

## Quick Start Guide

### Step 1: Backup Current Settings

```bash
cp .claude/settings.json .claude/settings.json.backup
```

### Step 2: Add Hook Configuration

Edit `.claude/settings.json` and add hooks to the `"hooks"` section.

### Step 3: Test Hook

Trigger the agent/action that should invoke the hook and verify behavior.

### Step 4: Monitor & Tune

Watch for false positives/negatives and adjust prompts accordingly.

## Phase 1: Critical Safety Hooks

### Example 1: Destructive Operation Validator

**Purpose**: Prevent accidental data loss or production modifications.

**File**: `.claude/settings.json`

```json
{
  "permissions": {
    "allow": [],
    "deny": [],
    "ask": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "name": "destructive-operation-validator",
        "description": "Prevents destructive operations without confirmation",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are a safety validation expert evaluating tool usage for potential destructive operations.\n\nAnalyze this tool use request:\n\nTool: $ARGUMENTS.toolName\nArguments: $ARGUMENTS.arguments\nFile path: $ARGUMENTS.filePath (if applicable)\nCurrent working directory: $ARGUMENTS.cwd\n\nEvaluate for these HIGH RISK patterns:\n\n1. **Git Force Operations**\n   - git push --force, git push -f\n   - Especially to main/master branches\n   - Decision: BLOCK with confirmation request\n\n2. **File/Directory Deletion**\n   - rm -rf, rmdir on critical directories\n   - Deletion of .git, node_modules, dist, build (OK)\n   - Deletion of src/, config/, production files (BLOCK)\n   - Decision: BLOCK for critical dirs, APPROVE for build artifacts\n\n3. **Database Operations**\n   - DROP DATABASE, TRUNCATE, DELETE without WHERE\n   - Production database connections\n   - Decision: BLOCK on production, APPROVE on dev/test\n\n4. **Production Environment**\n   - Modifications to files containing 'production', 'prod', 'prd'\n   - Changes to .env.production, config/production.*\n   - Deployment scripts\n   - Decision: BLOCK with explicit confirmation\n\n5. **Security Files**\n   - Deletion or disabling of auth/security code\n   - Changes to .github/workflows (CI/CD)\n   - Modifications to Dockerfile, docker-compose.yml\n   - Decision: APPROVE but add WARNING\n\n**Response Format**:\n\nFor HIGH RISK (force push to main, production changes, destructive DB ops):\n{\n  \"decision\": \"block\",\n  \"reason\": \"Destructive operation detected: [specific operation]\",\n  \"systemMessage\": \"⚠️ DESTRUCTIVE OPERATION\\n\\n[Operation details]\\n\\nThis operation could cause data loss or production issues.\\n\\nIf this is intentional, please:\\n1. [Specific mitigation steps]\\n2. Confirm by re-running with explicit flag\\n\\nOr modify your approach to avoid this risk.\"\n}\n\nFor MEDIUM RISK (security file changes, deployment configs):\n{\n  \"decision\": \"approve\",\n  \"systemMessage\": \"⚠️ CAUTION: Modifying [security/deployment] files. Ensure changes are reviewed.\"\n}\n\nFor LOW RISK (normal operations, build artifact cleanup):\n{\n  \"decision\": \"approve\"\n}\n\nNow evaluate the provided tool use request and respond with JSON only.",
            "timeout": 25
          }
        ],
        "toolNames": ["Bash", "Write", "Edit", "MultiEdit"]
      }
    ]
  }
}
```

**Test Cases**:

```bash
# Should BLOCK
git push --force origin main
rm -rf src/
DROP DATABASE production_db;

# Should WARN
# Editing .github/workflows/deploy.yml
# Editing Dockerfile

# Should APPROVE
rm -rf node_modules/
npm run build
pytest tests/
```

### Example 2: Security-Sensitive File Protection

**Purpose**: Require review for modifications to security-critical files.

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "security-file-protection",
        "description": "Protects security-critical files from unauthorized modification",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are a security file protection expert. Evaluate if this file modification affects security.\n\nFile path: $ARGUMENTS.filePath\nOperation: $ARGUMENTS.toolName\nChange type: [analyze from diff/content if available]\n\n**Security-Sensitive File Patterns**:\n\n1. **Authentication/Authorization**\n   - Patterns: **/auth*.{js,ts,py}, **/login*.{js,ts,py}, **/session*.{js,ts,py}\n   - Patterns: **/jwt*.{js,ts,py}, **/oauth*.{js,ts,py}, **/permission*.{js,ts,py}\n   - Risk: HIGH if disabling checks, MEDIUM if refactoring\n\n2. **Secrets/Configuration**\n   - Patterns: **/.env*, **/secrets*, **/credentials*, **/config/production*\n   - Patterns: **/keys/**, **/*.pem, **/*.key\n   - Risk: CRITICAL - should never be directly edited\n\n3. **Cryptography**\n   - Patterns: **/crypto*.{js,ts,py}, **/hash*.{js,ts,py}, **/encrypt*.{js,ts,py}\n   - Risk: HIGH if changing algorithms, MEDIUM if adding features\n\n4. **Infrastructure**\n   - Patterns: Dockerfile, docker-compose*.yml, **/*.k8s.yaml\n   - Patterns: .github/workflows/**, **/.circleci/**, **/.gitlab-ci.yml\n   - Risk: MEDIUM - changes affect deployment/security\n\n5. **Input Validation**\n   - Patterns: **/validation*.{js,ts,py}, **/sanitize*.{js,ts,py}\n   - Risk: HIGH if removing validation, LOW if adding\n\n**Change Type Detection**:\n\nAnalyze the intent (if code provided in $ARGUMENTS):\n- **DISABLING**: Commenting out, removing checks, disabling MFA\n- **WEAKENING**: Lowering requirements, reducing complexity, allowing bypass\n- **STRENGTHENING**: Adding checks, improving algorithms, fixing vulnerabilities\n- **REFACTORING**: Restructuring without changing security behavior\n- **ADDING**: New security features\n\n**Decision Logic**:\n\nCRITICAL RISK (secrets, credentials):\n{\n  \"decision\": \"block\",\n  \"reason\": \"Direct modification of secrets/credentials file detected\",\n  \"systemMessage\": \"🔒 SECURITY: Secrets files should not be directly edited.\\n\\nUse environment variables or secret management system instead.\\n\\nFile: [path]\\n\\nIf you must edit, use: vault edit [file]\"\n}\n\nHIGH RISK (disabling auth, weakening crypto):\n{\n  \"decision\": \"block\",\n  \"reason\": \"Security weakening detected in [file]\",\n  \"systemMessage\": \"🔒 SECURITY REVIEW REQUIRED\\n\\nChange type: [DISABLING/WEAKENING]\\nFile: [path]\\n\\nThis modification appears to reduce security.\\nRequired: Security team review\\n\\nTo proceed:\\n1. Create security review ticket\\n2. Get approval from security team\\n3. Document justification\"\n}\n\nMEDIUM RISK (refactoring, infrastructure):\n{\n  \"decision\": \"approve\",\n  \"systemMessage\": \"⚠️ Security-sensitive file modified: [path]\\n\\nChange type: [REFACTORING/INFRASTRUCTURE]\\n\\nReminders:\\n- Run security tests before merge\\n- Request security team review in PR\\n- Update security documentation if needed\"\n}\n\nLOW RISK (strengthening, adding features):\n{\n  \"decision\": \"approve\",\n  \"systemMessage\": \"✅ Security improvement detected in [path]. Good work!\"\n}\n\nNON-SECURITY (normal files):\n{\n  \"decision\": \"approve\"\n}\n\nNow evaluate the file modification and respond with JSON only.",
            "timeout": 25
          }
        ],
        "toolNames": ["Write", "Edit", "MultiEdit"],
        "filePatterns": [
          "**/auth*",
          "**/login*",
          "**/session*",
          "**/jwt*",
          "**/oauth*",
          "**/.env*",
          "**/secrets*",
          "**/credentials*",
          "**/crypto*",
          "**/validation*",
          "Dockerfile",
          "docker-compose*.yml",
          ".github/workflows/**"
        ]
      }
    ]
  }
}
```

**Test Cases**:

```javascript
// File: src/auth/login.js
// Should BLOCK
export function login(username, password) {
  // TODO: Skip password check for now
  // if (!validatePassword(password)) return false;
  return createSession(username);
}

// Should WARN
export function login(username, password) {
  // Refactored to use async/await
  return await validateAndCreateSession(username, password);
}

// Should APPROVE
export function login(username, password) {
  // Added MFA requirement
  if (!validatePassword(password)) return false;
  if (!verifyMFA(username)) return false;
  return createSession(username);
}
```

## Phase 2: Agent Quality Gate Hooks

### Example 3: TDD Orchestrator Completion Validator

**Purpose**: Ensure red-green-refactor cycle completed thoroughly.

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "name": "tdd-completion-validator",
        "description": "Validates TDD cycle completion before allowing agent to stop",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are a TDD methodology expert validating test-driven development cycle completion.\n\nAgent: $ARGUMENTS.agentName\nTask: $ARGUMENTS.taskDescription\nExecution summary: $ARGUMENTS.transcript (last 50 lines)\n\n**TDD Cycle Requirements**:\n\n**RED Phase (Failing Test)**:\n1. Did the agent write a failing test FIRST?\n2. Did the test fail for the RIGHT REASON? (not syntax error, not missing import)\n3. Are test assertions SPECIFIC and MEANINGFUL? (not just \"assert result is not None\")\n4. Is the test name DESCRIPTIVE? (test_user_login_with_valid_credentials)\n\n**GREEN Phase (Minimal Implementation)**:\n1. Did the agent implement MINIMAL code to make the test pass?\n2. Did the test actually PASS?\n3. Was over-engineering AVOIDED? (no premature optimization, no unnecessary features)\n\n**REFACTOR Phase (Code Improvement)**:\n1. Did the agent refactor for clarity/quality?\n2. Do all tests STILL PASS after refactoring?\n3. Was test coverage MAINTAINED or IMPROVED?\n\n**Coverage & Quality Gates**:\n1. Line coverage >= 80% ✅ or delta coverage = 100% ✅\n2. Branch coverage >= 75% ✅\n3. Critical path coverage = 100% (if applicable)\n4. Mutation score >= 85% (if mutation testing run)\n5. No test smells (brittle assertions, test interdependence)\n\n**Completion Checklist**:\n\n✅ All three phases completed (RED → GREEN → REFACTOR)\n✅ Coverage thresholds met\n✅ Tests are high quality (specific assertions, good naming)\n✅ No failing tests\n✅ Code quality maintained\n\n**Decision Logic**:\n\nBLOCK if:\n- RED phase skipped (test written after implementation)\n- Test didn't actually fail initially\n- Coverage below threshold (<80% line, <75% branch)\n- Tests failing\n- Critical path not covered\n\nAPPROVE if:\n- All three phases completed\n- Coverage meets or exceeds thresholds\n- Test quality is high\n- All tests passing\n\n**Response Format**:\n\nIncomplete cycle:\n{\n  \"decision\": \"block\",\n  \"reason\": \"TDD cycle incomplete\",\n  \"stopReason\": \"❌ TDD Cycle Incomplete\\n\\n[Specific missing items]\\n\\nRequired:\\n- [Action 1]\\n- [Action 2]\\n\\nCurrent coverage: XX% (target: 80%)\\nCurrent status: [phase] phase incomplete\"\n}\n\nComplete cycle:\n{\n  \"decision\": \"approve\",\n  \"reason\": \"TDD cycle complete with quality gates passed\",\n  \"systemMessage\": \"✅ TDD Cycle Complete\\n\\nRED: [test name] failed correctly\\nGREEN: Minimal implementation, test passes\\nREFACTOR: Code improved, tests still passing\\n\\nCoverage: XX% line, XX% branch ✅\\nMutation score: XX% ✅\\n\\nGreat work maintaining TDD discipline!\"\n}\n\nNow analyze the TDD cycle and respond with JSON only.",
            "timeout": 30
          }
        ],
        "agentNames": ["tdd-orchestrator", "tdd-python", "tdd-typescript"]
      }
    ]
  }
}
```

**Expected Behavior**:

When agent completes, hook evaluates the transcript:
- ✅ **Approves** if RED → GREEN → REFACTOR completed with coverage ≥80%
- ❌ **Blocks** if any phase skipped or coverage <80%

### Example 4: Security Analysis Completion Validator

**Purpose**: Ensure comprehensive OWASP Top 10 security audit.

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "name": "security-analysis-completion",
        "description": "Validates comprehensive security audit completion",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are a security audit expert validating analysis completeness.\n\nAgent: $ARGUMENTS.agentName\nScope: $ARGUMENTS.taskDescription\nFindings: $ARGUMENTS.transcript (security report)\n\n**OWASP Top 10 Coverage Checklist**:\n\nRequired Categories (must check ALL):\n\n1. ✅ A01: Broken Access Control\n   - IDOR vulnerabilities?\n   - Missing authorization checks?\n   - Privilege escalation paths?\n\n2. ✅ A02: Cryptographic Failures\n   - Weak algorithms (MD5, SHA1, DES)?\n   - Hardcoded secrets/keys?\n   - Insecure TLS configuration?\n\n3. ✅ A03: Injection\n   - SQL injection?\n   - XSS vulnerabilities?\n   - Command injection?\n\n4. ✅ A04: Insecure Design\n   - Missing rate limiting?\n   - Business logic flaws?\n   - Insufficient threat modeling?\n\n5. ✅ A05: Security Misconfiguration\n   - Default credentials?\n   - Verbose error messages?\n   - Missing security headers?\n\n6. ✅ A06: Vulnerable Components\n   - Outdated dependencies?\n   - Known CVEs?\n   - Supply chain risks?\n\n7. ✅ A07: Authentication Failures\n   - Weak password policies?\n   - Missing MFA?\n   - Session management issues?\n\n8. ✅ A08: Data Integrity Failures\n   - Insecure deserialization?\n   - Missing integrity checks?\n   - Unsigned updates?\n\n9. ✅ A09: Security Logging Failures\n   - Missing audit logs?\n   - Logging sensitive data?\n   - Insufficient monitoring?\n\n10. ✅ A10: Server-Side Request Forgery\n    - SSRF via user URLs?\n    - Internal service access?\n    - Cloud metadata exploitation?\n\n**Critical Findings Checklist**:\n\n✅ All Critical (CVSS 9.0+) vulnerabilities identified\n✅ Specific remediations provided for each finding\n✅ CVSS scores calculated\n✅ Exploit scenarios documented\n✅ Compliance mapping (PCI DSS, GDPR, etc. if applicable)\n\n**Secret Detection**:\n\n✅ Scanned for hardcoded credentials\n✅ Checked for API keys/tokens\n✅ Reviewed for private keys\n\n**Dependency Security**:\n\n✅ Ran dependency scanner (npm audit, pip-audit, etc.)\n✅ Identified vulnerable packages\n✅ Provided upgrade paths\n\n**Decision Logic**:\n\nBLOCK if:\n- Any OWASP category skipped (incomplete audit)\n- Critical vulnerabilities unresolved\n- No CVSS scores provided\n- Secrets detected but not addressed\n- Dependency scan not run\n\nAPPROVE if:\n- All 10 OWASP categories checked\n- Critical findings have remediations\n- CVSS scoring complete\n- Comprehensive report delivered\n\n**Response Format**:\n\nIncomplete audit:\n{\n  \"decision\": \"block\",\n  \"reason\": \"Security audit incomplete\",\n  \"stopReason\": \"🔒 Security Audit Incomplete\\n\\nMissing:\\n- [OWASP categories not covered]\\n- [Critical findings without remediation]\\n\\nRequired:\\n1. Complete OWASP Top 10 scan\\n2. Provide CVSS scores for all findings\\n3. Document remediation steps\\n\\nCurrent coverage: X/10 OWASP categories\"\n}\n\nComplete audit:\n{\n  \"decision\": \"approve\",\n  \"reason\": \"Comprehensive security audit complete\",\n  \"systemMessage\": \"✅ Security Audit Complete\\n\\nOWASP Top 10: 10/10 ✅\\nFindings: X Critical, X High, X Medium, X Low\\nCVSS Scoring: ✅\\nRemediation Plans: ✅\\n\\nSecurity Score: XX/100\\nRecommendation: [Ready for production / Requires fixes before deployment]\"\n}\n\nNow analyze the security audit and respond with JSON only.",
            "timeout": 30
          }
        ],
        "agentNames": ["security-analyzer"]
      }
    ]
  }
}
```

### Example 5: Smart Debug Resolution Validator

**Purpose**: Confirm bug actually fixed with root cause analysis.

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "name": "debug-resolution-validator",
        "description": "Validates bug fix completion and prevention strategy",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are a debugging expert validating bug fix completion.\n\nAgent: $ARGUMENTS.agentName\nBug: $ARGUMENTS.taskDescription\nResolution: $ARGUMENTS.transcript (debugging process)\n\n**Root Cause Analysis (5 Whys)**:\n\nDid the agent perform root cause analysis?\n- Surface symptom identified ✅\n- Immediate cause identified ✅\n- Underlying cause identified ✅\n- Root cause identified ✅\n- Contributing factors identified ✅\n\nExample good RCA:\n```\nSymptom: User registration fails with 500 error\nWhy 1: Database constraint violation\nWhy 2: Duplicate email addresses\nWhy 3: Multiple form submissions\nWhy 4: Submit button not disabled\nWhy 5: Missing client-side debouncing\n\nRoot Cause: Frontend missing submit button debounce\n```\n\n**Test-Driven Debugging**:\n\n1. ✅ Failing test created to reproduce bug\n2. ✅ Test initially fails (confirms reproduction)\n3. ✅ Fix applied\n4. ✅ Test now passes\n5. ✅ Full test suite still passes (no regressions)\n\n**Fix Quality**:\n\n- Addresses ROOT CAUSE (not just symptom)\n- Minimal change (surgical fix)\n- No side effects introduced\n- Code quality maintained\n- Documentation updated\n\n**Prevention Strategy**:\n\nDid the agent implement prevention measures?\n1. ✅ Regression test added\n2. ✅ Monitoring/alerting added (if production bug)\n3. ✅ Input validation improved (if applicable)\n4. ✅ Error handling enhanced (if applicable)\n5. ✅ Documentation/runbook updated\n\n**Decision Logic**:\n\nBLOCK if:\n- No root cause analysis performed (just symptom fix)\n- No failing test created\n- Tests still failing\n- Regression in test suite\n- No prevention strategy\n\nAPPROVE if:\n- Root cause identified (5 Whys)\n- Failing test created and now passes\n- Full test suite passes\n- Prevention measures documented\n- Fix addresses root cause\n\n**Response Format**:\n\nIncomplete fix:\n{\n  \"decision\": \"block\",\n  \"reason\": \"Bug fix incomplete\",\n  \"stopReason\": \"❌ Bug Fix Incomplete\\n\\nMissing:\\n- [Root cause analysis]\\n- [Failing test to reproduce bug]\\n- [Prevention strategy]\\n\\nRequired:\\n1. Perform 5 Whys root cause analysis\\n2. Create failing test: test_[bug_description]\\n3. Verify test passes after fix\\n4. Document prevention (monitoring, validation, etc.)\\n\\nCurrent: [Symptom fixed / Root cause unknown]\"\n}\n\nComplete fix:\n{\n  \"decision\": \"approve\",\n  \"reason\": \"Bug fix complete with prevention\",\n  \"systemMessage\": \"✅ Bug Fix Complete\\n\\nRoot Cause: [identified cause]\\nFix: [description]\\nTest: test_[name] ✅\\nRegression Suite: All passing ✅\\nPrevention: [measures taken]\\n\\nBug resolved and won't recur. Nice work!\"\n}\n\nNow analyze the bug fix and respond with JSON only.",
            "timeout": 30
          }
        ],
        "agentNames": ["smart-debug"]
      }
    ]
  }
}
```

## Phase 3: Hybrid Hooks

### Example 6: Enhanced Work Completion (Bash + Prompt)

**Purpose**: Fast checks (bash) + smart evaluation (prompt).

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "Stop": [
      {
        "name": "work-completion-check",
        "description": "Multi-stage work completion validation",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/work-completion-assistant.py",
            "description": "Fast checks: uncommitted changes, TODOs, tests"
          },
          {
            "type": "prompt",
            "prompt": "You are a work completion expert providing context-aware quality assessment.\n\nFast checks completed: $ARGUMENTS.bashHookResults\n\n**Context-Aware Evaluation**:\n\nThe bash hook already checked:\n- Uncommitted changes\n- TODOs in changed files\n- Test availability\n- Linting issues\n\nNow perform SMART evaluation:\n\n1. **Intent Alignment**\n   - Did we actually accomplish what the user requested?\n   - Is the work complete from a functional perspective?\n   - Are there obvious gaps?\n\n2. **Quality Assessment**\n   - Is the code production-ready?\n   - Are TODOs acceptable? (\"TODO: future feature\" OK, \"TODO: fix this hack\" NOT OK)\n   - Are uncommitted changes intentional? (\"WIP: experimenting\" OK, \"forgot to commit\" NOT OK)\n\n3. **Risk Evaluation**\n   - Are there unaddressed edge cases?\n   - Is error handling sufficient?\n   - Are security implications considered?\n\n**Decision Logic**:\n\nBLOCK if:\n- User request not actually fulfilled\n- Critical TODOs remain (\"fix this hack\", \"security issue\")\n- Tests failing\n- Production code without tests\n- Obvious quality issues\n\nWARN if:\n- Minor improvements possible\n- Documentation could be better\n- Test coverage could be higher (but meets minimum)\n\nAPPROVE if:\n- User request fulfilled\n- Quality acceptable\n- No critical issues\n- Future TODOs OK\n\n**Response Format**:\n\nIncomplete:\n{\n  \"decision\": \"block\",\n  \"reason\": \"Work incomplete or quality issues\",\n  \"stopReason\": \"❌ Work Incomplete\\n\\n[Specific issues]\\n\\nThe work doesn't fully address: [user request]\\n\\nRequired:\\n- [Action 1]\\n- [Action 2]\"\n}\n\nComplete with warnings:\n{\n  \"decision\": \"approve\",\n  \"systemMessage\": \"✅ Work Complete\\n\\n⚠️ Recommendations:\\n- [Suggestion 1]\\n- [Suggestion 2]\\n\\nThese can be addressed in future PRs.\"\n}\n\nComplete:\n{\n  \"decision\": \"approve\",\n  \"reason\": \"Work complete and quality verified\"\n}\n\nNow evaluate work completion and respond with JSON only.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

This hybrid approach:
1. **Bash hook** runs fast deterministic checks (0.1s)
2. **Prompt hook** does smart evaluation (1.5s)
3. Total latency: ~1.6s (acceptable for Stop event)

## Testing Your Hooks

### Manual Testing

```bash
# 1. Enable hook in settings
vim .claude/settings.json

# 2. Trigger the hook
# For SubagentStop: Run agent that should trigger validation
# For Stop: Try to stop Claude
# For PreToolUse: Use the tool (Bash, Write, etc.)

# 3. Observe behavior
# - Hook should execute (check latency)
# - Decision should be shown (approve/block)
# - Message should be clear

# 4. Test edge cases
# - Try operation that SHOULD be blocked
# - Try operation that SHOULD be approved
# - Verify false positive/negative rates
```

### Automated Testing

Create test script: `.claude/hooks/test-prompt-hooks.sh`

```bash
#!/bin/bash

echo "Testing prompt-based hooks..."

# Test destructive operation validator
echo "Test 1: Should BLOCK force push"
# Mock input
echo '{"toolName":"Bash","arguments":{"command":"git push --force origin main"},"cwd":"/repo"}' | \
  claude-hooks test-hook --name "destructive-operation-validator"

# Test 2: Should APPROVE normal operation
echo "Test 2: Should APPROVE normal commit"
echo '{"toolName":"Bash","arguments":{"command":"git commit -m \"fix: bug\""},"cwd":"/repo"}' | \
  claude-hooks test-hook --name "destructive-operation-validator"

# Add more tests...
```

## Monitoring & Metrics

### Hook Performance Dashboard

Track these metrics in your monitoring system:

```javascript
// Example metrics to collect
{
  "hook_name": "tdd-completion-validator",
  "executions_total": 1247,
  "decisions": {
    "approve": 1084,  // 87%
    "block": 163      // 13%
  },
  "latency": {
    "p50": 1.1,  // seconds
    "p95": 1.8,
    "p99": 2.4
  },
  "timeouts": 2,     // 0.16%
  "user_overrides": 37  // 3% (potential false positives)
}
```

### Alerts

Set up alerts for:
- Hook timeout rate >1%
- Hook latency p95 >3s
- User override rate >10% (too many false positives)
- Hook execution failures >5%

## Troubleshooting

### Common Issues

**Hook not triggering**:
```json
// Check agentNames/toolNames match exactly
{
  "agentNames": ["tdd-orchestrator"]  // Must match agent name exactly
}
```

**Timeout errors**:
```json
// Increase timeout or simplify prompt
{
  "timeout": 45  // Increase from 30s
}
```

**False positives (blocking when shouldn't)**:
```plaintext
Tune prompt to be more permissive:
- Add examples of acceptable cases
- Clarify decision criteria
- Consider WARN instead of BLOCK
```

**False negatives (approving when shouldn't)**:
```plaintext
Strengthen prompt evaluation:
- Add explicit MUST/MUST NOT rules
- Include specific patterns to detect
- Add security/quality checklists
```

## Next Steps

1. **Start with Phase 1**: Implement destructive operation + security file validators
2. **Test thoroughly**: Run on dev projects first
3. **Gather metrics**: Track latency, false positive/negative rates
4. **Iterate**: Tune prompts based on real-world usage
5. **Expand gradually**: Add Phase 2/3 hooks based on success

## Support

Questions or issues?
- Check main analysis doc: `PROMPT_BASED_HOOKS_ANALYSIS.md`
- Review Claude Code docs: https://code.claude.com/docs/en/hooks
- Create issue: https://github.com/greyhaven-ai/claude-code-config/issues

---

**Last Updated**: 2025-11-09
**Status**: Ready for implementation
**Phase**: Examples for Phase 1-3
