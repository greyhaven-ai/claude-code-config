# TDD Workflow Template

Step-by-step template for Test-Driven Development sessions in Python.

**Session**: [Feature Name]
**Date**: [YYYY-MM-DD]
**Duration**: [Estimated time]
**Framework**: pytest / unittest

---

## Pre-Session Setup

### 1. Define Goal

**Feature**: [Brief description of what you're building]

**User Story** (optional):
```
As a [user type]
I want to [action]
So that [benefit]
```

**Acceptance Criteria**:
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

### 2. Identify Test Cases

| Test Case | Input | Expected Output | Priority |
|-----------|-------|-----------------|----------|
| Happy path | [example] | [result] | High |
| Edge case 1 | [example] | [result] | High |
| Edge case 2 | [example] | [result] | Medium |
| Error case | [example] | [exception] | Medium |

### 3. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install pytest pytest-cov

# Verify setup
pytest --version
```

---

## TDD Cycle Template

### Cycle 1: [Test Name]

#### RED - Write Failing Test

**Test Code**:
```python
# tests/test_[module].py
def test_[feature]_[scenario]():
    """Should [expected behavior]."""
    # Arrange
    [setup code]

    # Act
    result = [function call]

    # Assert
    assert result == [expected]
```

**Run Test**:
```bash
pytest tests/test_[module].py::test_[feature]_[scenario] -v
```

**Expected**: ❌ FAIL (function/class not defined)

**Status**: [ ] Red phase complete

---

#### GREEN - Minimal Implementation

**Implementation Code**:
```python
# app/[module].py
def [function_name]([parameters]):
    """[Docstring]."""
    # Minimal code to pass test
    return [minimal implementation]
```

**Run Test**:
```bash
pytest tests/test_[module].py::test_[feature]_[scenario] -v
```

**Expected**: ✅ PASS

**Status**: [ ] Green phase complete

---

#### REFACTOR - Improve Code

**Refactoring Checklist**:
- [ ] Remove duplication
- [ ] Improve naming
- [ ] Extract methods/functions
- [ ] Add type hints
- [ ] Add docstrings
- [ ] Simplify logic

**Refactored Code**:
```python
# [Before → After comparison]
```

**Run Tests**:
```bash
pytest tests/test_[module].py -v
```

**Expected**: ✅ All tests still pass

**Status**: [ ] Refactor phase complete

---

### Cycle 2: [Test Name]

#### RED - Write Failing Test

```python
def test_[feature]_[next_scenario]():
    """Should [expected behavior]."""
    # Arrange
    [setup]

    # Act
    result = [call]

    # Assert
    assert result == [expected]
```

**Status**: [ ] Red phase complete

---

#### GREEN - Minimal Implementation

```python
# Update existing implementation
def [function_name]([parameters]):
    """[Updated docstring]."""
    [implementation]
```

**Status**: [ ] Green phase complete

---

#### REFACTOR - Improve Code

**Refactoring Notes**: [What you changed and why]

**Status**: [ ] Refactor phase complete

---

### Cycle 3: [Test Name]

[Repeat RED-GREEN-REFACTOR pattern]

---

## Coverage Check

### Run Coverage Report

```bash
pytest --cov=app --cov-report=term-missing tests/
```

### Coverage Results

```
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app/[module].py      XX     XX    XX%   [lines]
-----------------------------------------------
TOTAL                XX     XX    XX%
```

**Coverage Goal**: [Target %]
**Actual Coverage**: [Actual %]
**Status**: [ ] Meets goal / [ ] Needs improvement

### Missing Coverage

**Untested Lines**: [Line numbers]
**Reason**: [Why these lines aren't tested]
**Action**: [ ] Add tests / [ ] Mark as no cover / [ ] Remove dead code

---

## Final Checks

### Test Quality

- [ ] All tests pass
- [ ] Tests are independent (can run in any order)
- [ ] Tests are fast (< 1s per test)
- [ ] Tests have descriptive names
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] No test duplication
- [ ] Edge cases covered
- [ ] Error cases tested

### Code Quality

- [ ] No code duplication
- [ ] Clear naming (variables, functions, classes)
- [ ] Type hints added
- [ ] Docstrings added
- [ ] Follows style guide (PEP 8)
- [ ] No complex nested logic (max 3 levels)
- [ ] Functions are small (< 20 lines)

### Documentation

- [ ] README updated (if new feature)
- [ ] API documentation updated
- [ ] Examples added
- [ ] Changelog updated

---

## Session Summary

### Statistics

- **Total Time**: [Actual duration]
- **TDD Cycles**: [Number of cycles]
- **Tests Written**: [Number]
- **Tests Passing**: [Number]
- **Coverage**: [Final %]
- **Lines of Code**: [Implementation + Tests]

### What Went Well

1. [Success 1]
2. [Success 2]
3. [Success 3]

### Challenges

1. [Challenge 1] → [How you solved it]
2. [Challenge 2] → [How you solved it]

### Lessons Learned

1. [Lesson 1]
2. [Lesson 2]

### Next Steps

- [ ] [Next feature or refactoring]
- [ ] [Tech debt to address]
- [ ] [Performance optimization]

---

## Notes

[Any additional notes, observations, or reminders for next session]

---

## Example: Completed Session

### Session: Shopping Cart Discount Calculator

**Date**: 2024-01-15
**Duration**: 45 minutes
**Framework**: pytest

#### Cycle 1: Add Item
- ✅ RED: Test for adding item (FAIL - no function)
- ✅ GREEN: Implemented add_item() (PASS)
- ✅ REFACTOR: Extracted Item class

#### Cycle 2: Calculate Subtotal
- ✅ RED: Test for subtotal calculation (FAIL)
- ✅ GREEN: Implemented get_subtotal() (PASS)
- ✅ REFACTOR: Used sum() + list comprehension

#### Cycle 3: 10% Discount
- ✅ RED: Test for 10% discount over $100 (FAIL)
- ✅ GREEN: Added discount logic (PASS)
- ✅ REFACTOR: Extracted calculate_discount() method

#### Cycle 4: 20% Discount
- ✅ RED: Test for 20% discount over $200 (FAIL)
- ✅ GREEN: Updated discount logic (PASS)
- ✅ REFACTOR: Simplified discount calculation

#### Cycle 5: Fixtures
- ✅ RED: DRY tests with fixtures (REFACTOR ONLY)
- ✅ GREEN: N/A (tests already pass)
- ✅ REFACTOR: Created cart fixture

#### Final Results:
- **Tests**: 18 tests, all passing
- **Coverage**: 95% line, 92% branch
- **Duration**: 45 minutes (on target)
- **Lines**: 72 implementation + 156 test code

**Lessons Learned**:
1. Parametrize decorator reduced test duplication significantly
2. Early refactoring prevented complex nested conditions
3. Fixtures made tests much more readable

---

**Template Version**: 1.0
**Last Updated**: 2024-01-15
