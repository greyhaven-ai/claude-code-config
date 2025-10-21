---
name: doc-coverage
description: Validate documentation coverage across codebase, identify gaps, and generate comprehensive coverage reports with actionable recommendations
---
# Documentation Coverage Validator
Analyze documentation completeness across your codebase and generate actionable coverage reports.
## What This Command Does
Scans your entire codebase to:
- **Calculate Coverage Percentages** - Function, class, API endpoint, and type documentation
- **Identify Missing Documentation** - Specific locations of undocumented code
- **Generate Gap Reports** - Prioritized list of documentation improvements needed
- **Track Coverage Trends** - Historical coverage data and trending
- **Enforce Coverage Thresholds** - CI/CD integration for quality gates
- **Provide Actionable Recommendations** - Specific fixes to improve coverage
## When to Use This
- **Before code reviews** - Ensure new code is properly documented
- **Pre-release validation** - Verify documentation quality before shipping
- **During refactoring** - Update documentation alongside code changes
- **CI/CD pipeline checks** - Automated coverage enforcement
- **Quarterly documentation audits** - Identify and fix documentation debt
- **Onboarding preparation** - Ensure new team members have adequate docs
## Usage
```bash
/doc-coverage [options]
```
### Options
| Option | Description | Default |
|--------|-------------|---------|
| `--threshold` | Minimum coverage percentage (0-100) | `80` |
| `--fail-below` | Exit with error if below threshold | `false` |
| `--format` | Output format: `markdown`, `json`, `html`, `console` | `markdown` |
| `--output` | Output file path | `docs/coverage-report.md` |
| `--scope` | Scope: `all`, `api`, `functions`, `types` | `all` |
| `--ignore` | Patterns to ignore (glob) | `[]` |
| `--trend` | Include historical trend analysis | `false` |
| `--fix-suggestions` | Generate auto-fix suggestions | `true` |
### Examples
**Basic coverage check:**
```bash
/doc-coverage
```
**CI/CD enforcement (fail if < 80%):**
```bash
/doc-coverage --threshold 80 --fail-below true
```
**API-only coverage:**
```bash
/doc-coverage --scope api --format html
```
**With historical trends:**
```bash
/doc-coverage --trend true --output docs/coverage-trend.md
```
**Ignore test files:**
```bash
/doc-coverage --ignore "**/*.test.ts" --ignore "**/*.spec.py"
```
## Coverage Metrics
### 1. Function/Method Coverage
Percentage of functions with complete documentation:
```typescript
// SUCCESS: DOCUMENTED (100%)
/**
 * Retrieve a user by ID
 * @param userId - Unique user identifier
 * @returns User object or null if not found
 * @throws {NotFoundError} When user doesn't exist
 */
async function getUserById(userId: string): Promise<User | null> {
 // ...
}
// ERROR: UNDOCUMENTED (0%)
async function updateUserPreferences(userId: string, prefs: any) {
 // Missing JSDoc
}
// WARNING: PARTIAL (50%)
/**
 * Calculate order total
 */
function calculateTotal(items: OrderItem[]) {
 // Missing @param, @returns
}
```
**Coverage Calculation:**
```
Function Coverage = (Documented Functions / Total Functions) × 100
```
### 2. Class/Interface Coverage
Percentage of classes/interfaces with documentation:
```python
# DOCUMENTED
class UserService:
 """
 Service for user management operations.
 Handles user CRUD operations, authentication, and profile management.
 Attributes:
 db: Database connection
 cache: Redis cache instance
 Example:
 >>> service = UserService(db, cache)
 >>> user = service.get_user('usr_123')
 """
# UNDOCUMENTED
class OrderProcessor:
# No docstring
```
### 3. API Endpoint Coverage
Percentage of API endpoints with complete documentation:
**Required for 100% coverage:**
- Endpoint path and method
- Request parameters (path, query, body)
- Response schema
- Error responses (4xx, 5xx)
- Authentication requirements
- Code example (at least one language)
```typescript
// SUCCESS: FULLY DOCUMENTED (100%)
/**
 * List all users with pagination
 *
 * @route GET /users
 * @param page - Page number (default: 1)
 * @param limit - Items per page (default: 20, max: 100)
 * @returns Paginated list of users
 * @throws {401} Unauthorized - Missing or invalid token
 * @throws {429} Rate limit exceeded
 *
 * @example
 * const response = await client.users.list({ page: 1, limit: 20 });
 */
@Get('/users')
@UseGuards(AuthGuard)
async listUsers(@Query() query: ListUsersDto) {
 // ...
}
// ERROR: UNDOCUMENTED (0%)
@Post('/users/:id/preferences')
async updatePreferences(@Param('id') id: string, @Body() body: any) {
 // No documentation
}
```
### 4. Type Documentation Coverage
Percentage of types/interfaces with field descriptions:
```typescript
// SUCCESS: FULLY DOCUMENTED (100%)
/**
 * User account information
 */
interface User {
 /** Unique user identifier */
 id: string;
 /** User's email address */
 email: string;
 /** User's full name */
 name: string;
 /** Account role */
 role: 'admin' | 'user' | 'guest';
 /** Account creation timestamp */
 createdAt: Date;
}
// WARNING: PARTIAL (40% - 2/5 fields documented)
interface Order {
 /** Order ID */
 id: string;
 /** Customer ID */
 customerId: string;
 items: OrderItem[]; // Missing description
 total: number; // Missing description
 status: OrderStatus; // Missing description
}
// ERROR: UNDOCUMENTED (0%)
interface PaymentMethod {
 type: string;
 last4: string;
 expiryMonth: number;
 expiryYear: number;
}
```
### 5. Example Coverage
Percentage of public APIs with code examples:
**Required:**
- At least one working code example per public function/endpoint
- Examples should demonstrate realistic usage
- Examples should be tested and verified
## Coverage Report Format
### Console Output
```
╔══════════════════════════════════════════════════════════╗
║ DOCUMENTATION COVERAGE REPORT ║
╚══════════════════════════════════════════════════════════╝
Overall Coverage: 87.3% SUCCESS: (Target: 80%)
┌─────────────────────────┬───────┬─────────────┬──────────┐
│ Category │ Total │ Documented │ Coverage │
├─────────────────────────┼───────┼─────────────┼──────────┤
│ Functions │ 342 │ 312 │ 91.2% SUCCESS: │
│ Classes │ 54 │ 48 │ 88.9% SUCCESS: │
│ API Endpoints │ 42 │ 38 │ 90.5% SUCCESS: │
│ Types/Interfaces │ 127 │ 98 │ 77.2% WARNING: │
│ Code Examples │ 42 │ 30 │ 71.4% ERROR: │
└─────────────────────────┴───────┴─────────────┴──────────┘
Coverage by Module:
 SUCCESS: src/auth/ 95.2%
 SUCCESS: src/users/ 91.7%
 WARNING: src/orders/ 78.1%
 ERROR: src/payments/ 65.4%
Critical Gaps: 12 items require immediate attention
```
### Markdown Report
```markdown
# Documentation Coverage Report
**Generated**: 2025-01-17 14:30:00 UTC
**Overall Coverage**: 87.3% SUCCESS:
**Threshold**: 80%
**Status**: PASS
## Summary
| Category | Total | Documented | Coverage | Status |
|----------|-------|------------|----------|--------|
| **Functions** | 342 | 312 | 91.2% | SUCCESS: |
| **Classes** | 54 | 48 | 88.9% | SUCCESS: |
| **API Endpoints** | 42 | 38 | 90.5% | SUCCESS: |
| **Types/Interfaces** | 127 | 98 | 77.2% | WARNING: |
| **Code Examples** | 42 | 30 | 71.4% | ERROR: |
## Coverage by Module
### src/auth/ (95.2%)
- Functions: 24/25 (96.0%)
- Classes: 4/4 (100%)
- API Endpoints: 6/6 (100%)
- Types: 12/13 (92.3%)
### src/users/ (91.7%)
- Functions: 45/48 (93.8%)
- Classes: 8/8 (100%)
- API Endpoints: 12/12 (100%)
- Types: 23/26 (88.5%)
### src/orders/ (78.1%)
- Functions: 67/78 (85.9%)
- Classes: 6/8 (75.0%)
- API Endpoints: 10/12 (83.3%)
- Types: 18/28 (64.3%)
### src/payments/ (65.4%)
- Functions: 32/54 (59.3%)
- Classes: 4/8 (50.0%)
- API Endpoints: 8/10 (80.0%)
- Types: 14/25 (56.0%)
## Critical Gaps (12)
### Missing Function Documentation (5)
1. **src/users/user.service.ts:42**
 ```typescript
 async updateUserPreferences(userId: string, preferences: any)
 ```
 **Fix**: Add JSDoc with @param, @returns, @throws
2. **src/orders/order.service.ts:78**
 ```typescript
 calculateTotal(items: OrderItem[])
 ```
 **Fix**: Document calculation logic and edge cases
3. **src/payments/stripe.service.ts:91**
 ```typescript
 handleWebhook(event: StripeEvent)
 ```
 **Fix**: Document webhook handling and event types
### Incomplete API Documentation (3)
4. **POST /users/{id}/preferences**
 - Missing: Request body schema
 - Missing: Code example
 - Fix: Add Pydantic/DTO schema and TypeScript example
5. **GET /orders/{id}/items**
 - Missing: Response examples
 - Fix: Add example response with multiple items
6. **POST /payments/webhook**
 - Missing: Webhook payload documentation
 - Fix: Use AsyncAPI to document webhook events
### Undocumented Types (4)
7. **src/types/order.ts:15** - `OrderStatus` enum
 ```typescript
 enum OrderStatus {
 PENDING, // Add description
 CONFIRMED, // Add description
 SHIPPED, // Add description
 DELIVERED // Add description
 }
 ```
8. **src/types/payment.ts:23** - `PaymentMethod` interface
 - 0/4 fields documented
 - Fix: Add JSDoc for each field
## Recommendations
### Immediate Actions (Priority: High)
1. ✏️ Document payment service functions (22 undocumented)
2. ✏️ Add request/response schemas for 3 API endpoints
3. ✏️ Complete PaymentMethod and OrderStatus type documentation
### Short-term Improvements
4. Add code examples for 12 endpoints
5. Improve order service documentation
6. Document edge cases and error handling
### Long-term Goals
7.  Achieve 95% overall coverage
8.  Add integration examples for complex workflows
9.  Create architecture documentation for payment flow
## Auto-Fix Suggestions
Run these commands to automatically generate missing documentation:
```bash
# Generate function documentation
/doc-fix --file src/users/user.service.ts --function updateUserPreferences
# Generate API documentation
/doc-generate-api --endpoints "POST /users/{id}/preferences"
# Generate type documentation
/doc-fix --file src/types/order.ts --type OrderStatus
```
## Historical Trend
| Date | Coverage | Change |
|------|----------|--------|
| 2025-01-17 | 87.3% | +2.1% ⬆️ |
| 2025-01-10 | 85.2% | +1.5% ⬆️ |
| 2025-01-03 | 83.7% | -0.3% ⬇️ |
| 2024-12-27 | 84.0% | +3.2% ⬆️ |
 **Trend**: Improving (+6.3% over last month)
## Next Steps
1. Run `/doc-fix` commands listed above
2. Review and merge auto-generated documentation
3. Add manual documentation for complex logic
4. Re-run `/doc-coverage` to verify improvements
5. Set up pre-commit hook to prevent coverage drops
```
### JSON Report
```json
{
 "generated_at": "2025-01-17T14:30:00Z",
 "overall_coverage": 87.3,
 "threshold": 80,
 "status": "PASS",
 "summary": {
 "functions": {
 "total": 342,
 "documented": 312,
 "coverage": 91.2,
 "status": "PASS"
 },
 "classes": {
 "total": 54,
 "documented": 48,
 "coverage": 88.9,
 "status": "PASS"
 },
 "api_endpoints": {
 "total": 42,
 "documented": 38,
 "coverage": 90.5,
 "status": "PASS"
 },
 "types": {
 "total": 127,
 "documented": 98,
 "coverage": 77.2,
 "status": "WARN"
 },
 "examples": {
 "total": 42,
 "documented": 30,
 "coverage": 71.4,
 "status": "FAIL"
 }
 },
 "modules": [
 {
 "path": "src/auth/",
 "coverage": 95.2,
 "status": "PASS",
 "breakdown": {
 "functions": { "total": 25, "documented": 24, "coverage": 96.0 },
 "classes": { "total": 4, "documented": 4, "coverage": 100.0 },
 "api_endpoints": { "total": 6, "documented": 6, "coverage": 100.0 },
 "types": { "total": 13, "documented": 12, "coverage": 92.3 }
 }
 }
 ],
 "gaps": [
 {
 "id": "gap-001",
 "type": "function",
 "severity": "high",
 "file": "src/users/user.service.ts",
 "line": 42,
 "function": "updateUserPreferences",
 "issue": "Missing JSDoc documentation",
 "fix": "Add JSDoc with @param, @returns, @throws",
 "auto_fixable": true
 }
 ],
 "recommendations": [
 {
 "priority": "high",
 "action": "Document payment service functions",
 "count": 22,
 "command": "/doc-fix --module src/payments/"
 }
 ],
 "trend": [
 { "date": "2025-01-17", "coverage": 87.3, "change": 2.1 },
 { "date": "2025-01-10", "coverage": 85.2, "change": 1.5 }
 ]
}
```
## CI/CD Integration
### Pre-Commit Hook
```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit
echo "Checking documentation coverage..."
# Run coverage check
COVERAGE=$(claude /doc-coverage --format json --output /tmp/coverage.json)
COVERAGE_PCT=$(jq -r '.overall_coverage' /tmp/coverage.json)
# Check threshold
THRESHOLD=80
if (( $(echo "$COVERAGE_PCT < $THRESHOLD" | bc -l) )); then
 echo "ERROR: Documentation coverage ${COVERAGE_PCT}% is below ${THRESHOLD}% threshold"
 echo ""
 echo "Missing documentation:"
 jq -r '.gaps[] | " - \(.file):\(.line) - \(.function)"' /tmp/coverage.json | head -10
 echo ""
 echo "Run 'claude /doc-coverage' for full report"
 exit 1
fi
echo "SUCCESS: Documentation coverage: ${COVERAGE_PCT}%"
```
### GitHub Actions
```yaml
name: Documentation Coverage
on:
 pull_request:
 paths:
 - 'src/**'
 - 'packages/**'
jobs:
 doc-coverage:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v3
 - name: Check documentation coverage
 id: coverage
 run: |
# Run coverage check
 claude /doc-coverage \
 --threshold 80 \
 --fail-below true \
 --format json \
 --output coverage.json
# Extract coverage percentage
 COVERAGE=$(jq -r '.overall_coverage' coverage.json)
 echo "coverage=$COVERAGE" >> $GITHUB_OUTPUT
 - name: Comment on PR
 uses: actions/github-script@v6
 with:
 script: |
 const coverage = ${{ steps.coverage.outputs.coverage }};
 const fs = require('fs');
 const report = JSON.parse(fs.readFileSync('coverage.json', 'utf8'));
 const comment = `##  Documentation Coverage Report
 **Overall Coverage**: ${coverage}%
 **Status**: ${report.status}
 | Category | Coverage |
 |----------|----------|
 | Functions | ${report.summary.functions.coverage}% |
 | Classes | ${report.summary.classes.coverage}% |
 | API Endpoints | ${report.summary.api_endpoints.coverage}% |
 | Types | ${report.summary.types.coverage}% |
 ${report.gaps.length > 0 ? `
### Critical Gaps (${Math.min(5, report.gaps.length)})
 ${report.gaps.slice(0, 5).map(gap =>
 `- \`${gap.file}:${gap.line}\` - ${gap.function}`
 ).join('\n')}
 ` : 'SUCCESS: No critical gaps found'}
 `;
 github.rest.issues.createComment({
 issue_number: context.issue.number,
 owner: context.repo.owner,
 repo: context.repo.repo,
 body: comment
 });
 - name: Fail if below threshold
 if: steps.coverage.outputs.coverage < 80
 run: exit 1
