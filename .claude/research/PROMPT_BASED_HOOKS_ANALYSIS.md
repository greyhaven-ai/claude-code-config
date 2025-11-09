# Prompt-Based Hooks Implementation Analysis

**Date**: 2025-11-09
**Version**: 1.0
**Status**: Research & Planning

## Executive Summary

This document analyzes opportunities to implement prompt-based hooks in the Grey Haven plugin ecosystem. Prompt-based hooks leverage LLMs (Haiku) for intelligent, context-aware decision-making beyond simple bash command validation.

### Current State

**Existing Hooks (Bash-Based)**:
- `subagent-context-preparer.py` - SubagentStop event (bash)
- `security-validator.py` - PreToolUse event (bash)
- `prompt-enhancer.py` - UserPromptSubmit event (bash)
- `work-completion-assistant.py` - Stop event (bash)

**Agent Count**: 33 agents across 12 plugins
**Command Count**: 30+ slash commands

## Understanding Prompt-Based Hooks

### How They Work

1. Hook transmits input data + configured prompt to Haiku LLM
2. LLM processes context and returns structured JSON decision
3. Claude Code automatically acts on the decision

### Response Schema

```json
{
  "decision": "approve" | "block",
  "reason": "Explanation for the decision",
  "continue": false,
  "stopReason": "Message shown to user",
  "systemMessage": "Optional warning"
}
```

### Key Benefits vs Bash Hooks

| Aspect | Bash Commands | Prompt-Based |
|--------|---------------|--------------|
| Execution | Runs local scripts | Queries LLM |
| Logic | You implement in code | LLM evaluates context |
| Setup | Requires script files | Configure text prompt |
| Context Awareness | Limited to script logic | Natural language understanding |
| Best For | Deterministic rules | Context-aware decisions |

## Opportunity Analysis by Event Type

### 1. SubagentStop Hooks 🎯 **HIGH PRIORITY**

**Purpose**: Evaluate whether subagent completed assigned work or needs continuation.

#### A. TDD Orchestrator Completion Validator

**Agent**: `tdd-orchestrator` (core plugin)

**Use Case**: Validate red-green-refactor cycle completion before stopping.

**Why Prompt-Based**:
- Complex evaluation: Did tests actually fail for the right reason?
- Quality assessment: Are assertions meaningful?
- Coverage verification: Did we meet thresholds?
- Mutation testing: Should we run mutation tests?

