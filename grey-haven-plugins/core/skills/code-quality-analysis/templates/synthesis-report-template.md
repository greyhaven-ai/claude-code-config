# Synthesis Analysis Report

**Project**: [Project Name]
**Scope**: [Number of modules/files analyzed]
**Review Date**: [Date]
**Analyst**: [Analyst Name]
**Review Type**: Cross-File Architectural Analysis
**Status**: [Draft | In Review | Final]

---

## Executive Summary

**Overall Consistency Score**: [X]/100

**Architectural Compliance**: [X]% (Target: >90%)

**Cross-File Issues Found**: [X] issues
- 🔴 Critical (P0): [X] - Architectural violations
- 🟠 High (P1): [X] - Pattern inconsistencies
- 🟡 Medium (P2): [X] - Minor inconsistencies
- 🟢 Low (P3): [X] - Style variations

**Recommendation**: [Major refactoring needed | Improvements required | Architecture sound]

**Key Findings**:
1. [Most critical architectural issue]
2. [Most widespread inconsistency]
3. [Most impactful pattern violation]

---

## Scope

**Codebase Size**: [X] files, [Y] lines of code

**Modules Analyzed**:
- [ ] API Layer ([X] files)
- [ ] Service Layer ([X] files)
- [ ] Data Access Layer ([X] files)
- [ ] Models/Schemas ([X] files)
- [ ] Utilities ([X] files)

**Analysis Depth**:
- [X] Dependency analysis
- [X] Pattern consistency checks
- [X] Naming convention analysis
- [X] Error handling patterns
- [X] Architectural layer violations
- [X] Circular dependency detection
- [X] Response format consistency

---

## Architecture Overview

### Expected Architecture

```
┌─────────────────────────────────────┐
│      Presentation Layer (API)      │  ← HTTP handlers, routing
├─────────────────────────────────────┤
│      Business Logic (Services)     │  ← Core logic, orchestration
├─────────────────────────────────────┤
│    Data Access (Repositories)      │  ← Database queries, ORM
├─────────────────────────────────────┤
│         Database / Storage          │  ← PostgreSQL, Redis, etc.
└─────────────────────────────────────┘
```

### Actual Implementation

```
┌─────────────────────────────────────┐
│      Presentation Layer (API)      │
├─────────────────────────────────────┤  [X]% of endpoints
│      Business Logic (Services)     │   bypass this layer ⚠️
├─────────────────────────────────────┤
│    Data Access (Repositories)      │
├─────────────────────────────────────┤
│         Database / Storage          │
└─────────────────────────────────────┘
```

**Violations Detected**: [X] layer bypasses, [X] direct database access

---

## Consistency Scorecard

```
Category                        Score    Target   Status
---------------------------------------------------------------
Error Handling Consistency      [X]/100  90/100   [✅/⚠️/🔴]
Validation Pattern Consistency  [X]/100  95/100   [✅/⚠️/🔴]
Naming Convention Consistency   [X]/100  85/100   [✅/⚠️/🔴]
Response Format Consistency     [X]/100  90/100   [✅/⚠️/🔴]
Architectural Layer Compliance  [X]/100  95/100   [✅/⚠️/🔴]
Dependency Pattern Consistency  [X]/100  85/100   [✅/⚠️/🔴]
Code Style Consistency          [X]/100  80/100   [✅/⚠️/🔴]
---------------------------------------------------------------
OVERALL CONSISTENCY SCORE:      [X]/100  90/100   [Status]
```

**Scoring Guide**:
- 90-100: Excellent consistency
- 75-89: Good, minor variations
- 60-74: Fair, needs standardization
- 40-59: Poor, significant inconsistencies
- <40: Critical, major architectural issues

---

## Cross-File Issues

### Issue #1: [Issue Category] - [Brief Description]

**Severity**: [🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low]

**Affected Files**: [X] files
- `[file path 1]`
- `[file path 2]`
- `[file path 3]`

**Description**:
[Detailed description of the cross-file inconsistency or architectural issue]

**Pattern Inconsistency**:

