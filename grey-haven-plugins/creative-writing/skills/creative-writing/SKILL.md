---
name: grey-haven-creative-writing
description: "Professional writing assistance for blogs, research articles, fiction, essays, and marketing copy. Use when users want to write, edit, or improve any form of written content. Triggers: 'write a blog', 'write an article', 'help me write', 'write a story', 'write a chapter', 'draft an essay', 'creative writing', 'improve my writing', 'edit my writing', 'write copy', 'content writing'."
skills:
  - grey-haven-prompt-engineering
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Grep
  - Glob
  - TodoWrite
  - WebSearch
  - WebFetch
---

# Creative Writing

Professional writing assistance across genres: blogs, research, fiction, essays, and marketing copy.

## Writing Philosophy

Great writing follows universal principles regardless of genre:

1. **Clarity** - Every sentence serves a purpose
2. **Voice** - Consistent tone appropriate to audience
3. **Structure** - Logical flow that guides readers
4. **Engagement** - Hooks, tension, and payoff
5. **Polish** - Refined through editing

## Genre Selection

Choose your writing type to load genre-specific guidance:

| Genre | Reference | Best For |
|-------|-----------|----------|
| Blog posts | `references/blog-writing.md` | SEO content, thought leadership, tutorials |
| Research articles | `references/research-writing.md` | Academic papers, whitepapers, reports |
| Fiction | `references/fiction-writing.md` | Novels, short stories, creative narratives |
| Essays | `references/essay-writing.md` | Arguments, analysis, personal reflection |
| Marketing copy | `references/marketing-writing.md` | Landing pages, emails, ads |

## Universal Writing Process

### Phase 1: Understand

Before writing, clarify:

1. **Audience** - Who reads this? What do they know?
2. **Purpose** - Inform, persuade, entertain, or inspire?
3. **Constraints** - Word count, tone, format requirements?
4. **Success criteria** - What makes this piece successful?

### Phase 2: Structure

Create an outline before drafting:

```
1. Hook/Opening - Grab attention
2. Context - Set the stage
3. Main content - Deliver value
   - Point A with support
   - Point B with support
   - Point C with support
4. Conclusion - Synthesize and call to action
```

### Phase 3: Draft

Write freely without self-editing:

- **First draft is discovery** - Find what you're really saying
- **Momentum over perfection** - Keep moving forward
- **Mark uncertainties** - Use [TODO] or [CHECK] placeholders
- **Write the easy parts first** - Build confidence

### Phase 4: Revise

Systematic revision passes:

1. **Structure pass** - Does the logic flow?
2. **Clarity pass** - Is each sentence clear?
3. **Voice pass** - Is the tone consistent?
4. **Trim pass** - Cut unnecessary words
5. **Polish pass** - Refine word choices

### Phase 5: Finalize

Pre-publish checklist in `checklists/pre-publish-checklist.md`.

## Templates

Ready-to-use structures:

| Template | Use Case |
|----------|----------|
| `templates/blog-post.md` | Standard blog structure |
| `templates/research-article.md` | Academic/professional paper |
| `templates/fiction-chapter.md` | Novel chapter structure |
| `templates/essay.md` | Argumentative essay |
| `templates/landing-page.md` | Marketing landing page |

## Writing Techniques

### Hook Patterns

**Question hook**: "Have you ever wondered why...?"
**Statistic hook**: "73% of developers struggle with..."
**Story hook**: "Last Tuesday, everything changed when..."
**Contrarian hook**: "Everything you know about X is wrong."
**Promise hook**: "By the end of this article, you'll be able to..."

### Transition Patterns

**Additive**: Furthermore, Additionally, Moreover
**Contrasting**: However, On the other hand, Nevertheless
**Causal**: Therefore, As a result, Consequently
**Sequential**: First, Next, Finally
**Exemplifying**: For example, Specifically, Consider

### Ending Patterns

**Summary**: Recap key points
**Call to action**: Direct next step
**Question**: Provoke continued thought
**Vision**: Paint future picture
**Circle back**: Return to opening

## Readability Guidelines

| Audience | Reading Level | Sentence Length |
|----------|---------------|-----------------|
| General public | 8th grade | 15-20 words |
| Professional | 10th grade | 20-25 words |
| Academic | 12th+ grade | 25-30 words |
| Technical | Varies | Match documentation style |

### Readability Techniques

