# Security Checklist

Complete security checklist covering OWASP Top 10, input validation, authentication, cryptography, and data protection.

## OWASP Top 10 (2021)

### A01: Broken Access Control

**What to Check**:
- [ ] All API endpoints require authentication
- [ ] Authorization checks verify user permissions
- [ ] Users can only access their own data (multi-tenant isolation)
- [ ] No direct object references without authorization
- [ ] Admin functions require admin role
- [ ] CORS configured properly (not `allow_origin="*"`)
- [ ] Rate limiting on sensitive endpoints

**Example Vulnerabilities**:
```python
# ❌ Bad: No authentication check
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return db.get_user(user_id)  # Anyone can access any user!

# ✅ Good: Authentication + authorization
@app.get("/users/{user_id}")
def get_user(user_id: str, current_user = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(403, "Not authorized")
    return db.get_user(user_id)
```

### A02: Cryptographic Failures

**What to Check**:
- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] Secrets not hardcoded (use environment variables)
- [ ] TLS/HTTPS enforced in production
- [ ] Sensitive data not logged
- [ ] No weak algorithms (DES, RC4, MD5)
- [ ] Secure random for tokens (`secrets` module, not `random`)
- [ ] Database connections encrypted

**Example Vulnerabilities**:
```python
# ❌ Bad: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ Good: Strong hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = pwd_context.hash(password)

# ❌ Bad: Hardcoded secret
SECRET_KEY = "my-secret-key-123"

# ✅ Good: Environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY must be set")
```

### A03: Injection

**What to Check**:
- [ ] All SQL queries use parameterized queries or ORM
- [ ] No string concatenation in SQL
- [ ] User input validated before use
- [ ] Command injection prevented (no `os.system` with user input)
- [ ] LDAP injection prevented
- [ ] NoSQL injection prevented
- [ ] Input sanitized for XSS

**Example Vulnerabilities**:
```python
# ❌ Bad: SQL injection
query = f"SELECT * FROM users WHERE email = '{email}'"
db.execute(query)

# ✅ Good: Parameterized query
query = "SELECT * FROM users WHERE email = ?"
db.execute(query, (email,))

# ✅ Better: ORM
user = db.query(User).filter(User.email == email).first()

# ❌ Bad: Command injection
os.system(f"ping {user_input}")

# ✅ Good: Use subprocess with list
subprocess.run(["ping", user_input], check=True)
```

### A04: Insecure Design