```
## Coverage Tracking Over Time
Store historical coverage data to track trends:
```typescript
// .claude/coverage-history.json
{
 "project": "grey-haven-api",
 "measurements": [
 {
 "timestamp": "2025-01-17T14:30:00Z",
 "commit": "9daca03",
 "coverage": {
 "overall": 87.3,
 "functions": 91.2,
 "classes": 88.9,
 "api_endpoints": 90.5,
 "types": 77.2,
 "examples": 71.4
 }
 }
 ]
}
```
**Trend Visualization:**
```
Coverage Trend (Last 30 Days)
90% ┤ ╭─╮
85% ┤ ╭─────────╯ ╰
80% ┤ ╭─────╯
75% ┤ ╭─────╯
70% ┼───────────────╯
 └────────────────────────────────────────
 Dec 18 Jan 1 Jan 17
```
## Auto-Fix Capabilities
Generate missing documentation automatically:
### Function Documentation
```typescript
// Before
async function getUserById(userId: string): Promise<User | null> {
 return this.db.users.findUnique({ where: { id: userId } });
}
// After auto-fix
/**
 * Retrieve a user by their unique identifier
 *
 * @param userId - Unique user identifier
 * @returns User object if found, null otherwise
 * @throws {DatabaseError} When database query fails
 *
 * @example
 * const user = await getUserById('usr_123');
 * if (user) {
 * console.log(user.email);
 * }
 */
