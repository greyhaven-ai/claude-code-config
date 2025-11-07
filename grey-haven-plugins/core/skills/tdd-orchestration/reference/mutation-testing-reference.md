# Mutation Testing Reference

Comprehensive guide to mutation testing - tools, operators, score interpretation, and CI/CD integration.

## What is Mutation Testing?

### Concept

**Mutation testing** validates test quality by **introducing bugs** (mutations) into your code and checking if tests catch them.

```
Original Code → Mutate (introduce bug) → Run Tests
                                              ↓
                                    Tests Fail? ✅ Mutant killed (good test!)
                                    Tests Pass? 🔴 Mutant survived (weak test!)
```

### Why Coverage Isn't Enough

**Code Coverage** measures if code is **executed**.
**Mutation Score** measures if tests **validate correctness**.

```python
# Example: 100% coverage, but weak test
def calculate_discount(price, quantity):
    if quantity >= 10:
        return price * 0.9  # 10% discount
    return price

# Test with 100% coverage
def test_calculate_discount():
    result = calculate_discount(100, 10)
    assert result is not None  # ❌ Weak assertion!
    # Coverage: 100% ✅
    # Mutation score: 30% 🔴
```

**Mutation #1**: Change `0.9` to `0.95` → Test still passes! (wrong discount)
**Mutation #2**: Change `>=` to `>` → Test still passes! (off-by-one)
**Mutation #3**: Return original price → Test still passes! (no discount applied)

**Strong test**:
```python
def test_calculate_discount_at_threshold():
    result = calculate_discount(100, 10)
    assert result == 90  # ✅ Exact value check!
    # Coverage: 100% ✅
    # Mutation score: 100% ✅
```

---

## Mutation Testing Tools

### Python: mutmut

**Installation**:
```bash
pip install mutmut
```

**Basic Usage**:
```bash
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
    """Configure mutation behavior."""
    # Skip test files
    if "test_" in context.filename:
        context.skip = True

    # Skip migrations
    if "migrations/" in context.filename:
        context.skip = True

    # Skip generated code
    if context.filename.endswith("_pb2.py"):
        context.skip = True
```

**CI/CD Integration**:
```yaml
# .github/workflows/mutation-test.yml
name: Mutation Testing

on: [pull_request]

jobs:
  mutation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install dependencies
        run: |
          pip install mutmut pytest pytest-cov

      - name: Run mutation tests
        run: |
          mutmut run --paths-to-mutate app/

      - name: Check mutation score
        run: |
          mutmut junitxml > mutation-report.xml
          SCORE=$(mutmut results | grep "Mutation Score" | awk '{print $3}' | tr -d '%')
          if [ $SCORE -lt 85 ]; then
            echo "Mutation score $SCORE% below threshold (85%)"
            exit 1
          fi
```

---

### JavaScript/TypeScript: Stryker

**Installation**:
```bash
npm install --save-dev @stryker-mutator/core
npm install --save-dev @stryker-mutator/jest-runner  # For Jest
npm install --save-dev @stryker-mutator/vitest-runner  # For Vitest
```

**Configuration** (`stryker.conf.json`):
```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "progress", "dashboard"],
  "coverageAnalysis": "perTest",
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.spec.ts",
    "!src/**/*.test.ts"
  ],
  "thresholds": {
    "high": 90,
    "low": 75,
    "break": 70
  },
  "timeoutMS": 60000,
  "maxConcurrentTestRunners": 4
}
```

**Usage**:
```bash
# Run mutations
npx stryker run

# Run with specific config
npx stryker run --configFile stryker.conf.json

# Dry run (no mutations, just validation)
npx stryker run --dryRun
```

**CI/CD Integration**:
```yaml
# .github/workflows/mutation-test.yml
name: Stryker Mutation Testing

on: [pull_request]

jobs:
  mutation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install dependencies
        run: npm ci

      - name: Run Stryker
        run: npx stryker run

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: mutation-report
          path: reports/mutation/html/
```

