# unittest Guide

Comprehensive unittest reference - Python's built-in testing framework with TestCase classes, assertions, and test discovery.

**Version**: Python 3.8+ standard library
**Installation**: None required (built-in)

---

## Basic Structure

### Test Class

```python
# tests/test_calculator.py
import unittest
from app.calculator import Calculator

class TestCalculator(unittest.TestCase):
    """Test suite for Calculator class."""

    def test_addition(self):
        """Should add two numbers correctly."""
        calc = Calculator()
        result = calc.add(2, 3)
        self.assertEqual(result, 5)

    def test_subtraction(self):
        """Should subtract two numbers correctly."""
        calc = Calculator()
        result = calc.subtract(10, 4)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()
```

### Running Tests

```bash
# Run all tests in file
python -m unittest tests/test_calculator.py

# Run specific test class
python -m unittest tests.test_calculator.TestCalculator

# Run specific test method
python -m unittest tests.test_calculator.TestCalculator.test_addition

# Discover and run all tests
python -m unittest discover

# Verbose output
python -m unittest -v tests/

# Run file directly (if __name__ == '__main__')
python tests/test_calculator.py
```

---

## Assertion Methods

### Equality Assertions

```python
class TestAssertions(unittest.TestCase):

    def test_equality(self):
        self.assertEqual(2 + 2, 4)
        self.assertEqual("hello", "hello")
        self.assertEqual([1, 2], [1, 2])

    def test_inequality(self):
        self.assertNotEqual(5, 10)
        self.assertNotEqual("a", "b")

    def test_identity(self):
        x = [1, 2, 3]
        y = x
        self.assertIs(x, y)  # Same object
        self.assertIsNot(x, [1, 2, 3])  # Different objects
```

### Boolean Assertions

```python
def test_boolean(self):
    self.assertTrue(True)
    self.assertTrue(1 < 2)
    self.assertFalse(False)
    self.assertFalse(5 > 10)
```

### None Assertions

```python
def test_none(self):
    value = None
    self.assertIsNone(value)

    value = "something"
    self.assertIsNotNone(value)
```

### Membership Assertions

```python
def test_membership(self):
    self.assertIn(3, [1, 2, 3, 4])
    self.assertIn("a", {"a": 1, "b": 2})
    self.assertNotIn("x", "hello")
```

### Comparison Assertions

```python
def test_comparison(self):
    self.assertGreater(10, 5)
    self.assertGreaterEqual(10, 10)
    self.assertLess(3, 7)
    self.assertLessEqual(5, 5)
```

### Floating Point Assertions

```python
def test_floating_point(self):
    # Using assertAlmostEqual for floating point comparison
    self.assertAlmostEqual(0.1 + 0.2, 0.3)
    self.assertAlmostEqual(3.14159, 3.14, places=2)
```

### Collection Assertions

```python
def test_collections(self):
    # Check if sequences are equal (order matters)
    self.assertListEqual([1, 2, 3], [1, 2, 3])
    self.assertTupleEqual((1, 2), (1, 2))

    # Check if sets/dicts are equal (order doesn't matter)
    self.assertSetEqual({1, 2, 3}, {3, 2, 1})
    self.assertDictEqual({"a": 1}, {"a": 1})

    # Check dict contains subset
    self.assertDictContainsSubset(
        {"a": 1},
        {"a": 1, "b": 2}
    )
```

### String Assertions

```python
def test_strings(self):
    # Regex matching
    self.assertRegex("hello123", r"hello\d+")
    self.assertNotRegex("abc", r"\d+")

    # Multi-line string comparison
    self.assertMultiLineEqual(
        "line1\nline2",
        "line1\nline2"
    )
```

### Exception Assertions

```python
def test_exceptions(self):
    # Basic exception assertion
    with self.assertRaises(ValueError):
        int("not a number")

    # Check exception message
    with self.assertRaises(ValueError) as context:
        raise ValueError("Invalid input")

    self.assertIn("Invalid", str(context.exception))

    # Assert no exception raised
    with self.assertRaises(ZeroDivisionError):
        10 / 0  # Raises exception - test passes

def test_specific_exception_args(self):
    # Check exception arguments
    with self.assertRaisesRegex(ValueError, "must be positive"):
        validate_age(-5)
```

### Warning Assertions