**File 1**: `[file path 1]`
```python
# Pattern A
def handle_error():
    raise HTTPException(status_code=404, detail="Not found")
```

**File 2**: `[file path 2]`
```python
# Pattern B (different!)
def handle_error():
    return {"error": "Not found"}  # Inconsistent!
```

**File 3**: `[file path 3]`
```python
# Pattern C (yet another variation!)
def handle_error():
    raise CustomError("Not found")  # Third pattern!
```

**Impact**:
- [X] different patterns across codebase
- [X]% of files use Pattern A
- [X]% of files use Pattern B
- [X]% of files use Pattern C
- Makes codebase harder to understand and maintain

**Recommended Solution**:

```python
# utils/errors.py - Single source of truth
class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

# Apply consistently across all files
@app.exception_handler(AppError)
def handle_app_error(request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
```

**Estimated Fix Time**: [X] hours
**Priority**: [P0 | P1 | P2 | P3]
**Status**: [⏳ To Do | 🔄 In Progress | ✅ Fixed]

---

### Issue #2: Architectural Layer Violation

**Severity**: 🔴 Critical

**Affected Files**: [X] files

**Description**:
API layer directly accessing database, bypassing service and repository layers.

**Violation Pattern**:

```python
# api/users.py - ❌ WRONG: API directly accessing database
from database.connection import get_db

@app.get("/users/{user_id}")
def get_user(user_id: str):
    db = get_db()
    user = db.execute(f"SELECT * FROM users WHERE id = '{user_id}'").fetchone()
    return user
```

**Expected Pattern**:

```python
# ✅ CORRECT: Proper layering
# api/users.py
@app.get("/users/{user_id}")
def get_user(user_id: str, service: UserService = Depends()):
    return service.get_user(user_id)

# services/user_service.py
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: str) -> User:
        return self.repository.find_by_id(user_id)

# repositories/user_repository.py
class UserRepository:
    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
```

**Impact**: [X] endpoints bypass proper architecture

**Estimated Fix Time**: [X] hours
**Priority**: P0
**Status**: [⏳ To Do]

---

### Issue #3: [Issue Title]

[Repeat structure for each cross-file issue]

---

## Dependency Analysis

### Module Dependency Graph

```
api/
  ├─> services/           ✅ Correct
  ├─> database/           ❌ Violation (should go through services)
  └─> models/             ✅ Correct

services/
  ├─> repositories/       ✅ Correct
  ├─> models/             ✅ Correct
  └─> other services/     ⚠️  Check for circular dependencies

repositories/
  ├─> database/           ✅ Correct
  ├─> models/             ✅ Correct
  └─> services/           ❌ Violation (reverse dependency)
```

### Circular Dependencies Detected

**Circular Dependency #1**: `[module A]` ↔ `[module B]`

```python
# services/user_service.py
from services.team_service import get_user_teams  # ❌ Imports team service

def get_user_with_teams(user_id):
    teams = get_user_teams(user_id)  # Calls team service
    # ...

# services/team_service.py
from services.user_service import get_team_members  # ❌ Imports user service

def get_team_with_members(team_id):
    members = get_team_members(team_id)  # Calls user service
    # CIRCULAR DEPENDENCY!
```

**Solution**:

```python
# models/aggregates.py - Shared aggregation logic
def get_user_with_teams(user_id, user_repo, team_repo):
    """No service dependencies, uses repositories directly."""
    user = user_repo.find_by_id(user_id)
    teams = team_repo.find_by_user_id(user_id)
    return {**user.dict(), "teams": teams}
```

**Total Circular Dependencies**: [X]

---

## Pattern Consistency Analysis

### Error Handling Patterns

**Patterns Found**: [X] different patterns

| Pattern | Files Using | Percentage | Recommended |
|---------|-------------|------------|-------------|
| HTTPException | [X] | [X]% | ✅ |
| Custom exceptions | [X] | [X]% | |
| Dict with error key | [X] | [X]% | |
| Return None | [X] | [X]% | |

**Recommendation**: Standardize on [recommended pattern]

---

### Validation Patterns

**Patterns Found**: [X] different patterns

