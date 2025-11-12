---
name: doc-generate-api
description: Generate comprehensive API documentation from TypeScript/Python codebases with OpenAPI 3.1 specifications, interactive documentation, and multi-language code examples
---

# API Documentation Generator

Automatically generate production-ready API documentation from your TypeScript or Python codebase with OpenAPI 3.1 specifications, interactive Swagger UI, and multi-language code examples.

## What This Command Does

Analyzes your codebase to extract API routes, schemas, and types, then generates:
- **OpenAPI 3.1 Specification** - Complete API contract with schemas and examples
- **Interactive Documentation** - Swagger UI or Redoc with try-it-now functionality
- **Multi-Language Examples** - Code snippets in TypeScript, Python, JavaScript, cURL
- **Coverage Report** - Analysis of documentation completeness

## When to Use

- After implementing new API endpoints
- Before releasing API changes to external consumers
- During code reviews to validate API design
- For API versioning and migration documentation
- Setting up CI/CD documentation pipelines

## Quick Start

```bash
# Generate OpenAPI spec with Swagger UI
/doc-generate-api --format openapi --interactive true

# Generate and deploy to Cloudflare Pages
/doc-generate-api --deploy cloudflare-pages

# Generate with coverage report
/doc-generate-api --coverage true --validate true
```

## Supported Frameworks

**TypeScript**:
- Hono (Cloudflare Workers) - Primary Grey Haven stack
- NestJS - Decorator-based routing
- tRPC - Type-safe procedures

**Python**:
- FastAPI - Automatic OpenAPI generation enhancement
- Flask - Route decorator extraction

## Core Capabilities

### 1. Code Analysis and Extraction

**For TypeScript (Hono/TanStack Start)**:
```typescript
// Extracts from routes like this:
app.get('/users', async (c) => {
  const users = await db.query.users.findMany();
  return c.json({ data: users });
});
```

**For Python (FastAPI)**:
```python
# Extracts from routes like this:
@router.get("/users", response_model=List[UserSchema])
async def list_users():
    users = await db.query(User).all()
    return users
```

**Process**:
1. Scan codebase for route definitions (Glob for route files)
2. Extract route handlers and decorators
3. Analyze TypeScript interfaces or Pydantic models
4. Parse JSDoc/docstrings for descriptions
5. Build complete OpenAPI 3.1 specification

### 2. OpenAPI 3.1 Specification Generation

Complete specification with:
- **Paths**: All endpoints with parameters, request bodies, responses
- **Schemas**: Component schemas from TypeScript types or Pydantic models
- **Security**: Authentication schemes (Bearer, OAuth2, API keys)
- **Examples**: Request/response examples for each endpoint
- **Error Responses**: Standard error schemas (400, 401, 403, 404, 429, 500)

**Key Pattern** (Generated OpenAPI Structure):
```yaml
paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags: [Users]
      security:
        - bearerAuth: []
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
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
```

### 3. Multi-Language Code Examples

Generates code snippets for each endpoint:

**TypeScript/JavaScript**:
```typescript
const response = await fetch('https://api.greyhaven.com/users?page=1', {
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  }
});
const { data } = await response.json();
```

**Python**:
```python
response = requests.get(
    'https://api.greyhaven.com/users',
    params={'page': 1},
    headers={'Authorization': f'Bearer {API_KEY}'}
)
users = response.json()['data']
```

**cURL**:
```bash
curl -X GET 'https://api.greyhaven.com/users?page=1' \
  -H "Authorization: Bearer ${API_KEY}"
```

### 4. Interactive Documentation

**Swagger UI Features**:
- Try-it-out functionality for testing endpoints
- Interactive schema exploration
- Authentication token management
- Full-text search across endpoints
- Dark mode support

**Generated Structure**:
```
docs/api/
├── openapi.json          # OpenAPI 3.1 spec (JSON)
├── openapi.yaml          # OpenAPI 3.1 spec (YAML)
├── index.html            # Swagger UI
├── coverage-report.md    # Coverage analysis
├── examples/
│   ├── typescript/       # TS code examples
│   ├── python/           # Python examples
│   └── curl/             # cURL examples
└── schemas/              # JSON Schema files
```

### 5. Documentation Coverage Analysis

Generates comprehensive coverage report:

```markdown
# API Documentation Coverage Report

**Overall Coverage**: 87.3%

| Metric | Count | Documented | Coverage |
|--------|-------|------------|----------|
| Endpoints | 42 | 38 | 90.5% |
| Request Schemas | 35 | 31 | 88.6% |
| Response Schemas | 42 | 35 | 83.3% |
| Error Responses | 42 | 40 | 95.2% |
| Code Examples | 42 | 30 | 71.4% |

## Missing Documentation
- POST /orders/{id}/refund - Missing code examples
- PUT /users/{id}/preferences - Missing field descriptions
```

