# Code Quality Metrics

Understanding and interpreting code quality metrics including cyclomatic complexity, maintainability index, code duplication, and test coverage.

## Cyclomatic Complexity

**Definition**: Number of linearly independent paths through code

**Formula**: `Complexity = Edges - Nodes + 2` (for control flow graph)

**Practical Calculation**: Count decision points + 1
- Each `if`, `elif`, `while`, `for`, `and`, `or`, `except` adds 1

### Example Calculation

```python
def calculate_shipping(weight, country, express):  # Base: 1
    if weight < 0:                                  # +1 = 2
        raise ValueError("Invalid weight")

    if country == "US":                             # +1 = 3
        base_cost = 5
    elif country == "CA":                           # +1 = 4
        base_cost = 8
    else:
        base_cost = 15

    if express:                                     # +1 = 5
        base_cost *= 2

    if weight > 10:                                 # +1 = 6
        base_cost += 10

    return base_cost

# Cyclomatic Complexity: 6
```

### Complexity Ratings

```
Complexity   Rating      Risk          Recommendation
----------------------------------------------------
1-5          Simple      Low           No action needed
6-10         Moderate    Medium        Monitor, consider refactoring
11-20        Complex     High          Refactor soon
21-50        Very High   Very High     Refactor immediately
50+          Unmaintain. Critical      Rewrite
```

### Reducing Complexity

**Before** (Complexity: 15):
```python
def process_order(order, user, payment):
    if order:
        if user:
            if user.active:
                if payment:
                    if payment.valid:
                        if order.total > 0:
                            if user.balance >= order.total:
                                # Process order
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
```

**After** (Complexity: 7):
```python
def process_order(order, user, payment):
    # Guard clauses reduce branching
    _validate_order(order)
    _validate_user(user)
    _validate_payment(payment)
    _validate_balance(user, order)

    return _execute_order(order, user, payment)

def _validate_order(order):
    if not order or order.total <= 0:
        raise OrderError("Invalid order")

def _validate_user(user):
    if not user or not user.active:
        raise OrderError("Invalid user")

def _validate_payment(payment):
    if not payment or not payment.valid:
        raise OrderError("Invalid payment")

def _validate_balance(user, order):
    if user.balance < order.total:
        raise OrderError("Insufficient balance")
```

## Maintainability Index

**Definition**: Composite metric combining complexity, lines of code, and comments

**Formula** (simplified):
```
MI = 171
    - 5.2 * ln(HalsteadVolume)
    - 0.23 * CyclomaticComplexity
    - 16.2 * ln(LinesOfCode)
    + 50 * sin(sqrt(2.4 * PercentComments))
```

**Practical Interpretation**:
```
MI Score   Rating          Status
-----------------------------------
85-100     Excellent       Highly maintainable
65-84      Good            Maintainable
50-64      Moderate        Needs improvement
25-49      Difficult       Refactor soon
0-24       Unmaintainable  Rewrite
```

### Factors

1. **Lines of Code**: Shorter = better (but not too short)
2. **Cyclomatic Complexity**: Lower = better
3. **Halstead Volume**: Measures "information content"
4. **Comments**: More = better (to a point)

### Improving MI

**Before** (MI: 42 - Difficult):
```python
def process_data(data):
    # 150 lines
    # Complexity: 34
    # No docstrings
    # Mixed responsibilities
    pass
```

**After** (MI: 78 - Good):
```python
def process_data(data: List[DataPoint]) -> ProcessedData:
    """
    Process incoming data through validation and transformation pipeline.

    Args:
        data: List of data points to process

    Returns:
        ProcessedData object with validated and transformed data

    Raises:
        ValidationError: If data fails validation
    """
    validated_data = validate_data(data)  # 20 lines, complexity: 4
    transformed_data = transform_data(validated_data)  # 15 lines, complexity: 3
    return enrich_data(transformed_data)  # 10 lines, complexity: 2
```

## Code Duplication

**Definition**: Identical or similar code blocks repeated in codebase

**Types**:
1. **Exact duplication**: Identical code blocks
2. **Structural duplication**: Same structure, different names
3. **Semantic duplication**: Different code, same behavior

### Measuring Duplication

**Tools**:
- Python: `pylint --duplicate-code`
- JavaScript: `jscpd`
- Multi-language: `SonarQube`

