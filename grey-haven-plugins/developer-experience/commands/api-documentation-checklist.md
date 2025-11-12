# API Documentation Checklist

**Use when generating comprehensive API documentation with OpenAPI specifications.**

## Phase 1: Preparation

- [ ] Identify all API endpoints to document
- [ ] Determine target audience (internal devs, external partners, public)
- [ ] Choose documentation format (OpenAPI 3.1, AsyncAPI 2.6)
- [ ] Select interactive documentation tool (Swagger UI, Redoc)
- [ ] Define coverage threshold (target 90%+, minimum 80%)
- [ ] Establish deployment strategy (Cloudflare Pages, GitHub Pages)

## Phase 2: Code Analysis

### TypeScript/JavaScript
- [ ] Locate all route definitions (Hono, NestJS, Express, tRPC)
- [ ] Extract route handlers and HTTP methods
- [ ] Parse TypeScript interfaces and types
- [ ] Extract JSDoc comments for descriptions
- [ ] Identify authentication middleware
- [ ] Locate request validation schemas
- [ ] Extract response type definitions

### Python
- [ ] Locate FastAPI/Flask route decorators
- [ ] Extract Pydantic response models
- [ ] Parse docstrings (Google, NumPy styles)
- [ ] Identify dependency injection
- [ ] Locate authentication dependencies
- [ ] Extract validation schemas
- [ ] Identify error response handlers

## Phase 3: OpenAPI Specification

### Info Section
- [ ] API title defined
- [ ] API description written (1-2 paragraphs)
- [ ] API version specified (semantic versioning)
- [ ] Contact information added (name, email, URL)
- [ ] License specified (MIT, Apache, etc.)
- [ ] Terms of service URL added (if applicable)

### Servers Section
- [ ] Production server URL defined
- [ ] Staging server URL defined (if applicable)
- [ ] Development server URL defined
- [ ] Server descriptions added
- [ ] Server variables defined (for templating)

### Paths Section
- [ ] All endpoints documented
- [ ] HTTP methods specified (GET, POST, PUT, DELETE, PATCH)
- [ ] Operation IDs unique across all paths
- [ ] Summaries concise (1 line)
- [ ] Descriptions comprehensive (1-3 paragraphs)
- [ ] Tags assigned for grouping
- [ ] Parameters documented (path, query, header, cookie)
- [ ] Request bodies defined with schemas
- [ ] Response codes documented (200, 400, 401, 403, 404, 429, 500)
- [ ] Security requirements specified
- [ ] Deprecation warnings added (if applicable)

### Components Section
- [ ] Reusable schemas defined
- [ ] Request schemas created
- [ ] Response schemas created
- [ ] Error schemas defined
- [ ] Pagination schemas defined
- [ ] Security schemes configured (Bearer, OAuth2, API keys)
- [ ] Parameters reused via $ref
- [ ] Response objects reused via $ref
- [ ] Examples included in schemas

### Security Section
- [ ] Security schemes defined in components
- [ ] Bearer JWT configuration (if applicable)
- [ ] OAuth2 flows defined (if applicable)
- [ ] API key locations specified (header, query, cookie)
- [ ] Security applied to endpoints globally or per-operation
- [ ] Scopes defined for OAuth2 (if applicable)

## Phase 4: Schema Definitions

### Schema Quality
- [ ] All fields have descriptions
- [ ] Required fields marked
- [ ] Data types specified (string, integer, boolean, array, object)
- [ ] String constraints (minLength, maxLength, pattern)
- [ ] Number constraints (minimum, maximum, multipleOf)
- [ ] Array constraints (minItems, maxItems, uniqueItems)
- [ ] Enum values defined (for status codes, roles, etc.)
- [ ] Format specified (email, uri, date-time, uuid)
- [ ] Examples provided for each schema
- [ ] Default values specified (where appropriate)
- [ ] ReadOnly/WriteOnly fields marked

### Nested Objects
- [ ] Nested schemas properly referenced
- [ ] Recursive schemas handled (if applicable)
- [ ] Polymorphic schemas defined (oneOf, anyOf, allOf)
- [ ] Discriminator specified (for polymorphic schemas)

## Phase 5: Examples and Code Snippets

### Request/Response Examples
- [ ] Example requests provided for each endpoint
- [ ] Example responses provided for success cases
- [ ] Example error responses provided
- [ ] Examples match schema definitions
- [ ] Examples use realistic data

### Multi-Language Code Snippets
- [ ] TypeScript/JavaScript examples generated
- [ ] Python examples generated
- [ ] cURL examples generated
- [ ] Code snippets tested and verified
- [ ] Authentication included in examples
- [ ] Error handling demonstrated

## Phase 6: Interactive Documentation

### Swagger UI Setup
- [ ] Swagger UI HTML generated
- [ ] Custom styling applied (Grey Haven branding)
- [ ] Try-it-out functionality enabled
- [ ] Authentication configuration added
- [ ] Search functionality enabled
- [ ] Dark mode support added
- [ ] Favicon and logo added

### Redoc Setup (Alternative)
- [ ] Redoc HTML generated
- [ ] Three-panel layout configured
- [ ] Custom theme applied
- [ ] Download as HTML enabled
- [ ] Search functionality tested

## Phase 7: Validation and Quality Checks

