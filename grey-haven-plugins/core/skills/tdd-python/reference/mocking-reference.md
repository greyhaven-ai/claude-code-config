# Mocking Reference

Complete reference for Python mocking - unittest.mock, pytest-mock, patching strategies, assertion methods, and best practices.

**Modules**: unittest.mock (Python 3.3+), pytest-mock (pytest plugin)
**Use Cases**: Isolate units, test external dependencies, control non-deterministic behavior

---

## unittest.mock Module

### Mock Objects

```python
from unittest.mock import Mock

# Create basic mock
mock = Mock()

# Set return value
mock.return_value = "result"
result = mock()  # Returns "result"

# Set side effect (exception)
mock.side_effect = ValueError("error")
mock()  # Raises ValueError

# Set side effect (sequence of returns)
mock.side_effect = [1, 2, 3]
mock()  # Returns 1
mock()  # Returns 2
mock()  # Returns 3

# Set side effect (callable)
def dynamic_response(x):
    return x * 2
mock.side_effect = dynamic_response
mock(5)  # Returns 10
```

### Mock Attributes

```python
mock = Mock()

# Auto-generate attributes
mock.method.return_value = "value"
mock.attribute = "attr"

# Mock nested attributes
mock.database.query.return_value = {"data": []}
result = mock.database.query("SELECT * FROM users")

# Configure mock at creation
mock = Mock(
    return_value="result",
    side_effect=None,
    name="my_mock"
)
```

### MagicMock

```python
from unittest.mock import MagicMock

# Auto-implements magic methods
mock = MagicMock()

# Supports iteration
mock.__iter__.return_value = iter([1, 2, 3])
for item in mock:
    print(item)  # Prints 1, 2, 3

# Supports context manager
mock.__enter__.return_value = "context"
with mock as ctx:
    print(ctx)  # Prints "context"

# Supports len()
mock.__len__.return_value = 5
len(mock)  # Returns 5
```

### AsyncMock

```python
from unittest.mock import AsyncMock
import asyncio

# Mock async function
mock_async = AsyncMock(return_value="result")

async def test_async():
    result = await mock_async()
    assert result == "result"

asyncio.run(test_async())

# Mock async context manager
mock_async = AsyncMock()
mock_async.__aenter__.return_value = "context"

async def test_context():
    async with mock_async as ctx:
        assert ctx == "context"
```

---

## Mock Assertions

### Call Verification

```python
mock = Mock()

# Basic call assertions
mock()
mock.assert_called()  # Passes

mock.assert_called_once()  # Passes
mock()
mock.assert_called_once()  # Fails - called twice

# Assert with arguments
mock.method(1, 2, key="value")
mock.method.assert_called_with(1, 2, key="value")
mock.method.assert_called_once_with(1, 2, key="value")

# Assert not called
mock.other_method.assert_not_called()
```

### Call Count

```python
mock = Mock()

mock()
mock()
mock()

assert mock.call_count == 3

# Check specific method
mock.method()
assert mock.method.call_count == 1
```

### Call Arguments

```python
mock = Mock()
mock(1, 2, key="value")

# Get last call arguments
args, kwargs = mock.call_args
assert args == (1, 2)
assert kwargs == {"key": "value"}

# Get all calls
mock(3, 4)
mock(5, 6)
all_calls = mock.call_args_list
assert len(all_calls) == 3
```

### Call Objects

```python
from unittest.mock import call

mock = Mock()
mock(1, 2)
mock(3, 4, key="value")

# Assert any call
mock.assert_any_call(1, 2)
mock.assert_any_call(3, 4, key="value")

# Assert has calls (ordered)
mock.assert_has_calls([
    call(1, 2),
    call(3, 4, key="value")
])

# Assert has calls (unordered)
mock.assert_has_calls([
    call(3, 4, key="value"),
    call(1, 2)
], any_order=True)
```

---

## Patching

### Patch Decorator

