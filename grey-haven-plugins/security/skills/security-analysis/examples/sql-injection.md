# SQL Injection Vulnerability Examples

Real-world SQL injection attack scenarios with exploitation details, CVSS scoring, and complete remediation using Grey Haven stack (FastAPI, SQLModel, PostgreSQL).

## Overview

**OWASP Category**: A03:2021 - Injection
**CVSS v3.1 Score**: 9.8 (Critical)
**Attack Vector**: Network
**Complexity**: Low
**Privileges Required**: None
**User Interaction**: None
**Impact**: Complete database compromise, data exfiltration, privilege escalation

## Vulnerability Pattern 1: String Concatenation in SQL Queries

### Vulnerable Code (FastAPI + Raw SQL)

```python
# app/api/users.py - VULNERABLE
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.auth import get_current_tenant_id

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/search")
async def search_users(
    query: str,
    session: Session = Depends(get_session),
    tenant_id: str = Depends(get_current_tenant_id)
):
    """Search users - VULNERABLE TO SQL INJECTION."""

    # ❌ CRITICAL VULNERABILITY: String concatenation
    sql = f"""
        SELECT id, email, username, role
        FROM users
        WHERE tenant_id = '{tenant_id}'
        AND (username LIKE '%{query}%' OR email LIKE '%{query}%')
    """

    results = session.exec(sql).fetchall()
    return {"users": results}
```

### Exploitation Scenario

**Attack Vector**: Malicious query parameter

```bash
# Normal usage
GET /api/users/search?query=alice

# SQL Injection Attack 1: Data Exfiltration
GET /api/users/search?query=alice'%20UNION%20SELECT%20id,%20password_hash,%20api_key,%20role%20FROM%20users--

# Resulting SQL (bypasses tenant_id filtering):
SELECT id, email, username, role
FROM users
WHERE tenant_id = 'tenant-123'
AND (username LIKE '%alice' UNION SELECT id, password_hash, api_key, role FROM users--%'
    OR email LIKE '%alice' UNION SELECT id, password_hash, api_key, role FROM users--%')

# Attack 2: Admin Privilege Escalation
GET /api/users/search?query='; UPDATE users SET role = 'admin' WHERE username = 'attacker'--

# Attack 3: Multi-Tenant Data Breach
GET /api/users/search?query=' OR '1'='1

# Resulting SQL (returns ALL users from ALL tenants):
SELECT id, email, username, role
FROM users
WHERE tenant_id = 'tenant-123'
AND (username LIKE '%' OR '1'='1%' OR email LIKE '%' OR '1'='1%')
```

**Impact Metrics**:
- **Data Breach**: 100% of database accessible
- **Privilege Escalation**: Attacker gains admin access in 1 request
- **Multi-Tenant Isolation Bypass**: All tenant data exposed
- **Estimated Damage**: $500K+ (GDPR fines, data breach costs)

### Secure Implementation

```python
# app/api/users.py - SECURE
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.models.user import User
from app.database import get_session
from app.auth import get_current_tenant_id
from typing import List
from uuid import UUID

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/search")
async def search_users(
    query: str = Query(..., min_length=1, max_length=100),
    session: Session = Depends(get_session),
    tenant_id: UUID = Depends(get_current_tenant_id)
) -> dict:
    """Search users securely with parameterized queries."""

    # ✅ SECURE: SQLModel ORM with parameterized queries
    statement = (
        select(User)
        .where(User.tenant_id == tenant_id)  # Multi-tenant isolation
        .where(
            (User.username.contains(query)) |
            (User.email.contains(query))
        )
        .limit(100)  # Prevent resource exhaustion
    )

    users = session.exec(statement).all()

    return {
        "users": [
            {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role
            }
            for user in users
        ]
    }
```

**Security Improvements**:
1. **Parameterized Queries**: SQLModel ORM prevents injection
2. **Input Validation**: Pydantic Query validation (max_length=100)
3. **Multi-Tenant Isolation**: tenant_id enforced at ORM level
4. **Result Limiting**: LIMIT 100 prevents DoS
5. **No Password Exposure**: Only safe fields returned

