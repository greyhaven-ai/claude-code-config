# Security Review Example

Complete security review of an authentication service with 12 vulnerabilities found and fixed.

## Scenario

**Project**: FastAPI authentication service for multi-tenant SaaS application
**Initial State**: Multiple security vulnerabilities, failed security audit
**Goal**: Identify and fix all security issues before production deployment
**Time Investment**: 4 hours analysis + 6 hours fixes = 10 hours total

## Before: Vulnerable Code

### auth_service.py (Problematic)

```python
import hashlib
import jwt
import random
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text

app = FastAPI()

# ISSUE 1: Hardcoded secret key
SECRET_KEY = "my-super-secret-key-123"

# ISSUE 2: Using MD5 for password hashing
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# ISSUE 3: SQL injection vulnerability
def get_user_by_email(email: str, db):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    result = db.execute(text(query)).fetchone()
    return result

# ISSUE 4: Weak session token generation
def generate_session_token() -> str:
    return str(random.randint(100000, 999999))

# ISSUE 5: JWT with weak algorithm
def create_access_token(user_id: str) -> str:
    expires = datetime.utcnow() + timedelta(days=365)  # ISSUE 6: Token expires in 1 year
    payload = {
        "user_id": user_id,
        "exp": expires,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ISSUE 7: No rate limiting on login endpoint
@app.post("/login")
async def login(email: str, password: str, db=Depends(get_db)):
    user = get_user_by_email(email, db)

    if not user:
        # ISSUE 8: Information disclosure (reveals if email exists)
        raise HTTPException(status_code=404, detail="User not found")

    # ISSUE 9: Timing attack vulnerability
    if hash_password(password) == user.password_hash:
        token = create_access_token(user.id)

        # ISSUE 10: Token in URL parameter (logged in plaintext)
        return {"token": token, "redirect": f"/dashboard?token={token}"}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")

# ISSUE 11: No authentication required
@app.get("/user/{user_id}")
async def get_user(user_id: str, db=Depends(get_db)):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    user = db.execute(text(query)).fetchone()

    # ISSUE 12: Returns sensitive data without sanitization
    return {
        "id": user.id,
        "email": user.email,
        "password_hash": user.password_hash,  # Exposed!
        "ssn": user.ssn,  # PII exposed!
        "credit_card": user.credit_card,  # Payment data exposed!
    }
```

## Security Review Process

### Step 1: Automated Vulnerability Scan

```bash
# Run security scanner
bandit -r app/ -f json -o security-report.json

# Results: 12 HIGH severity issues found
```

### Step 2: Manual Code Review

**Critical Issues (P0 - Fix Immediately)**:
1. **SQL Injection** (CWE-89) - Lines 15-17, 53-54
2. **Hardcoded Secrets** (CWE-798) - Line 10
3. **Weak Cryptography** (CWE-327) - Lines 13-14

**High Priority (P1 - Fix Before Deployment)**:
4. **Weak Session Tokens** (CWE-330) - Lines 20-21
5. **Information Disclosure** (CWE-209) - Line 36
6. **Missing Authentication** (CWE-306) - Lines 47-60
7. **Sensitive Data Exposure** (CWE-311) - Lines 56-60

**Medium Priority (P2 - Fix Soon)**:
8. **Timing Attack** (CWE-208) - Line 31
9. **Token in URL** (CWE-598) - Line 35
10. **No Rate Limiting** (CWE-307) - Line 24
11. **Long-Lived Tokens** (CWE-613) - Line 24
12. **Weak JWT Algorithm** (CWE-327) - Line 29

### Step 3: Security Scorecard

```
Category                Score   Issues
-----------------------------------
Input Validation        20/100  SQL injection (2 instances)
Authentication          30/100  Weak passwords, timing attacks
Cryptography            25/100  MD5, weak JWT, hardcoded keys
Data Protection         15/100  PII exposure, sensitive data in responses
Session Management      40/100  Weak tokens, long expiry
Access Control          10/100  Missing auth checks
-----------------------------------
OVERALL SCORE:          28/100  ⛔️ CRITICAL - DO NOT DEPLOY
```

## After: Secure Code

### auth_service.py (Fixed)

```python
import secrets
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlmodel import Session, select
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, EmailStr
import structlog

app = FastAPI()
logger = structlog.get_logger()

# ✅ FIX 1: Use environment variables for secrets
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # ✅ FIX 6: Short-lived tokens

# ✅ FIX 2: Use bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ FIX 7: Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ✅ FIX 4: Cryptographically secure session tokens
def generate_session_token() -> str:
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ FIX 3: Parameterized query (SQL injection prevention)
def get_user_by_email(email: str, db: Session) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ✅ FIX 11: Authentication dependency
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """✅ FIX 12: Sanitized user response - no sensitive data"""
    id: str
    email: str
    name: str
    role: str
    created_at: datetime

# ✅ FIX 10: Rate limiting on login
@app.post("/login")
@limiter.limit("5/minute")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    # ✅ FIX 3: Use parameterized query
    user = get_user_by_email(request.email, db)

    # ✅ FIX 5 & 8: Generic error message (no information disclosure)
    if not user or not verify_password(request.password, user.password_hash):
        logger.warning("Failed login attempt", email=request.email)

        # Generic error - doesn't reveal if email exists
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # ✅ FIX 8: Constant-time comparison (timing attack prevention)
    # (passlib.verify already uses constant-time comparison)

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    logger.info("Successful login", user_id=user.id)

    # ✅ FIX 9: Token in header, not URL
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

# ✅ FIX 11: Authentication required
@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Authorization check: Users can only view their own profile
    # (unless admin)
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user",
        )

    # ✅ FIX 3: Parameterized query
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # ✅ FIX 12: Return sanitized response (Pydantic model filters fields)
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        created_at=user.created_at,
    )
```