- **Short paragraphs** - 3-4 sentences max
- **Active voice** - "The team built" not "It was built by"
- **Concrete nouns** - "hammer" not "implement"
- **Strong verbs** - "sprint" not "move quickly"
- **No jargon** - Unless audience expects it

## Checklists

Quality assurance tools:

| Checklist                              | Purpose                        |
|----------------------------------------|--------------------------------|
| `checklists/pre-publish-checklist.md`  | Final review before publishing |
| `checklists/revision-checklist.md`     | Systematic revision passes     |
| `checklists/prose-revision-checkpoint.md` | Inter-phase quality gate for revision pipeline |
| `checklists/novel-development-checkpoint.md` | Inter-phase quality gate for novel development pipeline |
| `checklists/manuscript-audit-checkpoint.md` | Audit completion gate for manuscript audit pipeline |
| `checklists/content-production-checkpoint.md` | Inter-phase quality gate for content production pipeline |
| `checklists/review-synthesis-checkpoint.md` | Synthesis gate for review synthesis pipeline |

## Prose Revision Pipeline

A 6-phase systematic revision pipeline for manuscripts, using SVQ scoring as the quality metric. Designed for multi-book series but works on single manuscripts.

### Reference Documents

| Reference | Path | Purpose |
|-----------|------|---------|
| Master SOP | `references/prose-revision/prose-revision-sop.md` | Framework overview, operational rules, config template |
| Phase 1 | `references/prose-revision/phase-1-surface-cleanup.md` | Verbal tics, closing spirals, voice differentiation |
| Phase 2 | `references/prose-revision/phase-2-prose-craft.md` | Perception verbs, over-explanation, sentence variety |
| Phase 3 | `references/prose-revision/phase-3-svq-polish.md` | Targeted over-explanation, counterpoint injection |
| Phase 4 | `references/prose-revision/phase-4-sentence-architecture.md` | Em-dash density, sentence shapes, character metaphors |
| Phase 5 | `references/prose-revision/phase-5-enrichment.md` | Sensory anchoring, body moments, dialogue beats |
| Phase 6 | `references/prose-revision/phase-6-final-audit.md` | SVQ scoring, consistency verification, final report |

### Commands

| Command | Purpose |
|---------|---------|
| `/prose-revision` | Run the full 6-phase pipeline with quality gates |
| `/revision-phase` | Run a single phase for targeted reruns or recovery |

### Pipeline Flow

```
Phase 1 (cuts) -> Phase 2 (cuts) -> Phase 3 (cuts) -> Phase 4 (refine) -> Phase 5 (adds) -> Phase 6 (audit)
     |                  |                 |                  |                  |                  |
  checkpoint         checkpoint        checkpoint       checkpoint        checkpoint        checkpoint
                    + SVQ score                         + SVQ score                         + SVQ score
```

## Novel Development Pipeline

A 5-phase pre-production pipeline for novels, using NRS scoring (Narrative Readiness Score) as the quality metric. Produces a Novel Foundation Package ready for drafting.

### Reference Documents

| Reference | Path | Purpose |
|-----------|------|---------|
| Master SOP | `references/novel-development/novel-development-sop.md` | NRS framework, operational rules, config template |
| Phase 1 | `references/novel-development/phase-1-research.md` | Genre conventions, setting research, thematic context |
| Phase 2 | `references/novel-development/phase-2-foundation.md` | Character profiles, world bible, beat sheet (3 agents parallel) |
| Phase 3 | `references/novel-development/phase-3-structure.md` | Chapter-by-chapter outline with scene breakdowns |
| Phase 4 | `references/novel-development/phase-4-dialogue.md` | Voice guides, sample dialogue, scene dialogue notes |
| Phase 5 | `references/novel-development/phase-5-integration.md` | Consistency check, NRS scoring, Novel Foundation Package |

### Commands

| Command | Purpose |
|---------|---------|
| `/writing-team` | Run the full 5-phase novel development pipeline |
| `/novel-phase` | Run a single phase for targeted reruns or recovery |

### Pipeline Flow

```
Phase 1 (research) -> Phase 2 (foundation: 3 agents parallel) -> Phase 3 (structure) -> Phase 4 (dialogue) -> Phase 5 (integration)
       |                         |                                       |                      |                      |
    checkpoint              checkpoint                               checkpoint            checkpoint            checkpoint
                           + NRS score                                                                         + NRS score
```

## Manuscript Audit Pipeline

