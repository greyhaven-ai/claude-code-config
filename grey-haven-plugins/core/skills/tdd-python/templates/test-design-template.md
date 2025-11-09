# Test Design Template

Pre-implementation planning template for designing test suites before writing code.

**Feature**: [Feature Name]
**Module**: [Module/Class Name]
**Date**: [YYYY-MM-DD]
**Designer**: [Name]

---

## Feature Overview

### Description

[Detailed description of the feature to be implemented]

### User Story

```
As a [user type]
I want to [action]
So that [benefit]
```

### Acceptance Criteria

1. [ ] [Criterion 1]
2. [ ] [Criterion 2]
3. [ ] [Criterion 3]

---

## API Design

### Function/Method Signatures

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Brief description.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Class Interface

```python
class ClassName:
    """Class description."""

    def __init__(self, arg1: Type1, arg2: Type2) -> None:
        """Constructor description."""
        pass

    def method1(self, param: Type) -> ReturnType:
        """Method description."""
        pass

    @property
    def property_name(self) -> Type:
        """Property description."""
        pass
```

---

## Test Case Inventory

### Happy Path Tests

| Test ID | Test Name | Input | Expected Output | Priority |
|---------|-----------|-------|-----------------|----------|
| HP-01 | `test_[name]_with_valid_input` | [example] | [result] | High |
| HP-02 | `test_[name]_returns_expected_type` | [example] | [type] | High |
| HP-03 | `test_[name]_with_typical_values` | [example] | [result] | High |

### Edge Cases

| Test ID | Test Name | Input | Expected Output | Priority |
|---------|-----------|-------|-----------------|----------|
| EC-01 | `test_[name]_with_empty_input` | `[]` | [result] | High |
| EC-02 | `test_[name]_with_single_item` | `[1]` | [result] | Medium |
| EC-03 | `test_[name]_with_max_value` | `MAX_INT` | [result] | Medium |
| EC-04 | `test_[name]_with_min_value` | `MIN_INT` | [result] | Medium |
| EC-05 | `test_[name]_with_boundary_value` | [boundary] | [result] | High |

### Error Cases

| Test ID | Test Name | Input | Expected Exception | Priority |
|---------|-----------|-------|-------------------|----------|
| ER-01 | `test_[name]_raises_on_null` | `None` | `TypeError` | High |
| ER-02 | `test_[name]_raises_on_invalid_type` | `"string"` | `TypeError` | High |
| ER-03 | `test_[name]_raises_on_negative` | `-1` | `ValueError` | Medium |

### State Tests (For Stateful Objects)

| Test ID | Test Name | Initial State | Action | Expected State | Priority |
|---------|-----------|---------------|--------|----------------|----------|
| ST-01 | `test_[name]_changes_state` | [state1] | [action] | [state2] | High |
| ST-02 | `test_[name]_maintains_invariant` | [state] | [action] | [invariant] | High |

### Integration Tests

| Test ID | Test Name | Dependencies | Expected Behavior | Priority |
|---------|-----------|--------------|-------------------|----------|
| IT-01 | `test_[name]_with_database` | DB connection | [behavior] | High |
| IT-02 | `test_[name]_with_external_api` | API mock | [behavior] | Medium |

---

## Test Data Design

### Valid Test Data

```python
# fixtures/valid_data.py

VALID_USER = {
    "username": "john_doe",
    "email": "john@example.com",
    "age": 30
}

VALID_PRODUCT = {
    "id": "PROD-001",
    "name": "Widget",
    "price": 9.99,
    "quantity": 100
}
```

### Invalid Test Data

```python
# fixtures/invalid_data.py

INVALID_EMAIL = "not-an-email"
INVALID_AGE = -5
INVALID_PRODUCT_ID = ""
```

### Boundary Test Data

```python
# fixtures/boundary_data.py

MIN_QUANTITY = 0
MAX_QUANTITY = 1000000
BOUNDARY_PRICE = 0.01
```

---

## Fixture Design

### Function-Scoped Fixtures

```python
@pytest.fixture
def fixture_name():
    """Fixture description."""
    # Setup
    resource = create_resource()

    yield resource

    # Teardown
    resource.cleanup()
```

### Class-Scoped Fixtures

```python
@pytest.fixture(scope="class")
def expensive_resource():
    """Expensive resource shared across test class."""
    resource = ExpensiveResource()
    resource.initialize()

    yield resource

    resource.cleanup()
```

### Parametrized Fixtures

```python
@pytest.fixture(params=[
    "scenario_1",
    "scenario_2",
    "scenario_3"
])
def multi_scenario(request):
    """Fixture that provides multiple scenarios."""
    return get_scenario(request.param)
```

---

## Mock Strategy

### External Dependencies to Mock

| Dependency | Mock Type | Reason | Strategy |
|------------|-----------|--------|----------|
| Database | Mock | No real DB in tests | Use in-memory DB / mock connection |
| HTTP API | Mock | No network calls | Use `responses` / `aioresponses` |
| File System | Mock | No disk I/O | Use `tmp_path` fixture |
| Time | Mock | Deterministic tests | Patch `datetime.now()` |
| Random | Mock | Deterministic tests | Patch `random.random()` |

### Mock Implementations

```python
# For Database
@pytest.fixture
def mock_database():
    mock_db = Mock()
    mock_db.query.return_value = [{"id": 1, "name": "test"}]
    return mock_db

# For HTTP API
@pytest.fixture
def mock_http_client():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://api.example.com/data",
            json={"result": "success"},
            status=200
        )
        yield rsps
```

---

## Parametrize Strategy

