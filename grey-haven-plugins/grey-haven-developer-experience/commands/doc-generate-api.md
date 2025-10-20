---
name: doc-generate-api
description: Generate comprehensive API documentation from TypeScript/Python codebases with OpenAPI 3.1 specifications, interactive documentation, and multi-language code examples
---

# API Documentation Generator

Automatically generate comprehensive, production-ready API documentation from your TypeScript or Python codebase.

## What This Command Does

Analyzes your codebase to extract API routes, request/response schemas, and type definitions, then generates:
- **OpenAPI 3.1 Specification** - Complete API contract with schemas, endpoints, and examples
- **Interactive Documentation** - Swagger UI or Redoc with try-it-now functionality
- **Multi-Language Examples** - Code snippets in TypeScript, Python, JavaScript, cURL
- **Developer Portal** - Comprehensive documentation site with guides and reference
- **Coverage Report** - Analysis of documentation completeness

## When to Use This

- **After implementing new API endpoints** - Generate docs automatically
- **Before releasing API changes** - Ensure comprehensive documentation
- **For external API consumers** - Provide professional developer experience
- **During code reviews** - Validate API design and documentation
- **For API versioning** - Document changes and migration paths

## Supported Frameworks

### TypeScript
- **NestJS** - Decorator-based routing (`@Get`, `@Post`, etc.)
- **Hono** (Cloudflare Workers) - Route definitions
- **Express** - Route handlers
- **tRPC** - Type-safe procedure definitions

### Python
- **FastAPI** - Automatic OpenAPI generation enhancement
- **Flask** - Route decorator extraction
- **Django REST Framework** - ViewSet and APIView documentation

## Usage

```bash
/doc-generate-api [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Output format: `openapi`, `asyncapi`, `graphql` | `openapi` |
| `--version` | OpenAPI version: `3.0`, `3.1` | `3.1` |
| `--output` | Output directory | `docs/api` |
| `--interactive` | Generate interactive docs (Swagger UI / Redoc) | `true` |
| `--examples` | Include code examples | `true` |
| `--deploy` | Deploy to platform: `cloudflare-pages`, `github-pages`, `none` | `none` |
| `--validate` | Validate generated spec | `true` |
| `--coverage` | Generate coverage report | `true` |

### Examples

**Generate OpenAPI spec with Swagger UI:**
```bash
/doc-generate-api --format openapi --interactive true
```

**Generate and deploy to Cloudflare Pages:**
```bash
/doc-generate-api --deploy cloudflare-pages
```

**Generate AsyncAPI for event-driven APIs:**
```bash
/doc-generate-api --format asyncapi --output docs/events
```

**Generate with coverage report:**
```bash
/doc-generate-api --coverage true --validate true
```

## Process Flow

### Phase 1: Code Analysis
1. **Scan Codebase** - Find API route definitions using Glob
2. **Extract Routes** - Parse decorators, handlers, and route definitions
3. **Analyze Types** - Extract TypeScript interfaces or Pydantic models
4. **Parse Documentation** - Read JSDoc/docstrings for descriptions

### Phase 2: Specification Generation
5. **Build OpenAPI Schema** - Create complete OpenAPI 3.1 specification
6. **Add Examples** - Generate request/response examples from types
7. **Document Authentication** - Extract auth requirements
8. **Add Error Schemas** - Document error responses

### Phase 3: Enhancement
9. **Generate Code Examples** - Multi-language snippets for each endpoint
10. **Create Interactive Docs** - Set up Swagger UI or Redoc
11. **Validate Specification** - Check OpenAPI schema validity
12. **Calculate Coverage** - Analyze documentation completeness

### Phase 4: Deployment (Optional)
13. **Build Documentation Site** - Compile all documentation
14. **Deploy to Platform** - Push to Cloudflare Pages or GitHub Pages
15. **Update CI/CD** - Configure automated regeneration

## Output Structure

```
docs/api/
├── openapi.json                 # OpenAPI 3.1 specification
├── openapi.yaml                 # YAML version (easier to read)
├── index.html                   # Interactive documentation (Swagger UI)
├── coverage-report.md           # Documentation coverage analysis
├── examples/
│   ├── typescript/              # TypeScript code examples
│   │   ├── users.ts
│   │   └── auth.ts
│   ├── python/                  # Python code examples
│   │   ├── users.py
│   │   └── auth.py
│   └── curl/                    # cURL examples
│       ├── users.sh
│       └── auth.sh
└── schemas/                     # JSON Schema files
    ├── User.json
    ├── Order.json
    └── errors.json
