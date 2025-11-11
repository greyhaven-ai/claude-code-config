# Phase 4 Implementation Plan: Hook Enhancement with LLM Intelligence

**Date**: 2025-11-11
**Status**: 🚧 IN PROGRESS
**Phase**: 4 of 5
**Priority**: 🟡 MEDIUM-HIGH

## Executive Summary

Phase 4 enhances existing bash/Python hooks with LLM intelligence using a **hybrid pattern**. Existing hooks excel at fast data collection (file searching, pattern matching, dependency analysis), while LLM hooks provide intelligent analysis, risk assessment, and context-aware recommendations.

**Key Principle**: Don't replace existing hooks - enhance them with prompt-based intelligence.

## Background: Hook Ecosystem Discovery

From our discovery analysis (`.claude/research/HOOKS_DISCOVERY_IMPACT_ANALYSIS.md`):

- **Total hooks**: 41 (4 production + 37 library hooks)
- **Categories**: Code quality, testing, performance, documentation, architecture
- **Finding**: Rich ecosystem of bash/Python hooks that work well for data collection
- **Opportunity**: Enhance with LLM for intelligent analysis and recommendations

## Phase 4 Objectives

### Primary Goals

1. **Enhance 4 high-priority hooks** with prompt-based intelligence
2. **Establish hybrid pattern** (bash collects → LLM analyzes)
3. **Demonstrate enhancement value** through measurable improvements
4. **Document best practices** for future hook enhancements

### Success Metrics

- ✅ 4 hooks enhanced with LLM intelligence
- ✅ Hybrid pattern documented and reusable
- ✅ Measurable improvement in output quality
- ✅ <3s total latency (bash + LLM combined)
- ✅ User satisfaction >4/5 for enhanced hooks

## Hook Enhancement Candidates

### Analysis Results

| Hook | Current Implementation | Enhancement Opportunity | Priority | ROI |
|------|------------------------|-------------------------|----------|-----|
| **code-narrator.py** | Regex pattern extraction, rule-based narratives | LLM for context-aware natural language | 🔴 HIGH | **VERY HIGH** |
| **test-data-generator.py** | Faker templates for common types | LLM for domain-aware realistic data | 🔴 HIGH | **VERY HIGH** |
| **similar-code-finder.py** | Text similarity (difflib), regex matching | LLM for semantic similarity | 🔴 HIGH | **HIGH** |
| **dependency-impact-analyzer.py** | Static analysis (grep/rg), import tracking | LLM for breaking change risk assessment | 🟡 MEDIUM-HIGH | **HIGH** |

### Phase 4 Scope

**Implement enhancements for all 4 hooks**:

1. ✅ **Code Narrator Enhancement** (PostToolUse)
2. ✅ **Test Data Generator Enhancement** (UserPromptSubmit)
3. ✅ **Similar Code Finder Enhancement** (PostToolUse)
4. ✅ **Dependency Impact Analyzer Enhancement** (PreToolUse)

## Hybrid Pattern Architecture

### Pattern Definition

**Hybrid Pattern**: Combine fast bash/Python operations with smart LLM analysis

```
┌─────────────────────────────────────────────┐
│  Hook Execution Flow (Hybrid Pattern)      │
├─────────────────────────────────────────────┤
│                                             │
│  1. Event Triggered (PreToolUse, PostToolUse) │
│           ↓                                 │
│  2. Bash/Python Hook (Fast - ~100ms)       │
│     • Find files                            │
│     • Extract patterns                      │
│     • Count dependencies                    │
│     • Collect data                          │
│           ↓                                 │
│  3. Prompt-Based Hook (Smart - ~1-2s)      │
│     • Analyze data                          │
│     • Assess risk                           │
│     • Generate recommendations              │
│     • Provide context                       │
│           ↓                                 │
│  4. Combined Output to User                 │
│                                             │
└─────────────────────────────────────────────┘
```

### Configuration Strategy

**Option A: Sequential Hooks** (Current approach for Phases 1-3)
- Configure both hooks for same event
- Claude Code runs them sequentially
- User sees combined output

**Option B: Enhanced Hook Replaces Original** (Phase 4 approach)
- Prompt-based hook includes bash logic OR
- Prompt-based hook calls existing bash hook
- Single consolidated output

**Phase 4 Decision**: Use **Option A** (Sequential Hooks)
- Maintains existing hooks unchanged
- Add new prompt-based hooks alongside
- Users get best of both worlds
- Easy rollback if needed

## Implementation Details

### Hook 1: Code Narrator Enhancement

**Current Hook**: `.claude/hooks/python/code-narrator.py`

