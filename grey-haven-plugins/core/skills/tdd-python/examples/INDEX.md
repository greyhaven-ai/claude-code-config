# TDD Python Implementer Examples

Real-world Test-Driven Development examples for Python using pytest, unittest, and Python-specific testing patterns.

## Available Examples

### [pytest-tdd-example.md](pytest-tdd-example.md)
Complete TDD workflow using pytest - fixtures, parametrize, and modern testing patterns.

**Implements**: E-commerce shopping cart with discount rules
**Techniques**: pytest fixtures, parametrize decorator, conftest.py, pytest-cov
**Duration**: 45-minute TDD session
**Coverage**: 95% line coverage, 92% branch coverage
**Tests**: 18 tests, all passing

---

### [unittest-tdd-example.md](unittest-tdd-example.md)
TDD using unittest framework - TestCase classes, setUp/tearDown, assertions.

**Implements**: User authentication system with password hashing
**Techniques**: TestCase classes, setUp/tearDown, mock library, test discovery
**Duration**: 30-minute TDD session
**Coverage**: 94% line coverage, 90% branch coverage
**Tests**: 12 tests, all passing

---

### [async-testing-example.md](async-testing-example.md)
Testing async/await code with pytest-asyncio - coroutines, async context managers.

**Implements**: Async HTTP client with retry logic
**Techniques**: pytest-asyncio, asyncio.gather, async with, aioresponses mocking
**Duration**: 35-minute TDD session
**Coverage**: 93% line coverage
**Tests**: 15 tests, all async

---

### [mocking-strategies-example.md](mocking-strategies-example.md)
Comprehensive mocking strategies - when to mock, mock vs stub vs spy, patching.

**Implements**: Email notification service with external API
**Techniques**: unittest.mock, patch decorator, MagicMock, assert_called_with
**Duration**: 40-minute TDD session
**Coverage**: 96% line coverage
**Mocks**: 8 different mocking strategies demonstrated

---

### [fixtures-and-parametrize-example.md](fixtures-and-parametrize-example.md)
Advanced pytest features - fixtures for reusable setup, parametrize for multiple test cases.

**Implements**: Data validation pipeline with custom validators
**Techniques**: pytest fixtures, parametrize, fixture scope, conftest organization
**Duration**: 50-minute TDD session
**Coverage**: 97% line coverage
**Tests**: 24 tests from 8 parametrized functions

---

## Usage Patterns

### Learning TDD with pytest
Start with [pytest-tdd-example.md](pytest-tdd-example.md) for modern Python testing workflow.

### Learning unittest
Review [unittest-tdd-example.md](unittest-tdd-example.md) for traditional Python testing approach.

### Async Code
Reference [async-testing-example.md](async-testing-example.md) when testing async/await code.

### External Dependencies
Study [mocking-strategies-example.md](mocking-strategies-example.md) for mocking patterns.

### Test Organization
Learn from [fixtures-and-parametrize-example.md](fixtures-and-parametrize-example.md) for fixture patterns.

---

## Quick Reference

### pytest vs unittest

| Feature | pytest | unittest |
|---------|--------|----------|
| **Test Discovery** | Auto-discovers `test_*.py` | Requires `unittest.main()` |
| **Assertions** | Plain `assert` statements | `self.assertEqual()` methods |
| **Setup/Teardown** | Fixtures | `setUp()`/`tearDown()` |
| **Parametrization** | `@pytest.mark.parametrize` | Manual loops or subTest |
| **Mocking** | `mocker` fixture | `unittest.mock` |
| **Plugins** | Rich ecosystem | Standard library only |

### Test Naming Conventions

```python
# pytest
def test_should_return_empty_list_when_no_items():
    pass

# unittest
class TestShoppingCart(unittest.TestCase):
    def test_should_return_empty_list_when_no_items(self):
        pass
```

### Coverage Goals

- **Line Coverage**: 90%+ (pytest: 95%, unittest: 94%)
- **Branch Coverage**: 85%+ (pytest: 92%, unittest: 90%)
- **Edge Cases**: All boundary conditions tested
- **Error Handling**: All exceptions tested

---

Return to [tdd-python-implementer agent](../tdd-python.md) | [reference/](../reference/INDEX.md) | [templates/](../templates/INDEX.md) | [checklists/](../checklists/INDEX.md)
