# TDD Orchestrator Reference

Comprehensive reference materials for TDD methodologies, tools, and best practices.

## Files in This Directory

### [red-green-refactor-guide.md](red-green-refactor-guide.md)
Complete guide to the red-green-refactor cycle - the core TDD methodology with phase-by-phase instructions, timing guidelines, and quality gates.

**When to use**: Learning TDD fundamentals, training teams
**Covers**: RED (write failing test), GREEN (minimal implementation), REFACTOR (improve design)
**Key Concepts**: Test-first discipline, incremental development, refactoring with confidence

---

### [tdd-methodologies.md](tdd-methodologies.md)
Comparison of TDD approaches - Chicago School (classicist), London School (mockist), ATDD, BDD, Outside-In, Inside-Out, and Hexagonal TDD.

**When to use**: Choosing TDD approach for project, understanding trade-offs
**Covers**: 7 TDD methodologies with pros/cons, decision matrix
**Key Concepts**: State vs. interaction testing, mocking strategies, test doubles

---

### [mutation-testing-reference.md](mutation-testing-reference.md)
Comprehensive mutation testing guide - tools, mutation operators, score thresholds, and CI/CD integration for Python, JavaScript, Java, and C#.

**When to use**: Validating test quality, improving test effectiveness
**Covers**: mutmut, Stryker, PITest, mutation operators, score interpretation
**Key Concepts**: Test effectiveness, mutation score, equivalent mutations

---

### [coverage-thresholds.md](coverage-thresholds.md)
Coverage metrics, thresholds, and quality gates - line coverage, branch coverage, critical path coverage, differential coverage, and enforcement strategies.

**When to use**: Setting quality gates, configuring CI/CD, defining team standards
**Covers**: Coverage types, threshold recommendations, exemption policies
**Key Concepts**: 80% line, 75% branch, 100% critical path, differential coverage

---

### [refactoring-patterns.md](refactoring-patterns.md)
Catalog of refactoring patterns with SOLID principles - Extract Method, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, and 20+ patterns.

**When to use**: Refactoring during REFACTOR phase, improving design
**Covers**: 25+ refactoring patterns, SOLID principles, code smells
**Key Concepts**: Refactoring safety, behavior preservation, incremental improvement

---

## Quick Reference

### TDD Cycle Summary

```
1. RED: Write failing test (3-10 min)
   ↓
2. GREEN: Minimal implementation (5-15 min)
   ↓
3. REFACTOR: Improve design (5-10 min)
   ↓
Repeat
```

**Total cycle time**: 15-35 minutes

### Coverage Targets

| Metric | Target | Critical Path |
|--------|--------|---------------|
| Line Coverage | 80%+ | 100% |
| Branch Coverage | 75%+ | 100% |
| Function Coverage | 85%+ | 100% |
| Mutation Score | 85%+ | 95%+ |

### Refactoring Triggers

- Duplicated code (DRY violation)
- Long functions (>50 lines)
- Deep nesting (>3 levels)
- Complex conditionals
- Many parameters (>4)
- God class (too many responsibilities)

### When to Use Each Methodology

| Methodology | Best For | Avoid When |
|-------------|----------|------------|
| Chicago School | Domain logic, algorithms | Complex dependencies |
| London School | Microservices, layered architecture | Simple utilities |
| ATDD | Business-driven features | Technical tasks |
| BDD | Customer-facing features | Internal APIs |
| Outside-In | New features, clean architecture | Refactoring legacy |
| Inside-Out | Core algorithms, utilities | User stories |

---

Return to [tdd-orchestrator agent](../tdd-orchestrator.md)
