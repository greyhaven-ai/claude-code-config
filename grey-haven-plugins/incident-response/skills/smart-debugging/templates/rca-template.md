# Root Cause Analysis: [Title]

**Instructions**: Copy this template and fill in all sections. Delete instructional text in [brackets] when complete.

---

## Metadata

**Date**: [YYYY-MM-DD when RCA was conducted]
**Incident Date**: [YYYY-MM-DD when incident occurred]
**Incident ID**: [INC-12345 or ticket number]
**Severity**: [SEV1 (Critical) / SEV2 (Major) / SEV3 (Minor)]
**Status**: [Draft / In Review / Completed]
**Owner**: [Name of person conducting RCA]
**Reviewers**: [Names of people who reviewed this RCA]
**Related Issues**: [Links to tickets, PRs, or incidents]

---

## Executive Summary

[2-3 sentence summary covering: What broke? What was the impact? What was the root cause?]

**Example**:
> On 2025-11-05 at 14:32 UTC, the user profile API began returning 500 errors for approximately 15% of requests. Users were unable to view or update their profiles for 2.5 hours. Root cause was a missing null check after a recent code change that allowed deleted users to remain in cache, causing null pointer errors when their profiles were accessed.

---

## Impact

### User Impact

**Users Affected**: [Number or percentage]
- [Describe which users were impacted and how]

**Duration**: [Time from detection to resolution]
- **Detected**: [YYYY-MM-DD HH:MM UTC]
- **Mitigated**: [YYYY-MM-DD HH:MM UTC]
- **Resolved**: [YYYY-MM-DD HH:MM UTC]
- **Total Duration**: [X hours Y minutes]

**User Experience**: [Describe what users saw/experienced]
- [e.g., "Error page when accessing profile"]
- [e.g., "Unable to complete checkout"]

### Business Impact

**Revenue Impact**: [Estimated or actual]
- [e.g., "$12,000 in lost transactions"]
- [e.g., "N/A - no direct revenue impact"]

**SLA Impact**: [If applicable]
- [e.g., "99.9% uptime SLA breached (99.4% actual)"]
- [e.g., "Within SLA bounds"]

**Reputation Impact**: [Qualitative assessment]
- [e.g., "12 support tickets, 5 negative social media mentions"]
- [e.g., "Minimal - caught before user reports"]

---

## Timeline

[Chronological sequence of events. Use relative timestamps (T-00:XX) or absolute (HH:MM UTC)]

| Time | Event | System State | Action Taken |
|------|-------|--------------|--------------|
| [T-00:10] | [What happened] | [Relevant system state] | [What was done] |
| [T-00:05] | [What happened] | [Relevant system state] | [What was done] |
| [T+00:00] | [Incident start - first error] | [System state at incident] | [Initial response] |
| [T+00:15] | [Detection/alerting] | [How issue was discovered] | [Investigation started] |
| [T+00:45] | [Mitigation deployed] | [Temporary fix applied] | [What was mitigated] |
| [T+02:30] | [Resolution deployed] | [Permanent fix deployed] | [What was fixed] |

**Example**:
| Time | Event | System State | Action Taken |
|------|-------|--------------|--------------|
| T-00:15 | User deletion feature deployed | Cache invalidation logic updated | Normal deployment |
| T-00:10 | Admin deleted test user account | User removed from DB, cache clear initiated | User deleted successfully |
| T-00:05 | Cache clear completed (async) | User data removed from cache | Background job finished |
| T+00:00 | Profile API starts returning 500 errors | Null pointer accessing deleted user's data | Errors logged but not alerted |
| T+00:15 | Error spike detected by monitoring | 15% error rate on /users/:id endpoint | On-call paged |
| T+00:30 | Investigation identified null pointer | Deleted users in cache causing errors | Root cause hypothesis formed |
| T+00:45 | Quick fix deployed (null check) | 500 errors stopped | Mitigation successful |
| T+02:30 | Proper fix deployed (validation) | Comprehensive null handling added | Permanent resolution |

---

## Root Cause

### Problem Statement

[Clear, specific description of what went wrong]

**Example**:
> User profile API returned 500 errors when accessing profiles of recently deleted users because the cache invalidation was asynchronous and completed after the user record was deleted from the database. When the API tried to access the cached user object, it was null, causing an unhandled null pointer exception.

### 5 Whys Analysis

**Why #1**: [First level cause]
**Evidence**: [Logs, metrics, stack traces, or other data supporting this]

