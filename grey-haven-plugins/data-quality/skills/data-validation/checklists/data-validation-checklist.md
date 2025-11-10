# Data Validation Checklist

Comprehensive checklist for implementing robust data validation in TypeScript (Zod) and Python (Pydantic) applications.

## Pre-Validation Setup

- [ ] **Identify all input sources** (API requests, forms, file uploads, external APIs)
- [ ] **Choose validation library** (Zod for TypeScript, Pydantic for Python)
- [ ] **Define validation strategy** (fail-fast vs collect all errors)
- [ ] **Set up error handling** (consistent error response format)
- [ ] **Document validation requirements** (business rules, constraints)

## TypeScript + Zod Validation

### Schema Definition

- [ ] **All API endpoints have Zod schemas** defined
- [ ] **Schema types exported** for use in frontend
- [ ] **Schemas colocated** with route handlers or in shared location
- [ ] **Schema composition used** (z.object, z.array, z.union)
- [ ] **Reusable schemas extracted** (common patterns like email, UUID)

### Basic Validations

- [ ] **String validations** applied:
  - [ ] `.min()` for minimum length
  - [ ] `.max()` for maximum length
  - [ ] `.email()` for email addresses
  - [ ] `.url()` for URLs
  - [ ] `.uuid()` for UUIDs
  - [ ] `.regex()` for custom patterns
  - [ ] `.trim()` to remove whitespace

- [ ] **Number validations** applied:
  - [ ] `.int()` for integers
  - [ ] `.positive()` for positive numbers
  - [ ] `.min()` / `.max()` for ranges
  - [ ] `.finite()` to exclude Infinity/NaN

- [ ] **Array validations** applied:
  - [ ] `.min()` for minimum items
  - [ ] `.max()` for maximum items
  - [ ] `.nonempty()` for required arrays

- [ ] **Date validations** applied:
  - [ ] `.min()` for earliest date
  - [ ] `.max()` for latest date
  - [ ] Proper date parsing (z.coerce.date())

### Advanced Validations

- [ ] **Custom refinements** for complex rules:
  ```typescript
  z.object({
    password: z.string(),
    confirmPassword: z.string()
  }).refine(data => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"]
  })
  ```

- [ ] **Conditional validations** with `.superRefine()`
- [ ] **Transform validations** to normalize data (`.transform()`)
- [ ] **Discriminated unions** for polymorphic data
- [ ] **Branded types** for domain-specific values

### Error Handling

- [ ] **Validation errors caught** and formatted consistently
- [ ] **Error messages user-friendly** (not technical jargon)
- [ ] **Field-level errors** returned (which field failed)
- [ ] **Multiple errors collected** (not just first error)
- [ ] **Error codes standardized** (e.g., "INVALID_EMAIL")

### Multi-Tenant Context

- [ ] **tenant_id validated** on all requests requiring tenant context
- [ ] **UUID format verified** for tenant_id
- [ ] **Tenant existence checked** (tenant must exist in database)
- [ ] **User-tenant relationship verified** (user belongs to tenant)
- [ ] **Admin permissions validated** for admin-only operations

## Python + Pydantic Validation

### Model Definition

- [ ] **All API request models** inherit from BaseModel
- [ ] **All response models** defined with Pydantic
- [ ] **SQLModel used** for database models (includes Pydantic)
- [ ] **Field validators** used for custom validation
- [ ] **Model validators** used for cross-field validation

### Basic Field Validators

