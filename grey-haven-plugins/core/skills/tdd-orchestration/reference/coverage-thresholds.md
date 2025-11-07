# Coverage Thresholds Reference

Comprehensive guide to coverage metrics, thresholds, quality gates, and enforcement strategies.

## Coverage Types

### Line Coverage

**Definition**: Percentage of code lines executed by tests.

```python
# app/discount.py
def calculate_discount(price, quantity):
    if quantity >= 10:              # Line 1
        return price * 0.9          # Line 2
    return price                     # Line 3

# Test
def test_bulk_discount():
    result = calculate_discount(100, 15)
    assert result == 90

# Line Coverage: 100% (3/3 lines executed)
```

**Calculation**:
```
Line Coverage = (Executed Lines / Total Lines) × 100
              = (3 / 3) × 100
              = 100%
```

**Limitations**:
- ✅ Easy to measure
- ❌ Doesn't guarantee correct behavior
- ❌ Doesn't test all paths

---

### Branch Coverage

**Definition**: Percentage of conditional branches executed.

```python
def calculate_discount(price, quantity):
    if quantity >= 10:              # Branch point
        return price * 0.9          # Branch A (true)
    return price                     # Branch B (false)

# Test 1: Only tests true branch
def test_bulk_discount():
    result = calculate_discount(100, 15)
    assert result == 90

# Line Coverage: 100% ✅
# Branch Coverage: 50% 🔴 (only Branch A tested)

# Test 2: Tests both branches
def test_no_discount():
    result = calculate_discount(100, 5)
    assert result == 100

# Branch Coverage: 100% ✅ (both branches tested)
```

**Calculation**:
```
Branch Coverage = (Branches Taken / Total Branches) × 100
                = (2 / 2) × 100
                = 100%
```

**Why It Matters**:
```python
# Bug hidden in untested branch!
def process_payment(amount, account):
    if account.balance >= amount:
        account.balance -= amount
        return "success"
    return "insufficient funds"  # Typo: "insufficent" ❌

# Test only true branch
def test_payment_success():
    account = Account(balance=100)
    result = process_payment(50, account)
    assert result == "success"

# Line Coverage: 100% ✅
# Branch Coverage: 50% 🔴
# Bug not caught! ❌
```

---

### Function Coverage

**Definition**: Percentage of functions executed.

```python
# app/auth.py
def login(email, password):         # Function 1
    pass

def logout(user_id):                # Function 2
    pass

def reset_password(email):          # Function 3
    pass

# Tests
def test_login():
    login("user@example.com", "password")

def test_logout():
    logout("user-123")

# Function Coverage: 67% (2/3 functions tested)
# reset_password() never called!
```

---

### Path Coverage

**Definition**: Percentage of unique execution paths tested.

```python
def calculate_price(base, is_member, has_coupon):
    price = base
    if is_member:                    # Branch 1
        price *= 0.9                 # 10% member discount
    if has_coupon:                   # Branch 2
        price *= 0.95                # 5% coupon discount
    return price

# Possible paths:
# 1. is_member=False, has_coupon=False → price = base
# 2. is_member=True,  has_coupon=False → price = base * 0.9
# 3. is_member=False, has_coupon=True  → price = base * 0.95
# 4. is_member=True,  has_coupon=True  → price = base * 0.9 * 0.95

# Tests
def test_no_discounts():
    assert calculate_price(100, False, False) == 100

def test_member_discount():
    assert calculate_price(100, True, False) == 90

# Path Coverage: 50% (2/4 paths tested)
```

**Path Coverage is Hardest**:
- With N branches, there are 2^N possible paths
- 10 branches = 1,024 paths!
- Often impractical to test all paths

---

### Critical Path Coverage

**Definition**: Coverage of business-critical code paths.

```python
# app/payment.py
def process_payment(amount, card):
    # CRITICAL PATH: Must be 100% tested!
    validate_card(card)
    charge_result = payment_gateway.charge(amount, card)
    if not charge_result.success:
        raise PaymentFailedError()
    return charge_result

# Non-critical: Logging
def log_payment(amount):
    logger.info(f"Payment processed: ${amount}")

# Critical Path Coverage: Must be 100%
# Overall Coverage: Can be <100% (logging is OK to skip)
```

**Critical Paths**:
- Payment processing
- Authentication/authorization
- Data validation
- Security checks
- Data integrity operations

---

## Recommended Thresholds

### Standard Thresholds

```
Metric              Minimum    Target     Critical Path
-------------------+-----------+----------+---------------
Line Coverage       80%        85-90%     100%
Branch Coverage     75%        80-85%     100%
Function Coverage   85%        90-95%     100%
Mutation Score      N/A        85%        95%
```

### By Code Category

```
Category                Line    Branch   Function
-----------------------+-------+--------+---------
Business Logic          85%     80%      90%
API Endpoints           90%     85%      95%
Data Access Layer       80%     75%      85%
Utilities               75%     70%      80%
Configuration           60%     50%      70%
Generated Code          Skip    Skip     Skip
```

