# Test Quality Checklist

Comprehensive checklist for ensuring high-quality, maintainable, and effective tests.

**Purpose**: Verify tests are well-written, maintainable, and provide value
**Use**: Review tests against this checklist before committing

---

## Test Structure Quality

### Naming

- [ ] **Test name is descriptive**
  - Format: `test_[what]_[scenario]_[expected]`
  - ✅ Good: `test_add_item_with_negative_quantity_raises_value_error`
  - ❌ Bad: `test_add_item` or `test1`

- [ ] **Test name reads like documentation**
  - Can understand what's tested without reading code
  - Describes behavior, not implementation
  - Uses domain language

### Organization

- [ ] **Tests follow AAA pattern**
  - **Arrange**: Setup clearly separated
  - **Act**: Single action being tested
  - **Assert**: Verification clearly marked
  - Blank lines between sections

- [ ] **One logical assertion per test**
  - Tests ONE behavior
  - Multiple physical assertions OK if testing same behavior
  - Example: `assert result.status == "success" and result.code == 200`

- [ ] **Test is self-contained**
  - No hidden dependencies
  - Can understand test without reading others
  - Setup within test or clear fixture

### Clarity

- [ ] **Test is easy to understand**
  - Simple, straightforward code
  - No complex logic in tests
  - Clear what's being tested

- [ ] **Magic numbers explained**
  - Constants have meaningful names
  - ✅ Good: `MIN_AGE = 18`
  - ❌ Bad: `assert age > 18`

- [ ] **Test data is meaningful**
  - Use realistic values
  - ✅ Good: `email = "user@example.com"`
  - ❌ Bad: `email = "aaa"`

---

## Test Independence

### Isolation

- [ ] **Test can run alone**
  - No dependency on other tests
  - No shared state
  - Can run with `pytest -k test_name`

- [ ] **Test can run in any order**
  - No dependency on execution order
  - Same result regardless of order
  - Can shuffle: `pytest --random-order`

- [ ] **Test doesn't modify global state**
  - No global variables changed
  - No environment variables changed (or restored)
  - No file system changes (or cleaned up)

### Setup and Teardown

- [ ] **Proper cleanup**
  - Resources released (files, connections)
  - Temporary data deleted
  - State restored if modified

- [ ] **Uses appropriate fixtures**
  - Function scope for independent setup
  - Class/module scope only when necessary
  - Session scope only for expensive resources

---

## Assertion Quality

### Specificity

- [ ] **Assertions are specific**
  - ✅ Good: `assert result == 42`
  - ❌ Bad: `assert result > 0`
  - Test exact expected value when possible

- [ ] **Uses appropriate assertion method**
  - pytest: `assert`, `pytest.raises`, `pytest.approx`
  - unittest: `assertEqual`, `assertRaises`, `assertIn`, etc.
  - Not just `assert result` (too vague)

- [ ] **Floating point comparisons handled**
  - ✅ Good: `assert result == pytest.approx(0.3)`
  - ❌ Bad: `assert 0.1 + 0.2 == 0.3`

### Error Messages

- [ ] **Meaningful failure messages**
  - pytest: Automatic introspection usually sufficient
  - unittest: Add message to assertions when helpful
  - ✅ `assert result == 42, f"Expected 42 but got {result}"`

- [ ] **Exception assertions check message**
  - Not just exception type
  - Verify exception message when important
  - Example: `with pytest.raises(ValueError, match="negative")`

---

## Test Coverage

### Scenarios Tested

- [ ] **Happy path covered**
  - Normal, expected usage
  - Typical valid inputs
  - Standard flow

- [ ] **Edge cases covered**
  - Boundary values (0, 1, MAX, MIN)
  - Empty collections ([], {}, "")
  - Single-item collections
  - Large values
  - Special values (None, NaN, infinity)

- [ ] **Error cases covered**
  - Invalid input types
  - Invalid input values
  - Null/None inputs
  - Exception conditions
  - Failure scenarios

- [ ] **State transitions covered** (for stateful objects)
  - All valid state transitions
  - Invalid state transitions raise errors
  - State invariants maintained

### Code Coverage Metrics

- [ ] **Line coverage ≥ 80%** (minimum)
  - Aim for 90%+ on new code
  - 100% on critical paths

- [ ] **Branch coverage ≥ 75%** (minimum)
  - Both sides of if/else tested
  - All loop conditions tested
  - Aim for 85%+

