---
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Grep, Glob, Task, TodoWrite, Teammate, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet
description: Comprehensive quality check pipeline leveraging multiple subagents
argument-hint: [file-pattern or directory]
---

Execute comprehensive quality pipeline for: $ARGUMENTS

<ultrathink>
Quality is not negotiable. Every line of code deserves scrutiny. Leverage the full power of our subagent and hook ecosystem.
</ultrathink>

<megaexpertise type="quality-assurance-orchestrator">
The assistant should orchestrate multiple specialized subagents in sequence, with hooks providing continuous validation and enhancement throughout the pipeline.
</megaexpertise>

<context>
Running quality pipeline on: $ARGUMENTS
Need comprehensive analysis across security, performance, clarity, and testing
Hooks will enhance each stage of the process
</context>

<requirements>
- Security vulnerability scanning
- Code clarity and maintainability analysis
- Performance bottleneck identification
- Test coverage assessment
- Documentation completeness check
- Automated fixes where safe
- Comprehensive report generation
</requirements>

<actions>
1. **Initialize Pipeline with TodoWrite**:
   - Create checklist of quality checks
   - Track progress through pipeline stages

2. **Mode Detection**:
   - Check if `Teammate` tool is available
   - If available AND target spans multiple files/modules: use **Team Mode**
   - Otherwise: use **Subagent Mode** (existing sequential pipeline)
   - Announce: "Using **Team Mode** — parallel quality analysis." or "Using **Subagent Mode** — sequential quality pipeline."

3. **Team Mode Workflow** (when Teammate is available):

   a. **Create Team**:
      ```
      Teammate(spawnTeam) with name: quality-{target-slug}
      ```

   b. **Create Task Board**:
      ```
      Layer 0 (parallel analysis — all independent):
        - security-rev: Security vulnerability scanning
        - quality-rev: Code clarity and maintainability analysis
        - perf-rev: Performance bottleneck identification

      Layer 1 (sequential — blocked by all Layer 0):
        - test-gen: Test coverage assessment + gap filling (if coverage < 80%)

      Layer 2 (sequential — blocked by Layer 1):
        - doc-update: Documentation completeness check

      Layer 3 (synthesis — blocked by all above):
        - Orchestrator generates unified quality report
      ```

   c. **Spawn Teammates**:
      | Teammate | Agent Type | Focus | Plan Required |
      |----------|-----------|-------|---------------|
      | security-rev | `core:code-quality-analyzer` | Security mode (OWASP Top 10) | No |
      | quality-rev | `core:code-quality-analyzer` | Clarity mode (readability rules) | No |
      | perf-rev | `core:performance-optimizer` | Performance analysis | No |
      | test-gen | `testing:test-generator` | Test coverage gaps | No |
      | doc-update | `research:tech-docs-maintainer` | Documentation updates | No |

      Spawn prompt template:
      ```
      You are {role} on the quality-{target-slug} team.

      ANALYSIS FOCUS: {specific quality dimension}
      TARGET: {files/directories being analyzed}

      Report findings via SendMessage to the orchestrator when complete.
      Your current task: see TaskList for your assigned tasks.
      ```

   d. **Monitor & Synthesize**:
      - Track task completion via `TaskList`
      - Unblock Layer 1 when all Layer 0 tasks complete
      - Collect all findings for unified report

   e. **Cleanup**:
      - Send `shutdown_request` to all teammates
      - Call `Teammate(cleanup)`

4. **Subagent Mode Workflow** (fallback — existing sequential pipeline):

   1. **Stage 1: Security Audit**:
      - Invoke security-analyzer subagent (direct analysis mode)
      - Hooks: security-validator will flag critical issues
      - Generate security scorecard

   2. **Stage 2: Code Review**:
      - Invoke code-quality-analyzer subagent (security & quality review mode)
      - Hooks: post-edit-validator ensures standards
      - Document code quality issues

   3. **Stage 3: Performance Analysis**:
      - Invoke performance-optimizer subagent
      - Hooks: performance-monitor tracks metrics
      - Identify optimization opportunities

   4. **Stage 4: Code Clarity**:
      - Invoke code-quality-analyzer subagent (clarity refactoring mode)
      - Apply 10 refactoring rules
      - Hooks validate refactoring safety

   5. **Stage 5: Test Coverage**:
      - Invoke test-generator subagent if coverage < 80%
      - Generate missing test cases
      - Hooks: test-runner validates new tests

   6. **Stage 6: Documentation**:
      - Invoke tech-docs-maintainer subagent
      - Update both @documentation and .claude directories
      - Ensure code changes are documented

5. **Generate Quality Report**:
   ```markdown
   # Quality Pipeline Report

   ## Orchestration
   - Mode: Team Mode / Subagent Mode
   - Teammates spawned: X (if team mode)
   - Parallel analysis time saved: ~Y% (if team mode)

   ## Security Score: X/100
   - Critical issues: X
   - High priority: Y
   - Resolved automatically: Z

   ## Code Quality: X/100
   - Complexity reduced: X%
   - Dead code removed: Y lines
   - Clarity improvements: Z refactorings

   ## Performance: X/100
   - Bottlenecks found: X
   - Optimizations applied: Y
   - Speed improvement: Z%

   ## Test Coverage: X%
   - Tests added: X
   - Coverage increased: +Y%

   ## Documentation: X% complete
   - Files documented: X/Y
   - API docs updated: [OK]/[X]
   ```

6. **Hook Integration Points**:
   - Pre-tool hooks prepare context for each subagent
   - Post-tool hooks validate changes
   - Session hooks track overall pipeline progress
</actions>

The assistant should treat this as a comprehensive quality gate, leveraging the full ecosystem of subagents and hooks to ensure code meets the highest standards before deployment.