```python
from unittest.mock import patch

# Patch function
@patch('module.function')
def test_something(mock_function):
    mock_function.return_value = "mocked"

    result = module.function()

    assert result == "mocked"
    mock_function.assert_called_once()

# Patch class
@patch('module.ClassName')
def test_with_class(MockClass):
    mock_instance = Mock()
    MockClass.return_value = mock_instance

    obj = module.ClassName()
    obj.method()

    MockClass.assert_called_once()
    mock_instance.method.assert_called_once()
```

### Multiple Patches

```python
# Stacked decorators (bottom-up parameter order)
@patch('module.function_a')
@patch('module.function_b')
def test_multiple(mock_b, mock_a):
    mock_a.return_value = "a"
    mock_b.return_value = "b"

    # Test code

# Single decorator with multiple targets
@patch.multiple('module',
    function_a=Mock(return_value="a"),
    function_b=Mock(return_value="b")
)
def test_multiple():
    # function_a and function_b are now mocked
    pass
```

### Context Manager Patch

```python
def test_with_context():
    with patch('module.function') as mock_function:
        mock_function.return_value = "mocked"

        result = module.function()

        assert result == "mocked"

    # Outside context: real function used
```

### Patch Object

```python
from unittest.mock import patch

class MyClass:
    def method(self):
        return "real"

# Patch instance method
obj = MyClass()
with patch.object(obj, 'method', return_value="mocked"):
    result = obj.method()
    assert result == "mocked"

# Patch class method
with patch.object(MyClass, 'method', return_value="mocked"):
    obj = MyClass()
    result = obj.method()
    assert result == "mocked"
```

### Patch Dictionary

```python
from unittest.mock import patch

# Patch dictionary
config = {"api_key": "real_key"}

with patch.dict(config, {"api_key": "test_key"}):
    assert config["api_key"] == "test_key"

# Outside context: original value restored
assert config["api_key"] == "real_key"

# Patch environment variables
import os

with patch.dict(os.environ, {"API_URL": "http://test.example.com"}):
    assert os.environ["API_URL"] == "http://test.example.com"
```

---

## pytest-mock Plugin

### mocker Fixture

```python
# Install: pip install pytest-mock

def test_with_mocker(mocker):
    # Create mock
    mock = mocker.Mock()
    mock.return_value = "result"

    result = mock()
    assert result == "result"

# Patch with mocker
def test_patch(mocker):
    mock_function = mocker.patch('module.function')
    mock_function.return_value = "mocked"

    result = module.function()
    assert result == "mocked"
```

### Advantages of mocker

```python
# Auto-cleanup (no manual stop needed)
def test_auto_cleanup(mocker):
    mocker.patch('module.function')
    # Automatically cleaned up after test

# Spy (wrap real object)
def test_spy(mocker):
    spy = mocker.spy(module, 'function')

    result = module.function(1, 2)

    # Real function called
    # But spy tracks calls
    spy.assert_called_once_with(1, 2)
```

### mocker Methods

```python
def test_mocker_methods(mocker):
    # Create mocks
    mock = mocker.Mock()
    magic_mock = mocker.MagicMock()
    async_mock = mocker.AsyncMock()

    # Patching
    mocker.patch('module.function')
    mocker.patch.object(obj, 'method')
    mocker.patch.dict(dictionary, {'key': 'value'})
    mocker.patch.multiple('module', func_a=mocker.Mock())

    # Spy
    spy = mocker.spy(module, 'function')

    # Stop all patches (manual cleanup)
    mocker.stopall()
```

---

## Patching Strategies

### Where to Patch

```python
# app/service.py
from app.database import Database

class Service:
    def __init__(self):
        self.db = Database()

# ❌ WRONG: Patch at definition location
@patch('app.database.Database')  # Wrong!
def test_wrong(MockDatabase):
    service = Service()  # Still uses real Database

# ✅ CORRECT: Patch at import location
@patch('app.service.Database')  # Correct!
def test_correct(MockDatabase):
    service = Service()  # Uses mock
```

**Rule**: Patch where the object is imported/used, not where it's defined.

### Patch Return Value vs Side Effect