**Example Configuration**:
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a TDD methodology expert. Evaluate if the TDD cycle is complete:\n\nInput: $ARGUMENTS\n\nCheck:\n1. Did RED phase produce a failing test for the right reason?\n2. Did GREEN phase implement minimal code to pass?\n3. Did REFACTOR phase maintain test coverage?\n4. Are coverage thresholds met (80% line, 75% branch)?\n5. Are test assertions specific and meaningful?\n\nIf incomplete, return {\"decision\": \"block\", \"reason\": \"<what's missing>\"}\nIf complete, return {\"decision\": \"approve\", \"reason\": \"TDD cycle complete with quality gates passed\"}",
        "timeout": 30
      }],
      "agentNames": ["tdd-orchestrator", "tdd-python", "tdd-typescript"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Prevent incomplete TDD cycles
- ✅ Enforce test quality standards
- ✅ Catch coverage threshold violations
- ✅ Ensure mutation testing when needed

#### B. Security Analysis Completeness Validator

**Agent**: `security-analyzer` (security plugin)

**Use Case**: Verify all OWASP Top 10 categories checked before completion.

**Why Prompt-Based**:
- Multi-category analysis (10 OWASP categories)
- Severity assessment requires judgment
- Context matters (what type of code was analyzed?)
- Compliance mapping needs verification

**Example Configuration**:
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a security audit expert. Evaluate if security analysis is complete:\n\nInput: $ARGUMENTS\n\nRequired checks:\n1. All OWASP Top 10 categories scanned\n2. Critical vulnerabilities (CVSS 9.0+) addressed\n3. Secrets/credentials scanned\n4. Dependencies checked for CVEs\n5. Cryptographic implementation reviewed\n\nIf any category skipped or critical findings unresolved, return {\"decision\": \"block\", \"reason\": \"<missing checks>\"}\nIf comprehensive scan complete, return {\"decision\": \"approve\", \"reason\": \"Security audit complete\"}",
        "timeout": 30
      }],
      "agentNames": ["security-analyzer"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Prevent incomplete security audits
- ✅ Ensure all OWASP categories covered
- ✅ Block on unresolved critical vulnerabilities
- ✅ Verify compliance requirements met

#### C. Code Quality Review Completeness

**Agent**: `code-quality-analyzer` (core plugin)

**Use Case**: Ensure security review, clarity refactoring, OR synthesis analysis completed.

**Why Prompt-Based**:
- Mode-specific completion criteria (Security/Clarity/Synthesis)
- Complexity metrics need interpretation
- Prioritization requires judgment (Critical vs Low)
- Fix verification needs validation

**Example Configuration**:
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a code quality expert. Evaluate analysis completion:\n\nInput: $ARGUMENTS\n\nMode-specific checks:\n- Security Review: Vulnerabilities identified, CVSS scored, fixes provided?\n- Clarity Refactoring: Complexity reduced, guard clauses added, symmetry normalized?\n- Synthesis Analysis: Cross-file issues found, API consistency checked, dependency mapping done?\n\nGeneral checks:\n1. All critical issues have specific fixes\n2. Priority ranking provided (Critical → Low)\n3. Before/after examples shown\n4. Test coverage maintained\n\nReturn {\"decision\": \"block\"} if incomplete, {\"decision\": \"approve\"} if thorough analysis delivered.",
        "timeout": 30
      }],
      "agentNames": ["code-quality-analyzer"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Ensure thorough multi-mode analysis
- ✅ Verify all critical issues have fixes
- ✅ Prevent premature completion
- ✅ Validate test coverage maintained

#### D. Smart Debug Resolution Validator

**Agent**: `smart-debug` (incident-response plugin)

**Use Case**: Confirm bug actually fixed and won't recur.

**Why Prompt-Based**:
- Root cause identification (5 Whys)
- Fix verification (did test pass?)
- Prevention strategy assessment
- Recurrence risk evaluation

**Example Configuration**:
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a debugging expert. Evaluate if bug fix is complete:\n\nInput: $ARGUMENTS\n\nRequired steps:\n1. Root cause identified (5 Whys methodology)\n2. Failing test created to reproduce bug\n3. Fix applied to address root cause (not symptom)\n4. Test now passes\n5. Full test suite still passes (no regressions)\n6. Prevention strategy documented (monitoring, tests, etc.)\n\nIf any step incomplete or tests failing, return {\"decision\": \"block\", \"reason\": \"<what's missing>\"}\nIf bug truly fixed with prevention, return {\"decision\": \"approve\"}",
        "timeout": 30
      }],
      "agentNames": ["smart-debug"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Ensure root cause fixed (not symptoms)
- ✅ Verify test coverage for bug
- ✅ Prevent regressions
- ✅ Mandate prevention strategies

### 2. Stop Hooks 🎯 **MEDIUM PRIORITY**

**Purpose**: Decide intelligently whether Claude should stop working.

#### A. Work Completion Validator (Upgrade Existing)

**Current**: `work-completion-assistant.py` (bash-based)

**Upgrade to Prompt-Based**:

**Why Upgrade**:
- Current hook has hardcoded rules (TODOs, uncommitted changes, etc.)
- Prompt-based can understand context ("WIP commit is OK", "TODO for future work")
- Can evaluate quality of work, not just presence of files
- Can assess if user request truly fulfilled

**Example Configuration**:
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a work completion expert. Evaluate if work is truly complete:\n\nInput: $ARGUMENTS\n\nContext-aware evaluation:\n1. Are there uncommitted changes? (OK if WIP documented)\n2. Are there TODOs? (OK if for future work, not current task)\n3. Did tests run and pass? (required for production code)\n4. Is code formatted/linted? (required for team standards)\n5. Is documentation updated? (required if APIs changed)\n6. Did we actually fulfill the user's request?\n\nReturn {\"decision\": \"block\"} with specific missing items if incomplete.\nReturn {\"decision\": \"approve\"} with summary if work complete and quality assured.",
        "timeout": 30
      }]
    }]
  }
}
```

**Migration Strategy**:
1. Run both hooks in parallel initially
2. Compare decisions (bash vs prompt-based)
3. Tune prompt based on false positives/negatives
4. Deprecate bash hook after validation period

**Expected Impact**:
- ✅ Smarter context-aware completion checks
- ✅ Fewer false positives (e.g., OK to have WIP commits)
- ✅ Better alignment with user intent
- ✅ Quality assessment beyond file presence

#### B. Agent Orchestration Completion

**Agent**: `multi-agent-synthesis-orchestrator` (core/research plugins)

**Use Case**: Validate multi-agent workflows completed successfully.

**Why Prompt-Based**:
- Complex workflows with dependencies
- Need to verify all sub-agents completed
- Context handoffs require validation
- Synthesis quality assessment

**Example Configuration**:
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a multi-agent workflow expert. Evaluate orchestration completion:\n\nInput: $ARGUMENTS\n\nChecks:\n1. Did all delegated sub-agents complete successfully?\n2. Were context handoffs clean (no missing data)?\n3. Is final synthesis coherent and comprehensive?\n4. Were dependencies between agents respected?\n5. Are there unhandled errors from any agent?\n\nReturn {\"decision\": \"block\"} if orchestration incomplete.\nReturn {\"decision\": \"approve\"} if all agents completed and synthesis delivered.",
        "timeout": 30
      }],
      "agentNames": ["multi-agent-synthesis-orchestrator"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Prevent incomplete multi-agent workflows
- ✅ Verify all sub-tasks completed
- ✅ Ensure synthesis quality
- ✅ Catch context handoff failures

### 3. UserPromptSubmit Hooks 🎯 **LOW PRIORITY**

**Purpose**: Validate/enhance prompts before processing.

#### A. Prompt Enhancer (Already Implemented, Consider Hybrid)

**Current**: `prompt-enhancer.py` (bash-based, working well)

**Consideration**: Keep bash for speed, add optional prompt-based validation

**Hybrid Approach**:
- Bash hook: Fast context injection (current behavior)
- Prompt-based: Optional validation for ambiguous requests

**When to Use Prompt-Based**:
- User request is ambiguous
- Multiple valid interpretations
- Requires clarification before proceeding

**Example Configuration**:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/prompt-enhancer.py"
          },
          {
            "type": "prompt",
            "prompt": "You are a prompt clarification expert. Evaluate if this user request is clear:\n\nUser prompt: $ARGUMENTS\n\nCheck:\n1. Is the intent unambiguous? (implement vs analyze vs fix)\n2. Are there multiple valid interpretations?\n3. Are critical details missing? (which file, which feature, which API)\n4. Would asking for clarification improve quality?\n\nReturn {\"decision\": \"approve\"} if prompt is clear.\nReturn {\"decision\": \"block\", \"systemMessage\": \"<clarifying question>\"} if ambiguous.",
            "timeout": 20,
            "enabled": false
          }
        ]
      }
    ]
  }
}
```

