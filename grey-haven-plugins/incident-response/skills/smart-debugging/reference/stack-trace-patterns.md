# Stack Trace Patterns

Comprehensive guide to reading, analyzing, and extracting insights from stack traces across different languages and environments.

## Python Stack Traces

### Anatomy

```python
Traceback (most recent call last):
  File "/app/api/users.py", line 45, in get_user
    user = db.query(User).filter(User.id == user_id).one()
  File "/venv/lib/sqlalchemy/orm/query.py", line 2890, in one
    raise NoResultFound("No row was found")
sqlalchemy.orm.exc.NoResultFound: No row was found
```

**Reading Order**: Bottom-up (exception → root cause)

| Component | Description | Example |
|-----------|-------------|---------|
| **Exception Type** | The error class | `sqlalchemy.orm.exc.NoResultFound` |
| **Exception Message** | Error description | `"No row was found"` |
| **Root Frame** | Where error originated | `query.py:2890, in one` |
| **Call Stack** | Function call chain | `users.py:45 → query.py:2890` |

### Identifying the Root Cause

```python
# Stack trace from user code → library code
Traceback (most recent call last):
  File "/app/api/orders.py", line 23, in create_order     # ← Your code (start here!)
    payment = process_payment(order.total)
  File "/app/services/payment.py", line 67, in process_payment
    stripe.charge.create(amount=amount)
  File "/venv/lib/stripe/api.py", line 342, in create    # ← Library code (ignore)
    raise InvalidRequestError("Amount must be positive")
stripe.error.InvalidRequestError: Amount must be positive
```

**Analysis**:
1. Exception: `InvalidRequestError` - Amount validation failed
2. Root frame in your code: `payment.py:67` - Calling Stripe with invalid amount
3. Source of bad data: `orders.py:23` - Passing `order.total` (likely 0 or negative)

**Fix Location**: Check `order.total` validation in `orders.py:23`

### Filtering Noise

**Focus on**:
- Files in your project directory (`/app/*`)
- First occurrence of error in your code

**Ignore**:
- Virtual environment files (`/venv/*`, `site-packages/*`)
- Standard library (`/usr/lib/python3.*/`)
- Framework internals (unless debugging framework)

### Async Stack Traces

```python
Traceback (most recent call last):
  File "/app/api/users.py", line 23, in get_user_profile
    user = await fetch_user(user_id)
  File "/app/services/users.py", line 45, in fetch_user
    data = await http_client.get(f"/users/{user_id}")
  File "/venv/lib/httpx/_client.py", line 1234, in get
    raise ConnectTimeout()
httpx.ConnectTimeout: Connection timed out
```

**Key Indicators**:
- `await` in frame descriptions
- Async function names (`async def`)
- Coroutine references

**Analysis**: Trace async call chain: `get_user_profile` → `fetch_user` → `httpx.get` → timeout

## JavaScript/TypeScript Stack Traces

### Node.js Format

```javascript
Error: User not found
    at UserService.findById (/app/services/user.service.ts:42:11)
    at async getUserProfile (/app/api/users.controller.ts:23:18)
    at async /app/middleware/auth.ts:67:5
    at async handleRequest (/app/server/request-handler.ts:15:3)
```

**Reading Order**: Top-down (error → call chain)

| Component | Description | Example |
|-----------|-------------|---------|
| **Error Type** | Error class | `Error` |
| **Error Message** | Description | `"User not found"` |
| **Root Frame** | Where thrown | `user.service.ts:42:11` |
| **Call Stack** | Caller chain | `getUserProfile` → middleware → request handler |

### Browser Stack Traces

```javascript
Uncaught TypeError: Cannot read property 'name' of undefined
    at UserProfile.render (UserProfile.tsx:15:32)
    at finishClassComponent (react-dom.production.min.js:123:45)
    at updateClassComponent (react-dom.production.min.js:456:12)
```

**Analysis**:
- Error: Accessing `.name` on undefined object
- Root: `UserProfile.tsx:15:32` (your component)
- Framework: React rendering internals (ignore)

**Fix**: Add null check in `UserProfile.tsx:15`

### Minified Stack Traces