**Example**:
```bash
# Check for duplicate code blocks (minimum 6 lines)
jscpd --min-lines 6 --threshold 5 src/

Duplication: 12.4%  # >5% is concerning
Files: 234
Duplicates: 89 blocks
Lines duplicated: 4,523 lines
```

### Acceptable Levels

```
Duplication   Rating    Action
------------------------------------
0-3%          Excellent No action needed
3-5%          Good      Monitor
5-10%         Fair      Reduce when refactoring
10-20%        Poor      Deduplicate systematically
>20%          Critical  Major refactoring needed
```

### Eliminating Duplication

**Before** (12% duplication):
```python
# users.py
def validate_email(email):
    if not email or "@" not in email:
        raise ValueError("Invalid email")

# orders.py
def validate_email(email):  # Duplicate!
    if not email or "@" not in email:
        raise ValueError("Invalid email")

# products.py
def validate_email(email):  # Duplicate!
    if not email or "@" not in email:
        raise ValueError("Invalid email")
```

**After** (0% duplication):
```python
# validators.py (centralized)
def validate_email(email: str) -> None:
    """Validate email format (single source of truth)."""
    if not email or "@" not in email:
        raise ValueError("Invalid email")

# users.py, orders.py, products.py
from validators import validate_email  # Reuse!
```

## Test Coverage

**Definition**: Percentage of code executed by tests

**Types**:
1. **Line Coverage**: Percentage of lines executed
2. **Branch Coverage**: Percentage of branches taken
3. **Function Coverage**: Percentage of functions called
4. **Statement Coverage**: Percentage of statements executed

### Coverage Goals

```
Code Type               Target    Minimum
-----------------------------------------
Critical Business Logic  95-100%   90%
Standard Features        80-90%    75%
Utilities                70-80%    60%
UI Components            60-70%    50%
Generated Code           0-50%     0%
```

### Measuring Coverage

**Python** (pytest-cov):
```bash
pytest --cov=app --cov-report=term-missing

Name                Stmts   Miss  Cover   Missing
-----------------------------------------------
app/users.py          120     12    90%    45-52, 89-93
app/orders.py         150     45    70%    60-105  ← Needs work
app/payments.py       100      5    95%    85-89   ← Good
-----------------------------------------------
TOTAL                 370     62    83%
```

**TypeScript** (Vitest):
```bash
vitest --coverage

File                  % Stmts  % Branch  % Funcs  % Lines
---------------------------------------------------------
UserService.ts         92.5     85.0      95.0     92.1
OrderService.ts        68.4     60.2      70.0     67.9   ← Low
PaymentService.ts      94.2     90.1      100      93.8   ← Good
---------------------------------------------------------
All files              85.0     78.4      88.3     84.6
```

### Coverage vs Quality

**80% coverage doesn't mean 80% tested**:

```python
# ❌ Bad: 100% coverage, useless tests
def add(a, b):
    return a + b

def test_add():
    add(2, 3)  # No assertion! Test passes but doesn't verify anything
    # Coverage: 100%, but test value: 0%

# ✅ Good: 100% coverage, meaningful test
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    # Coverage: 100%, test value: 100%
```

## Lines of Code (LOC)

**Types**:
- **Physical Lines**: All lines including blanks
- **Source Lines (SLOC)**: Excluding comments and blanks
- **Logical Lines**: Language-independent measure

### Interpreting LOC

```
Function Size    Rating      Action
------------------------------------
< 20 lines       Ideal       Maintain
20-50 lines      Good        Monitor
50-100 lines     Fair        Consider splitting
100-200 lines    Poor        Refactor
> 200 lines      Critical    Split immediately
```

**Not a Quality Metric Alone**:
- 1,000 lines of clear code > 500 lines of spaghetti
- But 1,000 lines of clear code > 2,000 lines of clear code

## Comment Density

**Definition**: Ratio of comment lines to code lines

**Formula**: `Comments / (Comments + Code) * 100`

### Optimal Density

```
Density    Rating    Interpretation
------------------------------------
< 10%      Low       Needs more documentation
10-30%     Good      Appropriate documentation
30-50%     High      Over-documented (noise)
> 50%      Excessive Code is too complex
```

**Quality > Quantity**:

```python
# ❌ Bad: High density, low value
# This function adds two numbers
# It takes two parameters
# It returns the sum
def add(a, b):  # a is first number, b is second number
    return a + b  # return the sum

# ✅ Good: Low density, high value
def calculate_tax(subtotal: float, tax_rate: float) -> float:
    """
    Calculate sales tax for order.

    Uses location-specific tax rate. Does not apply to tax-exempt items
    (handled separately in calculate_order_total).
    """
    return subtotal * tax_rate
```

