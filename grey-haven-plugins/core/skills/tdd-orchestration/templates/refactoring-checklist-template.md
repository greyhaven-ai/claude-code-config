# Refactoring Safety Checklist

**Date**: YYYY-MM-DD
**Developer**: [Your Name]
**Module**: [Module Name]
**Refactoring Goal**: [What you want to improve]

---

## Pre-Refactoring Safety Checks

### 1. Test Coverage Verification

```bash
$ pytest --cov=[module] tests/

Name                    Stmts   Miss  Cover
-------------------------------------------
[module].py              [X]    [X]   [X]%
-------------------------------------------
```

- [ ] **Line coverage**: ≥80% (Current: [X]%)
- [ ] **Branch coverage**: ≥75% (Current: [X]%)
- [ ] **All tests passing**: [X]/[X] tests pass
- [ ] **No flaky tests**: All tests consistently pass

**Status**: [✅ Ready | ⚠️ Needs Improvement | ❌ Not Safe]

---

### 2. Version Control Safety

```bash
$ git status
```

- [ ] **Working directory clean**: No uncommitted changes
- [ ] **On correct branch**: [branch name]
- [ ] **Latest changes pulled**: `git pull` completed
- [ ] **Backup branch created**: `git checkout -b refactor/[name]`

**Status**: [✅ Ready | ⚠️ Needs Action | ❌ Not Safe]

---

### 3. Code Understanding

- [ ] **Purpose understood**: Can explain what this code does
- [ ] **Dependencies mapped**: Know what depends on this code
- [ ] **Side effects identified**: Know all side effects
- [ ] **Edge cases documented**: Aware of boundary conditions

**Code Complexity**:
- Cyclomatic Complexity: [X] (Target: <10)
- Nesting Depth: [X] levels (Target: ≤3)
- Function Length: [X] lines (Target: <50)

**Status**: [✅ Ready | ⚠️ Review Needed | ❌ Not Safe]

---

## Refactoring Pattern Selection

### Selected Pattern: [Pattern Name]

**Patterns to Consider**:
- [ ] **Extract Method**: Break large function into smaller functions
- [ ] **Extract Class**: Separate concerns into distinct classes
- [ ] **Rename Variable**: Improve clarity with better names
- [ ] **Replace Magic Numbers**: Use named constants
- [ ] **Replace Conditional with Polymorphism**: Strategy pattern
- [ ] **Introduce Parameter Object**: Group related parameters
- [ ] **Remove Duplication**: Apply DRY principle
- [ ] **Simplify Conditional**: Reduce complexity
- [ ] **Move Method**: Better location for cohesion
- [ ] **Extract Interface**: Define contracts

**Why This Pattern**:
[Explain why this pattern is appropriate for the refactoring goal]

**Expected Outcome**:
[What will improve: readability, maintainability, testability, performance]

---

## Before Refactoring Snapshot

### Current Code Structure

```python
# [module].py (lines [X]-[Y])
[paste code that will be refactored]
```

### Current Test Coverage

```python
# tests/test_[module].py
[paste relevant tests]
```

### Current Metrics

| Metric | Value |
|--------|-------|
| **Lines of Code** | [X] |
| **Cyclomatic Complexity** | [X] |
| **Nesting Depth** | [X] |
| **Number of Parameters** | [X] |
| **Number of Dependencies** | [X] |

---

## Refactoring Steps

### Step 1: [Step Description]

**Action**: [What to do]

**Expected Result**: [What should happen]

#### Code Change
```python
# Before
[paste before code]

# After
[paste after code]
```

#### Verification
```bash
$ pytest tests/test_[module].py

[Expected: ALL TESTS PASS]
```

- [ ] **Tests pass**: All tests still pass
- [ ] **No new warnings**: No new warnings introduced
- [ ] **Behavior unchanged**: Functionality remains the same

**Status**: [✅ Complete | ⏳ In Progress | ❌ Failed]

---

### Step 2: [Step Description]

**Action**: [What to do]

**Expected Result**: [What should happen]

#### Code Change
```python
# Before
[paste before code]

# After
[paste after code]
```

#### Verification
```bash
$ pytest tests/

[Expected: ALL TESTS PASS]
```

