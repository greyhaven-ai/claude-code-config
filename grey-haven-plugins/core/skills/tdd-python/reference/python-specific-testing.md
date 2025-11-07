# Python-Specific Testing

Complete guide to testing Python-specific features - decorators, generators, context managers, async/await, type hints, and more.

**Python Version**: 3.8+
**Frameworks**: pytest, unittest
**Coverage**: Decorators, generators, context managers, async, metaclasses, descriptors

---

## Testing Decorators

### Function Decorators

```python
# Implementation
def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
        return wrapper
    return decorator

# Test
def test_retry_decorator_succeeds_first_attempt():
    call_count = 0

    @retry(max_attempts=3)
    def flaky_function():
        nonlocal call_count
        call_count += 1
        return "success"

    result = flaky_function()

    assert result == "success"
    assert call_count == 1

def test_retry_decorator_retries_on_failure():
    call_count = 0

    @retry(max_attempts=3)
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise ValueError("error")

    with pytest.raises(ValueError):
        always_fails()

    assert call_count == 3  # Retried 3 times
```

### Class Decorators

```python
# Implementation
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

# Test
def test_singleton_returns_same_instance():
    @singleton
    class Config:
        def __init__(self):
            self.value = "config"

    instance1 = Config()
    instance2 = Config()

    assert instance1 is instance2
```

### Method Decorators

```python
# Implementation
def cache(func):
    cached = {}
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    return wrapper

class Calculator:
    @cache
    def expensive_calculation(self, n):
        return n ** 2

# Test
def test_cache_decorator_caches_results():
    calc = Calculator()

    result1 = calc.expensive_calculation(5)
    result2 = calc.expensive_calculation(5)

    assert result1 == 25
    assert result2 == 25
    # Second call should be cached (test by mocking)
```

---

## Testing Generators

### Basic Generators

```python
# Implementation
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Test
def test_fibonacci_generates_correct_sequence():
    result = list(fibonacci(7))
    assert result == [0, 1, 1, 2, 3, 5, 8]

def test_fibonacci_is_lazy():
    gen = fibonacci(1000000)
    # Generator created but not executed
    assert next(gen) == 0
    assert next(gen) == 1
```

### Generator Exceptions

```python
# Implementation
def validated_input(values):
    for value in values:
        if value < 0:
            raise ValueError(f"Negative value: {value}")
        yield value

# Test
def test_generator_raises_on_invalid_input():
    gen = validated_input([1, 2, -1, 3])

    assert next(gen) == 1
    assert next(gen) == 2

    with pytest.raises(ValueError, match="Negative value: -1"):
        next(gen)
```

### Generator Send/Close

```python
# Implementation
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

# Test
def test_generator_send():
    gen = accumulator()
    next(gen)  # Prime generator

    assert gen.send(5) == 5
    assert gen.send(10) == 15
    assert gen.send(3) == 18

    gen.close()

def test_generator_close_raises_stopiteration():
    gen = accumulator()
    next(gen)
    gen.close()

    with pytest.raises(StopIteration):
        next(gen)
```

---

## Testing Context Managers

### Basic Context Managers

```python
# Implementation
class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions

# Test
def test_context_manager_opens_and_closes_file(tmp_path):
    filepath = tmp_path / "test.txt"

    with FileHandler(str(filepath)) as f:
        f.write("content")

    # Verify file closed
    assert filepath.read_text() == "content"

def test_context_manager_closes_on_exception(tmp_path):
    filepath = tmp_path / "test.txt"

    with pytest.raises(ValueError):
        with FileHandler(str(filepath)) as f:
            f.write("content")
            raise ValueError("error")

    # Verify file still closed
    assert filepath.exists()
```

### contextlib Context Managers

```python
from contextlib import contextmanager

# Implementation
@contextmanager
def temporary_setting(setting, value):
    old_value = get_setting(setting)
    set_setting(setting, value)
    try:
        yield old_value
    finally:
        set_setting(setting, old_value)

# Test
def test_temporary_setting_restores_original():
    set_setting("debug", False)

    with temporary_setting("debug", True):
        assert get_setting("debug") is True

    assert get_setting("debug") is False

def test_temporary_setting_restores_on_exception():
    set_setting("debug", False)

    with pytest.raises(ValueError):
        with temporary_setting("debug", True):
            raise ValueError("error")

    assert get_setting("debug") is False
```

---

## Testing Async Code

### Async Functions

```python
# Implementation
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Test with pytest-asyncio
@pytest.mark.asyncio
async def test_fetch_data_returns_json():
    with aioresponses() as mocked:
        mocked.get(
            "https://api.example.com/data",
            payload={"result": "success"}
        )

        data = await fetch_data("https://api.example.com/data")

        assert data["result"] == "success"
```

### Async Context Managers

