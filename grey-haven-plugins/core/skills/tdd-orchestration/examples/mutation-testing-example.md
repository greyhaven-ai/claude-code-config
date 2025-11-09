# Mutation Testing Example: Validating Test Quality

Using mutation testing to find weak tests and improve test suite effectiveness from 73% to 94% mutation score.

## The Problem: High Coverage ≠ Good Tests

### Scenario

**Project**: E-commerce discount calculator
**Coverage**: 100% line coverage ✅
**Defects in Production**: 8 bugs in 2 weeks 🔴
**Root Cause**: Tests execute code but don't validate correctness

**The Illusion**:
```bash
$ pytest --cov=app tests/

Coverage: 100% ✅
All tests passing ✅
```

**The Reality**:
```bash
$ mutmut run

Mutation Score: 73% 🔴
79 surviving mutations (tests didn't catch bugs!)
```

---

## What is Mutation Testing?

### Concept

Mutation testing **changes your code** (introduces bugs) and checks if your tests catch them.

**If tests catch the mutation** → Test killed the mutant ✅ (good test!)
**If tests still pass** → Mutant survived 🔴 (weak test!)

### Example Mutation

**Original Code**:
```python
def calculate_discount(price, quantity):
    if quantity >= 10:
        return price * 0.9  # 10% discount
    return price
```

**Mutation #1**: Change `>=` to `>`
```python
def calculate_discount(price, quantity):
    if quantity > 10:  # Changed! Off-by-one error
        return price * 0.9
    return price
```

**Mutation #2**: Change `0.9` to `0.95`
```python
def calculate_discount(price, quantity):
    if quantity >= 10:
        return price * 0.95  # Wrong discount!
    return price
```

**Mutation #3**: Remove discount entirely
```python
def calculate_discount(price, quantity):
    if quantity >= 10:
        pass  # Deleted return statement!
    return price
```

### Weak Test Example

```python
# ❌ Weak test - only checks function exists
def test_calculate_discount():
    result = calculate_discount(100, 10)
    assert result is not None  # Too vague!
```

**This test gives 100% coverage but doesn't validate correctness!**

Mutations #1, #2, #3 all survive because test never checks the actual value.

### Strong Test Example

```python
# ✅ Strong test - validates exact behavior
def test_calculate_discount_at_threshold():
    result = calculate_discount(100, 10)
    assert result == 90  # Exact value check!

def test_calculate_discount_below_threshold():
    result = calculate_discount(100, 9)
    assert result == 100  # No discount

def test_calculate_discount_above_threshold():
    result = calculate_discount(100, 15)
    assert result == 135  # price * 0.9 * quantity... wait, bug!
```

**Mutation #1 killed** → Test caught off-by-one
**Mutation #2 killed** → Test caught wrong discount
**Mutation #3 killed** → Test caught missing return

---

## Real-World Example: Discount Calculator

### Initial Implementation

```python
# app/discount.py
def calculate_total_with_discount(items: list[dict]) -> float:
    """Calculate cart total with quantity discounts."""
    total = 0

    for item in items:
        price = item["price"]
        quantity = item["quantity"]

        # Quantity discount tiers
        if quantity >= 20:
            price = price * 0.8  # 20% discount
        elif quantity >= 10:
            price = price * 0.9  # 10% discount

        total += price * quantity

    return round(total, 2)
```

### Initial Tests (100% Coverage, Weak Quality)

```python
# tests/test_discount.py
def test_calculate_total():
    """Should calculate total with discounts."""
    items = [
        {"price": 10.00, "quantity": 15},
        {"price": 20.00, "quantity": 5},
    ]

    result = calculate_total_with_discount(items)

    # ❌ Weak assertion
    assert result > 0
    assert isinstance(result, float)
```

**Coverage**: 100% (every line executed) ✅
**Quality**: Unknown 🤔

---

## Step 1: Run Mutation Testing

### Install mutmut (Python)

```bash
pip install mutmut
```

### Run Mutations

```bash
$ mutmut run --paths-to-mutate app/discount.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mutation Testing Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Progress: 100% [================================]

Generated: 108 mutations
Killed: 79 (73%)
Survived: 29 (27%) 🔴
Timeout: 0 (0%)

Mutation Score: 73% 🔴 (needs improvement!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Analysis**: 29 surviving mutations means tests are weak!

---

## Step 2: Analyze Surviving Mutations

### Show Survivors

```bash
$ mutmut show 1

Mutation ID: 1
Status: Survived 🔴
File: app/discount.py
Line: 11

Original:
    if quantity >= 20:

Mutated:
    if quantity > 20:

Why it survived:
No test checks the boundary condition (quantity = 20)
```

```bash
$ mutmut show 5

Mutation ID: 5
Status: Survived 🔴
File: app/discount.py
Line: 12

