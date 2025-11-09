# Red-Green-Refactor Example: User Authentication

Complete TDD cycle demonstrating strict red-green-refactor discipline for implementing user login functionality.

## Scenario

**Feature**: User authentication with email and password
**Starting Point**: Empty `auth.py` module
**Goal**: Implement secure login with proper TDD methodology
**Time Budget**: 20 minutes for complete cycle
**Coverage Target**: >80% line, >75% branch, 100% critical path

## Phase 1: RED (5 minutes)

### Step 1: Write Failing Test

**Time**: 3 minutes

```python
# tests/test_auth.py
import pytest
from app.auth import login
from app.models import User

def test_login_with_valid_credentials():
    """Should return user when credentials are valid."""
    # Arrange
    user = User(email="john@example.com", password_hash="$2b$12$...")

    # Act
    result = login(email="john@example.com", password="correct-password")

    # Assert
    assert result is not None
    assert result.email == "john@example.com"
    assert result.authenticated is True
```

### Step 2: Run Test (Verify RED)

**Time**: 1 minute

```bash
$ pytest tests/test_auth.py::test_login_with_valid_credentials

FAILED tests/test_auth.py::test_login_with_valid_credentials
ImportError: cannot import name 'login' from 'app.auth'
```

**✅ RED Phase Success**: Test fails for the right reason (function doesn't exist)

### Step 3: Validate Test Quality

**Time**: 1 minute

**Quality Checklist**:
- ✅ Test name describes behavior: "login_with_valid_credentials"
- ✅ Follows AAA pattern (Arrange, Act, Assert)
- ✅ Single responsibility (tests one behavior)
- ✅ Clear assertions (checks user returned and authenticated)
- ✅ Fails for right reason (missing function)

**RED Phase Duration**: 5 minutes
**Status**: ✅ Ready for GREEN

---

## Phase 2: GREEN (8 minutes)

### Step 1: Minimal Implementation

**Time**: 6 minutes

```python
# app/auth.py
from app.models import User
from app.database import get_user_by_email
import bcrypt

def login(email: str, password: str) -> User | None:
    """Authenticate user with email and password."""
    # Get user from database
    user = get_user_by_email(email)
    if not user:
        return None

    # Verify password
    if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        user.authenticated = True
        return user

    return None
```

**Note**: This is MINIMAL code to make the test pass. No fancy error handling, no logging, no optimization - just enough to turn RED → GREEN.

### Step 2: Run Test (Verify GREEN)

**Time**: 1 minute

```bash
$ pytest tests/test_auth.py::test_login_with_valid_credentials

PASSED tests/test_auth.py::test_login_with_valid_credentials  ✅

1 passed in 0.12s
```

**✅ GREEN Phase Success**: Test passes!

### Step 3: Run All Tests

**Time**: 1 minute

```bash
$ pytest tests/

tests/test_auth.py::test_login_with_valid_credentials PASSED
tests/test_models.py::test_user_creation PASSED
tests/test_models.py::test_user_validation PASSED
...

47 passed in 2.3s  ✅
```

**Coverage Check**:
```bash
$ pytest --cov=app tests/

Coverage: 87% (+12% from baseline)
  Line: 87%
  Branch: 82%
  Critical Path: 100%
```

**GREEN Phase Duration**: 8 minutes
**Status**: ✅ Ready for REFACTOR

---

## Phase 3: REFACTOR (6 minutes)

### Step 1: Identify Improvements

**Time**: 2 minutes

**Code Smells Detected**:
1. **Single Responsibility Violation**: `login()` handles both database lookup and password verification
2. **Hardcoded bcrypt**: Password verification should be abstracted
3. **Missing type hints**: Return type could be more specific
4. **No input validation**: Email format not validated

### Step 2: Apply Refactoring

**Time**: 3 minutes

**Extract Method** - Separate password verification:

```python
# app/auth.py
from app.models import User
from app.database import get_user_by_email
import bcrypt

def login(email: str, password: str) -> User | None:
    """Authenticate user with email and password."""
    user = get_user_by_email(email)
    if not user:
        return None

    if _verify_password(password, user.password_hash):
        user.authenticated = True
        return user

    return None

def _verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash using bcrypt."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())
```

**Benefits**:
- ✅ Single Responsibility: `login()` orchestrates, `_verify_password()` validates
- ✅ Testable: Can test password verification independently
- ✅ Reusable: `_verify_password()` can be used elsewhere
- ✅ Clear intent: Function names describe what, not how

### Step 3: Verify Refactoring

**Time**: 1 minute

```bash
$ pytest tests/

tests/test_auth.py::test_login_with_valid_credentials PASSED  ✅
tests/test_models.py::test_user_creation PASSED
tests/test_models.py::test_user_validation PASSED
...

47 passed in 2.3s  ✅

Coverage: 87% (maintained) ✅
```

**✅ Refactoring Success**: All tests still pass, coverage maintained!

**REFACTOR Phase Duration**: 6 minutes
**Status**: ✅ Cycle complete!

---

## Cycle Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TDD Cycle Complete: User Login Authentication
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RED Phase (5 min):
  ✅ Created test_login_with_valid_credentials()
  ✅ Test failed with: "ImportError: cannot import 'login'"
  ✅ Assertion quality: HIGH (clear assertions, AAA pattern)

GREEN Phase (8 min):
  ✅ Implemented minimal login() function
  ✅ Test passed
  ✅ Coverage: +12% (87% total)
  ✅ All 47 tests passing

REFACTOR Phase (6 min):
  ✅ Extracted _verify_password() helper
  ✅ Applied Single Responsibility Principle
  ✅ All 47 tests still passing
  ✅ Coverage maintained at 87%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Cycle Time: 19 minutes ✅ (under 20min budget)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Metrics:
  • Cycle time: 19 minutes
  • Line coverage: 87% ✅ (target: 80%)
  • Branch coverage: 82% ✅ (target: 75%)
  • Critical path: 100% ✅
  • Tests added: 1
  • Production code: 18 lines
  • Test-to-code ratio: 0.8:1
```

---

## Next Cycles

### Cycle 2: Invalid Credentials

**RED** (3 min):
```python
def test_login_with_invalid_password():
    """Should return None when password is incorrect."""
    result = login(email="john@example.com", password="wrong-password")
    assert result is None
```

**GREEN** (2 min):
- Already handled by existing implementation! ✅
- Test passes without changes

**REFACTOR** (2 min):
- No refactoring needed
- Move to next cycle

**Cycle Time**: 7 minutes (faster with good design!)

### Cycle 3: Non-Existent User

**RED** (3 min):
```python
def test_login_with_nonexistent_email():
    """Should return None when user doesn't exist."""
    result = login(email="nobody@example.com", password="any-password")
    assert result is None
```

**GREEN** (2 min):
- Already handled! ✅
- Test passes

**REFACTOR** (skip):
- Design covers this case elegantly

**Cycle Time**: 5 minutes

---

## Mutation Testing (Cycle 4)

After completing happy path and error cases, validate test quality with mutation testing.

### Run Mutation Tests

```bash
$ mutmut run --paths-to-mutate app/auth.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mutation Testing Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated: 23 mutations
Killed: 21 (91%) ✅
Survived: 2 (9%)
Timeout: 0 (0%)

Mutation Score: 91% ✅ (excellent)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Surviving Mutations (Need Attention)

**Mutation #1**: Line 15 - Changed `==` to `!=`
```python
# Original
if not user:
    return None

# Mutated (survived)
if user:  # Logic inverted!
    return None
```

**Why it survived**: No explicit test for `user=None` case

**Fix**: Add test for database returning None

```python
def test_login_when_database_returns_none():
    """Should handle database errors gracefully."""
    # Mock database to return None
    result = login(email="john@example.com", password="password")
    assert result is None
```

**Mutation #2**: Line 21 - Removed `authenticated = True`
```python
# Original
user.authenticated = True
return user

# Mutated (survived)
return user  # Missing authentication flag!
```

**Why it survived**: Test didn't check `authenticated` attribute strongly enough

**Fix**: Strengthen assertion

```python
def test_login_with_valid_credentials():
    result = login(email="john@example.com", password="password")
    assert result is not None
    assert result.authenticated is True  # Strict boolean check ✅
```

### Re-run Mutations

```bash
$ mutmut run

Mutation Score: 100% ✅ (all mutations killed!)
```

---

## Key Lessons

### 1. RED Phase Must Fail Correctly

**❌ Bad RED**:
```python
def test_login():
    result = login("email", "password")
    assert True  # Always passes!
```

**✅ Good RED**:
```python
def test_login_with_valid_credentials():
    result = login("john@example.com", "password")
    assert result is not None  # Specific assertion
    assert result.email == "john@example.com"
```

### 2. GREEN Phase: Resist Over-Engineering

**❌ Bad GREEN** (over-engineered):
```python
def login(email, password):
    # Too much for first test!
    validate_email_format(email)
    validate_password_strength(password)
    log_login_attempt(email)
    rate_limit_check(email)
    user = get_user_with_caching(email)
    # ... 50 more lines
```

**✅ Good GREEN** (minimal):
```python
def login(email, password):
    user = get_user_by_email(email)
    if user and verify_password(password, user.password_hash):
        return user
    return None
```

Add complexity ONLY when tests demand it!

### 3. REFACTOR Phase: Tests Enable Confidence

Without tests:
```
"Will this change break something? I'm scared to refactor..."
```

With tests:
```
"Run tests → All pass → Refactor safely → Run tests again ✅"
```

### 4. Mutation Testing Finds Weak Tests

**Coverage says**: "100% of code executed" ✅
**Mutation testing says**: "But does it catch bugs?" 🤔

73% mutation score = Lots of code executed, but tests don't verify correctness!
91% mutation score = Tests actually validate behavior ✅

---

## Metrics Dashboard

### Cycle Time Trends

```
Feature            | RED  | GREEN | REFACTOR | Total
-------------------|------|-------|----------|-------
User Login         | 5min | 8min  | 6min     | 19min ✅
Invalid Password   | 3min | 2min  | 2min     | 7min  ✅
Nonexistent User   | 3min | 2min | 0min     | 5min  ✅
Mutation Fixes     | 5min | 3min  | 0min     | 8min  ✅
-------------------|------|-------|----------|-------
Average            | 4min | 4min  | 2min     | 10min
Target             | <10  | <15   | <10      | <35
Status             | ✅   | ✅    | ✅       | ✅
```

### Coverage Progression

```
Cycle              | Line  | Branch | Critical | Mutation
-------------------|-------|--------|----------|----------
Initial            | 75%   | 68%    | 85%      | N/A
After Cycle 1      | 87%   | 82%    | 100%     | 91%
After Cycle 2      | 89%   | 85%    | 100%     | 91%
After Cycle 3      | 91%   | 87%    | 100%     | 91%
After Mutations    | 91%   | 87%    | 100%     | 100% ✅
-------------------|-------|--------|----------|----------
Target             | 80%   | 75%    | 100%     | 85%
Status             | ✅    | ✅     | ✅       | ✅
```

### Quality Indicators

```
Metric                    | Before TDD | After TDD | Change
--------------------------|------------|-----------|--------
Defects in Production     | 12/sprint  | 1/sprint  | -92% ✅
Code Review Time          | 45min      | 15min     | -67% ✅
Feature Development Time  | 3.5 days   | 2.8 days  | -20% ✅
Test Maintenance Burden   | High       | Low       | ✅
Developer Confidence      | Low        | High      | ✅
```

---

## Common Pitfalls

### Pitfall #1: Test Passes on First Run

**Symptom**: Write test, run it, test passes immediately

**Problem**: Test doesn't actually test the feature (always-passing test)

**Solution**: Modify implementation to break test, verify it fails, then fix

```python
# Write test
def test_login():
    assert login("email", "pass") is not None

# Test passes immediately? 🤔

# Verify it actually tests something
def login(email, password):
    return "fake"  # Should make test fail if properly written

# Test still passes? Your test is broken! Fix it.
```

### Pitfall #2: Multiple Features Per Cycle

**Symptom**: Write 10 tests, implement entire feature, then run tests

**Problem**: Not true TDD - you're doing test-after development

**Solution**: ONE test, ONE implementation, ONE refactor. Repeat.

### Pitfall #3: Skipping Refactor

**Symptom**: Tests pass → move to next feature without refactoring

**Problem**: Technical debt accumulates, code becomes unmaintainable

**Solution**: ALWAYS refactor, even if "it works"

---

Related: [Outside-In TDD Example](outside-in-tdd-example.md) | [Mutation Testing Example](mutation-testing-example.md) | [TDD Rescue Example](tdd-rescue-example.md) | [Return to INDEX](INDEX.md)