```python
# return_value: For simple returns
mock.return_value = "result"

# side_effect: For complex behavior
def dynamic_behavior(*args, **kwargs):
    if args[0] == "error":
        raise ValueError("error")
    return f"Result for {args[0]}"

mock.side_effect = dynamic_behavior
```

### Partial Mocking

```python
from unittest.mock import Mock

# Real class with some mocked methods
class RealClass:
    def real_method(self):
        return "real"

    def to_mock(self):
        return "original"

obj = RealClass()

# Mock only one method
with patch.object(obj, 'to_mock', return_value="mocked"):
    assert obj.to_mock() == "mocked"
    assert obj.real_method() == "real"  # Still real
```

---

## Advanced Patterns

### Mock Chaining

```python
mock = Mock()

# Chain attributes
mock.client.database.query.return_value = {"data": []}

result = mock.client.database.query("SELECT * FROM users")
assert result == {"data": []}
```

### Spec and Autospec

```python
from unittest.mock import create_autospec

class RealClass:
    def method(self, x: int) -> str:
        return str(x)

# spec: Mock has same attributes
mock = Mock(spec=RealClass)
mock.method()  # OK
mock.invalid_method()  # AttributeError

# autospec: Also checks signatures
mock = create_autospec(RealClass)
mock.method(5)  # OK
mock.method()  # TypeError: missing required argument
```

### PropertyMock

```python
from unittest.mock import PropertyMock, patch

class MyClass:
    @property
    def value(self):
        return "real"

# Mock property
obj = MyClass()
with patch.object(MyClass, 'value', new_callable=PropertyMock) as mock_prop:
    mock_prop.return_value = "mocked"
    assert obj.value == "mocked"
```

### Mock Context Managers

```python
# Mock context manager
mock_file = Mock()
mock_file.__enter__.return_value = mock_file
mock_file.read.return_value = "file contents"

with mock_file as f:
    contents = f.read()
    assert contents == "file contents"
```

### Mock Async Context Managers

```python
from unittest.mock import AsyncMock

async def test_async_context():
    mock_async = AsyncMock()
    mock_async.__aenter__.return_value = "context value"

    async with mock_async as ctx:
        assert ctx == "context value"
```

---

## Mock Verification Patterns

### Verify Call Order

```python
from unittest.mock import Mock, call

mock = Mock()

mock.method_a()
mock.method_b()
mock.method_c()

# Verify exact order
mock.assert_has_calls([
    call.method_a(),
    call.method_b(),
    call.method_c()
])
```

### Verify Partial Arguments

```python
from unittest.mock import ANY

mock = Mock()
mock.method(1, "value", extra="data")

# Use ANY for arguments you don't care about
mock.method.assert_called_with(1, ANY, extra=ANY)
```

### Reset Mock

```python
mock = Mock()

mock()
assert mock.called

# Reset
mock.reset_mock()
assert not mock.called
assert mock.call_count == 0
```

---

## Decision Matrix

| Scenario | Use | Reason |
|----------|-----|--------|
| **External API** | Mock | No real network calls |
| **Database** | Mock | Isolate from DB |
| **Filesystem** | Mock | No disk I/O |
| **Time/Random** | Mock | Deterministic tests |
| **Simple function** | Spy | Test real + verify |
| **Complex interface** | MagicMock | Auto-generate methods |
| **Async code** | AsyncMock | async/await support |
| **Multiple values** | side_effect list | Different per call |
| **Dynamic behavior** | side_effect callable | Logic-based returns |

---

## Anti-Patterns

### ❌ Over-Mocking

```python
# BAD: Too many mocks
def test_over_mocked():
    mock_a = Mock()
    mock_b = Mock()
    mock_c = Mock()
    mock_d = Mock()
    mock_e = Mock()
    # If you need this many mocks, it's not a unit test
```

**Fix**: Mock only external boundaries.

### ❌ Testing Implementation Details

```python
# BAD: Testing internal method calls
def test_implementation():
    service = Service(Mock())
    service.public_method()

    # Don't verify internal private methods!
    service._internal_method.assert_called()  # ❌
```