Original:
    price = price * 0.8  # 20% discount

Mutated:
    price = price * 0.85  # Wrong discount!

Why it survived:
Test only checks result > 0, doesn't verify exact discount amount
```

```bash
$ mutmut show 12

Mutation ID: 12
Status: Survived 🔴
File: app/discount.py
Line: 20

Original:
    return round(total, 2)

Mutated:
    return round(total, 3)  # Different precision

Why it survived:
Test doesn't check decimal precision
```

---

## Step 3: Strengthen Tests

### Fix #1: Add Boundary Condition Tests

**Surviving Mutation**: `if quantity >= 20` → `if quantity > 20`

**New Tests**:
```python
def test_discount_at_20_quantity_boundary():
    """Should apply 20% discount at exactly 20 items."""
    items = [{"price": 10.00, "quantity": 20}]

    result = calculate_total_with_discount(items)

    # 20 items * $10 * 0.8 (20% discount) = $160.00
    assert result == 160.00  # Exact value!

def test_discount_below_20_quantity_boundary():
    """Should apply 10% discount at 19 items."""
    items = [{"price": 10.00, "quantity": 19}]

    result = calculate_total_with_discount(items)

    # 19 items * $10 * 0.9 (10% discount) = $171.00
    assert result == 171.00

def test_discount_at_10_quantity_boundary():
    """Should apply 10% discount at exactly 10 items."""
    items = [{"price": 10.00, "quantity": 10}]

    result = calculate_total_with_discount(items)

    # 10 items * $10 * 0.9 = $90.00
    assert result == 90.00

def test_no_discount_at_9_items():
    """Should not apply discount below 10 items."""
    items = [{"price": 10.00, "quantity": 9}]

    result = calculate_total_with_discount(items)

    # 9 items * $10 = $90.00 (no discount)
    assert result == 90.00
```

### Fix #2: Add Exact Value Assertions

**Surviving Mutation**: `price * 0.8` → `price * 0.85`

**New Tests**:
```python
def test_20_percent_discount_calculation():
    """Should calculate exactly 20% discount."""
    items = [{"price": 50.00, "quantity": 25}]

    result = calculate_total_with_discount(items)

    # 25 * $50 * 0.8 = $1,000.00
    assert result == 1000.00

def test_10_percent_discount_calculation():
    """Should calculate exactly 10% discount."""
    items = [{"price": 50.00, "quantity": 15}]

    result = calculate_total_with_discount(items)

    # 15 * $50 * 0.9 = $675.00
    assert result == 675.00
```

### Fix #3: Add Precision Tests

**Surviving Mutation**: `round(total, 2)` → `round(total, 3)`

**New Test**:
```python
def test_rounds_to_two_decimal_places():
    """Should round result to 2 decimal places."""
    items = [{"price": 10.999, "quantity": 3}]

    result = calculate_total_with_discount(items)

    # Should round to 2 decimals: $32.997 → $33.00
    assert result == 33.00
    assert len(str(result).split('.')[-1]) <= 2
```

### Fix #4: Add Multiple Items Test

**New Test**:
```python
def test_multiple_items_with_different_discounts():
    """Should correctly calculate mixed discount tiers."""
    items = [
        {"price": 10.00, "quantity": 25},  # 20% discount
        {"price": 20.00, "quantity": 15},  # 10% discount
        {"price": 30.00, "quantity": 5},   # No discount
    ]

    result = calculate_total_with_discount(items)

    # Item 1: 25 * $10 * 0.8 = $200.00
    # Item 2: 15 * $20 * 0.9 = $270.00
    # Item 3: 5 * $30 = $150.00
    # Total: $620.00
    assert result == 620.00
```

---

## Step 4: Re-run Mutation Testing

```bash
$ mutmut run --paths-to-mutate app/discount.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mutation Testing Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated: 108 mutations
Killed: 102 (94%) ✅
Survived: 6 (6%)
Timeout: 0 (0%)

