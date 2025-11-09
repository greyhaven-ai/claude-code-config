# Fix Generation Patterns

Comprehensive guide to generating, evaluating, and implementing fixes for software bugs.

## Multiple Fix Options Strategy

**Core Principle**: Always generate 2-3 fix options with trade-off analysis.

### Fix Option Template

```markdown
**Option 1: [Name]** (e.g., Quick Fix)
**Implementation**: [What to change]
**Pros**: [Benefits]
**Cons**: [Drawbacks]
**Effort**: [Time estimate]
**Risk**: [Low/Medium/High]

**Option 2: [Name]** (e.g., Proper Fix)
**Implementation**: [What to change]
**Pros**: [Benefits]
**Cons**: [Drawbacks]
**Effort**: [Time estimate]
**Risk**: [Low/Medium/High]

**Option 3: [Name]** (e.g., Comprehensive Fix)
**Implementation**: [What to change]
**Pros**: [Benefits]
**Cons**: [Drawbacks]
**Effort**: [Time estimate]
**Risk**: [Low/Medium/High]

**Recommendation**: Option [X] because [reasoning]
```

_See [null-pointer-debug-example.md](../examples/null-pointer-debug-example.md) for complete fix options example._

## Quick Fix vs. Proper Fix

### Decision Matrix

| Criteria | Quick Fix | Proper Fix |
|----------|-----------|------------|
| **Urgency** | Production down, immediate relief needed | Incident resolved, addressing root cause |
| **Scope** | Minimal changes, single file | Multiple files, architectural changes |
| **Time** | Minutes to hours | Hours to days |
| **Testing** | Manual verification | Full test coverage required |
| **Risk** | Low (minimal changes) | Medium (broader impact) |
| **Longevity** | Temporary patch | Permanent solution |

### When to Use Quick Fix

✅ **Production incident** - System is down, users impacted
✅ **Known workaround** - Clear, safe mitigation exists
✅ **Low risk** - Change is isolated and reversible
✅ **Follow-up planned** - Proper fix scheduled for next sprint

**Pattern**: Quick fix now → Monitor → Proper fix later

### When to Use Proper Fix

✅ **Root cause addressed** - Not just treating symptoms
✅ **Proper testing** - Comprehensive test coverage added
✅ **Type safety** - Leverages static type checking
✅ **Prevention** - Prevents entire class of similar bugs
✅ **Documentation** - Code is self-documenting

**Pattern**: Understand root cause → Comprehensive fix → Prevent recurrence

## Fix Priority Assessment

### Priority Matrix

| Severity | Frequency | Priority | Response Time |
|----------|-----------|----------|---------------|
| **Critical** | High | P0 | Immediate (< 1 hour) |
| **Critical** | Low | P1 | Same day |
| **Major** | High | P1 | Same day |
| **Major** | Low | P2 | This week |
| **Minor** | High | P2 | This week |
| **Minor** | Low | P3 | Next sprint |

**Severity Criteria**:
- **Critical**: Data loss, security breach, production down
- **Major**: Degraded performance, incorrect results, feature broken
- **Minor**: Edge case, cosmetic issue, rare error

**Frequency Criteria**:
- **High**: Affects >10% of users or happens >10 times/day
- **Low**: Affects <1% of users or happens occasionally

## Common Fix Patterns by Error Type

### Null/Undefined Errors

**Pattern 1: Null Check with Default**
```python
# Before
name = user.name  # NoneType error

# After
name = user.name if user else "Unknown"
```

**Pattern 2: Raise Exception** (API boundaries)
```python
# Before
user = db.users.find_one(user_id)
return user.name  # NoneType error

# After
user = db.users.find_one(user_id)
if user is None:
    raise HTTPException(404, "User not found")
return user.name
```

### Type Errors

**Pattern 1: Type Conversion with Validation**
```python
# Before
total = base_price + discount  # TypeError: int + str

# After
from pydantic import BaseModel

class PriceInput(BaseModel):
    base_price: int
    discount: int  # Automatic validation and conversion

input_data = PriceInput(**request_body)  # Validates types
total = input_data.base_price + input_data.discount
```

### Database Errors