- [ ] **Tests pass**: All tests still pass
- [ ] **Coverage maintained**: Coverage ≥ previous level
- [ ] **No regressions**: No existing functionality broken

**Status**: [✅ Complete | ⏳ In Progress | ❌ Failed]

---

### Step 3: [Step Description]

**Action**: [What to do]

**Expected Result**: [What should happen]

#### Code Change
```python
# Before
[paste before code]

# After
[paste after code]
```

#### Verification
```bash
$ pytest tests/

[Expected: ALL TESTS PASS]
```

- [ ] **Tests pass**: All tests still pass
- [ ] **Design improved**: Code structure better
- [ ] **SOLID principles**: Applied appropriately

**Status**: [✅ Complete | ⏳ In Progress | ❌ Failed]

---

### Step 4: [Step Description]

[Repeat structure for each incremental step]

---

## After Refactoring Snapshot

### New Code Structure

```python
# [module].py
[paste refactored code]
```

### Test Coverage After Refactoring

```bash
$ pytest --cov=[module] tests/

Name                    Stmts   Miss  Cover
-------------------------------------------
[module].py              [X]    [X]   [X]%
-------------------------------------------
```

### New Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Lines of Code** | [X] | [X] | [+/- X] |
| **Cyclomatic Complexity** | [X] | [X] | [+/- X] |
| **Nesting Depth** | [X] | [X] | [+/- X] |
| **Parameters** | [X] | [X] | [+/- X] |
| **Dependencies** | [X] | [X] | [+/- X] |

**Overall Improvement**: [✅ Improved | ➖ No Change | ❌ Worse]

---

## Validation Checklist

### 1. Functional Correctness

- [ ] **All unit tests pass**: [X]/[X] tests passing
- [ ] **All integration tests pass**: [X]/[X] tests passing
- [ ] **Manual testing complete**: Key workflows verified
- [ ] **Edge cases verified**: Boundary conditions tested

**Test Execution**:
```bash
$ pytest tests/ -v

[Paste full test output]
```

**Status**: [✅ Valid | ⚠️ Issues | ❌ Failed]

---

### 2. Coverage Maintenance

- [ ] **Line coverage maintained**: [X]% (was [X]%)
- [ ] **Branch coverage maintained**: [X]% (was [X]%)
- [ ] **No coverage gaps**: All new code paths tested
- [ ] **Critical paths**: 100% coverage maintained

**Coverage Report**:
```bash
$ pytest --cov=app --cov-report=term-missing tests/

[Paste coverage report]
```

**Status**: [✅ Maintained | ⚠️ Decreased | ❌ Significant Loss]

---

### 3. Code Quality Improvement

- [ ] **Readability improved**: Code easier to understand
- [ ] **Maintainability improved**: Easier to modify
- [ ] **Testability improved**: Easier to test
- [ ] **Complexity reduced**: Lower cyclomatic complexity
- [ ] **Duplication removed**: No repeated code
- [ ] **Clear naming**: Variables/functions well-named
- [ ] **SOLID principles**: Applied appropriately

**Quality Score**: [X]/100 (was [X]/100)

**Status**: [✅ Improved | ➖ Same | ❌ Worse]

---

### 4. Performance Impact

```bash
$ pytest tests/ --durations=10

[Paste slowest test durations]
```

- [ ] **No performance regression**: Tests run in similar time
- [ ] **Response time maintained**: Key operations same speed
- [ ] **Memory usage maintained**: No memory leaks introduced

**Performance Metrics**:
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Test Suite Time** | [X]s | [X]s | [+/- X]s |
| **Slowest Test** | [X]s | [X]s | [+/- X]s |
| **Memory Usage** | [X]MB | [X]MB | [+/- X]MB |

**Status**: [✅ No Impact | ⚠️ Slight Impact | ❌ Regression]

---

### 5. Integration Testing

- [ ] **Local integration tests**: All pass
- [ ] **API contracts**: No breaking changes
- [ ] **Database migrations**: Compatible with changes
- [ ] **Dependencies updated**: If needed

**Integration Test Results**:
```bash
$ pytest tests/integration/

[Paste integration test results]
```

