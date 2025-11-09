# Documentation Alignment Report Template

Standard template for documenting alignment verification results.

**Date**: [YYYY-MM-DD]
**Project**: [Project Name]
**Scope**: [Module/Component/Full Codebase]
**Verifier**: [Name/Team]

---

## Executive Summary

**Overall Alignment Score**: [X]/100

**Status**: ✅ Pass (≥85) / ⚠️ Warning (60-84) / ❌ Fail (<60)

**Key Findings**:
- Critical Issues: [count]
- Important Issues: [count]
- Minor Issues: [count]

**Recommendation**: [Ready for Production / Fix Critical First / Major Refactor Needed]

---

## Scope Analysis

### Files Analyzed

**Code Files**: [count]
```
src/
├── auth/          (5 files, 450 LOC)
├── api/           (12 files, 1200 LOC)
└── utils/         (8 files, 600 LOC)
Total: 25 files, 2250 LOC
```

**Documentation Files**: [count]
```
docs/
├── api/           (8 markdown files)
├── guides/        (5 markdown files)
└── README.md
Total: 14 files
```

**Functions Checked**: [count]
- Public functions: [X]
- Documented: [Y]
- Coverage: [Y/X × 100]%

---

## Alignment Score Breakdown

| Category | Weight | Score | Weighted | Status |
|----------|--------|-------|----------|--------|
| Signature Match | 30% | [X]/100 | [X × 0.3] | [✅/⚠️/❌] |
| Type Match | 25% | [X]/100 | [X × 0.25] | [✅/⚠️/❌] |
| Behavior Match | 20% | [X]/100 | [X × 0.2] | [✅/⚠️/❌] |
| Error Match | 15% | [X]/100 | [X × 0.15] | [✅/⚠️/❌] |
| Example Match | 10% | [X]/100 | [X × 0.1] | [✅/⚠️/❌] |
| **Total** | **100%** | **[Total]** | **[Total]** | **[Status]** |

**Legend:**
- ✅ Excellent (90-100)
- ⚠️ Needs Work (60-89)
- ❌ Critical (0-59)

---

## Critical Issues (Must Fix)

### Issue 1: [Title]

**Location**: [file.ts:line] → [docs/file.md:section]

**Severity**: Critical

**Category**: [Signature Mismatch / Type Mismatch / Broken Example / Behavior Divergence]