- [ ] **Function coverage ≥ 85%** (minimum)
  - All public functions tested
  - Private functions tested via public API
  - Aim for 90%+

---

## Test Performance

### Speed

- [ ] **Tests run fast (< 1 second each)**
  - Unit tests < 100ms ideal
  - Integration tests < 1s acceptable
  - Slow tests should be rare and marked

- [ ] **No unnecessary waits**
  - No `time.sleep()` unless testing timing
  - Mock time instead of waiting
  - Use timeouts for potentially hanging tests

- [ ] **Expensive operations optimized**
  - Database setup once per session (if possible)
  - File I/O minimized
  - Network calls mocked

### Resource Usage

- [ ] **Tests don't leak resources**
  - Files closed
  - Connections closed
  - Memory released

- [ ] **Parallel execution supported**
  - Tests can run in parallel: `pytest -n auto`
  - No race conditions
  - No shared mutable state

---

## Fixture Quality

### Fixture Design

- [ ] **Fixtures have clear purpose**
  - Name describes what fixture provides
  - One responsibility per fixture
  - Not doing too much

- [ ] **Fixtures are reusable**
  - Used by multiple tests
  - General enough for various scenarios
  - Not test-specific (use inline setup instead)

- [ ] **Fixtures have appropriate scope**
  - Function scope (default): Fresh per test
  - Class scope: Shared across test class
  - Module scope: Once per module (expensive setup)
  - Session scope: Once per test run (very expensive)

### Fixture Composition

- [ ] **Fixtures compose well**
  - Fixtures can depend on other fixtures
  - Dependency tree is clear
  - No circular dependencies

- [ ] **Fixture cleanup**
  - Uses `yield` for cleanup
  - Cleanup always runs (even on failure)
  - Resources released properly

---

## Mock Quality

### When to Mock

- [ ] **Mocking external dependencies**
  - ✅ Database connections
  - ✅ HTTP API calls
  - ✅ File system (sometimes)
  - ✅ Time/random (for determinism)

- [ ] **NOT mocking too much**
  - ❌ Don't mock everything
  - ❌ Don't mock internal logic
  - ❌ Don't mock simple functions
  - Focus on boundaries

### Mock Configuration

- [ ] **Mocks are realistic**
  - Return values match real API
  - Exceptions match real behavior
  - Side effects realistic

- [ ] **Mocks verify behavior**
  - Check mock was called
  - Check with correct arguments
  - Check call count when relevant

- [ ] **Mocks don't hide issues**
  - Not mocking bugs away
  - Integration tests verify real behavior
  - Mock drift monitored

---

## Test Maintainability

### Code Quality

- [ ] **Tests are DRY**
  - No duplication between tests
  - Common setup in fixtures
  - Parametrize for similar scenarios

- [ ] **Tests are simple**
  - No complex logic in tests
  - No loops in tests (use parametrize)
  - No conditionals in tests

- [ ] **Test code quality**
  - Follows same standards as production
  - Clear variable names
  - Well-organized
  - Type hints (if using in production)

### Documentation

- [ ] **Test has docstring (when needed)**
  - Complex tests documented
  - Non-obvious behavior explained
  - Why test exists (if not obvious from name)

- [ ] **Comments for non-obvious code**
  - Explain why, not what
  - Document edge cases
  - Clarify complex setup

---

## Test Reliability

### Determinism

- [ ] **Test is deterministic**
  - Same result every time
  - No random failures
  - No flaky tests

- [ ] **No time dependencies**
  - Mock `datetime.now()` if needed
  - Use fixed timestamps
  - No race conditions

- [ ] **No environment dependencies**
  - Works on any machine
  - No hardcoded paths
  - No localhost dependencies

### Error Handling

- [ ] **Test failures are clear**
  - Easy to understand what failed
  - Assertion message helpful
  - Stack trace points to issue

- [ ] **Tests fail for right reason**
  - Failure indicates real problem
  - Not infrastructure issues
  - Not test setup issues

---

## Special Test Types

### Async Tests

- [ ] **Marked with `@pytest.mark.asyncio`**
- [ ] **Uses `await` correctly**
- [ ] **Uses `AsyncMock` for async mocks**
- [ ] **No blocking operations**

### Parametrized Tests

- [ ] **Parameters are well-chosen**
  - Cover important scenarios
  - Not too many (< 20 per test)
  - Clear what each tests