### Test Scenarios

```python
@pytest.mark.parametrize("input,expected", [
    # (input, expected_output)
    (0, 0),                    # Edge: zero
    (1, 1),                    # Edge: one
    (5, 25),                   # Typical: small positive
    (100, 10000),              # Typical: large positive
    pytest.param(-1, None, marks=pytest.mark.xfail, id="negative"),  # Error case
])
def test_function_with_various_inputs(input, expected):
    """Test function with parametrized inputs."""
    result = function(input)
    assert result == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("width,height,expected_area", [
    (10, 20, 200),
    (5, 5, 25),
    (1, 1, 1),
    (0, 10, 0),  # Edge case: zero width
])
def test_calculate_area(width, height, expected_area):
    """Test area calculation with various dimensions."""
    area = calculate_area(width, height)
    assert area == expected_area
```

---

## Coverage Goals

### Target Coverage

| Metric | Target | Minimum Acceptable |
|--------|--------|-------------------|
| **Line Coverage** | 95% | 80% |
| **Branch Coverage** | 90% | 75% |
| **Function Coverage** | 95% | 85% |

### Exclusions

```python
# Lines excluded from coverage
if __name__ == "__main__":  # pragma: no cover
    main()

def debug_function():  # pragma: no cover
    """Development only."""
    import pdb; pdb.set_trace()
```

---

## Test Organization

### Directory Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_[module1].py
│   └── test_[module2].py
├── integration/
│   └── test_[integration].py
└── fixtures/
    ├── valid_data.py
    └── invalid_data.py
```

### Test Class Structure

```python
class TestClassName:
    """Test suite for ClassName."""

    # Happy path tests
    def test_method_with_valid_input(self):
        pass

    # Edge cases
    def test_method_with_empty_input(self):
        pass

    # Error cases
    def test_method_raises_on_invalid_input(self):
        pass

    # State tests
    def test_method_changes_state_correctly(self):
        pass
```

---

## Test Execution Plan

### Phase 1: Core Functionality (Priority: High)

**Duration**: [Estimated time]

**Tests**:
- [ ] HP-01: Valid input test
- [ ] HP-02: Type validation test
- [ ] ER-01: Null input exception test

**Success Criteria**: Core functionality working, basic error handling

---

### Phase 2: Edge Cases (Priority: Medium)

**Duration**: [Estimated time]

**Tests**:
- [ ] EC-01: Empty input test
- [ ] EC-02: Single item test
- [ ] EC-05: Boundary value test

**Success Criteria**: Edge cases handled correctly

---

### Phase 3: Integration (Priority: High)

**Duration**: [Estimated time]

**Tests**:
- [ ] IT-01: Database integration test
- [ ] IT-02: API integration test

**Success Criteria**: Works with external dependencies

---

### Phase 4: Performance (Priority: Low)

**Duration**: [Estimated time]

**Tests**:
- [ ] Performance test for large inputs
- [ ] Memory usage test

**Success Criteria**: Meets performance requirements

---

## Risk Assessment

### Testing Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Flaky tests due to external dependencies | Medium | High | Use mocks/stubs |
| Slow tests (> 1s) | Medium | Medium | Use lightweight fixtures |
| Incomplete edge case coverage | Low | High | Systematic edge case analysis |
| Mock drift (mocks don't match reality) | Medium | High | Integration tests |

---

## Dependencies

### Test Dependencies

```txt
# requirements-test.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-asyncio==0.21.1  # If testing async code
responses==0.24.0       # If mocking HTTP
```

### Setup

```bash
pip install -r requirements-test.txt
```

---

## Checklist

### Before Starting

- [ ] Feature requirements clearly understood
- [ ] API design documented
- [ ] Test cases identified
- [ ] Test data prepared
- [ ] Fixtures planned
- [ ] Mock strategy defined
- [ ] Coverage goals set

### During Development

- [ ] Follow RED-GREEN-REFACTOR cycle
- [ ] Write failing test first
- [ ] Minimal implementation to pass
- [ ] Refactor for quality
- [ ] Run tests frequently
- [ ] Check coverage regularly

### After Completion

- [ ] All tests passing
- [ ] Coverage goals met
- [ ] Code refactored
- [ ] Documentation updated
- [ ] Review completed
- [ ] Ready for merge

---

## Notes

[Any additional notes, considerations, or questions]

---

## Example: Shopping Cart Test Design

### Feature: Shopping Cart

**Module**: `app.cart`

#### API Design

```python
class ShoppingCart:
    def add_item(self, product_id: str, name: str, price: float, quantity: int = 1) -> None:
        """Add item to cart."""

    def remove_item(self, product_id: str) -> None:
        """Remove item from cart."""

    def get_subtotal(self) -> float:
        """Calculate subtotal before discounts."""

    def get_discount_amount(self) -> float:
        """Calculate discount based on subtotal."""

    def get_total(self) -> float:
        """Calculate final total with discounts."""
```

#### Test Cases (Abbreviated)

| ID | Test Name | Input | Expected |
|----|-----------|-------|----------|
| HP-01 | `test_add_item_increases_count` | Add 1 item | Count = 1 |
| HP-02 | `test_subtotal_sums_prices` | 2 items @ $10 | $20 |
| EC-01 | `test_empty_cart_total_is_zero` | Empty cart | $0 |
| ER-01 | `test_add_item_negative_price_raises` | Price = -5 | ValueError |

#### Coverage Goals

- Line: 95%
- Branch: 92%
- Focus: Discount logic (complex branches)

---

**Template Version**: 1.0
**Last Updated**: 2024-01-15
