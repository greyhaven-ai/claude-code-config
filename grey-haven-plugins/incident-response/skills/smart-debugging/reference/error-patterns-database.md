# Error Patterns Database

Comprehensive catalog of common error patterns with fixes and prevention strategies.

## Null Pointer / None Type Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **NoneType Attribute** | `'NoneType' object has no attribute 'x'` | Accessing property on None | Add null check: `if obj is None: return` | Use Optional[] types, validation |
| **Undefined Variable** | `undefined is not defined` (JS) | Using variable before assignment | Initialize variable | Use `let`/`const`, enable strict mode |
| **Null Dereference** | `Cannot read property 'x' of null` | Object is null/undefined | Optional chaining: `obj?.property` | Use TypeScript strict null checks |

### Fix Template

```python
# Before
user.name  # May be None

# After
if user is None:
    return "Unknown"
return user.name

# Or use get() with default
getattr(user, 'name', 'Unknown')
```

## Type Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **Operand Type Mismatch** | `unsupported operand type(s) for +: 'int' and 'str'` | Wrong types in operation | Type conversion or fix type hint | mypy, Pydantic validation |
| **Wrong Argument Type** | `expected str, got int` | Passing wrong type | Convert type or fix signature | Static type checking |
| **JSON Serialization** | `Object of type datetime is not JSON serializable` | Can't serialize type | Custom JSON encoder | Use Pydantic models |

### Fix Template

```python
# Type validation with Pydantic
from pydantic import BaseModel

class UserInput(BaseModel):
    age: int  # Automatic validation and conversion

# Input: {"age": "25"} → converts to int(25)
# Input: {"age": "abc"} → ValidationError
```

## Index / Key Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **List Index Out of Range** | `list index out of range` | Accessing beyond list length | Check length first | Use `.get()` or try/except |
| **Dict KeyError** | `KeyError: 'missing_key'` | Key doesn't exist in dict | Use `.get()` with default | Pydantic models, TypedDict |
| **Array Out of Bounds** | `undefined` (JS array) | Accessing invalid index | Check array length | Use `?.[]` optional chaining |

### Fix Template

```python
# Bad
user_dict['email']  # KeyError if 'email' missing

# Good
user_dict.get('email', 'no-email@example.com')

# Best (with Pydantic)
class User(BaseModel):
    email: EmailStr  # Required, validated
```

## Import / Module Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **Module Not Found** | `ModuleNotFoundError: No module named 'x'` | Missing dependency | Install: `pip install x` | Add to requirements.txt |
| **Circular Import** | `ImportError: cannot import name 'X' from partially initialized module` | A imports B, B imports A | Refactor to remove cycle | Dependency injection |
| **Relative Import** | `attempted relative import with no known parent package` | Incorrect relative import | Use absolute imports | Configure PYTHONPATH |

### Fix Template

```bash
# Check installed packages
pip list | grep package_name

# Install missing package
pip install package_name

# Add to requirements
echo "package_name==1.2.3" >> requirements.txt
```

## Database Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **Connection Refused** | `Connection refused` | DB not running or wrong host | Check connection string | Health checks, retry logic |
| **Timeout** | `timeout exceeded` | Query too slow or DB overloaded | Optimize query, add indexes | Query analysis, connection pooling |
| **Unique Constraint** | `UNIQUE constraint failed` | Duplicate key | Handle conflict (upsert) | Pre-check existence |
| **Foreign Key Violation** | `FOREIGN KEY constraint failed` | Referenced record doesn't exist | Validate FK exists first | Use transactions |

### Fix Template

```python
# Handle constraint violations
from sqlalchemy.exc import IntegrityError

try:
    db.add(user)
    db.commit()
except IntegrityError as e:
    db.rollback()
    if 'UNIQUE constraint' in str(e):
        raise DuplicateUserError()
    raise
```

## API / HTTP Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **400 Bad Request** | Malformed request | Invalid JSON or missing fields | Validate request schema | Pydantic, OpenAPI validation |
| **401 Unauthorized** | Missing/invalid auth token | Token expired or missing | Refresh token logic | Token rotation, validation |
| **404 Not Found** | Resource doesn't exist | Wrong ID or deleted resource | Return 404 with helpful message | Check existence first |
| **422 Unprocessable** | Validation failed | Data doesn't meet constraints | Fix validation or API call | Schema validation |
| **500 Internal Error** | Server-side error | Unhandled exception | Fix server code, add logging | Error handling, monitoring |

### Fix Template

```python
# Proper error handling
from fastapi import HTTPException

@app.post("/users")
async def create_user(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(
            status_code=409,  # Conflict
            detail="User with this email already exists"
        )
    return await db.users.insert_one(user)
```

## Concurrency / Race Condition Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **Race Condition** | Inconsistent results, data corruption | Multiple threads accessing shared state | Use locks, atomic operations | Immutable data, message queues |
| **Deadlock** | System hangs | Circular wait for resources | Order lock acquisition consistently | Avoid nested locks |
| **Lost Update** | Changes overwritten | Concurrent updates | Optimistic locking (version field) | Transactions, SELECT FOR UPDATE |

### Fix Template

```python
# Use distributed lock (Redis)
import redis_lock

with redis_lock.Lock(redis_client, "order:123"):
    order = db.orders.get(123)
    order.status = "processed"
    db.orders.save(order)
```

## Memory / Performance Errors

| Pattern | Indicators | Root Cause | Fix | Prevention |
|---------|-----------|------------|-----|------------|
| **Out of Memory** | `MemoryError` | Loading too much data | Stream/paginate data | Lazy loading, generators |
| **N+1 Query Problem** | Slow performance | Loop with query inside | Use JOIN or eager loading | Query analysis, APM tools |
| **Memory Leak** | Memory grows over time | Objects not garbage collected | Fix circular references | Profiling, weak references |

### Fix Template

```python
# Bad: N+1 queries
for user in users:  # 1 query
    posts = db.posts.find(user_id=user.id)  # N queries

# Good: Single query with join
users_with_posts = db.execute("""
    SELECT users.*, json_agg(posts.*) as posts
    FROM users
    LEFT JOIN posts ON posts.user_id = users.id
    GROUP BY users.id
""")
```

## Quick Reference: Error → Pattern

| Error Message | Pattern | Fix Priority |
|---------------|---------|--------------|
| `'NoneType' object has no attribute` | null_pointer | High |
| `unsupported operand type` | type_mismatch | Medium |
| `list index out of range` | index_error | Medium |
| `KeyError` | key_error | Medium |
| `ModuleNotFoundError` | import_error | High |
| `Connection refused` | db_connection | High |
| `UNIQUE constraint failed` | db_constraint | Medium |
| `401 Unauthorized` | api_auth | High |
| `MemoryError` | memory_error | Critical |

---

**Usage**: When debugging, match error message to pattern, apply fix template, implement prevention strategy.
