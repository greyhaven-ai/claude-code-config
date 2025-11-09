# Quality Gates Checklist

Comprehensive quality gates for coverage thresholds, mutation scores, and production readiness.

**Purpose**: Ensure code meets quality standards before code review, merge, and deployment.

---

## Gate 1: Test Coverage Thresholds

### Line Coverage

```bash
$ pytest --cov=app --cov-report=term-missing tests/

Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py            0      0   100%
app/[module].py          [X]    [X]   [X]%   [lines]
-----------------------------------------------------
TOTAL                    [X]    [X]   [X]%
```

**Thresholds**:
- [ ] **Minimum**: ≥80% line coverage (REQUIRED)
- [ ] **Target**: ≥85% line coverage (RECOMMENDED)
- [ ] **Critical Path**: 100% coverage (REQUIRED)

**Current Coverage**: [X]%

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

### Branch Coverage

```bash
$ pytest --cov=app --cov-branch --cov-report=term-missing tests/
```

**Thresholds**:
- [ ] **Minimum**: ≥75% branch coverage (REQUIRED)
- [ ] **Target**: ≥80% branch coverage (RECOMMENDED)
- [ ] **Critical Path**: 100% coverage (REQUIRED)

**Current Coverage**: [X]%

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

### Function Coverage

**Thresholds**:
- [ ] **Minimum**: ≥85% function coverage (REQUIRED)
- [ ] **Target**: ≥90% function coverage (RECOMMENDED)
- [ ] **Critical Path**: 100% coverage (REQUIRED)

**Current Coverage**: [X]%

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

### Differential Coverage (New Code Only)

```bash
$ pytest --cov=app --cov-report=xml tests/
$ diff-cover coverage.xml --compare-branch=main --fail-under=100
```

**Thresholds**:
- [ ] **New Code**: 100% coverage (REQUIRED)
- [ ] **Changed Code**: 100% coverage (REQUIRED)

**Current Differential Coverage**: [X]%

**Status**: [✅ Pass | ❌ Fail - Add Tests]

---

### Coverage Exemptions

**Exempted Code**:
- [ ] Platform-specific code (with approval)
- [ ] Generated code (with approval)
- [ ] Defensive error handling (with approval)

**Exemption Justification**:
[Explain why code is exempted]

**Approver**: [Name]

---

### Coverage Gate Summary

**Overall Status**: [✅ Pass All Gates | ⚠️ Some Below Target | ❌ Below Minimum]

**Action Required**: [None | Add tests for [X]% gap]

---

## Gate 2: Mutation Testing

### Mutation Score

```bash
$ mutmut run --paths-to-mutate app/
$ mutmut results

Killed: [X]
Survived: [X]
Timeout: [X]
Total: [X]

Mutation Score: [X]%
```

**Thresholds**:
- [ ] **Minimum**: ≥85% mutation score (REQUIRED)
- [ ] **Target**: ≥90% mutation score (RECOMMENDED)
- [ ] **Critical Path**: ≥95% mutation score (REQUIRED)

**Current Mutation Score**: [X]%

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

### Survived Mutants Analysis

**Mutant #1**:
- **Location**: [file:line]
- **Mutation**: [original → mutant]
- **Why Survived**: [Reason]
- **Action**: [ ] [Fix test | Accept as equivalent]

**Mutant #2**:
- **Location**: [file:line]
- **Mutation**: [original → mutant]
- **Why Survived**: [Reason]
- **Action**: [ ] [Fix test | Accept as equivalent]

**Total Survived**: [X]
**Equivalent Mutants**: [X]
**Must Fix**: [X]

---

### Mutation Testing Gate Summary

**Overall Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

**Action Required**: [None | Fix [X] weak tests]

---

## Gate 3: Test Quality

### Test Execution Performance

```bash
$ pytest tests/ --durations=10

============================= slowest 10 durations =============================
[X.XX]s call     tests/test_[module].py::test_[name]
[X.XX]s call     tests/test_[module].py::test_[name]
```

