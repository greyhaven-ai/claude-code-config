# Coverage Guide

Complete guide to code coverage in Python - coverage.py, pytest-cov, coverage types, interpreting reports, and CI integration.

**Tools**: coverage.py 7.0+, pytest-cov 4.0+
**Coverage Types**: Line, branch, function coverage
**Goal**: 80% minimum, 90%+ production-ready

---

## Installation

```bash
# Install coverage.py
pip install coverage

# Install pytest-cov (includes coverage.py)
pip install pytest-cov

# Install in project
pip install -e ".[test]"  # If defined in setup.py/pyproject.toml
```

---

## Coverage Types

### Line Coverage

**What it measures**: Percentage of lines executed during tests.

```python
def calculate_discount(price, is_member):
    if is_member:           # Line 1
        return price * 0.9  # Line 2 (covered if is_member=True)
    else:                   # Line 3
        return price        # Line 4 (covered if is_member=False)

# Test 1: is_member=True → Lines 1,2 covered
# Test 2: is_member=False → Lines 1,3,4 covered
# Line coverage: 100% (all lines covered)
```

### Branch Coverage

**What it measures**: Percentage of decision branches taken.

```python
def calculate_discount(price, is_member):
    if is_member:           # Branch point
        return price * 0.9  # True branch
    else:
        return price        # False branch

# Test 1: is_member=True → True branch covered
# Test 2: is_member=False → False branch covered
# Branch coverage: 100% (both branches covered)
```

**Missing branch example**:

```python
def process(value):
    if value > 0:       # Branch point
        return value

# Test: process(5) → True branch covered
# Branch coverage: 50% (False branch NOT covered)
```

### Function Coverage

**What it measures**: Percentage of functions called.

```python
def function_a():
    return "a"

def function_b():
    return "b"

# Test calls function_a() only
# Function coverage: 50% (1 of 2 functions)
```

---

## Running Coverage

### With pytest-cov

```bash
# Basic coverage report
pytest --cov=app tests/

# Show missing lines
pytest --cov=app --cov-report=term-missing tests/

# Branch coverage
pytest --cov=app --cov-branch tests/

# HTML report
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html

# XML report (for CI)
pytest --cov=app --cov-report=xml tests/

# Multiple formats
pytest --cov=app \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-report=xml \
  tests/
```

### With coverage.py

```bash
# Run tests with coverage
coverage run -m pytest tests/

# Generate report
coverage report

# Show missing lines
coverage report -m

# HTML report
coverage html
open htmlcov/index.html

# XML report
coverage xml

# Erase previous data
coverage erase
```

---

## Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
addopts =
    --cov=app
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-branch
    --cov-fail-under=80