**Pattern 1: Constraint Violations**
```python
# Before
db.add(user)
db.commit()  # IntegrityError: UNIQUE constraint failed

# After
from sqlalchemy.exc import IntegrityError

try:
    db.add(user)
    db.commit()
except IntegrityError:
    db.rollback()
    # Option A: Return error
    raise HTTPException(409, "User with this email already exists")
    # Option B: Upsert
    existing = db.query(User).filter_by(email=user.email).first()
    if existing:
        existing.name = user.name
        db.commit()
```

**Pattern 2: Connection Failures**
```python
# Before
engine = create_engine(DATABASE_URL)
connection = engine.connect()  # OperationalError: connection refused

# After
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def get_connection():
    engine = create_engine(DATABASE_URL)
    return engine.connect()

connection = get_connection()
```

### API/Integration Errors

**Pattern 1: Validation at Boundary**
```python
# Before
response = payment_api.create_charge(amount=order.total)
# Fails with 422 if amount < 50 (API minimum)

# After
class CreateChargeRequest(BaseModel):
    amount: int

    @validator('amount')
    def amount_meets_minimum(cls, v):
        if v < 50:
            raise ValueError('Amount must be at least $0.50')
        return v

# Validate before API call
request = CreateChargeRequest(amount=order.total)  # Fails early
response = payment_api.create_charge(**request.dict())
```

**Pattern 2: Retry with Backoff**
```python
# Before
response = httpx.get(api_url)  # Timeout occasionally

# After
from tenacity import retry, retry_if_exception_type, stop_after_attempt

@retry(
    retry=retry_if_exception_type(httpx.TimeoutException),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def fetch_with_retry(url: str):
    async with httpx.AsyncClient(timeout=5.0) as client:
        return await client.get(url)
```

### Performance Errors

**Pattern 1: N+1 Query Fix**
```python
# Before (N+1 queries)
users = db.query(User).all()  # 1 query
for user in users:
    posts = db.query(Post).filter(Post.user_id == user.id).all()  # N queries

# After (Single query with join)
users = db.query(User).options(
    joinedload(User.posts)
).all()  # 1 query with join
```

**Pattern 2: Caching**
```python
# Before
def get_user_profile(user_id: str):
    return db.query(User).filter_by(id=user_id).first()  # Every time

# After
from functools import lru_cache
from cachetools import TTLCache, cached

cache = TTLCache(maxsize=1000, ttl=300)  # 5 minute TTL

@cached(cache)
def get_user_profile(user_id: str):
    return db.query(User).filter_by(id=user_id).first()
```

## Fix Validation Strategies

### Validation Checklist

```markdown
Before deploying fix:
- [ ] Fix addresses root cause (not just symptoms)
- [ ] Tests added to prevent recurrence
- [ ] Tests pass locally
- [ ] Code reviewed by peer
- [ ] No new linting/type errors
- [ ] Performance impact assessed
- [ ] Security implications reviewed
- [ ] Rollback plan documented
- [ ] Monitoring/alerts updated
```

### Test-Driven Fix Approach

**Pattern**: Write failing test → Implement fix → Test passes

```python
# Step 1: Write failing test
def test_get_user_with_invalid_id_returns_404():
    """Test that invalid user_id returns 404, not 500."""
    response = client.get("/users/invalid-id")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

# Step 2: Run test (should fail with current bug)
# pytest tests/test_users.py::test_get_user_with_invalid_id_returns_404
# AssertionError: 500 != 404

# Step 3: Implement fix
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(404, "User not found")
    return user

# Step 4: Run test (should pass)
# pytest tests/test_users.py::test_get_user_with_invalid_id_returns_404
# PASSED
```

### Integration Testing

```python
# Test fix with realistic scenario
@pytest.mark.integration
async def test_order_creation_with_negative_total():
    """Integration test: Ensure negative order total is rejected."""
    # Setup
    user = await create_test_user()

    # Attempt to create order with negative total
    response = await client.post("/orders", json={
        "user_id": user.id,
        "items": [],
        "total": -100  # Invalid
    })

    # Assert validation error
    assert response.status_code == 422
    assert "total must be positive" in response.json()["detail"]

    # Verify no order created in database
    orders = await db.orders.find({"user_id": user.id})
    assert len(orders) == 0
```

