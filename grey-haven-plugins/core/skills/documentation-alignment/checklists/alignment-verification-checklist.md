# Documentation Alignment Verification Checklist

Comprehensive checklist for verifying code-documentation alignment.

**Project**: _______________
**Date**: _______________
**Verifier**: _______________

---

## Phase 1: Discovery (Find All Documentation)

### Code Documentation
- [ ] Located all source code files (.ts, .tsx, .js, .py)
- [ ] Found inline documentation (JSDoc, docstrings)
- [ ] Identified type definitions (.d.ts, type hints)
- [ ] Located comment blocks explaining complex logic

### External Documentation
- [ ] Found README.md files (root and subdirectories)
- [ ] Located /docs or /documentation directory
- [ ] Found API documentation (OpenAPI, Swagger specs)
- [ ] Checked for wiki or external doc sites
- [ ] Located tutorial/guide content

### Example Code
- [ ] Found example files in /examples directory
- [ ] Located code snippets in markdown docs
- [ ] Identified test files that demonstrate usage
- [ ] Found inline examples in docstrings

**Discovery Score**: ___/12

---

## Phase 2: Extraction (Parse Code & Docs)

### Function Signature Extraction
- [ ] Extracted all public function names
- [ ] Captured parameter lists with types
- [ ] Identified return types
- [ ] Noted async/sync indicators
- [ ] Extracted generic type parameters

### Documentation String Extraction
- [ ] Parsed JSDoc/docstring content
- [ ] Extracted parameter descriptions
- [ ] Found return value documentation
- [ ] Located error/exception documentation
- [ ] Captured usage examples

### Type Information Extraction
- [ ] Extracted TypeScript interface definitions
- [ ] Found Python type hints (Pydantic models)
- [ ] Identified union types and optionals
- [ ] Located type constraints
- [ ] Captured generic constraints

**Extraction Score**: ___/15

---

## Phase 3: Analysis (Compare Code vs Docs)

### Signature Alignment
- [ ] Function names match between code and docs
- [ ] Parameter count is identical
- [ ] Parameter names match exactly
- [ ] Parameter order is correct
- [ ] Optional parameters marked correctly

**Score**: ___/5 signatures matched

### Type Alignment
- [ ] All parameter types documented
- [ ] Return types match implementation
- [ ] Type nullability documented (`| null`, `| undefined`)
- [ ] Generic types explained
- [ ] Type constraints documented

**Score**: ___/5 types aligned

### Behavior Alignment
- [ ] Documented behavior matches implementation
- [ ] Side effects documented (file writes, API calls)
- [ ] Async/sync behavior correct in docs
- [ ] Performance characteristics accurate
- [ ] Thread safety / concurrency documented

**Score**: ___/5 behaviors aligned

### Error Alignment
- [ ] All thrown exceptions documented
- [ ] Error conditions listed
- [ ] Error message examples provided
- [ ] Recovery strategies documented
- [ ] Error types match implementation

**Score**: ___/5 errors aligned

### Example Alignment
- [ ] All code examples run successfully
- [ ] Examples use current API (not deprecated)
- [ ] Import statements correct
- [ ] Examples are copy-paste ready
- [ ] Examples demonstrate real use cases

**Score**: ___/5 examples working

**Analysis Score**: ___/25

---

## Phase 4: Classification (Prioritize Issues)

### Critical Issues (Count: ___)
- [ ] Breaking changes not documented
- [ ] Function signatures completely different
- [ ] Required parameters missing from docs
- [ ] Code examples that error/crash
- [ ] Security-relevant behavior undocumented

**Priority**: Fix immediately (within 24 hours)

### Important Issues (Count: ___)
- [ ] Public APIs without documentation
- [ ] Missing parameter descriptions
- [ ] Undocumented error cases
- [ ] Outdated examples (work but deprecated)
- [ ] Missing type information

**Priority**: Fix soon (within 1 week)

### Minor Issues (Count: ___)
- [ ] Sparse function descriptions
- [ ] Missing edge case documentation
- [ ] No performance notes
- [ ] Missing "why" explanations
- [ ] Internal functions publicly documented

**Priority**: Nice to fix (next sprint)

**Classification Score**: Critical + Important issues = ___

---

## Phase 5: Fix Generation (Create Solutions)

### Missing Documentation Fixes
- [ ] Generated docstrings for undocumented functions
- [ ] Added parameter descriptions
- [ ] Documented return types
- [ ] Listed possible errors
- [ ] Created usage examples

### Outdated Documentation Fixes
- [ ] Updated changed function signatures
- [ ] Fixed parameter names/types
- [ ] Updated return type documentation
- [ ] Revised behavioral descriptions
- [ ] Updated code examples

### Broken Example Fixes
- [ ] Fixed import statements
- [ ] Updated to current API
- [ ] Added missing parameters
- [ ] Corrected type usage
- [ ] Verified examples run

### Style Consistency Fixes
- [ ] Standardized docstring format
- [ ] Consistent parameter notation
- [ ] Uniform example formatting
- [ ] Matched project style guide

**Fix Generation Score**: ___/19 fixes created

---

## Phase 6: Validation (Verify Fixes Work)

### Syntax Validation
- [ ] Generated documentation is valid (JSDoc, reStructuredText, etc.)
- [ ] Markdown formatting correct
- [ ] Code blocks properly fenced
- [ ] Links are valid
- [ ] No syntax errors