```

## OpenAPI Specification Features

### Complete Endpoint Documentation

```yaml
paths:
  /users:
    get:
      summary: List all users
      description: |
        Retrieve a paginated list of users with optional filtering.

        **Rate Limit**: 100 requests per minute
      operationId: listUsers
      tags:
        - Users
      security:
        - bearerAuth: []
      parameters:
        - name: page
          in: query
          description: Page number for pagination
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: filter
          in: query
          description: Filter users by email or name
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
              examples:
                default:
                  value:
                    data:
                      - id: "usr_123"
                        email: "john@example.com"
                        name: "John Doe"
                        createdAt: "2025-01-15T10:30:00Z"
                    pagination:
                      page: 1
                      limit: 20
                      total: 150
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimitExceeded'
```

### Schema Definitions

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          description: Unique user identifier
          example: "usr_123abc"
        email:
          type: string
          format: email
          description: User's email address
          example: "john@example.com"
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: User's full name
          example: "John Doe"
        role:
          type: string
          enum: [admin, user, guest]
          description: User's role in the system
          default: user
        createdAt:
          type: string
          format: date-time
          description: Account creation timestamp
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          description: Last update timestamp
          readOnly: true

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
      properties:
        page:
          type: integer
          minimum: 1
        limit:
          type: integer
          minimum: 1
          maximum: 100
        total:
          type: integer
          minimum: 0
        hasMore:
          type: boolean

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Error code for programmatic handling
          example: "VALIDATION_ERROR"
        message:
          type: string
          description: Human-readable error message
          example: "Invalid email format"
        field:
          type: string
          description: Field that caused the error (for validation errors)
          example: "email"
        details:
          type: object
          description: Additional error context
          additionalProperties: true

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token obtained from `/auth/login` endpoint.

        Format: `Authorization: Bearer <token>`
```

## Multi-Language Code Examples

### TypeScript Example

```typescript
import { GreyHavenClient } from '@grey-haven/sdk';

const client = new GreyHavenClient({
  apiKey: process.env.GREY_HAVEN_API_KEY,
  baseUrl: 'https://api.greyhaven.com'
});

// List users with pagination
const response = await client.users.list({
  page: 1,
  limit: 20,
  filter: 'john'
});

console.log(response.data); // User[]
console.log(response.pagination.total); // Total count
```

### Python Example

```python
from grey_haven import Client
import os

client = Client(
    api_key=os.getenv('GREY_HAVEN_API_KEY'),
    base_url='https://api.greyhaven.com'
)

# List users with pagination
response = client.users.list(
    page=1,
    limit=20,
    filter='john'
)

print(response.data)  # List[User]
print(response.pagination.total)  # Total count
```

### JavaScript (Fetch API)

```javascript
const response = await fetch('https://api.greyhaven.com/users?page=1&limit=20', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${process.env.GREY_HAVEN_API_KEY}`,
    'Content-Type': 'application/json'
  }
});

if (!response.ok) {
  throw new Error(`HTTP error! status: ${response.status}`);
}

const { data, pagination } = await response.json();
console.log(data); // Array of users
```

### cURL Example

```bash
curl -X GET 'https://api.greyhaven.com/users?page=1&limit=20' \
  -H "Authorization: Bearer ${GREY_HAVEN_API_KEY}" \
  -H "Content-Type: application/json"
```

## Documentation Coverage Report

The command generates a comprehensive coverage report:

```markdown
# API Documentation Coverage Report

**Generated**: 2025-01-17 14:30:00 UTC
**Overall Coverage**: 87.3%

## Summary

