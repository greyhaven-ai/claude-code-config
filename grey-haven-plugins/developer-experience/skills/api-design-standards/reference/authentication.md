# Authentication Configuration

**JWT setup with bcrypt password hashing.**

```python
# app/core/auth.py
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user_id: str, tenant_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode({"sub": user_id, "tenant_id": tenant_id, "exp": expire}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

**Doppler:** `JWT_SECRET_KEY` must be set in Doppler secrets.
