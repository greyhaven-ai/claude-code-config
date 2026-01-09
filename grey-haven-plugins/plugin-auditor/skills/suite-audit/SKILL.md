---
name: grey-haven-suite-audit
description: "Meta-level plugin suite auditor that uses subagents to analyze any plugin for usability improvements, missing agents, duplication, and workflow optimizations. Generates comprehensive reports with user-approved todo conversion. Triggers: 'audit suite', 'analyze plugin usability', 'find duplicate agents', 'suggest new agents', 'optimize plugin workflow', 'plugin gap analysis'."
skills:
  - grey-haven-plugin-audit
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - TodoWrite
  - AskUserQuestion
---

# Plugin Suite Auditor

Meta-level audit skill that analyzes any plugin suite using specialized subagents to identify usability improvements, coverage gaps, duplication, and workflow optimizations.

## Purpose

Systematically evaluate a plugin ecosystem to:
- Identify usability improvements for existing agents/skills
- Recommend new agents that fill workflow gaps
- Find duplication across agents that can be consolidated
- Suggest workflow optimizations and integration points
- Generate actionable improvement roadmaps

## Audit Methodology

This skill orchestrates **four specialized analysis passes** using subagents, then synthesizes findings into a prioritized report.

---

## Phase 1: Usability Analysis

**Goal**: Evaluate each agent/skill for user experience quality.

### Usability Criteria

| Criterion | Question | Weight |
|-----------|----------|--------|
| Discoverability | Can users find the right agent easily? | 20% |
| Clarity | Are instructions clear and unambiguous? | 20% |
| Completeness | Does the agent deliver on its promise? | 20% |
| Flexibility | Can it handle edge cases and variations? | 15% |
| Integration | Does it work well with other agents? | 15% |
| Output Quality | Are outputs immediately usable? | 10% |

### Usability Red Flags

- Vague or missing description triggers
- No example requests provided
- Missing collaboration/integration guidance
- Incomplete output format definitions
- No behavioral traits defined
- Unclear scope boundaries

### Subagent Analysis Prompt

```
Analyze [agent-name] for usability issues:

1. Read the agent definition thoroughly
2. Evaluate against these criteria:
   - Discoverability: Clear description with good trigger words?
   - Clarity: Unambiguous instructions?
   - Completeness: Covers expected use cases?
   - Flexibility: Handles variations?
   - Integration: Connects to other agents?
   - Output Quality: Well-defined formats?
3. Score each criterion 1-5
4. Identify specific improvement opportunities
5. Suggest concrete fixes

Output format:
## Usability Analysis: [Agent Name]
**Overall Score**: X/30
**Critical Issues**: [list]
**Improvements**: [list with specific recommendations]
```

---

## Phase 2: Gap Analysis

**Goal**: Identify missing agents that would strengthen the suite.

### Coverage Analysis Process

1. Identify the plugin's domain (e.g., creative writing, testing, deployment)
2. Map the complete workflow for that domain
3. Check which stages have agent coverage
4. Identify stages without dedicated support
5. Evaluate gap significance

### Gap Identification Criteria

A gap is worth filling if:
1. **Frequency**: Users commonly need this capability
2. **Complexity**: Task is complex enough to benefit from specialization
3. **Distinctness**: Not adequately covered by existing agents
4. **Integration**: Would enhance existing agent workflows

### Subagent Analysis Prompt

```
Analyze [plugin-name] for coverage gaps:

1. Determine the plugin's domain and purpose
2. Map the complete workflow for this domain
3. Identify which workflow stages have agent coverage
4. Find stages without dedicated support
5. Evaluate gap significance:
   - How often do users need this?
   - Is it complex enough for an agent?
   - Could existing agents cover it with modifications?
6. Recommend new agents with specifications

Output format:
## Gap Analysis: [Plugin Name]
**Domain**: [what this plugin covers]
**Coverage Score**: X% of workflow covered
**Workflow Map**: [stages with coverage indicators]
**Critical Gaps**: [list with justification]
**Recommended New Agents**: [name, purpose, why needed]
```

---

## Phase 3: Duplication Analysis

**Goal**: Find overlapping functionality that can be consolidated.

### Duplication Types

| Type | Description | Action |
|------|-------------|--------|
| **Full Overlap** | Two agents do same thing | Merge or deprecate one |
| **Partial Overlap** | Significant shared functionality | Extract common patterns |
| **Conceptual Overlap** | Similar approaches in different contexts | Document boundaries |
| **Output Overlap** | Produce similar artifacts | Standardize formats |

### Detection Patterns

Scan for:
- Similar section headings across agents
- Duplicate checklists or frameworks
- Overlapping example requests
- Redundant output templates
- Repeated behavioral traits
- Shared workflows

### Subagent Analysis Prompt

```
Analyze [plugin-name] for duplication:

1. Read all agent definitions in the plugin
2. Create a feature matrix showing what each agent provides
3. Identify overlapping functionality:
   - Exact duplicates
   - Similar but not identical features
   - Overlapping scopes
4. Recommend consolidation strategies:
   - Merge agents
   - Extract shared components
   - Clarify boundaries
5. Estimate effort to consolidate

Output format:
## Duplication Analysis: [Plugin Name]
**Redundancy Level**: [Low/Medium/High]
**Full Overlaps**: [specific examples with quotes]
**Partial Overlaps**: [specific examples]
**Consolidation Recommendations**: [actions with rationale]
```

---

## Phase 4: Workflow Optimization

**Goal**: Improve how agents work together.

### Integration Analysis