### By Project Phase

```
Phase                  Line    Branch   Function
----------------------+-------+--------+---------
MVP/Prototype          60%     50%      70%
Early Development      70%     60%      75%
Production Ready       80%     75%      85%
Mature Product         85%+    80%+     90%+
```

---

## Coverage Enforcement

### Pre-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run tests with coverage
pytest --cov=app --cov-report=term-missing --cov-fail-under=80

if [ $? -ne 0 ]; then
    echo "❌ Coverage below 80% threshold"
    echo "Run 'pytest --cov=app --cov-report=html' to see details"
    exit 1
fi

echo "✅ Coverage check passed"
```

### CI/CD Quality Gates

```yaml
# .github/workflows/test.yml
name: Test & Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install dependencies
        run: pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=app \
                 --cov-report=xml \
                 --cov-report=term-missing \
                 --cov-fail-under=80

      - name: Check branch coverage
        run: |
          pytest --cov=app \
                 --cov-report=term-missing \
                 --cov-branch \
                 --cov-fail-under=75

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
        with:
          files: ./coverage.xml
          fail_ci_if_error: true
```

### Pull Request Gates

```yaml
# .github/workflows/pr-check.yml
name: PR Coverage Check

on: [pull_request]

jobs:
  coverage-diff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Full history for comparison

      - name: Get base coverage
        run: |
          git checkout ${{ github.base_ref }}
          pytest --cov=app --cov-report=json
          mv coverage.json base-coverage.json

      - name: Get PR coverage
        run: |
          git checkout ${{ github.head_ref }}
          pytest --cov=app --cov-report=json
          mv coverage.json pr-coverage.json

      - name: Compare coverage
        run: |
          BASE_COV=$(jq '.totals.percent_covered' base-coverage.json)
          PR_COV=$(jq '.totals.percent_covered' pr-coverage.json)
          DIFF=$(echo "$PR_COV - $BASE_COV" | bc)

          echo "Base coverage: $BASE_COV%"
          echo "PR coverage: $PR_COV%"
          echo "Diff: $DIFF%"

          if (( $(echo "$DIFF < 0" | bc -l) )); then
            echo "❌ Coverage decreased by $DIFF%"
            exit 1
          fi

          echo "✅ Coverage maintained or increased"
```

---

## Differential Coverage

### What is Differential Coverage?

**Only measure coverage on new/changed code** in PR.

```python
# Existing code (not changed)
def old_function():
    return "hello"  # Not counted in differential coverage

# New code (in this PR)
def new_function():
    if condition:      # Must be covered!
        return "yes"
    return "no"        # Must be covered!

# Differential Coverage: 100% required for new code
# Overall Coverage: Can be lower (old code may have gaps)
```

### Why Differential Coverage?

**Prevents new untested code**:
- Legacy code may have low coverage (technical debt)
- New code must have 100% coverage
- Gradually improves overall coverage

### Implementation

```bash
# Using coverage.py with diff
$ pip install diff_cover

# Generate coverage report
$ pytest --cov=app --cov-report=xml

# Check diff coverage
$ diff-cover coverage.xml --compare-branch=main --fail-under=100

# Fails if new code has <100% coverage
```

**CI/CD Integration**:
```yaml
- name: Check differential coverage
  run: |
    pytest --cov=app --cov-report=xml
    diff-cover coverage.xml \
              --compare-branch=origin/main \
              --fail-under=100 \
              --html-report=diff-coverage.html

- name: Comment PR with results
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ github.token }}
    MINIMUM_GREEN: 100
    MINIMUM_ORANGE: 80
```

---

## Coverage Exemptions

### When to Exempt Code

**Legitimate exemptions**:
1. **Generated code** (protobuf, OpenAPI)
2. **Defensive code** (should-never-happen cases)
3. **Platform-specific code** (OS-specific paths)
4. **Deprecation wrappers**

### Exemption Syntax

**Python (coverage.py)**:
```python
def critical_function():
    # Main logic (must be tested)
    result = process()

    if not result:  # pragma: no cover
        # Should never happen, but defensive
        raise SystemError("Unexpected state")

    return result
```

**JavaScript (Istanbul/NYC)**:
```javascript
function processData(data) {
    // Main logic
    const result = transform(data);

    /* istanbul ignore next */
    if (typeof result === 'undefined') {
        // Defensive code
        throw new Error('Unexpected undefined');
    }

    return result;
}
```

### Exemption Policy

```markdown
# Coverage Exemption Policy

## Approval Required
All exemptions must be:
1. Documented with `pragma: no cover` comment
2. Justified in code review
3. Tracked in exemption registry

## Valid Reasons
✅ Generated code
✅ Platform-specific branches
✅ Defensive "should-never-happen" code
✅ Deprecation wrappers

## Invalid Reasons
❌ "Too hard to test"
❌ "Not enough time"
❌ "Legacy code"
❌ "Low risk"
```

---

## Coverage Reports

### Terminal Report

```bash
$ pytest --cov=app --cov-report=term-missing