| Pattern | Files Using | Duplication |
|---------|-------------|-------------|
| Inline validation | [X] | [X] lines |
| Pydantic models | [X] | [X] lines |
| Custom validators | [X] | [X] lines |
| No validation | [X] | N/A |

**Code Duplication**: [X] lines of duplicated validation logic

**Recommendation**: Centralize validation with Pydantic schemas

---

### Naming Conventions

**Conventions Found**: [X] different styles

| Convention | Files Using | Percentage |
|------------|-------------|------------|
| snake_case | [X] | [X]% |
| camelCase | [X] | [X]% |
| PascalCase | [X] | [X]% |
| Abbreviated | [X] | [X]% |

**Inconsistency Score**: [X]/100 (lower is better)

**Recommendation**: Enforce [snake_case for Python | camelCase for JavaScript]

---

### Response Format Patterns

**Patterns Found**: [X] different formats

| Format | Endpoints Using | Percentage |
|--------|----------------|------------|
| Pydantic models | [X] | [X]% |
| Dict (snake_case) | [X] | [X]% |
| Dict (camelCase) | [X] | [X]% |
| Raw models | [X] | [X]% |

**Recommendation**: Enforce consistent response models

---

## Code Duplication Analysis

**Total Duplicated Code**: [X] lines ([X]% of codebase)

### Duplication Hotspot #1

**Pattern**: [Description of duplicated logic]

**Found in**: [X] files
- `[file path 1]:[line range]`
- `[file path 2]:[line range]`
- `[file path 3]:[line range]`

**Example**:

```python
# Duplicated in 6 files
def validate_email(email):
    if not email or "@" not in email:
        raise ValueError("Invalid email")
    # ... more validation
```

**Recommendation**: Extract to shared utility module

```python
# utils/validators.py
def validate_email(email: str) -> None:
    """Centralized email validation."""
    if not email or "@" not in email:
        raise ValueError("Invalid email")
```

**Potential Savings**: [X] lines removed

---

### Duplication Hotspot #2

[Repeat structure]

---

## Architectural Recommendations

### Immediate Actions (P0)

1. **Fix Layer Violations**: [X] endpoints directly accessing database
   - Estimated time: [X] hours
   - Impact: High - Prevents proper testing and maintenance

2. **Resolve Circular Dependencies**: [X] circular imports detected
   - Estimated time: [X] hours
   - Impact: High - Causes import errors and tight coupling

3. **Standardize Error Handling**: [X] different patterns
   - Estimated time: [X] hours
   - Impact: High - Improves error consistency

### Short-term Improvements (P1)

1. **Centralize Validation**: Remove [X] lines of duplicated validation
2. **Enforce Naming Conventions**: Update [X] files
3. **Standardize Response Formats**: Update [X] endpoints

### Long-term Improvements (P2-P3)

1. **Architectural Testing**: Add tests to enforce layer boundaries
2. **Dependency Rules**: Implement import linting rules
3. **Code Review Checklist**: Include consistency checks

---

## Consistency Enforcement

### Pre-commit Hooks

```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-architecture
        name: Check architectural boundaries
        entry: python scripts/check_architecture.py
        language: system
        pass_filenames: false
```

### Architecture Testing

```python
# tests/test_architecture.py
import pytest
from architecture_checker import check_dependencies

def test_api_should_not_import_database():
    """API layer should only import services, not database."""
    violations = check_dependencies("api/", forbidden=["database"])
    assert len(violations) == 0, f"Found violations: {violations}"

def test_no_circular_dependencies():
    """Check for circular dependencies."""
    cycles = detect_circular_dependencies()
    assert len(cycles) == 0, f"Found cycles: {cycles}"
```

### CI/CD Quality Gates

```yaml
# .github/workflows/architecture.yml
- name: Check Architecture
  run: |
    python scripts/check_architecture.py
    python scripts/check_circular_deps.py
    python scripts/check_consistency.py
```

---

## Refactoring Plan

### Week 1: Critical Issues (P0)

**Day 1-2**: Fix layer violations
- [ ] Move database access to repositories
- [ ] Update [X] endpoints
- [ ] Add integration tests