| Metric | Count | Documented | Coverage |
|--------|-------|------------|----------|
| **Endpoints** | 42 | 38 | 90.5% |
| **Request Schemas** | 35 | 31 | 88.6% |
| **Response Schemas** | 42 | 35 | 83.3% |
| **Error Responses** | 42 | 40 | 95.2% |
| **Code Examples** | 42 | 30 | 71.4% |

## Missing Documentation

### Endpoints Without Examples (12)
- `POST /orders/{id}/refund` - Missing code examples
- `PUT /users/{id}/preferences` - Missing code examples
- `GET /analytics/reports` - Missing code examples

### Incomplete Request Schemas (4)
- `POST /orders` - Request body schema incomplete
- `PATCH /users/{id}` - Missing field descriptions

### Incomplete Response Schemas (7)
- `GET /orders/{id}/items` - Missing example responses
- `POST /payments/webhook` - Missing webhook payload schema

## Recommendations

1. **Add code examples** for the 12 endpoints missing them
2. **Complete request schemas** for POST /orders and PATCH /users/{id}
3. **Add response examples** for order and payment endpoints
4. **Document webhook payloads** with AsyncAPI specification

## Next Steps

Run `/doc-generate-api --fix-gaps` to automatically generate missing documentation.
```

## Interactive Documentation

### Swagger UI Features

The generated Swagger UI includes:
- **Try It Out** - Test endpoints directly from documentation
- **Model Schema** - Interactive schema exploration
- **Response Examples** - Real response previews
- **Authentication** - Integrated auth token management
- **Search** - Full-text search across all endpoints
- **Dark Mode** - Accessibility and eye comfort

### Redoc Features

Alternative to Swagger UI with:
- **Three-Panel Layout** - Menu, content, code examples
- **Responsive Design** - Mobile-friendly documentation
- **Search** - Advanced search with filtering
- **Export** - Download as HTML for offline use
- **Custom Branding** - Grey Haven styling

## Deployment Integration

### Cloudflare Pages Deployment

```yaml
# wrangler.toml
name = "grey-haven-docs"
pages_build_output_dir = "docs/build"

[env.production]
routes = [
  { pattern = "docs.greyhaven.com", zone_name = "greyhaven.com" }
]
```

**Deployment Command:**
```bash
wrangler pages deploy docs/build --project-name grey-haven-docs
```

### GitHub Actions CI/CD

```yaml
name: Generate API Documentation

on:
  push:
    branches: [main]
    paths:
      - 'src/**/*.ts'
      - 'src/**/*.py'
      - 'packages/**/src/**'

jobs:
  generate-docs:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: pnpm install

      - name: Generate API documentation
        run: pnpm run doc:generate-api

      - name: Validate OpenAPI spec
        run: |
          npx @redocly/cli lint docs/api/openapi.json

      - name: Check coverage threshold
        run: |
          COVERAGE=$(node scripts/check-doc-coverage.js)
          if [ "$COVERAGE" -lt 80 ]; then
            echo "Documentation coverage $COVERAGE% below 80% threshold"
            exit 1
          fi

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: grey-haven-docs
          directory: docs/build
```

## Validation and Quality Checks

### OpenAPI Spec Validation

Validates the generated specification against OpenAPI 3.1 schema:

```bash
npx @redocly/cli lint docs/api/openapi.json
```

**Checks:**
- Schema structure validity
- Required fields present
- Valid HTTP methods
- Proper $ref references
- Example conformance to schemas
- Security scheme definitions

### Code Example Testing

Automatically tests generated code examples:

```typescript
// tests/api-examples.test.ts
import { runExample } from './utils/example-runner';

describe('API Documentation Examples', () => {
  it('TypeScript user list example works', async () => {
    const result = await runExample('typescript/users.ts');
    expect(result).toBeDefined();
    expect(result.data).toBeArray();
  });

  it('Python user list example works', async () => {
    const result = await runExample('python/users.py');
    expect(result).toBeDefined();
  });
});
```

### Schema Consistency Check

Ensures request/response schemas match actual TypeScript/Pydantic definitions:

```typescript
// Compares generated OpenAPI schemas with source type definitions
const schemaValidator = new SchemaConsistencyChecker();
const inconsistencies = schemaValidator.check({
  openApiSpec: 'docs/api/openapi.json',
  sourceFiles: 'src/**/*.ts'
});

