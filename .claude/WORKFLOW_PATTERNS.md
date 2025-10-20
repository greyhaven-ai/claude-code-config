# Workflow Orchestration Patterns

**Last Updated**: 2025-01-17
**Purpose**: Document proven patterns for multi-agent workflow orchestration

---

## Overview

This document catalogs workflow orchestration patterns for coordinating multiple Claude Code agents to accomplish complex software engineering tasks. These patterns enable systematic, reproducible workflows that leverage specialized agents working together.

## Core Principles

### 1. Phase-Based Execution
Break complex workflows into distinct phases with clear validation gates:
- **Sequential Phases**: Each phase completes before next begins
- **Parallel Phases**: Independent work streams execute simultaneously
- **Validation Gates**: Success criteria checked between phases

### 2. Specialized Agent Coordination
Assign tasks to agents based on their strengths:
- **Opus agents**: Complex reasoning, architecture decisions, security
- **Sonnet agents**: Standard implementation, testing, documentation
- **Haiku agents**: Quick operations, scaffolding, context management

### 3. Context Handoff
Explicit context transfer between agents:
- **Input Specification**: What each agent receives
- **Output Definition**: What each agent produces
- **Validation**: Verify output meets next agent's input requirements

### 4. Progressive Disclosure
Minimize token usage while maintaining completeness:
- **Metadata Layer**: Quick reference (agent names, capabilities)
- **Instructions Layer**: What to do (step-by-step guidance)
- **Examples Layer**: How to do it (detailed implementations)

---

## Pattern Catalog

## Pattern 1: Sequential Pipeline

**When to Use**: Linear workflow where each step depends on previous output

**Structure**:
```
Phase 1 → Phase 2 → Phase 3 → ... → Phase N
  ↓         ↓         ↓               ↓
Agent A   Agent B   Agent C         Agent N
```

**Example: TDD Red-Green-Refactor**
```markdown
## Phase 1: Red (Write Failing Test)
**Agent**: tdd-orchestrator
**Input**: Feature requirements
**Output**: Failing test suite
**Validation**: Tests run and fail as expected

## Phase 2: Green (Minimal Implementation)
**Agent**: tdd-python or tdd-typescript
**Input**: Failing tests from Phase 1
**Output**: Passing tests with minimal code
**Validation**: All tests pass

## Phase 3: Refactor (Code Quality)
**Agent**: code-quality-analyzer
**Input**: Working code from Phase 2
**Output**: Refactored, clean code
**Validation**: Tests still pass, quality metrics improved
```

**Benefits**:
- Clear dependencies
- Easy to debug (know exactly where failure occurred)
- Predictable execution time

**Drawbacks**:
- Slower than parallel execution
- Agents wait idle between phases

---

## Pattern 2: Parallel Fan-Out / Fan-In

**When to Use**: Independent work streams that converge

**Structure**:
```
         Phase 1
            ↓
    ┌───────┼───────┐
    ↓       ↓       ↓
 Agent A  Agent B  Agent C  (Parallel)
    ↓       ↓       ↓
    └───────┼───────┘
            ↓
         Phase 3
         Agent D    (Integration)
```

**Example: Full-Stack Feature Development**
```markdown
## Phase 1: Planning
**Agent**: docs-architect
**Output**: API contract, database schema

## Phase 2: Parallel Implementation
### Stream A: Backend
**Agent**: tdd-typescript
**Input**: API contract from Phase 1
**Output**: Implemented API with tests

### Stream B: Frontend
**Agent**: react-tanstack-tester
**Input**: API contract from Phase 1
**Output**: UI components with tests

### Stream C: Database
**Agent**: data-validator
**Input**: Schema from Phase 1
**Output**: Migration and validation

## Phase 3: Integration
**Agent**: test-generator
**Input**: Backend (A), Frontend (B), Database (C)
**Output**: E2E tests, integration validation
```

**Benefits**:
- Faster execution (parallel work)
- Efficient use of multiple agents
- Natural separation of concerns

**Drawbacks**:
- Requires careful coordination
- Integration phase can be complex
- Context aggregation needed

---

## Pattern 3: Incremental Refinement

**When to Use**: Iterative improvement of artifacts

**Structure**:
```
Initial → Refine 1 → Refine 2 → ... → Final
  ↓         ↓          ↓              ↓
Agent A   Agent A    Agent B        Agent C
         (iterate)  (different      (polish)
                     perspective)
```

