# pytest Guide

Complete pytest reference - modern Python testing framework with fixtures, parametrize, marks, and rich plugin ecosystem.

**Version**: pytest 7.4+
**Installation**: `pip install pytest pytest-cov pytest-mock`

---

## Installation & Configuration

### Installation

```bash
# Basic
pip install pytest

# With plugins
pip install pytest pytest-cov pytest-mock pytest-asyncio pytest-xdist

# Development
pip install pytest pytest-cov pytest-mock pre-commit
```

### pytest.ini Configuration

```ini
# pytest.ini
[pytest]
# Test discovery patterns
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Test paths
testpaths = tests

# Command-line options (always applied)
addopts =
    --verbose
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-branch
    -ra

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    smoke: marks tests as smoke tests

# Asyncio mode
asyncio_mode = auto

# Minimum Python version
minversion = 7.0
```

---

## Test Discovery

### Automatic Discovery

pytest automatically finds tests matching these patterns:

**Files**: `test_*.py` or `*_test.py`
**Classes**: `Test*` (no `__init__` method)
**Functions**: `test_*`

```python
# tests/test_calculator.py - DISCOVERED
def test_add():
    pass

class TestCalculator:  # DISCOVERED
    def test_multiply(self):
        pass

# tests/calculator_test.py - ALSO DISCOVERED
def test_subtract():
    pass
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_calculator.py

# Specific test
pytest tests/test_calculator.py::test_add

# Specific class
pytest tests/test_calculator.py::TestCalculator

# Specific method
pytest tests/test_calculator.py::TestCalculator::test_multiply

# Pattern matching
pytest -k "add or subtract"  # Test names containing "add" or "subtract"
pytest -k "not slow"  # Exclude slow tests

# By marker
pytest -m unit  # Only unit tests
pytest -m "not integration"  # Exclude integration tests

# Stop on first failure
pytest -x

# Run N failures before stopping
pytest --maxfail=3

# Verbose output
pytest -v

# Show local variables on failure
pytest -l

# Parallel execution (pytest-xdist)
pytest -n auto  # Auto-detect CPU count
pytest -n 4     # Use 4 processes
```

---

## Assertions

### Plain assert Statements

pytest uses plain Python `assert` with intelligent introspection:

```python
def test_assertions():
    # Equality
    assert 2 + 2 == 4
    assert "hello" == "hello"

    # Inequality
    assert 5 != 10

    # Comparison
    assert 10 > 5
    assert 3 < 7

    # Membership
    assert "a" in ["a", "b", "c"]
    assert "x" not in {"y", "z"}

    # Boolean
    assert True
    assert not False

    # None
    value = None
    assert value is None

    # Exceptions (use pytest.raises)
    with pytest.raises(ValueError):
        int("not a number")
```

### Assertion Introspection

pytest shows detailed information on assertion failures:

```python
def test_list_comparison():
    expected = [1, 2, 3, 4]
    actual = [1, 2, 9, 4]

    assert actual == expected

# Output shows exact difference:
# AssertionError: assert [1, 2, 9, 4] == [1, 2, 3, 4]
#   At index 2 diff: 9 != 3
```

### pytest.approx for Floating Point

```python
def test_floating_point():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert math.sqrt(2) == pytest.approx(1.414, abs=0.001)
```

---

## Fixtures

### Basic Fixtures

```python
# conftest.py or test file
import pytest

@pytest.fixture
def user_data():
    """Provide test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com"
    }

def test_user_creation(user_data):
    """Fixtures are injected by name."""
    assert user_data["username"] == "testuser"
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: per test
def function_fixture():
    return "fresh every test"

@pytest.fixture(scope="class")  # Per test class
def class_fixture():
    return "shared across class"

@pytest.fixture(scope="module")  # Per module
def module_fixture():
    return "shared across module"

@pytest.fixture(scope="session")  # Once per test session
def session_fixture():
    return "shared across entire session"
```

### Fixture Setup/Teardown

```python
@pytest.fixture
def database_connection():
    """Setup and teardown with yield."""
    # Setup
    db = Database.connect("test.db")
    db.create_tables()

    yield db  # Test runs here

    # Teardown
    db.drop_tables()
    db.close()

def test_query(database_connection):
    result = database_connection.query("SELECT 1")
    assert result is not None
```

### Fixture Composition

```python
@pytest.fixture
def database():
    return Database()

@pytest.fixture
def user_repository(database):
    """Fixture depending on another fixture."""
    return UserRepository(database)

def test_save_user(user_repository):
    """pytest resolves dependencies automatically."""
    user_repository.save({"name": "John"})
```

### Factory Fixtures

```python
@pytest.fixture
def make_user():
    """Factory fixture for creating multiple users."""
    def _make_user(name, email=None):
        return User(name=name, email=email or f"{name}@example.com")
    return _make_user

def test_multiple_users(make_user):
    user1 = make_user("Alice")
    user2 = make_user("Bob")
    assert user1.name != user2.name
```

### Built-in Fixtures

```python
def test_tmp_path(tmp_path):
    """Temporary directory (unique per test)."""
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

def test_capsys(capsys):
    """Capture stdout/stderr."""
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

def test_monkeypatch(monkeypatch):
    """Modify objects/environment variables."""
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setattr("app.config.DEBUG", True)
```

---

## Parametrize