async function getUserById(userId: string): Promise<User | null> {
 return this.db.users.findUnique({ where: { id: userId } });
}
```
### Type Documentation
```typescript
// Before
interface User {
 id: string;
 email: string;
 name: string;
 role: 'admin' | 'user';
}
// After auto-fix
/**
 * User account information
 */
interface User {
 /** Unique user identifier */
 id: string;
 /** User's email address */
 email: string;
 /** User's full name */
 name: string;
 /** User's role in the system */
 role: 'admin' | 'user';
}
```
## Best Practices
### 1. Set Realistic Thresholds
- Start with current coverage as baseline
- Increase threshold gradually (e.g., +5% per quarter)
- Different thresholds for different categories
### 2. Focus on Public APIs First
- 100% coverage for public API endpoints
- 90% coverage for public functions
- Lower priority for internal utilities
### 3. Quality Over Quantity
- Verify documentation accuracy
- Ensure examples are tested
- Keep descriptions concise but complete
### 4. Automate Where Possible
- Use auto-fix for simple cases
- Generate from types and schemas
- Validate in CI/CD pipeline
### 5. Regular Audits
- Quarterly documentation reviews
- Update outdated examples
- Improve based on user feedback
## Troubleshooting
### Issue: Coverage lower than expected
**Causes:**
- JSDoc/docstrings not in standard format
- Comments instead of proper documentation
- Inline type definitions instead of interfaces
**Solution:**
```bash
# Check what's being counted
/doc-coverage --format json --output /tmp/cov.json
# Review specific module
jq '.modules[] | select(.path == "src/users/")' /tmp/cov.json
```
### Issue: False positives (marked as undocumented)
**Cause**: Non-standard documentation format
**Solution:**
Configure documentation patterns:
```json
// .claude/doc-coverage-config.json
{
 "patterns": {
 "jsdoc": ["/**", " * ", " */"],
 "python_docstring": ["\"\"\"", "'''"],
 "required_tags": ["@param", "@returns"]
 }
}
```
### Issue: Coverage calculation inconsistent
**Cause**: Different calculation method
**Solution:**
```bash
# Use strict mode (requires all tags)
/doc-coverage --strict true
# Or lenient mode (just requires any documentation)
/doc-coverage --strict false
```
## Related Commands
- `/doc-generate-api` - Generate API documentation (includes coverage report)
- `/doc-fix` - Auto-fix specific documentation gaps
- `/code-review` - Code review includes documentation checks
- `/refactor-clarity` - Improve code clarity and documentation
## Agent Coordination
This command works with:
- **docs-architect** - Reviews coverage and generates missing docs
- **code-quality-analyzer** - Includes documentation in quality metrics
- **tdd-orchestrator** - Ensures tests document behavior
- **onboarding-coordinator** - Uses coverage data to prioritize docs
---
**Pro Tip**: Run `/doc-coverage --trend true` monthly to track documentation health over time. Set a coverage threshold in CI/CD to prevent documentation debt from accumulating.
