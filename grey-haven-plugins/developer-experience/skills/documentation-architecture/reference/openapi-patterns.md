# OpenAPI 3.1 Patterns and Best Practices

Comprehensive guide to OpenAPI 3.1 specification patterns for Grey Haven stack (FastAPI + TanStack Start).

## OpenAPI 3.1 Overview

OpenAPI 3.1 is fully compatible with JSON Schema Draft 2020-12.

**Key Differences from 3.0**: Full JSON Schema compatibility, `examples` replaces `example`, `webhooks` support, better discriminator

## Basic Structure

```yaml
openapi: 3.1.0
info:
  title: Grey Haven API
  version: 1.0.0

servers:
  - url: https://api.greyhaven.com

paths:
  /users:
    get:
      operationId: listUsers
      tags: [users]
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

## Authentication

### JWT Bearer

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

### OAuth2

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.greyhaven.com/oauth/authorize
          tokenUrl: https://auth.greyhaven.com/oauth/token
          scopes:
            read:users: Read user data
```

### API Key

```yaml
components:
  securitySchemes:
    ApiKey:
      type: apiKey
      in: header
      name: X-API-Key
```

## Schema Patterns

### Pydantic v2 to OpenAPI

```python
from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
    id: str = Field(..., pattern="^usr_[a-z0-9]{16}$")
    email: str = Field(..., examples=["user@example.com"])
    role: Literal["admin", "member", "guest"] = "member"
```

Generates:

```yaml
User:
  type: object
  required: [id, email]
  properties:
    id:
      type: string
      pattern: ^usr_[a-z0-9]{16}$
    email:
      type: string
      examples: ["user@example.com"]
    role:
      type: string
      enum: [admin, member, guest]
      default: member
```

### Nullable and Optional

```yaml
# Optional (can be omitted)
username:
  type: string

# Nullable (can be null)
middle_name:
  type: [string, 'null']

# Both
nickname:
  type: [string, 'null']
```

### Discriminated Unions

```yaml
PaymentMethod:
  type: object
  required: [type]
  discriminator:
    propertyName: type
    mapping:
      card: '#/components/schemas/CardPayment'
      bank: '#/components/schemas/BankPayment'

CardPayment:
  allOf:
    - $ref: '#/components/schemas/PaymentMethod'
    - type: object
      properties:
        card_number:
          type: string
          pattern: ^\d{16}$
```

## Response Patterns

### Error Response

```yaml
ErrorResponse:
  type: object
  required: [error, message]
  properties:
    error:
      type: string
      examples: ["VALIDATION_ERROR"]
    message:
      type: string
    details:
      type: object
      additionalProperties: true

# Use in responses
responses:
  '400':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/ErrorResponse'
```

### Paginated Response

```yaml
PaginatedUsers:
  type: object
  properties:
    data:
      type: array
      items:
        $ref: '#/components/schemas/User'
    pagination:
      type: object
      properties:
        page:
          type: integer
          minimum: 1
        per_page:
          type: integer
          minimum: 1
          maximum: 100
        total:
          type: integer
        total_pages:
          type: integer
```

### Multiple Status Codes

```yaml
responses:
  '201':
    description: Created
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  '202':
    description: Accepted (async)
    content:
      application/json:
        schema:
          type: object
          properties:
            job_id:
              type: string
```

## Request Body

### Required vs Optional

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required: [email, password]  # Required
        properties:
          email:
            type: string
            format: email
          password:
            type: string
            minLength: 8
          name:
            type: string  # Optional
```

### File Upload

```yaml
requestBody:
  content:
    multipart/form-data:
      schema:
        properties:
          file:
            type: string
            format: binary
```

## Parameters

### Path

```yaml
parameters:
  - name: user_id
    in: path
    required: true
    schema:
      type: string
      pattern: ^usr_[a-z0-9]{16}$
```

### Query

```yaml
parameters:
  - name: status
    in: query
    schema:
      type: string
      enum: [pending, processing, shipped]
  - name: created_after
    in: query
    schema:
      type: string
      format: date-time
  - name: sort
    in: query
    schema:
      type: string
      enum: [created_at:asc, created_at:desc]
      default: created_at:desc
```

### Headers

```yaml
components:
  parameters:
    TenantId:
      name: X-Tenant-ID
      in: header
      required: true
      schema:
        type: string

paths:
  /orders:
    post:
      parameters:
        - $ref: '#/components/parameters/TenantId'
```

## Response Headers

```yaml
responses:
  '200':
    headers:
      X-RateLimit-Limit:
        schema:
          type: integer
      X-RateLimit-Remaining:
        schema:
          type: integer
      X-Request-ID:
        schema:
          type: string
          format: uuid
```

## Multi-Language Examples

```yaml
x-codeSamples:
  - lang: TypeScript
    source: |
      const response = await fetch("https://api.greyhaven.com/users", {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: JSON.stringify({ email, password })
      });
  
  - lang: Python
    source: |
      async with httpx.AsyncClient() as client:
          response = await client.post(
              "https://api.greyhaven.com/users",
              headers={"Authorization": f"Bearer {token}"},
              json={"email": email, "password": password}
          )
  
  - lang: Shell
    source: |
      curl -X POST https://api.greyhaven.com/users \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"email": "user@example.com"}'
```

## Webhooks (OpenAPI 3.1)

```yaml
webhooks:
  orderCreated:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [event, data]
              properties:
                event:
                  type: string
                  const: order.created
                data:
                  $ref: '#/components/schemas/Order'
      responses:
        '200':
          description: Received
```

## Best Practices

1. **Use $ref**: Define schemas once, reference everywhere
2. **Examples**: Realistic examples for all schemas
3. **Error Schemas**: Consistent error format
4. **Validation**: Use pattern, minLength, minimum
5. **Descriptions**: Document every field
6. **operationId**: Unique for SDK generation
7. **Tags**: Group related endpoints
8. **Deprecation**: Mark with `deprecated: true`
9. **Security**: Define at global or operation level
10. **Versioning**: Include in URL (/api/v1/)

## Common Patterns

### Multi-Tenant

```yaml
components:
  parameters:
    TenantId:
      name: X-Tenant-ID
      in: header
      required: true
      schema:
        type: string
```

### Idempotency

```yaml
components:
  parameters:
    IdempotencyKey:
      name: Idempotency-Key
      in: header
      schema:
        type: string
        format: uuid
```

### Rate Limiting

```yaml
responses:
  '429':
    description: Rate limit exceeded
    headers:
      X-RateLimit-Reset:
        schema:
          type: integer
```

## FastAPI Integration

```python
from fastapi import FastAPI

app = FastAPI(
    title="Grey Haven API",
    version="1.0.0",
    openapi_version="3.1.0"
)

# Customize OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

## Validation

Use @redocly/cli for validation:

```bash
npx @redocly/cli lint openapi.yaml
```

Common issues:
- Missing operationId
- Missing response descriptions
- Inconsistent naming
- Missing examples
- Invalid $ref paths

---

Related: [mermaid-diagrams.md](mermaid-diagrams.md) | [documentation-standards.md](documentation-standards.md) | [Return to INDEX](INDEX.md)