## Refactoring Considerations

### When to Refactor During Fix

**Refactor if**:
✅ Fix requires understanding convoluted code
✅ Code duplication prevents proper fix
✅ Poor structure makes fix risky
✅ Fix is part of larger architectural improvement

**Don't refactor if**:
❌ Production incident needs immediate fix
❌ Refactoring scope unclear
❌ Tests insufficient to ensure safety
❌ Refactoring can be done separately

### Refactoring Patterns

**Pattern 1: Extract Function**
```python
# Before (hard to fix null error)
def process_order(order_data):
    user = db.users.find_one(order_data["user_id"])
    if user.is_active and user.credits > 0:
        # 50 lines of order processing
        pass

# After (easier to add null check)
def process_order(order_data):
    user = get_validated_user(order_data["user_id"])
    process_order_for_user(user, order_data)

def get_validated_user(user_id: str) -> User:
    """Get user and validate they can place orders."""
    user = db.users.find_one(user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    if not user.is_active:
        raise HTTPException(403, "User account inactive")
    if user.credits <= 0:
        raise HTTPException(402, "Insufficient credits")
    return user
```

## Production Safety

### Pre-Deployment Checklist

```markdown
- [ ] Fix tested in staging environment
- [ ] Performance impact measured (CPU, memory, latency)
- [ ] Database migrations tested with production-sized data
- [ ] Feature flag available for gradual rollout
- [ ] Rollback procedure documented and tested
- [ ] Monitoring dashboard shows relevant metrics
- [ ] Alerts configured for fix-related failures
- [ ] On-call engineer briefed on deployment
- [ ] Communication sent to stakeholders
```

### Gradual Rollout Pattern

```python
# Use feature flag for gradual rollout
from launchdarkly import LDClient

ld_client = LDClient("sdk-key")

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    use_new_validation = ld_client.variation(
        "new-user-validation",
        {"key": user_id},
        default=False
    )

    if use_new_validation:
        # New fix with validation
        user = await get_validated_user(user_id)
    else:
        # Old code (fallback)
        user = await db.users.find_one(user_id)

    return user
```

## Rollback Planning

### Rollback Decision Criteria

**Rollback immediately if**:
- Error rate spikes >5% above baseline
- Critical functionality broken
- Data corruption detected
- Performance degrades >50%
- Security vulnerability introduced

**Monitor and investigate if**:
- Error rate increases <5%
- Non-critical functionality affected
- Performance degrades <20%
- Edge cases failing

### Rollback Procedures

**1. Application Code Rollback**
```bash
# Git-based rollback
git revert <commit-hash>
git push origin main

# Or redeploy previous version
git checkout <previous-tag>
./deploy.sh
```

**2. Database Migration Rollback**
```bash
# Alembic (Python)
alembic downgrade -1

# Drizzle (TypeScript)
bun run drizzle-kit drop --migration <migration-name>
```

**3. Feature Flag Disable**
```python
# Instantly disable via LaunchDarkly dashboard or API
ld_client.variation("new-user-validation", context, default=False)
```

**4. Cache Invalidation**
```python
# Clear cache after rollback
redis_client.flushdb()  # Clear all cache
# Or selectively
redis_client.delete("user:*")  # Clear user cache only
```

## Quick Reference

| Error Type | Primary Fix Pattern | Testing Strategy |
|------------|-------------------|------------------|
| **Null/Undefined** | Null check, optional chaining, raise exception | Unit test with None input |
| **Type Mismatch** | Pydantic validation, type guards | Unit test with wrong types |
| **Database** | Try/except with rollback, retries | Integration test with DB |
| **API/Integration** | Validation at boundary, retries | Mock API responses |
| **Performance** | Caching, query optimization | Performance benchmark test |

| Fix Type | When to Use | Risk Level |
|----------|-------------|------------|
| **Quick Fix** | Production incident | Low (isolated change) |
| **Proper Fix** | Root cause resolution | Medium (broader changes) |
| **Comprehensive Fix** | Prevention of entire class | Medium-High (architectural) |

---

**Usage**: When implementing fix, generate 2-3 options with trade-offs, select best option based on priority, validate with tests, deploy with gradual rollout, monitor closely, document rollback procedure.
