# TDD Discipline Checklist

Checklist to ensure strict adherence to Test-Driven Development methodology and RED-GREEN-REFACTOR cycle.

**Purpose**: Maintain TDD discipline and prevent reverting to code-first development
**Use**: Review this checklist regularly during TDD sessions

---

## Before Starting Session

### Planning

- [ ] **Feature requirements clearly defined**
  - User story written
  - Acceptance criteria listed
  - Expected behavior documented

- [ ] **Test cases identified**
  - Happy path scenarios
  - Edge cases
  - Error conditions
  - Minimum 3-5 test cases planned

- [ ] **Environment setup complete**
  - Test framework installed (pytest/unittest)
  - Coverage tool configured
  - Project structure ready

- [ ] **Time allocated**
  - Estimated duration set
  - No interruptions planned
  - Focus time blocked

---

## RED Phase Checklist

### Writing the Failing Test

- [ ] **Test written BEFORE implementation**
  - ⚠️ CRITICAL: Implementation code does not exist yet
  - Function/class/method is undefined
  - No production code written

- [ ] **Test follows AAA pattern**
  - **Arrange**: Setup is clear and minimal
  - **Act**: Single action being tested
  - **Assert**: Expected outcome verified

- [ ] **Test is specific and focused**
  - Tests ONE behavior only
  - Clear what is being tested
  - Not testing multiple scenarios in one test

- [ ] **Test name is descriptive**
  - Format: `test_[function]_[scenario]_[expected]`
  - Example: `test_add_item_with_valid_product_adds_to_cart`
  - Reads like documentation

- [ ] **Test uses appropriate assertions**
  - pytest: `assert result == expected`
  - unittest: `self.assertEqual(result, expected)`
  - Specific assertion (not just `assert result`)

