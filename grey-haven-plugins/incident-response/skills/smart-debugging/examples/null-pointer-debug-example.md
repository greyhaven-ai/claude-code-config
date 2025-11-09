# Null Pointer Debug Example

Complete walkthrough of debugging a NoneType AttributeError using smart-debug systematic methodology.

## Error Encountered

**Environment**: Production
**Severity**: SEV2 (Degraded service - user profile pages failing)
**Frequency**: 127 occurrences in last 24 hours
**First Occurrence**: 2025-01-16 14:23:00 UTC

### Error Message

```python
AttributeError: 'NoneType' object has no attribute 'name'
```

### User Report

> "When I click on a user's profile after they've deleted their account, the page crashes with a 500 error instead of showing a 'User not found' message."

## Phase 1: Triage (3 minutes)

**Severity Assessment**:
- Not production down (SEV1)
- Affects specific user workflow (profile viewing)
- 127 occurrences = moderate frequency
- **Decision**: SEV2 - Proceed with full smart-debug workflow

**Error Category**: Runtime Exception (NoneType error)

## Phase 2: Stack Trace Analysis

### Full Stack Trace

```python
Traceback (most recent call last):
  File "/app/api/users.py", line 42, in get_user_profile
    return {"name": user.name, "email": user.email}
  File "/app/models/user.py", line 89, in name
    return self._name.upper()
AttributeError: 'NoneType' object has no attribute 'name'
```

### Pattern Match

**Pattern**: `null_pointer`
**Indicators**: `'NoneType' object has no attribute`
**Likely Cause**: Accessing property on None value - check for null/undefined
**Fix Template**: Add null check before access

## Phase 3: Code Inspection

### Problematic Code (api/users.py:42)

```python
@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile information."""
    user = await db.users.find_one({"id": user_id})

    # Line 42 - THE PROBLEM
    return {
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }
```

