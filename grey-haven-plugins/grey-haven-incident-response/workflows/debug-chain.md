---
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Grep, Task, TodoWrite, WebSearch
description: Intelligent debugging chain that adapts based on bug characteristics
argument-hint: [bug description or error message]
---

Debug with intelligent agent chaining: $ARGUMENTS

<ultrathink>
Bugs hide in patterns. Different bugs need different specialists. Let the symptoms guide the investigation chain.
</ultrathink>

<megaexpertise type="adaptive-debugging-orchestrator">
The assistant should analyze bug characteristics and dynamically chain appropriate debugging specialists.
</megaexpertise>

<context>
Debugging issue: $ARGUMENTS
Will analyze symptoms and select appropriate agent chain
Each agent provides clues for next agent selection
</context>

<requirements>
- Bug characteristic analysis
- Dynamic specialist selection
- Progressive investigation depth
- Root cause identification
- Fix validation chain
</requirements>

<actions>
1. **Initial Bug Analysis**:
   ```python
   # Analyze bug characteristics from description/error
   bug_characteristics = {
       "memory_related": ["memory", "leak", "heap", "allocation", "oom"],
       "performance": ["slow", "timeout", "hanging", "freeze", "lag"],
       "concurrency": ["race", "deadlock", "thread", "async", "concurrent"],
       "api_related": ["404", "500", "cors", "fetch", "request", "response"],
       "state_related": ["state", "redux", "context", "undefined", "null"],
       "type_related": ["type error", "cannot read", "undefined is not"],
       "security": ["injection", "xss", "csrf", "auth", "permission"],
       "data": ["database", "query", "migration", "constraint", "foreign key"]
   }
   
   detected_categories = analyze_bug_text($ARGUMENTS, bug_characteristics)
   ```

2. **Dynamic Chain Construction**:
   ```
   SYMPTOM-BASED AGENT CHAINS:
   
   Memory Issues:
   memory-profiler → code-synthesis-analyzer → performance-optimizer
   
   Type Errors (React/TypeScript):
   react-tanstack-tester → tdd-typescript → code-quality-analyzer
   
   Performance Problems:
   performance-optimizer → memory-profiler → test-generator (benchmarks)
   
   Security Vulnerabilities:
   security-analyzer → code-quality-analyzer (security mode) → test-generator (security tests)
   
   Unknown/Complex:
   multi-agent-synthesis-orchestrator → [dynamic based on findings]
   ```

3. **Phase 1: Broad Investigation**:
   - If error message exists:
     * Invoke web-docs-researcher: "Research error: $ARGUMENTS"
     * Capture: Known issues, common causes, solutions
   
   - If no clear error:
     * Invoke code-synthesis-analyzer: "Analyze potential issues in code related to: $ARGUMENTS"
     * Capture: Code smells, inconsistencies, suspicious patterns

4. **Phase 2: Specialized Deep Dive** (based on Phase 1):
   ```python
   # Dynamic agent selection based on initial findings
   
   if "memory leak detected" in phase1_findings:
       # Memory leak chain
       agents = [
           ("memory-profiler", "Deep profile memory allocations"),
           ("performance-optimizer", "Fix memory leaks found"),
           ("test-generator", "Create memory leak regression tests")
       ]
   
   elif "type mismatch" in phase1_findings:
       # Type error chain (TypeScript/React)
       agents = [
           ("tdd-typescript", "Fix type errors with proper typing"),
           ("react-tanstack-tester", "Verify component type safety"),
           ("code-quality-analyzer", "Ensure type consistency")
       ]
   
   elif "race condition suspected" in phase1_findings:
       # Concurrency chain
       agents = [
           ("code-synthesis-analyzer", "Identify async flow issues"),
           ("test-generator", "Create concurrency tests"),
           ("code-quality-analyzer", "Refactor for thread safety")
       ]
   
   else:
       # Fallback comprehensive chain
       agents = [
           ("multi-agent-synthesis-orchestrator", "Comprehensive bug analysis"),
           ("code-quality-analyzer", "Full code review"),
           ("test-generator", "Create reproducing tests")
       ]
   
   # Execute chain with context passing
   for agent, task in agents:
       context = previous_agent_output
       invoke_agent(agent, f"{task}. Previous findings: {context}")
   ```

