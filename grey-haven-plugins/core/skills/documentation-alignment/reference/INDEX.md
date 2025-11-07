# Documentation Alignment Reference

Complete reference for verifying and maintaining code-documentation alignment.

## Quick Navigation

| Resource | Purpose | Best For |
|----------|---------|----------|
| [Alignment Verification Guide](alignment-verification-guide.md) | Complete verification methodology | Understanding the process |
| [Misalignment Patterns](misalignment-patterns.md) | Common issues and solutions | Troubleshooting |
| [Automation Strategies](automation-strategies.md) | CI/CD integration | Production implementation |

## The 6-Phase Verification Process

### Phase 1: Discovery
**Goal:** Find all documentation sources

**Tasks:**
- Locate inline documentation (docstrings, JSDoc, comments)
- Find markdown documentation (README, /docs)
- Identify API specs (OpenAPI, Swagger)
- Search for external documentation
- Map code structure and dependencies

**Tools:**
- File globbing for `*.md`, `README*`
- AST parsing for docstrings
- grep for comment patterns
- Documentation generators

**Output:** Complete inventory of code and docs

---

### Phase 2: Extraction
**Goal:** Parse code and documentation into comparable format

**Tasks:**
- Extract function signatures (name, parameters, return types)
- Parse type information (TypeScript, Python type hints)
- Extract documentation strings
- Identify examples in docs
- Build structured data model

**Tools:**
- TypeScript Compiler API
- Python `ast` module
- Pydantic for Python
- JSDoc parser for JavaScript
- markdown-it for docs

**Output:** Structured representation of code vs docs

---

### Phase 3: Analysis
**Goal:** Compare code against documentation

**Comparisons:**
1. **Signature Alignment**
   - Function name matches
   - Parameter count matches
   - Parameter names match
   - Parameter order correct

2. **Type Alignment**
   - Parameter types documented
   - Return types match
   - Generic types documented
   - Type constraints listed

3. **Behavior Alignment**
   - Documented behavior matches implementation
   - Side effects documented
   - Performance characteristics accurate
   - Async/sync behavior correct

4. **Error Alignment**
   - All thrown exceptions documented
   - Error conditions listed
   - Error messages match
   - Recovery strategies documented

5. **Example Alignment**
   - Code examples run successfully
   - Examples use current API
   - Examples demonstrate real use cases
   - Examples are copy-paste ready

**Output:** List of misalignments with severity

---

### Phase 4: Classification
**Goal:** Prioritize issues for fixing

**Severity Levels:**

**Critical (Fix Immediately):**
- Breaking changes not documented
- Function signatures don't match
- Required parameters missing
- Examples that error
- Security implications

**Important (Fix Soon):**
- Public APIs undocumented
- Missing error documentation
- Type information incomplete
- Outdated examples
- Deprecated features still shown

**Minor (Nice to Fix):**
- Missing edge case docs
- Sparse descriptions
- No performance notes
- Internal functions documented as public

**Alignment Scoring:**
```
Score = (
  (SignatureMatch × 30) +
  (TypeMatch × 25) +
  (BehaviorMatch × 20) +
  (ErrorMatch × 15) +
  (ExampleMatch × 10)
) / 100

95-100: Perfect alignment
80-94: Good alignment
60-79: Poor alignment
0-59: Failing
```

**Output:** Prioritized list with alignment score

---

### Phase 5: Fix Generation
**Goal:** Create fixes for misalignments

**Fix Types:**

**1. Missing Documentation:**
```typescript
// Before (no docs)
function processData(data: Data[]): Result {
  return data.map(transform).filter(validate);
}

// After (generated docs)
/**
 * Process data items through transformation and validation pipeline.
 *
 * @param data - Array of data items to process
 * @returns Processed and validated results
 *
 * @example
 * ```typescript
 * const data = [{ id: 1, value: "test" }];
 * const results = processData(data);
 * // Returns validated, transformed data
 * ```
 */
function processData(data: Data[]): Result {
  return data.map(transform).filter(validate);
}
```

**2. Outdated Documentation:**
```typescript
// Code updated but docs stale
function createUser(orgId: string, email: string, name: string) { ... }

// Old docs say:
// createUser(email, name)

// Generated fix:
/**
 * Create a new user in an organization.
 *
 * @param orgId - Organization ID (required as of v2.0)
 * @param email - User email address
 * @param name - User display name
 *
 * @migration v1.x → v2.0
 * organizationId is now the first required parameter
 */
```

**3. Broken Examples:**
```typescript
// Example uses deprecated API
// Old: const user = await api.getUser(id);
// New: const user = await api.users.get(id);

// Generated replacement with migration note
```