**Note**: Disabled by default (adds latency), enable for novice users or critical projects.

### 4. PreToolUse Hooks 🎯 **HIGH PRIORITY**

**Purpose**: Make context-aware permission decisions before tool execution.

#### A. Destructive Operation Validator

**Use Case**: Prevent accidental data loss or production modifications.

**Why Prompt-Based**:
- Context matters (dev vs staging vs production)
- Intent evaluation (is this deliberate or accidental?)
- Risk assessment (how critical is this operation?)

**Example Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a safety validation expert. Evaluate this tool use for risk:\n\nInput: $ARGUMENTS\n\nRisk assessment:\n1. Is this a destructive operation? (delete, drop, truncate, force push)\n2. What environment? (production > staging > dev)\n3. Is there backup/rollback capability?\n4. Did user explicitly request this operation?\n5. What's the blast radius if this goes wrong?\n\nFor HIGH RISK operations, return {\"decision\": \"block\", \"systemMessage\": \"⚠️ Destructive operation detected: <details>. Please confirm.\"}\nFor MEDIUM RISK, return {\"decision\": \"approve\", \"systemMessage\": \"⚠️ Caution: <warning>\"}\nFor LOW RISK, return {\"decision\": \"approve\"}",
        "timeout": 20
      }],
      "toolNames": ["Bash", "Write", "MultiEdit"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Prevent accidental production changes
- ✅ Catch force pushes to main branch
- ✅ Warn before destructive database operations
- ✅ Context-aware risk assessment

#### B. Security-Sensitive File Protection

**Use Case**: Prevent modifications to security-critical files without review.

**Why Prompt-Based**:
- File criticality depends on project context
- Some changes to sensitive files are OK (adding tests)
- Intent matters (refactor vs disable security)

**Example Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a security file protection expert. Evaluate this file modification:\n\nInput: $ARGUMENTS\n\nSecurity-sensitive file patterns:\n- auth*, login*, session*, jwt*, crypto*\n- .env*, secrets*, credentials*, config/production*\n- Dockerfile, docker-compose.yml, k8s/*.yaml\n- .github/workflows/* (CI/CD)\n\nEvaluation:\n1. Is this a security-sensitive file?\n2. What type of change? (add feature, disable check, refactor)\n3. Is security being weakened or strengthened?\n4. Should this require security team review?\n\nFor SECURITY WEAKENING, return {\"decision\": \"block\", \"reason\": \"Security modification requires review\"}\nFor SECURITY STRENGTHENING or REFACTOR, return {\"decision\": \"approve\"}\nFor NON-SENSITIVE, return {\"decision\": \"approve\"}",
        "timeout": 20
      }],
      "toolNames": ["Write", "MultiEdit", "Edit"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Prevent accidental auth bypass
- ✅ Flag secret exposure attempts
- ✅ Require review for security changes
- ✅ Allow safe refactoring of auth code

#### C. Test Coverage Protection

**Use Case**: Prevent test deletion or coverage reduction.

**Why Prompt-Based**:
- Sometimes OK to delete tests (obsolete feature removed)
- Refactoring tests is OK if coverage maintained
- Need to evaluate overall impact

**Example Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "You are a test coverage protection expert. Evaluate this test modification:\n\nInput: $ARGUMENTS\n\nChecks:\n1. Are tests being deleted without replacement?\n2. Is coverage being reduced? (check before/after)\n3. Is this part of feature removal? (OK to delete tests)\n4. Is this test refactoring? (OK if coverage maintained)\n\nFor COVERAGE REDUCTION without justification, return {\"decision\": \"block\", \"reason\": \"Test coverage reduction detected\"}\nFor JUSTIFIED changes or COVERAGE MAINTAINED, return {\"decision\": \"approve\"}",
        "timeout": 20
      }],
      "toolNames": ["Write", "Edit", "MultiEdit"],
      "filePatterns": ["**/*.test.*", "**/*.spec.*", "**/tests/**/*", "**/__tests__/**/*"]
    }]
  }
}
```

**Expected Impact**:
- ✅ Prevent accidental test deletion
- ✅ Catch coverage regressions
- ✅ Allow justified test removal
- ✅ Permit safe test refactoring

## Implementation Priority Matrix

| Opportunity | Event Type | Priority | Complexity | Impact |
|-------------|-----------|----------|------------|--------|
| TDD Orchestrator Completion | SubagentStop | 🔴 HIGH | Medium | High |
| Security Analysis Completion | SubagentStop | 🔴 HIGH | Medium | High |
| Smart Debug Resolution | SubagentStop | 🔴 HIGH | Low | High |
| Destructive Operation Validator | PreToolUse | 🔴 HIGH | Medium | Critical |
| Security File Protection | PreToolUse | 🔴 HIGH | Low | Critical |
| Work Completion Upgrade | Stop | 🟡 MEDIUM | Medium | Medium |
| Code Quality Completion | SubagentStop | 🟡 MEDIUM | Medium | Medium |
| Test Coverage Protection | PreToolUse | 🟡 MEDIUM | Medium | Medium |
| Multi-Agent Orchestration | Stop | 🟢 LOW | High | Medium |
| Prompt Clarification | UserPromptSubmit | 🟢 LOW | Low | Low |

## Recommended Implementation Phases

### Phase 1: Critical Safety (Week 1-2)
**Goal**: Prevent destructive operations and security issues

1. **Destructive Operation Validator** (PreToolUse)
   - Prevent production accidents
   - Catch force pushes
   - High ROI, low complexity

2. **Security File Protection** (PreToolUse)
   - Protect auth/secrets/config files
   - Require review for security changes
   - Critical for compliance

### Phase 2: Agent Quality Gates (Week 3-4)
**Goal**: Ensure agents complete work thoroughly

3. **TDD Orchestrator Completion** (SubagentStop)
   - Enforce red-green-refactor discipline
   - Verify coverage thresholds
   - High impact on code quality

4. **Security Analysis Completion** (SubagentStop)
   - Ensure OWASP Top 10 coverage
   - Verify critical vulnerabilities resolved
   - Critical for security posture

5. **Smart Debug Resolution** (SubagentStop)
   - Confirm root cause fixed
   - Require prevention strategies
   - Prevent regression bugs

### Phase 3: Code Quality & Testing (Week 5-6)
**Goal**: Maintain code quality and test coverage

6. **Code Quality Completion** (SubagentStop)
   - Multi-mode analysis validation
   - Fix verification
   - Moderate impact

7. **Test Coverage Protection** (PreToolUse)
   - Prevent test deletion
   - Catch coverage regressions
   - Maintain quality bar

8. **Work Completion Upgrade** (Stop)
   - Context-aware completion checks
   - Quality assessment
   - Better UX

### Phase 4: Advanced Orchestration (Week 7-8)
**Goal**: Improve multi-agent workflows

9. **Multi-Agent Orchestration** (Stop)
   - Validate complex workflows
   - Verify synthesis quality
   - Advanced use case

10. **Prompt Clarification** (UserPromptSubmit)
    - Optional ambiguity detection
    - User experience enhancement
    - Low priority, nice-to-have

## Technical Implementation Guide

### Configuration Structure

Place prompt-based hooks in `.claude/settings.json`:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "<evaluation prompt with $ARGUMENTS placeholder>",
            "timeout": 30
          }
        ],
        "agentNames": ["agent-name-1", "agent-name-2"]
      }
    ],
    "Stop": [...],
    "PreToolUse": [...],
    "UserPromptSubmit": [...]
  }
}
```