---

### Java: PITest

**Maven Configuration** (`pom.xml`):
```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.15.0</version>
  <dependencies>
    <dependency>
      <groupId>org.pitest</groupId>
      <artifactId>pitest-junit5-plugin</artifactId>
      <version>1.2.0</version>
    </dependency>
  </dependencies>
  <configuration>
    <targetClasses>
      <param>com.example.myapp.*</param>
    </targetClasses>
    <targetTests>
      <param>com.example.myapp.*Test</param>
    </targetTests>
    <outputFormats>
      <outputFormat>XML</outputFormat>
      <outputFormat>HTML</outputFormat>
    </outputFormats>
    <mutationThreshold>80</mutationThreshold>
    <coverageThreshold>75</coverageThreshold>
    <timestampedReports>false</timestampedReports>
  </configuration>
</plugin>
```

**Usage**:
```bash
# Run mutations
mvn org.pitest:pitest-maven:mutationCoverage

# Run with custom config
mvn pitest:mutationCoverage -DtargetClasses=com.example.* -DtargetTests=com.example.*Test
```

**Gradle Configuration** (`build.gradle`):
```groovy
plugins {
    id 'info.solidsoft.pitest' version '1.15.0'
}

pitest {
    targetClasses = ['com.example.myapp.*']
    targetTests = ['com.example.myapp.*Test']
    outputFormats = ['XML', 'HTML']
    timestampedReports = false
    mutationThreshold = 80
    coverageThreshold = 75
}
```

---

### C#: Stryker.NET

**Installation**:
```bash
dotnet tool install --global dotnet-stryker
```

**Configuration** (`stryker-config.json`):
```json
{
  "stryker-config": {
    "project": "MyProject.csproj",
    "test-projects": ["MyProject.Tests.csproj"],
    "reporters": ["html", "progress", "cleartext"],
    "thresholds": {
      "high": 90,
      "low": 75,
      "break": 70
    },
    "mutation-level": "complete"
  }
}
```

**Usage**:
```bash
# Run mutations
dotnet stryker

# With specific config
dotnet stryker --config-file stryker-config.json
```

---

## Mutation Operators

### Arithmetic Operators

| Original | Mutation | Example |
|----------|----------|---------|
| `+` | `-` | `a + b` → `a - b` |
| `-` | `+` | `a - b` → `a + b` |
| `*` | `/` | `a * b` → `a / b` |
| `/` | `*` | `a / b` → `a * b` |
| `%` | `*` | `a % b` → `a * b` |
| `//` | `/` | `a // b` → `a / b` |

**Test Impact**:
```python
# Code
def calculate_tax(amount):
    return amount * 0.08  # Mutation: * → /

# Weak test (survives)
def test_calculate_tax():
    result = calculate_tax(100)
    assert result > 0  # Passes even with wrong operator!

# Strong test (kills mutation)
def test_calculate_tax():
    result = calculate_tax(100)
    assert result == 8.0  # Exact value check catches mutation!
```

---

### Comparison Operators

| Original | Mutation | Example |
|----------|----------|---------|
| `>` | `>=`, `<`, `!=` | `x > 5` → `x >= 5` |
| `>=` | `>`, `<=` | `x >= 10` → `x > 10` |
| `<` | `<=`, `>` | `x < 20` → `x <= 20` |
| `<=` | `<`, `>=` | `x <= 5` → `x < 5` |
| `==` | `!=` | `x == 0` → `x != 0` |
| `!=` | `==` | `x != 5` → `x == 5` |

**Test Impact**:
```python
# Code
def is_bulk_order(quantity):
    return quantity >= 10  # Mutation: >= → >

# Weak test (survives)
def test_is_bulk_order():
    assert is_bulk_order(15) is True  # Doesn't test boundary!

# Strong test (kills mutation)
def test_is_bulk_order_at_threshold():
    assert is_bulk_order(10) is True  # Boundary test catches off-by-one!
```

