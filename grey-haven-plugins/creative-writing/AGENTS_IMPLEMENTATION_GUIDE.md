# Creative Writing Agents Implementation Guide

Systematic implementation plan for creative-writing plugin agents.

## Current State

**Existing agents** (v1.1.0):
- [x] `research-gatherer` - Research and fact-finding
- [x] `character-developer` - Character profiles and psychology

## New Agents to Implement

### 1. story-architect
**File**: `agents/story-architect.md`

| Attribute | Value |
|-----------|-------|
| Name | `writing-story-architect` |
| Color | `orange` |
| Model | `sonnet` |
| Tools | `Read, Write, MultiEdit, Glob, Grep, TodoWrite` |

**Covers**:
- Three-act structure, five-act, hero's journey, save the cat
- Scene sequencing and chapter breaks
- Conflict escalation patterns
- Pacing (scene vs summary)
- Subplot weaving
- Tension/release cycles
- Story spine and premise

**Outputs**:
- Plot outlines
- Scene breakdowns
- Beat sheets
- Story structure analysis

---

### 2. editor-reviewer
**File**: `agents/editor-reviewer.md`

| Attribute | Value |
|-----------|-------|
| Name | `writing-editor-reviewer` |
| Color | `red` |
| Model | `sonnet` |
| Tools | `Read, Write, MultiEdit, Glob, Grep, TodoWrite` |

**Covers**:
- Line editing (clarity, concision, flow)
- Copy editing (grammar, punctuation, consistency)
- Developmental feedback (structure, pacing, character)
- Style consistency checks
- Voice maintenance
- Show vs tell analysis
- Redundancy elimination

**Outputs**:
- Annotated drafts
- Revision suggestions
- Style reports
- Consistency checklists

---

### 3. world-builder
**File**: `agents/world-builder.md`

| Attribute | Value |
|-----------|-------|
| Name | `writing-world-builder` |
| Color | `green` |
| Model | `sonnet` |
| Tools | `Read, Write, MultiEdit, Glob, Grep, TodoWrite` |

**Covers**:
- Physical geography and climate
- Political systems and history
- Economic systems and trade
- Magic/technology systems with rules
- Cultures, religions, customs
- Languages and naming conventions
- Flora, fauna, ecosystems
- Internal consistency tracking

**Outputs**:
- World bibles
- Setting documents
- System rules
- Consistency matrices

---

### 4. dialogue-coach
**File**: `agents/dialogue-coach.md`

| Attribute | Value |
|-----------|-------|
| Name | `writing-dialogue-coach` |
| Color | `cyan` |
| Model | `sonnet` |
| Tools | `Read, Write, MultiEdit, Glob, Grep, TodoWrite` |

**Covers**:
- Natural speech patterns
- Character voice differentiation
- Subtext and implication
- Dialect and accent representation
- Dialogue tags and action beats
- Exposition through conversation
- Conflict in dialogue
- Rhythm and pacing

**Outputs**:
- Dialogue rewrites
- Voice guides per character
- Dialogue analysis
- Speech pattern references

---

### 5. content-strategist
**File**: `agents/content-strategist.md`

| Attribute | Value |
|-----------|-------|
| Name | `writing-content-strategist` |
| Color | `yellow` |
| Model | `sonnet` |
| Tools | `Read, Write, Glob, Grep, WebSearch, WebFetch, TodoWrite` |
| MCP Tools | `firecrawl_search, exa_web_search` |

**Covers**:
- Content calendar planning
- SEO keyword research
- Audience persona development
- Competitive content analysis
- Topic clustering
- Content repurposing strategies
- Headline optimization
- Distribution planning

**Outputs**:
- Content calendars
- Keyword maps
- Audience personas
- Content audits

---

### 6. outline-architect
**File**: `agents/outline-architect.md`

| Attribute | Value |
|-----------|-------|
| Name | `writing-outline-architect` |
| Color | `indigo` |
| Model | `sonnet` |
| Tools | `Read, Write, MultiEdit, Glob, Grep, TodoWrite` |

**Covers**:
- Hierarchical outline structures
- Research organization
- Argument flow mapping
- Section dependencies
- Parallel structure
- Progressive disclosure
- Logical sequencing
- Gap identification

**Outputs**:
- Detailed outlines
- Structure maps
- Section summaries
- Dependency diagrams

---

## Implementation Checklist

### Per-Agent Tasks

For each agent:
- [x] Create `agents/{name}.md` with frontmatter and content
- [x] Follow established format from existing agents
- [x] Include: Purpose, Philosophy, Methodology, Output Formats, Behavioral Traits, Collaboration, Example Requests, Quality Standards

### Integration Tasks

After all agents created:
- [x] Update `plugin.json` with all 8 agents
- [x] Bump version to 1.2.0
- [x] Update plugin description
- [x] Add new keywords if needed
- [x] Update marketplace.json description and version

### Documentation Tasks

- [ ] Update SKILL.md to reference agents (optional)
- [x] Update gap analysis if applicable
- [x] Commit with descriptive message
- [x] Push to remote

---

## Agent Collaboration Matrix

| Agent | Works With | Purpose |
|-------|------------|---------|
| story-architect | character-developer | Character arcs drive plot |
| story-architect | outline-architect | Structure informs outline |
| editor-reviewer | dialogue-coach | Dialogue quality review |
| world-builder | research-gatherer | Historical/cultural accuracy |
| content-strategist | research-gatherer | Market research |
| outline-architect | story-architect | Fiction structure |
| outline-architect | content-strategist | Non-fiction planning |
| dialogue-coach | character-developer | Voice consistency |

---

## Implementation Order

Recommended sequence based on dependencies:

1. **story-architect** - Foundational for fiction, pairs with existing character-developer
2. **editor-reviewer** - Universal utility, closes feedback loop
3. **world-builder** - Extends research-gatherer for fiction settings
4. **dialogue-coach** - Connects character to story
5. **outline-architect** - Universal planning tool
6. **content-strategist** - Marketing/blog focus, uses web tools

---

## Version Plan

| Version | Agents | Status |
|---------|--------|--------|
| 1.0.0 | (skill only) | Released |
| 1.1.0 | +research-gatherer, +character-developer | Released |
| 1.2.0 | +story-architect, +editor-reviewer, +world-builder, +dialogue-coach, +outline-architect, +content-strategist | **Complete** |

---

*Guide created: 2025-12-26*
*Implementation completed: 2025-12-26*
