# Systematic Debugging Checklist

**Use when debugging errors, exceptions, or unexpected behavior.**

## Phase 1: Triage (2-5 minutes)

- [ ] Error message captured completely
- [ ] Stack trace obtained (full, not truncated)
- [ ] Environment identified (production, staging, development)
- [ ] Severity assessed (SEV1, SEV2, SEV3, SEV4)
- [ ] Error frequency determined (one-time, intermittent, consistent)
- [ ] First occurrence timestamp identified
- [ ] Recent changes reviewed (deployments, config changes)
- [ ] Production impact assessed (users affected, revenue impact)

### Triage Decision
- [ ] **SEV1 (Production Down)** - Escalate to incident-responder immediately
- [ ] **SEV2 (Degraded)** - Quick investigation (10 min max), then escalate if unresolved
- [ ] **SEV3 (Bug)** - Continue with full smart-debug workflow
- [ ] **SEV4 (Enhancement)** - Document and queue for later

## Phase 2: Stack Trace Analysis

- [ ] Error type identified (TypeError, ValueError, KeyError, etc.)
- [ ] Error message parsed and understood
- [ ] Call stack extracted (all frames with file, line, function)
- [ ] Root file identified (where error originated, not propagated)
- [ ] Root line number identified
- [ ] Stdlib/third-party frames filtered out
- [ ] Related files identified (files in call stack)
- [ ] Likely cause predicted using pattern matching

### Stack Trace Quality
- [ ] Stack trace is complete (not truncated)
- [ ] Source maps applied (for minified JavaScript)
- [ ] Line numbers accurate (code and deployed version match)

## Phase 3: Pattern Matching

- [ ] Error pattern database searched
- [ ] Matching error pattern found (or "unknown")
- [ ] Root cause hypothesis generated
- [ ] Fix template identified
- [ ] Prevention strategy identified
- [ ] Similar historical bugs reviewed (if available)

### Common Patterns Checked
- [ ] Null pointer / NoneType errors
- [ ] Type mismatch errors
- [ ] Index out of range errors
- [ ] Missing dictionary keys
- [ ] Module/import errors
- [ ] Database connection errors
- [ ] API contract violations
- [ ] Concurrency errors

## Phase 4: Code Inspection

- [ ] Root file read completely
- [ ] Problematic line identified
- [ ] Context examined (5 lines before/after)
- [ ] Function signature examined
- [ ] Variable types inferred
- [ ] Data flow traced (inputs to problematic line)
- [ ] Assumptions identified (null checks, type validations missing)

### Code Quality Check
- [ ] Tests exist for this code path (yes/no)
- [ ] Code has type hints (TypeScript, Python type hints)
- [ ] Code has input validation
- [ ] Code has error handling

## Phase 5: Observability Investigation

### Log Analysis
- [ ] Logs queried for error occurrences
- [ ] Error frequency calculated (per hour, per day)
- [ ] First occurrence timestamp confirmed
- [ ] Recent occurrences reviewed (last 10)
- [ ] Affected users identified (user IDs from logs)
- [ ] Error correlation checked (other errors at same time)

### Metrics Analysis
- [ ] Error rate queried (Prometheus, Cloudflare Analytics)
- [ ] Error spike identified (yes/no, when)
- [ ] Correlation with traffic spike checked
- [ ] Correlation with deployment checked
- [ ] Resource utilization checked (CPU, memory, connections)

### Trace Analysis
- [ ] Trace ID extracted from logs
- [ ] Distributed trace viewed (Jaeger, Zipkin)
- [ ] Span timings analyzed
- [ ] Upstream/downstream services checked
- [ ] Trace context propagation verified

## Phase 6: Reproduce Locally

- [ ] Test environment set up (matches production config)
- [ ] Input data identified (from logs or user report)
- [ ] Reproduction steps documented
- [ ] Error reproduced locally (consistent reproduction)
- [ ] Minimal reproduction case created (simplest input that triggers error)
- [ ] Failing test case written (pytest, vitest)
- [ ] Test runs and fails as expected

### Reproduction Quality
- [ ] Reproduction is reliable (100% reproducible)
- [ ] Reproduction is minimal (fewest steps possible)
- [ ] Test is isolated (no external dependencies if possible)

## Phase 7: Fix Generation

- [ ] Fix hypothesis generated (based on pattern match and code inspection)
- [ ] Fix option 1 generated (quick fix)
- [ ] Fix option 2 generated (robust fix)
- [ ] Fix option 3 generated (best practice fix)
- [ ] Trade-offs analyzed (complexity vs. robustness)
- [ ] Fix option selected (document rationale)

### Fix Options Evaluated
- [ ] **Quick fix** - Minimal code change, may not cover all cases
- [ ] **Robust fix** - Handles edge cases, more defensive
- [ ] **Best practice fix** - Follows design patterns, prevents similar bugs

## Phase 8: Fix Application

- [ ] Code changes made (Edit or MultiEdit tool)
- [ ] Changes reviewed for correctness
- [ ] No new bugs introduced (code review)
- [ ] Code style consistent (matches project conventions)
- [ ] Type hints added (if applicable)
- [ ] Comments added (explaining why, not what)