---

### Boolean Logic

| Original | Mutation | Example |
|----------|----------|---------|
| `and` | `or` | `a and b` → `a or b` |
| `or` | `and` | `a or b` → `a and b` |
| `not` | `` (remove) | `not x` → `x` |
| `True` | `False` | `return True` → `return False` |
| `False` | `True` | `return False` → `return True` |

**Test Impact**:
```python
# Code
def can_checkout(has_items, has_payment):
    return has_items and has_payment  # Mutation: and → or

# Weak test (survives)
def test_can_checkout():
    assert can_checkout(True, True) is True  # Doesn't test edge cases!

# Strong tests (kill mutation)
def test_cannot_checkout_without_items():
    assert can_checkout(False, True) is False  # Catches 'or' mutation!

def test_cannot_checkout_without_payment():
    assert can_checkout(True, False) is False  # Catches 'or' mutation!
```

---

### Statement Deletion

| Original | Mutation |
|----------|----------|
| `x = 5` | `` (delete) |
| `return x` | `return None` |
| `break` | `` (delete) |
| `continue` | `` (delete) |

**Test Impact**:
```python
# Code
def process_order(order):
    validate_order(order)  # Mutation: delete this line
    return save_order(order)

# Weak test (survives)
def test_process_order():
    result = process_order(order)
    assert result is not None  # Doesn't verify validation happened!

# Strong test (kills mutation)
def test_process_order_validates():
    invalid_order = Order(items=[])
    with pytest.raises(ValidationError):
        process_order(invalid_order)  # Catches missing validation!
```

---

### Return Value Mutations

| Original Type | Mutations |
|---------------|-----------|
| `return x` | `return None`, `return x + 1`, `return x - 1` |
| `return True` | `return False` |
| `return 0` | `return 1`, `return -1` |
| `return []` | `return [None]` |
| `return ""` | `return "X"` |

---

## Mutation Score Interpretation

### Score Ranges

```
Score      Quality      Status      Action
-----------+------------+-----------+------------------------
95-100%    Excellent    ✅         Maintain quality
85-94%     Good         🟢         Minor improvements
75-84%     Fair         🟡         Strengthen tests
60-74%     Poor         🟠         Significant work needed
< 60%      Critical     🔴         Major overhaul required
```

### What Score Means

**90% Mutation Score**:
- 90 out of 100 mutations killed by tests
- 10 mutations survived (potential weak spots)
- High confidence in test suite

**70% Mutation Score**:
- 70 out of 100 mutations killed
- 30 mutations survived (many weak spots)
- Tests execute code but don't validate behavior

### Acceptable Survivors

Not all surviving mutations are bad:

**Equivalent Mutations** (acceptable):
```python
# Original
def calculate(x):
    return x * 2

# Mutation (equivalent)
def calculate(x):
    return x + x  # Same behavior!
```

**Logging/Debug Code** (acceptable):
```python
# Original
def process():
    logger.info("Processing...")  # Mutation: delete
    return result

# Tests don't validate logging (acceptable)
```

**Performance Optimizations** (acceptable):
```python
# Original
items = [x for x in data]

# Mutation
items = list(data)  # Equivalent but different syntax
```

---

## Best Practices

### 1. Run on Critical Code Only

**Focus on**:
- Payment processing
- Authentication/authorization
- Data validation
- Security-critical paths

**Skip**:
- Configuration files
- Migrations
- Generated code
- Test files

```bash
# Run only on critical paths
mutmut run --paths-to-mutate app/payment/ app/auth/
```

### 2. Set Realistic Thresholds

```
Critical Paths:  95%+ mutation score
Business Logic:  85%+ mutation score
Infrastructure:  75%+ mutation score
Utilities:       70%+ mutation score
```

### 3. Incremental Improvement

```bash
# Current mutation score: 65%
# Don't aim for 95% immediately!

# Sprint 1: Target 70% (focus on critical paths)
# Sprint 2: Target 75% (expand to business logic)
# Sprint 3: Target 80% (utilities and edge cases)
# Sprint 4: Target 85%+ (maintain and improve)
```