```python
def test_warnings(self):
    with self.assertWarns(DeprecationWarning):
        deprecated_function()

    with self.assertWarnsRegex(UserWarning, "deprecated"):
        another_deprecated_function()
```

---

## Setup and Teardown

### Method-Level Setup

```python
class TestDatabase(unittest.TestCase):
    """Setup and teardown for each test method."""

    def setUp(self):
        """Called before each test method."""
        self.db = Database.connect("test.db")
        self.db.create_tables()

    def tearDown(self):
        """Called after each test method."""
        self.db.drop_tables()
        self.db.close()

    def test_insert(self):
        """Database is fresh for this test."""
        self.db.insert("users", {"name": "Alice"})
        self.assertEqual(self.db.count("users"), 1)

    def test_query(self):
        """Database is fresh again (setUp called)."""
        self.assertEqual(self.db.count("users"), 0)
```

### Class-Level Setup

```python
class TestExpensiveResource(unittest.TestCase):
    """Setup once for entire test class."""

    @classmethod
    def setUpClass(cls):
        """Called once before any test methods."""
        cls.expensive_resource = ExpensiveResource()
        cls.expensive_resource.initialize()

    @classmethod
    def tearDownClass(cls):
        """Called once after all test methods."""
        cls.expensive_resource.cleanup()

    def test_use_resource(self):
        """Resource shared across all tests in this class."""
        result = self.expensive_resource.query()
        self.assertIsNotNone(result)
```

### Module-Level Setup

```python
# tests/test_module.py

def setUpModule():
    """Called once before all tests in module."""
    global test_database
    test_database = Database.connect("test.db")

def tearDownModule():
    """Called once after all tests in module."""
    test_database.close()

class TestFeatureA(unittest.TestCase):
    def test_something(self):
        test_database.query("...")
```

---

## Test Organization

### Test Suites

```python
# Manually create test suite
import unittest
from tests.test_calculator import TestCalculator
from tests.test_database import TestDatabase

def suite():
    """Create custom test suite."""
    suite = unittest.TestSuite()

    # Add specific tests
    suite.addTest(TestCalculator('test_addition'))
    suite.addTest(TestDatabase('test_insert'))

    # Add all tests from class
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCalculator))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
```

### Test Discovery

```bash
# Discover all test files matching pattern
python -m unittest discover -s tests -p "test_*.py"

# Custom pattern
python -m unittest discover -s tests -p "*_test.py"

# Start directory and top-level directory
python -m unittest discover -s tests -t .
```

---

## Skipping Tests

### Skip Decorators

```python
import unittest
import sys

class TestFeatures(unittest.TestCase):

    @unittest.skip("Not implemented yet")
    def test_future_feature(self):
        pass

    @unittest.skipIf(sys.platform == "win32", "Unix only")
    def test_unix_specific(self):
        pass

    @unittest.skipUnless(sys.platform == "linux", "Linux only")
    def test_linux_specific(self):
        pass

    @unittest.expectedFailure
    def test_known_bug(self):
        """Known to fail, won't count as failure."""
        self.assertEqual(buggy_function(), "expected")
```

### Conditional Skip

```python
class TestConditional(unittest.TestCase):

    def test_something(self):
        if not has_feature():
            self.skipTest("Feature not available")

        # Test code here
```

---

## Mocking with unittest.mock

### Basic Mock

```python
from unittest.mock import Mock

class TestEmailService(unittest.TestCase):

    def test_send_email(self):
        # Create mock SMTP client
        mock_smtp = Mock()
        mock_smtp.send.return_value = {"status": "sent"}

        service = EmailService(smtp_client=mock_smtp)
        result = service.send_email("user@example.com", "Hello")

        # Verify mock was called
        mock_smtp.send.assert_called_once()
        self.assertEqual(result["status"], "sent")
```

### Patch Decorator

```python
from unittest.mock import patch

class TestAPI(unittest.TestCase):

    @patch('app.api.requests.get')
    def test_fetch_data(self, mock_get):
        """Patch requests.get for this test."""
        mock_get.return_value.json.return_value = {"data": "test"}

        result = fetch_data("http://api.example.com")

        mock_get.assert_called_once_with("http://api.example.com")
        self.assertEqual(result["data"], "test")
```

### Patch Context Manager

```python
def test_with_patch_context(self):
    """Patch only within context."""
    with patch('app.module.external_call') as mock_call:
        mock_call.return_value = "mocked"

        result = function_that_calls_external()

        self.assertEqual(result, "mocked")

    # Outside context: real external_call used
```