```python
# Implementation
class AsyncDatabaseConnection:
    async def __aenter__(self):
        self.conn = await connect_database()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()
        return False

# Test
@pytest.mark.asyncio
async def test_async_context_manager():
    async with AsyncDatabaseConnection() as conn:
        result = await conn.query("SELECT 1")
        assert result == [(1,)]

    # Connection closed after context
```

### Async Generators

```python
# Implementation
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0)  # Yield control
        yield i

# Test
@pytest.mark.asyncio
async def test_async_generator():
    result = []
    async for value in async_range(5):
        result.append(value)

    assert result == [0, 1, 2, 3, 4]
```

### Testing Asyncio Tasks

```python
# Implementation
async def process_items(items):
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# Test
@pytest.mark.asyncio
async def test_process_items_concurrently():
    items = ["a", "b", "c"]

    with patch("module.process_item") as mock_process:
        mock_process.return_value = asyncio.coroutine(lambda: "result")()

        results = await process_items(items)

        assert len(results) == 3
        assert mock_process.call_count == 3
```

---

## Testing Properties

### Property Getters/Setters

```python
# Implementation
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

# Test
def test_temperature_property_getter():
    temp = Temperature(25)
    assert temp.celsius == 25
    assert temp.fahrenheit == 77

def test_temperature_property_setter():
    temp = Temperature(0)
    temp.celsius = 100
    assert temp.celsius == 100

def test_temperature_setter_validation():
    temp = Temperature(0)
    with pytest.raises(ValueError, match="Below absolute zero"):
        temp.celsius = -300
```

---

## Testing Descriptors

```python
# Implementation
class ValidatedString:
    def __init__(self, min_length=0):
        self.min_length = min_length

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, "")

    def __set__(self, obj, value):
        if len(value) < self.min_length:
            raise ValueError(f"{self.name} too short")
        setattr(obj, self.name, value)

class User:
    username = ValidatedString(min_length=3)

# Test
def test_descriptor_validation():
    user = User()

    with pytest.raises(ValueError):
        user.username = "ab"  # Too short

    user.username = "alice"
    assert user.username == "alice"
```

---

## Testing Metaclasses

```python
# Implementation
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.connected = True

# Test
def test_metaclass_singleton():
    conn1 = DatabaseConnection()
    conn2 = DatabaseConnection()

    assert conn1 is conn2

def test_metaclass_singleton_different_classes():
    class CacheConnection(metaclass=SingletonMeta):
        pass

    cache1 = CacheConnection()
    cache2 = CacheConnection()
    db = DatabaseConnection()

    assert cache1 is cache2
    assert cache1 is not db
```

---

## Testing Type Hints

### Runtime Type Checking

```python
from typing import List, Dict, Optional

# Implementation
def process_users(users: List[Dict[str, str]]) -> int:
    return len(users)

# Test
def test_type_hints_with_valid_types():
    users = [{"name": "Alice"}, {"name": "Bob"}]
    result = process_users(users)
    assert result == 2

# Type checking with mypy
def test_type_checking():
    # Run: mypy module.py
    # Catches type errors at static analysis time
    pass
```

### Type Guards

```python
from typing import Union

# Implementation
def is_string_list(val: Union[List[str], List[int]]) -> bool:
    return isinstance(val, list) and all(isinstance(x, str) for x in val)

def process(val: Union[List[str], List[int]]) -> str:
    if is_string_list(val):
        return ",".join(val)  # Type narrowed to List[str]
    return ",".join(str(x) for x in val)

# Test
def test_type_guard_with_strings():
    result = process(["a", "b", "c"])
    assert result == "a,b,c"

def test_type_guard_with_integers():
    result = process([1, 2, 3])
    assert result == "1,2,3"
```

---

## Testing Dataclasses

```python
from dataclasses import dataclass, field
from typing import List

# Implementation
@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")

# Test
def test_dataclass_creation():
    product = Product(name="Widget", price=9.99)
    assert product.name == "Widget"
    assert product.price == 9.99
    assert product.tags == []

def test_dataclass_validation():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product(name="Widget", price=-5)

def test_dataclass_equality():
    p1 = Product(name="Widget", price=9.99)
    p2 = Product(name="Widget", price=9.99)
    assert p1 == p2
```

---

## Testing Enums

```python
from enum import Enum, auto

# Implementation
class Status(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

def can_transition(from_status: Status, to_status: Status) -> bool:
    valid_transitions = {
        Status.PENDING: [Status.PROCESSING, Status.FAILED],
        Status.PROCESSING: [Status.COMPLETED, Status.FAILED],
        Status.COMPLETED: [],
        Status.FAILED: []
    }
    return to_status in valid_transitions[from_status]

# Test
def test_enum_valid_transition():
    assert can_transition(Status.PENDING, Status.PROCESSING)
    assert can_transition(Status.PROCESSING, Status.COMPLETED)

def test_enum_invalid_transition():
    assert not can_transition(Status.COMPLETED, Status.PENDING)
    assert not can_transition(Status.PENDING, Status.COMPLETED)

def test_enum_values():
    assert Status.PENDING.name == "PENDING"
    assert len(Status) == 4
```

