# Phase 5 Implementation: Hybrid Pattern Formalization

**Date**: 2025-11-11
**Status**: ✅ COMPLETE
**Version**: 1.0

## Overview

Phase 5 formalizes the hybrid bash + LLM pattern established in Phase 4, creating comprehensive documentation, templates, and best practices for future hook development. This phase transforms our proof-of-concept hybrid hooks into a reusable framework for the entire Claude Code ecosystem.

## What Was Delivered

### Primary Deliverable: Comprehensive Hybrid Pattern Guide

**Document**: `.claude/research/HYBRID_PATTERN_GUIDE.md` (1,050 lines)

**Contents**:
1. **Pattern Overview** - What hybrid patterns are and why they matter
2. **Architecture** - How bash + LLM hooks work together
3. **Decision Framework** - When to use hybrid vs. bash-only vs. LLM-only
4. **Implementation Guide** - Step-by-step hook creation
5. **Templates** - Ready-to-use bash and LLM templates
6. **Best Practices** - Design principles, performance optimization, testing
7. **Examples** - Real patterns from Phases 1-4
8. **Performance Optimization** - Strategies for speed and cost
9. **Testing Strategy** - Unit, integration, and E2E testing approaches
10. **Common Pitfalls** - What to avoid and how to fix
11. **Advanced Patterns** - Future opportunities (cascading, multi-stage, feedback loops)
12. **Quick Reference** - Minimal templates and decision one-liners

## Pattern Types Formalized

### Type 1: Data Collection + Analysis

**Definition**: Bash collects data quickly, LLM analyzes intelligently

**Examples from Phase 4**:
- code-narrator: bash extracts patterns → LLM explains intent
- test-data-generator: bash detects context → LLM generates domain data
- similar-code-finder: bash finds text matches → LLM identifies semantic duplicates
- dependency-impact: bash counts dependencies → LLM assesses breaking changes

**Template**:
```
Bash Hook (~100-300ms):
  - Find files
  - Extract patterns
  - Count occurrences
  - Gather metrics

LLM Hook (~1.5-2.5s):
  - Analyze context
  - Assess risk
  - Infer intent
  - Generate recommendations

Combined: Facts + Intelligence
```

**Best For**: Informational hooks (PostToolUse, UserPromptSubmit)

### Type 2: Validation + Smart Assessment

**Definition**: LLM performs intelligent validation with optional bash pre-checks

**Examples from Phases 1-3**:
- destructive-operation-validator: LLM evaluates bash command risk
- security-file-protection: LLM understands security implications
- tdd-completion-validator: LLM validates methodology adherence
- work-completion-validator: LLM distinguishes acceptable vs. blocking TODOs

**Template**:
```
Bash Hook (optional, fast checks):
  - Pattern matching
  - File type detection
  - Quick validations

LLM Hook (intelligent validation):
  - Context understanding
  - Risk assessment
  - Decision with rationale

Combined: Fast filtering + Smart decisions
```

**Best For**: Quality gates and safety validations (PreToolUse, SubagentStop, Stop)

### Type 3: Conditional Execution (Future)

**Definition**: Bash performs fast check, LLM only runs if triggered

**Template**:
```
Bash Hook:
  if condition_needs_deep_analysis:
    trigger_llm()
    return "⚠️ Analyzing..."
  else:
    return "✅ Fast check passed"

LLM Hook (conditional):
  if not triggered:
    return approve
  else:
    perform_deep_analysis()

Combined: Minimal LLM usage for performance
```

**Best For**: Performance-critical paths with occasional deep analysis

**Status**: Pattern documented, awaiting Claude Code native support

## Decision Framework

### Simple Decision Tree

```
Need data collection?
  ├─ Yes → Can bash collect quickly?
  │   ├─ Yes → Hybrid ✓
  │   └─ No → LLM-only
  └─ No → LLM-only

Need intelligent analysis?
  ├─ Yes → Is context complex?
  │   ├─ Yes → Hybrid or LLM-only ✓
  │   └─ No → Bash-only
  └─ No → Bash-only

Performance requirement?
  ├─ <500ms → Bash-only
  ├─ <3s → Hybrid ✓
  └─ >3s acceptable → LLM-only
```

### Pattern Selection Matrix

| Requirement | Bash-Only | LLM-Only | Hybrid |
|-------------|-----------|----------|--------|
| Fast (<500ms) | ✅ | ❌ | ❌ |
| Complex analysis | ❌ | ✅ | ✅ |
| Data collection | ✅ | ❌ | ✅ |
| Cost-sensitive | ✅ | ❌ | 🟡 |
| Context-aware | ❌ | ✅ | ✅ |
| Informational | ✅ | ✅ | ✅ Best |
| Safety-critical | ❌ | ✅ | 🟡 |

