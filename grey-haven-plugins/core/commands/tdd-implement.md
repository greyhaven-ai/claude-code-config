---
allowed-tools: Read, Write, MultiEdit, Bash, Grep, Glob, Task, TodoWrite, Teammate, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet
description: Implement feature using strict TDD methodology with red-green-refactor cycle
argument-hint: [feature description or requirements]
---
Implement with TDD: $ARGUMENTS
<ultrathink>
Test-Driven Development is the path to quality. Red, Green, Refactor. No shortcuts. Tests drive design.
</ultrathink>
<megaexpertise type="tdd-practitioner">
The assistant should follow strict TDD methodology, leveraging specialist agents and the hook ecosystem to ensure proper test-first development. Prefer team mode for parallel execution when available.
</megaexpertise>
<context>
Implementing feature: $ARGUMENTS
Using Test-Driven Development methodology
Hooks will validate each phase of the TDD cycle
</context>
<requirements>
- Write failing tests first (Red phase)
- Write minimal code to pass (Green phase)
- Refactor while keeping tests green
- Maintain high test coverage (>90%)
- Follow project test conventions
- Document test scenarios
</requirements>
<actions>
1. **Analyze Requirements**:
 - Break down $ARGUMENTS into testable units
 - Identify edge cases and error scenarios
 - Create test plan with TodoWrite
2. **Detect Test Framework**:
 - Use Glob to find test config files (`**/pytest.ini`, `**/vitest.config.*`, `**/jest.config.*`, `**/pyproject.toml`)
 - Use Grep to check for framework references in package.json or pyproject.toml
 - Identify test directory structure with Glob (`**/test*/**`, `**/*.test.*`, `**/*.spec.*`)
3. **Detect Orchestration Mode**:
 - **Team Mode**: If the feature has 2+ independent components AND the Teammate tool is available, use the tdd-orchestrator agent in team mode. This spawns specialist teammates (test-writer, implementer, quality reviewer) with file ownership and plan approval gates for parallel TDD execution.
 - **Subagent Mode**: For single-component features or when team tools are unavailable, delegate to language-specific TDD agents sequentially.
 - Announce the selected mode before proceeding.
4. **Team Mode TDD Cycle** (preferred for multi-component features):
 ```
 Invoke tdd-orchestrator via Task tool. It will:
 a. Create team: tdd-{feature-slug}
 b. Build task board with layered dependencies:
    Layer 0: Red Phase   (test-writer writes failing tests, parallel per component)
    Layer 1: Green Phase (implementer passes tests, blocked by Red)
    Layer 2: Refactor    (implementer refactors, blocked by Green)
    Layer 3: Quality     (quality reviewer, blocked by Refactor)
    Layer 4: Integration (cross-component integration tests)
    Layer 5: Synthesis   (final report)
 c. Spawn teammates with file ownership boundaries
 d. Review and approve/reject teammate plans
 e. Monitor progress and unblock as needed
 f. Run full test suite and generate report
 g. Cleanup team resources
 ```
5. **Subagent Mode TDD Cycle** (fallback):
 ```
 For each feature component:
 [CRITICAL] RED PHASE:
 - Write failing test describing desired behavior
 - Hook: test-runner confirms test fails
 - Verify failure is for correct reason
 [OK] GREEN PHASE:
 - Write minimal code to pass test
 - Hook: test-runner confirms test passes
 - No over-engineering allowed
  REFACTOR PHASE:
 - Improve code structure
 - Hook: test-runner ensures tests still pass
 - Hook: code-clarity-analyzer suggests improvements
 ```
6. **Coverage Tracking**:
 - Hook: coverage-reporter tracks progress
 - Ensure each new feature has tests
 - Target: >90% coverage for new code
7. **Test Quality Validation**:
 - Tests are independent and isolated
 - Tests run fast (<100ms per unit test)
 - Tests have clear assertions
 - Tests document behavior
8. **Integration with CI/CD**:
 ```yaml
# Example GitHub Actions integration
 - name: Run TDD Tests
 run: |
 pytest tests/ -v --cov=src --cov-report=term-missing
# or
 bun test --coverage
 ```
9. **Documentation Generation**:
 - Generate test documentation
 - Create examples from test cases
 - Update README with test instructions
10. **TDD Report**:
 ```markdown
## TDD Implementation Report

### Orchestration
 - Mode: {Team Mode | Subagent Mode}
 - Team: {team name, if team mode}
 - Teammates: {list, if team mode}

### Test Statistics
 - Tests written: X
 - Tests passing: X/X (100%)
 - Coverage achieved: X%

### Red-Green-Refactor Cycles
 - Cycles completed: X
 - Average cycle time: Y minutes

### Team Coordination (if team mode)
 - Plans submitted: X
 - Plans approved: X
 - Plans rejected & revised: X
 - File ownership violations: 0

### Code Quality
 - Functions tested: X/Y
 - Edge cases covered: [OK]
 - Error scenarios tested: [OK]

### Next Steps
 - [ ] Integration tests
 - [ ] Performance tests
 - [ ] Documentation updates
 ```
</actions>
The assistant should maintain strict TDD discipline, never writing production code without a failing test first. Hooks provide continuous validation throughout the cycle. Prefer team mode for multi-component features to maximize parallel execution.