### OpenAPI Spec Validation
- [ ] Spec validated against OpenAPI 3.1 schema
- [ ] All $ref references resolved
- [ ] No validation errors
- [ ] No validation warnings (or documented exceptions)
- [ ] Run: `npx @redocly/cli lint docs/api/openapi.json`

### Coverage Analysis
- [ ] Coverage report generated
- [ ] Endpoint coverage ≥ 90% (or ≥ 80% minimum)
- [ ] Request schema coverage ≥ 90%
- [ ] Response schema coverage ≥ 90%
- [ ] Error response coverage ≥ 95%
- [ ] Code example coverage ≥ 80%
- [ ] Missing documentation identified
- [ ] Remediation plan created

### Code Example Testing
- [ ] Example test suite created
- [ ] TypeScript examples tested
- [ ] Python examples tested
- [ ] cURL examples tested
- [ ] All examples pass tests
- [ ] Examples updated when API changes

### Schema Consistency
- [ ] Generated schemas match source types
- [ ] TypeScript interfaces align with OpenAPI schemas
- [ ] Pydantic models align with OpenAPI schemas
- [ ] No drift between code and documentation

## Phase 8: Deployment

### Build Documentation Site
- [ ] Documentation site built successfully
- [ ] All assets included (CSS, JS, images)
- [ ] OpenAPI spec accessible at `/openapi.json`
- [ ] OpenAPI spec accessible at `/openapi.yaml`
- [ ] Swagger UI accessible at `/` or `/docs`
- [ ] Code examples accessible

### Cloudflare Pages Deployment
- [ ] Cloudflare project created
- [ ] Custom domain configured (docs.greyhaven.com)
- [ ] DNS records configured
- [ ] SSL/TLS enabled
- [ ] Deploy command tested: `wrangler pages deploy docs/build`
- [ ] Deployment successful
- [ ] Documentation accessible via URL
- [ ] Cache invalidation configured

### GitHub Actions CI/CD
- [ ] GitHub Actions workflow created
- [ ] Workflow triggers on code changes (src/**/*.ts, src/**/*.py)
- [ ] Dependencies installed (Node.js, bun)
- [ ] Documentation generated automatically
- [ ] OpenAPI spec validated in CI/CD
- [ ] Coverage threshold enforced (fail if < 80%)
- [ ] Deployment to Cloudflare Pages automated
- [ ] Secrets configured (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)
- [ ] Workflow tested with test commit

## Phase 9: Maintenance

### Continuous Updates
- [ ] Documentation regenerated on every merge to main
- [ ] Pre-commit hooks validate coverage (optional)
- [ ] Code reviews include documentation updates
- [ ] Breaking changes documented
- [ ] Migration guides created (for API versioning)

### Monitoring
- [ ] Documentation build failures monitored
- [ ] Coverage trend tracked over time
- [ ] User feedback collected (via GitHub Issues, feedback form)
- [ ] Analytics configured (page views, search queries)

### Versioning
- [ ] API versioned (v1, v2, etc.)
- [ ] Documentation versioned per API version
- [ ] Legacy versions accessible (for backward compatibility)
- [ ] Deprecation warnings added to old endpoints
- [ ] Sunset dates communicated (for deprecated endpoints)

## Phase 10: Documentation Quality

### Accuracy
- [ ] All endpoints tested and verified
- [ ] Code examples tested against live API
- [ ] Schemas match actual request/response data
- [ ] Error responses match actual behavior
- [ ] Authentication flows verified

### Completeness
- [ ] All endpoints documented
- [ ] All parameters documented
- [ ] All request schemas documented
- [ ] All response schemas documented
- [ ] All error codes documented
- [ ] Rate limiting documented
- [ ] Pagination documented
- [ ] Filtering/sorting documented

### Clarity
- [ ] Descriptions clear and concise
- [ ] Technical jargon explained
- [ ] Examples demonstrate common use cases
- [ ] Authentication flows explained step-by-step
- [ ] Error handling guidance provided

### Accessibility
- [ ] Documentation site is mobile-friendly
- [ ] WCAG 2.1 AA compliance (for public APIs)
- [ ] Keyboard navigation supported
- [ ] Screen reader compatible
- [ ] Sufficient color contrast

## Critical Validations

- [ ] OpenAPI spec passes validation (`npx @redocly/cli lint`)
- [ ] Documentation coverage ≥ 80% (target 90%+)
- [ ] All code examples tested and working
- [ ] Deployment successful and accessible
- [ ] CI/CD workflow passing
- [ ] No schema drift between code and docs
- [ ] Authentication flows documented and tested
- [ ] Error responses complete and accurate
- [ ] Versioning strategy defined
- [ ] Maintenance plan established

## Post-Implementation

### Testing
- [ ] Documentation site load tested
- [ ] Search functionality tested
- [ ] Try-it-out functionality tested (Swagger UI)
- [ ] Mobile responsiveness tested
- [ ] Cross-browser compatibility tested

### Performance
- [ ] Documentation site loads in < 3 seconds
- [ ] OpenAPI spec size optimized (< 5 MB)
- [ ] Images optimized
- [ ] Caching configured (Cloudflare)

### Security
- [ ] API keys not exposed in examples
- [ ] Sensitive data redacted
- [ ] Authentication documented securely
- [ ] Rate limiting documented
- [ ] CORS policies documented

### User Experience
- [ ] Navigation intuitive
- [ ] Search returns relevant results
- [ ] Code examples copy-able
- [ ] Feedback mechanism available
- [ ] Contact information visible