**Why #2**: [Deeper cause - why did #1 happen?]
**Evidence**: [Supporting data]

**Why #3**: [Even deeper - why did #2 happen?]
**Evidence**: [Supporting data]

**Why #4**: [Near root cause - why did #3 happen?]
**Evidence**: [Supporting data]

**Why #5**: [Root cause - fundamental reason]
**Evidence**: [Supporting data]

**Example**:

**Why #1**: API returned 500 error (NullPointerException)
**Evidence**: Stack trace shows `'NoneType' object has no attribute 'name'` at `users.py:45`

**Why #2**: User object was null when accessing `.name` property
**Evidence**: Database query returned None for user_id `usr_12345`

**Why #3**: User ID didn't exist in database
**Evidence**: User was deleted 5 minutes before error occurred

**Why #4**: Deleted user's profile was still being accessed
**Evidence**: Cache contained user_id `usr_12345` in "recently viewed" list

**Why #5**: Cache invalidation completed after user record deletion
**Evidence**: Cache clear is asynchronous and took 3 seconds; user accessed profile during this window

**Root Cause**: Asynchronous cache invalidation creates timing window where deleted users can be accessed before cache clears, causing null pointer errors.

### Root Cause Category

[Select one or more]
- [ ] Code Logic Error
- [ ] Missing Validation
- [ ] Missing Error Handling
- [ ] Configuration Error
- [ ] Infrastructure Issue
- [ ] Dependency Failure
- [ ] Performance/Scale Issue
- [ ] Race Condition/Timing Issue
- [ ] Security Vulnerability
- [ ] Data Quality Issue
- [ ] Process/Communication Gap

---

## Contributing Factors

