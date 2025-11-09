# Fix PR Template

**Instructions**: Copy this template when creating a pull request for a bug fix. Delete instructional text in [brackets] when complete.

---

## PR Title Format

```
fix: [concise description of what was fixed]
```

**Examples**:
- `fix: handle null user in profile API endpoint`
- `fix: add missing index on users.email column`
- `fix: prevent negative order totals in payment processing`

---

## Summary

[2-3 sentence overview of the bug and the fix]

**Template**:
> This PR fixes [issue/symptom]. The root cause was [explanation]. The fix [what was changed].

**Example**:
> This PR fixes the 500 errors occurring when accessing recently deleted user profiles. The root cause was a race condition where async cache invalidation completed after the user record was deleted from the database, causing null pointer exceptions. The fix makes cache invalidation synchronous and adds null checks at API boundaries.

---

## Related Issues

**Fixes**: [#123 or INC-456]
**Related**: [#789, #012]
**RCA**: [Link to Root Cause Analysis document]

---

## Root Cause

### Problem Description

[Detailed description of the bug with evidence]

**Template**:
- **Symptom**: [What users experienced]
- **Error**: [Error message or behavior]
- **Frequency**: [How often it occurred]
- **Affected Users**: [Who was impacted]

**Example**:
- **Symptom**: Users received error page when accessing profile pages
- **Error**: `NullPointerException: 'NoneType' object has no attribute 'name'`
- **Frequency**: 150 errors/hour (15% of profile requests)
- **Affected Users**: Anyone accessing recently deleted user profiles

### Root Cause Analysis

[Brief explanation using 5 Whys or other RCA method]

**Example**:
```
Why? → API returned 500 error
Why? → User object was null
Why? → User didn't exist in database
Why? → User was recently deleted
Why? → Cache invalidation completed after deletion
Root Cause: Async cache invalidation creates timing window
```

---

## Fix Approach

### Selected Approach

[Describe the chosen fix with justification]

**Template**:
**Chosen Fix**: [Option name]
**Implementation**: [What was changed]
**Rationale**: [Why this approach was selected]

**Example**:
**Chosen Fix**: Synchronous cache invalidation + defensive null checks
**Implementation**:
1. Changed cache invalidation from async to sync in user deletion flow
2. Added null checks in all user profile endpoints
3. Return 404 instead of 500 when user not found
**Rationale**: Eliminates race condition while also adding defensive programming. Low risk as deletion is infrequent operation where slight delay is acceptable.

### Alternative Approaches Considered

[List other approaches and why they weren't chosen]

**Template**:
**Option [X]**: [Approach name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

**Example**:
**Option 2**: Keep async invalidation, add retry logic
- **Pros**: Maintains async pattern, no performance impact
- **Cons**: Increases complexity, doesn't prevent issue (just reduces frequency)
- **Why not chosen**: Doesn't address root cause, just mitigates

**Option 3**: Implement soft-delete pattern
- **Pros**: Prevents entire class of "deleted resource" bugs
- **Cons**: Requires DB migration, changes data model, larger scope
- **Why not chosen**: Good long-term solution but too large for immediate fix (scheduled for future sprint)

---

## Changes

### Files Modified

[List of changed files with brief description]

- `[file path]`: [What changed]
- `[file path]`: [What changed]
- `[file path]`: [What changed]

**Example**:
- `api/endpoints/users.py`: Added null checks and 404 returns
- `services/user_service.py`: Changed cache.clear_async() to cache.clear()
- `tests/test_user_endpoints.py`: Added test for deleted user scenarios

### Key Code Changes

**Before** (Buggy Code):
```python
[Paste relevant buggy code section]
```

**After** (Fixed Code):
```python
[Paste fixed code section]
```

**Example**:

**Before** (Buggy Code):
```python
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id})
    # No null check - causes 500 if user is None
    return {"name": user.name, "email": user.email}
```

**After** (Fixed Code):
```python
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    return {"name": user.name, "email": user.email}
```

---

## Testing

### Test Coverage

[Describe what tests were added/modified]

**New Tests**:
- [Test 1]: [What it tests]
- [Test 2]: [What it tests]
- [Test 3]: [What it tests]

**Modified Tests**:
- [Test 1]: [What changed and why]

**Example**:

**New Tests**:
- `test_get_deleted_user_returns_404`: Verifies 404 returned for deleted users
- `test_cache_invalidation_synchronous`: Verifies cache cleared before deletion completes
- `test_null_user_handled_gracefully`: Tests all endpoints with None user

**Modified Tests**:
- `test_get_user_success`: Updated assertions to match new response format

### Test Results

```
[Paste test output showing all tests passing]
```

**Example**:
```
tests/test_user_endpoints.py::test_get_user_success PASSED
tests/test_user_endpoints.py::test_get_deleted_user_returns_404 PASSED
tests/test_user_endpoints.py::test_null_user_handled_gracefully PASSED
tests/integration/test_cache.py::test_cache_invalidation_synchronous PASSED

==================== 48 passed in 2.34s ====================
```

### Manual Testing

[Describe manual testing performed]

**Scenarios Tested**:
- [X] [Scenario 1]
- [X] [Scenario 2]
- [X] [Scenario 3]

**Example**:
- [X] Delete user, immediately try to access profile → Returns 404 ✅
- [X] Access existing user profile → Returns profile successfully ✅
- [X] Access non-existent user → Returns 404 ✅
- [X] Verified cache clears before deletion completes ✅

---

## Risk Assessment

**Risk Level**: [Low / Medium / High]

**Rationale**: [Explain risk assessment]

### Potential Issues

[List potential issues and mitigations]

**Template**:
**Risk**: [Description of risk]
**Likelihood**: [Low / Medium / High]
**Impact**: [Low / Medium / High]
**Mitigation**: [How risk is addressed]

**Example**:

**Risk**: Synchronous cache clear could slow down user deletion
**Likelihood**: Low (cache clear takes <100ms)
**Impact**: Low (user deletion is infrequent operation)
**Mitigation**: Measured cache clear duration in staging (avg 45ms, p99 120ms)

**Risk**: Breaking change to API response structure
**Likelihood**: Low (only changes error cases)
**Impact**: Low (clients already handle 4xx errors)
**Mitigation**: No changes to success response format; only 500 → 404 for deleted users

---

## Rollback Plan

### Rollback Procedure

[Step-by-step rollback instructions]

**If issues detected**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Example**:

**If issues detected after deployment**:
1. Revert PR via GitHub: Click "Revert" button on merged PR
2. Deploy reverted commit: `git pull && ./deploy.sh`
3. Monitor error rate: Should return to baseline within 5 minutes
4. If cache issues persist: Run `redis-cli FLUSHDB` to clear cache

### Rollback Decision Criteria

**Rollback immediately if**:
- [Condition 1]
- [Condition 2]

**Example**:
- Error rate increases >5% above baseline
- User deletion fails or hangs
- Cache performance degrades significantly
- Any data corruption detected

---

## Deployment Notes

### Prerequisites

[Any requirements before deployment]

- [X] [Requirement 1]
- [X] [Requirement 2]

**Example**:
- [X] Database backup completed
- [X] Staging deployment successful
- [X] All integration tests passed
- [X] Performance testing completed

### Deployment Steps

[Special deployment instructions if needed]

**Standard Deployment**:
1. [Step 1]
2. [Step 2]

**Example**:
**Standard Deployment**:
1. Merge PR to main branch
2. CI/CD automatically deploys to production
3. Monitor error rate dashboard for 15 minutes
4. Verify cache invalidation metrics

**Feature Flag** (if applicable):
- Feature flag `new_user_validation` controls this fix
- Start at 10%, gradually increase to 100% over 24 hours

### Post-Deployment Verification

[How to verify the fix is working]

- [ ] [Verification step 1]
- [ ] [Verification step 2]
- [ ] [Verification step 3]

**Example**:
- [ ] Error rate returns to baseline (<0.1%)
- [ ] No 500 errors for profile endpoints in last hour
- [ ] Response time (p99) under 200ms
- [ ] Cache hit rate returns to >95%
- [ ] User deletion completes successfully

---

## Monitoring

### Metrics to Watch

[Key metrics to monitor after deployment]

**Template**:
| Metric | Baseline | Alert Threshold | Dashboard |
|--------|----------|-----------------|-----------|
| [Metric name] | [Normal value] | [Alert at] | [Link] |

**Example**:
| Metric | Baseline | Alert Threshold | Dashboard |
|--------|----------|-----------------|-----------|
| API Error Rate | 0.1% | >1% | [Grafana Dashboard](link) |
| Cache Invalidation Duration | 45ms avg | >500ms p99 | [Cache Metrics](link) |
| User Profile Response Time | 120ms p99 | >500ms | [API Latency](link) |

### New Alerts

[Any new alerts added]

- [Alert 1]: [Description and threshold]
- [Alert 2]: [Description and threshold]

**Example**:
- User Deletion Failures: Alert if user deletion fails or takes >5 seconds
- Cache Invalidation Timeout: Alert if cache clear takes >1 second

---

## Documentation

### Updated Documentation

[List of documentation updated]

- [ ] [Doc 1]: [What was updated]
- [ ] [Doc 2]: [What was updated]

**Example**:
- [X] API docs: Updated error response documentation for 404 cases
- [X] Runbook: Added user deletion troubleshooting section
- [X] Architecture docs: Updated cache invalidation flow diagram

### Knowledge Sharing

[How findings will be shared]

- [ ] RCA shared with team
- [ ] Post-mortem meeting scheduled
- [ ] Lessons learned documented

---

## Checklist

### Pre-Merge Checklist

- [ ] All tests pass locally
- [ ] Code reviewed by at least one teammate
- [ ] No linting or type errors
- [ ] Documentation updated
- [ ] Changelog updated (if applicable)
- [ ] Tests added for bug scenario
- [ ] Manual testing completed
- [ ] Performance impact assessed
- [ ] Security implications reviewed

### Post-Merge Checklist

- [ ] CI/CD pipeline passed
- [ ] Deployed to staging successfully
- [ ] Staging verification completed
- [ ] Deployed to production
- [ ] Post-deployment verification completed
- [ ] Metrics monitored for 24 hours
- [ ] RCA completed and shared
- [ ] Related tickets updated/closed

---

## Screenshots / Evidence

[Include any relevant screenshots, logs, or evidence]

**Before Fix**:
```
[Paste error logs or screenshots showing the bug]
```

**After Fix**:
```
[Paste logs or screenshots showing the fix working]
```

**Example**:

**Before Fix - Error Logs**:
```
2025-11-05 14:32:15 ERROR NullPointerException: 'NoneType' object has no attribute 'name'
  File "api/users.py", line 45, in get_user
2025-11-05 14:32:16 ERROR NullPointerException: 'NoneType' object has no attribute 'name'
  [150 similar errors]
```

**After Fix - Success Logs**:
```
2025-11-06 10:15:23 INFO GET /users/deleted_user_id → 404 Not Found
2025-11-06 10:15:24 INFO User deletion completed, cache cleared (45ms)
2025-11-06 10:15:25 INFO GET /users/deleted_user_id → 404 Not Found
```

**Error Rate Graph**:
![Error rate before and after fix](link-to-graph)

---

## Additional Context

[Any other relevant information]

**Related Work**:
- [Link to related PRs]
- [Link to follow-up work]

**Follow-up Items**:
- [ ] [Future improvement 1]
- [ ] [Future improvement 2]

**Example**:

**Related Work**:
- #1245 - Added soft-delete pattern (long-term fix scheduled for Q1)
- #1246 - Comprehensive cache strategy review

**Follow-up Items**:
- [ ] Migrate to soft-delete pattern for all entities (Q1 2025)
- [ ] Add cache invalidation duration monitoring dashboard
- [ ] Create automated tests for all "deleted resource" scenarios

---

## Reviewers

**Required Reviewers**:
- @[username] - [Role - e.g., Tech Lead]
- @[username] - [Role - e.g., SRE]

**Optional Reviewers**:
- @[username] - [Role - e.g., Domain Expert]

---

**Template Version**: 1.0
**Last Updated**: 2025-11-06
