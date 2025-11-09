# TDD Workflow: [Feature Name]

**Date**: YYYY-MM-DD
**Developer**: [Your Name]
**Duration**: [Total Time]
**Cycles Completed**: [Number]

---

## Feature Description

**User Story**: [As a ... I want to ... so that ...]

**Acceptance Criteria**:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

**TDD Approach**: [Chicago School | London School | Outside-In | Inside-Out | ATDD | BDD | Hexagonal]

---

## Cycle 1: [Behavior Name]

### 🔴 RED Phase (3-10 min)

**Start Time**: [HH:MM]
**Duration**: [X min]

#### Behavior to Test
[Describe the smallest next behavior to implement]

#### Test Code
```python
# tests/test_[module].py
def test_[behavior_description]():
    """[Test description - what behavior is being verified]"""
    # Arrange
    [setup test data]

    # Act
    [execute behavior]

    # Assert
    [verify expected result]
```

#### Test Execution
```bash
$ pytest tests/test_[module].py::test_[behavior_description]

[Paste test output - should FAIL]
```

#### Quality Checklist
- [ ] Test fails for right reason (code doesn't exist)
- [ ] Test name describes behavior
- [ ] Single behavior per test
- [ ] Clear, specific assertions
- [ ] Fast execution (<1s)
- [ ] Independent (no dependencies on other tests)
- [ ] Follows AAA pattern (Arrange-Act-Assert)

---

### 🟢 GREEN Phase (5-15 min)

**Start Time**: [HH:MM]
**Duration**: [X min]

#### Implementation Strategy
[Fake It | Obvious Implementation | Triangulation]

#### Implementation Code
```python
# app/[module].py
[paste minimal implementation that makes test pass]
```

#### Test Execution
```bash
$ pytest tests/test_[module].py::test_[behavior_description]

[Paste test output - should PASS]
```

#### All Tests Execution
```bash
$ pytest tests/

[Paste output - all tests should PASS]
```

#### Quality Checklist
- [ ] Test passes
- [ ] All existing tests still pass
- [ ] Minimal implementation (no over-engineering)
- [ ] No premature optimization
- [ ] No untested features added

---

### 🔵 REFACTOR Phase (5-10 min)

**Start Time**: [HH:MM]
**Duration**: [X min]

#### Refactoring Needed
[Describe what needs improvement]

**Refactoring Pattern**: [Extract Method | Extract Class | Replace Conditional | Parameter Object | etc.]

#### Before Refactoring
```python
[paste code before refactoring]
```

#### After Refactoring
```python
[paste code after refactoring]
```

#### Test Execution
```bash
$ pytest tests/

[Paste output - all tests should still PASS]
```

#### Quality Checklist
- [ ] All tests still pass
- [ ] Behavior unchanged (no new functionality)
- [ ] Code quality improved
- [ ] No duplication (DRY)
- [ ] Clear naming
- [ ] SOLID principles applied

---

### Cycle 1 Summary

**Total Cycle Time**: [X min]
**Status**: ✅ Complete

**Key Learnings**:
- [Learning 1]
- [Learning 2]

---

## Cycle 2: [Behavior Name]

### 🔴 RED Phase (3-10 min)

**Start Time**: [HH:MM]
**Duration**: [X min]

#### Behavior to Test
[Describe the smallest next behavior to implement]

#### Test Code
```python
def test_[behavior_description]():
    """[Test description]"""
    # Arrange

    # Act

    # Assert
```

#### Test Execution
```bash
$ pytest tests/test_[module].py::test_[behavior_description]

[Should FAIL]
```

#### Quality Checklist
- [ ] Test fails for right reason
- [ ] Test name describes behavior
- [ ] Single behavior per test
- [ ] Clear assertions
- [ ] Fast execution
- [ ] Independent
- [ ] AAA pattern

---

### 🟢 GREEN Phase (5-15 min)

**Start Time**: [HH:MM]
**Duration**: [X min]

#### Implementation Code
```python
[paste minimal implementation]
```

#### Test Execution
```bash
$ pytest tests/

[All tests should PASS]
```

#### Quality Checklist
- [ ] Test passes
- [ ] All tests pass
- [ ] Minimal implementation
- [ ] No over-engineering

---

### 🔵 REFACTOR Phase (5-10 min)

**Start Time**: [HH:MM]
**Duration**: [X min]

#### Refactoring Needed
[Describe improvements]

#### After Refactoring
```python
[paste refactored code]
```

#### Test Execution
```bash
$ pytest tests/

[All tests should still PASS]
```

#### Quality Checklist
- [ ] All tests pass
- [ ] Behavior unchanged
- [ ] Code quality improved

---

### Cycle 2 Summary

**Total Cycle Time**: [X min]
**Status**: ✅ Complete

---

## Cycle 3: [Behavior Name]

[Repeat RED-GREEN-REFACTOR structure]

---

## Cycle 4: [Behavior Name]

[Repeat RED-GREEN-REFACTOR structure]

---

## Session Metrics

### Time Spent
| Phase | Cycle 1 | Cycle 2 | Cycle 3 | Cycle 4 | Total |
|-------|---------|---------|---------|---------|-------|
| RED   | [X min] | [X min] | [X min] | [X min] | [X min] |
| GREEN | [X min] | [X min] | [X min] | [X min] | [X min] |
| REFACTOR | [X min] | [X min] | [X min] | [X min] | [X min] |
| **Total** | [X min] | [X min] | [X min] | [X min] | **[X min]** |

**Average Cycle Time**: [X min]

### Coverage Metrics

```bash
$ pytest --cov=app tests/

---------- coverage: platform [platform], python [version] ----------
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py            0      0   100%
app/[module].py           [X]    [X]   [X]%
-------------------------------------------
TOTAL                     [X]    [X]   [X]%
```

**Line Coverage**: [X]%
**Branch Coverage**: [X]%
**Function Coverage**: [X]%

### Mutation Testing

```bash
$ mutmut run --paths-to-mutate app/

[Paste mutation testing results]
```

**Mutation Score**: [X]%
**Killed Mutants**: [X]
**Survived Mutants**: [X]
**Timeouts**: [X]

---

## Test Quality Analysis

### Strengths
- [What worked well in tests]
- [Good patterns observed]

### Weaknesses
- [What could be improved]
- [Gaps in test coverage]

### Action Items
- [ ] [Improvement 1]
- [ ] [Improvement 2]
- [ ] [Improvement 3]

---

## Code Quality Analysis

### Design Improvements
- [What design patterns emerged]
- [How code structure improved]

### Refactoring Applied
1. **[Pattern Name]**: [Where applied and why]
2. **[Pattern Name]**: [Where applied and why]

### Technical Debt
- [Any remaining debt]
- [Plan to address it]

---

## Learnings and Insights

### What Went Well
- [Success 1]
- [Success 2]

### What Could Be Improved
- [Challenge 1]
- [Challenge 2]

### Key Takeaways
- [Insight 1]
- [Insight 2]

---

## Next Steps

### Remaining Behaviors
1. [ ] [Next behavior to implement]
2. [ ] [Behavior after that]
3. [ ] [Future behavior]

### Technical Improvements
- [ ] [Improvement 1]
- [ ] [Improvement 2]

---

## Final Summary

**Feature Status**: [Complete | In Progress | Blocked]
**Total Cycles**: [X]
**Total Time**: [X hours X min]
**Tests Written**: [X]
**Tests Passing**: [X]
**Line Coverage**: [X]%
**Mutation Score**: [X]%

**Ready for**: [Code Review | Integration Testing | Deployment]

---

## Appendix: Test Output

### Full Test Suite Output
```bash
$ pytest tests/ -v

[Paste full test output]
```

### Coverage Report
```bash
$ pytest --cov=app --cov-report=term-missing tests/

[Paste detailed coverage report]
```

### Mutation Testing Details
```bash
$ mutmut results
$ mutmut show [id]

[Paste mutation details]
```

---

**Template Version**: 1.0
**Last Updated**: 2025-01-07