## Templates Provided

### Template 1: Data Collection + Analysis

**Use Case**: PostToolUse hooks for insights

**Components**:
- Bash script template (data collection)
- LLM prompt template (analysis)
- settings.json configuration template

**Example Application**: Creating a "performance-analyzer" hook
1. Bash: Collect execution time, memory usage, complexity metrics
2. LLM: Analyze if performance is acceptable, suggest optimizations
3. Output: Facts (metrics) + Intelligence (recommendations)

### Template 2: Validation + Smart Assessment

**Use Case**: PreToolUse hooks for quality gates

**Components**:
- Optional bash script (fast checks)
- LLM prompt template (intelligent validation)
- Response schema with BLOCK/WARN/APPROVE

**Example Application**: Creating a "api-breaking-change-detector" hook
1. Bash (optional): Check if file exports public API
2. LLM: Analyze if changes break API contract
3. Output: Validation decision with specific guidance

### Template 3: Conditional Execution

**Use Case**: Performance-critical with occasional deep analysis

**Components**:
- Bash script with trigger logic
- LLM prompt with conditional check
- Flag file communication pattern

**Example Application**: Creating a "security-deep-scan" hook
1. Bash: Quick pattern scan, trigger if suspicious
2. LLM: Only runs if triggered, performs deep security analysis
3. Output: Fast check results, deep analysis when needed

**Status**: Template ready, awaiting Claude Code native conditional support

## Best Practices Documented

### 1. Design Principles

✅ **Separation of Concerns**
- Bash: Data collection and fast pattern matching
- LLM: Context understanding and intelligent analysis

✅ **Fail-Open Philosophy**
- Bash hooks: Always `exit 0` (informational)
- LLM hooks: Default to approve on errors
- Clear user guidance on failures

✅ **Clear Communication**
- Bash: Factual output
- LLM: Contextual insights
- Both: Actionable recommendations

### 2. Performance Optimization

✅ **Pre-filter with Bash**
- Reduce LLM token usage by 80-90%
- Search 1000 files with bash, analyze 10 with LLM

✅ **Cache Results**
- Bash: Cache file search results
- Invalidate on file modification

✅ **Limit Search Scope**
- Use ripgrep with `--max-count`
- Limit directory depth with `-maxdepth`

✅ **Parallel Processing**
- Use `xargs -P` for multi-core utilization

### 3. Prompt Engineering

✅ **Structure Your Prompts**
1. Role definition
2. Context provision
3. Task description
4. Evaluation criteria
5. Decision logic
6. Response format
7. Final instruction

✅ **Use $ARGUMENTS Effectively**
- `$ARGUMENTS.filePath` - File context
- `$ARGUMENTS.toolName` - Tool being used
- `$ARGUMENTS.prompt` - User prompt (UserPromptSubmit)

✅ **Provide Examples**
- Show desired response format
- Include edge cases
- Demonstrate decision logic

### 4. Testing Strategy

✅ **Test Levels**
1. Unit testing (bash and LLM independently)
2. Integration testing (combined hooks)
3. End-to-end testing (real usage scenarios)

✅ **Test Cases**
- Happy path (normal usage)
- Edge cases (empty files, special characters)
- Error handling (non-existent files, permissions)
- Performance (large files, many dependencies)
- False positives (test fixtures, examples)

### 5. Maintenance

✅ **Version Your Hooks**
- Include version in file header
- Document changes in comments

✅ **Monitor Performance**
- Add timing to bash hooks
- Track LLM latency

✅ **Collect Metrics**
- Execution count
- Average latency
- False positive rate
- User satisfaction

## Common Pitfalls Documented

### Pitfall 1: Bash Hook Blocks Operations

**Problem**: `exit 1` blocks Claude Code
**Solution**: Always `exit 0`, let LLM enforce gates

### Pitfall 2: LLM Analyzes What Bash Should Do

**Problem**: LLM counting files (slow, expensive)
**Solution**: Bash counts, LLM analyzes meaning

### Pitfall 3: Too Much Context to LLM

**Problem**: Sending 500 files to LLM (huge tokens)
**Solution**: Bash pre-filters to 5 suspicious files

### Pitfall 4: Unclear User Messages

**Problem**: "Error: condition failed"
**Solution**: "⚠️ [Issue]\n\nAction: [specific step]\nWhy: [rationale]"

### Pitfall 5: No Timeout Protection

**Problem**: 60s timeout makes users wait
**Solution**: 25-30s timeout, fail fast

### Pitfall 6: Inconsistent Response Formats

