# TDD Orchestrator Templates

Ready-to-use templates for TDD workflows, session reports, and refactoring checklists.

## Available Templates

### [tdd-workflow-template.md](tdd-workflow-template.md)
Copy-paste template for documenting TDD cycles with RED-GREEN-REFACTOR structure.

**Use when**:
- Starting a new TDD feature
- Documenting TDD sessions for team review
- Teaching TDD to new developers
- Creating examples for knowledge base

**Includes**:
- RED phase checklist (write failing test)
- GREEN phase checklist (minimal implementation)
- REFACTOR phase checklist (improve design)
- Test quality checklist
- Coverage and mutation score tracking

---

### [tdd-session-report-template.md](tdd-session-report-template.md)
Report template for TDD session metrics - cycle times, coverage, mutation scores, and learnings.

**Use when**:
- End of TDD session
- Sprint retrospectives
- Team TDD reviews
- Performance tracking

**Includes**:
- Session metrics (cycles completed, time spent)
- Coverage metrics (line, branch, function)
- Mutation testing results
- Key learnings and improvements
- Action items

---

### [refactoring-checklist-template.md](refactoring-checklist-template.md)
Comprehensive checklist for safe refactoring during REFACTOR phase.

**Use when**:
- Before refactoring production code
- Code review preparation
- Refactoring retrospectives
- Training new developers on safe refactoring

**Includes**:
- Pre-refactoring safety checks
- Refactoring pattern selection
- Step-by-step execution checklist
- Validation and rollback procedures

---

## Usage Pattern

### 1. Starting a TDD Session

Copy [tdd-workflow-template.md](tdd-workflow-template.md) and use it to document each RED-GREEN-REFACTOR cycle.

### 2. During Refactoring

Open [refactoring-checklist-template.md](refactoring-checklist-template.md) and follow the checklist step-by-step to ensure safe refactoring.

### 3. Ending a TDD Session

Fill out [tdd-session-report-template.md](tdd-session-report-template.md) to capture metrics and learnings.

---

## Quick Reference

### TDD Cycle Duration
```
RED: 3-10 min   → Write failing test
GREEN: 5-15 min → Minimal implementation
REFACTOR: 5-10 min → Improve design
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 13-35 min per cycle
```

### Quality Gates
- ✅ Test fails before GREEN phase
- ✅ All tests pass before REFACTOR phase
- ✅ All tests pass after REFACTOR phase
- ✅ Coverage maintained or increased

---

Return to [tdd-orchestrator agent](../tdd-orchestrator.md) | [examples/](../examples/INDEX.md) | [reference/](../reference/INDEX.md)