```javascript
TypeError: Cannot read property 'name' of undefined
    at t.render (main.a3b4c5d6.js:1:23456)
    at u (2.chunk.js:4:567)
```

**Problem**: Minified code is unreadable (`t`, `u`, cryptic filenames)

**Solution**: Use source maps

```javascript
// With source map
TypeError: Cannot read property 'name' of undefined
    at UserProfile.render (src/components/UserProfile.tsx:15:32)
    at ReactComponent.update (src/lib/react.ts:45:12)
```

**How**: Ensure source maps are available:
- Development: Always enabled
- Production: Enable for debugging (`.map` files)
- Error tracking: Sentry, Bugsnag auto-apply source maps

## Java Stack Traces

### Format

```java
java.lang.NullPointerException: Cannot invoke "User.getName()" because "user" is null
    at com.example.UserService.getFullName(UserService.java:42)
    at com.example.UserController.getUserProfile(UserController.java:23)
    at org.springframework.web.method.support.InvocableHandlerMethod.invoke(InvocableHandlerMethod.java:219)
    at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:142)
```

**Reading Order**: Top-down

**Analysis**:
- Exception: `NullPointerException` with helpful message (Java 14+)
- Root: `UserService.java:42` calling `.getName()` on null
- Caller: `UserController.java:23`
- Framework: Spring MVC (ignore)

**Fix**: Add null check at `UserService.java:42`

## FastAPI/Pydantic Stack Traces

### Validation Error

```python
pydantic.error_wrappers.ValidationError: 2 validation errors for UserCreate
email
  field required (type=value_error.missing)
age
  ensure this value is greater than 0 (type=value_error.number.not_gt; limit_value=0)
```

**Analysis**:
- Not a traditional stack trace - validation error report
- Lists all validation failures
- Each error shows: field, message, type

**Fix**: Client must send valid `email` (required) and `age > 0`

### FastAPI Exception

```python
Traceback (most recent call last):
  File "/app/api/endpoints/users.py", line 45, in create_user
    db_user = await crud.user.create(user_in)
  File "/app/crud/user.py", line 23, in create
    db.add(db_obj)
  File "/venv/lib/sqlalchemy/orm/session.py", line 2345, in add
    raise IntegrityError("UNIQUE constraint failed: users.email")
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.email
```

**Analysis**:
- Database constraint violation
- Root in your code: `crud/user.py:23` trying to insert duplicate email
- Caller: `api/endpoints/users.py:45`

**Fix**: Check if user exists before insert, or use upsert

## Cloudflare Workers Stack Traces

### Format

```javascript
Error: Failed to fetch user data
    at fetchUser (worker.js:45:11)
    at handleRequest (worker.js:23:18)
```

**Characteristics**:
- Minimal stack (no Node.js internals)
- V8 isolate execution context
- Limited to worker code only

**Edge Cases**:
```javascript
Uncaught (in promise) TypeError: response.json is not a function
```
- Common: Missing `await` on fetch response
- Fix: `await response.json()` instead of `response.json()`

## Pattern Recognition

### Null/Undefined Access Patterns

**Python**:
```
AttributeError: 'NoneType' object has no attribute 'X'
TypeError: 'NoneType' object is not subscriptable
```

**JavaScript**:
```
TypeError: Cannot read property 'X' of null
TypeError: Cannot read property 'X' of undefined
```

**Java**:
```
java.lang.NullPointerException: Cannot invoke "X" because "Y" is null
```

### Type Mismatch Patterns

**Python**:
```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
TypeError: 'X' object is not callable
```

**JavaScript**:
```
TypeError: X is not a function
TypeError: Cannot convert undefined or null to object
```

### Import/Module Patterns

**Python**:
```
ModuleNotFoundError: No module named 'X'
ImportError: cannot import name 'X' from 'Y'
```

**JavaScript**:
```
Error: Cannot find module 'X'
SyntaxError: Unexpected token 'export'
```

### Database Patterns

**SQLAlchemy**:
```
sqlalchemy.orm.exc.NoResultFound
sqlalchemy.exc.IntegrityError: UNIQUE constraint failed
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection refused
```