**Fix**: Test public interface only.

### ❌ Brittle Mocks

```python
# BAD: Positional arguments
mock.method.assert_called_with("arg1", "arg2", "arg3")

# GOOD: Keyword arguments (flexible)
mock.method.assert_called_with(
    user_id="arg1",
    action="arg2",
    timestamp="arg3"
)
```

### ❌ Patching at Wrong Location

```python
# BAD: Patch where defined
@patch('library.module.Function')  # ❌

# GOOD: Patch where imported
@patch('myapp.service.Function')  # ✅
```

---

## pytest-mock vs unittest.mock

| Feature | unittest.mock | pytest-mock |
|---------|---------------|-------------|
| **Import** | `from unittest.mock import Mock` | `mocker` fixture |
| **Cleanup** | Manual `stop()` | Automatic |
| **Syntax** | `@patch('module.func')` | `mocker.patch('module.func')` |
| **Spy** | Manual with `wraps` | `mocker.spy()` |
| **pytest integration** | Works | Native |

### When to Use Each

**unittest.mock**:
- Standard library (no dependencies)
- Works with unittest and pytest
- Corporate environments

**pytest-mock**:
- pytest-only projects
- Cleaner syntax
- Auto-cleanup
- Better spy support

---

## Common Patterns

### Mock Dependency Injection

```python
class Service:
    def __init__(self, client):
        self.client = client

# Test with mocked dependency
def test_service():
    mock_client = Mock()
    mock_client.fetch.return_value = {"data": []}

    service = Service(client=mock_client)
    result = service.process()

    mock_client.fetch.assert_called_once()
```

### Mock Configuration

```python
# Mock with configuration
mock = Mock(
    return_value="default",
    side_effect=None,
    name="readable_name",
    spec=RealClass,  # Has same attributes
    **{'method.return_value': 'value'}  # Configure nested
)
```

### Conditional Side Effects

```python
def conditional_response(arg):
    if arg == "error":
        raise ValueError("Invalid")
    elif arg == "empty":
        return []
    else:
        return [{"data": arg}]

mock.side_effect = conditional_response
```

---

## Best Practices

### ✅ DO

```python
# Clear mock setup
mock = Mock()
mock.method.return_value = "expected"

# Verify behavior, not implementation
result = function_that_calls_mock()
assert result == "expected_output"

# Use keyword arguments
mock.assert_called_with(user_id=123, action="login")

# Reset between tests (if needed)
def test_a():
    mock()
    mock.reset_mock()
```

### ❌ DON'T

```python
# Vague mocks
mock = Mock()  # ❌ What does this mock?

# Too many assertions
mock.method.assert_called()
mock.method.assert_called_once()
mock.method.assert_called_with(...)  # Redundant

# Mock everything
# Only mock external boundaries
```

---

## Quick Reference

### Create Mocks
```python
Mock()                    # Basic mock
MagicMock()              # Auto-magic methods
AsyncMock()              # Async functions
mocker.Mock()            # pytest-mock
create_autospec(Class)   # With signature
```

### Set Behavior
```python
mock.return_value = "result"
mock.side_effect = Exception("error")
mock.side_effect = [1, 2, 3]
mock.side_effect = lambda x: x * 2
```

### Verify Calls
```python
mock.assert_called()
mock.assert_called_once()
mock.assert_called_with(1, 2)
mock.assert_called_once_with(1, 2)
mock.assert_not_called()
mock.assert_any_call(1, 2)
```

### Patching
```python
@patch('module.function')        # Decorator
with patch('module.function'):   # Context
mocker.patch('module.function')  # pytest-mock
patch.object(obj, 'method')      # Object
patch.dict(dict, {'key': 'val'}) # Dictionary
```

---

Related: [pytest-guide.md](pytest-guide.md) | [unittest-guide.md](unittest-guide.md) | [coverage-guide.md](coverage-guide.md) | [Return to INDEX](INDEX.md)
