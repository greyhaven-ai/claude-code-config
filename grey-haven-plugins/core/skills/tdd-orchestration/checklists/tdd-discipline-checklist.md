# TDD Discipline Checklist

Comprehensive checklist for ensuring test-first discipline throughout RED-GREEN-REFACTOR cycles.

**Purpose**: Maintain strict TDD discipline, prevent test-after development, ensure quality at every step.

---

## Pre-Session Setup

### Development Environment

- [ ] **Test framework installed**: pytest, Jest, JUnit, etc.
- [ ] **Coverage tool available**: coverage.py, Istanbul, JaCoCo
- [ ] **Mutation testing tool**: mutmut, Stryker, PITest (optional)
- [ ] **Editor/IDE configured**: Test runner integrated
- [ ] **Git repository clean**: No uncommitted changes

### Test Infrastructure

- [ ] **Test directory exists**: `tests/` or appropriate location
- [ ] **Test utilities available**: Fixtures, factories, mocks
- [ ] **Test data prepared**: Sample data for tests
- [ ] **Continuous testing**: Watch mode or auto-run configured

### Session Planning

- [ ] **Goal defined**: Clear objective for session
- [ ] **Behaviors identified**: List of behaviors to implement
- [ ] **Priority ordered**: Starting with simplest behavior
- [ ] **Time allocated**: Realistic estimate (15-35 min/cycle)
- [ ] **Distractions minimized**: Focus time blocked

**Status**: [✅ Ready | ⏳ Setup Needed]

---

## Cycle Discipline

For each RED-GREEN-REFACTOR cycle, complete all sections:

---

## 🔴 RED Phase Checklist (3-10 min)

### Step 1: Identify Behavior

- [ ] **Single behavior**: One specific behavior identified
- [ ] **Smallest step**: Simplest possible behavior chosen
- [ ] **Not implementation**: Focus on WHAT, not HOW
- [ ] **Clear acceptance**: Know what "done" looks like

**Behavior**: [Describe the behavior]

---

### Step 2: Write Test FIRST

**⚠️ CRITICAL**: NO PRODUCTION CODE YET!

- [ ] **Test written**: Complete test code written
- [ ] **No implementation**: Production code does NOT exist
- [ ] **AAA pattern**: Arrange-Act-Assert structure
- [ ] **Descriptive name**: `test_[behavior_description]`
- [ ] **Clear assertions**: Specific, measurable expectations
- [ ] **Single behavior**: Tests only ONE thing

**Test File**: [Filename and line numbers]

---

### Step 3: Verify Test Fails

```bash
$ pytest tests/test_[module].py::test_[behavior]
```

- [ ] **Test executed**: Ran the test
- [ ] **Test FAILS**: Test fails as expected
- [ ] **Right reason**: Fails because code doesn't exist (not syntax error)
- [ ] **Error message**: Clear, helpful error message
- [ ] **No false positives**: Test would pass if code existed

**Failure Output**: [Paste error message]

**Status**: [✅ RED | ⚠️ Need Fix | ❌ Passed - DANGER!]

---

### Step 4: Test Quality Verification

- [ ] **Descriptive name**: Name describes behavior clearly
- [ ] **Single assertion**: Ideally 1-3 related assertions
- [ ] **Fast execution**: Test runs in <1 second
- [ ] **Deterministic**: Same result every time
- [ ] **Independent**: Doesn't depend on other tests
- [ ] **Isolated**: Uses mocks for external dependencies
- [ ] **Readable**: Easy to understand what's being tested

**Test Quality Score**: [X]/7

**Status**: [✅ High Quality | ⚠️ Acceptable | ❌ Needs Improvement]

---

## 🟢 GREEN Phase Checklist (5-15 min)

### Step 1: Write MINIMAL Implementation

**⚠️ CRITICAL**: Write ONLY enough code to pass the test!

- [ ] **Minimal code**: Absolute minimum to pass test
- [ ] **No extras**: No features test doesn't require
- [ ] **No optimization**: No premature optimization
- [ ] **No error handling**: Unless test demands it
- [ ] **No logging**: Unless test demands it
- [ ] **No comments**: Unless absolutely necessary

**Implementation Strategy**: [Fake It | Obvious Implementation | Triangulation]

---

### Step 2: Run Test - Should Pass

```bash
$ pytest tests/test_[module].py::test_[behavior]
```

- [ ] **Test executed**: Ran the test
- [ ] **Test PASSES**: Test now passes
- [ ] **Right reason**: Passes because implementation works
- [ ] **No warnings**: No new warnings introduced

**Status**: [✅ GREEN | ⚠️ Still Failing - Debug]

---

### Step 3: Run All Tests - No Regressions

```bash
$ pytest tests/
```

- [ ] **All tests executed**: Full test suite ran
- [ ] **All tests pass**: No existing tests broken
- [ ] **No new failures**: No regressions introduced
- [ ] **Execution time**: No significant slowdown

