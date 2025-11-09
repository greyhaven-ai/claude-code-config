# Documentation Standards and Quality Guidelines

Comprehensive standards for creating high-quality technical documentation for Grey Haven projects.

## Documentation Principles

### 1. Progressive Disclosure
Start with overview, provide details on demand.

**Good**:
```markdown
# User Authentication

Quick overview: Our authentication uses JWT tokens with refresh rotation.

## Getting Started
[Simple example]

## Advanced Usage
[Detailed configuration options]

## Security Considerations
[Deep dive into security]
```

### 2. Show, Don't Tell
Use code examples instead of lengthy explanations.

**Bad**: "To create a user, you need to instantiate a User class with email and password, then call the save method."

**Good**:
```python
user = User(email="user@example.com", password="secure123")
user.save()
```

### 3. Keep It Current
Documentation that's out of date is worse than no documentation.

Use automation:
- Auto-generate API docs from code
- CI/CD validation (fail if docs outdated)
- Link to code for truth source

## Writing Style

### Voice and Tone

**Use Active Voice**:
- ❌ "The order will be processed by the system"
- ✅ "The system processes the order"

**Be Direct**:
- ❌ "It might be a good idea to consider using..."
- ✅ "Use X when Y"

**Avoid Jargon**:
- ❌ "Leverage our enterprise-grade synergistic platform"
- ✅ "Use our API to manage users"

### Structure

**Every Page Should Have**:
1. **Title**: Clear, descriptive
2. **Summary**: 1-2 sentence overview
3. **Prerequisites**: What user needs to know/have
4. **Step-by-Step**: Numbered instructions
5. **Code Examples**: Working, copy-paste ready
6. **Troubleshooting**: Common errors and solutions
7. **Next Steps**: Where to go next

### Code Examples

**Always Include**:
- ✅ Complete, working examples
- ✅ Expected output/result
- ✅ Error handling
- ✅ Comments explaining why, not what

**Example Template**:
```python
# Create a new user
# Requires: Admin authentication
# Returns: User object or raises ValidationError

try:
    user = User.objects.create(
        email="user@example.com",
        password="secure123",
        role="member"  # Default role for new users
    )
    print(f"User created: {user.id}")
except ValidationError as e:
    print(f"Validation failed: {e.message}")
```

## API Documentation Standards

### Endpoint Documentation Template

```markdown
## POST /api/v1/users

Create a new user account.

### Authentication
Requires: Admin JWT token in Authorization header

### Request

**Headers**:
- `Authorization: Bearer <token>` (required)
- `Content-Type: application/json` (required)

**Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| password | string | Yes | Min 8 characters |
| role | string | No | Default: "member" |

**Example**:
```json
{
  "email": "user@example.com",
  "password": "secure123",
  "role": "member"
}
```

### Response

**Success (201 Created)**:
```json
{
  "id": "usr_123abc",
  "email": "user@example.com",
  "role": "member",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
- `400 Bad Request`: Validation failed (email invalid, password too short)
- `401 Unauthorized`: Missing or invalid auth token
- `403 Forbidden`: User lacks admin role
- `409 Conflict`: Email already exists
- `429 Too Many Requests`: Rate limit exceeded

**Error Response**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Email address is invalid",
  "details": {
    "field": "email",
    "value": "invalid-email"
  }
}
```

### Rate Limiting
- Authenticated: 1000 requests/hour
- Unauthenticated: 100 requests/hour

### Code Examples

**TypeScript**:
```typescript
const response = await fetch("https://api.greyhaven.com/users", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    email: "user@example.com",
    password: "secure123"
  })
});

if (!response.ok) {
  const error = await response.json();
  throw new Error(error.message);
}

const user = await response.json();
console.log(`User created: ${user.id}`);
```

**Python**:
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://api.greyhaven.com/users",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "user@example.com", "password": "secure123"}
    )
    response.raise_for_status()
    user = response.json()
    print(f"User created: {user['id']}")
```
```

## Function Documentation Standards

### JSDoc (TypeScript)

```typescript
/**
 * Calculate order total including tax and shipping.
 * 
 * @param items - Array of order items with quantity and price
 * @param shippingAddress - Address for tax calculation
 * @returns Total amount in USD cents
 * @throws {ValidationError} If items array is empty
 * @throws {TaxCalculationError} If tax lookup fails
 * 
 * @example
 * const total = calculateTotal(
 *   [{ quantity: 2, price: 2999 }],
 *   { zip: "94105", country: "US" }
 * );
 * // Returns: 6398 (5998 + 400 tax + 0 shipping)
 */