---------- coverage: platform darwin, python 3.11.0 -----------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
app/__init__.py              10      0   100%
app/auth.py                  45      3    93%   78-80
app/payment.py               67      0   100%
app/discount.py              34      8    76%   12-15, 45-48
-------------------------------------------------------
TOTAL                       156     11    93%
```

### HTML Report

```bash
$ pytest --cov=app --cov-report=html

# Opens in browser showing:
# - Per-file coverage
# - Line-by-line highlighting (green = covered, red = missed)
# - Branch coverage visualization
```

### XML Report (for CI/CD)

```bash
$ pytest --cov=app --cov-report=xml

# Generates coverage.xml
# Used by: Codecov, Coveralls, SonarQube
```

### JSON Report (for Scripting)

```bash
$ pytest --cov=app --cov-report=json

# Generates coverage.json
# Parse programmatically
```

---

## Coverage Badges

### GitHub README Badge

```markdown
# Add to README.md
![Coverage](https://img.shields.io/codecov/c/github/username/repo?token=YOUR_TOKEN)
```

### Codecov Integration

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
```

### Custom Badge

```python
# generate_badge.py
from coverage import Coverage
import json

cov = Coverage()
cov.load()
total = cov.report()

color = "red" if total < 70 else "yellow" if total < 80 else "brightgreen"

badge = {
    "schemaVersion": 1,
    "label": "coverage",
    "message": f"{total:.0f}%",
    "color": color
}

with open("coverage-badge.json", "w") as f:
    json.dump(badge, f)
```

---

## Common Pitfalls

### Pitfall #1: Chasing 100% Coverage

**Problem**: Obsessing over 100% coverage

```python
# Generated code, not worth testing
# app/pb/user_pb2.py (generated by protoc)
class UserProto:
    def __init__(self):
        pass  # Auto-generated boilerplate

# Don't waste time testing this!
```

**Solution**: Focus on critical paths, exempt generated code.

```python
# pytest.ini
[tool:pytest]
omit =
    */pb/*_pb2.py
    */migrations/*.py
    */tests/*.py
```

### Pitfall #2: Coverage Without Assertions

```python
# ❌ Bad: 100% coverage, 0% validation
def test_process_order():
    order = Order(items=[...])
    result = process_order(order)
    # No assertions! ❌
    # Coverage: 100% ✅ but meaningless!
```

**Solution**: Always assert something meaningful.

```python
# ✅ Good: Coverage + validation
def test_process_order():
    order = Order(items=[...])
    result = process_order(order)
    assert result.status == "confirmed"  # ✅ Validates behavior
    assert result.total > 0
```

### Pitfall #3: Ignoring Branch Coverage

```python
# 100% line coverage, 50% branch coverage
def calculate_discount(price, is_member):
    if is_member:
        return price * 0.9  # Line covered
    return price            # Line covered

# Test only true branch
def test_member_discount():
    assert calculate_discount(100, True) == 90
    # Line Coverage: 100% ✅
    # Branch Coverage: 50% 🔴
```

**Solution**: Always test both branches.

```python
def test_member_discount():
    assert calculate_discount(100, True) == 90

def test_no_discount():
    assert calculate_discount(100, False) == 100
    # Branch Coverage: 100% ✅
```

---

## Coverage + Mutation Testing

### Combined Metrics

```
Scenario                      Line Cov  Branch Cov  Mutation Score  Quality
----------------------------+---------+-----------+---------------+---------
Tests run, no assertions     100%      100%        0%              ❌
Weak assertions              100%      100%        50%             🔴
Good assertions              100%      100%        85%             ✅
Strong assertions            100%      100%        95%+            ✅✅
```

### Quality Matrix

```
If Coverage is HIGH (>80%) but Mutation Score is LOW (<70%):
  → Tests execute code but don't validate behavior
  → Strengthen assertions

If Coverage is LOW (<80%) and Mutation Score is HIGH (>85%):
  → Tests are strong but incomplete
  → Add more tests

If both Coverage and Mutation Score are HIGH:
  → Excellent test quality! ✅
```

---

## Team Policies

### Coverage Policy Example

```markdown
# Test Coverage Policy

## Minimum Thresholds
- Line Coverage: 80%
- Branch Coverage: 75%
- Critical Path: 100%

## Differential Coverage
- New code: 100% required
- Changed code: No decrease allowed

## Quality Gates
- Pre-commit: 80% line coverage
- Pull Request: No coverage decrease
- Main Branch: 85% line + 80% branch

## Exemptions
- Require code review approval
- Must document reason
- Reviewed quarterly

## Reporting
- Daily: Coverage dashboard updated
- Weekly: Team review of coverage trends
- Monthly: Critical path audit
```

---

Related: [Mutation Testing Reference](mutation-testing-reference.md) | [Red-Green-Refactor Guide](red-green-refactor-guide.md) | [Refactoring Patterns](refactoring-patterns.md) | [Return to INDEX](INDEX.md)
