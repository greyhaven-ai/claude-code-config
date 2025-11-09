# Code Quality Analyzer Reference

Comprehensive reference guides for code quality analysis, security review, clarity refactoring, and architectural patterns.

## Files in This Directory

### [security-checklist.md](security-checklist.md)
Complete security checklist covering OWASP Top 10, input validation, authentication, cryptography, and data protection with actionable checks.

**When to use**: Security reviews, pre-deployment audits, vulnerability assessments
**Coverage**: OWASP Top 10, CWE database, common vulnerabilities

### [clarity-refactoring-rules.md](clarity-refactoring-rules.md)
10 proven refactoring rules for improving code clarity, reducing complexity, and eliminating technical debt without changing behavior.

**When to use**: Code reviews, refactoring sessions, complexity reduction
**Key topics**: Guard clauses, extract functions, explaining variables, naming conventions

### [code-quality-metrics.md](code-quality-metrics.md)
Understanding and interpreting code quality metrics including cyclomatic complexity, maintainability index, code duplication, and test coverage.

**When to use**: Quality assessments, setting standards, tracking improvements
**Metrics**: Complexity, duplication, coverage, maintainability scores

### [architecture-patterns.md](architecture-patterns.md)
Best practices for clean architecture, layering, dependency management, and preventing architectural erosion in multi-module codebases.

**When to use**: Synthesis analysis, architectural reviews, system design
**Patterns**: Layered architecture, dependency injection, circular dependency prevention

### [analysis-workflows.md](analysis-workflows.md)
Step-by-step workflows for conducting security reviews, clarity refactorings, and synthesis analysis with practical timelines and checklists.

**When to use**: Planning code quality initiatives, conducting audits
**Workflows**: Security review process, refactoring workflow, synthesis analysis

## Quick Reference

### Security Review Process
1. Run automated scanners (Bandit, Semgrep)
2. Manual code review for OWASP Top 10
3. Generate security scorecard
4. Prioritize by severity (Critical → High → Medium)
5. Fix and verify
6. Re-scan to confirm

### Clarity Refactoring Process
1. Identify complexity hotspots (complexity > 10)
2. Apply guard clauses to flatten nesting
3. Extract functions for single responsibility
4. Add explaining variables for complex logic
5. Replace magic numbers with constants
6. Measure before/after complexity

### Synthesis Analysis Process
1. Map module dependencies
2. Identify circular dependencies
3. Detect architectural violations
4. Find code duplication across files
5. Check consistency (naming, errors, patterns)
6. Enforce architectural standards

## Navigation by Use Case

**I need to**... | **Use this guide**...
---|---
Fix security vulnerabilities | [security-checklist.md](security-checklist.md)
Reduce code complexity | [clarity-refactoring-rules.md](clarity-refactoring-rules.md)
Understand quality metrics | [code-quality-metrics.md](code-quality-metrics.md)
Enforce clean architecture | [architecture-patterns.md](architecture-patterns.md)
Plan a code quality audit | [analysis-workflows.md](analysis-workflows.md)

---

Return to [agent documentation](../code-quality-analyzer.md)