**Output:** Ready-to-apply fixes

---

### Phase 6: Validation
**Goal:** Ensure fixes resolve issues

**Validation Steps:**
1. **Syntax Check:** Generated docs are valid
2. **Example Test:** All examples run successfully
3. **Type Check:** Types match implementation
4. **Consistency Check:** Style matches project standards
5. **Regression Check:** Didn't break existing docs

**Tools:**
- TypeScript compiler for type checking
- Jest/Vitest for example testing
- ESLint/TSDoc for style
- Git diff for changes review

**Output:** Verified, production-ready documentation

---

## Alignment Metrics

### Code Coverage vs Doc Coverage

**Code Coverage** (tests):
- Measures % of code executed by tests
- Industry standard: 80%+

**Doc Coverage** (documentation):
- Measures % of public API documented
- Target: 95%+ for public APIs
- Target: 60%+ for internal APIs

**Alignment Coverage:**
- % of documented features that work as described
- Target: 98%+ alignment for production

### Key Performance Indicators

**Developer Productivity:**
- Time to understand API: Target < 15 min
- Onboarding time: Target 1-2 days
- Support tickets from docs: Target < 5%

**Documentation Quality:**
- Alignment score: Target 95+
- Example success rate: Target 100%
- Doc freshness: Updated within 1 week of code changes

**Maintenance Burden:**
- Time to update docs: Target < 10% of dev time
- Automated coverage: Target 70%+
- Manual review needed: Target < 30%

---

## Common Misalignment Patterns

### Pattern 1: "Feature Creep"
**Symptom:** Function grows parameters, docs stay same
**Fix:** Automated parameter detection
**Prevention:** Pre-commit hooks

### Pattern 2: "Refactor Drift"
**Symptom:** Function renamed, old name in docs
**Fix:** AST-based find/replace
**Prevention:** IDE refactoring tools

### Pattern 3: "Example Rot"
**Symptom:** Examples use deprecated APIs
**Fix:** Example test suite
**Prevention:** CI testing all examples

### Pattern 4: "Type Evolution"
**Symptom:** Types change, docs outdated
**Fix:** Type extraction from code
**Prevention:** Generated type docs

### Pattern 5: "Behavior Divergence"
**Symptom:** Code does something different than docs say
**Fix:** Behavioral testing + doc update
**Prevention:** TDD with docs as specs

---

## Tool Integration

### TypeScript Projects
```json
{
  "scripts": {
    "check-docs": "ts-node scripts/verify-docs-alignment.ts",
    "generate-docs": "typedoc --plugin typedoc-plugin-markdown",
    "test-examples": "vitest examples/**/*.test.ts"
  }
}
```

### Python Projects
```toml
[tool.pydantic-docs]
alignment-threshold = 95
auto-fix = true

[tool.pytest.ini_options]
testpaths = ["docs/examples"]
doctest_optionflags = "NORMALIZE_WHITESPACE"
```

### CI/CD Integration
```yaml
# .github/workflows/docs.yml
- name: Check Documentation Alignment
  run: npm run check-docs
  # Fails if score < 85

- name: Test Documentation Examples
  run: npm run test-examples
  # Ensures all examples work
```

---

## Best Practices

### 1. Single Source of Truth
**Principle:** Code is the source of truth for signatures
**Implementation:**
- Generate docs from code when possible
- Extract types directly from implementation
- Auto-generate parameter lists

### 2. Test Documentation
**Principle:** Documentation should be testable
**Implementation:**
- Run code examples in CI
- Use doctest for Python
- TypeScript examples as tests

### 3. Version Documentation
**Principle:** Docs should match code version
**Implementation:**
- Tag docs with version numbers
- Maintain changelog for API changes
- Show migration guides

### 4. Automate Where Possible
**Principle:** Reduce manual documentation burden
**Implementation:**
- Generate from types (TypeDoc, Sphinx autodoc)
- Extract from comments (JSDoc → markdown)
- Test examples automatically

### 5. Make Breaking Changes Obvious
**Principle:** API changes should be impossible to miss
**Implementation:**
- BREAKING CHANGE tags
- Migration guides
- Deprecation warnings
- Version badges

---

**Quick Start:**
1. Read [Alignment Verification Guide](alignment-verification-guide.md)
2. Identify misalignments using [Patterns](misalignment-patterns.md)
3. Automate with [Strategies](automation-strategies.md)
4. Use [Templates](../templates/) for common scenarios

**Success Metrics:**
- 95%+ alignment score
- < 5% documentation-related bugs
- 70%+ automated coverage
- 1-day onboarding time