**Test Results**: [X passed, Y failed]

**Status**: [✅ All Pass | ❌ Regressions - Fix First]

---

### Step 4: Resist Over-Engineering

**Check for anti-patterns**:

- [ ] **No extra features**: Only implemented tested behavior
- [ ] **No abstractions**: Unless multiple tests demand it
- [ ] **No frameworks**: Unless actually needed
- [ ] **No design patterns**: Unless tests drove the need
- [ ] **No "future-proofing"**: YAGNI (You Aren't Gonna Need It)

**Over-Engineering Score**: [0 = None, 5 = Lots]

**Status**: [✅ Minimal | ⚠️ Some Extras | ❌ Over-Engineered]

---

### Step 5: Commit (Optional)

```bash
$ git add -A
$ git commit -m "feat: [behavior description]"
```

- [ ] **Tests included**: Test file committed
- [ ] **Implementation included**: Production code committed
- [ ] **Descriptive message**: Commit message clear
- [ ] **Tests passing**: All tests pass at commit

**Status**: [✅ Committed | ⏳ Will Commit After Refactor]

---

## 🔵 REFACTOR Phase Checklist (5-10 min)

### Step 1: Identify Improvements

**Code smells detected**:

- [ ] **Duplication**: Repeated code (DRY violation)
- [ ] **Long function**: Function >50 lines
- [ ] **Deep nesting**: Nesting >3 levels
- [ ] **Many parameters**: >4 parameters
- [ ] **Complex conditionals**: Nested if/else
- [ ] **Poor naming**: Unclear variable/function names
- [ ] **Magic numbers**: Hardcoded values
- [ ] **God class**: Class with too many responsibilities

**Refactoring Needed**: [Describe what to improve]

**Refactoring Pattern**: [Extract Method | Extract Class | etc.]

---

### Step 2: Refactor in Small Steps

**⚠️ CRITICAL**: Change ONE thing at a time!

#### Refactoring Step 1

- [ ] **Change identified**: Clear what to change
- [ ] **Small change**: Single refactoring action
- [ ] **Code modified**: Refactoring applied
- [ ] **Tests run**: All tests still pass
- [ ] **Behavior unchanged**: No functionality changed

**Status**: [✅ Complete | ❌ Tests Broke - Revert]

#### Refactoring Step 2

- [ ] **Change identified**: Next refactoring
- [ ] **Tests pass**: After this change
- [ ] **Behavior unchanged**: No functionality changed

**Status**: [✅ Complete | ❌ Tests Broke - Revert]

#### Refactoring Step 3

[Continue for each incremental refactoring]

---

### Step 3: Verify No Behavior Change

**⚠️ CRITICAL**: Refactoring = SAME behavior, BETTER design!

- [ ] **All tests pass**: Every single test passes
- [ ] **Same output**: Functionality unchanged
- [ ] **No new tests**: Didn't add new behavior
- [ ] **No skipped tests**: Didn't disable tests

```bash
$ pytest tests/
```

**Test Results**: [X passed]

**Status**: [✅ Behavior Preserved | ❌ Behavior Changed - Revert]

---

### Step 4: Verify Design Improvement

- [ ] **Readability**: Code easier to read
- [ ] **Maintainability**: Code easier to modify
- [ ] **Testability**: Code easier to test
- [ ] **Complexity**: Cyclomatic complexity reduced
- [ ] **SOLID**: Principles applied appropriately
- [ ] **DRY**: No code duplication
- [ ] **Clear intent**: Purpose obvious

**Design Improvement**: [How code improved]

**Status**: [✅ Improved | ➖ No Change | ❌ Worse - Revert]

---

### Step 5: Verify Coverage Maintained

```bash
$ pytest --cov=app tests/
```

- [ ] **Coverage maintained**: Coverage ≥ previous level
- [ ] **No gaps**: All code paths covered
- [ ] **Critical paths**: 100% coverage maintained

**Coverage**: [X]% (was [Y]%)

**Status**: [✅ Maintained | ⚠️ Decreased]

---

### Step 6: Commit

```bash
$ git add -A
$ git commit -m "refactor: [improvement description]"
```

- [ ] **Changes committed**: Refactoring committed
- [ ] **Descriptive message**: Clear what improved
- [ ] **Tests passing**: All tests pass
- [ ] **Clean history**: Logical commit

**Status**: [✅ Committed]

---

## Post-Cycle Review

### Cycle Metrics

**Cycle #**: [X]
**Total Time**: [X min]
- RED: [X min]
- GREEN: [X min]
- REFACTOR: [X min]

**Tests Added**: [X]
**Tests Passing**: [X]/[X]
**Coverage**: [X]%

**Status**: [✅ Complete | ⏳ Continuing]

---

### Discipline Score

Calculate discipline score for this cycle:

**RED Phase**:
- Test written first? [Yes=10pts | No=0pts]
- Test failed correctly? [Yes=10pts | No=0pts]
- Quality test? [Yes=10pts | No=0pts]

**GREEN Phase**:
- Minimal implementation? [Yes=10pts | No=0pts]
- All tests pass? [Yes=10pts | No=0pts]
- No over-engineering? [Yes=10pts | No=0pts]

**REFACTOR Phase**:
- Small steps? [Yes=10pts | No=0pts]
- Tests still pass? [Yes=10pts | No=0pts]
- Behavior unchanged? [Yes=10pts | No=0pts]
- Design improved? [Yes=10pts | No=0pts]

**Total Score**: [X]/100

**Rating**:
- 90-100: Excellent TDD discipline
- 75-89: Good discipline, minor lapses
- 60-74: Acceptable, needs improvement
- <60: Poor discipline, review fundamentals

---

## End of Session Review

### Session Summary

**Date**: [YYYY-MM-DD]
**Duration**: [X hours X min]
**Cycles Completed**: [X]
**Tests Written**: [X]
**Tests Passing**: [X]
**Coverage**: [X]%

---

### Discipline Compliance

**Test-First Discipline**:
- [ ] All tests written BEFORE implementation
- [ ] All tests failed correctly before GREEN
- [ ] No production code without failing test

**Compliance Rate**: [X]/[X] cycles (100% target)

**Status**: [✅ Perfect | ⚠️ Some Lapses | ❌ Frequent Violations]

---

### RED Phase Compliance

- [ ] **Tests written first**: [X]/[X] cycles
- [ ] **Tests failed correctly**: [X]/[X] cycles
- [ ] **Quality tests**: [X]/[X] cycles

**RED Compliance**: [X]%

---

### GREEN Phase Compliance

- [ ] **Minimal implementation**: [X]/[X] cycles
- [ ] **All tests passed**: [X]/[X] cycles
- [ ] **No over-engineering**: [X]/[X] cycles

**GREEN Compliance**: [X]%

---

### REFACTOR Phase Compliance

- [ ] **Small steps**: [X]/[X] cycles
- [ ] **Tests kept passing**: [X]/[X] cycles
- [ ] **Behavior preserved**: [X]/[X] cycles
- [ ] **Design improved**: [X]/[X] cycles

**REFACTOR Compliance**: [X]%

---

### Overall Discipline Score

**Average Cycle Score**: [X]/100

**Session Rating**:
- 90-100: Excellent - exemplary TDD discipline
- 75-89: Good - minor areas for improvement
- 60-74: Acceptable - needs attention
- <60: Poor - review TDD fundamentals

---

### Violations Log

**Violation #1**: [Description]
- Cycle: [X]
- Phase: [RED | GREEN | REFACTOR]
- Impact: [How it affected quality]
- Lesson: [What to do differently]

**Violation #2**: [Description]
- Cycle: [X]
- Phase: [RED | GREEN | REFACTOR]
- Impact: [How it affected quality]
- Lesson: [What to do differently]

---

### Action Items

**To Improve Discipline**:
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

**To Improve Process**:
- [ ] [Action 1]
- [ ] [Action 2]

---

## Anti-Pattern Detection

### Test-After Development (CRITICAL)

- [ ] **No production code before tests**: All code test-driven
- [ ] **No "I'll test it later"**: Tests written immediately
- [ ] **No skipped test phases**: Complete RED-GREEN-REFACTOR

**Detected**: [Yes ⚠️ | No ✅]

---

### Over-Engineering (WARNING)

- [ ] **No unnecessary abstractions**: Only what tests demand
- [ ] **No premature optimization**: Only when needed
- [ ] **No "future-proofing"**: YAGNI applied

**Detected**: [Yes ⚠️ | No ✅]

---

### Refactoring Without Tests (CRITICAL)

- [ ] **Tests pass before refactoring**: All green before refactor
- [ ] **Tests pass after refactoring**: All green after refactor
- [ ] **No behavior changes**: Functionality unchanged

**Detected**: [Yes ⚠️ | No ✅]

---

### Large Steps (WARNING)

- [ ] **Cycles <35 minutes**: Each cycle reasonable
- [ ] **Small behaviors**: Incremental progress
- [ ] **Frequent commits**: Regular checkpoints

**Detected**: [Yes ⚠️ | No ✅]

---

## Final Checklist

### Before Ending Session

- [ ] **All tests passing**: [X]/[X] tests pass
- [ ] **All changes committed**: Clean working directory
- [ ] **Coverage recorded**: Metrics captured
- [ ] **Discipline scored**: Compliance calculated
- [ ] **Learnings documented**: Insights captured
- [ ] **Action items created**: Improvements identified

---

**Session Completed**: [Date and Time]
**Next Session Planned**: [Date and Time]
**Checklist Version**: 1.0
