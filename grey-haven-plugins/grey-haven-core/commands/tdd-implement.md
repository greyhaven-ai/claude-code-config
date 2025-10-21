---
allowed-tools: Read, Write, MultiEdit, Bash, Grep, Task, TodoWrite
description: Implement feature using strict TDD methodology with red-green-refactor cycle
argument-hint: [feature description or requirements]
---
Implement with TDD: $ARGUMENTS
<ultrathink>
Test-Driven Development is the path to quality. Red, Green, Refactor. No shortcuts. Tests drive design.
</ultrathink>
<megaexpertise type="tdd-practitioner">
The assistant should follow strict TDD methodology, leveraging the tdd-python-implementer subagent and hook ecosystem to ensure proper test-first development.
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
 ```bash
# Check for Python test framework
 grep -E "pytest|unittest" requirements.txt pyproject.toml setup.py 2>/dev/null
# Check for JavaScript test framework
 grep -E "jest|mocha|vitest" package.json 2>/dev/null
# Find test directory structure
 find . -type d -name "test*" -o -name "*test*" | head -5
 ```
3. **Invoke TDD Subagent**:
 - For Python: Use tdd-python-implementer subagent
 - For JavaScript: Use test-generator subagent with TDD approach
 - Provide clear requirements and test scenarios
4. **TDD Cycle Execution**:
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
5. **Coverage Tracking**:
 - Hook: coverage-reporter tracks progress
 - Ensure each new feature has tests
 - Target: >90% coverage for new code
6. **Test Quality Validation**:
 - Tests are independent and isolated
 - Tests run fast (<100ms per unit test)
 - Tests have clear assertions
 - Tests document behavior
7. **Integration with CI/CD**:
 ```yaml
# Example GitHub Actions integration
 - name: Run TDD Tests
 run: |
 pytest tests/ -v --cov=src --cov-report=term-missing
# or
 bun test --coverage
 ```
8. **Documentation Generation**:
 - Generate test documentation
 - Create examples from test cases
 - Update README with test instructions
9. **TDD Report**:
 ```markdown
## TDD Implementation Report
### Test Statistics
 - Tests written: X
 - Tests passing: X/X (100%)
 - Coverage achieved: X%
### Red-Green-Refactor Cycles
 - Cycles completed: X
 - Average cycle time: Y minutes
### Code Quality
 - Functions tested: X/Y
 - Edge cases covered: ✓
 - Error scenarios tested: ✓
### Next Steps
 - [ ] Integration tests
 - [ ] Performance tests
 - [ ] Documentation updates
 ```
</actions>
The assistant should maintain strict TDD discipline, never writing production code without a failing test first. Hooks provide continuous validation throughout the cycle.