**Current Capabilities**:
- Detects change type (created, deleted, expanded, reduced, modified)
- Extracts functions, classes, imports via regex
- Counts error handling, documentation
- Generates rule-based narratives

**Limitations**:
- Rule-based narratives lack context awareness
- Can't understand intent or purpose
- Generic stakeholder summaries
- Misses semantic meaning

**Enhancement Strategy**:

Create **`code-narrator-llm`** prompt-based hook (PostToolUse) that:
1. Receives code change context
2. LLM analyzes actual change intent
3. Generates natural, context-aware narrative
4. Provides specific stakeholder-relevant insights

**Prompt Engineering**:
```
You are a code change narrator expert generating plain-English explanations.

File: $ARGUMENTS.filePath
Old content: $ARGUMENTS.oldString
New content: $ARGUMENTS.newString

Generate a narrative that:
1. Explains WHAT changed (functions, logic, dependencies)
2. Explains WHY (infer intent from change patterns)
3. Explains IMPACT (who needs to know, what to test)
4. Tailors message for different stakeholders

Be concise but insightful. Avoid jargon. Focus on business impact.
```

**Response Format**:
```json
{
  "narrative": "Plain English summary",
  "key_changes": ["Change 1", "Change 2"],
  "stakeholder_impact": {
    "pm": "Impact for project managers",
    "qa": "Impact for QA team",
    "docs": "Impact for documentation team"
  },
  "testing_recommendation": "What to test",
  "risk_level": "low|medium|high"
}
```

**Expected Improvement**:
- Better context awareness (understands intent, not just patterns)
- More accurate narratives (semantic understanding)
- Stakeholder messages tailored to actual changes
- Actionable testing recommendations

### Hook 2: Test Data Generator Enhancement

**Current Hook**: `.claude/hooks/python/test-data-generator.py`

**Current Capabilities**:
- Uses Faker library for realistic data
- Templates for common types (user, product, order, API)
- Detects data types from prompt keywords
- Generates edge cases

**Limitations**:
- Template-based (not context-aware)
- Domain knowledge limited to hardcoded patterns
- Can't understand project-specific entities
- Generic edge cases (not scenario-specific)

**Enhancement Strategy**:

Create **`test-data-generator-llm`** prompt-based hook (UserPromptSubmit) that:
1. Analyzes user's test writing intent
2. Understands domain context from codebase
3. Generates domain-specific, realistic test data
4. Suggests scenario-specific edge cases

**Prompt Engineering**:
```
You are a test data generation expert creating realistic, domain-appropriate test data.

User prompt: $ARGUMENTS.prompt
Project context: [Inferred from codebase if available]

Generate test data that:
1. Matches the domain (e-commerce, finance, healthcare, etc.)
2. Is realistic and internally consistent
3. Includes relevant edge cases for the scenario
4. Uses appropriate data types and formats

Provide data in the detected programming language format.
```

**Response Format**:
```json
{
  "data_type": "user|product|order|custom",
  "domain": "ecommerce|finance|healthcare|custom",
  "test_data": {...},
  "edge_cases": [...],
  "usage_example": "Code snippet",
  "rationale": "Why this data is appropriate"
}
```

**Expected Improvement**:
- Domain-aware data generation (understands context)
- Project-specific entities (not generic templates)
- Scenario-specific edge cases
- Realistic, internally consistent data

### Hook 3: Similar Code Finder Enhancement

**Current Hook**: `.claude/hooks/python/similar-code-finder.py`

**Current Capabilities**:
- Text-based similarity (difflib)
- Regex pattern matching (loops, conditionals, error handling)
- Finds files with similar names
- Searches for similar patterns via ripgrep

**Limitations**:
- Text similarity ≠ semantic similarity
- Misses functionally equivalent code with different syntax
- Can't identify refactoring opportunities
- No understanding of code intent

**Enhancement Strategy**:

Create **`similar-code-finder-llm`** prompt-based hook (PostToolUse) that:
1. Receives bash hook's findings (similar files, patterns)
2. LLM performs semantic analysis
3. Identifies true semantic duplicates
4. Suggests specific refactoring opportunities

**Prompt Engineering**:
```
You are a code similarity expert identifying semantic duplication and refactoring opportunities.

Modified file: $ARGUMENTS.filePath
Modified code: $ARGUMENTS.newString
Similar files found: [From bash hook]
Similar patterns found: [From bash hook]

Analyze and identify:
1. True semantic duplicates (functionally equivalent)
2. Refactoring opportunities (extract common logic)
3. Inconsistent implementations (same intent, different approach)
4. Specific refactoring steps

Be specific: provide file locations and refactoring patterns.
```

