---
allowed-tools: Bash, Read, Write, Edit, MultiEdit, Grep, Glob, Task, TodoWrite
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

2. **Stage 1: Security Audit**:
   - Invoke security-analyzer subagent (direct analysis mode)
   - Hooks: security-validator will flag critical issues
   - Generate security scorecard

3. **Stage 2: Code Review**:
   - Invoke code-quality-analyzer subagent (security & quality review mode)  
   - Hooks: post-edit-validator ensures standards
   - Document code quality issues

4. **Stage 3: Performance Analysis**:
   - Invoke performance-optimizer subagent
   - Hooks: performance-monitor tracks metrics
   - Identify optimization opportunities

5. **Stage 4: Code Clarity**:
   - Invoke code-quality-analyzer subagent (clarity refactoring mode)
   - Apply 10 refactoring rules
   - Hooks validate refactoring safety

6. **Stage 5: Test Coverage**:
   - Invoke test-generator subagent if coverage < 80%
   - Generate missing test cases
   - Hooks: test-runner validates new tests

7. **Stage 6: Documentation**:
   - Invoke tech-docs-maintainer subagent
   - Update both @documentation and .claude directories
   - Ensure code changes are documented

8. **Generate Quality Report**:
   ```markdown
   # Quality Pipeline Report
   
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
   - API docs updated: ✓/✗
   ```

9. **Hook Integration Points**:
   - Pre-tool hooks prepare context for each subagent
   - Post-tool hooks validate changes
   - Session hooks track overall pipeline progress
</actions>

The assistant should treat this as a comprehensive quality gate, leveraging the full ecosystem of subagents and hooks to ensure code meets the highest standards before deployment.