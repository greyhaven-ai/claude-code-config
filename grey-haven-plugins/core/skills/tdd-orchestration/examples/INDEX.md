# TDD Orchestrator Examples

Real-world TDD workflow examples demonstrating red-green-refactor discipline, mutation testing, and multi-agent coordination.

## Files in This Directory

### [red-green-refactor-example.md](red-green-refactor-example.md)
Complete TDD cycle for implementing user authentication - demonstrates strict red-green-refactor discipline with 19-minute cycle time, 87% coverage, and 91% mutation score.

**When to use**: Learning core TDD cycle, demonstrating methodology to teams
**Demonstrates**: RED phase validation, GREEN minimal implementation, REFACTOR with confidence
**Metrics**: 5min RED, 8min GREEN, 6min REFACTOR = 19min total

---

### [outside-in-tdd-example.md](outside-in-tdd-example.md)
Feature-first TDD approach for order processing system - starts with acceptance test, works inward through layers (API → Service → Repository → Database).

**When to use**: Building new features, establishing architectural boundaries
**Demonstrates**: Acceptance tests first, mocking collaborators, layer-by-layer implementation
**Metrics**: 4-day feature, 95% coverage, zero defects in production

---

### [mutation-testing-example.md](mutation-testing-example.md)
Mutation testing workflow to validate test quality - identifies weak tests through code mutations, improves from 73% to 94% mutation score.

**When to use**: Validating test suite quality, finding edge cases
**Demonstrates**: Mutation generation, survivor analysis, test strengthening
**Tools**: mutmut (Python), Stryker (JavaScript)

---

### [tdd-rescue-example.md](tdd-rescue-example.md)
Recovery protocols for TDD failures - handles test passing unexpectedly, green phase failures, and refactoring breaks.

**When to use**: Recovering from TDD anti-patterns, training teams on recovery
**Demonstrates**: RED phase failures, GREEN phase debugging, REFACTOR rollback
**Outcome**: 3 failed cycles recovered, methodology restored

---

## Usage Patterns

**Learning TDD**: Start with [red-green-refactor-example.md](red-green-refactor-example.md)

**Building Features**: Use [outside-in-tdd-example.md](outside-in-tdd-example.md)

**Improving Test Quality**: Follow [mutation-testing-example.md](mutation-testing-example.md)

**Handling Problems**: Reference [tdd-rescue-example.md](tdd-rescue-example.md)

## Quick Reference

**TDD Cycle Duration**:
- RED: 3-10 minutes (write failing test)
- GREEN: 5-15 minutes (minimal implementation)
- REFACTOR: 5-10 minutes (improve design)
- Total: 15-35 minutes per cycle

**Coverage Targets**:
- Line coverage: 80% minimum
- Branch coverage: 75% minimum
- Critical path: 100% required
- Mutation score: 85%+ excellent

**Anti-Patterns to Avoid**:
- Writing implementation before test
- Multiple tests before implementation
- Skipping refactor phase
- Tests that don't fail first
- Over-engineering in GREEN phase

---

Return to [tdd-orchestrator agent](../tdd-orchestrator.md)