### Safety Checks
- [ ] No hardcoded values (use constants or config)
- [ ] No security vulnerabilities introduced
- [ ] No performance regressions introduced
- [ ] Backwards compatibility maintained (if API change)

## Phase 9: Test Verification

- [ ] Failing test now passes (verify fix works)
- [ ] Full test suite runs (pytest, vitest)
- [ ] All tests pass (no regressions)
- [ ] Code coverage maintained or improved
- [ ] Integration tests pass (if applicable)
- [ ] Edge cases tested (null, empty, large inputs)

### Test Quality
- [ ] Test is clear and readable
- [ ] Test documents expected behavior
- [ ] Test will catch regressions
- [ ] Test runs quickly (<1 second)

## Phase 10: Root Cause Analysis

- [ ] 5 Whys analysis performed
- [ ] True root cause identified (not just symptom)
- [ ] Contributing factors identified
- [ ] Timeline reconstructed (what happened when)
- [ ] RCA document created (using template)

### RCA Document Contents
- [ ] Error summary (what, where, when, impact)
- [ ] Timeline of events
- [ ] Investigation steps documented
- [ ] Root cause clearly stated
- [ ] Fix applied documented (with code snippet)
- [ ] Prevention strategy documented

## Phase 11: Prevention Strategy

- [ ] Immediate prevention: Unit test added (prevents this specific bug)
- [ ] Short-term prevention: Integration tests added (prevents similar bugs)
- [ ] Long-term prevention: Architecture changes proposed (prevents class of bugs)
- [ ] Monitoring added: Alert created (detects recurrence)
- [ ] Documentation updated: Runbook created (guides future debugging)

### Prevention Levels
- [ ] **Test Coverage** - Tests prevent regression
- [ ] **Type Safety** - Type hints catch errors at dev time
- [ ] **Input Validation** - Validates data early (Pydantic, zod)
- [ ] **Error Handling** - Graceful degradation
- [ ] **Monitoring** - Detects issues quickly
- [ ] **Documentation** - Team learns from incident

## Phase 12: Deploy & Monitor

### Pre-Deployment
- [ ] Fix tested in staging environment
- [ ] Performance impact assessed (no significant regression)
- [ ] Security review completed (if security-related bug)
- [ ] Deployment plan created (gradual rollout, rollback plan)
- [ ] Stakeholders notified (if high-impact bug)

### Deployment
- [ ] Fix deployed to staging first
- [ ] Staging verification successful
- [ ] Fix deployed to production (gradual rollout if possible)
- [ ] Deployment monitoring active (logs, metrics, traces)

### Post-Deployment
- [ ] Error logs monitored (1 hour post-deploy)
- [ ] Error rate confirmed to zero (or significantly reduced)
- [ ] No new errors introduced
- [ ] No performance degradation
- [ ] User reports checked (customer support, social media)

### Monitoring Duration
- [ ] 1 hour: Active monitoring (logs, errors, metrics)
- [ ] 24 hours: Passive monitoring (alerting enabled)
- [ ] 1 week: Review error trends (ensure no recurrence)

## Phase 13: Documentation & Learning

- [ ] Error pattern database updated (add new pattern if discovered)
- [ ] Team notified of fix (Slack, email)
- [ ] Postmortem conducted (if SEV1 or SEV2)
- [ ] Lessons learned documented
- [ ] Similar code locations reviewed (apply fix broadly if needed)
- [ ] Architecture improvements proposed (if needed)

### Knowledge Sharing
- [ ] RCA document shared with team
- [ ] Runbook created or updated
- [ ] Presentation given (if interesting or impactful bug)
- [ ] Blog post written (if educational value)

## Critical Validations

- [ ] Bug reliably reproduced before fixing
- [ ] Fix verified with passing test
- [ ] No regressions introduced
- [ ] Root cause identified (not just symptom fixed)
- [ ] Prevention strategy implemented
- [ ] Monitoring in place to detect recurrence
- [ ] Documentation complete (RCA, runbook)
- [ ] Team learns from incident

## Debugging Anti-Patterns (Avoid These)

- [X] Random code changes without hypothesis
- [X] Adding print statements without plan
- [X] Debugging production directly (use staging)
- [X] Ignoring error messages or stack traces
- [X] Not writing tests to verify fix
- [X] Fixing symptoms instead of root cause
- [X] Skipping reproduction step
- [X] Not documenting investigation
- [X] Not learning from mistakes (no RCA)
- [X] Working alone for > 30 min when stuck

## When to Escalate

**Escalate immediately if**:
- Production is down (SEV1)
- You're stuck for > 30 minutes with no progress
- Bug is in unfamiliar code/system
- Security vulnerability suspected
- Data corruption suspected
- Multiple systems affected

**Who to escalate to**:
- **incident-responder** - Production SEV1/SEV2
- **performance-optimizer** - Performance bugs
- **security-analyzer** - Security vulnerabilities
- **data-validator** - Data validation errors
- **Senior engineer** - Stuck for > 30 min
- **On-call engineer** - Outside business hours

## Success Criteria

- [ ] Bug fixed and verified with test
- [ ] Root cause identified and documented
- [ ] Prevention strategy implemented
- [ ] Team learns from incident
- [ ] Similar bugs prevented in future
- [ ] Documentation complete and accurate
- [ ] Debugging completed in reasonable time (< 2 hours for SEV3)
