# Phase 2: Research

| Field | Value |
|-------|-------|
| **Phase** | 2 of 4 |
| **Name** | Research |
| **Agent** | research-gatherer (`creative-writing:writing-research-gatherer`) |
| **CRS Scoring** | No |

---

## Objectives

Phase 2 gathers the factual foundation for each content piece defined in the strategy. Research does not create content or build outlines -- it produces organized briefs that Phase 3 will structure into production-ready plans.

### 1. Factual Research Per Content Piece

For each content piece in the strategy:

- Core facts and data points that support the content angle
- Current state of the topic (what is known, what is debated, what is emerging)
- Historical context where relevant (how did we get here)
- Counter-arguments and alternative perspectives (strong content acknowledges complexity)

Research depth should match content type. A 500-word blog post needs key facts. A 3,000-word definitive guide needs comprehensive coverage.

### 2. Source Gathering

Build a source library for each content piece:

- Primary sources (original research, official reports, direct data)
- Secondary sources (expert analysis, reputable publications, industry reports)
- Quotable experts (names, titles, relevant quotes or positions)
- Source credibility assessment (recency, authority, methodology)

Every factual claim in the eventual content should be traceable to a source documented in Phase 2.

### 3. Statistics and Data Points

Collect quantitative evidence:

- Key statistics with source attribution and dates
- Trend data (year-over-year changes, growth rates, adoption curves)
- Benchmark data (industry averages, competitive metrics)
- Data visualisation opportunities (tables, charts, comparison data)

Prioritize recent data. A statistic from five years ago may be interesting but misleading if the landscape has changed.

### 4. Gap Identification

Flag areas where research reveals problems with the strategy:

- Topics where reliable sources are scarce (may need angle adjustment)
- Claims from the strategy that research does not support
- Emerging angles that the strategy did not anticipate
- Keyword targets where existing SERP content is unexpectedly strong or weak

Gaps are escalated to the lead. The researcher does not modify the strategy -- that authority belongs to Phase 1.

---

## Agent Prompt Template

Use the following prompt when dispatching the research-gatherer agent for Phase 2. Replace placeholder values with project-specific content.

```markdown
# Phase 2: Research

You are performing Phase 2 of the content production pipeline. Your scope is strictly limited to research and source gathering. Do not build outlines, write content, or modify the strategy -- those are other phases.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Strategy output**: {{STRATEGY_OUTPUT}}
- **Content topics**: {{CONTENT_TOPICS}}

Read the strategy output first. It contains audience personas, keyword assignments, competitive analysis, and the content calendar. Your research must serve the strategy, not diverge from it.

## Instructions

For each content piece in the strategy:

1. **Factual research**: Gather core facts, data points, and current knowledge relevant to the content angle. Match research depth to content type and target word count.

2. **Source gathering**: Build a source library with primary and secondary sources. Assess credibility (recency, authority, methodology). Identify quotable experts.

3. **Statistics collection**: Collect quantitative evidence -- key statistics, trend data, benchmarks. Include source attribution and dates for every data point.

4. **Gap identification**: Flag topics where sources are scarce, where research contradicts the strategy, or where unexpected opportunities emerge. Do not resolve gaps yourself -- document them for the lead.

## Rules

- **Research only. No content creation.** You may gather, organize, and annotate information. You may not write prose, build outlines, or modify the strategy.
- **Source everything.** Every fact, statistic, and claim must have a documented source. Unsourced claims are not research -- they are assumptions.
- **Prioritize recency.** Prefer data from the last 1-2 years unless historical context is specifically needed. Flag any source older than 3 years.
- **Respect the strategy.** Research serves the angles and keywords defined in Phase 1. If you discover a better angle, document it as a gap -- do not pivot the research independently.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

For each content piece, produce a research brief containing:

- Topic and target keyword (from strategy)
- Key facts and findings (organized by relevance)
- Source library (with credibility notes)
- Statistics and data points (with attribution)
- Research gaps or strategy conflicts (if any)
- Recommended research depth assessment (sufficient / needs more / oversaturated topic)
```

---

## Phase Checklist

Verify all items before marking Phase 2 complete:

- [ ] Research brief produced for every content piece in the strategy
- [ ] Every factual claim has a documented source
- [ ] Statistics include source attribution and dates
- [ ] Source credibility assessed (recency, authority, methodology)
- [ ] Research gaps and strategy conflicts documented and escalated
- [ ] Research depth matches content type (brief for short pieces, comprehensive for long-form)
- [ ] No outlines, prose, or strategy modifications were produced
- [ ] Git commit created: `content: phase 2 research complete - <project>`

---

## Common Pitfalls

**Research without boundaries.** A topic like "artificial intelligence in marketing" has infinite depth. The strategy defines the angle and the keyword defines the scope. Research that wanders beyond these boundaries wastes time and produces briefs too large to be useful.

**Quantity over quality.** Twenty weak sources do not outweigh three authoritative ones. Prioritize source quality. An industry report from a recognized authority carries more weight than a dozen blog posts citing each other.

**Ignoring contradictions.** When research contradicts the strategy, the temptation is to quietly focus on supporting evidence. This produces content built on cherry-picked data. Document contradictions honestly -- the lead needs to know.

**Stale data presented as current.** A statistic from 2019 presented without date context implies it is current. Always include the date of every data point. Let the outline architect and content writer decide whether older data is still relevant.

**Researching what to write instead of what supports writing.** Phase 2 gathers evidence. It does not decide structure, narrative arc, or argument flow. A research brief that reads like an outline has overstepped its scope.

---

*Good research does not tell you what to write. It tells you what is true, and leaves the writing to those who come next.*