**Example: Documentation Creation**
```markdown
## Iteration 1: Draft
**Agent**: docs-architect (Opus)
**Input**: Codebase and requirements
**Output**: Draft documentation

## Iteration 2: Technical Review
**Agent**: code-quality-analyzer
**Input**: Draft from Iteration 1
**Output**: Technical accuracy improvements

## Iteration 3: Code Examples
**Agent**: tdd-orchestrator
**Input**: Documentation from Iteration 2
**Output**: Tested code examples added

## Iteration 4: Coverage Validation
**Agent**: docs-architect
**Input**: Enhanced docs from Iteration 3
**Output**: Final documentation with 95%+ coverage
```

**Benefits**:
- Continuous improvement
- Multiple perspectives
- High-quality output

**Drawbacks**:
- Longer execution time
- Potential for scope creep
- Need clear stop criteria

---

## Pattern 4: Multi-Perspective Analysis

**When to Use**: Comprehensive review from different angles

**Structure**:
```
       Input
         ↓
    ┌────┼────┬────┐
    ↓    ↓    ↓    ↓
 View A View B View C View D  (Parallel)
    ↓    ↓    ↓    ↓
    └────┼────┴────┘
         ↓
    Synthesize
```

**Example: Code Review**
```markdown
## Phase 1: Parallel Analysis

### Perspective A: Security
**Agent**: security-analyzer (Opus)
**Focus**: Vulnerabilities, auth, data protection
**Output**: Security findings

### Perspective B: Performance
**Agent**: performance-optimizer
**Focus**: Bottlenecks, caching, queries
**Output**: Performance recommendations

### Perspective C: Code Quality
**Agent**: code-quality-analyzer
**Focus**: Maintainability, complexity, patterns
**Output**: Refactoring suggestions

### Perspective D: Documentation
**Agent**: docs-architect
**Focus**: API docs, comments, examples
**Output**: Documentation gaps

## Phase 2: Synthesis
**Agent**: multi-agent-synthesis-orchestrator
**Input**: All perspectives (A, B, C, D)
**Output**: Prioritized action items
```

**Benefits**:
- Comprehensive coverage
- Leverages specialized expertise
- Identifies issues early

**Drawbacks**:
- Expensive (multiple Opus/Sonnet agents)
- May find conflicting recommendations
- Synthesis phase is critical

---

## Pattern 5: Conditional Branching

**When to Use**: Workflow varies based on conditions

**Structure**:
```
   Phase 1
      ↓
  Condition?
    ↙   ↘
  Yes    No
   ↓      ↓
Path A  Path B
```

**Example: Security Scan with Remediation**
```markdown
## Phase 1: Security Scan
**Agent**: security-analyzer
**Output**: Security findings

## Conditional: Vulnerabilities Found?

### Path A: Vulnerabilities Detected
#### Step A1: Prioritize Issues
**Agent**: security-analyzer
**Output**: Prioritized vulnerability list

#### Step A2: Auto-Remediation
**Agent**: code-quality-analyzer
**Input**: High-priority vulnerabilities
**Output**: Automated fixes applied

#### Step A3: Re-scan
**Agent**: security-analyzer
**Output**: Validation that fixes worked

### Path B: Clean Scan
#### Step B1: Documentation
**Agent**: docs-architect
**Output**: Security compliance documentation
```

**Benefits**:
- Efficient (only run needed steps)
- Handles different scenarios
- Adaptive workflows

**Drawbacks**:
- More complex logic
- Harder to predict execution time
- Need robust condition evaluation

---

## Pattern 6: Hierarchical Decomposition

**When to Use**: Large task breaks into smaller subtasks

**Structure**:
```
      Main Task
         ↓
    ┌────┼────┐
    ↓    ↓    ↓
 Sub 1 Sub 2 Sub 3
    ↓
  ┌─┼─┐
  ↓ ↓ ↓
Sub 1a 1b 1c
```