**Response Format**:
```json
{
  "semantic_duplicates": [
    {
      "file": "path/to/file.py",
      "similarity_reason": "Both implement X using Y pattern",
      "confidence": "high|medium|low"
    }
  ],
  "refactoring_opportunities": [
    {
      "pattern": "Extract common logic",
      "affected_files": ["file1", "file2"],
      "suggested_refactoring": "Create shared utility function",
      "effort": "low|medium|high"
    }
  ],
  "priority": "high|medium|low"
}
```

**Expected Improvement**:
- Semantic understanding (not just text matching)
- Identifies true duplicates (functionally equivalent)
- Actionable refactoring suggestions
- Prioritized by impact

### Hook 4: Dependency Impact Analyzer Enhancement

**Current Hook**: `.claude/hooks/python/dependency-impact-analyzer.py`

**Current Capabilities**:
- Finds files that import target file
- Identifies function callers via ripgrep
- Locates test files
- Calculates impact score (low/medium/high/critical)

**Limitations**:
- Impact score is simplistic (count-based)
- Can't assess breaking change risk
- No understanding of API contract changes
- Generic warnings (not specific to change)

**Enhancement Strategy**:

Create **`dependency-impact-analyzer-llm`** prompt-based hook (PreToolUse) that:
1. Receives bash hook's dependency analysis
2. LLM analyzes proposed change
3. Assesses breaking change risk
4. Provides specific migration guidance

**Prompt Engineering**:
```
You are a dependency impact expert assessing breaking change risk.

File being modified: $ARGUMENTS.filePath
Old content: [If available]
New content: [Proposed change]
Dependencies found: [From bash hook]
- X files import this module
- Functions called: [list]
- Test files: [list]

Analyze breaking change risk:
1. API contract changes (signature, return type, behavior)
2. Backward compatibility impact
3. Migration complexity (easy/medium/hard)
4. Specific files that need updates

Provide actionable guidance for safe migration.
```

**Response Format**:
```json
{
  "breaking_changes_detected": true|false,
  "risk_level": "low|medium|high|critical",
  "breaking_change_types": [
    {
      "type": "function_signature_change",
      "function": "foo()",
      "old_signature": "foo(a, b)",
      "new_signature": "foo(a, b, c)",
      "affected_files_count": 5
    }
  ],
  "migration_guidance": [
    {
      "file": "path/to/file.py",
      "required_change": "Add third parameter with default value",
      "difficulty": "easy"
    }
  ],
  "recommendation": "Specific steps to safely migrate",
  "estimated_effort": "2 hours (5 files to update)"
}
```

**Expected Improvement**:
- Breaking change detection (API contract analysis)
- Risk assessment beyond counts
- Specific migration guidance (file-by-file)
- Estimated migration effort

## Configuration

### settings.json Updates

Add 4 new prompt-based hooks to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "code-narrator-llm",
        "description": "Generates context-aware natural language narratives of code changes (Phase 4 - Hook Enhancement)",
        "hooks": [{
          "type": "prompt",
          "prompt": "...",
          "timeout": 25
        }],
        "toolNames": ["Edit", "Write", "MultiEdit"]
      },
      {
        "name": "similar-code-finder-llm",
        "description": "Finds semantically similar code using LLM analysis (Phase 4 - Hook Enhancement)",
        "hooks": [{
          "type": "prompt",
          "prompt": "...",
          "timeout": 25
        }],
        "toolNames": ["Edit", "MultiEdit"]
      }
    ],
    "PreToolUse": [
      {
        "name": "dependency-impact-analyzer-llm",
        "description": "Assesses breaking change risk with LLM intelligence (Phase 4 - Hook Enhancement)",
        "hooks": [{
          "type": "prompt",
          "prompt": "...",
          "timeout": 30
        }],
        "toolNames": ["Edit", "Write", "MultiEdit"]
      }
    ],
    "UserPromptSubmit": [
      {
        "name": "test-data-generator-llm",
        "description": "Generates domain-aware test data using LLM (Phase 4 - Hook Enhancement)",
        "hooks": [{
          "type": "prompt",
          "prompt": "...",
          "timeout": 25
        }]
      }
    ]
  }
}
```

### Integration with Existing Hooks

**Existing hooks remain active** and run independently. Users get:
1. Bash hook output (fast, data-focused)
2. LLM hook output (smart, analysis-focused)
3. Combined value

**Example flow** for dependency-impact-analyzer:
```
1. User edits file
2. dependency-impact-analyzer.py runs (bash)
   → Output: "⚠️ 5 files import this, 12 function calls"
