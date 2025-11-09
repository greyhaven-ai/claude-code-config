# [METHOD] /api/v1/[resource]

[One sentence description of what this endpoint does]

## Authentication

**Required**: [Yes/No]
**Roles**: [Admin, Member, Guest] _(if applicable)_
**Scopes**: [read:resource, write:resource] _(if applicable)_

## Request

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | Bearer token: `Bearer <token>` |
| `Content-Type` | Yes | `application/json` |
| `X-Tenant-ID` | Yes | Tenant identifier _(if multi-tenant)_ |

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `[param_name]` | string | [Description] |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `[param_name]` | string | No | [default] | [Description] |
| `page` | integer | No | 1 | Page number (min: 1) |
| `per_page` | integer | No | 20 | Items per page (min: 1, max: 100) |

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `[field_name]` | string | Yes | [Description, validation rules] |
| `[field_name]` | integer | No | [Description, validation rules] |

**Example**:
```json
{
  "[field_name]": "value",
  "[field_name]": 123
}
```

## Response

### Success (200 OK)

```json
{
  "id": "res_1234567890abcdef",
  "[field_name]": "value",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Success (201 Created)

**Headers**:
- `Location: /api/v1/[resource]/res_1234567890abcdef`

```json
{
  "id": "res_1234567890abcdef",
  "[field_name]": "value",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Responses

| Code | Description | Example |
|------|-------------|---------|
| 400 | Bad Request - Validation failed | `{"error": "VALIDATION_ERROR", "message": "Field 'email' is invalid"}` |
| 401 | Unauthorized - Missing or invalid token | `{"error": "UNAUTHORIZED", "message": "Invalid or missing authentication token"}` |
| 403 | Forbidden - Insufficient permissions | `{"error": "FORBIDDEN", "message": "User lacks required role"}` |
| 404 | Not Found - Resource doesn't exist | `{"error": "NOT_FOUND", "message": "Resource with id 'xyz' not found"}` |
| 409 | Conflict - Resource already exists | `{"error": "CONFLICT", "message": "Resource with this identifier already exists"}` |
| 429 | Too Many Requests - Rate limit exceeded | `{"error": "RATE_LIMIT_EXCEEDED", "message": "Rate limit exceeded, retry after 60 seconds"}` |
| 500 | Internal Server Error | `{"error": "INTERNAL_ERROR", "message": "An unexpected error occurred"}` |

**Error Response Schema**:
```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "field": "field_name",
    "reason": "specific reason"
  }
}
```

## Rate Limiting

- **Authenticated**: [1000] requests per hour
- **Unauthenticated**: [100] requests per hour

**Response Headers**:
- `X-RateLimit-Limit`: Maximum requests per hour
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when limit resets

## Pagination

_(If endpoint returns paginated results)_

**Request**: Use `page` and `per_page` query parameters
**Response**: Includes `pagination` object

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 145,
    "total_pages": 8,
    "next_page": 2,
    "prev_page": null
  }
}
```

## Code Examples

### TypeScript

```typescript
const response = await fetch('https://api.greyhaven.com/[resource]', {
  method: '[METHOD]',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    [field_name]: 'value'
  })
});

if (!response.ok) {
  const error = await response.json();
  throw new Error(error.message);
}

const data = await response.json();
console.log('[Resource] created:', data.id);
```

### Python

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.[method](
        'https://api.greyhaven.com/[resource]',
        headers={'Authorization': f'Bearer {token}'},
        json={'[field_name]': 'value'}
    )
    response.raise_for_status()
    data = response.json()
    print(f'[Resource] created: {data["id"]}')
```

### cURL

```bash
curl -X [METHOD] https://api.greyhaven.com/[resource] \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "[field_name]": "value"
  }'
```

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2024-01-15 | Initial release |

---

[Return to API Reference](../README.md)
