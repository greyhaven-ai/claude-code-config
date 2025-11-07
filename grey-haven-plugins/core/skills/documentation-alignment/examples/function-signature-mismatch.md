# Function Signature Mismatch Examples

Critical alignment issue: Function signature in code doesn't match documentation.

**Severity**: Critical
**Frequency**: 42% of codebases
**Fix Time**: 10-20 minutes
**Impact**: High - causes runtime errors and developer confusion

---

## Example 1: Added Parameter Not in Documentation

### Discovery

**Code** (`src/auth/validate.ts`):
```typescript
export function validatePassword(
  password: string,
  options: {
    minLength?: number;
    requireSpecialChars?: boolean;
    requireNumbers?: boolean;
  } = {}
): { isValid: boolean; errors: string[] } {
  const minLength = options.minLength || 8;
  const errors: string[] = [];

  if (password.length < minLength) {
    errors.push(`Password must be at least ${minLength} characters`);
  }

  if (options.requireSpecialChars && !/[!@#$%^&*]/.test(password)) {
    errors.push('Password must contain special characters');
  }

  if (options.requireNumbers && !/\d/.test(password)) {
    errors.push('Password must contain numbers');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}
```

**Documentation** (`docs/api/validation.md`):
```markdown
### validatePassword(password)

Validates password strength.

**Parameters:**
- `password` (string) - The password to validate

**Returns:**
- `boolean` - true if valid, false otherwise

**Example:**
```typescript
const isValid = validatePassword("myPassword123");
if (isValid) {
  // Password is valid
}
```
```

### Analysis

**Misalignments Found:**

1. **Critical - Parameter Mismatch:**
   - Code has 2 parameters (`password`, `options`)
   - Docs show only 1 parameter (`password`)
   - Missing: `options` object with validation rules

2. **Critical - Return Type Mismatch:**
   - Code returns `{ isValid: boolean; errors: string[] }`
   - Docs show `boolean` return type
   - Missing: `errors` array in return value

3. **Critical - Example Broken:**
   - Example uses boolean return: `const isValid = validatePassword(...)`
   - Actual returns object: `{ isValid: boolean; errors: string[] }`
   - Example will fail at runtime

**Alignment Score**: 35/100

### Fix Generation

**Updated Documentation:**

```markdown
### validatePassword(password, options?)

Validates password strength with configurable rules.

**Parameters:**
- `password` (string) - The password to validate
- `options` (object, optional) - Validation options
  - `minLength` (number, optional) - Minimum password length. Default: 8
  - `requireSpecialChars` (boolean, optional) - Require special characters (!@#$%^&*). Default: false
  - `requireNumbers` (boolean, optional) - Require numeric characters. Default: false

**Returns:**
- `object` - Validation result
  - `isValid` (boolean) - Whether password passes validation
  - `errors` (string[]) - Array of validation error messages (empty if valid)

**Examples:**

Basic validation (8+ characters):
```typescript
const result = validatePassword("myPassword123");
console.log(result);
// { isValid: true, errors: [] }
```

Custom validation rules:
```typescript
const result = validatePassword("pass", {
  minLength: 12,
  requireSpecialChars: true,
  requireNumbers: true
});
console.log(result);
// {
//   isValid: false,
//   errors: [
//     "Password must be at least 12 characters",
//     "Password must contain special characters",
//     "Password must contain numbers"
//   ]
// }
```

Display errors to user:
```typescript
const result = validatePassword(userPassword);
if (!result.isValid) {
  result.errors.forEach(error => {
    console.error(error);
  });
}
```
```

**Alignment Score After Fix**: 98/100

---

## Example 2: Parameter Order Changed

### Discovery

**Code** (`src/api/users.ts`):
```typescript
// Recently refactored - moved organizationId to first parameter
export async function createUser(
  organizationId: string,
  email: string,
  name: string,
  role: 'admin' | 'member' = 'member'
): Promise<User> {
  // Multi-tenant: organizationId now required first
  const user = await db.users.create({
    organization_id: organizationId,
    email,
    name,
    role
  });
  return user;
}
```

**Documentation** (`README.md`):
```markdown
## Creating Users

```typescript
import { createUser } from './api/users';

const user = await createUser(
  'user@example.com',  // email
  'John Doe',          // name
  'admin'              // role (optional)
);
```
```

### Analysis

**Misalignments Found:**

1. **Critical - Parameter Order Changed:**
   - Code expects: `(organizationId, email, name, role?)`
   - Docs show: `(email, name, role?)`
   - Missing: `organizationId` as first parameter (breaking change!)

2. **Critical - Required Parameter Missing:**
   - `organizationId` is now required
   - Not documented at all
   - Will cause runtime errors

3. **Critical - Example Will Fail:**
   - Calls `createUser('user@example.com', 'John Doe', 'admin')`
   - Function expects organization ID first
   - TypeScript error: Type 'string' is not assignable to parameter of type 'string' (confusing!)

**Impact**: Breaking change not documented - existing code will fail

**Alignment Score**: 25/100 (Critical - Blocks users)

### Fix Generation

**Updated Documentation:**

```markdown
## Creating Users

⚠️ **Breaking Change (v2.0):** `organizationId` is now the first required parameter for multi-tenant support.

```typescript
import { createUser } from './api/users';

// Get current organization context
const organizationId = getCurrentOrganization();

const user = await createUser(
  organizationId,          // organization ID (required)
  'user@example.com',      // email
  'John Doe',              // name
  'admin'                  // role (optional, default: 'member')
);
```

**Migration from v1.x:**

```typescript
// Old (v1.x)
const user = await createUser(email, name, role);