**Drizzle ORM**:
```
DrizzleError: Unique constraint failed on column: email
DrizzleError: Connection to database server failed
```

## Analysis Workflow

### 1. Identify Exception Type

```python
# Example
sqlalchemy.exc.IntegrityError: UNIQUE constraint failed: users.email
# ↓
# Type: IntegrityError (database constraint)
# Subtype: UNIQUE (duplicate key)
```

### 2. Locate Root Frame in Your Code

```python
Traceback (most recent call last):
  File "/app/api/users.py", line 45, in create_user     # ← Root frame
    db.add(user)
  File "/venv/lib/sqlalchemy/orm/session.py", line 2345, in add  # ← Library
    raise IntegrityError()
```

**Rule**: First frame in your project directory before library/framework code

### 3. Trace Backwards Through Call Chain

```python
create_user (users.py:45)
    ↓ calls
UserService.create (user_service.py:23)
    ↓ calls
db.add (sqlalchemy) → IntegrityError
```

**Analysis**: Error originates in `db.add`, propagates through `UserService.create`, surfaces in `create_user` endpoint

### 4. Identify Data Flow

```python
# users.py:45
user = User(email=request.email)  # ← Where does request.email come from?
db.add(user)  # ← Fails with UNIQUE constraint

# Trace back:
# request.email ← Request body
# ← Client sent duplicate email
# ← Need validation before DB insert
```

### 5. Formulate Hypothesis

**Pattern**: UNIQUE constraint → Attempting duplicate insert
**Root Cause**: No existence check before insert
**Fix**: Add existence check or use upsert

## Advanced Patterns

### Recursive Stack Traces

```python
RecursionError: maximum recursion depth exceeded
  File "/app/services/tree.py", line 23, in calculate_depth
    return 1 + calculate_depth(node.parent)
  File "/app/services/tree.py", line 23, in calculate_depth
    return 1 + calculate_depth(node.parent)
  [Previous line repeated 996 more times]
```

**Analysis**: Circular reference in `node.parent` chain

**Fix**: Add base case or cycle detection

### Chained Exceptions (Python 3)

```python
Traceback (most recent call last):
  File "/app/db/connection.py", line 15, in connect
    engine.connect()
  sqlalchemy.exc.OperationalError: connection refused

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/app/api/users.py", line 45, in get_user
    db.connect()
  File "/app/db/connection.py", line 20, in connect
    raise DatabaseConnectionError() from e
app.exceptions.DatabaseConnectionError: Failed to connect to database
```

**Reading**: Two stack traces:
1. Original: `OperationalError` (connection refused)
2. Wrapped: `DatabaseConnectionError` (user-friendly message)

**Root Cause**: Original exception (connection refused)

### Multiple Exception Points

```javascript
UnhandledPromiseRejectionWarning: Error: API request failed
    at fetchData (api.js:23:11)
    (node:12345) UnhandledPromiseRejectionWarning: Unhandled promise rejection.
```

**Analysis**: Promise rejected but no `.catch()` handler

**Fix**: Add `.catch()` or use `try/await/catch`

## Quick Reference

| Language | Read Direction | Focus On | Ignore |
|----------|---------------|----------|--------|
| **Python** | Bottom-up | Last frame in your code | `/venv/`, stdlib |
| **JavaScript** | Top-down | First frame in your code | `node_modules/` |
| **Java** | Top-down | `com.example.*` | `org.springframework.*` |
| **TypeScript** | Top-down | `src/`, `.ts` files | `node_modules/`, `.min.js` |

| Error Pattern | Stack Trace Indicator | Fix Priority |
|---------------|----------------------|--------------|
| **Null/undefined** | `NoneType`, `null`, `undefined` | High |
| **Type mismatch** | `unsupported operand`, `is not a function` | Medium |
| **Import error** | `ModuleNotFoundError`, `Cannot find module` | High |
| **Database** | `IntegrityError`, `OperationalError` | High |
| **Async** | `await`, `Promise`, `Coroutine` | Medium |

---

**Usage**: When debugging, identify exception type, locate root frame in your code, trace backwards through call chain, identify data flow, formulate hypothesis.