---

## Testing Exception Hierarchies

```python
# Implementation
class APIError(Exception):
    """Base exception for API errors."""
    pass

class AuthenticationError(APIError):
    """Authentication failed."""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded."""
    pass

def make_request(api_key: str):
    if not api_key:
        raise AuthenticationError("API key required")
    if len(api_key) < 10:
        raise RateLimitError("Rate limit exceeded")
    return {"status": "success"}

# Test
def test_exception_hierarchy_authentication():
    with pytest.raises(AuthenticationError):
        make_request("")

    with pytest.raises(APIError):  # Catches subclasses
        make_request("")

def test_exception_hierarchy_rate_limit():
    with pytest.raises(RateLimitError):
        make_request("short")

def test_exception_hierarchy_success():
    result = make_request("valid_api_key")
    assert result["status"] == "success"
```

---

## Testing Magic Methods

### Comparison Methods

```python
# Implementation
@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < \
               (other.major, other.minor, other.patch)

# Test
def test_version_comparison():
    v1 = Version(1, 2, 3)
    v2 = Version(1, 2, 4)
    v3 = Version(2, 0, 0)

    assert v1 < v2
    assert v2 < v3
    assert not v3 < v1
```

### Container Methods

```python
# Implementation
class Inventory:
    def __init__(self):
        self.items = {}

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __contains__(self, key):
        return key in self.items

    def __len__(self):
        return len(self.items)

# Test
def test_inventory_container_protocol():
    inv = Inventory()

    inv["apple"] = 5
    assert inv["apple"] == 5

    assert "apple" in inv
    assert "banana" not in inv

    assert len(inv) == 1
```

---

## Testing Class Methods and Static Methods

```python
# Implementation
class DateUtil:
    @staticmethod
    def is_weekend(date):
        return date.weekday() in (5, 6)

    @classmethod
    def from_string(cls, date_string):
        from datetime import datetime
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return cls(date)

# Test
def test_static_method():
    from datetime import datetime

    saturday = datetime(2024, 1, 6)  # Saturday
    monday = datetime(2024, 1, 8)    # Monday

    assert DateUtil.is_weekend(saturday)
    assert not DateUtil.is_weekend(monday)

def test_class_method():
    util = DateUtil.from_string("2024-01-15")
    assert isinstance(util, DateUtil)
```

---

## Testing Abstract Base Classes

```python
from abc import ABC, abstractmethod

# Implementation
class Animal(ABC):
    @abstractmethod
    def make_sound(self) -> str:
        pass

class Dog(Animal):
    def make_sound(self) -> str:
        return "Woof!"

# Test
def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        Animal()

def test_concrete_class_implements_abstract_method():
    dog = Dog()
    assert dog.make_sound() == "Woof!"
```

---

## Best Practices

### ✅ DO

```python
# Test actual Python behavior
def test_generator_is_lazy():
    def infinite():
        while True:
            yield 1

    gen = infinite()  # Should not hang
    assert next(gen) == 1

# Test edge cases
@pytest.mark.asyncio
async def test_async_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=0.1)

# Test cleanup
def test_context_manager_cleanup_on_error():
    with pytest.raises(ValueError):
        with resource_manager():
            raise ValueError()
    # Verify cleanup happened
```

### ❌ DON'T

```python
# Don't test Python itself
def test_list_append():  # ❌ Testing stdlib
    lst = []
    lst.append(1)
    assert lst == [1]

# Don't ignore async properly
def test_async_wrong():  # ❌ Missing @pytest.mark.asyncio
    result = await async_function()

# Don't forget generator exhaustion
def test_generator_wrong():
    gen = fibonacci(5)
    list(gen)  # Exhausted
    list(gen)  # ❌ Empty now
```

---

## Quick Reference

### Decorators
```python
# Test decorated function behavior
@decorator
def func(): pass

# Test decorator itself
wrapped = decorator(func)
```

### Generators
```python
list(generator())          # Exhaust
next(gen)                  # Single value
gen.send(value)            # Send to generator
gen.close()                # Close generator
```

### Context Managers
```python
with manager as m:         # Test __enter__/__exit__
    pass

@contextmanager            # Using contextlib
def manager():
    try:
        yield
    finally:
        cleanup()
```

### Async
```python
@pytest.mark.asyncio       # Mark async test
async def test():
    await func()

AsyncMock()                # Mock async function
aioresponses()             # Mock aiohttp
```

---

Related: [pytest-guide.md](pytest-guide.md) | [unittest-guide.md](unittest-guide.md) | [mocking-reference.md](mocking-reference.md) | [Return to INDEX](INDEX.md)
