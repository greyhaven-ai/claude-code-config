---
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Grep, Glob, Task, TodoWrite, Teammate, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet
description: Complete feature development cycle with dynamic agent selection based on technology stack
argument-hint: [feature description or requirements]
---

Implement complete feature cycle: $ARGUMENTS

<ultrathink>
Features need the full cycle: design, implement, test, optimize, document. Let the codebase tell us which agents to invoke.
</ultrathink>

<megaexpertise type="adaptive-feature-orchestrator">
The assistant should dynamically select and chain agents based on detected technology stack and feature requirements.
</megaexpertise>

<context>
Implementing feature: $ARGUMENTS
Will detect tech stack and dynamically select appropriate agents
Each phase builds on previous, with intelligent handoffs
</context>

<requirements>
- Technology stack detection
- Appropriate agent selection per stack
- Full development cycle coverage
- Quality gates between phases
- Comprehensive documentation
</requirements>

<actions>
1. **Technology Stack Detection**:
   ```bash
   # Detect frontend framework
   if grep -q '"react"' package.json 2>/dev/null; then
     FRONTEND="react"
     if grep -q '@tanstack' package.json; then
       FRONTEND="react-tanstack"
     fi
   elif grep -q '"vue"' package.json 2>/dev/null; then
     FRONTEND="vue"
   elif grep -q '"angular"' package.json 2>/dev/null; then
     FRONTEND="angular"
   fi

   # Detect backend
   if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
     BACKEND="python"
   elif [ -f "package.json" ]; then
     BACKEND="node"
   elif [ -f "go.mod" ]; then
     BACKEND="go"
   fi

   # Detect testing framework
   if grep -q '"vitest"' package.json 2>/dev/null; then
     TEST_FRAMEWORK="vitest"
   elif grep -q '"jest"' package.json 2>/dev/null; then
     TEST_FRAMEWORK="jest"
   elif grep -q 'pytest' requirements.txt 2>/dev/null; then
     TEST_FRAMEWORK="pytest"
   fi
   ```

1b. **Mode Detection**:
    - Check if `Teammate` tool is available
    - If available: use **Team Mode** for Phase 3 (parallel quality) and Phase 6 (parallel docs)
    - Otherwise: use **Subagent Mode** (existing sequential pipeline)
    - Announce: "Using **Team Mode** — parallelizing quality and documentation phases." or "Using **Subagent Mode** — sequential feature cycle."
    - **IMPORTANT**: Do NOT create a team for Phase 2 (TDD Implementation). Phase 2 delegates to `tdd-orchestrator`, which manages its own team internally. Avoid nested teams.

1c. **Team Mode — Phase 3: Parallel Code Quality** (replaces sequential Phase 3):

    When in Team Mode, run the 3 independent quality passes in parallel:

    a. **Create Team**:
       ```
       Teammate(spawnTeam) with name: quality-{feature-slug}
       ```

    b. **Create Task Board**:
       ```
       Layer 0 (parallel — 3 independent quality passes):
         - security-rev: code-quality-analyzer (security mode)
         - clarity-rev: code-quality-analyzer (clarity mode)
         - synthesis-rev: code-quality-analyzer (synthesis mode)

       Layer 1 (synthesis — blocked by all Layer 0):
         - Orchestrator merges quality findings and applies fixes
       ```

    c. **Spawn Teammates**:
       | Teammate | Agent Type | Focus | Plan Required |
       |----------|-----------|-------|---------------|
       | security-rev | `core:code-quality-analyzer` | Security vulnerabilities (OWASP) | No |
       | clarity-rev | `core:code-quality-analyzer` | Code clarity and readability | No |
       | synthesis-rev | `core:code-quality-analyzer` | Cross-file consistency | No |

    d. **Monitor & Merge**: Collect all findings, apply fixes, cleanup team.

1d. **Team Mode — Phase 6: Parallel Documentation** (replaces sequential Phase 6):

    When in Team Mode, run the 3 independent doc tasks in parallel:

    a. **Create Team** (or reuse existing if Phase 3 team was already created):
       ```
       Teammate(spawnTeam) with name: docs-{feature-slug}
       ```

    b. **Create Task Board**:
       ```
       Layer 0 (parallel — 3 independent doc tasks):
         - docs-maintainer: Update API and technical documentation
         - diff-documenter: Document code changes from git diff
         - web-researcher: Validate against best practices

       Layer 1 (synthesis — blocked by all Layer 0):
         - Orchestrator merges documentation updates
       ```

    c. **Spawn Teammates**:
       | Teammate | Agent Type | Focus | Plan Required |
       |----------|-----------|-------|---------------|
       | docs-maintainer | `research:tech-docs-maintainer` | API docs, technical docs | No |
       | diff-documenter | `core:git-diff-documenter` | Change documentation | No |
       | web-researcher | `research:web-docs-researcher` | Best practices validation | No |

    d. **Monitor & Merge**: Collect all doc updates, cleanup team.

