# Phase 3: Outline

| Field | Value |
|-------|-------|
| **Phase** | 3 of 4 |
| **Name** | Outline |
| **Agent** | outline-architect (`creative-writing:writing-outline-architect`) |
| **CRS Scoring** | No |

---

## Objectives

Phase 3 transforms strategy and research into production-ready outlines. An outline is not a rough sketch -- it is a blueprint detailed enough that a writer can produce the final content without guesswork about structure, flow, or keyword placement.

### 1. Production-Ready Outlines

For each content piece, build a hierarchical outline that includes:

- Title and subtitle (incorporating primary keyword naturally)
- H2 and H3 section headings (reflecting logical argument flow)
- Bullet points under each section describing what that section covers
- Key points to make in each section (drawn from research briefs)
- Statistics and sources to cite in each section (mapped from Phase 2)

The outline should be detailed enough that two different writers given the same outline would produce structurally similar content.

### 2. Keyword Mapping

Every outline must demonstrate clear keyword integration:

- Primary keyword placement (title, H2s, introduction, conclusion)
- Secondary keywords distributed across relevant sections
- Keyword cluster coverage verified against the strategy map
- Search intent alignment (does the outline structure match what the searcher expects?)

Keyword placement should feel natural within the outline structure. Forced keyword insertion produces content that reads as optimized rather than authoritative.

### 3. Word Count Allocation

Distribute the target word count across sections:

- Introduction (typically 5-10% of total)
- Core sections (proportional to importance and research depth)
- Conclusion / CTA (typically 5-10% of total)
- Total allocation should match the target word count from the strategy

Word count allocation prevents the common problem of front-loaded content that rushes through later sections.

### 4. Argument Flow Verification

Ensure the outline tells a coherent story:

- Each section builds on the previous one
- The reader's journey progresses logically (problem -> context -> solution -> action)
- No section duplicates another's purpose
- Transitions between sections are implied by the structure
- The conclusion delivers on the promise made in the introduction

---

## Agent Prompt Template

Use the following prompt when dispatching the outline-architect agent for Phase 3. Replace placeholder values with project-specific content.

```markdown
# Phase 3: Outline

You are performing Phase 3 of the content production pipeline. Your scope is strictly limited to building production-ready outlines. Do not write prose, conduct new research, or modify the strategy -- those are other phases.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Strategy output**: {{STRATEGY_OUTPUT}}
- **Research output**: {{RESEARCH_OUTPUT}}
- **Content types**: {{CONTENT_TYPES}}

Read both the strategy and research outputs. The strategy defines what to write, for whom, and why. The research provides the factual foundation. Your outlines must honour both.

## Instructions

For each content piece in the strategy:

1. **Build hierarchical outline**: Create a detailed outline with title, H2/H3 headings, bullet points per section, key points, and source references. The outline must be detailed enough for a writer to produce the content without structural decisions.

2. **Map keywords**: Place the primary keyword in the title and key H2 headings. Distribute secondary keywords across relevant sections. Verify that keyword cluster coverage matches the strategy map.

3. **Allocate word counts**: Distribute the target word count across sections proportionally. Introduction and conclusion get 5-10% each. Core sections share the remainder based on importance and research depth.

4. **Verify argument flow**: Ensure the outline progresses logically. Each section should build on the previous. The reader's journey should move from problem to context to solution to action.

## Rules

- **Outlines only. No prose.** You may structure, organize, and annotate. You may not write paragraphs, craft sentences, or produce draft content.
- **Honour the strategy.** Every outline section must trace back to a keyword, persona need, or business goal from Phase 1. Sections that serve no strategic purpose need justification.
- **Incorporate research.** Map specific facts, statistics, and sources from Phase 2 to the outline sections where they belong. An outline without research references is a guess.
- **Be specific.** "Discuss benefits" is not an outline point. "List 5 measurable benefits with supporting statistics from [source], emphasizing ROI for [persona]" is an outline point.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

For each content piece, produce:

- Complete hierarchical outline (title, H2s, H3s, bullet points)
- Keyword placement map (which keywords appear where)
- Word count allocation table (section name, target words, percentage)
- Research integration notes (which sources/stats map to which sections)
- Argument flow summary (one sentence describing the reader's journey)
```

---

## Phase Checklist

Verify all items before marking Phase 3 complete:

- [ ] Production-ready outline created for every content piece
- [ ] Outlines include H2/H3 headings with descriptive bullet points
- [ ] Primary keyword placed in title and key headings
- [ ] Secondary keywords distributed across relevant sections
- [ ] Word count allocated across sections (totals match target)
- [ ] Research briefs integrated (statistics and sources mapped to sections)
- [ ] Argument flow verified (logical progression, no duplication)
- [ ] No prose, new research, or strategy modifications were produced
- [ ] Git commit created: `content: phase 3 outline complete - <project>`

---

## Common Pitfalls

**Outlines that are actually drafts.** An outline is a structure, not a first draft. If the bullet points read as prose paragraphs, the scope has been violated. Keep points as directives ("Explain X using Y data") not as draft sentences.

**Ignoring research briefs.** An outline built purely from the strategist's keyword map without incorporating Phase 2 research produces structures that sound strategic but lack substance. Every core section should reference specific research findings.

**Uniform section weighting.** Not every section deserves equal word count. A comparison section backed by extensive research data deserves more space than a brief contextual introduction. Allocate words based on substance, not symmetry.

**Keyword stuffing in headings.** Placing the primary keyword in every H2 produces headings that read as SEO artifacts rather than useful navigation. Distribute keywords across the outline naturally -- readers and search engines both prefer headings that describe content accurately.

**Missing the reader's journey.** An outline is not a list of topics. It is a path the reader walks. If the sections could be reordered without loss, the outline lacks narrative logic. Each section should build on what came before and set up what comes next.

**Outlines without word count allocation.** Without target word counts, writers inevitably front-load content -- investing heavily in early sections and rushing through later ones. Explicit allocation prevents this and keeps the final content balanced.

---

*A good outline makes the writing inevitable. The words have nowhere else to go.*