**Thresholds**:
- [ ] **Total Suite**: <60s for full suite (REQUIRED)
- [ ] **Average Test**: <100ms per test (RECOMMENDED)
- [ ] **Slowest Test**: <1s (RECOMMENDED)

**Current Metrics**:
- Total Suite Time: [X]s
- Average Test Time: [X]ms
- Slowest Test: [X]s

**Status**: [✅ Pass | ⚠️ Some Slow | ❌ Too Slow]

---

### Test Reliability

**Flaky Tests**:
```bash
$ pytest tests/ --count=10
```

- [ ] **No flaky tests**: All tests pass consistently (REQUIRED)
- [ ] **Deterministic**: Same result every run (REQUIRED)
- [ ] **No random failures**: No intermittent issues (REQUIRED)

**Flaky Tests Found**: [X]

**Status**: [✅ No Flaky Tests | ❌ Flaky Tests - Fix Immediately]

---

### Test Independence

- [ ] **Order independent**: Tests pass in any order (REQUIRED)
- [ ] **Isolation**: Each test sets up own state (REQUIRED)
- [ ] **No shared state**: Tests don't affect each other (REQUIRED)

```bash
$ pytest tests/ --random-order
```

**Status**: [✅ Independent | ❌ Dependency - Fix]

---

### Test Quality Score

**Calculation**:
- Fast execution: [X]/10 points
- No flaky tests: [X]/10 points
- Independent tests: [X]/10 points

**Total Score**: [X]/30

**Status**: [✅ High Quality | ⚠️ Acceptable | ❌ Poor Quality]

---

## Gate 4: Code Quality Metrics

### Cyclomatic Complexity

```bash
$ radon cc app/ -a -s

app/[module].py
    M [X] - [function] ([line])
    M [X] - [function] ([line])

Average complexity: M ([X.X])
```

**Thresholds**:
- [ ] **Per Function**: <10 (REQUIRED)
- [ ] **Per Module**: <15 average (RECOMMENDED)

**Current Metrics**:
- Max Complexity: [X]
- Average Complexity: [X.X]

**Status**: [✅ Pass | ⚠️ High Complexity | ❌ Too Complex]

---

### Maintainability Index

```bash
$ radon mi app/

app/[module].py - A ([X.X])
```

**Thresholds**:
- [ ] **Minimum**: B (≥20) (REQUIRED)
- [ ] **Target**: A (≥80) (RECOMMENDED)

**Current Index**: [Grade] ([Score])

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

### Code Duplication

```bash
$ pylint --disable=all --enable=duplicate-code app/
```

- [ ] **No duplication**: <5% duplicated code (REQUIRED)
- [ ] **DRY principle**: Reusable functions extracted (RECOMMENDED)

**Duplication Found**: [X]%

**Status**: [✅ Pass | ⚠️ Some Duplication | ❌ High Duplication]

---

### Linting

```bash
$ pylint app/ --fail-under=9.0

Your code has been rated at [X.X]/10
```

**Thresholds**:
- [ ] **Minimum**: ≥8.0/10 (REQUIRED)
- [ ] **Target**: ≥9.0/10 (RECOMMENDED)

**Current Score**: [X.X]/10

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

### Type Coverage (TypeScript/Python)

```bash
# TypeScript
$ npx type-coverage --at-least 95

# Python
$ mypy app/ --strict
```

- [ ] **Type coverage**: ≥95% (REQUIRED for typed languages)
- [ ] **Strict mode**: No `any` types (RECOMMENDED)

**Current Type Coverage**: [X]%

**Status**: [✅ Pass | ⚠️ Below Target | ❌ Below Minimum]

---

## Gate 5: Security Requirements

### Dependency Vulnerabilities

```bash
# Python
$ pip-audit

# JavaScript
$ npm audit

# All
$ snyk test
```

- [ ] **No critical vulnerabilities**: 0 critical (REQUIRED)
- [ ] **No high vulnerabilities**: 0 high (REQUIRED)
- [ ] **Low/medium reviewed**: All acknowledged or fixed (RECOMMENDED)

