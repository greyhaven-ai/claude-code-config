# TDD Orchestrator Checklists

Quick-reference checklists for TDD discipline and quality gates.

## Available Checklists

### [tdd-discipline-checklist.md](tdd-discipline-checklist.md)
Comprehensive checklist for ensuring test-first discipline throughout RED-GREEN-REFACTOR cycles.

**Use when**:
- Starting a TDD session
- Training new developers on TDD
- Auditing TDD compliance
- Sprint retrospectives

**Covers**:
- Pre-session setup
- RED phase discipline (test-first)
- GREEN phase discipline (minimal implementation)
- REFACTOR phase discipline (behavior preservation)
- Post-session review

---

### [quality-gates-checklist.md](quality-gates-checklist.md)
Quality gates for coverage thresholds, mutation scores, and production readiness.

**Use when**:
- Before code review
- Before merge to main
- Before production deployment
- Sprint quality reviews

**Covers**:
- Coverage thresholds (line, branch, function)
- Mutation testing scores
- Code quality metrics
- Performance requirements
- Security requirements

---

## Usage Pattern

### Daily TDD Work

1. **Start of session**: Review [tdd-discipline-checklist.md](tdd-discipline-checklist.md)
2. **During cycles**: Follow RED-GREEN-REFACTOR discipline
3. **End of session**: Check [quality-gates-checklist.md](quality-gates-checklist.md)

### Code Review

1. **Developer**: Complete [quality-gates-checklist.md](quality-gates-checklist.md)
2. **Reviewer**: Verify checklist items
3. **Approve**: Only if all quality gates pass

### Production Deployment

1. **All quality gates**: Must pass
2. **Coverage thresholds**: Must meet or exceed
3. **Mutation score**: Must meet minimum
4. **Performance**: No regressions

---

## Quick Reference

### TDD Discipline

- ✅ Write test BEFORE code (RED)
- ✅ Write MINIMAL code to pass (GREEN)
- ✅ Improve design WITHOUT changing behavior (REFACTOR)
- ✅ Run tests after EVERY change
- ✅ Commit after GREEN or REFACTOR

### Quality Gates

| Metric | Minimum | Target | Critical Path |
|--------|---------|--------|---------------|
| Line Coverage | 80% | 85-90% | 100% |
| Branch Coverage | 75% | 80-85% | 100% |
| Function Coverage | 85% | 90-95% | 100% |
| Mutation Score | 85% | 90-95% | 95%+ |

---

Return to [tdd-orchestrator agent](../tdd-orchestrator.md) | [examples/](../examples/INDEX.md) | [reference/](../reference/INDEX.md) | [templates/](../templates/INDEX.md)