### Prompt Engineering Best Practices

**DO**:
- ✅ List explicit decision criteria
- ✅ Use structured evaluation (numbered checks)
- ✅ Provide clear examples of approve/block cases
- ✅ Include context about agent purpose
- ✅ Request specific JSON response format
- ✅ Set appropriate timeouts (20-30s)

**DON'T**:
- ❌ Use vague criteria ("check if good")
- ❌ Make prompts too long (>500 words)
- ❌ Forget $ARGUMENTS placeholder
- ❌ Use prompts for deterministic rules (use bash instead)
- ❌ Set timeout too low (<15s for complex evaluation)

### Testing Strategy

1. **Unit Testing**: Test prompts in isolation
   ```bash
   echo '{"tool": "Bash", "args": {"command": "git push -f origin main"}}' | \
     claude-hooks eval-prompt --prompt-file destructive-op-validator.txt
   ```

2. **Integration Testing**: Test with actual agents
   - Run agent
   - Trigger hook
   - Verify decision matches expectation

3. **A/B Testing**: Run bash + prompt-based in parallel
   - Compare decisions
   - Measure false positive/negative rates
   - Tune prompts based on data

### Monitoring & Metrics

Track these metrics for each prompt-based hook:

- **Latency**: Hook execution time (target: <2s p95)
- **Approval Rate**: % of approve vs block decisions
- **False Positives**: Incorrect blocks (user overrides)
- **False Negatives**: Incorrect approvals (bugs shipped)
- **Timeout Rate**: % of hooks hitting timeout