**Example: Microservice Development**
```markdown
## Level 1: Service Design
**Agent**: docs-architect (Opus)
**Output**: Service architecture, API contracts

## Level 2: Component Implementation (Parallel)

### Component A: Authentication Service
#### Sub-task A1: User Registration
**Agent**: tdd-typescript
**Output**: Registration endpoint + tests

#### Sub-task A2: Login/Logout
**Agent**: tdd-typescript
**Output**: Auth endpoints + tests

#### Sub-task A3: Token Management
**Agent**: tdd-typescript
**Output**: JWT handling + tests

### Component B: Data Service
[Similar breakdown]

### Component C: Notification Service
[Similar breakdown]

## Level 3: Integration
**Agent**: test-generator
**Output**: Service integration tests
```

**Benefits**:
- Manageable complexity
- Parallel execution at each level
- Clear progress tracking

**Drawbacks**:
- Requires upfront decomposition
- Coordination overhead
- Deep nesting can be confusing

---

## Pattern 7: Continuous Validation

**When to Use**: Quality gates throughout workflow

**Structure**:
```
Step 1 → Validate → Step 2 → Validate → Step 3
   ↓        ↓         ↓         ↓         ↓
Agent A  Validator  Agent B  Validator  Agent C
                 ↓ (fail)      ↓ (fail)
                Rollback      Rollback
```

**Example: Deployment Pipeline**
```markdown
## Step 1: Code Commit
**Agent**: tdd-orchestrator
**Output**: New feature code

## Validation 1: Test Suite
**Validator**: Automated tests
**Pass**: Proceed to Step 2
**Fail**: Rollback, fix tests

## Step 2: Security Scan
**Agent**: security-analyzer
**Output**: Security assessment

## Validation 2: No Critical Vulnerabilities
**Validator**: Security threshold check
**Pass**: Proceed to Step 3
**Fail**: Rollback, remediate issues

## Step 3: Staging Deployment
**Agent**: Deployment automation
**Output**: Deployed to staging

## Validation 3: Health Checks
**Validator**: Observability metrics
**Pass**: Proceed to production
**Fail**: Rollback deployment

## Step 4: Production Deployment
**Agent**: Deployment automation
**Output**: Deployed to production
```

**Benefits**:
- Early failure detection
- Quality enforcement
- Automated rollback

**Drawbacks**:
- Slower execution
- More validation logic needed
- Can be overly conservative

---

## Pattern 8: Context Accumulation

**When to Use**: Build comprehensive context across phases

**Structure**:
```
Phase 1 → Context Store → Phase 2 → Context Store → Phase 3
   ↓           ↑            ↓           ↑            ↓
Agent A     Context      Agent B     Context      Agent C
          (accumulate)             (accumulate)
```

**Example: Feature Development with Documentation**
```markdown
## Phase 1: Implementation
**Agent**: tdd-typescript
**Output**: Feature code + tests
**Context Stored**:
- API endpoints added
- Database changes
- New dependencies

## Phase 2: Documentation
**Agent**: docs-architect
**Input**: Implementation + Context (Phase 1)
**Output**: API documentation
**Context Added**:
- OpenAPI spec
- Code examples
- Migration guide

## Phase 3: Integration Guide
**Agent**: onboarding-coordinator
**Input**: Full context (Phases 1 + 2)
**Output**: Developer integration guide
**Context Complete**:
- Implementation details
- API documentation
- Setup instructions
- Troubleshooting guide
```

**Benefits**:
- Comprehensive artifacts
- Knowledge preservation
- Easier handoffs

**Drawbacks**:
- Context can grow large
- May duplicate information
- Storage management needed

---

## Implementation Guidelines

### 1. Define Clear Phases

```yaml
# workflow-template.yml
phases:
  - id: phase-1
    name: "Requirements Analysis"
    type: sequential
    agent: docs-architect
    input:
      - linear_issue_id
    output:
      - requirements_doc
      - api_contract
    success_criteria:
      - requirements_complete
      - stakeholder_approval

  - id: phase-2
    name: "Parallel Implementation"
    type: parallel
    streams:
      - id: backend
        agent: tdd-typescript
        input: ${phase-1.api_contract}
        output: backend_implementation

      - id: frontend
        agent: react-tanstack-tester
        input: ${phase-1.api_contract}
        output: frontend_components
```

### 2. Specify Context Handoff

```typescript
// Phase output specification
interface PhaseOutput {
  phase: string;
  agent: string;
  timestamp: Date;
  artifacts: {
    files: string[];
    documentation: string[];
    tests: string[];
  };
  metadata: {
    coverage: number;
    quality_score: number;
    warnings: string[];
  };
}

// Next phase uses output
interface PhaseInput {
  previous_phase: PhaseOutput;
  additional_context?: any;
}
```