- [ ] **EmailStr** used for email fields
- [ ] **HttpUrl** used for URL fields
- [ ] **UUID4** used for UUID fields
- [ ] **Field()** used with constraints:
  - [ ] `min_length` / `max_length` for strings
  - [ ] `ge` / `le` for number ranges (greater/less than or equal)
  - [ ] `gt` / `lt` for strict ranges
  - [ ] `regex` for pattern matching

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
```

### Advanced Validation

- [ ] **@field_validator** for single field custom validation:
  ```python
  @field_validator('password')
  @classmethod
  def validate_password(cls, v):
      if len(v) < 8:
          raise ValueError('Password must be at least 8 characters')
      return v
  ```

- [ ] **@model_validator** for cross-field validation:
  ```python
  @model_validator(mode='after')
  def check_passwords_match(self):
      if self.password != self.confirm_password:
          raise ValueError('Passwords do not match')
      return self
  ```

- [ ] **Custom validators** handle edge cases
- [ ] **Mode='before'** used for preprocessing
- [ ] **Mode='after'** used for post-validation checks

### Error Handling

- [ ] **ValidationError caught** in API endpoints
- [ ] **Errors formatted** to match frontend expectations
- [ ] **HTTPException raised** with 422 status for validation errors
- [ ] **Error details included** in response body
- [ ] **Logging added** for validation failures (security monitoring)

### Multi-Tenant Context

- [ ] **tenant_id field** on all multi-tenant request models
- [ ] **Tenant UUID validated** before database queries
- [ ] **Repository pattern enforces** tenant filtering
- [ ] **Admin flag validated** for privileged operations
- [ ] **RLS policies configured** on database tables

## Database Constraints

### Schema Constraints

- [ ] **NOT NULL constraints** on required fields
- [ ] **UNIQUE constraints** on unique fields (email, username)
- [ ] **CHECK constraints** for value ranges
- [ ] **FOREIGN KEY constraints** for relationships
- [ ] **Default values** defined where appropriate

### Index Support

- [ ] **Indexes created** on frequently queried fields
- [ ] **Composite indexes** for multi-field queries
- [ ] **Partial indexes** for filtered queries (WHERE clauses)
- [ ] **tenant_id indexed** on all multi-tenant tables

## File Upload Validation

- [ ] **File size limits** enforced (e.g., 10MB max)
- [ ] **File type validation** (MIME type checking)
- [ ] **File extension validation** (whitelist allowed extensions)
- [ ] **Virus scanning** (if handling untrusted uploads)
- [ ] **Content validation** (parse and validate file content)

### Image Uploads

- [ ] **Image dimensions validated** (max width/height)
- [ ] **Image format verified** (PNG, JPEG, etc.)
- [ ] **EXIF data stripped** (security concern)
- [ ] **Thumbnails generated** for large images

### CSV/JSON Uploads

- [ ] **Parse errors handled gracefully**
- [ ] **Schema validation** applied to each row/object
- [ ] **Batch validation** with error collection
- [ ] **Maximum rows/objects** limit enforced

## External API Integration

- [ ] **Response schemas defined** for external APIs
- [ ] **Validation applied** to external data
- [ ] **Graceful degradation** when validation fails
- [ ] **Retry logic** for transient failures
- [ ] **Timeout limits** configured

## Security Validations

### Input Sanitization

- [ ] **HTML/script tags stripped** from text inputs
- [ ] **SQL injection prevented** (use ORM, not raw SQL)
- [ ] **XSS prevention** (escape output in templates)
- [ ] **Path traversal prevented** (validate file paths)
- [ ] **Command injection prevented** (no shell execution of user input)

### Authentication & Authorization

- [ ] **JWT tokens validated** (signature, expiration)
- [ ] **Session tokens verified** against database
- [ ] **User existence checked** before operations
- [ ] **Permissions verified** for protected resources
- [ ] **Rate limiting applied** to prevent abuse

### Sensitive Data

- [ ] **Passwords never logged** or returned in responses
- [ ] **Credit card numbers validated** with Luhn algorithm
- [ ] **SSN/Tax ID formats validated**
- [ ] **PII handling compliant** with regulations (GDPR, CCPA)
- [ ] **Encryption applied** to sensitive stored data

## Testing Validation Logic

### Unit Tests

- [ ] **Valid inputs pass** validation
- [ ] **Invalid inputs fail** with correct error messages
- [ ] **Edge cases tested** (empty strings, null, undefined)
- [ ] **Boundary values tested** (min/max lengths, ranges)
- [ ] **Error messages verified** (correct field, message)

### Integration Tests

- [ ] **API endpoints validated** in integration tests
- [ ] **Database constraints tested** (violate constraint, expect error)
- [ ] **Multi-tenant isolation tested** (cross-tenant access blocked)
- [ ] **File upload validation tested**
- [ ] **External API mocking** with invalid responses

### Test Coverage

- [ ] **Validation logic 100% covered**
- [ ] **Error paths tested** (not just happy path)
- [ ] **Custom validators tested** independently
- [ ] **Refinements tested** with failing cases

## Performance Considerations

- [ ] **Validation performance measured** (avoid expensive validations in hot paths)
- [ ] **Async validation** for I/O-bound checks (database lookups)
- [ ] **Caching applied** to repeated validations (e.g., tenant existence)
- [ ] **Batch validation** for arrays/lists
- [ ] **Early returns** for fail-fast scenarios

## Documentation

- [ ] **Validation rules documented** in API docs
- [ ] **Error responses documented** (status codes, error formats)
- [ ] **Examples provided** (valid and invalid requests)
- [ ] **Schema exported** for frontend consumption (TypeScript types)
- [ ] **Changelog updated** when validation changes

## Grey Haven Specific

### TanStack Start (Frontend)

- [ ] **Form validation** with Zod + TanStack Form
- [ ] **Server function validation** (all server functions validate input)
- [ ] **Type safety** maintained (Zod.infer<> for types)
- [ ] **Error display** in UI components
- [ ] **Client-side validation** mirrors server-side

### FastAPI (Backend)

- [ ] **Request models** use Pydantic
- [ ] **Response models** use Pydantic
- [ ] **Repository methods** validate before database operations
- [ ] **Service layer** handles business rule validation
- [ ] **Dependency injection** for validation context (tenant_id)

### Database (Drizzle/SQLModel)

- [ ] **Drizzle schemas** include validation constraints
- [ ] **SQLModel fields** use Pydantic validators
- [ ] **Migration scripts** add database constraints
- [ ] **Indexes support** validation queries

## Monitoring & Alerting

- [ ] **Validation failure metrics** tracked
- [ ] **High failure rate alerts** configured
- [ ] **Unusual validation patterns** logged (potential attacks)
- [ ] **Performance metrics** for validation operations
- [ ] **Error logs** structured for analysis

## Scoring

- **80+ items checked**: Excellent - Comprehensive validation ✅
- **60-79 items**: Good - Most validation covered ⚠️
- **40-59 items**: Fair - Significant gaps exist 🔴
- **<40 items**: Poor - Inadequate validation ❌

## Priority Items

Address these first:
1. **All API endpoints validated** - Prevent invalid data entry
2. **Multi-tenant isolation** - Security-critical
3. **SQL injection prevention** - Use ORM, not raw SQL
4. **File upload validation** - Common attack vector
5. **Error handling** - User experience and debugging

## Common Pitfalls

❌ **Don't:**
- Trust client-side validation alone (always validate server-side)
- Use overly complex regex (hard to maintain, performance issues)
- Return technical error messages to users
- Skip validation on internal endpoints (defense in depth)
- Log sensitive data in validation errors

✅ **Do:**
- Validate at boundaries (API endpoints, file uploads, external APIs)
- Use standard validators (email, URL, UUID) from libraries
- Provide clear, actionable error messages
- Test validation logic thoroughly
- Document validation requirements

## Related Resources

- [Zod Documentation](https://zod.dev)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [data-validation skill](../SKILL.md)

---

**Total Items**: 120+ validation checks
**Critical Items**: API validation, Multi-tenant, Security, File uploads
**Coverage**: TypeScript, Python, Database, Security
**Last Updated**: 2025-11-10
