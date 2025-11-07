# Root Cause Analysis (RCA) Methodology

Comprehensive guide to performing effective root cause analysis for software bugs and incidents.

## What is Root Cause Analysis?

**Definition**: Systematic process of identifying the fundamental reason why a problem occurred, not just treating symptoms.

**Goal**: Find the root cause(s) to implement prevention strategies that stop recurrence.

**Key Principle**: Distinguish between:
- **Symptom**: Observable error (e.g., "API returns 500 error")
- **Proximate Cause**: Immediate trigger (e.g., "Database query timeout")
- **Root Cause**: Fundamental reason (e.g., "Missing database index on frequently queried column")

## The 5 Whys Technique

### Overview

**Method**: Ask "Why?" five times (or more) to drill down from symptom to root cause.

**Origin**: Toyota Production System (Lean Manufacturing)

**Best For**: Sequential cause-effect chains

### Example: Null Pointer Error

```
Problem: API endpoint returns 500 error

Why? → User object is null when accessing .name property
Why? → Database query returned null instead of user
Why? → User ID doesn't exist in database
Why? → Frontend sent incorrect user ID from stale cache
Why? → Cache invalidation not triggered after user deletion
ROOT CAUSE: Missing cache invalidation on user deletion
```

### Rules for Effective 5 Whys

1. **Be Specific**: "Database slow" → "Query takes 4.5s (target: <200ms)"
2. **Use Data**: Support each "Why" with evidence (logs, metrics, traces)
3. **Don't Stop Too Early**: Keep asking until you reach a process/policy root cause
4. **Don't Blame People**: Focus on processes, not individuals
5. **May Need More/Fewer Than 5**: Stop when you reach actionable root cause

### Template

```markdown
**Problem Statement**: [Observable symptom with impact]

**Why #1**: [First level cause]
**Evidence**: [Logs, metrics, traces]

**Why #2**: [Deeper cause]
**Evidence**: [Supporting data]

**Why #3**: [Even deeper]
**Evidence**: [Supporting data]

**Why #4**: [Near root cause]
**Evidence**: [Supporting data]

**Why #5**: [Root cause]
**Evidence**: [Supporting data]

**Root Cause**: [Fundamental reason]
**Prevention**: [How to prevent recurrence]
```

## Fishbone (Ishikawa) Diagram

### Overview

**Method**: Visual diagram categorizing potential causes into major categories.

**Best For**: Complex problems with multiple contributing factors

**Categories (Software Context)**:
- **Code**: Logic errors, missing validation, edge cases
- **Data**: Invalid inputs, corrupt data, missing records
- **Infrastructure**: Server issues, network problems, resource limits
- **Dependencies**: Third-party APIs, libraries, services
- **Process**: Deployment issues, configuration errors, environment mismatches
- **People**: Knowledge gaps, communication failures, assumptions

### Example Structure

```
                     Code
                      |
            Missing validation
                 /
                /
API 500 ─────────────── Infrastructure
Error            \
                  \
                Database timeout
                      |
                    Data
```

### When to Use

- Multiple potential root causes
- Need stakeholder alignment on cause
- Complex systems with many dependencies
- Post-incident reviews with team

## Timeline Analysis

### Overview

**Method**: Create chronological sequence of events leading to incident.

**Best For**: Understanding cascading failures, race conditions, timing issues

### Example

```markdown
## Timeline: User Profile Page Crash

**T-00:05** - User updates profile information
**T-00:03** - Profile update succeeds, cache invalidation triggered
**T-00:02** - Cache clear initiated but takes 3s (network latency)
**T-00:00** - User refreshes page, cache still has old data
**T+00:01** - API fetches user from cache (stale)
**T+00:02** - Frontend renders with field that was deleted in update
**T+00:03** - JavaScript error: Cannot read property 'X' of undefined
**T+00:04** - Error boundary catches error, shows crash page

**Root Cause**: Cache invalidation is async and completes after page reload, causing stale data rendering.
```

### Components

| Element | Description | Example |
|---------|-------------|---------|
| **Timestamp** | Relative or absolute time | `T-00:05` or `14:32:15 UTC` |
| **Event** | What happened | `User clicked submit` |
| **System State** | Relevant state at time | `Cache: stale, DB: updated` |
| **Decision Point** | Branch in event chain | `If cache miss: fetch DB` |