2. **Dynamic Agent Selection Matrix**:
   ```
   DETECTED STACK → AGENT SELECTION:

   react-tanstack + vitest:
     → tdd-typescript → react-tanstack-tester → performance-optimizer

   python + pytest:
     → tdd-python → test-generator → code-quality-analyzer

   node + no-tests:
     → test-generator → tdd-typescript → code-quality-analyzer

   unknown-stack:
     → code-synthesis-analyzer → test-generator → tech-docs-maintainer
   ```

**Subagent Mode Phases** (when Team Mode is unavailable, execute phases sequentially as below):

3. **Phase 1: Design & Planning** (always runs):
   - If complex feature: Invoke multi-agent-synthesis-orchestrator
     * Task: "Research best practices for implementing $ARGUMENTS"
   - Else: Use sequential-thinking for design
     * Task: "Design implementation approach for $ARGUMENTS"
   - Create implementation plan with TodoWrite

4. **Phase 2: TDD Implementation** (stack-specific):
   ```python
   # Dynamic agent selection based on detected stack
   if FRONTEND == "react-tanstack":
       invoke_agent("tdd-typescript",
                   "Implement $ARGUMENTS using React with TanStack libraries, Vite, and Vitest")
       invoke_agent("react-tanstack-tester",
                   "Create comprehensive tests for TanStack Query/Router components")

   elif BACKEND == "python":
       invoke_agent("tdd-python",
                   "Implement $ARGUMENTS using Python with pytest following TDD")

   else:
       # Fallback to generic TDD
       invoke_agent("test-generator",
                   "Generate test structure for $ARGUMENTS")
       # Then implement based on tests
   ```

5. **Phase 3: Code Quality** (conditional chaining):
   - First pass: code-quality-analyzer (security mode)
     * If security issues found → fix → re-run
   - Second pass: code-quality-analyzer (clarity mode)
     * If complexity > threshold → refactor
   - Third pass: code-quality-analyzer (synthesis mode)
     * If inconsistencies found → harmonize

6. **Phase 4: Performance** (conditional):
   ```python
   # Only run performance chain if:
   # - Feature involves data processing
   # - Feature has UI components
   # - Feature handles concurrent requests

   if needs_performance_optimization:
       # Chain performance agents
       invoke_agent("memory-profiler",
                   "Profile memory for new feature: $ARGUMENTS")
       # Pass results to next agent
       invoke_agent("performance-optimizer",
                   "Optimize based on profiling: [memory-profiler results]")
   ```

7. **Phase 5: Testing** (adaptive):
   - If TEST_FRAMEWORK == "vitest" and FRONTEND == "react-tanstack":
     * Use react-tanstack-tester for integration tests
   - If coverage < 80%:
     * Chain test-generator to fill gaps
   - If performance-critical:
     * Add performance regression tests

8. **Phase 6: Documentation** (comprehensive):
   - Chain documentation agents with context accumulation:
     ```
     tech-docs-maintainer (API docs) →
     git-diff-documentation-agent (change docs) →
     web-docs-researcher (best practices validation)
     ```

9. **Intelligent Handoffs**:
   ```markdown
   ## Agent Context Handoff Protocol

   Each agent passes forward:
   - What was implemented/changed
   - Decisions made and rationale
   - Warnings or concerns for next agent
   - Suggested focus areas

   Example handoff:
   "tdd-typescript completed UserProfile component with 95% coverage.
   Note: Used TanStack Query for data fetching.
   Concern: Potential N+1 query in user posts.
   Suggest: performance-optimizer focus on query batching."
   ```

10. **Dynamic Branching**:
    ```python
    # Based on feature type, branch to specialized flows

    if "api" in feature_description:
        chain.append("api-tester")
        chain.append("api-docs-generator")

    if "database" in feature_description:
        chain.append("database-migration-handler")
        chain.append("query-optimizer")

    if "ui" in feature_description:
        chain.append("ui-component-tester")
        chain.append("accessibility-checker")
    ```

11. **Final Report with Full Context**:
    ```markdown
    # Feature Implementation Report

    ## Orchestration
    - Mode: Team Mode / Subagent Mode
    - Phase 3 teammates: {count} (if team mode)
    - Phase 6 teammates: {count} (if team mode)
    - Nested teams avoided: Phase 2 delegated to tdd-orchestrator's own team

    ## Technology Stack Detected
    - Frontend: React with TanStack (Vite)
    - Backend: Node.js
    - Testing: Vitest

    ## Agent Execution Chain
    1. multi-agent-synthesis-orchestrator → Design document created
    2. tdd-typescript → 15 tests written, all passing
    3. react-tanstack-tester → Component tests added
    4. code-quality-analyzer → 3 security fixes applied
    5. performance-optimizer → Reduced bundle size by 30%
    6. tech-docs-maintainer → API docs updated

    ## Context Flow Summary
    - Design identified need for real-time updates
    - TDD implementation used TanStack Query subscriptions
    - Testing revealed race condition, fixed in iteration 2
    - Quality analysis suggested memoization, applied
    - Performance testing confirmed 50ms response time
    - Documentation includes subscription lifecycle
    ```
</actions>

The assistant should let the codebase guide agent selection, creating an adaptive chain that fits the specific technology stack and feature requirements. Each agent should build on previous context for comprehensive feature delivery.