**Day 3-4**: Resolve circular dependencies
- [ ] Create shared aggregation modules
- [ ] Refactor [X] service dependencies
- [ ] Verify no import cycles

**Day 5**: Standardize error handling
- [ ] Create unified error classes
- [ ] Update [X] files
- [ ] Add global error handlers

**Estimated Time**: [X] hours

---

### Week 2: High Priority (P1)

**Day 1-2**: Centralize validation
- [ ] Create Pydantic schemas
- [ ] Remove duplicated validation
- [ ] Update [X] endpoints

**Day 3-4**: Enforce naming conventions
- [ ] Rename inconsistent functions
- [ ] Update [X] files
- [ ] Run automated formatters

**Day 5**: Standardize responses
- [ ] Create response models
- [ ] Update [X] endpoints
- [ ] Add response validation

**Estimated Time**: [X] hours

---

### Weeks 3-4: Medium Priority (P2)

- [ ] Add architectural tests
- [ ] Implement dependency rules
- [ ] Update documentation
- [ ] Code review checklist

**Estimated Time**: [X] hours

---

## Monitoring and Prevention

### Consistency Metrics Dashboard

```python
# Track consistency over time
metrics = {
    "error_handling_consistency": track_error_patterns(),
    "naming_consistency": track_naming_patterns(),
    "architecture_compliance": track_layer_violations(),
    "circular_dependencies": detect_cycles(),
}
```

### Regular Reviews

- **Weekly**: Automated consistency checks in CI/CD
- **Monthly**: Manual architectural review
- **Quarterly**: Comprehensive synthesis analysis

---

## Benefits

### Before Synthesis Analysis

- Architectural compliance: [X]%
- Pattern consistency: [X]%
- Code duplication: [X]%
- Circular dependencies: [X]
- Developer onboarding: [X] days

### After Fixes

- Architectural compliance: [X]%
- Pattern consistency: [X]%
- Code duplication: [X]%
- Circular dependencies: 0
- Developer onboarding: [X] days

### ROI Calculation

```
Time Investment: [X] hours refactoring
Time Savings:
  - Faster debugging: [X] hours/month
  - Easier onboarding: [X] hours/new developer
  - Fewer bugs: [X] hours/month

Payback Period: [X] weeks
Annual ROI: [X]%
```

---

## Appendix

### Analysis Methodology

1. **Dependency Extraction**: Parse import statements across all files
2. **Pattern Detection**: Identify common code patterns and variations
3. **Naming Analysis**: Extract all function/class names and detect styles
4. **Duplication Detection**: Use AST comparison for semantic duplication
5. **Architecture Mapping**: Map actual vs. expected layer interactions

### Tools Used

- **Radon v[X.X.X]** - Complexity and maintainability
- **Bandit v[X.X.X]** - Security analysis
- **jscpd v[X.X.X]** - Duplication detection
- **pylint v[X.X.X]** - Code quality
- **import-linter v[X.X.X]** - Dependency rules

### Consistency Formulas

```python
# Pattern Consistency Score
consistency = (most_common_pattern_count / total_occurrences) * 100

# Architectural Compliance Score
compliance = ((total_interactions - violations) / total_interactions) * 100

# Overall Consistency Score
overall = (
    error_consistency * 0.20 +
    validation_consistency * 0.15 +
    naming_consistency * 0.15 +
    response_consistency * 0.15 +
    architecture_compliance * 0.25 +
    dependency_consistency * 0.10
)
```

### References

- Clean Architecture by Robert C. Martin
- Dependency Inversion Principle (SOLID)
- Domain-Driven Design by Eric Evans

### Reviewer Information

**Name**: [Analyst Name]
**Role**: [Software Architect/Senior Engineer]
**Contact**: [Email]
**Date**: [Date]

---

**Approval**:
- [ ] Architecture Team: ________________ Date: ________
- [ ] Engineering Lead: ________________ Date: ________
- [ ] Product Owner: ________________ Date: ________

---

Related: [Security Report Template](security-report-template.md) | [Clarity Report Template](clarity-report-template.md) | [Complete Audit Template](complete-audit-report-template.md)