- [ ] **Test run and FAILS for the right reason**
  - ✅ NameError / AttributeError (function doesn't exist)
  - ✅ AssertionError (wrong behavior)
  - ❌ Not: SyntaxError, ImportError (fix these first)

### RED Phase Verification

```bash
# Run test
pytest tests/test_module.py::test_name -v

# Expected output
❌ FAILED tests/test_module.py::test_name
```

- [ ] **Test fails as expected**
- [ ] **Failure reason is clear**
- [ ] **No other tests broken**

---

## GREEN Phase Checklist

### Minimal Implementation

- [ ] **Write MINIMAL code to pass test**
  - ⚠️ CRITICAL: Only code needed to make THIS test pass
  - No "nice to have" features
  - No premature optimization
  - No extra functionality

- [ ] **Implementation is simple**
  - Simplest solution that works
  - No complex logic (yet)
  - No abstraction (yet)
  - OK to hard-code initially

- [ ] **Test now PASSES**
  - ✅ Test runs successfully
  - ✅ Assertion passes
  - ✅ No errors or warnings

### GREEN Phase Verification

```bash
# Run test
pytest tests/test_module.py::test_name -v

# Expected output
✅ PASSED tests/test_module.py::test_name
```

- [ ] **Test passes**
- [ ] **All previous tests still pass**
- [ ] **Implementation is minimal**

### Anti-Patterns to Avoid

- [ ] **NOT writing extra code "just in case"**
  - ❌ Don't add features not tested
  - ❌ Don't optimize prematurely
  - ❌ Don't refactor during GREEN phase

- [ ] **NOT skipping test execution**
  - ❌ Don't assume test passes
  - ❌ Must actually run test
  - ❌ Must see green output

---

## REFACTOR Phase Checklist

### Code Improvement

- [ ] **Tests still pass BEFORE refactoring**
  - ✅ All tests green
  - ✅ Coverage stable
  - ✅ No failures

- [ ] **Refactoring improves code quality**
  - Remove duplication
  - Improve naming
  - Simplify logic
  - Extract methods/functions
  - Add type hints

- [ ] **Refactoring does NOT change behavior**
  - ⚠️ CRITICAL: Tests must still pass
  - No new features added
  - No behavior changes
  - Only internal improvements

- [ ] **Tests still pass AFTER refactoring**
  - ✅ All tests green
  - ✅ Same number of tests
  - ✅ Coverage maintained or improved

### Refactoring Targets

- [ ] **Duplication removed**
  - No repeated code
  - Common logic extracted
  - DRY principle applied

- [ ] **Names improved**
  - Variables clear
  - Functions descriptive
  - Classes well-named

- [ ] **Complexity reduced**
  - Cyclomatic complexity < 10
  - Nested levels < 3
  - Functions < 20 lines

- [ ] **Documentation added**
  - Docstrings present
  - Type hints added
  - Comments where needed

### REFACTOR Phase Verification

```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest --cov=app --cov-report=term-missing tests/
```

- [ ] **All tests pass**
- [ ] **Coverage maintained or improved**
- [ ] **Code quality improved**

---

## Cycle Completion Checklist

### After Each RED-GREEN-REFACTOR Cycle

- [ ] **Cycle completed successfully**
  - RED: Test failed for right reason
  - GREEN: Minimal code made test pass
  - REFACTOR: Code improved without breaking tests

- [ ] **All tests passing**
  - Current test passes
  - Previous tests still pass
  - No regressions

- [ ] **Code committed (optional)**
  - If using git, commit after each cycle
  - Clear commit message
  - Green tests in commit

### Ready for Next Cycle

- [ ] **Current functionality complete**
- [ ] **Next test identified**
- [ ] **Ready to write next failing test**

---

## Session-Level Checklist

### During Session

- [ ] **Following TDD cycle strictly**
  - Always RED → GREEN → REFACTOR
  - Never GREEN → RED (code first)
  - Never skip RED (test first)

- [ ] **Writing tests first**
  - ⚠️ CRITICAL: Test before implementation
  - No production code without failing test
  - No "I'll test it later"

- [ ] **Running tests frequently**
  - After writing test (RED)
  - After minimal implementation (GREEN)
  - After refactoring (still GREEN)
  - Every 2-5 minutes

- [ ] **Committing regularly**
  - After each cycle (optional)
  - After significant milestone
  - Always with passing tests

### Discipline Check

- [ ] **Have I written ANY production code without a failing test?**
  - If YES → ⚠️ Stop and delete that code
  - Write test first

- [ ] **Have I written MORE code than needed to pass the test?**
  - If YES → ⚠️ Consider if it's tested
  - Remove untested code or add tests

- [ ] **Have I refactored while tests were failing?**
  - If YES → ⚠️ Revert and fix tests first
  - Only refactor when green

---

## End of Session Checklist

### Session Completion

- [ ] **All tests passing**
  - No failing tests
  - No skipped tests (unless intentional)
  - No warnings

- [ ] **Coverage goals met**
  - Line coverage ≥ 80%
  - Branch coverage ≥ 75%
  - All critical paths tested

- [ ] **Code quality maintained**
  - No duplication
  - Clear naming
  - Low complexity
  - Well-documented

- [ ] **Clean state**
  - No uncommitted changes (if using git)
  - No debug code left
  - No commented-out code

### Retrospective

- [ ] **TDD discipline maintained?**
  - Followed RED-GREEN-REFACTOR?
  - Wrote tests first?
  - Kept implementation minimal?

- [ ] **Challenges encountered?**
  - What was difficult?
  - Where did discipline slip?
  - How to improve next time?

- [ ] **Lessons learned?**
  - What worked well?
  - What to do differently?
  - Any new insights?

---

## Common Discipline Failures

### ❌ Writing Production Code First

**Symptom**: Code exists before test
**Impact**: Not doing TDD
**Fix**: Delete code, write test first

### ❌ Writing Too Much Code in GREEN

**Symptom**: Code does more than test requires
**Impact**: Untested code, overengineering
**Fix**: Remove extra code or add tests

### ❌ Refactoring Before Green

**Symptom**: Improving code while tests fail
**Impact**: Can't verify refactoring is safe
**Fix**: Get to green first, then refactor

### ❌ Not Running Tests

**Symptom**: Assuming tests pass
**Impact**: False confidence, hidden failures
**Fix**: Run tests after every change

### ❌ Skipping RED Phase

**Symptom**: Test passes immediately
**Impact**: Test might not be testing anything
**Fix**: Verify test fails first

### ❌ Large TDD Cycles

**Symptom**: Writing many tests before implementation
**Impact**: Not following cycle discipline
**Fix**: One test at a time

---

## TDD Mantras

### Core Principles

1. **"Red, Green, Refactor"**
   - Always in this order
   - Never skip a phase
   - Complete each phase

2. **"Test First, Code Second"**
   - Always write test before code
   - No exceptions
   - No shortcuts

3. **"Make It Fail, Make It Pass, Make It Better"**
   - RED: Write failing test
   - GREEN: Minimal code to pass
   - REFACTOR: Improve quality

4. **"One Behavior Per Test"**
   - Each test focuses on one thing
   - Clear what's being tested
   - Easy to understand failures

5. **"Simplest Thing That Could Possibly Work"**
   - Don't overcomplicate
   - Minimal implementation
   - Refactor later if needed

### Discipline Reminders

- **"If in doubt, test it"**
- **"When tests pass, don't add code"**
- **"When tests fail, don't refactor"**
- **"Run tests constantly"**
- **"Keep cycles short (< 10 minutes)"**

---

## Quick Reference Card

### The TDD Cycle

```
1. RED:      Write failing test
             ↓
2. GREEN:    Minimal code to pass
             ↓
3. REFACTOR: Improve code quality
             ↓
             Repeat
```

### Phase Rules

**RED Phase**:
- Write test FIRST
- Test MUST fail
- Fail for RIGHT reason

**GREEN Phase**:
- MINIMAL code only
- Test MUST pass
- Don't refactor yet

**REFACTOR Phase**:
- Tests MUST stay green
- Improve code quality
- No new features

### Essential Commands

```bash
# Run single test (RED/GREEN check)
pytest tests/test_module.py::test_name -v

# Run all tests (REFACTOR check)
pytest tests/ -v

# Check coverage
pytest --cov=app --cov-report=term-missing tests/
```

---

**Version**: 1.0
**Last Updated**: 2024-01-15