### 3. Validate Between Phases

```typescript
function validatePhaseOutput(output: PhaseOutput, criteria: SuccessCriteria): ValidationResult {
  const results = [];

  for (const criterion of criteria) {
    const result = criterion.validate(output);
    results.push(result);
  }

  return {
    passed: results.every(r => r.passed),
    failures: results.filter(r => !r.passed),
    warnings: results.filter(r => r.warning)
  };
}
```

### 4. Handle Errors Gracefully

```typescript
async function executeWorkflow(workflow: Workflow): Promise<WorkflowResult> {
  const results = [];

  for (const phase of workflow.phases) {
    try {
      const output = await executePhase(phase);
      const validation = validatePhaseOutput(output, phase.success_criteria);

      if (!validation.passed) {
        // Rollback or retry
        if (phase.retry_on_failure) {
          output = await retryPhase(phase);
        } else {
          return {
            status: 'failed',
            failed_phase: phase.id,
            error: validation.failures
          };
        }
      }

      results.push(output);

    } catch (error) {
      // Handle unexpected errors
      if (phase.rollback_on_error) {
        await rollbackPhases(results);
      }

      return {
        status: 'error',
        failed_phase: phase.id,
        error
      };
    }
  }

  return {
    status: 'success',
    results
  };
}
```

---

## Best Practices

### 1. Start Simple, Add Complexity

Begin with sequential pipeline, add parallelism only when beneficial:
```
❌ Don't start with: Complex 7-phase parallel workflow
✅ Start with: 3-phase sequential pipeline
✅ Then add: Parallel streams where independent
```

### 2. Make Validation Explicit

Every phase should have clear success criteria:
```yaml
success_criteria:
  - name: "Tests pass"
    validator: "pytest --cov=80"
  - name: "No security issues"
    validator: "bandit -r src/"
  - name: "Code quality"
    validator: "pylint src/ --fail-under=8.0"
```

### 3. Optimize Agent Selection

Use the right model for each task:
```
Opus  → Architecture, security, incident response
Sonnet → Implementation, testing, documentation
Haiku  → Scaffolding, quick operations, context management
```

### 4. Document Context Flow

Make it explicit what each phase receives and produces:
```markdown
## Phase 2: Backend Implementation
**Input**:
- API contract (OpenAPI spec) from Phase 1
- Database schema from Phase 1
- Security requirements from Phase 1

**Output**:
- Implemented API endpoints (TypeScript + Hono)
- Test suite (Vitest) with 80%+ coverage
- API documentation (auto-generated from code)
```

### 5. Enable Debugging

Add logging and checkpoints:
```typescript
// Log phase transitions
console.log(`Starting ${phase.name} (${phase.id})`);
console.log(`Agent: ${phase.agent}`);
console.log(`Input: ${JSON.stringify(phase.input)}`);

// Save intermediate artifacts
await saveArtifact(`${phase.id}_output.json`, output);

// Log completion
console.log(`Completed ${phase.name}: ${validation.passed ? 'PASS' : 'FAIL'}`);
```

---

## Common Workflow Templates

We've created templates for common scenarios in `.claude/workflow-templates/`:

1. **full-stack-feature.md** - Complete feature from design to deployment
2. **security-hardening.md** (to be created) - Security audit and remediation
3. **refactoring-workflow.md** (to be created) - Systematic code refactoring
4. **deployment-pipeline.md** (to be created) - Automated deployment with validation

---

## Metrics to Track

Monitor workflow effectiveness:

**Execution Metrics**:
- Phase execution time
- Total workflow duration
- Parallel efficiency (time saved vs sequential)

**Quality Metrics**:
- Validation pass rate
- Rollback frequency
- Error rate by phase

**Efficiency Metrics**:
- Agent utilization
- Token usage per phase
- Cost per workflow

---

## Conclusion

Effective workflow orchestration requires:
- Clear phase boundaries
- Explicit context handoff
- Validation gates
- Appropriate agent selection
- Error handling

Start with simple patterns and add complexity as needed. Document your workflows so they're reproducible and improvable.

---

**Next**: Apply these patterns to create team-specific workflows in `.claude/workflow-templates/`.