A parallel-dispatch audit pipeline for manuscripts, using SVQ, Believability, and World Consistency scores with acceptance thresholds.

### Reference Documents

| Reference | Path | Purpose |
|-----------|------|---------|
| Master SOP | `references/manuscript-audit/manuscript-audit-sop.md` | Acceptance thresholds, synthesis protocol, config template |
| Believability | `references/manuscript-audit/audit-believability.md` | Verisimilitude, consistency, plausibility (0-100 score) |
| Prose Quality | `references/manuscript-audit/audit-prose-quality.md` | SVQ scoring in audit mode (1-10 per dimension) |
| World Consistency | `references/manuscript-audit/audit-world-consistency.md` | Rule verification, timeline, system coherence |

### Acceptance Thresholds

| Decision | SVQ Composite | Believability | World Issues |
|----------|:------------:|:-------------:|:------------:|
| **ACCEPT** | >= 7.0 | >= 80/100 | No critical issues |
| **REVISE** | 5.0 - 6.9 | 60 - 79 | Major issues |
| **REWORK** | < 5.0 | < 60 | Critical issues |

### Command

| Command | Purpose |
|---------|---------|
| `/writing-audit` | Run the parallel 3-agent manuscript audit with synthesis |

## Content Production Pipeline

A 4-phase sequential pipeline for non-fiction content, using CRS scoring (Content Readiness Score) as the quality metric. Produces a Content Production Package ready for writing.

### Reference Documents

| Reference | Path | Purpose |
|-----------|------|---------|
| Master SOP | `references/content-production/content-production-sop.md` | CRS framework, operational rules, config template |
| Phase 1 | `references/content-production/phase-1-strategy.md` | Audience analysis, keyword research, content calendar |
| Phase 2 | `references/content-production/phase-2-research.md` | Factual research per content piece |
| Phase 3 | `references/content-production/phase-3-outline.md` | Production-ready outlines mapped to keywords |
| Phase 4 | `references/content-production/phase-4-production-readiness.md` | Lead synthesis, CRS scoring, Content Production Package |

### Command

| Command | Purpose |
|---------|---------|
| `/content-team` | Run the full 4-phase content production pipeline |

### Pipeline Flow

```
Phase 1 (strategy) -> Phase 2 (research) -> Phase 3 (outline) -> Phase 4 (readiness)
       |                     |                     |                     |
    checkpoint           checkpoint            checkpoint           checkpoint
   + CRS score                                                     + CRS score
```

## Review Synthesis Pipeline

A parallel-dispatch review pipeline with structured synthesis protocol for resolving reviewer disagreements.

### Reference Documents

| Reference | Path | Purpose |
|-----------|------|---------|
| Master SOP | `references/review-synthesis/review-synthesis-sop.md` | Synthesis protocol, review focus mapping, config template |
| Editorial | `references/review-synthesis/review-editorial.md` | Developmental feedback, line editing, copy editing |
| Prose Quality | `references/review-synthesis/review-prose-quality.md` | SVQ scoring, style analysis, voice profiling |
| Dialogue | `references/review-synthesis/review-dialogue.md` | Voice differentiation, subtext, authenticity |

### Synthesis Protocol

| Agreement Level | Rule | Action |
|----------------|------|--------|
| All 3 agree | High confidence | Highest priority in revision list |
| 2 of 3 agree | Majority | Include with dissenting note |
| All 3 disagree | Author decides | Present all perspectives |
| Severity conflict | Highest wins | If one says critical, it is critical |

### Command

| Command | Purpose |
|---------|---------|
| `/writing-review` | Run the parallel 3-agent review with synthesis |

## Use This Skill When

- Writing any form of content from scratch
- Improving existing drafts
- Learning writing techniques
- Structuring complex pieces
- Overcoming writer's block
- Editing for clarity and impact
- Running systematic manuscript revision pipelines
- Developing novel foundations with structured pre-production
- Auditing manuscripts for quality and consistency
- Producing content with strategy-first workflows
- Synthesizing multi-reviewer feedback into actionable revision lists

## Related Skills

- `prompt-engineering` - Crafting effective prompts
- `documentation-alignment` - Technical documentation

---

**Skill Version**: 1.2
**Genres Covered**: Blog, Research, Fiction, Essay, Marketing
**Pipelines**: Prose Revision, Novel Development, Manuscript Audit, Content Production, Review Synthesis
**Last Updated**: 2026-02-06