3. dependency-impact-analyzer-llm runs (prompt)
   → Output: "🔴 BREAKING CHANGE: Function signature changed
              Affected files:
              - api/routes.py (update call to add 3rd param)
              - services/auth.py (update call to add 3rd param)
              Estimated effort: 30 minutes"
4. User sees both outputs
```

## Performance Characteristics

### Latency Analysis

| Hook | Bash Hook | LLM Hook | Total | Acceptable? |
|------|-----------|----------|-------|-------------|
| code-narrator | ~100ms | ~1.5s | ~1.6s | ✅ PostToolUse (informational) |
| test-data-generator | ~50ms | ~2s | ~2.05s | ✅ UserPromptSubmit (not blocking) |
| similar-code-finder | ~200ms | ~2s | ~2.2s | ✅ PostToolUse (informational) |
| dependency-impact | ~300ms | ~2.5s | ~2.8s | ✅ PreToolUse (critical info) |

**Total added latency**: ~2-2.5s per LLM hook execution

**Mitigation strategies**:
- Hooks are informational (don't block operations)
- Timeout protection (25-30s)
- Fail-open on errors
- Can disable individual hooks if needed

### Cost Analysis

**Model**: Haiku (fast, economical)

| Hook | Input Tokens | Output Tokens | Cost per Execution | Monthly (100 exec) |
|------|--------------|---------------|--------------------|--------------------|
| code-narrator-llm | ~600 | ~200 | ~$0.0002 | ~$0.02 |
| test-data-generator-llm | ~500 | ~300 | ~$0.00025 | ~$0.025 |
| similar-code-finder-llm | ~700 | ~250 | ~$0.00025 | ~$0.025 |
| dependency-impact-llm | ~800 | ~300 | ~$0.0003 | ~$0.03 |
| **Total** | | | | **~$0.10/month** |

**Cost**: Negligible (~$0.10/month for 100 executions per hook)

## Testing Strategy

### Test Scenarios

**Code Narrator LLM**:
- Edit file with obvious intent (bug fix, feature add, refactor)
- Verify narrative explains intent accurately
- Check stakeholder messages are specific

**Test Data Generator LLM**:
- Prompt: "Write test for user authentication"
- Verify generates auth-specific test data
- Check edge cases are authentication-relevant

**Similar Code Finder LLM**:
- Edit file with known semantic duplicates
- Verify identifies true duplicates (not just text matches)
- Check refactoring suggestions are actionable

**Dependency Impact Analyzer LLM**:
- Change function signature (breaking change)
- Verify detects breaking change
- Check migration guidance is specific and accurate

### Validation Checklist

- [ ] ⏳ settings.json valid JSON
- [ ] ⏳ All 4 LLM hooks configured
- [ ] ⏳ Prompts use proper format
- [ ] ⏳ Response format is valid JSON schema
- [ ] ⏳ Timeouts set appropriately
- [ ] ⏳ Tested code-narrator-llm
- [ ] ⏳ Tested test-data-generator-llm
- [ ] ⏳ Tested similar-code-finder-llm
- [ ] ⏳ Tested dependency-impact-analyzer-llm
- [ ] ⏳ Measured latency (<3s total)
- [ ] ⏳ Validated output quality improvements

## Success Metrics

### Quantitative Metrics

1. **Latency**: p95 <3s total (bash + LLM)
2. **Accuracy**: >90% correct intent identification
3. **Usefulness**: >80% of suggestions actionable
4. **Cost**: <$0.15/month total for all 4 hooks

### Qualitative Metrics

1. **Narrative Quality**: Context-aware, insightful vs. generic
2. **Test Data Realism**: Domain-appropriate vs. template-based
3. **Similarity Detection**: Semantic vs. text-only
4. **Impact Assessment**: Specific guidance vs. generic warnings

### Comparison Baseline

**Before Enhancement** (Bash hooks only):
- Narratives: Rule-based, generic
- Test data: Template-based, common types only
- Similarity: Text matching (difflib)
- Impact: Count-based scores (low/medium/high)

**After Enhancement** (Bash + LLM):
- Narratives: Context-aware, intent-focused
- Test data: Domain-aware, project-specific
- Similarity: Semantic understanding
- Impact: Breaking change detection, specific guidance

## Rollout Plan

### Phase 4A: Implementation (Week 1)

- [x] ✅ Analyze existing hooks
- [x] ✅ Design hybrid pattern
- [ ] ⏳ Implement 4 LLM hooks in settings.json
- [ ] ⏳ Configure proper prompts
- [ ] ⏳ Test individually
- [ ] ⏳ Validate JSON configuration

### Phase 4B: Testing (Week 2)

- [ ] ⏳ Test with Grey Haven team (5 developers)
- [ ] ⏳ Measure latency and accuracy
- [ ] ⏳ Collect feedback on usefulness
- [ ] ⏳ Tune prompts based on feedback
- [ ] ⏳ Address high-priority issues

### Phase 4C: Documentation (Week 2)

- [ ] ⏳ Create Phase 4 implementation documentation
- [ ] ⏳ Document hybrid pattern best practices
- [ ] ⏳ Update hook ecosystem inventory
- [ ] ⏳ Create user guide for enhanced hooks

### Phase 4D: Release (Week 3)

- [ ] ⏳ Enable for 100% of users
- [ ] ⏳ Publish documentation
- [ ] ⏳ Monitor metrics
- [ ] ⏳ Prepare for Phase 5 (Hybrid Patterns)

## Relationship to Other Phases

### Building on Previous Phases

**Phase 1** (Critical Safety):
- Established prompt-based hook patterns
- Validated LLM decision-making

**Phase 2** (Agent Quality Gates):
- Demonstrated agent-specific validation
- Showed value of specialized prompts

**Phase 3** (Code Quality & Testing):
- Context-aware evaluation patterns
- Smart TODO/WIP classification

**Phase 4** (Hook Enhancement):
- Applies learnings to existing hooks
- Establishes hybrid pattern
- Demonstrates enhancement value

### Preparing for Phase 5

**Phase 5** (Hybrid Patterns):
- Will formalize hybrid bash + LLM pattern
- Will create reusable templates
- Will migrate 5+ additional hooks
- Will document best practices

## Known Limitations

### Current Limitations

1. **Latency**: 2-3s added per LLM hook (acceptable for informational hooks)
2. **Cost**: ~$0.10/month (negligible)
3. **Accuracy**: LLM interpretation may vary on edge cases
4. **Context**: Limited to tool use context (no full project history)

### Mitigation Strategies

1. **Latency**: Informational hooks don't block, timeout protection
2. **Cost**: Use Haiku (cheapest model), monitor usage
3. **Accuracy**: Clear prompts, examples, regular tuning
4. **Context**: Provide relevant context in prompts

### Future Improvements

**Short term** (Phase 5):
- Formalize hybrid pattern with templates
- Optimize prompts to reduce token usage
- Add caching for repeated analyses

**Medium term**:
- Project-specific prompt tuning
- Learn from user feedback/overrides
- Integration with test runners, linters

**Long term**:
- Predictive enhancements (suggest before user asks)
- Cross-hook correlation (insights from multiple hooks)
- Custom domain-specific enhancements

## Next Steps

### Immediate (This Session)

1. ✅ Create Phase 4 implementation plan (this document)
2. ⏳ Implement 4 LLM hooks in settings.json
3. ⏳ Configure prompts with proper format
4. ⏳ Validate JSON configuration
5. ⏳ Create implementation documentation

### Short Term (Next Week)

6. ⏳ Test all 4 enhanced hooks
7. ⏳ Measure latency and quality
8. ⏳ Gather team feedback
9. ⏳ Tune prompts based on results
10. ⏳ Begin Phase 5 planning

## Conclusion

### Implementation Summary

**Phase 4 Scope**:
- 4 hooks enhanced with LLM intelligence
- Hybrid pattern established (bash + LLM)
- Existing hooks remain unchanged
- Users get best of both worlds

**Expected Impact**:
- Better code change narratives (context-aware)
- Smarter test data generation (domain-aware)
- Semantic similarity detection (not just text)
- Breaking change risk assessment (specific guidance)

**Success Criteria**:
- ✅ 4 hooks implemented and tested
- ✅ Hybrid pattern documented
- ✅ Latency <3s total
- ✅ User satisfaction >4/5
- ✅ Measurable quality improvement

### Readiness Status

**Status**: 🚧 **READY FOR IMPLEMENTATION**

**Next Action**: Implement 4 LLM hooks in settings.json

---

**Last Updated**: 2025-11-11
**Status**: Implementation Plan Complete
**Phase**: 4 of 5
**Priority**: 🟡 MEDIUM-HIGH

**Total Hooks Implemented**: 8 prompt-based hooks (Phase 1-3) + 4 enhanced hooks (Phase 4) = 12 hooks

**Coverage**: Critical Safety ✅ | Agent Quality ✅ | Code Quality ✅ | Hook Enhancement 🚧