**Vulnerabilities Found**:
- Critical: [X]
- High: [X]
- Medium: [X]
- Low: [X]

**Status**: [✅ Pass | ⚠️ Low/Medium Only | ❌ Critical/High Found]

---

### Static Security Analysis

```bash
$ bandit -r app/
$ semgrep --config=auto app/
```

- [ ] **No security issues**: All findings resolved (REQUIRED)
- [ ] **Input validation**: All inputs validated (REQUIRED)
- [ ] **Output sanitization**: All outputs sanitized (REQUIRED)

**Security Issues**: [X]

**Status**: [✅ Pass | ⚠️ Minor Issues | ❌ Security Issues]

---

### Secrets Detection

```bash
$ trufflehog filesystem app/
$ gitleaks detect --source=.
```

- [ ] **No hardcoded secrets**: 0 secrets found (REQUIRED)
- [ ] **No API keys**: All externalized (REQUIRED)
- [ ] **Environment variables**: Proper configuration (REQUIRED)

**Secrets Found**: [X]

**Status**: [✅ Pass | ❌ Secrets Found - Remove Immediately]

---

## Gate 6: Performance Requirements

### Response Time

```bash
$ pytest tests/performance/
```

**Thresholds**:
- [ ] **API endpoints**: <200ms p95 (REQUIRED)
- [ ] **Database queries**: <100ms p95 (REQUIRED)
- [ ] **Background jobs**: <5s p95 (REQUIRED)

**Current Performance**:
- API: [X]ms p95
- Database: [X]ms p95
- Jobs: [X]s p95

**Status**: [✅ Pass | ⚠️ Some Slow | ❌ Performance Regression]

---

### Resource Usage

```bash
$ pytest tests/performance/ --profile
```

**Thresholds**:
- [ ] **Memory usage**: <500MB per process (REQUIRED)
- [ ] **CPU usage**: <70% average (REQUIRED)
- [ ] **No memory leaks**: Stable over time (REQUIRED)

**Current Usage**:
- Memory: [X]MB
- CPU: [X]%
- Leaks: [None | Detected]

**Status**: [✅ Pass | ⚠️ High Usage | ❌ Leaks/Excessive]

---

### Database Performance

```bash
$ EXPLAIN ANALYZE [query]
```

- [ ] **No N+1 queries**: All optimized (REQUIRED)
- [ ] **Proper indexes**: All queries indexed (REQUIRED)
- [ ] **Query time**: <100ms per query (REQUIRED)

**N+1 Queries**: [X]
**Missing Indexes**: [X]
**Slow Queries**: [X]

**Status**: [✅ Pass | ⚠️ Some Issues | ❌ Major Issues]

---

## Gate 7: Documentation Requirements

### Code Documentation

- [ ] **Public API documented**: All public functions (REQUIRED)
- [ ] **Complex logic explained**: Comments for complex code (RECOMMENDED)
- [ ] **Type hints**: All functions typed (REQUIRED for typed languages)

**Documentation Coverage**: [X]%

**Status**: [✅ Pass | ⚠️ Partial | ❌ Missing]

---

### Test Documentation

- [ ] **Test names descriptive**: Clear what's tested (REQUIRED)
- [ ] **Complex tests explained**: Comments for complex assertions (RECOMMENDED)
- [ ] **Test data documented**: Sample data explained (RECOMMENDED)

**Status**: [✅ Pass | ⚠️ Some Unclear | ❌ Poor Documentation]

---

### README Updated

- [ ] **Feature documented**: New features in README (REQUIRED)
- [ ] **API changes**: Breaking changes documented (REQUIRED)
- [ ] **Migration guide**: If needed (REQUIRED for breaking changes)

**Status**: [✅ Updated | ⏳ Needs Update | ❌ Not Updated]

---

## Gate 8: CI/CD Integration

### Build Status

```bash
$ ./build.sh
```