**Problem**: Different schemas for different hooks
**Solution**: Standardize on `{decision, reason, systemMessage}`

## Examples from Existing Phases

### Phase 1 Example: Destructive Operation Validator

**Pattern**: LLM-only (validation + smart assessment)

**Why**: No data collection needed, bash command provided by Claude Code

**Value**: Context-aware risk assessment (understands git force, production files, database operations)

### Phase 2 Example: TDD Completion Validator

**Pattern**: LLM-only (validation + smart assessment)

**Why**: Agent context provided, no external data needed

**Value**: Methodology validation (RED-GREEN-REFACTOR, coverage, test quality)

### Phase 3 Example: Work Completion Validator

**Pattern**: LLM-only (validation + smart assessment)

**Why**: Context-aware evaluation, no data collection

**Value**: Distinguishes acceptable TODOs from blocking issues

### Phase 4 Example: Code Narrator

**Pattern**: Hybrid (data collection + analysis)

**Bash**: Extracts functions, classes, imports, metrics
**LLM**: Infers intent, explains why, provides stakeholder insights

**Value**: Facts (what changed) + Intelligence (why and impact)

### Phase 4 Example: Dependency Impact Analyzer

**Pattern**: Hybrid (data collection + analysis)

**Bash**: Finds importers, callers, test files, counts dependencies
**LLM**: Detects breaking changes, assesses risk, provides migration guidance

**Value**: Facts (who depends) + Intelligence (breaking change risk)

## Performance Targets

| Hook Type | Target Latency | Acceptable Latency |
|-----------|----------------|-------------------|
| Bash-only | <200ms | <500ms |
| LLM-only | <2s | <3s |
| Hybrid (bash + LLM) | <2.5s | <4s |
| Critical safety | N/A | <5s (quality matters) |

**Phase 4 Results**:
- code-narrator-llm: 1.6s total ✅
- test-data-generator-llm: 2.05s total ✅
- similar-code-finder-llm: 2.2s total ✅
- dependency-impact-llm: 2.8s total ✅

All within acceptable latency targets.

## Cost Analysis

**Model**: Haiku (fast, economical)

| Hook Type | Input Tokens | Output Tokens | Cost/Exec |
|-----------|--------------|---------------|-----------|
| Simple analysis | ~500 | ~200 | ~$0.0002 |
| Medium analysis | ~700 | ~250 | ~$0.00025 |
| Complex analysis | ~800 | ~300 | ~$0.0003 |

**Phase 4 Monthly Cost** (100 executions per hook):
- 4 hooks × $0.00025 × 100 = ~$0.10/month

**Hybrid vs. LLM-Only**:
- Hybrid: Bash pre-filters, LLM analyzes 10 items = ~$0.01
- LLM-only: LLM analyzes all 100 items = ~$0.10
- **Savings**: 90% cost reduction with hybrid pattern

## Future Directions

### Short Term (Next Month)

1. **Hook Testing Framework**
   - Automated testing for bash + LLM hooks
   - Performance profiling tools
   - False positive detection

2. **Hook Templates Library**
   - Expand templates for common patterns
   - Domain-specific templates (security, performance, quality)
   - Language-specific templates (Python, JavaScript, Go)

3. **Metrics Dashboard**
   - Hook execution statistics
   - Performance monitoring
   - User satisfaction tracking

### Medium Term (Next Quarter)

4. **Conditional Execution Support**
   - Native Claude Code support for bash-triggered LLM
   - Performance optimization for conditional patterns
   - Advanced triggering logic

5. **Hook Communication**
   - Pass data between bash and LLM hooks
   - Shared context mechanism
   - Pipeline patterns

6. **Hook Marketplace**
   - Community-contributed hooks
   - Best practices repository
   - Template showcase

### Long Term (Next Year)

7. **AI-Assisted Hook Development**
   - Generate bash scripts from descriptions
   - Generate LLM prompts from requirements
   - Suggest optimizations

8. **Adaptive Hooks**
   - Learn from user feedback
   - Tune prompts automatically
   - Project-specific customization

9. **Cross-Hook Intelligence**
   - Correlate insights from multiple hooks
   - Holistic project analysis
   - Predictive recommendations

## Adoption Strategy

### Phase 5A: Documentation (Complete)

- [x] ✅ Create Hybrid Pattern Guide (1,050 lines)
- [x] ✅ Document all pattern types
- [x] ✅ Provide templates and examples
- [x] ✅ Establish best practices
- [x] ✅ Document common pitfalls

### Phase 5B: Enablement (Next 2 Weeks)