**Dashboard Example**:
```
TDD Orchestrator Completion Hook
─────────────────────────────────
Executions:     1,247
Approval Rate:  87%
Block Rate:     13%
Avg Latency:    1.2s (p95: 1.8s)
Timeouts:       0.2%
User Overrides: 3% (likely false positives)
```

## Integration with Existing Agents

### How Agents See Hook Feedback

Agents won't directly see hook execution, but they'll experience:

1. **Block Decision**: Agent stops, user sees error message
2. **Approve with Warning**: Agent continues, warning logged
3. **Approve**: Agent continues normally

**Agent Documentation Updates**:

Update agent docs to mention hooks:

```markdown
## Hook Integration

### SubagentStop Hook: TDD Completion Validator

This agent integrates with a prompt-based completion validator that checks:
- Red-green-refactor cycle completion
- Coverage thresholds (80% line, 75% branch)
- Test quality and mutation testing

If the hook blocks completion, review:
- Did you run all three TDD phases?
- Are coverage thresholds met?
- Are test assertions specific?
```

### Agent Hook Integration Points

Agents can provide hook-friendly outputs:

**Example from TDD Orchestrator**:

```markdown
## TDD Cycle Complete ✅

**RED Phase**: test_user_login_valid_credentials() failed correctly
**GREEN Phase**: login() implemented, test passes
**REFACTOR Phase**: extracted validate_credentials() helper

**Metrics**:
- Cycle time: 19 minutes
- Coverage: 87% line, 82% branch ✅
- Mutation score: 91% ✅

<!-- Hook: TDD completion validator will check these metrics -->
```