**Coverage Thresholds**:
- Target: 90%+ endpoint documentation
- Minimum: 80% for CI/CD pass
- Fail builds if coverage drops below threshold

### 6. Validation and Quality Checks

**OpenAPI Spec Validation**:
```bash
npx @redocly/cli lint docs/api/openapi.json
```

**Validates**:
- Schema structure validity
- Required fields present
- Valid HTTP methods and status codes
- Proper $ref references
- Example conformance to schemas
- Security scheme definitions

**Code Example Testing**:
```typescript
describe('API Documentation Examples', () => {
  it('TypeScript user list example works', async () => {
    const result = await runExample('typescript/users.ts');
    expect(result.data).toBeArray();
  });
});
```

### 7. Deployment Integration

**Cloudflare Pages Deployment**:
```bash
# Deploy documentation
wrangler pages deploy docs/build --project-name grey-haven-docs
```

**GitHub Actions CI/CD**:
```yaml
name: Generate API Documentation

on:
  push:
    branches: [main]
    paths:
      - 'src/**/*.ts'
      - 'src/**/*.py'

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: bun install
      - run: bun run doc:generate-api
      - run: npx @redocly/cli lint docs/api/openapi.json

      # Check coverage threshold
      - name: Check coverage
        run: |
          COVERAGE=$(node scripts/check-doc-coverage.js)
          if [ "$COVERAGE" -lt 80 ]; then
            echo "Coverage $COVERAGE% below 80% threshold"
            exit 1
          fi

      # Deploy to Cloudflare Pages
      - uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          projectName: grey-haven-docs
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Output format: `openapi`, `asyncapi` | `openapi` |
| `--version` | OpenAPI version: `3.0`, `3.1` | `3.1` |
| `--output` | Output directory | `docs/api` |
| `--interactive` | Generate Swagger UI / Redoc | `true` |
| `--examples` | Include code examples | `true` |
| `--deploy` | Deploy to: `cloudflare-pages`, `none` | `none` |
| `--validate` | Validate generated spec | `true` |
| `--coverage` | Generate coverage report | `true` |

## Best Practices

1. **Keep Documentation In Sync**
   - Run generation on every merge to main
   - Add pre-commit hooks to validate coverage
   - Include documentation updates in code reviews

2. **Maintain High Coverage**
   - Target 90%+ endpoint documentation
   - Require examples for all public APIs
   - Document all error responses

3. **Version Your APIs**
   - Use semantic versioning (1.0.0, 2.0.0)
   - Document breaking changes
   - Provide migration guides

4. **Test Your Examples**
   - Run automated tests on code examples
   - Verify examples against live API
   - Update examples when API changes

## Troubleshooting

**Issue: Generated spec has validation errors**
```bash
# Validate and see specific errors
npx @redocly/cli lint docs/api/openapi.json --format=stylish

# Fix common issues automatically
npx @redocly/cli lint docs/api/openapi.json --fix
```

**Issue: Missing route definitions**
- Check decorators match expected patterns
- Verify TypeScript compilation settings
- Ensure Pydantic models are properly imported

**Issue: Code examples don't work**
```bash
# Run example tests
bun test:api-examples

# Regenerate examples
/doc-generate-api --examples true --force
```

## Agent Coordination

Works with:
- **docs-architect** - Reviews and enhances generated documentation
- **code-quality-analyzer** - Ensures code is well-documented
- **tdd-orchestrator** - Uses API contracts for test generation

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete generation examples
  - [typescript-route-extraction.md](examples/typescript-route-extraction.md) - Extract from Hono/TanStack routes
  - [python-fastapi-extraction.md](examples/python-fastapi-extraction.md) - Extract from FastAPI
  - [openapi-output-example.md](examples/openapi-output-example.md) - Complete OpenAPI spec example
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Configuration and patterns
  - [openapi-3-1-patterns.md](reference/openapi-3-1-patterns.md) - OpenAPI 3.1 specification patterns
  - [schema-patterns.md](reference/schema-patterns.md) - Common schema patterns
  - [deployment-configs.md](reference/deployment-configs.md) - Deployment configuration
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [openapi-spec-template.yaml](templates/openapi-spec-template.yaml) - Base OpenAPI template
  - [code-example-templates.md](templates/code-example-templates.md) - Multi-language templates

- **[checklists/](checklists/)** - Documentation checklists
  - [api-documentation-checklist.md](checklists/api-documentation-checklist.md) - Complete checklist

---

**Pro Tip**: Run this command after implementing new endpoints, then share the generated Swagger UI link with your team. They can start integration immediately with interactive documentation and code examples.