### Basic Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    """One test function → 3 test cases."""
    assert input ** 2 == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (5, 10, 15),
    (0, 0, 0),
])
def test_addition(x, y, expected):
    assert x + y == expected
```

### Parametrize with IDs

```python
@pytest.mark.parametrize("input,expected", [
    pytest.param(2, 4, id="two_squared"),
    pytest.param(3, 9, id="three_squared"),
    pytest.param(4, 16, id="four_squared"),
])
def test_square_with_ids(input, expected):
    assert input ** 2 == expected

# Output:
# test_square_with_ids[two_squared] PASSED
# test_square_with_ids[three_squared] PASSED
```

### Cartesian Product

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_multiply(x, y):
    """4 test cases: (1,3), (1,4), (2,3), (2,4)."""
    assert x * y > 0
```

---

## Marks

### Built-in Marks

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_issue():
    pass

@pytest.mark.slow
def test_long_running():
    time.sleep(10)
```

### Custom Marks

```ini
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests (>1s)
```

```python
@pytest.mark.unit
def test_calculator_add():
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_database_query():
    pass

# Run specific marks
# pytest -m unit
# pytest -m "unit and not slow"
```

---

## Plugins

### pytest-cov (Coverage)

```bash
pip install pytest-cov
pytest --cov=app --cov-report=term-missing --cov-report=html tests/
```

### pytest-mock (Mocking)

```bash
pip install pytest-mock

def test_with_mocker(mocker):
    mock = mocker.patch('app.external_api.call')
    mock.return_value = {"status": "ok"}
```

### pytest-asyncio (Async Testing)

```bash
pip install pytest-asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### pytest-xdist (Parallel Testing)

```bash
pip install pytest-xdist
pytest -n auto  # Use all CPU cores
```

### pytest-timeout

```bash
pip install pytest-timeout

@pytest.mark.timeout(5)  # 5 second timeout
def test_fast_function():
    pass
```

---

## conftest.py

### Purpose

- Define fixtures shared across multiple test files
- One per directory, hierarchical
- Automatically discovered by pytest

### Example Structure

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def app_config():
    """Load app configuration once."""
    return load_config("test")

@pytest.fixture
def database(app_config):
    """Database connection per test."""
    db = Database(app_config.db_url)
    db.create_tables()
    yield db
    db.drop_tables()
    db.close()

@pytest.fixture
def client(database):
    """Test client with database."""
    from app import create_app
    app = create_app(database=database)
    return app.test_client()

# Hooks
def pytest_collection_modifyitems(items):
    """Automatically mark slow tests."""
    for item in items:
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
```

---

## Advanced Patterns

### Parameterized Fixtures

```python
@pytest.fixture(params=["postgres", "test"])
def database(request):
    """Test runs with different database configs (production vs test)."""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.close()

def test_query(database):
    """Runs for each database configuration."""
    result = database.query("SELECT 1")
    assert result is not None
```

### Fixture Finalization

```python
@pytest.fixture
def resource(request):
    res = acquire_resource()

    def cleanup():
        release_resource(res)

    request.addfinalizer(cleanup)
    return res
```

### Conditional Skip

```python
@pytest.mark.skipif(not HAS_REDIS, reason="Redis not available")
def test_redis_cache():
    pass
```

---

## Best Practices

### Test Organization

```python
# Good: Descriptive test names
def test_user_registration_sends_welcome_email():
    pass

# Bad: Vague names
def test_user():
    pass

# Good: AAA pattern
def test_calculate_total():
    # Arrange
    cart = ShoppingCart()
    cart.add_item(price=10.00, quantity=2)

    # Act
    total = cart.get_total()

    # Assert
    assert total == 20.00
```

### Fixture Best Practices

```python
# Good: Appropriate scope
@pytest.fixture(scope="module")  # Expensive resource
def database_connection():
    pass

# Bad: Too wide scope (state pollution)
@pytest.fixture(scope="session")
def mutable_state():
    return []  # Shared across ALL tests!
```

### Assertion Messages

```python
# Good: Clear failure message
assert user.is_active, f"User {user.id} should be active"

# pytest shows: AssertionError: User 123 should be active
```

---

## Common Patterns

### Testing Exceptions

```python
def test_invalid_input_raises():
    with pytest.raises(ValueError) as exc_info:
        parse_age("not a number")

    assert "invalid" in str(exc_info.value).lower()
```

### Testing Warnings

```python
def test_deprecation_warning():
    with pytest.warns(DeprecationWarning):
        old_function()
```

### Multiple Assertions

```python
def test_user_data():
    user = create_user("john@example.com")

    # All assertions checked (doesn't stop on first)
    assert user.email == "john@example.com"
    assert user.is_active is True
    assert user.created_at is not None
```

---

## Debugging

### Print Debugging

```bash
pytest -s  # Show print statements
pytest -s -v  # Verbose + print
```

### PDB Debugging

```bash
pytest --pdb  # Drop to debugger on failure
pytest --trace  # Drop to debugger at start of each test
```

### Local Variables

```bash
pytest -l  # Show local variables on failure
pytest -l -vv  # Very verbose + locals
```

---

## CI Integration

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
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=app --cov-fail-under=80 tests/
```

---

Related: [unittest-guide.md](unittest-guide.md) | [mocking-reference.md](mocking-reference.md) | [coverage-guide.md](coverage-guide.md) | [Return to INDEX](INDEX.md)