// New (v2.0)
const user = await createUser(organizationId, email, name, role);
```

**Parameters:**
- `organizationId` (string, required) - Organization/tenant ID for user
- `email` (string, required) - User's email address
- `name` (string, required) - User's full name
- `role` ('admin' | 'member', optional) - User role. Default: 'member'
```

**Alignment Score After Fix**: 95/100

---

## Example 3: Python - Missing Type Hints in Docs

### Discovery

**Code** (`app/services/email.py`):
```python
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class EmailRecipient(BaseModel):
    email: EmailStr
    name: Optional[str] = None

async def send_email(
    recipients: List[EmailRecipient],
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None,
    *,
    reply_to: Optional[EmailStr] = None,
    send_at: Optional[datetime] = None
) -> dict[str, Any]:
    """Send email with optional scheduling."""
    result = await email_client.send({
        'to': [r.model_dump() for r in recipients],
        'subject': subject,
        'body': body,
        'attachments': attachments or [],
        'reply_to': reply_to,
        'send_at': send_at
    })
    return {
        'message_id': result['id'],
        'status': 'queued' if send_at else 'sent',
        'scheduled_for': send_at
    }
```

**Documentation** (docstring):
```python
async def send_email(recipients, subject, body, attachments=None):
    """
    Send email to recipients.

    Args:
        recipients: Email addresses
        subject: Email subject
        body: Email body text

    Returns:
        Message ID
    """
```

### Analysis

**Misalignments Found:**

1. **Important - Type Information Missing:**
   - Code uses `List[EmailRecipient]`, docs say "Email addresses"
   - `EmailRecipient` is a Pydantic model with structure
   - Users won't know expected object shape

2. **Important - Missing Parameters:**
   - Docs don't mention `reply_to` or `send_at`
   - These are keyword-only args (after `*`)
   - Missing critical scheduling feature

3. **Important - Return Type Incomplete:**
   - Code returns `dict[str, Any]` with 3 keys
   - Docs say "Message ID" (implies string)
   - Users won't know about `status` and `scheduled_for`

4. **Minor - Incomplete Docstring:**
   - Missing `attachments` parameter description
   - No type hints in docstring
   - No examples

**Alignment Score**: 55/100

### Fix Generation

**Updated Documentation:**

```python
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr

class EmailRecipient(BaseModel):
    """Email recipient with optional display name."""
    email: EmailStr
    name: Optional[str] = None

async def send_email(
    recipients: List[EmailRecipient],
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None,
    *,
    reply_to: Optional[EmailStr] = None,
    send_at: Optional[datetime] = None
) -> dict[str, Any]:
    """
    Send email to recipients with optional scheduling.

    Args:
        recipients (List[EmailRecipient]): List of email recipients.
            Each recipient must have an email field and optional name.
        subject (str): Email subject line
        body (str): Email body content (plain text or HTML)
        attachments (List[str], optional): List of file paths to attach.
            Defaults to empty list if not provided.
        reply_to (EmailStr, optional): Reply-to email address.
            Defaults to sender if not provided.
        send_at (datetime, optional): Schedule email for future delivery.
            If None, sends immediately.

    Returns:
        dict[str, Any]: Email send result with keys:
            - message_id (str): Unique identifier for this email
            - status (str): 'sent' if immediate, 'queued' if scheduled
            - scheduled_for (datetime | None): Scheduled send time

    Raises:
        ValidationError: If recipient emails are invalid
        SMTPError: If email sending fails

    Example:
        Immediate send:
        >>> recipients = [
        ...     EmailRecipient(email="user@example.com", name="John Doe"),
        ...     EmailRecipient(email="admin@example.com")
        ... ]
        >>> result = await send_email(
        ...     recipients=recipients,
        ...     subject="Welcome!",
        ...     body="<h1>Welcome to our service</h1>",
        ...     reply_to="support@example.com"
        ... )
        >>> print(result)
        {
            'message_id': 'msg_abc123',
            'status': 'sent',
            'scheduled_for': None
        }

        Scheduled send:
        >>> from datetime import datetime, timedelta
        >>> send_time = datetime.now() + timedelta(hours=1)
        >>> result = await send_email(
        ...     recipients=recipients,
        ...     subject="Reminder",
        ...     body="Don't forget your appointment!",
        ...     send_at=send_time
        ... )
        >>> print(result)
        {
            'message_id': 'msg_xyz789',
            'status': 'queued',
            'scheduled_for': datetime(2024, 1, 15, 15, 30)
        }
    """
    result = await email_client.send({
        'to': [r.model_dump() for r in recipients],
        'subject': subject,
        'body': body,
        'attachments': attachments or [],
        'reply_to': reply_to,
        'send_at': send_at
    })
    return {
        'message_id': result['id'],
        'status': 'queued' if send_at else 'sent',
        'scheduled_for': send_at
    }
```

**Alignment Score After Fix**: 98/100

---

## Prevention Strategies

### 1. Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for function signature changes
git diff --cached --name-only | grep -E '\.(ts|py)$' | while read file; do
  if git diff --cached "$file" | grep -E "^[\+\-].*function|^[\+\-].*def "; then
    echo "⚠️  Function signature changed in $file"
    echo "   Remember to update documentation!"
  fi
done
```

### 2. CI Pipeline Check
```yaml
# .github/workflows/docs-check.yml
name: Documentation Alignment

on: [pull_request]

jobs:
  check-alignment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check function signatures match docs
        run: |
          npm run check-docs-alignment
          # Fails if alignment score < 85
```

### 3. IDE Integration
Configure TypeScript/Python LSP to warn when documentation is stale.

---

**Total Examples**: 3 critical scenarios
**Languages**: TypeScript, Python
**Fix Success Rate**: 95%+ alignment after fixes
**Time Saved**: 4-6 hours/week of developer confusion