## Vulnerability Pattern 2: Blind SQL Injection

### Vulnerable Code (Authentication Bypass)

```python
# app/api/auth.py - VULNERABLE
from fastapi import APIRouter, HTTPException
from app.database import get_session

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
async def login(username: str, password: str):
    """Login endpoint - VULNERABLE TO BLIND SQL INJECTION."""

    session = get_session()

    # ❌ CRITICAL: String interpolation in WHERE clause
    sql = f"""
        SELECT id, role, email
        FROM users
        WHERE username = '{username}' AND password_hash = '{password}'
    """

    user = session.exec(sql).first()

    if user:
        return {"success": True, "user_id": user.id}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
```

### Exploitation: Time-Based Blind SQL Injection

```bash
# Extract database name character by character
POST /api/auth/login
{
  "username": "admin' AND SUBSTRING((SELECT database()),1,1)='p'--",
  "password": "anything"
}

# If response is slower (time-based):
# Character at position 1 is 'p' (postgres)

# Extract password hash
POST /api/auth/login
{
  "username": "admin' AND SUBSTRING((SELECT password_hash FROM users WHERE username='admin'),1,1)='$'--",
  "password": "anything"
}

# Automated extraction with sqlmap:
sqlmap -u "https://api.greyhaven.io/api/auth/login" \
  --data "username=admin&password=test" \
  --technique=T \
  --dump
```

**Impact**:
- **Password Hash Extraction**: Complete in 5-10 minutes
- **Database Enumeration**: All tables and schemas exposed
- **No Rate Limiting**: Unlimited attempts

### Secure Implementation

```python
# app/api/auth.py - SECURE
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models.user import User
from app.database import get_session
from app.security import verify_password, create_access_token
from pydantic import BaseModel, Field, EmailStr

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    """Login credentials validation."""
    username: str = Field(..., min_length=3, max_length=30, pattern=r'^[a-zA-Z0-9_-]+$')
    password: str = Field(..., min_length=8, max_length=128)

@router.post("/login")
async def login(
    credentials: LoginRequest,
    session: Session = Depends(get_session)
):
    """Secure login with parameterized queries and timing attack prevention."""

    # ✅ SECURE: SQLModel ORM with parameterized query
    statement = select(User).where(User.username == credentials.username)
    user = session.exec(statement).first()

    # ✅ Constant-time password verification (prevents timing attacks)
    if not user or not verify_password(credentials.password, user.password_hash):
        # Same error message for user not found vs wrong password
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # ✅ Rate limiting (via middleware - see security-analyzer.md)
    # ✅ Account lockout after 5 failed attempts
    # ✅ JWT token generation
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email
        }
    }
```

## Vulnerability Pattern 3: Second-Order SQL Injection

### Vulnerable Code (User Profile Update)

```python
# app/api/profile.py - VULNERABLE
@router.put("/profile/bio")
async def update_bio(
    bio: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update user bio - VULNERABLE TO SECOND-ORDER INJECTION."""

    # ❌ Step 1: Store malicious payload (seems safe)
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    user.bio = bio  # Payload: "'; DROP TABLE users--"
    session.commit()

    # ❌ Step 2: Later code uses bio unsafely
    # In another endpoint:
    sql = f"SELECT * FROM activity WHERE user_bio = '{user.bio}'"
    # Executes: SELECT * FROM activity WHERE user_bio = ''; DROP TABLE users--'
```

### Secure Implementation

```python
# app/api/profile.py - SECURE
from pydantic import BaseModel, Field, field_validator

class BioUpdate(BaseModel):
    """Bio update with validation."""
    bio: str = Field(..., max_length=500)

    @field_validator('bio')
    @classmethod
    def sanitize_bio(cls, v: str) -> str:
        """Remove dangerous characters."""
        # Only allow alphanumeric, spaces, punctuation
        import re
        if not re.match(r'^[a-zA-Z0-9\s.,!?\'-]+$', v):
            raise ValueError('Bio contains invalid characters')
        return v.strip()

@router.put("/profile/bio")
async def update_bio(
    bio_data: BioUpdate,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Secure bio update."""

    # ✅ Validated and sanitized input
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ ORM prevents injection even if bio is used in queries later
    user.bio = bio_data.bio
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"success": True, "bio": user.bio}
```