Mutation Score: 94% ✅ (excellent!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Improvement: +21% mutation score ✅
```

---

## Step 5: Handle Remaining Survivors

### Analyze Last 6 Survivors

```bash
$ mutmut results

Survived mutations:
  ID 87: Changed variable name (cosmetic, acceptable)
  ID 91: Swapped equivalent conditions (acceptable)
  ID 94: Changed comment text (not code, acceptable)
  ID 99: Inlined constant (equivalent behavior, acceptable)
  ID 102: Reordered independent operations (acceptable)
  ID 105: Changed string formatting (output identical, acceptable)
```

**Decision**: These are **equivalent mutations** (don't change behavior).
**Action**: Mark as acceptable survivors.

```bash
$ mutmut mark 87 91 94 99 102 105 as acceptable

Effective Mutation Score: 100% ✅
```

---

## Results: Before vs After

### Test Suite Quality

```
Metric                    Before    After    Change
-----------------------------------------------------
Line Coverage             100%      100%     +0%
Branch Coverage           85%       95%      +10%
Tests                     4         12       +8 tests
Mutation Score            73%       94%      +21% ✅
Bugs Caught               Low       High     ✅
Defects in Production     8/2wk     0/2wk    ✅
```

### Mutation Score Breakdown

```
Mutation Type              Before    After
----------------------------------------------
Boundary Conditions        45%       100% ✅
Arithmetic Operators       60%       95% ✅
Boolean Logic              80%       100% ✅
Return Values              70%       90% ✅
Negations                  85%       100% ✅
----------------------------------------------
Overall                    73%       94% ✅
```

---

## Mutation Testing Tools

### Python: mutmut

```bash
# Install
pip install mutmut

# Run mutations
mutmut run

# Show results
mutmut results

# Show specific mutation
mutmut show 5

# Generate HTML report
mutmut html
```

**Configuration** (`.mutmut-config.py`):
```python
def pre_mutation(context):
    """Skip certain mutations."""
    # Don't mutate test files
    if "test_" in context.filename:
        context.skip = True
```

### JavaScript: Stryker

```bash
# Install
npm install --save-dev @stryker-mutator/core

# Run
npx stryker run

# Config (stryker.conf.json)
{
  "mutate": ["src/**/*.ts"],
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "progress"],
  "coverageAnalysis": "perTest"
}
```

### Java: PITest

```xml
<!-- pom.xml -->
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <configuration>
    <targetClasses>
      <param>com.example.*</param>
    </targetClasses>
    <targetTests>
      <param>com.example.*Test</param>
    </targetTests>
  </configuration>
</plugin>
```

```bash
# Run
mvn org.pitest:pitest-maven:mutationCoverage
```

---

## Best Practices

### 1. Run Mutations Regularly

**CI/CD Integration**:
```yaml
# .github/workflows/mutation-test.yml
name: Mutation Testing

on: [pull_request]

jobs:
  mutation-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run mutmut
        run: |
          pip install mutmut pytest
          mutmut run
      - name: Check mutation score
        run: |
          SCORE=$(mutmut show | grep "Mutation Score" | awk '{print $3}')
          if (( $(echo "$SCORE < 85" | bc -l) )); then
            echo "Mutation score $SCORE below threshold (85%)"
            exit 1
          fi
```

### 2. Set Mutation Score Thresholds

```
Mutation Score    Quality    Action
------------------------------------------
< 70%             Poor       Needs work
70-84%            Fair       Acceptable
85-94%            Good       Excellent ✅
95-100%           Excellent  Outstanding ✅
```

### 3. Focus on Critical Paths

Don't mutate everything - focus on critical code:

```bash
# Only mutate payment logic (critical!)
mutmut run --paths-to-mutate app/payment/

# Skip boilerplate code
mutmut run --paths-to-mutate app/ --exclude app/config/
```

### 4. Combine with Coverage

```bash
# Step 1: Check coverage first
pytest --cov=app --cov-report=term-missing

# Step 2: If coverage > 80%, run mutations
if [ $COVERAGE -gt 80 ]; then
  mutmut run
fi
```

---

## Common Mutation Types

### Arithmetic Operators

| Original | Mutation |
|----------|----------|
| `+` | `-` |
| `-` | `+` |
| `*` | `/` |
| `*` | `//` |
| `%` | `//` |

### Comparison Operators

| Original | Mutation |
|----------|----------|
| `>` | `>=` |
| `>=` | `>` |
| `<` | `<=` |
| `<=` | `<` |
| `==` | `!=` |
| `!=` | `==` |

### Boolean Logic

| Original | Mutation |
|----------|----------|
| `and` | `or` |
| `or` | `and` |
| `True` | `False` |
| `not` | `` (remove) |

### Return Values

| Original | Mutation |
|----------|----------|
| `return x` | `return None` |
| `return True` | `return False` |
| `return 0` | `return 1` |

---

## Key Takeaways

### 1. Coverage ≠ Quality

100% code coverage means every line executed.
94% mutation score means tests validate correctness.

### 2. Mutation Testing Finds Edge Cases

Boundary conditions (`>=` vs `>`), off-by-one errors, wrong constants - mutations catch what coverage misses.

### 3. Strong Assertions Matter

```python
# ❌ Weak
assert result is not None

# ✅ Strong
assert result == 90.00
```

### 4. Cost vs Benefit

**Mutation testing is slow** - run on critical code only.
**But the payoff is huge** - fewer production bugs.

---

Related: [Red-Green-Refactor Example](red-green-refactor-example.md) | [Outside-In TDD Example](outside-in-tdd-example.md) | [TDD Rescue Example](tdd-rescue-example.md) | [Return to INDEX](INDEX.md)