## Distinguishing Root Cause from Symptoms

### Symptom vs. Root Cause

| Symptom | Root Cause |
|---------|------------|
| API returns 500 error | Missing error handling for null user |
| Database query slow | Missing index on `user_id` column |
| Memory leak in production | Circular reference in event listeners |
| User can't login | Session cookie expires after 5 minutes (should be 24h) |

### Test: The Prevention Question

**Ask**: "If I fix this, will the problem never happen again?"

**If Yes** → Likely root cause
**If No** → Still a symptom or contributing factor

**Example**:
- "Add null check" → Prevents this specific null error, but why was data null? (Symptom fix)
- "Add database foreign key constraint" → Prevents any invalid user_id from being stored (Root cause fix)

## Contributing Factors vs. Root Cause

### Multiple Contributing Factors

Complex incidents often have multiple contributing factors and one primary root cause.

**Example: Data Loss Incident**

```markdown
**Primary Root Cause**: Database backup script fails silently (no monitoring)

**Contributing Factors**:
1. No backup validation process
2. Backup monitoring disabled in production
3. Backup script lacks error logging
4. No runbook for backup verification
5. Manual backup never tested

**Analysis**: All factors contributed, but root cause is silent failure. Fix that first.
```

### Prioritization

| Priority | Factor Type | Action |
|----------|-------------|--------|
| **P0** | Root cause | Fix immediately |
| **P1** | Major contributor | Fix in same release |
| **P2** | Minor contributor | Fix in next sprint |
| **P3** | Edge case | Backlog |

## RCA Documentation Format

### Standard Structure

```markdown
# Root Cause Analysis: [Title]

**Date**: YYYY-MM-DD
**Incident ID**: INC-12345
**Severity**: [SEV1/SEV2/SEV3]
**Participants**: [Names of people involved in RCA]

## Summary

[2-3 sentence overview of incident and root cause]

## Impact

- **Users Affected**: [Number or %]
- **Duration**: [Time from start to resolution]
- **Business Impact**: [Revenue loss, SLA breach, etc.]

## Timeline

[Chronological sequence of events]

## Root Cause

[Detailed explanation of fundamental cause]

### 5 Whys Analysis

[Step-by-step "Why?" chain]

## Contributing Factors

[List of factors that enabled or worsened the incident]

## Prevention

### Immediate Actions (Within 24h)
- [ ] Action 1
- [ ] Action 2

### Short-term Actions (Within 1 week)
- [ ] Action 1
- [ ] Action 2

### Long-term Actions (Within 1 month)
- [ ] Action 1
- [ ] Action 2

## Lessons Learned

[Key takeaways and process improvements]
```

## Prevention Strategy Development

### Fix Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Technical** | Code, config, infrastructure changes | Add database index, implement retry logic |
| **Process** | Changes to how work is done | Require code review for DB changes |
| **Monitoring** | Detect issues before they cause incidents | Alert on slow query thresholds |
| **Testing** | Catch issues before production | Add integration test for edge case |
| **Documentation** | Improve knowledge sharing | Document backup restoration procedure |

### Prevention Checklist

```markdown
**Can we prevent the root cause?**
- [ ] Technical fix implemented
- [ ] Tests added to catch recurrence
- [ ] Monitoring added to detect early

**Can we detect it faster?**
- [ ] Alerts configured
- [ ] Logging improved
- [ ] Dashboards updated

**Can we mitigate impact?**
- [ ] Graceful degradation added
- [ ] Circuit breaker implemented
- [ ] Fallback logic added

**Can we recover faster?**
- [ ] Runbook created
- [ ] Automation added
- [ ] Team trained

**Can we prevent similar issues?**
- [ ] Pattern identified
- [ ] Linting rule added
- [ ] Architecture review scheduled
```

## Common RCA Pitfalls

### Pitfall 1: Stopping Too Early

**Bad**:
```
Why? → User got 500 error
Root Cause: Server returned error

Prevention: Fix server error
```

**Good**:
```
Why? → User got 500 error
Why? → Server threw unhandled exception
Why? → Null pointer accessing user.email
Why? → User object was null
Why? → Database returned no user
Why? → User ID didn't exist
Why? → Frontend sent deleted user's ID
Why? → Frontend cache not invalidated after deletion
Root Cause: Missing cache invalidation on user deletion

Prevention: Trigger cache clear on user deletion, add cache TTL as safety
```