Evaluate:
- Are handoff points clearly defined?
- Do agents reference each other appropriately?
- Is there a natural workflow sequence?
- Can outputs of one agent feed directly into another?
- Are there workflow bottlenecks?

### Workflow Pattern Template

```
WORKFLOW CHAINS
===============

Chain Name:
agent-1 → agent-2 → agent-3

Evaluation:
- Handoffs clear: [Yes/No]
- Output compatibility: [Yes/No]
- Documentation: [Yes/No]
```

### Optimization Opportunities

- Missing chain links
- Unclear transition points
- Redundant intermediate steps
- Opportunity for parallel processing
- Automation potential

### Subagent Analysis Prompt

```
Analyze [plugin-name] agent workflow integration:

1. Map typical user journeys through the plugin
2. Identify how agents currently reference each other
3. Find workflow friction points:
   - Unclear handoffs
   - Missing integration
   - Redundant steps
4. Recommend optimizations:
   - New integration points
   - Workflow templates
   - Automation opportunities

Output format:
## Workflow Analysis: [Plugin Name]
**Integration Score**: X/10
**Workflow Chains Identified**: [list]
**Friction Points**: [specific issues]
**Optimization Recommendations**: [actions]
```

---

## Audit Execution Protocol

### Step 1: Load Plugin Context

```
1. Read plugin.json for metadata and component list
2. Glob all agents: [plugin-path]/agents/*.md
3. Glob all skills: [plugin-path]/skills/*/SKILL.md
4. Glob all commands: [plugin-path]/commands/*.md
5. Build inventory of all components
```

### Step 2: Launch Subagent Analyses

Launch four analysis passes using the Task tool:
1. **Usability Analyzer** - Reviews each agent for UX quality
2. **Gap Analyzer** - Maps workflow coverage
3. **Duplication Detector** - Finds redundancies
4. **Workflow Optimizer** - Evaluates integration

### Step 3: Synthesize Findings

Combine analyses into unified audit report:

```markdown
# Plugin Suite Audit Report: [Plugin Name]

**Date**: [Date]
**Version Audited**: [version from plugin.json]
**Components Analyzed**: X agents, Y skills, Z commands

## Executive Summary

**Overall Health Score**: X/100

| Category | Score | Issues |
|----------|-------|--------|
| Usability | X/25 | X critical, X major |
| Coverage | X/25 | X gaps identified |
| Duplication | X/25 | X redundancies found |
| Workflow | X/25 | X friction points |

**Key Findings**:
1. [Most critical finding]
2. [Second finding]
3. [Third finding]

---

## Detailed Findings

### Usability Issues
[From Phase 1]

### Coverage Gaps
[From Phase 2]

### Duplication Concerns
[From Phase 3]

### Workflow Friction
[From Phase 4]

---

## Prioritized Recommendations

### Critical (Do First)
| # | Recommendation | Category | Effort | Impact |
|---|----------------|----------|--------|--------|
| 1 | [Action] | [Category] | [Low/Med/High] | [High] |

### Important (Do Soon)
[Table continues]

### Nice to Have (Consider)
[Table continues]

---

## Suggested New Agents

| Agent Name | Purpose | Gap Filled | Priority |
|------------|---------|------------|----------|
| [name] | [what it does] | [workflow gap] | [High/Med/Low] |

---

## Consolidation Targets

| Source A | Source B | Overlap | Recommendation |
|----------|----------|---------|----------------|
| [agent] | [agent] | [what overlaps] | [merge/extract/clarify] |
```

### Step 4: Convert to Todos (User-Approved)

After presenting the report, use AskUserQuestion:

```
Which findings should I convert to actionable todos?

Options:
1. All recommendations (Critical + Important + Nice to Have)
2. Critical and Important only
3. Critical only
4. Let me select specific items
5. Report only, no todos
```

Upon approval, create todos with:
- Clear action description
- Category tag: `[Usability]`, `[Gap]`, `[Duplication]`, `[Workflow]`
- Priority indicator
- Estimated effort

---

## Example Audit Scenarios

### Full Suite Audit

```
User: "Audit the creative-writing plugin suite"

Action:
1. Load creative-writing plugin context
2. Run all four analysis phases
3. Generate comprehensive report
4. Offer todo conversion
```

### Targeted Usability Review

```
User: "Check usability of testing plugin agents"

Action:
1. Load testing plugin context
2. Run usability analysis only
3. Generate focused report
```

### Gap Analysis Only

```
User: "What agents should we add to the observability plugin?"

Action:
1. Load observability plugin context
2. Run gap analysis only
3. Generate agent recommendations with specs
```

### Duplication Check

```
User: "Find duplicate functionality in the knowledge-base plugin"

Action:
1. Load knowledge-base plugin context
2. Run duplication analysis only
3. Generate consolidation recommendations
```

---

## Integration with Plugin Audit

This skill complements the `grey-haven-plugin-audit` skill:

| Skill | Focus | Level |
|-------|-------|-------|
| `plugin-audit` | Structure, frontmatter, deprecations | Technical validation |
| `suite-audit` | Usability, gaps, duplication, workflow | Strategic improvement |

**Recommended workflow**:
1. Run `plugin-audit` first for technical health
2. Run `suite-audit` for strategic improvements
3. Combine findings into comprehensive roadmap

---

## Quality Standards

- Base recommendations on evidence from agent files
- Provide specific quotes and file locations
- Distinguish opinion from fact
- Acknowledge when existing design is intentional
- Prioritize actionable over theoretical improvements
- Consider maintenance burden of recommendations
- Respect existing architecture patterns
- Be domain-aware (different plugins have different needs)

---

**Skill Version**: 1.0
**Last Updated**: 2025-01-08