if (inconsistencies.length > 0) {
  console.error('Schema inconsistencies found:', inconsistencies);
  process.exit(1);
}
```

## Customization

### Custom Templates

Override default templates for code examples:

```typescript
// templates/typescript-example.hbs
import { GreyHavenClient } from '@grey-haven/sdk';

const client = new GreyHavenClient({
  apiKey: process.env.GREY_HAVEN_API_KEY
});

{{#each operations}}
// {{summary}}
const {{operationId}}Result = await client.{{tag}}.{{operationId}}({{#if parameters}}{
  {{#each parameters}}
  {{name}}: {{example}}{{#unless @last}},{{/unless}}
  {{/each}}
}{{/if}});
{{/each}}
```

### Custom Styling (Swagger UI)

```css
/* docs/api/custom.css */
.swagger-ui .topbar {
  background-color: #1a1a2e;
}

.swagger-ui .info .title {
  color: #16213e;
  font-family: 'Inter', sans-serif;
}
```

### Custom Configuration

```json
// docs/api/config.json
{
  "title": "Grey Haven API Documentation",
  "description": "Production API for Grey Haven services",
  "version": "1.0.0",
  "servers": [
    {
      "url": "https://api.greyhaven.com",
      "description": "Production"
    },
    {
      "url": "https://staging-api.greyhaven.com",
      "description": "Staging"
    },
    {
      "url": "http://localhost:8787",
      "description": "Local Development"
    }
  ],
  "contact": {
    "name": "Grey Haven API Support",
    "email": "api@greyhaven.com",
    "url": "https://docs.greyhaven.com/support"
  },
  "license": {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT"
  }
}
```

## Best Practices

### 1. Keep Documentation In Sync
- Run documentation generation on every merge to main
- Add pre-commit hooks to validate coverage
- Include documentation updates in code reviews

### 2. Maintain High Coverage
- Target 90%+ endpoint documentation
- Require examples for all public APIs
- Document all error responses

### 3. Version Your APIs
- Use semantic versioning (1.0.0, 2.0.0)
- Document breaking changes
- Provide migration guides

### 4. Test Your Examples
- Run automated tests on code examples
- Verify examples against live API
- Update examples when API changes

### 5. Make It Interactive
- Enable try-it-now functionality
- Provide sandbox environment
- Include realistic example data

## Troubleshooting

### Issue: Generated spec has validation errors

**Solution:**
```bash
# Validate spec and see specific errors
npx @redocly/cli lint docs/api/openapi.json --format=stylish

# Fix common issues automatically
npx @redocly/cli lint docs/api/openapi.json --fix
```

### Issue: Missing route definitions

**Cause**: Route decorators not recognized

**Solution:**
- Check that decorators match expected patterns (`@Get`, `@Post`, etc.)
- Verify TypeScript compilation settings
- Ensure Pydantic models are properly imported

### Issue: Code examples don't work

**Cause**: Examples not tested or outdated

**Solution:**
```bash
# Run example tests
npm run test:api-examples

# Regenerate examples with current API
/doc-generate-api --examples true --force
```

### Issue: Deployment fails

**Cause**: Missing environment variables or permissions

**Solution:**
```bash
# Verify Cloudflare credentials
echo $CLOUDFLARE_API_TOKEN
echo $CLOUDFLARE_ACCOUNT_ID

# Test local build
npm run build:docs
wrangler pages deploy docs/build --dry-run
```

## Related Commands

- `/doc-coverage` - Check documentation coverage without generating docs
- `/doc-validate` - Validate existing OpenAPI specification
- `/doc-deploy` - Deploy documentation without regenerating
- `/refactor-clarity` - Improve code clarity for better documentation extraction

## Agent Coordination

This command works with:
- **docs-architect** - Reviews and enhances generated documentation
- **api-documenter** - Quick updates to existing API docs
- **code-quality-analyzer** - Ensures code is well-documented
- **tdd-orchestrator** - Uses API contracts for test generation

---

**Pro Tip**: Run this command after implementing new endpoints, then share the generated Swagger UI link with your frontend team. They can start integration immediately with interactive documentation and code examples.