### Additional Security: .env.example

```bash
# ✅ FIX 1: Environment variables for secrets
JWT_SECRET_KEY=generate-with-openssl-rand-base64-32
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
```

### Additional Security: requirements.txt

```
# ✅ Updated dependencies with security fixes
fastapi==0.104.1
sqlmodel==0.0.14
passlib[bcrypt]==1.7.4  # ✅ FIX 2: Secure password hashing
python-jose[cryptography]==3.3.0  # ✅ JWT with strong crypto
slowapi==0.1.9  # ✅ FIX 10: Rate limiting
structlog==23.2.0  # ✅ Secure logging
pydantic[email]==2.5.0  # ✅ Email validation
```

## Results

### Security Scorecard: After Fixes

```
Category                Before  After   Change
-------------------------------------------
Input Validation        20/100  95/100  +75 ✅
Authentication          30/100  95/100  +65 ✅
Cryptography            25/100  95/100  +70 ✅
Data Protection         15/100  100/100 +85 ✅
Session Management      40/100  90/100  +50 ✅
Access Control          10/100  95/100  +85 ✅
-------------------------------------------
OVERALL SCORE:          28/100  95/100  +67 ✅

Status: ✅ PRODUCTION READY
```

### Vulnerabilities Fixed

| Issue | Severity | Fix | Time |
|-------|----------|-----|------|
| SQL Injection (2x) | 🔴 Critical | Parameterized queries | 30 min |
| Hardcoded Secret | 🔴 Critical | Environment variables | 15 min |
| Weak Hashing (MD5) | 🔴 Critical | bcrypt with salt | 20 min |
| Weak Session Tokens | 🟠 High | Cryptographically secure | 10 min |
| Information Disclosure | 🟠 High | Generic error messages | 10 min |
| Missing Authentication | 🟠 High | JWT bearer auth | 45 min |
| PII Exposure | 🟠 High | Response sanitization | 20 min |
| Timing Attack | 🟡 Medium | Constant-time comparison | 5 min |
| Token in URL | 🟡 Medium | Header-based auth | 10 min |
| No Rate Limiting | 🟡 Medium | slowapi integration | 30 min |
| Long-Lived Tokens | 🟡 Medium | 30-minute expiry | 5 min |
| Weak JWT Algorithm | 🟡 Medium | HS256 with strong key | 5 min |

**Total Time**: 3 hours 25 minutes of focused fixes

### Metrics

**Lines of Code**:
- Before: 65 lines
- After: 145 lines
- Change: +80 lines (+123%) - Security requires more code!

**Dependency Changes**:
- Added: passlib, python-jose, slowapi, structlog
- Security-focused dependencies: 4 added

**Test Coverage**:
- Before: 0% (no tests for auth)
- After: 95% (comprehensive security tests added)

## Key Lessons

### 1. Defense in Depth

Don't rely on a single security measure:
- ✅ Rate limiting + strong passwords + account lockout
- ✅ Parameterized queries + input validation + WAF
- ✅ HTTPS + secure tokens + short expiry

### 2. Secure by Default

Use secure defaults from the start:
- ✅ bcrypt (not MD5)
- ✅ secrets module (not random)
- ✅ Environment variables (not hardcoded)
- ✅ Short-lived tokens (not 1 year)

### 3. Information Disclosure

Attackers use error messages to probe:
- ❌ "User not found" → Reveals valid emails
- ❌ "Invalid password" → Confirms email exists
- ✅ "Invalid email or password" → Generic, secure

### 4. Input Validation

Never trust user input:
- ✅ Parameterized queries (SQL injection prevention)
- ✅ Pydantic models (type validation)
- ✅ EmailStr (email format validation)

### 5. Sensitive Data Handling

Minimize exposure:
- ✅ Never return password hashes
- ✅ Never return PII unless necessary
- ✅ Use response models to whitelist fields
- ✅ Log securely (no PII in logs)

## Production Deployment Checklist

- [x] All critical vulnerabilities fixed
- [x] Security dependencies updated
- [x] Environment variables configured
- [x] Rate limiting enabled
- [x] Authentication required on all endpoints
- [x] Response sanitization implemented
- [x] Security tests passing (95% coverage)
- [x] Penetration testing completed
- [x] Security audit passed (95/100 score)
- [x] WAF configured
- [x] HTTPS enforced
- [x] Security headers configured

---

Related: [Clarity Refactoring Example](clarity-refactoring-example.md) | [Synthesis Analysis Example](synthesis-analysis-example.md) | [Return to INDEX](INDEX.md)