## Cognitive Complexity

**Definition**: Measure of how difficult code is to understand

**Differs from Cyclomatic**: Counts nested logic heavier

### Example Calculation

```python
def example(a, b, c):
    if a:                    # +1 (decision)
        if b:                # +2 (nested decision, +1 for nesting)
            if c:            # +3 (nested decision, +2 for nesting)
                return 1

    for item in items:       # +1 (loop)
        if item.valid:       # +2 (nested in loop)
            process(item)

# Cognitive Complexity: 9
# Cyclomatic Complexity: 4
# (Cognitive weights nesting more heavily)
```

### Reducing Cognitive Complexity

**Before** (Cognitive: 12):
```python
def process_items(items):
    for item in items:
        if item.active:
            if item.valid:
                if item.price > 0:
                    if item.stock > 0:
                        process(item)
```

**After** (Cognitive: 3):
```python
def process_items(items):
    processable_items = [
        item for item in items
        if item.active and item.valid and item.price > 0 and item.stock > 0
    ]
    for item in processable_items:
        process(item)
```

## Composite Quality Score

**Combining Multiple Metrics**:

```
Overall Quality Score = (
    (100 - Complexity/50 * 100) * 0.25 +      # 25% weight
    Maintainability_Index * 0.20 +             # 20% weight
    (100 - Duplication_Percent) * 0.15 +       # 15% weight
    Test_Coverage * 0.25 +                     # 25% weight
    (100 - Cognitive_Complexity/20 * 100) * 0.15  # 15% weight
)

Score    Rating          Status
--------------------------------
85-100   Excellent       Production ready
70-84    Good            Minor improvements
55-69    Fair            Needs work
40-54    Poor            Refactor required
< 40     Critical        Do not deploy
```

## Metric Tracking Over Time

**Example Dashboard**:
```
Project: E-commerce Platform
Date: 2024-01-15

Metric                    Current  Target   Trend
-------------------------------------------------
Cyclomatic Complexity     8.2      < 10     ✅ ↓
Maintainability Index     76       > 70     ✅ ↑
Code Duplication          4.2%     < 5%     ✅ ↓
Test Coverage             84%      > 80%    ✅ ↑
Lines per Function        24       < 30     ✅ ↓
-------------------------------------------------
Overall Quality Score     82/100   > 80     ✅ PASS
```

## Anti-Patterns to Avoid

### 1. Optimizing for Metrics Instead of Quality

```python
# ❌ Bad: Artificially splitting to reduce LOC
def get_user(id):
    return _get(id)

def _get(id):
    return db.get(id)

# ✅ Good: Keep it simple
def get_user(user_id: str) -> User:
    return db.get(User, user_id)
```

### 2. Tests for Coverage Only

```python
# ❌ Bad: No assertions (100% coverage, 0% value)
def test_calculate_total():
    calculate_total([Item(10), Item(20)])

# ✅ Good: Meaningful test
def test_calculate_total():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total(items) == 30
```

### 3. Over-Commenting to Increase Density

```python
# ❌ Bad: Comments state the obvious
x = x + 1  # Increment x by 1
if x > 10:  # Check if x is greater than 10
    print(x)  # Print x

# ✅ Good: Comments explain "why"
x = x + 1  # Offset timezone difference
if x > BUSINESS_HOURS_END:
    print(x)  # Log after-hours access
```

## Tools and Automation

### Python
```bash
# Complexity
radon cc app/ -a  # Average complexity
radon mi app/     # Maintainability index

# Duplication
pylint app/ --duplicate-code

# Coverage
pytest --cov=app --cov-report=html
```

### TypeScript/JavaScript
```bash
# Complexity
npx es6-plato -r -d reports src/

# Duplication
npx jscpd src/

# Coverage
vitest --coverage
```

### CI/CD Integration
```yaml
# .github/workflows/quality.yml
- name: Check code quality
  run: |
    radon cc app/ -n C  # Fail if any function has C or worse rating
    pytest --cov=app --cov-fail-under=80
```

---

Related: [Security Checklist](security-checklist.md) | [Clarity Refactoring Rules](clarity-refactoring-rules.md) | [Return to INDEX](INDEX.md)