### 4. Review Survivors Weekly

```bash
# Weekly review
$ mutmut results

# Investigate survivors
$ mutmut show <id>

# Strengthen tests or mark as acceptable
```

### 5. Cache Results

Mutation testing is slow - use caching:

```bash
# mutmut caches results automatically
# Only re-runs mutations for changed code

# Clear cache if needed
mutmut results --force
```

---

## Mutation Testing Workflow

### Step 1: Baseline

```bash
# Establish baseline
$ mutmut run

Mutation Score: 68% 🟠
```

### Step 2: Identify Weak Areas

```bash
# Show survivors
$ mutmut results

Surviving mutations:
  app/discount.py: 12 survivors
  app/validation.py: 8 survivors
  app/payment.py: 5 survivors
```

### Step 3: Strengthen Tests

```python
# Focus on file with most survivors
# app/discount.py had 12 survivors

# Add boundary tests
def test_discount_at_threshold():
    assert calculate_discount(100, 10) == 90

def test_discount_below_threshold():
    assert calculate_discount(100, 9) == 100
```

### Step 4: Re-run Mutations

```bash
$ mutmut run --paths-to-mutate app/discount.py

app/discount.py survivors: 12 → 3 ✅
```

### Step 5: Repeat

Continue strengthening tests until target score reached.

---

## Integration with Coverage

### Combined Metrics

```yaml
# .github/workflows/quality.yml
- name: Run tests with coverage
  run: pytest --cov=app --cov-report=xml

- name: Check coverage threshold
  run: |
    COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | tr -d '%')
    if [ $COVERAGE -lt 80 ]; then
      echo "Coverage $COVERAGE% below threshold"
      exit 1
    fi

- name: Run mutation tests
  run: mutmut run

- name: Check mutation score
  run: |
    SCORE=$(mutmut results | grep "Mutation Score" | awk '{print $3}' | tr -d '%')
    if [ $SCORE -lt 85 ]; then
      echo "Mutation score $SCORE% below threshold"
      exit 1
    fi
```

### Quality Matrix

```
Coverage   Mutation   Quality    Status
---------+----------+----------+---------
  100%      95%      Excellent   ✅
  95%       90%      Very Good   ✅
  85%       85%      Good        🟢
  80%       75%      Fair        🟡
  75%       70%      Poor        🟠
  < 75%     < 70%    Critical    🔴
```

---

## Common Issues

### Issue #1: Slow Execution

**Problem**: Mutation testing takes hours

**Solutions**:
```bash
# 1. Limit scope
mutmut run --paths-to-mutate app/critical/

# 2. Increase parallelization
mutmut run --runners 8

# 3. Use incremental mode (only changed files)
mutmut run --use-coverage

# 4. Set timeout
mutmut run --timeout 30
```

### Issue #2: Flaky Tests

**Problem**: Tests pass/fail randomly

**Solution**: Fix flaky tests before mutation testing
```python
# ❌ Flaky (time-dependent)
def test_expiration():
    token = create_token(expires_in=1)
    time.sleep(2)
    assert is_expired(token)  # Flaky!

# ✅ Stable (controlled time)
def test_expiration(freezer):
    token = create_token(expires_in=1)
    freezer.move_to('2024-01-01 00:00:02')
    assert is_expired(token)
```

### Issue #3: Too Many Survivors

**Problem**: 40% survival rate, overwhelming

**Solution**: Focus on critical paths first
```bash
# Instead of all code
mutmut run

# Focus on payment (critical!)
mutmut run --paths-to-mutate app/payment/
```

---

Related: [Red-Green-Refactor Guide](red-green-refactor-guide.md) | [Coverage Thresholds](coverage-thresholds.md) | [TDD Methodologies](tdd-methodologies.md) | [Return to INDEX](INDEX.md)