### Example Testing
- [ ] All code examples run without errors
- [ ] Examples produce expected output
- [ ] Import statements resolve
- [ ] Type checking passes
- [ ] No runtime warnings

### Type Checking
- [ ] TypeScript compilation successful
- [ ] mypy passes (Python)
- [ ] Type annotations match implementation
- [ ] No `any` types introduced
- [ ] Generic constraints satisfied

### Consistency Checking
- [ ] Documentation style matches project standards
- [ ] Terminology used consistently
- [ ] Format follows template
- [ ] Examples follow conventions
- [ ] Version numbers correct

### Regression Testing
- [ ] Existing documentation still valid
- [ ] No broken links introduced
- [ ] Navigation still works
- [ ] Search indexes updated
- [ ] No unintended removals

**Validation Score**: ___/25 checks passed

---

## Final Alignment Score Calculation

**Formula**:
```
Alignment Score = (
  (Signature Match / 5 × 30) +
  (Type Match / 5 × 25) +
  (Behavior Match / 5 × 20) +
  (Error Match / 5 × 15) +
  (Example Match / 5 × 10)
)
```

**Calculations**:
- Signature: ___/5 × 30 = ___
- Type: ___/5 × 25 = ___
- Behavior: ___/5 × 20 = ___
- Error: ___/5 × 15 = ___
- Example: ___/5 × 10 = ___

**Total Score**: ___/100

### Score Interpretation
- **95-100**: Perfect alignment ✅
- **80-94**: Good alignment, minor issues ✅
- **60-79**: Poor alignment, needs work ⚠️
- **0-59**: Failing, critical issues ❌

---

## Quality Gates

### Must Pass (Blocking Issues)
- [ ] No critical issues remain
- [ ] All public APIs documented
- [ ] All code examples run successfully
- [ ] Alignment score ≥ 85
- [ ] Breaking changes documented

### Should Pass (Important)
- [ ] Type coverage ≥ 90%
- [ ] Error documentation complete
- [ ] No outdated examples
- [ ] Documentation freshness < 1 week old

### Nice to Have
- [ ] Alignment score ≥ 95
- [ ] All edge cases documented
- [ ] Performance notes included
- [ ] Migration guides present

**Gates Passed**: ___/12

---

## Coverage Metrics

### Documentation Coverage
- **Public Functions**: ___ total, ___ documented = ___%
- **Parameters**: ___ total, ___ described = ___%
- **Return Types**: ___ total, ___ documented = ___%
- **Errors**: ___ total, ___ documented = ___%

**Target**: 95%+ for all categories

### Example Coverage
- **Functions with Examples**: ___/___  = ___%
- **Working Examples**: ___/___ = ___%

**Target**: 80%+ functions with examples, 100% examples working

---

## Automation Checklist

### CI/CD Integration
- [ ] Alignment check runs in CI pipeline
- [ ] Fails build if score < 85
- [ ] Runs on pull requests
- [ ] Reports sent to team
- [ ] Metrics tracked over time

### Pre-commit Hooks
- [ ] Warns on function signature changes
- [ ] Prompts to update docs
- [ ] Runs example tests
- [ ] Checks type alignment

### Automated Generation
- [ ] Type documentation auto-generated
- [ ] API reference updated automatically
- [ ] Examples tested in CI
- [ ] Coverage reports generated

**Automation Score**: ___/11

---

## Action Items

### Immediate (This Week)
1. [ ] Fix ___ critical issues
2. [ ] Update ___ broken examples
3. [ ] Document ___ missing functions

**Owner**: ___________
**Due Date**: ___________

### Short-term (This Sprint)
1. [ ] Fix ___ important issues
2. [ ] Improve coverage to ___%
3. [ ] Implement ___ automation

**Owner**: ___________
**Due Date**: ___________

### Long-term (This Quarter)
1. [ ] Achieve 95%+ alignment score
2. [ ] Full CI/CD integration
3. [ ] < 5% doc-related bugs

**Owner**: ___________
**Due Date**: ___________

---

## Review & Sign-off

**Alignment Score**: ___/100

**Status**: [ ] ✅ Pass / [ ] ⚠️ Warning / [ ] ❌ Fail

**Critical Issues**: ___
**Important Issues**: ___
**Minor Issues**: ___

**Recommendation**:
[ ] Ready for production
[ ] Fix critical issues first
[ ] Major documentation refactor needed

**Reviewer**: ___________
**Date**: ___________
**Next Review**: ___________ (recommended: monthly)

---

## Quick Reference

**Minimum Passing Criteria**:
- ✅ Alignment score ≥ 85
- ✅ Zero critical issues
- ✅ All examples work
- ✅ Public API 95%+ documented

**Best Practice Targets**:
- 🎯 Alignment score ≥ 95
- 🎯 Type coverage 100%
- 🎯 Example coverage 80%+
- 🎯 Automated checks in CI
- 🎯 Documentation < 48 hours stale

**Common Red Flags**:
- 🚩 Score < 60 (failing)
- 🚩 > 5 critical issues
- 🚩 > 20% examples broken
- 🚩 Public APIs undocumented
- 🚩 Breaking changes not noted

---

**Checklist Version**: 1.0
**Last Updated**: 2025-01-15