```

### .coveragerc

```ini
[run]
source = app, src
omit =
    */tests/*
    */migrations/*
    */venv/*
    */virtualenv/*
    */__pycache__/*
    */site-packages/*

[report]
precision = 2
show_missing = True
skip_covered = False
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

[html]
directory = htmlcov

[xml]
output = coverage.xml
```

### pyproject.toml

```toml
[tool.coverage.run]
source = ["app", "src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*"
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod"
]
fail_under = 80

[tool.coverage.html]
directory = "htmlcov"
```

---

## Interpreting Reports

### Terminal Report

```bash
$ pytest --cov=app --cov-report=term-missing tests/

---------- coverage: platform darwin, python 3.11.5 -----------
Name                      Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------
app/__init__.py               2      0      0      0   100%
app/calculator.py            15      2      8      1    85%   23, 45
app/service.py               42      5     12      2    88%   67-71, 89
---------------------------------------------------------------------
TOTAL                        59      7     20      3    88%
```

**Key Metrics**:
- **Stmts**: Total statements (lines of code)
- **Miss**: Missed statements (not executed)
- **Branch**: Total branches (if/else, loops)
- **BrPart**: Partial branches (one side not covered)
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

### HTML Report

```bash
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html
```

**Features**:
- Color-coded coverage (green=covered, red=missed)
- Click on files to see line-by-line coverage
- Branch visualization
- Sortable columns
- Search functionality

### Coverage Badge

```markdown
<!-- README.md -->
![Coverage](https://img.shields.io/badge/coverage-88%25-green)
```

---

## Coverage Goals

### Recommended Thresholds

| Coverage Type | Minimum | Good | Excellent |
|---------------|---------|------|-----------|
| **Line** | 80% | 90% | 95%+ |
| **Branch** | 75% | 85% | 90%+ |
| **Function** | 85% | 90% | 95%+ |

### By Code Type

| Code Type | Target | Reason |
|-----------|--------|--------|
| **Business logic** | 95%+ | Critical functionality |
| **Controllers/Views** | 85%+ | Integration points |
| **Utilities** | 90%+ | Reused across codebase |
| **Config/Settings** | 60%+ | Mostly static |
| **Tests** | N/A | Don't test tests |

---

## Improving Coverage

### Find Uncovered Code

```bash
# Show only uncovered lines
pytest --cov=app --cov-report=term-missing tests/ | grep -v "100%"

# Generate report focusing on gaps
coverage report --skip-covered
```

### Prioritize Coverage

```python
# 1. Critical paths first
def process_payment(amount, card):
    # Must be tested!
    if amount > 10000:
        require_manual_approval()

# 2. Error handling
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # Test error path!
        logger.error(f"Failed to fetch: {e}")
        return None

# 3. Edge cases
def calculate_discount(price, quantity):
    if quantity >= 100:    # Test boundary
        return price * 0.2
    elif quantity >= 10:   # Test boundary
        return price * 0.1
    return 0
```

### Exclude Unreachable Code

```python
# Exclude from coverage
def debug_info():  # pragma: no cover
    """Development only - not tested."""
    import pdb; pdb.set_trace()

# Exclude conditional imports
try:
    import optional_library
except ImportError:  # pragma: no cover
    optional_library = None

# Exclude type checking
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from module import TypeHint
```

---

## Differential Coverage

**What it measures**: Coverage of new/changed code only.

### With pytest-cov

```bash
# Generate baseline
pytest --cov=app --cov-report=xml tests/
mv coverage.xml baseline-coverage.xml

# After changes, compare
pytest --cov=app --cov-report=xml tests/
coverage-diff baseline-coverage.xml coverage.xml
```

### With diff-cover

```bash
# Install
pip install diff-cover

# Generate coverage for current branch
pytest --cov=app --cov-report=xml tests/

# Compare against main branch
diff-cover coverage.xml --compare-branch=main

# Fail if new code coverage < 100%
diff-cover coverage.xml --compare-branch=main --fail-under=100
```

**Output**:
```
Diff Coverage: 95.5%
main...feature-branch, staged and unstaged changes

app/new_feature.py (95.5%): Missing lines 23, 45
```

---

## Coverage in CI/CD

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: pytest --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Check coverage threshold
        run: |
          COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi
```

### Codecov

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 100%
        threshold: 0%

comment:
  layout: "reach, diff, flags, files"
  behavior: default
```

---

## Advanced Patterns

### Parallel Coverage

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest --cov=app -n auto tests/

# Combine coverage from parallel runs
coverage combine
coverage report
```

### Subprocess Coverage

```python
# .coveragerc
[run]
concurrency = multiprocessing
parallel = True

# In code
import coverage
coverage.process_startup()
```

```bash
# Run and combine
coverage run -m pytest tests/
coverage combine
coverage report
```

### Coverage for Scripts

```bash
# Direct script execution
coverage run script.py arg1 arg2
coverage report

# Module execution
coverage run -m module_name
coverage report
```

---

## Coverage Pitfalls

### ❌ False Positives

```python
# Lines executed but not properly tested
def divide(a, b):
    return a / b  # Covered, but ZeroDivisionError not tested!

# Test
def test_divide():
    assert divide(10, 2) == 5  # ✅ Line covered, ❌ Exception not tested
```

**Fix**: Test error cases explicitly.

### ❌ Gaming Coverage

```python
# BAD: Empty test for coverage
def test_function():
    function()  # Just calls it, doesn't verify behavior!
```

**Fix**: Meaningful assertions required.

### ❌ 100% Obsession

```python
# Don't sacrifice quality for 100% coverage
def error_handler():
    # This is hard to test and rarely executed
    system.critical_shutdown()  # Skip this line
```

**Fix**: Use `pragma: no cover` for acceptable gaps.

---

## Coverage Reports

### Terminal (term)

```bash
pytest --cov=app --cov-report=term tests/
```

**Best for**: Quick feedback during development.

### Terminal with Missing Lines (term-missing)

```bash
pytest --cov=app --cov-report=term-missing tests/
```

**Best for**: Identifying what to test next.

### HTML

```bash
pytest --cov=app --cov-report=html tests/
```

**Best for**: Visual analysis, code review.

### XML (Cobertura)

```bash
pytest --cov=app --cov-report=xml tests/
```

**Best for**: CI/CD integration (Codecov, Coveralls).

### JSON

```bash
pytest --cov=app --cov-report=json tests/
```

**Best for**: Custom tooling, programmatic access.

### Annotate

```bash
coverage annotate
cat app/module.py,cover
```

**Best for**: Line-by-line text annotation.

---

## Best Practices

### ✅ DO

```python
# Set reasonable thresholds
# .coveragerc
[report]
fail_under = 80

# Exclude appropriate code
exclude_lines =
    pragma: no cover
    def __repr__
    if TYPE_CHECKING:

# Focus on meaningful tests
def test_business_logic():
    # Test behavior, not just coverage
    result = calculate_discount(price=100, is_member=True)
    assert result == 90.0
```

### ❌ DON'T

```python
# Don't test for coverage only
def test_everything():
    function_a()
    function_b()
    function_c()  # No assertions!

# Don't ignore untested critical code
def process_payment():  # pragma: no cover  # ❌ BAD!
    charge_card()

# Don't aim for 100% blindly
# Some code is legitimately hard to test
```

---

## Quick Reference

### Run Coverage
```bash
pytest --cov=app tests/              # Basic
pytest --cov=app --cov-branch        # Branch coverage
pytest --cov=app --cov-report=html   # HTML report
coverage run -m pytest               # Using coverage.py
```

### Generate Reports
```bash
coverage report                      # Terminal
coverage report -m                   # Show missing
coverage html                        # HTML
coverage xml                         # XML (Cobertura)
```

### Configuration
```ini
# .coveragerc or pyproject.toml
[run]
source = app
branch = True

[report]
fail_under = 80
show_missing = True
```

### CI Integration
```bash
pytest --cov=app --cov-report=xml    # Generate XML
diff-cover coverage.xml              # Differential
codecov                              # Upload to Codecov
```

---

Related: [pytest-guide.md](pytest-guide.md) | [unittest-guide.md](unittest-guide.md) | [mocking-reference.md](mocking-reference.md) | [Return to INDEX](INDEX.md)