5. **Phase 3: Root Cause Synthesis**:
   - Collect all agent findings
   - Use sequential-thinking to synthesize root cause:
     ```
     "Given these findings from multiple agents:
      1. Memory profiler: Found leak in event listeners
      2. Code analyzer: Missing cleanup in useEffect
      3. Test generator: Created failing test reproducing issue
      
      What is the root cause and optimal fix?"
     ```

6. **Phase 4: Fix Implementation Chain**:
   ```python
   # Based on root cause, chain fix agents
   
   if root_cause == "missing_cleanup":
       fix_chain = [
           ("code-quality-analyzer", "Add cleanup to React components"),
           ("react-tanstack-tester", "Verify cleanup works"),
           ("git-diff-documentation-agent", "Document the fix")
       ]
   
   elif root_cause == "algorithm_inefficiency":
       fix_chain = [
           ("performance-optimizer", "Optimize algorithm"),
           ("test-generator", "Create performance benchmarks"),
           ("tech-docs-maintainer", "Document complexity improvement")
       ]
   ```

7. **Phase 5: Validation Chain**:
   - Always run after fix:
     ```
     1. test-generator → "Create regression test for bug"
     2. code-quality-analyzer → "Verify fix doesn't introduce issues"
     3. performance-optimizer → "Ensure no performance regression"
     ```

8. **Conditional Branching Logic**:
   ```python
   # Mid-chain decisions based on findings
   
   def continue_chain(current_findings):
       if "external_api_issue" in current_findings:
           # Branch to API specialists
           return ["web-docs-researcher", "api-mock-creator"]
       
       elif "database_deadlock" in current_findings:
           # Branch to database specialists
           return ["database-analyzer", "query-optimizer"]
       
       elif "third_party_bug" in current_findings:
           # Research workarounds
           return ["web-docs-researcher", "workaround-implementer"]
       
       else:
           # Continue main chain
           return None
   ```

9. **Learning Feedback Loop**:
   ```markdown
   ## Bug Pattern Learning
   
   After successful debug:
   1. Record: Bug type → Successful agent chain
   2. Update: Agent router patterns for better future selection
   3. Document: Add to .claude/debugging/ knowledge base
   
   Example learning:
   "useEffect cleanup issues" → [react-tanstack-tester, code-quality-analyzer]
   Confidence: 0.9 (worked 9/10 times)
   ```

10. **Comprehensive Debug Report**:
    ```markdown
    # Intelligent Debug Report
    
    ## Bug Characteristics
    - Category: Memory leak in React component
    - Symptoms: Increasing memory on route changes
    - Severity: High
    
    ## Agent Chain Executed
    1. web-docs-researcher → Found: Common useEffect cleanup issue
    2. memory-profiler → Confirmed: 50MB leak per navigation
    3. react-tanstack-tester → Identified: Missing cleanup in 3 components
    4. code-quality-analyzer → Fixed: Added cleanup functions
    5. test-generator → Created: Memory leak regression tests
    
    ## Root Cause
    Event listeners and subscriptions not cleaned up in useEffect
    
    ## Fix Applied
    ```javascript
    useEffect(() => {
      const handler = () => {};
      window.addEventListener('resize', handler);
      return () => window.removeEventListener('resize', handler); // Added
    }, []);
    ```
    
    ## Validation Results
    - Memory leak: Fixed [OK]
    - Tests: 5 new tests, all passing [OK]
    - Performance: No regression [OK]
    - Code quality: Improved [OK]
    ```

11. **Meta-Learning from Chain**:
    - Save successful chains for similar bugs
    - Update agent selection confidence scores
    - Refine bug characteristic patterns
    - Improve future chain construction
</actions>

The assistant should treat debugging as an adaptive investigation, where each clue determines the next specialist to consult, building a complete understanding through intelligent agent orchestration.