Hook can parse this structured output for validation.

## Migration Strategy for Existing Hooks

### Converting Bash to Prompt-Based

**When to Convert**:
- Hook logic is complex (many if/else branches)
- Context interpretation needed
- Rules aren't deterministic
- False positive rate high

**When to Keep Bash**:
- Simple, fast checks (file exists, syntax valid)
- Deterministic rules (coverage > 80%)
- Performance critical (runs on every save)
- Works well already

**Hybrid Approach**:

Run bash first (fast), then prompt-based (smart):

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {
          "type": "command",
          "command": ".claude/hooks/quick-checks.sh"
        },
        {
          "type": "prompt",
          "prompt": "Context-aware evaluation...",
          "timeout": 30
        }
      ]
    }]
  }
}
```

Bash hook does fast checks, prompt-based does smart evaluation.

## Cost & Performance Considerations

### API Costs

**Per Hook Execution**:
- Model: Haiku (fast, cheap)
- Input: ~500 tokens (prompt + $ARGUMENTS)
- Output: ~100 tokens (JSON response)
- Cost: ~$0.0001 per execution

**Monthly Estimate** (1000 agent runs):
- 1000 executions × $0.0001 = **$0.10/month**

**Conclusion**: Cost negligible compared to main Claude API usage.

### Latency Impact

**Typical Hook Execution**:
- Bash hook: 10-100ms
- Prompt-based hook: 800-2000ms (Haiku)

**Mitigation**:
- Use appropriate timeouts (20-30s)
- Only apply to end-of-work events (Stop, SubagentStop)
- Avoid on high-frequency events (OnSave, OnType)
- Consider async execution for non-blocking hooks

### Performance Budget

**Acceptable Latency**:
- SubagentStop: 2s (agent just finished, user expects some delay)
- Stop: 2s (user stopping work, acceptable wait)
- PreToolUse: 1s (before action, should be quick)
- UserPromptSubmit: 500ms (user waiting, keep it fast)

## Documentation & Team Adoption

### Developer Education

**Create docs**:
1. `docs/hooks/PROMPT_BASED_HOOKS_GUIDE.md` - How they work
2. `docs/hooks/WRITING_HOOK_PROMPTS.md` - Best practices
3. `docs/hooks/TROUBLESHOOTING_HOOKS.md` - Debug guide

**Training**:
- Demo session showing hook decisions
- Walkthrough of prompt engineering
- Q&A on use cases

### User Communication

**When hook blocks**:
```
⚠️ TDD Completion Validator

The TDD cycle appears incomplete:
❌ Coverage threshold not met (73% line, target: 80%)
❌ No mutation testing performed

