---
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Grep, Task, TodoWrite
description: Chain performance analysis, optimization, and validation agents
argument-hint: [file-pattern or critical code path]
---

Execute performance optimization chain for: $ARGUMENTS

<ultrathink>
Performance is a journey: measure, analyze, optimize, validate. Each agent builds on the previous one's findings.
</ultrathink>

<megaexpertise type="performance-chain-orchestrator">
The assistant should chain multiple specialized agents, passing context between them for comprehensive performance optimization.
</megaexpertise>

<context>
Optimizing performance for: $ARGUMENTS
Need to chain agents intelligently, passing findings between them
Each agent should build on previous discoveries
</context>

<requirements>
- Performance profiling and bottleneck detection
- Memory usage analysis
- Optimization implementation
- Regression testing
- Documentation of improvements
</requirements>

<actions>
1. **Chain Setup with Context Passing**:
   ```
   CHAIN FLOW:
   memory-profiler → performance-optimizer → test-generator → tech-docs-maintainer
   
   Each agent receives context from previous:
   - Memory hotspots → Target for optimization
   - Optimizations made → Tests to write
   - Tests written → Documentation to update
   ```

2. **Stage 1: Memory Analysis**:
   - Invoke memory-profiler subagent with specific focus
   - Task prompt: "Profile memory usage for $ARGUMENTS, identify leaks and inefficient allocations"
   - Capture output: memory hotspots, leak locations, allocation patterns
   - Pass findings to next agent via context

3. **Stage 2: Performance Optimization** (using context from Stage 1):
   - Invoke performance-optimizer subagent
   - Task prompt: "Optimize the following memory hotspots found: [context from Stage 1]. Focus on $ARGUMENTS"
   - Apply optimizations based on memory findings:
     * Reduce allocations in hot paths
     * Implement object pooling where beneficial
     * Optimize data structures based on usage patterns
   - Capture: optimization techniques applied, expected improvements

4. **Stage 3: Regression Test Generation** (using context from Stage 2):
   - Invoke test-generator subagent
   - Task prompt: "Generate performance regression tests for optimizations: [context from Stage 2]. Ensure optimizations in $ARGUMENTS remain effective"
   - Create tests that:
     * Benchmark critical paths
     * Verify memory improvements persist
     * Test edge cases that might degrade performance
   - Capture: test coverage, benchmark baselines

5. **Stage 4: Documentation Update** (using context from all stages):
   - Invoke tech-docs-maintainer subagent
   - Task prompt: "Document performance improvements: Memory analysis showed [Stage 1], optimizations applied [Stage 2], tests added [Stage 3] for $ARGUMENTS"
   - Update:
     * Performance documentation
     * Optimization rationale
     * Benchmark results
     * Maintenance guidelines

6. **Dynamic Agent Selection**:
   ```python
   # Based on findings, dynamically select additional agents
   if "database_queries" in performance_issues:
       # Chain in a database optimization specialist
       invoke_agent("database-query-optimizer")
   
   if "react_rendering" in performance_issues:
       # Chain in React-specific optimizer
       invoke_agent("react-tanstack-tester", mode="performance")
   
   if "api_latency" in performance_issues:
       # Chain in API optimization
       invoke_agent("api-performance-analyzer")
   ```

7. **Context Accumulation Report**:
   ```markdown
   # Performance Optimization Chain Report
   
   ## Chain Execution Path
   1. memory-profiler → Found: 3 memory leaks, 5 inefficient allocations
   2. performance-optimizer → Applied: Object pooling, lazy loading, memoization
   3. test-generator → Created: 12 regression tests, 5 benchmarks
   4. tech-docs-maintainer → Updated: 3 doc files, added performance guide
   
   ## Cumulative Improvements
   - Memory usage: -45% (from 512MB to 281MB)
   - Response time: -60% (from 1.2s to 480ms)
   - Throughput: +120% (from 1000 to 2200 req/s)
   
   ## Context Flow
   - Memory profiler identified HashMap overhead
   - Optimizer switched to array-based structure
   - Test generator created HashMap vs Array benchmarks
   - Docs updated with data structure decision rationale
   ```

8. **Intelligent Chaining Decisions**:
   - If memory issues found → chain memory-specific optimizers
   - If CPU bottlenecks found → chain algorithm optimizers
   - If I/O issues found → chain async/parallel processors
   - If test coverage low → chain test generators before optimization

9. **Feedback Loop**:
   - After optimization, re-run memory-profiler to validate improvements
   - Compare before/after metrics
   - If improvements insufficient, chain alternative optimization agents
</actions>

The assistant should treat each agent as a link in a chain, where output becomes input, building comprehensive understanding and solutions through intelligent agent orchestration.