**Status**: [✅ Pass | ⚠️ Issues | ❌ Fail]

---

## SOLID Principles Verification

### Single Responsibility Principle (SRP)

**Before**: [How code violated or followed SRP]

**After**: [How refactoring improved SRP compliance]

- [ ] Each class has one reason to change
- [ ] Each function does one thing

**Status**: [✅ Improved | ➖ Same | ❌ Worse]

---

### Open/Closed Principle (OCP)

**Before**: [How code violated or followed OCP]

**After**: [How refactoring improved OCP compliance]

- [ ] Open for extension
- [ ] Closed for modification

**Status**: [✅ Improved | ➖ Same | ❌ Worse]

---

### Liskov Substitution Principle (LSP)

**Before**: [How code violated or followed LSP]

**After**: [How refactoring improved LSP compliance]

- [ ] Subtypes substitutable for base types
- [ ] Contracts preserved

**Status**: [✅ Improved | ➖ Same | ❌ N/A]

---

### Interface Segregation Principle (ISP)

**Before**: [How code violated or followed ISP]

**After**: [How refactoring improved ISP compliance]

- [ ] Clients not forced to depend on unused interfaces
- [ ] Focused, cohesive interfaces

**Status**: [✅ Improved | ➖ Same | ❌ N/A]

---

### Dependency Inversion Principle (DIP)

**Before**: [How code violated or followed DIP]

**After**: [How refactoring improved DIP compliance]

- [ ] Depends on abstractions, not concretions
- [ ] High-level modules don't depend on low-level modules

**Status**: [✅ Improved | ➖ Same | ❌ N/A]

---

## Rollback Plan

### If Refactoring Fails

**Rollback Command**:
```bash
$ git checkout [original-branch]
# or
$ git reset --hard [commit-hash]
```

**Verification After Rollback**:
- [ ] Tests pass on original branch
- [ ] Code reverted to stable state
- [ ] No artifacts from failed refactoring

### If Tests Break

**Debugging Steps**:
1. Identify which test(s) broke
2. Determine if test is wrong or code is wrong
3. If code is wrong: revert last change
4. If test is wrong: fix test, verify behavior

**Small Step Recovery**:
- [ ] Revert to last passing state
- [ ] Make smaller refactoring steps
- [ ] Run tests after each micro-change

---

## Final Approval Checklist

### Code Review Readiness

- [ ] **All tests passing**: [X]/[X] tests pass
- [ ] **Coverage maintained**: ≥[X]%
- [ ] **Code quality improved**: Metrics better
- [ ] **Commit message clear**: Describes refactoring
- [ ] **No behavior changes**: Functionality same
- [ ] **Documentation updated**: If needed
- [ ] **Ready for review**: Clean, understandable changes

### Commit Information

**Commit Message**:
```
refactor: [brief description]

- [Detail 1]
- [Detail 2]
- [Detail 3]

Before: [metric] = [value]
After: [metric] = [value]
```

**Git Commands**:
```bash
$ git add [files]
$ git commit -m "refactor: [message]"
$ git push origin [branch]
```

---

## Post-Refactoring Actions

### Documentation Updates

- [ ] **Code comments**: Updated if needed
- [ ] **README**: Updated if API changed
- [ ] **Architecture docs**: Updated if structure changed
- [ ] **Team wiki**: Updated if patterns changed

### Team Communication

- [ ] **PR created**: [Link to PR]
- [ ] **Team notified**: [How notified]
- [ ] **Knowledge shared**: [How shared]

### Follow-up Tasks

- [ ] **[Task 1]**: [Description]
- [ ] **[Task 2]**: [Description]
- [ ] **[Task 3]**: [Description]

---

## Lessons Learned

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

## Summary

**Refactoring Status**: [✅ Complete | ⏳ In Progress | ❌ Rolled Back]

**Outcome**: [Brief summary of what was achieved]

**Quality Improvement**: [How code quality improved]

**Time Spent**: [X min]

**Ready for**: [Code Review | Merge | Further Refactoring]

---

**Checklist Completed**: [Date]
**Checklist Version**: 1.0
**Template Version**: 1.0