[List factors that enabled or worsened the incident, but aren't the primary root cause]

1. **[Factor Name]**: [Description]
   - **Impact**: [How it contributed]
   - **Evidence**: [Supporting data]

2. **[Factor Name]**: [Description]
   - **Impact**: [How it contributed]
   - **Evidence**: [Supporting data]

**Example**:

1. **No Monitoring on User Deletion**: User deletion events had no metrics or alerts
   - **Impact**: Delayed detection by 15 minutes (relied on error spike detection)
   - **Evidence**: No alert fired until error rate threshold exceeded

2. **Insufficient Error Handling**: API endpoint lacked null checks for user objects
   - **Impact**: Null pointer became 500 error instead of graceful 404
   - **Evidence**: No null validation in `get_user_profile` function

3. **Missing Integration Tests**: No test covered "access recently deleted user" scenario
   - **Impact**: Issue not caught before production deployment
   - **Evidence**: Test suite has 0 tests for deleted user scenarios

---

## Prevention

### Immediate Actions (Within 24 hours)

**Target Completion**: [Date]

- [ ] **[Action 1]**: [Description]
  - **Owner**: [Name]
  - **Status**: [Not Started / In Progress / Completed]
  - **Completion Date**: [YYYY-MM-DD]

- [ ] **[Action 2]**: [Description]
  - **Owner**: [Name]
  - **Status**: [Not Started / In Progress / Completed]
  - **Completion Date**: [YYYY-MM-DD]

**Example**:
- [x] **Add null checks**: Add defensive null checks in all user profile endpoints
  - **Owner**: Alice Smith
  - **Status**: Completed
  - **Completion Date**: 2025-11-06
  - **PR**: #1234

### Short-term Actions (Within 1 week)

**Target Completion**: [Date]

- [ ] **[Action 1]**: [Description]
  - **Owner**: [Name]
  - **Status**: [Not Started / In Progress / Completed]
  - **Completion Date**: [YYYY-MM-DD]

- [ ] **[Action 2]**: [Description]
  - **Owner**: [Name]
  - **Status**: [Not Started / In Progress / Completed]
  - **Completion Date**: [YYYY-MM-DD]

**Example**:
- [ ] **Make cache invalidation synchronous**: Update user deletion to wait for cache clear
  - **Owner**: Bob Johnson
  - **Status**: In Progress
  - **Target Date**: 2025-11-12
  - **Issue**: PROJ-567

- [ ] **Add monitoring for user deletions**: Track user deletion events and cache invalidation duration
  - **Owner**: Carol Williams
  - **Status**: Not Started
  - **Target Date**: 2025-11-13
  - **Issue**: PROJ-568

### Long-term Actions (Within 1 month)

**Target Completion**: [Date]

- [ ] **[Action 1]**: [Description]
  - **Owner**: [Name]
  - **Status**: [Not Started / In Progress / Completed]
  - **Completion Date**: [YYYY-MM-DD]

- [ ] **[Action 2]**: [Description]
  - **Owner**: [Name]
  - **Status**: [Not Started / In Progress / Completed]
  - **Completion Date**: [YYYY-MM-DD]

**Example**:
- [ ] **Implement soft-delete pattern**: Replace hard deletes with soft deletes (deleted_at timestamp)
  - **Owner**: Alice Smith
  - **Status**: Not Started
  - **Target Date**: 2025-12-06
  - **Issue**: PROJ-569

- [ ] **Add comprehensive deleted user test suite**: Cover all scenarios involving deleted users
  - **Owner**: David Lee
  - **Status**: Not Started
  - **Target Date**: 2025-12-13
  - **Issue**: PROJ-570

---

## Technical Details

### Code Changes

**Files Modified**:
- [File path 1]: [Description of changes]
- [File path 2]: [Description of changes]

**Key Code Snippets**:

```python
# Before (buggy code)
[paste relevant buggy code]
```

```python
# After (fixed code)
[paste fixed code]
```

### Monitoring and Metrics

**Key Metrics During Incident**:
- [Metric name]: [Value during incident] (baseline: [normal value])
- [Metric name]: [Value during incident] (baseline: [normal value])

**Example**:
- API Error Rate: 15% (baseline: 0.1%)
- Response Time (p99): 5.2s (baseline: 200ms)
- Cache Hit Rate: 65% (baseline: 95%)

**New Monitoring Added**:
- [New alert/dashboard/metric 1]
- [New alert/dashboard/metric 2]

---

## Lessons Learned

### What Went Well

1. [Positive aspect 1 - e.g., "Quick detection via monitoring"]
2. [Positive aspect 2 - e.g., "Clear communication during incident"]
3. [Positive aspect 3 - e.g., "Effective rollback procedure"]

### What Could Be Improved

1. [Improvement area 1 - e.g., "Better integration test coverage"]
2. [Improvement area 2 - e.g., "Faster root cause identification"]
3. [Improvement area 3 - e.g., "More comprehensive error handling"]

### Action Items for Process Improvement

- [ ] **[Process improvement 1]**: [Description]
  - **Owner**: [Name]
  - **Target Date**: [YYYY-MM-DD]

- [ ] **[Process improvement 2]**: [Description]
  - **Owner**: [Name]
  - **Target Date**: [YYYY-MM-DD]

**Example**:
- [ ] **Update deployment checklist**: Add "verify cache invalidation timing" step
  - **Owner**: DevOps Team
  - **Target Date**: 2025-11-20

- [ ] **Create runbook for cache issues**: Document cache investigation procedures
  - **Owner**: SRE Team
  - **Target Date**: 2025-11-27

---

## Review and Sign-off

### RCA Review Checklist

Before finalizing this RCA, verify:

- [ ] Root cause clearly identified with evidence
- [ ] Timeline is accurate and complete
- [ ] All contributing factors documented
- [ ] Prevention actions are specific and actionable
- [ ] All action items have owners and due dates
- [ ] Technical details are accurate and helpful
- [ ] Lessons learned capture key takeaways
- [ ] No blame directed at individuals

### Reviewers

| Reviewer | Role | Date Reviewed | Approved |
|----------|------|---------------|----------|
| [Name] | [Engineering Lead / SRE / etc.] | [YYYY-MM-DD] | ☐ Yes ☐ No |
| [Name] | [Engineering Lead / SRE / etc.] | [YYYY-MM-DD] | ☐ Yes ☐ No |

### Sign-off

**RCA Completed By**: [Name]
**Date**: [YYYY-MM-DD]

**Incident Commander**: [Name]
**Date**: [YYYY-MM-DD]

---

## Follow-up

**Next Review Date**: [YYYY-MM-DD - typically 2-4 weeks after incident]

**Follow-up Items**:
- [ ] Verify all immediate actions completed
- [ ] Check progress on short-term actions
- [ ] Review long-term action planning
- [ ] Assess effectiveness of prevention measures
- [ ] Share learnings with broader team

---

## Additional Notes

[Any additional context, references, or notes that don't fit above sections]

**References**:
- [Link to incident Slack channel]
- [Link to monitoring dashboard]
- [Link to related RCAs]
- [Link to fix PRs]

---

**Template Version**: 1.0
**Last Updated**: 2025-11-06
