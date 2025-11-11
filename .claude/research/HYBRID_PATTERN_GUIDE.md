# Hybrid Hook Pattern Guide

**Date**: 2025-11-11
**Version**: 1.0
**Status**: ✅ COMPLETE

## Executive Summary

The **Hybrid Hook Pattern** combines fast bash/Python data collection with intelligent LLM analysis to create hooks that are both performant and insightful. This guide provides comprehensive documentation, templates, and best practices for implementing hybrid hooks in the Claude Code ecosystem.

**Key Benefits**:
- ✅ **Performance**: Fast data collection (bash) + smart analysis (LLM)
- ✅ **Cost-effective**: Pre-filtering reduces LLM token usage
- ✅ **Reliable**: Bash provides factual baseline even if LLM fails
- ✅ **Independent**: Easy to enable/disable components separately
- ✅ **Maintainable**: Clear separation of concerns

## Table of Contents

1. [Pattern Overview](#pattern-overview)
2. [Architecture](#architecture)
3. [When to Use Hybrid Patterns](#when-to-use-hybrid-patterns)
4. [Implementation Guide](#implementation-guide)
5. [Templates](#templates)
6. [Best Practices](#best-practices)
7. [Examples from Phases 1-4](#examples-from-phases-1-4)
8. [Performance Optimization](#performance-optimization)
9. [Testing Strategy](#testing-strategy)
10. [Common Pitfalls](#common-pitfalls)

## Pattern Overview

### What is the Hybrid Hook Pattern?

The Hybrid Hook Pattern pairs a **data collection hook** (bash/Python) with an **intelligent analysis hook** (LLM) to provide comprehensive insights.

**Simple Definition**:
> Bash finds the facts, LLM explains what they mean.

**Visual Representation**:

```
┌─────────────────────────────────────────────────────┐
│           Hybrid Hook Pattern Flow                   │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Event Triggered (PreToolUse, PostToolUse, etc.)    │
│              ↓                                        │
│  ┌──────────────────────────┐                       │
│  │  Bash/Python Hook        │                       │
│  │  (Fast ~100-300ms)       │                       │
│  └──────────────────────────┘                       │
│              ↓                                        │
│  • Find files                                        │
│  • Extract patterns                                  │
│  • Count dependencies                                │
│  • Collect metrics                                   │
│              ↓                                        │
│  ┌──────────────────────────┐                       │
│  │  LLM Hook                │                       │
│  │  (Smart ~1.5-2.5s)       │                       │
│  └──────────────────────────┘                       │
│              ↓                                        │
│  • Analyze context                                   │
│  • Assess risk                                       │
│  • Infer intent                                      │
│  • Generate recommendations                          │
│              ↓                                        │
│  Combined Output to User                             │
│  • Facts + Intelligence                              │
│                                                       │
└─────────────────────────────────────────────────────┘
```

### Pattern Types

We've identified three main hybrid pattern types based on Phases 1-4:

#### Type 1: Data Collection + Analysis (Phase 4)

**Bash**: Collects data
**LLM**: Analyzes and provides insights

**Examples**:
- code-narrator: Bash extracts patterns → LLM explains intent
- test-data-generator: Bash detects context → LLM generates domain-specific data
- similar-code-finder: Bash finds text matches → LLM identifies semantic duplicates
- dependency-impact: Bash counts dependencies → LLM assesses breaking changes

**Best for**: Informational hooks that enhance understanding

#### Type 2: Validation + Smart Assessment (Phases 1-3)

**Bash**: Could do fast pattern checks (optional)
**LLM**: Performs intelligent validation with context awareness

**Examples**:
- destructive-operation-validator: LLM evaluates risk of bash commands
- security-file-protection: LLM understands security implications
- tdd-completion-validator: LLM validates methodology adherence
- work-completion-validator: LLM distinguishes acceptable vs. blocking TODOs

**Best for**: Quality gates and safety validations

#### Type 3: Fast Check + Deep Analysis (Future)

**Bash**: Quick pass/fail check
**LLM**: Only runs if bash check triggers (conditional execution)

**Example Pattern**:
```
Bash: Is this a test file? → No → Skip LLM
                          ↓
                         Yes
                          ↓
LLM: Would this reduce coverage? → Assess and decide
```

**Best for**: Performance-critical paths where LLM only needed sometimes

## Architecture

### Sequential Execution Model

Claude Code hooks with the same event type execute **sequentially** in configuration order:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "bash-hook",
        "hooks": [{"type": "script", "script": "./bash-hook.sh"}],
        "toolNames": ["Edit"]
      },
      {
        "name": "llm-hook",
        "hooks": [{"type": "prompt", "prompt": "..."}],
        "toolNames": ["Edit"]
      }
    ]
  }
}
```

**Execution order**:
1. bash-hook runs (100ms)
2. bash-hook output shown to user
3. llm-hook runs (2s)
4. llm-hook output shown to user

**Total time**: ~2.1s

### Communication Between Hooks

**Current State**: Hooks operate independently (no direct communication)

**Implication**: LLM hooks cannot directly access bash hook output

**Solution**: LLM hooks re-analyze the same context using $ARGUMENTS

**Example**:
```
Bash Hook:
  Input: $ARGUMENTS.filePath
  Action: Count dependencies with ripgrep
  Output: "Found 12 dependencies"

LLM Hook:
  Input: $ARGUMENTS.filePath (same context)
  Action: Analyze for breaking changes
  Output: "Breaking change detected: function signature changed"
```

Both analyze the same file, but from different perspectives (counting vs. understanding).

### Event Type Coverage

| Event | Bash Speed | LLM Value | Hybrid Benefit |
|-------|------------|-----------|----------------|
| **PreToolUse** | High (prevents ops) | High (smart decisions) | Critical for safety |
| **PostToolUse** | High (quick info) | High (insights) | Excellent for analysis |
| **UserPromptSubmit** | Medium (context detection) | High (understanding) | Good for assistance |
| **SubagentStop** | Low (limited context) | High (quality gates) | LLM-focused |
| **Stop** | Low (limited context) | High (completion checks) | LLM-focused |

**Recommendation**: Hybrid pattern most valuable for PreToolUse and PostToolUse events.

## When to Use Hybrid Patterns

### Decision Framework

```
┌─────────────────────────────────────────────┐
│  Should I use a Hybrid Pattern?            │
├─────────────────────────────────────────────┤
│                                             │
│  Is there data to collect?                 │
│  ├─ Yes: Can bash collect it quickly?     │
│  │  ├─ Yes: Hybrid candidate ✓            │
│  │  └─ No: LLM-only                       │
│  └─ No: LLM-only                          │
│                                             │
│  Does analysis require context?            │
│  ├─ Yes: Is context complex/semantic?     │
│  │  ├─ Yes: Hybrid or LLM-only ✓         │
│  │  └─ No: Bash-only                      │
│  └─ No: Bash-only                         │
│                                             │
│  What's the performance requirement?       │
│  ├─ <500ms: Bash-only                     │
│  ├─ <3s: Hybrid ✓                         │
│  └─ >3s acceptable: LLM-only              │
│                                             │
│  What's the cost tolerance?                │
│  ├─ Minimize: Bash-only                   │
│  ├─ Moderate: Hybrid ✓                    │
│  └─ Quality matters most: LLM-only        │
│                                             │
└─────────────────────────────────────────────┘
```

### Use Hybrid When:

✅ **Data collection is well-defined** (files, patterns, counts)
✅ **Analysis requires understanding** (intent, risk, semantic meaning)
✅ **Latency <3s is acceptable** (informational hooks)
✅ **You want factual baseline + insights** (best of both worlds)
✅ **Cost is a consideration** (bash pre-filters, reduces LLM tokens)

### Use Bash-Only When:

✅ **Analysis is deterministic** (regex, counting, sorting)
✅ **Latency must be <500ms** (blocking operations)
✅ **Cost must be zero** (no LLM calls)
✅ **Context is simple** (pattern matching sufficient)

### Use LLM-Only When:

✅ **No data collection needed** (context provided by Claude Code)
✅ **Analysis requires deep understanding** (intent, semantic, contextual)
✅ **Latency up to 5s acceptable** (complex analysis)
✅ **Quality more important than cost** (critical decisions)

## Implementation Guide

### Step-by-Step: Creating a Hybrid Hook

#### Step 1: Identify the Need

**Question**: What problem am I solving?

**Example**: "I want to detect when developers are about to commit secrets to git"

#### Step 2: Define Bash Component

**Question**: What data can bash collect quickly?

**Example**:
- Scan staged files for patterns (API keys, passwords, tokens)
- Check file extensions (.env, .pem, credentials.json)
- Search for regex patterns (API_KEY=, password:, secret=)

**Implementation**:
```bash
#!/usr/bin/env bash
# secret-detector.sh

# Scan staged files
FILES=$(git diff --cached --name-only)

# Check for secret patterns
SECRETS_FOUND=0
for file in $FILES; do
    # Check file extensions
    if [[ "$file" =~ \.(pem|key|env)$ ]]; then
        echo "⚠️ Secret file detected: $file"
        SECRETS_FOUND=1
    fi

    # Check content patterns
    if git diff --cached "$file" | grep -E "API_KEY|password|secret|token" > /dev/null; then
        echo "⚠️ Secret pattern in: $file"
        SECRETS_FOUND=1
    fi
done

if [ $SECRETS_FOUND -eq 1 ]; then
    echo "🔴 Potential secrets detected in commit"
fi
```

**Output**: Fast facts (which files, which patterns)

#### Step 3: Define LLM Component

**Question**: What intelligent analysis adds value?

**Example**:
- Distinguish false positives (test fixtures, examples)
- Assess severity (production keys vs. development placeholders)
- Provide specific remediation (use environment variables, secret manager)
- Check if secrets are already gitignored

**Implementation**:
```json
{
  "name": "secret-analyzer-llm",
  "description": "Analyzes detected secrets for severity and remediation",
  "hooks": [{
    "type": "prompt",
    "prompt": "You are a security expert analyzing potential secrets in code.\n\nFiles flagged: [from bash hook]\nPatterns found: [from bash hook]\n\nAnalyze:\n1. False positive rate (test fixtures, examples, placeholders?)\n2. Severity (production vs. development secrets?)\n3. Remediation (specific steps to secure)\n\nRespond with JSON:\n{\n  \"is_false_positive\": true|false,\n  \"severity\": \"critical|high|medium|low\",\n  \"rationale\": \"Why this is/isn't a secret\",\n  \"remediation\": \"Specific steps\"\n}",
    "timeout": 25
  }],
  "toolNames": ["Bash"]
}
```

**Output**: Smart analysis (severity, remediation, context)

#### Step 4: Configure in settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "secret-detector",
        "description": "Detects potential secrets in commits (bash)",
        "hooks": [{
          "type": "script",
          "script": ".claude/hooks/bash/secret-detector.sh"
        }],
        "toolNames": ["Bash"]
      },
      {
        "name": "secret-analyzer-llm",
        "description": "Analyzes secrets with intelligent assessment (LLM)",
        "hooks": [{
          "type": "prompt",
          "prompt": "..."
        }],
        "toolNames": ["Bash"]
      }
    ]
  }
}
```

#### Step 5: Test

```bash
# Test bash component
echo "API_KEY=test123" > test.py
git add test.py
# → Should detect secret pattern

# Test LLM component
# → Should analyze if "test123" is real secret or placeholder

# Test combined
# → User sees: Facts (pattern found) + Analysis (severity, remediation)
```

## Templates

### Template 1: Data Collection + Analysis Pattern

**Use for**: PostToolUse hooks that provide insights

**Bash Template**:
```bash
#!/usr/bin/env bash
# [hook-name]-data-collector.sh

# 1. Extract context from arguments
FILE_PATH="$1"
TOOL_NAME="$2"

# 2. Collect data quickly
# - Find relevant files
# - Extract patterns
# - Count occurrences
# - Gather metrics

# 3. Output structured data
echo "=== Data Collection Results ==="
echo "Metric 1: [value]"
echo "Metric 2: [value]"
echo "Found X items in Y locations"

exit 0  # Always exit 0 (don't block operations)
```

**LLM Template**:
```json
{
  "name": "[hook-name]-analyzer",
  "description": "Analyzes [data type] with intelligent insights",
  "hooks": [{
    "type": "prompt",
    "prompt": "You are a [domain] expert analyzing [context].\n\nContext: $ARGUMENTS.filePath\nTool: $ARGUMENTS.toolName\n\n**Your Task**:\n\nAnalyze the [data type] and provide:\n1. [Insight type 1]\n2. [Insight type 2]\n3. [Recommendation type]\n\n**Response Format** (JSON only):\n\n{\n  \"analysis\": \"Brief summary\",\n  \"insights\": [\n    {\"type\": \"...\", \"detail\": \"...\"}\n  ],\n  \"recommendations\": [\n    {\"action\": \"...\", \"rationale\": \"...\"}\n  ],\n  \"priority\": \"high|medium|low\"\n}\n\nRespond with JSON only.",
    "timeout": 25
  }],
  "toolNames": ["Edit", "Write", "MultiEdit"]
}
```

### Template 2: Validation + Smart Assessment Pattern

**Use for**: PreToolUse hooks that enforce quality gates

**LLM Template** (bash optional for this pattern):
```json
{
  "name": "[validation-name]",
  "description": "Validates [aspect] with intelligent assessment",
  "hooks": [{
    "type": "prompt",
    "prompt": "You are a [domain] validation expert.\n\nContext: $ARGUMENTS.filePath\nOperation: $ARGUMENTS.toolName\n\n**Validation Criteria**:\n\n1. [Criterion 1]\n2. [Criterion 2]\n3. [Criterion 3]\n\n**Decision Logic**:\n\nBLOCK if:\n- [Blocking condition 1]\n- [Blocking condition 2]\n\nWARN if:\n- [Warning condition 1]\n- [Warning condition 2]\n\nAPPROVE if:\n- [Approval condition 1]\n- [Approval condition 2]\n\n**Response Format**:\n\nBlock:\n{\n  \"decision\": \"block\",\n  \"reason\": \"[specific reason]\",\n  \"systemMessage\": \"[user-facing message with remediation steps]\"\n}\n\nWarn:\n{\n  \"decision\": \"approve\",\n  \"systemMessage\": \"⚠️ [warning message]\"\n}\n\nApprove:\n{\n  \"decision\": \"approve\"\n}\n\nRespond with JSON only.",
    "timeout": 30
  }],
  "toolNames": ["Bash", "Write", "Edit", "MultiEdit"]
}
```

### Template 3: Conditional Execution Pattern (Future)

**Use for**: Performance-critical paths with conditional LLM usage

**Bash Template** (with LLM trigger):
```bash
#!/usr/bin/env bash
# [hook-name]-fast-check.sh

# Fast pattern check
if [[ condition_that_needs_llm ]]; then
    # Write flag file to trigger LLM
    echo "trigger" > /tmp/llm-needed.flag
    echo "⚠️ Condition detected, running deep analysis..."
else
    echo "✅ Fast check passed, no deep analysis needed"
fi

exit 0
```

**LLM Template** (conditional execution):
```json
{
  "name": "[hook-name]-deep-analysis",
  "description": "Deep analysis when fast check triggers",
  "hooks": [{
    "type": "prompt",
    "prompt": "Check if /tmp/llm-needed.flag exists. If not, return {\"decision\": \"approve\"}.\n\nIf exists, perform deep analysis:\n\n[Analysis logic]\n\nRespond with JSON only.",
    "timeout": 30
  }],
  "toolNames": ["Bash"]
}
```

**Note**: This pattern requires LLM to check flag file, not yet optimized. Future Claude Code versions may support native conditional execution.

## Best Practices

### 1. Design Principles

#### Separation of Concerns

**✅ Do**:
- Bash: Data collection and fast pattern matching
- LLM: Context understanding and intelligent analysis

**❌ Don't**:
- Bash: Complex analysis or decision-making
- LLM: File searching or pattern counting (waste of tokens)

#### Fail-Open Philosophy

**✅ Do**:
- Bash hooks: `exit 0` (always succeed)
- LLM hooks: timeout protection, default to approve on errors
- Both: Informational by default

**❌ Don't**:
- Bash hooks: `exit 1` unless absolutely critical
- LLM hooks: Block operations on errors
- Either: Fail without clear user guidance

#### Clear User Communication

**✅ Do**:
- Bash: Factual output ("Found 12 dependencies")
- LLM: Contextual insights ("Breaking change detected: signature changed")
- Both: Actionable recommendations

**❌ Don't**:
- Bash: Vague messages ("Something wrong")
- LLM: Technical jargon without explanation
- Either: Output without context

### 2. Performance Optimization

#### Minimize Bash Execution Time

```bash
# ❌ Slow: Search entire codebase
find . -name "*.py" | xargs grep "pattern"

# ✅ Fast: Use ripgrep with limits
rg -l --max-count 10 "pattern" --type py

# ❌ Slow: Multiple passes
for file in $(find . -name "*.py"); do
    grep "pattern1" "$file"
    grep "pattern2" "$file"
done

# ✅ Fast: Single pass with combined patterns
rg "pattern1|pattern2" --type py
```

#### Minimize LLM Token Usage

**✅ Do**:
- Pre-filter data with bash (reduce context size)
- Use structured prompts (clear, concise)
- Limit output format (JSON schema)
- Use shortest model (Haiku) when possible

**❌ Don't**:
- Send full file contents to LLM (use bash to extract relevant parts)
- Use verbose prompts (be concise)
- Allow free-form output (always use JSON)
- Use Opus for simple tasks (waste of cost)

#### Set Appropriate Timeouts

| Hook Complexity | Timeout | Rationale |
|----------------|---------|-----------|
| Simple pattern check | 20s | Fast LLM response |
| Medium analysis | 25s | Standard response time |
| Complex analysis | 30s | Allows thorough evaluation |
| Critical safety | 35s | Extra buffer for important decisions |

### 3. Prompt Engineering

#### Structure Your Prompts

```
✅ Good Prompt Structure:

1. Role Definition: "You are a [domain] expert..."
2. Context Provision: "File: $ARGUMENTS.filePath"
3. Task Description: "Analyze for [specific aspect]"
4. Evaluation Criteria: Numbered list of what to check
5. Decision Logic: Clear BLOCK/WARN/APPROVE conditions
6. Response Format: JSON schema
7. Final Instruction: "Respond with JSON only"
```

```
❌ Bad Prompt Structure:

"Look at this file and tell me if there are any issues with it."

- No role definition
- No specific criteria
- Vague instructions
- No response format
```

#### Use $ARGUMENTS Effectively

**Available Context**:
- `$ARGUMENTS.filePath` - File being modified
- `$ARGUMENTS.toolName` - Tool being used (Edit, Write, Bash, etc.)
- `$ARGUMENTS.arguments` - Tool arguments (if applicable)
- `$ARGUMENTS.prompt` - User prompt (for UserPromptSubmit)
- `$ARGUMENTS.cwd` - Current working directory

**Example**:
```
Context: $ARGUMENTS.filePath
Tool: $ARGUMENTS.toolName

If tool is "Bash", analyze command for safety.
If tool is "Edit", analyze code changes.
If tool is "Write", analyze new file creation.
```

#### Provide Examples in Prompts

```
✅ With Examples:

Response Format:

High risk:
{
  "decision": "block",
  "reason": "Breaking change detected",
  "systemMessage": "🔴 BREAKING CHANGE\\n\\nSpecific issue...\\n\\nActions required..."
}

Low risk:
{
  "decision": "approve",
  "systemMessage": "✅ Safe change detected"
}
```

```
❌ Without Examples:

Respond with JSON containing decision, reason, and systemMessage fields.
```

### 4. Testing Strategy

#### Test Bash Component Independently

```bash
# Unit test the bash hook
cd .claude/hooks/bash
./dependency-analyzer.sh /path/to/test/file.py

# Expected output:
# Found 5 imports
# 3 files depend on this
# 2 test files found
```

#### Test LLM Component Independently

```bash
# Simulate LLM hook with test context
echo '{
  "filePath": "/test/file.py",
  "toolName": "Edit"
}' | jq -c '.' | # In real scenario, Claude Code provides context

# Manually verify LLM response format
```

#### Test Combined Hybrid Hook

```bash
# 1. Make a change that triggers both hooks
echo "def new_function():" >> test.py
git add test.py

# 2. Observe bash output (facts)
# Expected: "Modified file: test.py, Added 1 function"

# 3. Observe LLM output (analysis)
# Expected: "Intent: feature_addition, Impact: low, Testing: verify new_function()"

# 4. Verify combined value
# Facts + Insights = Better understanding
```

### 5. Maintenance

#### Version Your Hooks

```bash
# In hook file header
#!/usr/bin/env bash
# Version: 1.2.0
# Last updated: 2025-11-11
# Author: Grey Haven Studio
# Description: Dependency impact analyzer
```

#### Monitor Performance

```bash
# Add timing to bash hooks
START=$(date +%s%N)
# ... hook logic ...
END=$(date +%s%N)
ELAPSED=$(( (END - START) / 1000000 ))  # Convert to ms
echo "# Execution time: ${ELAPSED}ms" >&2
```

#### Collect Metrics

```json
{
  "hook_metrics": {
    "executions": 150,
    "avg_latency_ms": 1800,
    "false_positive_rate": 0.05,
    "user_satisfaction": 4.2
  }
}
```

## Examples from Phases 1-4

### Example 1: Code Narrator (Phase 4 - Data + Analysis)

**Bash Component**: `.claude/hooks/python/code-narrator.py`
- Extracts functions, classes, imports (regex)
- Counts error handling, documentation
- Detects file type and change type

**LLM Component**: `code-narrator-llm`
- Infers intent (bug fix, feature, refactoring)
- Explains WHY changes were made
- Provides stakeholder-specific insights
- Assesses risk level

**Hybrid Value**: Facts (what changed) + Intelligence (why and impact)

### Example 2: Dependency Impact (Phase 4 - Data + Analysis)

**Bash Component**: `.claude/hooks/python/dependency-impact-analyzer.py`
- Finds files that import target file (ripgrep)
- Identifies function callers
- Locates test files
- Calculates dependency count

**LLM Component**: `dependency-impact-analyzer-llm`
- Detects breaking changes (API signatures)
- Assesses risk beyond counts
- Provides file-by-file migration guidance
- Estimates effort

**Hybrid Value**: Facts (who depends) + Intelligence (breaking change risk)

### Example 3: TDD Completion (Phase 2 - LLM-focused)

**Bash Component**: None (not needed)

**LLM Component**: `tdd-completion-validator`
- Validates RED-GREEN-REFACTOR cycle
- Checks coverage thresholds
- Assesses test quality
- Verifies methodology adherence

**Pattern**: LLM-only (no data collection needed, agent context provided)

### Example 4: Destructive Operations (Phase 1 - LLM-focused)

**Bash Component**: None (command provided by Claude Code)

**LLM Component**: `destructive-operation-validator`
- Evaluates bash command for risk
- Detects force operations, deletions, production changes
- Provides specific mitigation steps

**Pattern**: LLM-only (validates tool arguments, no external data needed)

## Performance Optimization

### Optimization Strategies

#### 1. Pre-filter with Bash

**Before** (LLM analyzes everything):
```json
{
  "prompt": "Analyze all files in project for security issues..."
}
```
**Cost**: High (large context)
**Time**: Slow (many tokens)

**After** (Bash pre-filters):
```bash
# Bash: Find only security-sensitive files
rg -l "password|secret|key" --type py
```
**LLM**: Analyze only flagged files
**Cost**: Low (focused context)
**Time**: Fast (fewer tokens)

#### 2. Cache Results

```bash
# Bash hook with caching
CACHE_FILE="/tmp/dependency-cache-$(md5sum $FILE_PATH | cut -d' ' -f1).json"

if [ -f "$CACHE_FILE" ] && [ "$CACHE_FILE" -nt "$FILE_PATH" ]; then
    cat "$CACHE_FILE"
    exit 0
fi

# Calculate dependencies...
echo "$RESULT" | tee "$CACHE_FILE"
```

**Note**: Cache invalidation is important (use file modification time)

#### 3. Limit Search Scope

```bash
# ❌ Slow: Search entire project
find . -type f -name "*.py"

# ✅ Fast: Limit to relevant directories
find src/ tests/ -type f -name "*.py" -maxdepth 3
```

#### 4. Parallel Processing

```bash
# ❌ Sequential
for file in $FILES; do
    analyze "$file"
done

# ✅ Parallel (use xargs)
echo "$FILES" | xargs -P 4 -I {} analyze {}
```

#### 5. Short-Circuit Evaluation

```bash
# ❌ Always check everything
check_condition_1
check_condition_2
check_condition_3

# ✅ Stop early if possible
check_condition_1 && {
    echo "Condition 1 failed, skipping rest"
    exit 0
}
```

### Performance Targets

| Hook Type | Target Latency | Acceptable Latency |
|-----------|----------------|-------------------|
| Bash-only | <200ms | <500ms |
| LLM-only | <2s | <3s |
| Hybrid (bash + LLM) | <2.5s | <4s |
| Critical safety | N/A | <5s (quality matters more) |

## Testing Strategy

### Test Levels

#### 1. Unit Testing (Individual Components)

**Bash Hook Unit Test**:
```bash
#!/usr/bin/env bash
# test-dependency-analyzer.sh

# Test 1: No dependencies
./dependency-analyzer.sh empty-file.py
# Expected: "No dependencies found"

# Test 2: Multiple dependencies
./dependency-analyzer.sh complex-file.py
# Expected: "Found 5 imports, 3 dependent files"

# Test 3: Edge case
./dependency-analyzer.sh nonexistent.py
# Expected: Graceful handling, exit 0
```

**LLM Hook Unit Test**:
```bash
# Simulate context
echo '{
  "filePath": "test.py",
  "toolName": "Edit",
  "oldString": "def foo(a, b):",
  "newString": "def foo(a, b, c):"
}' > /tmp/test-context.json

# Verify LLM detects breaking change
# Expected: {"breaking_changes_detected": true}
```

#### 2. Integration Testing (Combined Hooks)

**Test Scenario**:
```bash
# Setup
echo "import requests" > test.py
git add test.py

# Execute hooks
# 1. Bash hook should run
# 2. LLM hook should run
# 3. Both outputs should appear

# Verify
# - Bash output: "Found 1 import: requests"
# - LLM output: "External dependency added, ensure version pinned"
```

#### 3. End-to-End Testing (Real Usage)

**Test Cases**:
1. **Happy Path**: Normal code change
2. **Edge Case**: Empty file, special characters
3. **Error Handling**: Non-existent file, permission denied
4. **Performance**: Large file, many dependencies
5. **False Positives**: Test fixtures, examples

### Validation Checklist

- [ ] Bash hook runs successfully
- [ ] Bash hook output is clear and factual
- [ ] Bash hook completes <500ms
- [ ] LLM hook runs successfully
- [ ] LLM hook output is insightful and actionable
- [ ] LLM hook completes <3s
- [ ] Combined output provides value
- [ ] No false positives (or <10% rate)
- [ ] Error handling is graceful
- [ ] User guidance is clear

## Common Pitfalls

### Pitfall 1: Bash Hook Blocks Operations

**Problem**:
```bash
#!/usr/bin/env bash
# Bad: exits with error
if [ condition ]; then
    exit 1  # BLOCKS CLAUDE CODE
fi
```

**Solution**:
```bash
#!/usr/bin/env bash
# Good: always exits successfully
if [ condition ]; then
    echo "⚠️ Warning: condition detected"
fi
exit 0  # NEVER BLOCKS
```

**Principle**: Bash hooks should be informational, LLM hooks should enforce gates.

### Pitfall 2: LLM Hook Analyzes What Bash Already Did

**Problem**:
```json
{
  "prompt": "Count the number of functions in $ARGUMENTS.filePath and analyze them..."
}
```
**Issue**: LLM counting is slow and expensive (bash should do this)

**Solution**:
```bash
# Bash: COUNT=$(rg "^def " file.py | wc -l)
# LLM: Analyze WHAT the functions do, not count them
```

**Principle**: Bash counts, LLM understands.

### Pitfall 3: Too Much Context to LLM

**Problem**:
```json
{
  "prompt": "Analyze all 500 files in the project for security issues..."
}
```
**Issue**: Huge token usage, slow, expensive

**Solution**:
```bash
# Bash: Pre-filter to 5 suspicious files
# LLM: Analyze only the 5 flagged files
```

**Principle**: Bash filters, LLM analyzes filtered results.

### Pitfall 4: Unclear User Messages

**Problem**:
```bash
echo "Error: condition failed"
```
**Issue**: User doesn't know what to do

**Solution**:
```bash
echo "⚠️ Dependency Detected"
echo ""
echo "Found: requests library"
echo "Action: Add to requirements.txt"
echo "Why: Ensures reproducible builds"
```

**Principle**: Every message should be actionable.

### Pitfall 5: No Timeout Protection

**Problem**:
```json
{
  "type": "prompt",
  "prompt": "...",
  "timeout": 60  # Too long
}
```
**Issue**: User waits 60s for response

**Solution**:
```json
{
  "type": "prompt",
  "prompt": "...",
  "timeout": 25  # Reasonable for informational
}
```

**Principle**: Fail fast, don't make users wait.

### Pitfall 6: Inconsistent Response Formats

**Problem**:
```
Sometimes: {"decision": "approve"}
Sometimes: {"status": "ok"}
Sometimes: Just text
```

**Solution**:
```
Always: {"decision": "approve|block", "reason": "...", "systemMessage": "..."}
```

**Principle**: Consistent schema makes hooks reliable.

## Advanced Patterns

### Pattern 1: Cascading Analysis

**Concept**: Bash → Fast LLM → Deep LLM (if needed)

```
Bash: Is this a security file? → Yes
Fast LLM: Is change risky? → Yes (high confidence)
Deep LLM: Detailed security analysis
```

**Use case**: Performance-critical with occasional deep analysis

### Pattern 2: Multi-Stage Filtering

**Concept**: Bash → Filter 1 → LLM → Filter 2 → Output

```
Bash: Find 100 potential duplicates
LLM: Analyze top 10 most likely
Output: 3 true duplicates with recommendations
```

**Use case**: Large search space, need intelligent prioritization

### Pattern 3: Feedback Loop

**Concept**: LLM suggests → Bash validates → LLM refines

```
LLM: "Consider refactoring function X"
Bash: Check if function X exists, is used
LLM: Refine recommendation based on usage
```

**Use case**: Iterative improvement suggestions

**Note**: Requires multiple hook executions, not currently supported in single event.

## Conclusion

### Key Takeaways

1. **Hybrid = Fast + Smart**: Bash collects data quickly, LLM analyzes intelligently
2. **Pre-filter for Performance**: Reduce LLM token usage with bash pre-filtering
3. **Fail Open**: Hooks should inform, not block (unless critical safety)
4. **Clear Communication**: Every message should be actionable
5. **Test Thoroughly**: Unit test components, integration test combined

### Pattern Selection Summary

| Need | Pattern | Components |
|------|---------|------------|
| Informational insights | Data + Analysis | Bash + LLM |
| Safety validation | Smart Assessment | LLM (bash optional) |
| Performance critical | Bash-only | Bash |
| Complex understanding | LLM-only | LLM |
| Occasional deep analysis | Conditional | Bash + LLM (conditional) |

### Future Directions

**Phase 5 Opportunities**:
- Formalize conditional execution (bash triggers LLM)
- Create hook testing framework
- Develop hook performance profiler
- Build hook marketplace

**Claude Code Feature Requests**:
- Native hybrid hook support (automatic pairing)
- Hook communication (pass data between hooks)
- Conditional execution primitives
- Hook performance metrics dashboard

---

**Version**: 1.0
**Last Updated**: 2025-11-11
**Status**: Complete and ready for use
**Next Steps**: Apply patterns to new hook development

**Feedback**: Report issues or suggestions to Grey Haven Studio

---

## Appendix: Quick Reference

### Bash Hook Template (Minimal)

```bash
#!/usr/bin/env bash
FILE_PATH="$1"

# Collect data
RESULT=$(some_analysis "$FILE_PATH")

# Output
echo "$RESULT"

exit 0  # Always succeed
```

### LLM Hook Template (Minimal)

```json
{
  "name": "hook-name",
  "description": "Brief description",
  "hooks": [{
    "type": "prompt",
    "prompt": "You are a [role].\n\nContext: $ARGUMENTS.filePath\n\nTask: [task]\n\nRespond with JSON:\n{\"analysis\": \"...\", \"recommendation\": \"...\"}",
    "timeout": 25
  }],
  "toolNames": ["Edit", "Write"]
}
```

### Decision Framework (One-Liner)

**Bash-only**: Fast + deterministic
**LLM-only**: Complex + understanding needed
**Hybrid**: Data collection + intelligent analysis