### Pitfall 2: Blaming People

**Bad**:
```
Root Cause: Developer forgot to add validation
Prevention: Tell developer to remember next time
```

**Good**:
```
Root Cause: No validation enforced at API boundary
Prevention:
- Use Pydantic for automatic validation
- Add linting rule to detect missing validation
- Update code review checklist
```

### Pitfall 3: Accepting "Human Error" as Root Cause

**Bad**:
```
Root Cause: Admin accidentally deleted production database
Prevention: Be more careful
```

**Good**:
```
Root Cause: Production database lacks deletion protection
Prevention:
- Enable RDS deletion protection
- Require MFA for production access
- Implement soft-delete instead of hard-delete
- Add "Are you sure?" confirmation with typed confirmation
```

### Pitfall 4: Multiple Root Causes Without Prioritization

**Bad**:
```
Root Causes:
1. Missing error handling
2. No monitoring
3. Bad documentation
4. Insufficient testing
5. Poor communication

Prevention: Fix all of them
```

**Good**:
```
Primary Root Cause: Missing error handling (caused immediate incident)

Contributing Factors:
- No monitoring (delayed detection)
- Insufficient testing (didn't catch before deployment)

Prevention Priority:
1. Add error handling (prevents recurrence) - P0
2. Add monitoring (faster detection) - P1
3. Add tests (catch in CI) - P1
4. Improve docs (better response) - P2
```

### Pitfall 5: Technical Fix Without Process Improvement

**Bad**:
```
Root Cause: Missing database index
Prevention: Add index
```

**Good**:
```
Root Cause: Missing database index causing slow queries
Prevention:
- Technical: Add index on user_id column
- Process: Require query performance review in code review
- Monitoring: Alert on queries >200ms
- Testing: Add performance test asserting query count
```

## RCA Review and Validation

### Review Checklist

```markdown
- [ ] Root cause clearly identified and evidence-based
- [ ] Timeline accurate and complete
- [ ] All contributing factors documented
- [ ] Prevention strategies are actionable
- [ ] Prevention strategies assigned owners and due dates
- [ ] Lessons learned documented
- [ ] Incident review meeting scheduled
- [ ] RCA shared with relevant teams
```

### Validation Questions

1. **Completeness**: Does the RCA explain all observed symptoms?
2. **Preventability**: Will the proposed fixes prevent recurrence?
3. **Testability**: Can we verify the fixes work?
4. **Generalizability**: Are there similar issues we should address?
5. **Sustainability**: Will fixes remain effective long-term?

## Best Practices

### Do's

✅ **Start RCA immediately** after incident resolution
✅ **Involve multiple people** for diverse perspectives
✅ **Use data** to support each "Why" answer
✅ **Focus on processes**, not people
✅ **Document everything** even if it seems obvious
✅ **Assign owners** to all prevention actions
✅ **Set deadlines** for prevention implementation
✅ **Follow up** to ensure actions completed

### Don'ts

❌ **Don't rush** - Thorough RCA takes time
❌ **Don't blame** - Focus on systemic issues
❌ **Don't accept vague answers** - "System was slow" → "Query took 4.5s"
❌ **Don't stop at technical fixes** - Address process and monitoring too
❌ **Don't skip documentation** - Future incidents benefit from past RCAs
❌ **Don't forget to close the loop** - Verify prevention actions worked

## Quick Reference

| Technique | Best For | Output |
|-----------|----------|--------|
| **5 Whys** | Sequential cause-effect chains | Linear cause chain → root cause |
| **Fishbone** | Multiple potential causes | Categorized causes diagram |
| **Timeline** | Cascading failures, timing issues | Chronological event sequence |

| Root Cause Type | Fix Strategy |
|-----------------|--------------|
| **Missing validation** | Add validation at boundary + tests |
| **Missing error handling** | Add try/catch + logging + monitoring |
| **Performance issue** | Optimize + add performance test + alert |
| **Configuration error** | Fix config + add validation + documentation |
| **Process gap** | Update process + add checklist + training |

---

**Usage**: When debugging is complete, perform RCA to understand why the bug existed and how to prevent similar issues. Use 5 Whys for most cases, Fishbone for complex multi-factor incidents, Timeline for cascading failures.