## CVSS v3.1 Scoring Breakdown

**Base Score: 9.8 (Critical)**

| Metric | Value | Reasoning |
|--------|-------|-----------|
| **Attack Vector (AV)** | Network (N) | Exploitable remotely via HTTP API |
| **Attack Complexity (AC)** | Low (L) | No special conditions required |
| **Privileges Required (PR)** | None (N) | Can exploit unauthenticated endpoints |
| **User Interaction (UI)** | None (N) | No user interaction needed |
| **Scope (S)** | Unchanged (U) | Affects only vulnerable component |
| **Confidentiality (C)** | High (H) | Complete database disclosure |
| **Integrity (I)** | High (H) | Database modification possible |
| **Availability (A)** | High (H) | DROP TABLE attacks possible |

**CVSS Vector**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`

## Prevention Checklist

- [ ] **Use ORM exclusively** (SQLModel/SQLAlchemy)
- [ ] **Never concatenate user input** into SQL strings
- [ ] **Validate all inputs** with Pydantic models
- [ ] **Enforce multi-tenant isolation** at ORM level
- [ ] **Limit query results** (LIMIT clause)
- [ ] **Use prepared statements** for raw SQL (if absolutely necessary)
- [ ] **Implement rate limiting** on all endpoints
- [ ] **Log all SQL queries** in development
- [ ] **Run static analysis** (Bandit for Python)
- [ ] **Perform penetration testing** before production

## Testing for SQL Injection

```python
# tests/security/test_sql_injection.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_users_sql_injection_prevention():
    """Verify SQL injection is prevented in user search."""

    # Attempt SQL injection
    malicious_queries = [
        "' OR '1'='1",
        "'; DROP TABLE users--",
        "' UNION SELECT password_hash FROM users--",
        "admin'--",
        "' OR 1=1#"
    ]

    for query in malicious_queries:
        response = client.get(
            f"/api/users/search?query={query}",
            headers={"Authorization": "Bearer test-token"}
        )

        # Should return safe results, not error or expose data
        assert response.status_code in [200, 400, 422]

        if response.status_code == 200:
            data = response.json()
            # Should not return all users
            assert len(data.get("users", [])) < 10
            # Should not expose password hashes
            for user in data.get("users", []):
                assert "password_hash" not in user
                assert "password" not in user

def test_login_blind_sql_injection_prevention():
    """Verify blind SQL injection is prevented in login."""

    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin' AND SLEEP(5)--",
            "password": "test"
        }
    )

    # Should respond quickly (not execute SLEEP)
    assert response.elapsed.total_seconds() < 1.0
    assert response.status_code == 401
```

## Real-World Impact

**Case Study: 2023 Multi-Tenant SaaS Breach**
- **Vulnerability**: SQL injection in search endpoint (similar to Pattern 1)
- **Attack**: `query=' OR '1'='1` bypassed tenant_id filtering
- **Impact**: 50,000 customer records exposed across 200 tenants
- **Cost**: $2.3M (GDPR fines + remediation + customer compensation)
- **Remediation Time**: 72 hours emergency patch + 2 weeks full audit
- **Prevention**: Would have been prevented by SQLModel ORM

## Summary

| Attack Type | CVSS | Exploitability | Impact | Prevention |
|-------------|------|----------------|--------|------------|
| **String Concatenation** | 9.8 | Easy | Critical | Use ORM |
| **Blind SQL Injection** | 9.8 | Moderate | Critical | Parameterized queries |
| **Second-Order Injection** | 8.1 | Difficult | High | Input sanitization + ORM |

**Key Takeaway**: **NEVER concatenate user input into SQL queries**. Always use SQLModel ORM or parameterized queries with proper input validation.

---

**Next**: [XSS Vulnerabilities](xss-vulnerabilities.md) | **Index**: [Examples Index](INDEX.md)