- [ ] ⏳ Create hook development workshop
- [ ] ⏳ Train Grey Haven team on hybrid patterns
- [ ] ⏳ Develop 2-3 example hooks using templates
- [ ] ⏳ Collect feedback on guide usability

### Phase 5C: Community (Next Month)

- [ ] ⏳ Publish guide to Claude Code community
- [ ] ⏳ Create template repository
- [ ] ⏳ Host office hours for hook developers
- [ ] ⏳ Build hook showcase

### Phase 5D: Evolution (Ongoing)

- [ ] ⏳ Iterate on templates based on usage
- [ ] ⏳ Add new patterns as discovered
- [ ] ⏳ Update best practices from learnings
- [ ] ⏳ Expand examples library

## Success Metrics

### Adoption Metrics

**Target**:
- 5+ new hooks using hybrid pattern (next month)
- 80% of new hooks follow guide best practices
- <10% false positive rate across all hooks

**Measurement**:
- Track hooks created using templates
- Survey developers on guide usefulness
- Monitor hook performance and quality

### Quality Metrics

**Target**:
- All new hooks meet latency targets
- 90%+ user satisfaction with hybrid hooks
- <5% cost overrun from optimization guidance

**Measurement**:
- Performance monitoring dashboard
- User satisfaction surveys
- Cost tracking per hook execution

### Impact Metrics

**Target**:
- 50% reduction in hook development time
- 80% reduction in performance issues
- 90% reduction in common pitfalls

**Measurement**:
- Compare development time before/after guide
- Track performance issues reported
- Track pitfall occurrences (blocking hooks, unclear messages, etc.)

## Conclusion

### Phase 5 Summary

✅ **Formalized Hybrid Pattern**: Comprehensive 1,050-line guide covering all aspects

✅ **Three Pattern Types**: Data+Analysis, Validation+Assessment, Conditional (future)

✅ **Templates Provided**: Ready-to-use bash and LLM templates for each pattern

✅ **Best Practices**: Design, performance, prompt engineering, testing, maintenance

✅ **Examples**: Real patterns from Phases 1-4 with analysis

✅ **Decision Framework**: Clear guidance on when to use each pattern

✅ **Future Roadmap**: Short, medium, and long-term enhancements

### Transformation Achieved

**Before Phase 5**:
- Hybrid pattern proven in Phase 4
- Ad-hoc implementation
- No formal guidance
- Unclear when to use what

**After Phase 5**:
- Hybrid pattern formalized with comprehensive guide
- Templates and best practices established
- Clear decision frameworks
- Reusable for all future hook development

### Impact on Hook Development

**Development Time**: 50% reduction expected
- Templates provide starting point
- Best practices prevent common mistakes
- Examples show proven patterns

**Code Quality**: Significant improvement expected
- Performance optimization built-in
- Testing strategy included
- Pitfalls documented and avoided

**Maintainability**: Much easier
- Consistent patterns across hooks
- Clear documentation standards
- Version control and metrics

### Phase Completion Status

**Total Phases**: 5 of 5 ✅ COMPLETE

| Phase | Hooks | Focus | Status |
|-------|-------|-------|--------|
| Phase 1 | 2 | Critical Safety | ✅ Complete |
| Phase 2 | 3 | Agent Quality Gates | ✅ Complete |
| Phase 3 | 3 | Code Quality & Testing | ✅ Complete |
| Phase 4 | 4 | Hook Enhancement | ✅ Complete |
| Phase 5 | 0 | Hybrid Pattern Formalization | ✅ Complete |

**Total Hooks Implemented**: 12 prompt-based hooks
**Total Documentation**: 6 comprehensive guides

**Coverage**:
- ✅ Critical Safety
- ✅ Agent Quality
- ✅ Code Quality
- ✅ Hook Enhancement
- ✅ Pattern Formalization

### Next Steps

**Immediate**:
1. Share Hybrid Pattern Guide with team
2. Conduct workshop on hybrid patterns
3. Gather feedback on templates

**Short Term**:
1. Create 2-3 example hooks using templates
2. Develop hook testing framework
3. Build metrics dashboard

**Long Term**:
1. Publish to Claude Code community
2. Expand pattern library
3. Develop AI-assisted hook tools

---

**Version**: 1.0
**Last Updated**: 2025-11-11
**Status**: Phase 5 Complete
**Phases**: 5 of 5 ✅

**Total Implementation**:
- **12 hooks** across 4 implementation phases
- **6 comprehensive documentation guides**
- **Hybrid pattern framework** for future development
- **Complete coverage** of safety, quality, and enhancement

**Achievement**: Comprehensive prompt-based hooks ecosystem with formalized patterns and best practices for sustainable development.