export function calculateTotal(
  items: OrderItem[],
  shippingAddress: Address
): number {
  if (items.length === 0) {
    throw new ValidationError("Items array cannot be empty");
  }
  
  const subtotal = items.reduce((sum, item) => 
    sum + (item.quantity * item.price), 0
  );
  
  const tax = calculateTax(subtotal, shippingAddress);
  const shipping = calculateShipping(items, shippingAddress);
  
  return subtotal + tax + shipping;
}
```

### Python Docstrings (Google Style)

```python
def calculate_total(items: List[OrderItem], shipping_address: Address) -> int:
    """Calculate order total including tax and shipping.
    
    Args:
        items: Array of order items with quantity and price.
        shipping_address: Address for tax calculation.
    
    Returns:
        Total amount in USD cents.
    
    Raises:
        ValidationError: If items array is empty.
        TaxCalculationError: If tax lookup fails.
    
    Example:
        >>> items = [OrderItem(quantity=2, price=2999)]
        >>> address = Address(zip="94105", country="US")
        >>> total = calculate_total(items, address)
        >>> print(total)
        6398  # 5998 + 400 tax + 0 shipping
    """
    if not items:
        raise ValidationError("Items array cannot be empty")
    
    subtotal = sum(item.quantity * item.price for item in items)
    tax = calculate_tax(subtotal, shipping_address)
    shipping = calculate_shipping(items, shipping_address)
    
    return subtotal + tax + shipping
```

## README Structure

Every project should have a comprehensive README:

```markdown
# Project Name

One-line description of what this project does.

## Quick Start

```bash
npm install
npm run dev
```

Visit http://localhost:3000

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Installation

### Prerequisites
- Node.js 20+
- PostgreSQL 14+
- Redis (optional)

### Steps

1. Clone repository
```bash
git clone https://github.com/greyhaven/project.git
cd project
```

2. Install dependencies
```bash
npm install
```

3. Configure environment
```bash
cp .env.example .env
# Edit .env with your values
```

4. Run migrations
```bash
npm run migrate
```

5. Start development server
```bash
npm run dev
```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `REDIS_URL` | No | - | Redis connection string |
| `API_KEY` | Yes | - | API key for external service |

## Architecture

[Link to architecture docs or include Mermaid diagram]

## Development

### Running Tests
```bash
npm test
```

### Code Quality
```bash
npm run lint
npm run type-check
```

### Building
```bash
npm run build
```

## Deployment

[Link to deployment guide or include basic steps]

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE)
```

## Documentation Coverage

### Minimum Requirements

**Code Coverage**:
- Public functions: 100%
- Exported types: 100%
- API endpoints: 100%

**Content Coverage**:
- Every function has description
- Every parameter documented
- Return value documented
- Errors/exceptions documented
- At least one example

### Validation

Use automated tools:
- TypeScript: ts-morph for AST analysis
- Python: AST module for docstring coverage
- API: OpenAPI schema validation

```bash
# Check coverage
npm run docs:coverage

# Expected output
TypeScript: 87% (124/142 documented)
Python: 91% (98/108 documented)
API Endpoints: 95% (42/44 documented)
```

## Quality Checklist

Before publishing documentation:

- [ ] All code examples work (copy-paste tested)
- [ ] Links are valid (no 404s)
- [ ] Screenshots are current
- [ ] Version numbers are correct
- [ ] Prerequisite versions are accurate
- [ ] Examples use realistic data
- [ ] Error messages match actual errors
- [ ] Spelling and grammar checked
- [ ] Follows style guide
- [ ] Reviewed by another person

## Common Mistakes

### 1. Outdated Examples

❌ **Bad**: Uses deprecated API
```typescript
// This was removed in v2.0
const user = User.create({ email, password });
```

✅ **Good**: Current API with version note
```typescript
// As of v2.0, use createUser instead of User.create
const user = await createUser({ email, password });
```

### 2. Missing Error Handling

❌ **Bad**: Happy path only
```typescript
const user = await api.getUser(id);
console.log(user.email);
```

✅ **Good**: Error handling included
```typescript
try {
  const user = await api.getUser(id);
  console.log(user.email);
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    console.error(`User ${id} not found`);
  } else {
    throw error;
  }
}
```

### 3. Vague Instructions

❌ **Bad**: "Configure the database"

✅ **Good**: Specific steps
```markdown
1. Create database: `createdb myapp`
2. Run migrations: `npm run migrate`
3. Verify: `psql myapp -c "\dt"`
```

## Best Practices

1. **Update docs with code**: Documentation changes in same PR as code changes
2. **Link to code**: Reference specific files and line numbers
3. **Version everything**: Document which version each feature was added
4. **Test examples**: All code examples must be tested
5. **Screenshots with captions**: Always explain what image shows
6. **Consistent terminology**: Use same terms throughout
7. **Mobile-friendly**: Documentation should work on phones
8. **Search-optimized**: Use descriptive headings and keywords
9. **Accessible**: Alt text for images, semantic HTML
10. **Feedback loops**: Easy way for users to report doc issues

---

Related: [openapi-patterns.md](openapi-patterns.md) | [mermaid-diagrams.md](mermaid-diagrams.md) | [Return to INDEX](INDEX.md)