**Description**:
[What's wrong - be specific]

**Impact**:
- [How this affects users]
- [Potential for bugs/confusion]
- [Security implications if any]

**Current State**:
```typescript
// Code (actual implementation)
function authenticate(email: string, password: string, orgId: string): Promise<Token> {
  ...
}
```

```markdown
<!-- Documentation (outdated) -->
### authenticate(email, password)
Returns authentication token.
```

**Required Fix**:
```markdown
### authenticate(email, password, orgId)

Authenticate user and return JWT token.

**Parameters:**
- `email` (string) - User email address
- `password` (string) - User password
- `orgId` (string) - Organization ID for multi-tenant auth

**Returns:**
- `Promise<Token>` - JWT authentication token

**Example:**
```typescript
const token = await authenticate(
  'user@example.com',
  'password123',
  'org_abc123'
);
```
```

**Estimated Fix Time**: [X minutes/hours]

**Priority**: [1-5, with 1 being highest]

---

### Issue 2: [Title]

[Repeat structure for each critical issue]

---

## Important Issues (Should Fix Soon)

### Issue [N]: [Title]

**Location**: [file:line]
**Severity**: Important
**Category**: [Category]

**Brief Description**:
[One-line summary]

**Impact**:
[How it affects users]

**Suggested Fix**:
[Quick fix description or code snippet]

**Estimated Time**: [X min]

---

## Minor Issues (Nice to Fix)

### Issue [N]: [Title]

**Location**: [file:line]
**Issue**: [Brief description]
**Fix**: [Quick suggestion]

---

## Documentation Coverage

### Public API Coverage

| Module | Public Functions | Documented | Coverage |
|--------|------------------|------------|----------|
| auth/ | 5 | 4 | 80% |
| api/ | 12 | 11 | 92% |
| utils/ | 8 | 6 | 75% |
| **Total** | **25** | **21** | **84%** |

**Target**: 95%+ for public APIs

**Missing Documentation**:
- `utils/validateInput.ts` - `sanitizeHtml()`
- `utils/formatters.ts` - `formatCurrency()`
- `auth/tokens.ts` - `refreshToken()`
- `api/users.ts` - `bulkUpdateUsers()`

---

## Example Validation Results

**Total Examples Found**: [count]
**Examples Tested**: [count]
**Passing**: [count]
**Failing**: [count]

### Failing Examples

**Example 1**: [Location]
```typescript
// Example code that fails
const user = await createUser(email, name);
// Error: Missing required parameter 'organizationId'
```

**Fix Required**:
```typescript
// Corrected example
const user = await createUser(organizationId, email, name);
```

---

## Type Safety Analysis

### TypeScript Projects

**Strict Mode**: [✅ Enabled / ❌ Disabled]

**Type Coverage**:
- Functions with type annotations: [X]%
- Parameters typed: [X]%
- Return types explicit: [X]%

**Type Mismatches in Docs**:
- [file.ts:line] - Docs say `string`, code expects `string | null`
- [file.ts:line] - Docs say `boolean`, code returns `Promise<boolean>`

### Python Projects

**Type Hints Coverage**:
- Functions with hints: [X]%
- mypy strict mode: [✅/❌]

**Pydantic Models**:
- Total models: [count]
- Documented models: [count]
- Coverage: [X]%

---

## Behavioral Alignment

### Tested Behaviors

| Function | Documented Behavior | Actual Behavior | Match |
|----------|---------------------|-----------------|-------|
| validateEmail() | Returns boolean | Returns {isValid, errors} | ❌ |
| createUser() | Throws on error | Returns null on error | ❌ |
| processData() | Async operation | Sync operation | ❌ |

**Behavior Mismatches**: [count]

**Impact**: Users expect one behavior but get another

---

## Error Handling Alignment

### Documented vs Actual Errors

**Function**: `createUser()`

**Documented Errors**:
- `ValidationError` - Invalid email format

**Actual Errors**:
- `ValidationError` - Invalid email format ✅
- `DuplicateError` - Email already exists ❌ Undocumented
- `AuthorizationError` - No permission ❌ Undocumented

**Missing Error Docs**: [count]

---

## Recommendations

### Immediate Actions (This Sprint)

1. **Fix Critical Issues** ([count] issues)
   - Estimated time: [X hours]
   - Priority: Highest
   - Owner: [Team/Person]

2. **Update Broken Examples** ([count] examples)
   - Estimated time: [X hours]
   - Priority: High
   - Owner: [Team/Person]

3. **Document Missing Errors** ([count] functions)
   - Estimated time: [X hours]
   - Priority: High
   - Owner: [Team/Person]

### Short-term (Next Sprint)

1. **Improve Coverage** (target: 95%)
   - Document [count] missing public functions
   - Add type information to all docs

2. **Fix Important Issues** ([count] issues)
   - Parameter descriptions
   - Outdated examples
   - Type mismatches

### Long-term (This Quarter)

1. **Implement Automation**
   - CI/CD alignment checks
   - Auto-generated docs for types
   - Example testing in pipeline

2. **Establish Standards**
   - Documentation style guide
   - Review checklist
   - Alignment SLA (24-48 hours)

---

## Automation Opportunities

**Current Manual Effort**: [X hours/week]

**Opportunities**:

1. **Auto-generate Type Docs** (save: [X hrs/week])
   - Use TypeDoc / Sphinx autodoc
   - Extract from code directly

2. **Test Examples in CI** (save: [X hrs/week])
   - Run examples as tests
   - Catch breaks immediately

3. **Pre-commit Hooks** (save: [X hrs/week])
   - Warn on signature changes
   - Require doc updates

**Potential Savings**: [X%] of current effort

---

## Comparison with Previous Reports

| Metric | [Previous Date] | [Current Date] | Change |
|--------|-----------------|----------------|--------|
| Alignment Score | [X] | [Y] | [+/-Z] |
| Critical Issues | [X] | [Y] | [+/-Z] |
| Doc Coverage | [X]% | [Y]% | [+/-Z]% |
| Passing Examples | [X]% | [Y]% | [+/-Z]% |

**Trend**: [Improving / Stable / Declining]

---

## Action Items

### For Developers

- [ ] Fix [count] critical issues by [date]
- [ ] Update [count] broken examples
- [ ] Add missing error documentation

### For Tech Writers

- [ ] Review and update API reference
- [ ] Create migration guides for breaking changes
- [ ] Standardize documentation format

### For DevOps

- [ ] Implement CI alignment checks
- [ ] Set up example testing
- [ ] Configure pre-commit hooks

---

## Sign-off

**Verified By**: [Name]
**Date**: [YYYY-MM-DD]
**Next Review**: [YYYY-MM-DD] (recommended: monthly)

**Approval**: [ ] Ready for Production / [ ] Needs Fixes

**Notes**:
[Any additional context or concerns]

---

**Attachments**:
- Full issue list: [link to detailed report]
- Example test results: [link to test output]
- Coverage report: [link to coverage data]