- [ ] **Test IDs provided (when helpful)**
  - `pytest.param(..., id="description")`
  - Makes failures easier to understand

### Property-Based Tests (if using hypothesis)

- [ ] **Properties are meaningful**
  - Test invariants, not examples
  - Properties hold for all inputs
  - Constraints reasonable

---

## Anti-Patterns to Avoid

### ❌ Testing Implementation Details

```python
# BAD: Testing internal method
def test_internal_method():
    obj._private_method()  # ❌ Testing private method
```

**Fix**: Test public interface only

### ❌ Tests That Test Nothing

```python
# BAD: No assertions
def test_function():
    function()  # ❌ Just calls function, doesn't verify
```

**Fix**: Add meaningful assertions

### ❌ Overly Complex Tests

```python
# BAD: Complex logic in test
def test_with_loop():
    for i in range(10):  # ❌ Loop in test
        if i % 2 == 0:   # ❌ Conditional in test
            assert function(i) == i * 2
```

**Fix**: Use parametrize or separate tests

### ❌ Hidden Dependencies

```python
# BAD: Depends on test execution order
class TestSequence:
    def test_a_create(self):
        self.data = "value"  # ❌ Shared state

    def test_b_use(self):
        assert self.data == "value"  # ❌ Depends on test_a
```

**Fix**: Make tests independent with fixtures

### ❌ Testing Multiple Things

```python
# BAD: Testing multiple behaviors
def test_user_operations():
    user = create_user()    # Tests creation
    update_user(user)       # Tests update
    delete_user(user)       # Tests deletion
```

**Fix**: Separate into 3 tests

### ❌ Brittle Tests

```python
# BAD: Depends on exact internal implementation
def test_brittle():
    result = function()
    # ❌ Checks internal structure instead of behavior
    assert result._internal_state == "specific_value"
```

**Fix**: Test behavior, not implementation

---

## Pre-Commit Checklist

### Before Committing Tests

- [ ] All tests pass locally
- [ ] No skipped tests (unless intentional)
- [ ] No commented-out tests
- [ ] No debug statements (`print`, `breakpoint`)
- [ ] Coverage goals met
- [ ] Tests reviewed against this checklist
- [ ] Code review (if applicable)

---

## Test Review Questions

### Essential Questions

1. **Does this test actually test something?**
   - Not just calling function
   - Verifies expected behavior
   - Has meaningful assertions

2. **Is it clear what's being tested?**
   - Name is descriptive
   - Test body is clear
   - Easy to understand

3. **Will this test catch bugs?**
   - Tests important behavior
   - Covers error cases
   - Meaningful assertions

4. **Is this test maintainable?**
   - Simple code
   - No duplication
   - Uses fixtures appropriately

5. **Is this test reliable?**
   - Deterministic
   - Independent
   - No flakiness

---

## Quick Reference

### Good Test Characteristics

**FIRST Principles**:
- **Fast**: Runs in < 1 second
- **Independent**: Can run alone
- **Repeatable**: Same result every time
- **Self-validating**: Pass/fail, no manual checking
- **Timely**: Written with (or before) code

**Additional Quality Markers**:
- Clear naming
- Single behavior tested
- Appropriate assertions
- Good coverage
- Well-organized
- Maintainable

### Test Smells

🚩 **Red Flags**:
- Test name not descriptive
- Multiple behaviors tested
- Complex logic in test
- Shared state between tests
- Long test (> 20 lines)
- Slow test (> 1s)
- Flaky test
- No assertions
- Mocking too much

---

## Scoring Your Tests

### Test Quality Score

Give each test a score:

| Criteria | Weight | Score (0-10) | Weighted |
|----------|--------|--------------|----------|
| Clear naming | 2x | __/10 | __ |
| Independence | 3x | __/10 | __ |
| Appropriate assertions | 3x | __/10 | __ |
| Speed | 1x | __/10 | __ |
| Maintainability | 2x | __/10 | __ |
| Coverage | 2x | __/10 | __ |

**Total**: __/130

**Rating**:
- 110-130: Excellent ⭐⭐⭐⭐⭐
- 90-109: Good ⭐⭐⭐⭐
- 70-89: Acceptable ⭐⭐⭐
- 50-69: Needs Improvement ⭐⭐
- < 50: Poor ⭐

---

**Version**: 1.0
**Last Updated**: 2024-01-15