Please:
1. Add tests to reach 80% coverage
2. Run mutation testing: pytest --mutate

Need help? Run: /tdd-help
```

Clear, actionable feedback.

### Configuration Management

**Version control**:
- Commit `.claude/settings.json` to git
- Document hook changes in changelog
- Use feature flags for experimental hooks

**Rollback strategy**:
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "prompt",
        "enabled": false,  // Quick disable
        "prompt": "..."
      }]
    }]
  }
}
```

## Success Metrics

### KPIs to Track

1. **Quality Gates**:
   - % of TDD cycles completing all phases
   - % of security audits covering all OWASP categories
   - % of bug fixes with root cause analysis

2. **Safety**:
   - Destructive operations prevented
   - Security file modifications caught
   - Production incidents avoided

3. **Developer Experience**:
   - False positive rate (<5% target)
   - Time to resolution when blocked
   - User override frequency

4. **Performance**:
   - Hook latency p95 (<2s target)
   - Timeout rate (<1% target)
   - API cost per month (<$5 target)

### Success Criteria

**Phase 1 Success** (Critical Safety):
- Zero production incidents from destructive ops
- 100% of security file changes reviewed
- <2% false positive rate

**Phase 2 Success** (Agent Quality Gates):
- 90%+ TDD cycles complete all phases
- 95%+ security audits cover all OWASP
- 80%+ bugs fixed with prevention strategy

**Phase 3 Success** (Code Quality):
- Test coverage maintained or improved
- Code quality scores trending up
- Developer satisfaction >4/5

## Next Steps

### Immediate Actions (This Week)

1. **Create settings branch**: `git checkout -b feature/prompt-based-hooks`
2. **Implement Phase 1**: Add destructive op + security file validators
3. **Test with team**: Run on dev projects, gather feedback
4. **Measure baseline**: Track metrics before full rollout

### Short Term (Next 2 Weeks)

5. **Implement Phase 2**: Add agent completion validators
6. **A/B test**: Compare bash vs prompt-based decisions
7. **Tune prompts**: Iterate based on false positives/negatives
8. **Documentation**: Write user-facing guides

### Medium Term (Next Month)

9. **Implement Phase 3-4**: Code quality + orchestration hooks
10. **Team training**: Educate on hook system
11. **Monitor metrics**: Track KPIs, adjust as needed
12. **Iterate**: Continuous improvement based on data

### Long Term (Next Quarter)

13. **Custom hooks**: Let teams write custom prompt-based hooks
14. **Hook marketplace**: Share successful hooks across teams
15. **Advanced features**: Conditional hooks, multi-stage validation
16. **AI tuning**: Train custom models for hook evaluation

## Conclusion

Prompt-based hooks offer significant opportunities to enhance the Grey Haven plugin ecosystem:

**Highest ROI**:
1. 🔴 **Destructive Operation Validator** - Prevent production accidents
2. 🔴 **Security File Protection** - Maintain security posture
3. 🔴 **TDD Completion Validator** - Enforce quality discipline
4. 🔴 **Security Analysis Completion** - Ensure thorough audits

**Key Benefits**:
- ✅ Context-aware decision making beyond simple rules
- ✅ Natural language understanding of work quality
- ✅ Flexible evaluation criteria without code changes
- ✅ Better alignment with user intent

**Trade-offs**:
- ⚠️ Increased latency (800-2000ms per hook)
- ⚠️ Small API cost (~$0.10/month for 1000 runs)
- ⚠️ Requires prompt engineering expertise
- ⚠️ Potential for false positives/negatives

**Recommendation**: Proceed with **Phase 1** implementation immediately. The safety benefits of destructive operation prevention alone justify the effort. Then iterate based on metrics and team feedback.

---

**Document Status**: Ready for review and implementation planning
**Next Review**: After Phase 1 completion
**Owner**: Grey Haven Studio
**Related Docs**:
- `.claude/V2_ARCHITECTURE_PLAN.md`
- `.claude/hooks/README.md` (to be created)
- `docs/hooks/PROMPT_BASED_HOOKS_GUIDE.md` (to be created)
