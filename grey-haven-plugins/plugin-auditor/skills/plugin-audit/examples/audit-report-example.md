# Example Audit Report

Example output from the plugin-auditor agent.

## Sample Audit: core Plugin

```markdown
# Plugin Audit Report: core

**Audit Date**: 2026-01-08
**Claude Code Version**: v2.1.0
**Auditor**: plugin-auditor agent

## Summary

| Metric | Value |
|--------|-------|
| **Overall Score** | 82/100 |
| **Structure** | ✅ Valid |
| **Deprecations** | 0 found |
| **Missing Features** | 4 recommendations |

## Structure Analysis

### Directory Structure ✅
```
core/
├── .claude-plugin/
│   └── plugin.json         ✅ Valid
├── agents/
│   ├── code-quality-analyzer.md
│   ├── documentation-alignment-verifier.md
│   ├── performance-optimizer.md
│   ├── prompt-engineer.md
│   ├── tdd-orchestrator.md
│   ├── tdd-python.md
│   └── tdd-typescript.md
├── commands/
│   ├── code-review.md
│   ├── debug-chain.md
│   └── tdd-implement.md
└── skills/
    ├── code-quality-analysis/
    ├── tdd-typescript/
    └── ...
```

### plugin.json ✅
- `name`: ✅ Present
- `description`: ✅ Present
- `version`: ✅ Present (1.0.0)
- `author`: ✅ Present
- `keywords`: ✅ Present (7 keywords)
- `license`: ✅ Present (MIT)
- `skills`: ✅ Present (12 skills)

## Agent Analysis

### tdd-typescript-implementer

**Frontmatter:**
```yaml
name: tdd-typescript-implementer ✅
description: "Expert TypeScript..." ✅ (includes examples)
model: sonnet ✅
color: yellow ✅
tools: [...] ✅ (YAML list)
disallowedTools: [...] ✅
```

**Score**: 95/100

**Strengths:**
- ✅ Explicit model preference
- ✅ Color for visual identification
- ✅ YAML-style tool lists
- ✅ disallowedTools configured
- ✅ Comprehensive description with examples

**Recommendations:**
- Consider adding `hooks:` for pre-execution validation

### performance-optimizer

**Frontmatter:**
```yaml
name: performance-optimizer ✅
description: "Speed and efficiency..." ✅
model: ❌ Not specified
color: ❌ Not specified
tools: [...] ⚠️ (comma-separated)
disallowedTools: ❌ Not specified
```

**Score**: 65/100

**Issues:**
- ⚠️ No explicit model specification
- ⚠️ No color defined
- ⚠️ Uses comma-separated tools instead of YAML list
- ⚠️ No disallowedTools - may access unnecessary tools

**Recommendations:**
1. Add `model: opus` for quality optimization analysis
2. Add `color: green` or similar for identification
3. Convert tools to YAML-style list
4. Add `disallowedTools:` to block MCP and web tools

## Skill Analysis

### tdd-typescript

**Frontmatter:**
```yaml
name: grey-haven-tdd-typescript ✅
description: "TypeScript TDD..." ✅
skills: ✅ (2 skills)
allowed-tools: ✅ (YAML list, 7 tools)
```

**Score**: 90/100

**Strengths:**
- ✅ skills auto-load configured
- ✅ allowed-tools with YAML list
- ✅ Comprehensive supporting materials

**Recommendations:**
- Consider adding `context: fork` for isolated execution
- Consider adding skill-scoped `hooks:`

### code-quality-analysis

**Frontmatter:**
```yaml
name: grey-haven-code-quality ✅
description: "..." ✅
skills: ❌ Not configured
allowed-tools: ⚠️ (comma-separated)
```

**Score**: 70/100

**Issues:**
- ⚠️ No skills auto-load for subagents
- ⚠️ Uses comma-separated allowed-tools

**Recommendations:**
1. Add `skills:` field for related skills
2. Convert allowed-tools to YAML list

## Command Analysis

### /tdd-implement

**Frontmatter:**
```yaml
description: ✅ Present
allowed-tools: ✅ Present
argument-hint: ✅ Present
```

**Score**: 85/100

**Recommendations:**
- Consider adding `context: fork` for isolation
- Consider adding command-scoped `hooks:`

## Deprecation Warnings

✅ No deprecated patterns found.

## Feature Recommendations

### High Priority
- [ ] Convert all comma-separated tool lists to YAML format
- [ ] Add `model:` to agents without explicit model
- [ ] Add `disallowedTools:` to agents to block unnecessary tools

### Medium Priority
- [ ] Add `color:` to agents for visual identification
- [ ] Add `skills:` auto-load to skills
- [ ] Consider `context: fork` for isolated command execution
- [ ] Consider agent/skill-scoped `hooks:` for validation

### Low Priority
- [ ] Add `once: true` to appropriate hooks
- [ ] Add LSP tool integration where beneficial

## Action Items

1. **Update performance-optimizer agent**:
   - Add `model: opus`
   - Add `color: green`
   - Convert tools to YAML list
   - Add disallowedTools

2. **Update code-quality-analysis skill**:
   - Add `skills:` field
   - Convert allowed-tools to YAML list

3. **Consider v2.1.0 features**:
   - Add hook support to critical agents
   - Use `context: fork` for isolated execution

## Score Breakdown

| Category | Score | Max | Notes |
|----------|-------|-----|-------|
| Structure | 20 | 20 | Perfect structure |
| Frontmatter | 20 | 25 | Some agents missing fields |
| No Deprecations | 15 | 15 | Clean |
| Feature Adoption | 15 | 20 | Missing some v2.1.0 features |
| Documentation | 8 | 10 | Good but could add README |
| Security | 4 | 10 | Some agents lack tool restrictions |
| **Total** | **82** | **100** | |
```

## Before/After Example

### Before (Old Style)

```yaml
---
name: my-agent
description: Does something useful
tools: Read, Write, Bash, Grep
---
```

### After (v2.1.0 Best Practices)

```yaml
---
name: my-agent
description: "Expert agent that [capability]. Use when [scenarios]. Triggers: '[keywords]'. <example>Context: [context] user: \"[message]\" assistant: \"[response]\" <commentary>[reasoning]</commentary></example>"
model: opus
color: cyan
tools:
  - Read
  - Write
  - Bash
  - Grep
  - TodoWrite
disallowedTools:
  - WebFetch
  - WebSearch
  - mcp__*
hooks:
  PreToolUse:
    - command: "validate-input.sh"
      once: true
---
```

**Improvements:**
1. Rich description with examples
2. Explicit model selection
3. Visual color identification
4. YAML-style tool lists
5. Dangerous tools blocked
6. Hook for validation