**What to Check**:
- [ ] Threat modeling completed
- [ ] Security requirements documented
- [ ] Secure defaults configured
- [ ] Principle of least privilege applied
- [ ] Defense in depth implemented
- [ ] Fail securely (errors don't expose information)
- [ ] Security testing in CI/CD

**Design Patterns**:
```python
# ✅ Fail securely
try:
    user = authenticate(email, password)
except Exception as e:
    logger.error("Auth error", exc_info=True)
    # Generic message (no information disclosure)
    raise HTTPException(401, "Invalid credentials")

# ✅ Principle of least privilege
class User:
    role: str  # "member", "admin", "owner"

    def can_delete_user(self, target_user_id: str) -> bool:
        # Only admins/owners can delete, not members
        if self.role not in ["admin", "owner"]:
            return False
        # Users can't delete themselves
        if self.id == target_user_id:
            return False
        return True
```

### A05: Security Misconfiguration

**What to Check**:
- [ ] Debug mode disabled in production
- [ ] Default passwords changed
- [ ] Unnecessary features disabled
- [ ] Security headers configured (CSP, X-Frame-Options)
- [ ] Error messages don't expose stack traces
- [ ] Dependencies up to date
- [ ] Cloud storage not publicly accessible

**Common Misconfigurations**:
```python
# ❌ Bad: Debug mode in production
app = FastAPI(debug=True)  # Exposes stack traces!

# ✅ Good: Debug only in development
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
app = FastAPI(debug=DEBUG)

# ❌ Bad: Permissive CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accepts any origin!
    allow_credentials=True,
)

# ✅ Good: Restricted CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
)
```

### A06: Vulnerable and Outdated Components

**What to Check**:
- [ ] All dependencies updated regularly
- [ ] Security advisories monitored
- [ ] No known vulnerabilities in dependencies
- [ ] Unused dependencies removed
- [ ] Dependency scanning in CI/CD
- [ ] Lock files committed (requirements.txt, package-lock.json)

**Tools**:
```bash
# Python
pip-audit  # Check for known vulnerabilities
safety check

# JavaScript/TypeScript
npm audit
npm audit fix

# GitHub
# Enable Dependabot alerts
```

### A07: Identification and Authentication Failures

**What to Check**:
- [ ] Multi-factor authentication available
- [ ] Strong password requirements enforced
- [ ] Account lockout after failed attempts
- [ ] Session timeout configured
- [ ] Session tokens cryptographically random
- [ ] Logout invalidates session
- [ ] No default credentials

**Example Vulnerabilities**:
```python
# ❌ Bad: Weak session token
session_token = str(random.randint(100000, 999999))

# ✅ Good: Strong session token
import secrets
session_token = secrets.token_urlsafe(32)

# ❌ Bad: No password requirements
def create_user(password: str):
    if len(password) < 3:  # Too weak!
        raise ValueError("Password too short")

# ✅ Good: Strong password requirements
import re

def validate_password(password: str):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain uppercase letter")
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain lowercase letter")
    if not re.search(r'[0-9]', password):
        raise ValueError("Password must contain number")
    if not re.search(r'[!@#$%^&*]', password):
        raise ValueError("Password must contain special character")
```

### A08: Software and Data Integrity Failures

**What to Check**:
- [ ] Code signing implemented
- [ ] Dependencies verified (checksums, signatures)
- [ ] CI/CD pipeline secured
- [ ] Serialization/deserialization secured
- [ ] Auto-update mechanisms verified
- [ ] Integrity checks on critical data

**Example Vulnerabilities**:
```python
# ❌ Bad: Unsafe deserialization
import pickle
data = pickle.loads(user_input)  # Can execute arbitrary code!

# ✅ Good: Safe deserialization
import json
data = json.loads(user_input)  # Only supports safe data types

# ❌ Bad: No integrity check
def save_config(config_data):
    with open("config.json", "w") as f:
        json.dump(config_data, f)

# ✅ Good: Integrity check with HMAC
import hmac
import hashlib

def save_config(config_data, secret_key):
    json_data = json.dumps(config_data)
    signature = hmac.new(
        secret_key.encode(),
        json_data.encode(),
        hashlib.sha256
    ).hexdigest()

    with open("config.json", "w") as f:
        json.dump({"data": config_data, "signature": signature}, f)
```

### A09: Security Logging and Monitoring Failures

**What to Check**:
- [ ] Failed logins logged
- [ ] Access violations logged
- [ ] Input validation failures logged
- [ ] Logs centralized and monitored
- [ ] Logs don't contain sensitive data
- [ ] Alerting configured for anomalies
- [ ] Audit trail for critical operations

**Example Implementation**:
```python
import structlog

logger = structlog.get_logger()

# ✅ Good: Security event logging
@app.post("/login")
def login(email: str, password: str):
    user = authenticate(email, password)

    if not user:
        logger.warning("Failed login attempt",
            email=email,
            ip=request.client.host,
            timestamp=datetime.utcnow()
        )
        raise HTTPException(401, "Invalid credentials")

    logger.info("Successful login",
        user_id=user.id,
        ip=request.client.host
    )
    return generate_token(user)

# ❌ Bad: Logging sensitive data
logger.info("User login", password=password)  # DON'T LOG PASSWORDS!

# ✅ Good: No sensitive data in logs
logger.info("User login", user_id=user.id)
```

### A10: Server-Side Request Forgery (SSRF)

**What to Check**:
- [ ] URLs validated before fetching
- [ ] Internal IPs blocked
- [ ] URL schema whitelisted (http/https only)
- [ ] Network segmentation implemented
- [ ] Response validation

**Example Vulnerabilities**:
```python
# ❌ Bad: SSRF vulnerability
import requests

@app.get("/fetch")
def fetch_url(url: str):
    response = requests.get(url)  # Can access internal services!
    return response.text

# User could provide: url=http://localhost:6379/  (Redis)
# Or: url=http://169.254.169.254/latest/meta-data/  (AWS metadata)

# ✅ Good: URL validation
from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = ["http", "https"]
BLOCKED_HOSTS = ["localhost", "127.0.0.1"]

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)

    # Check scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        return False

    # Check for internal IPs
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback:
            return False
    except ValueError:
        pass  # Not an IP, check hostname

    # Check blocked hosts
    if parsed.hostname in BLOCKED_HOSTS:
        return False

    return True

@app.get("/fetch")
def fetch_url(url: str):
    if not is_safe_url(url):
        raise HTTPException(400, "Invalid URL")

    response = requests.get(url, timeout=5)
    return response.text
```

## Additional Security Checks

### Input Validation

- [ ] All user input validated at entry point
- [ ] Whitelist validation preferred over blacklist
- [ ] Length limits enforced
- [ ] Type validation (Pydantic models)
- [ ] File upload size limits
- [ ] File type validation (not just extension)

### Output Encoding

- [ ] HTML output escaped (prevents XSS)
- [ ] JSON responses properly encoded
- [ ] SQL parameters escaped (parameterized queries)
- [ ] URL parameters encoded

### Rate Limiting

- [ ] Login endpoints rate limited
- [ ] API endpoints rate limited
- [ ] Password reset rate limited
- [ ] Search endpoints rate limited

### Security Headers

```python
# ✅ Security headers
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

## Security Checklist Summary

```
Category                    Checks  Critical
-------------------------------------------
Access Control              7       Yes
Cryptographic Failures      7       Yes
Injection                   7       Yes
Insecure Design             7       No
Security Misconfiguration   7       Yes
Vulnerable Components       6       Yes
Authentication Failures     7       Yes
Data Integrity              6       No
Logging & Monitoring        7       No
SSRF                        5       Yes
Additional Checks           16      Yes
-------------------------------------------
TOTAL:                      82      9 critical
```

---

Related: [Clarity Refactoring Rules](clarity-refactoring-rules.md) | [Code Quality Metrics](code-quality-metrics.md) | [Return to INDEX](INDEX.md)