**Issue Identified**: No null check! If `find_one()` returns `None` (user doesn't exist), accessing `user.name` causes AttributeError.

### Root Cause

When a user deletes their account:
1. User record is deleted from database
2. But references to that user ID may still exist (links, mentions, etc.)
3. When someone tries to view the deleted user's profile, `find_one()` returns `None`
4. Code tries to access `None.name` → AttributeError

## Phase 4: Reproduce Locally

### Test Case (Failing)

```python
# tests/test_user_api.py
import pytest
from fastapi.testclient import TestClient

def test_get_deleted_user_profile(client: TestClient, db):
    """Test viewing profile of deleted user."""
    # Setup: Create and then delete a user
    user_id = "usr_deleted_123"
    db.users.insert_one({"id": user_id, "name": "Deleted User"})
    db.users.delete_one({"id": user_id})

    # Action: Try to get profile of deleted user
    response = client.get(f"/users/{user_id}/profile")

    # Expected: 404 Not Found, not 500 Internal Server Error
    assert response.status_code == 404
    assert response.json() == {"detail": f"User {user_id} not found"}
```

### Run Test (Fails as Expected)

```bash
$ pytest tests/test_user_api.py::test_get_deleted_user_profile -v

tests/test_user_api.py::test_get_deleted_user_profile FAILED

E   assert 500 == 404
E    +  where 500 = <Response [500 Internal Server Error]>.status_code
```

✅ **Reproduction Successful** - Test reliably reproduces the bug.

## Phase 5: Fix Generation

### Option 1: Quick Fix (Return Early)

```python
@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile information."""
    user = await db.users.find_one({"id": user_id})

    # Quick fix: Return early if user not found
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    return {
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }
```

**Pros**: Simple, fixes the immediate issue
**Cons**: Doesn't prevent similar issues elsewhere

### Option 2: Robust Fix (Custom Exception)

```python
# models/exceptions.py
class UserNotFoundError(Exception):
    """Raised when user is not found in database."""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

# api/users.py
@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile information."""
    user = await db.users.find_one({"id": user_id})

    if user is None:
        raise UserNotFoundError(user_id)

    return {
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }

# Global exception handler
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )
```

**Pros**: Reusable, type-safe, better error handling
**Cons**: More boilerplate

### Option 3: Best Practice (Helper Function)

```python
# services/user_service.py
async def get_user_or_404(user_id: str) -> User:
    """Get user by ID or raise 404."""
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user

# api/users.py
@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile information."""
    user = await get_user_or_404(user_id)  # Handles None case

    return {
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }
```

**Pros**: Reusable pattern, prevents similar bugs, clean API code
**Cons**: Slightly more abstraction

**Selected**: **Option 3** - Best practice with reusable helper

## Phase 6: Apply Fix

```python
# services/user_service.py
from fastapi import HTTPException

async def get_user_or_404(user_id: str) -> User:
    """
    Get user by ID or raise 404 Not Found.

    Args:
        user_id: User ID to retrieve

    Returns:
        User object

    Raises:
        HTTPException: 404 if user not found

    Example:
        user = await get_user_or_404("usr_123")
    """
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    return user

# api/users.py (FIXED)
@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile information."""
    user = await get_user_or_404(user_id)  # Null-safe!

    return {
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }
```

## Phase 7: Verify Fix

### Run Test Again (Should Pass)

```bash
$ pytest tests/test_user_api.py::test_get_deleted_user_profile -v

tests/test_user_api.py::test_get_deleted_user_profile PASSED ✅
```

### Run Full Test Suite

```bash
$ pytest tests/ -v

======================== 127 passed in 4.23s ========================
```

✅ **All tests pass** - No regressions introduced

### Manual Verification

```bash
# Test in staging
$ curl https://api-staging.example.com/users/usr_deleted_123/profile

HTTP/1.1 404 Not Found
{
  "detail": "User usr_deleted_123 not found"
}
```

✅ **Fix verified** - Returns proper 404 instead of 500

## Phase 8: Root Cause Analysis (5 Whys)

**Why 1**: Why did the API return 500 error?
→ Code tried to access `user.name` on None

**Why 2**: Why was `user` None?
→ Database query returned None (user doesn't exist)

**Why 3**: Why didn't code handle None case?
→ No null check before accessing user properties

**Why 4**: Why was there no null check?
→ Developer assumed user would always exist (invalid assumption)

**Why 5**: Why was invalid assumption made?
→ No code review guideline requiring null checks for database queries

**ROOT CAUSE**: Missing null-safety pattern for database queries + no enforcement in code review

## Phase 9: Prevention Strategy

### Immediate Prevention

✅ **Unit test added** (prevents this specific bug)

```python
def test_get_deleted_user_profile(client, db):
    # Test ensures 404 is returned for deleted users
    pass
```

### Short-term Prevention

✅ **Integration test added** (prevents similar bugs)

```python
@pytest.mark.parametrize("endpoint", [
    "/users/{id}/profile",
    "/users/{id}/settings",
    "/users/{id}/posts"
])
def test_user_endpoints_return_404_for_deleted_users(client, db, endpoint):
    """All user endpoints should return 404 for deleted users."""
    user_id = create_and_delete_user(db)
    response = client.get(endpoint.format(id=user_id))
    assert response.status_code == 404
```

### Long-term Prevention

✅ **Architecture change proposed**: Create `get_resource_or_404()` pattern

```python
# services/base_service.py
from typing import TypeVar, Generic, Type

T = TypeVar('T')

class BaseService(Generic[T]):
    """Base service with null-safe query methods."""

    async def get_or_404(
        self,
        resource_id: str,
        resource_type: str = "Resource"
    ) -> T:
        """Get resource by ID or raise 404."""
        resource = await self.find_one({"id": resource_id})
        if resource is None:
            raise HTTPException(
                status_code=404,
                detail=f"{resource_type} {resource_id} not found"
            )
        return resource

# Usage across all resources
user_service = UserService()
post_service = PostService()
comment_service = CommentService()

user = await user_service.get_or_404(user_id, "User")
post = await post_service.get_or_404(post_id, "Post")
```

### Monitoring Added

✅ **Alert created** (detects recurrence)

```yaml
# prometheus/alerts/user_not_found.yml
groups:
  - name: user_api
    rules:
    - alert: HighUserNotFoundRate
      expr: |
        rate(http_requests_total{
          endpoint="/users/:id/profile",
          status_code="404"
        }[5m]) > 10
      for: 5m
      annotations:
        summary: "High rate of user not found errors"
        description: "{{ $value }} 404s/sec on user profile endpoint"
```

### Documentation Updated

✅ **Runbook created**

```markdown
# Runbook: User Not Found Errors

## Symptom
404 errors when accessing user profiles

## Diagnosis
- Check if user was recently deleted
- Verify database replication lag
- Check for stale cache entries

## Resolution
- User deleted: Expected behavior
- Replication lag: Wait 30 seconds
- Stale cache: Clear user cache

## Prevention
Always use `get_user_or_404()` helper
```

## Phase 10: Deploy & Monitor

### Pre-Deployment Checklist

- [x] Fix tested in staging
- [x] No performance impact
- [x] Security review not needed (defensive fix)
- [x] Deployment plan created
- [x] Rollback plan ready

### Deployment

```bash
# Deploy to staging
$ git push origin feature/fix-user-not-found
$ ./scripts/deploy-staging.sh

# Verify in staging (1 hour)
$ ./scripts/monitor-staging.sh --duration 1h

# Deploy to production (gradual rollout)
$ ./scripts/deploy-production.sh --canary 10%  # 10% traffic
$ sleep 600  # Monitor for 10 minutes
$ ./scripts/deploy-production.sh --canary 50%  # 50% traffic
$ sleep 600
$ ./scripts/deploy-production.sh --canary 100% # Full traffic
```

### Post-Deployment Monitoring

**1 Hour Post-Deploy**:
```bash
# Check error logs
$ kubectl logs -l app=api --since=1h | grep "User.*not found"
# No unexpected errors ✅

# Check error rate
$ curl prometheus/query?query='rate(http_errors_total[1h])'
# No increase in error rate ✅
```

**24 Hours Post-Deploy**:
```bash
# Verify user not found rate is zero
$ curl prometheus/query?query='rate(http_requests_total{status_code="404",endpoint="/users/:id/profile"}[24h])'
# Result: 0 errors ✅
```

## Summary

| Metric | Value |
|--------|-------|
| **Time to Reproduce** | 5 minutes |
| **Time to Fix** | 15 minutes |
| **Time to Deploy** | 30 minutes |
| **Total Time** | 50 minutes |
| **Tests Added** | 2 (unit + integration) |
| **Prevention Strategies** | 3 (tests, architecture, monitoring) |
| **Recurrences** | 0 (monitored for 1 week) |

## Lessons Learned

### What Went Well
1. Clear stack trace made root cause obvious
2. Test-driven debugging caught the issue immediately
3. Helper function prevents similar bugs across codebase

### What Could Be Improved
1. Should have had null-safety pattern from the start
2. Code review should catch missing null checks
3. Static analysis could detect this pattern

### Recommendations
1. Add `mypy` or similar for null-safety checking
2. Update code review checklist to include null-safety checks
3. Create linter rule: "Database queries must use `get_or_404` pattern"

---

**Bug Fixed**: ✅
**Tests Pass**: ✅
**Prevention Implemented**: ✅
**Production Stable**: ✅