- [ ] **Build succeeds**: Clean build (REQUIRED)
- [ ] **No warnings**: All warnings resolved (RECOMMENDED)
- [ ] **Linting passes**: All linters pass (REQUIRED)

**Status**: [✅ Pass | ⚠️ Warnings | ❌ Build Fails]

---

### Automated Tests in CI

```bash
$ .github/workflows/test.yml
```

- [ ] **All tests run**: Full suite in CI (REQUIRED)
- [ ] **Coverage enforced**: Minimum coverage in CI (REQUIRED)
- [ ] **Mutation testing**: In CI or pre-merge (RECOMMENDED)

**CI Status**: [✅ Pass | ❌ Fail]

---

### Deployment Readiness

- [ ] **Staging tested**: Deployed to staging (REQUIRED)
- [ ] **Smoke tests pass**: Basic functionality verified (REQUIRED)
- [ ] **Rollback tested**: Rollback procedure verified (REQUIRED)

**Status**: [✅ Ready | ⏳ Testing | ❌ Not Ready]

---

## Final Gate Summary

### Critical Gates (Must Pass)

| Gate | Status | Action Required |
|------|--------|-----------------|
| Line Coverage ≥80% | [✅/❌] | [Action if needed] |
| Branch Coverage ≥75% | [✅/❌] | [Action if needed] |
| Differential Coverage 100% | [✅/❌] | [Action if needed] |
| Mutation Score ≥85% | [✅/❌] | [Action if needed] |
| No Critical/High Vulnerabilities | [✅/❌] | [Action if needed] |
| No Secrets | [✅/❌] | [Action if needed] |
| No Flaky Tests | [✅/❌] | [Action if needed] |
| Build Passes | [✅/❌] | [Action if needed] |

---

### Recommended Gates (Should Pass)

| Gate | Status | Action Recommended |
|------|--------|--------------------|
| Line Coverage ≥85% | [✅/⚠️/❌] | [Action if needed] |
| Mutation Score ≥90% | [✅/⚠️/❌] | [Action if needed] |
| Performance <200ms | [✅/⚠️/❌] | [Action if needed] |
| Complexity <10 | [✅/⚠️/❌] | [Action if needed] |
| Type Coverage ≥95% | [✅/⚠️/❌] | [Action if needed] |

---

## Overall Quality Status

**Critical Gates**: [X]/8 passed
**Recommended Gates**: [X]/5 passed

**Overall Status**:
- [✅] **Pass**: All critical gates passed, ready for review/merge
- [⚠️] **Warning**: Critical gates passed, but recommended gates need attention
- [❌] **Fail**: Critical gates failed, cannot proceed

---

## Action Items

### Must Fix (Blocking)
- [ ] [Action 1] - Blocker for: [Gate Name]
- [ ] [Action 2] - Blocker for: [Gate Name]

### Should Fix (Recommended)
- [ ] [Action 1] - Improves: [Gate Name]
- [ ] [Action 2] - Improves: [Gate Name]

### Nice to Have (Optional)
- [ ] [Action 1] - Enhancement: [Description]
- [ ] [Action 2] - Enhancement: [Description]

---

## Approval

### Developer Sign-off

- [ ] **All critical gates passed**: Confirmed
- [ ] **Known issues documented**: Listed above
- [ ] **Action items created**: All tracked

**Developer**: [Name]
**Date**: [YYYY-MM-DD]

---

### Reviewer Sign-off

- [ ] **Quality gates verified**: Independently checked
- [ ] **Code reviewed**: Approved
- [ ] **Tests reviewed**: Approved

**Reviewer**: [Name]
**Date**: [YYYY-MM-DD]

---

### Deployment Approval

- [ ] **All gates passed**: Verified
- [ ] **Staging tested**: Successful
- [ ] **Rollback ready**: Procedure tested

**Approver**: [Name]
**Date**: [YYYY-MM-DD]

---

**Checklist Completed**: [Date and Time]
**Checklist Version**: 1.0
**Next Review**: [Date]