---

## SubTests

### Testing Multiple Cases

```python
class TestSubTests(unittest.TestCase):

    def test_multiple_cases(self):
        """Continue testing even if one case fails."""
        for value, expected in [(2, 4), (3, 9), (4, 16)]:
            with self.subTest(value=value, expected=expected):
                result = value ** 2
                self.assertEqual(result, expected)

# Output shows which specific subtest failed:
# FAIL: test_multiple_cases (test_example.TestSubTests) (expected=9, value=3)
```

---

## Test Runners

### TextTestRunner

```python
# Basic runner
if __name__ == '__main__':
    unittest.main()

# Custom runner with verbosity
if __name__ == '__main__':
    unittest.main(verbosity=2)

# Custom runner with options
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    suite = unittest.TestLoader().discover('tests')
    runner.run(suite)
```

### XMLTestRunner (for CI)

```python
# Using xmlrunner package
import xmlrunner

if __name__ == '__main__':
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
```

---

## Best Practices

### Test Independence

```python
# Good: Each test is independent
class TestIndependent(unittest.TestCase):

    def setUp(self):
        self.counter = Counter()  # Fresh for each test

    def test_increment(self):
        self.counter.increment()
        self.assertEqual(self.counter.value, 1)

    def test_decrement(self):
        self.counter.decrement()
        self.assertEqual(self.counter.value, -1)  # Doesn't depend on test_increment

# Bad: Tests depend on each other
class TestDependent(unittest.TestCase):  # ❌ ANTI-PATTERN

    counter = Counter()  # Shared state!

    def test_a_increment(self):
        self.counter.increment()

    def test_b_check_value(self):  # Depends on test_a!
        self.assertEqual(self.counter.value, 1)
```

### Descriptive Names

```python
# Good
def test_login_with_invalid_password_returns_none(self):
    pass

# Bad
def test_login(self):
    pass
```

### AAA Pattern

```python
def test_shopping_cart_total(self):
    # Arrange
    cart = ShoppingCart()
    cart.add_item(price=10.00, quantity=2)

    # Act
    total = cart.get_total()

    # Assert
    self.assertEqual(total, 20.00)
```

---

## Command-Line Options

```bash
# Verbose output
python -m unittest -v

# Buffer stdout/stderr (show only on failure)
python -m unittest -b

# Catch Ctrl+C gracefully
python -m unittest -c

# Start directory for discovery
python -m unittest discover -s tests

# Pattern for test files
python -m unittest discover -p "*_test.py"

# Failfast (stop on first failure)
python -m unittest -f
```

---

## Coverage with unittest

```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run -m unittest discover

# Generate report
coverage report

# Generate HTML report
coverage html

# View in browser
open htmlcov/index.html
```

---

## Comparison: unittest vs pytest

| Feature | unittest | pytest |
|---------|----------|--------|
| **Test discovery** | `python -m unittest discover` | `pytest` |
| **Test style** | Class-based (`TestCase`) | Function-based or class |
| **Assertions** | `self.assertEqual()` | Plain `assert` |
| **Setup/teardown** | `setUp()/tearDown()` | Fixtures |
| **Parametrize** | Manual (subTest) | `@pytest.mark.parametrize` |
| **Mocking** | `unittest.mock` | `pytest-mock` (mocker) |
| **Dependencies** | Built-in | `pip install pytest` |
| **Plugin ecosystem** | Limited | Extensive |

### When to Use unittest

✅ **Good for**:
- No external dependencies allowed
- Corporate environments
- Legacy codebases
- Teams familiar with JUnit (Java)

❌ **Consider pytest when**:
- Modern Python project (3.6+)
- Want simpler syntax
- Need fixtures
- Want parametrize
- Want plugins

---

## Migration: unittest → pytest

pytest can run unittest tests!

```python
# unittest test (works with pytest too!)
import unittest

class TestExample(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1, 1)

# Run with pytest
$ pytest tests/test_example.py  # Works!
```

**Gradual migration**:
1. Run existing unittest tests with pytest
2. Write new tests using pytest style
3. Gradually convert old tests

---

Related: [pytest-guide.md](pytest-guide.md) | [mocking-reference.md](mocking-reference.md) | [coverage-guide.md](coverage-guide.md) | [Return to INDEX](INDEX.md)
