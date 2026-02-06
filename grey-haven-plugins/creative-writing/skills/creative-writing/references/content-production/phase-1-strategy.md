# Phase 1: Strategy

| Field | Value |
|-------|-------|
| **Phase** | 1 of 4 |
| **Name** | Strategy |
| **Agent** | content-strategist (`creative-writing:writing-content-strategist`) |
| **CRS Scoring** | Yes (first checkpoint) |

---

## Objectives

Phase 1 establishes the strategic foundation for all content that follows. Without a validated strategy, research wanders and outlines lack purpose. This phase produces the documents that every subsequent phase depends on.

### 1. Audience Analysis

Define who the content serves. For each target persona:

- Role and responsibilities
- Primary pain points the content addresses
- Content consumption habits (format, length, channel preferences)
- Decision-making triggers (what moves them to act)
- Knowledge level (beginner, intermediate, expert)

Personas must be specific enough to guide keyword selection and outline structure. "Marketing professionals" is too broad. "B2B SaaS marketing managers evaluating content tools" is actionable.

### 2. Keyword Research

Build a keyword map that connects business goals to search intent:

- Primary keywords (high-priority targets for each content piece)
- Secondary keywords (supporting terms and long-tail variations)
- Keyword clusters (groups of related terms that a single piece can target)
- Search intent classification (informational, navigational, transactional, commercial)
- Difficulty and volume assessment (prioritize winnable terms)

Every content piece in the production plan must have at least one primary keyword assigned.

### 3. Competitive Landscape

Analyze the competitive URLs from the project config:

- What topics competitors cover (and what gaps exist)
- Content format and depth (word count, structure, media usage)
- Strengths to match and weaknesses to exploit
- SERP features present (featured snippets, people also ask, video carousels)

The goal is not to copy competitors but to identify where the content can provide superior value.

### 4. Content Calendar Planning

Map content pieces to a publishing timeline:

- Content titles and types (blog post, guide, landing page)
- Target keywords per piece
- Publishing cadence aligned with project config schedule
- Dependencies between pieces (pillar content before cluster content)
- Seasonal or event-driven timing considerations

---

## Agent Prompt Template

Use the following prompt when dispatching the content-strategist agent for Phase 1. Replace placeholder values with project-specific content.

```markdown
# Phase 1: Strategy

You are performing Phase 1 of the content production pipeline. Your scope is strictly limited to strategic analysis and planning. Do not research facts, build outlines, or write content -- those are later phases.

## Inputs

- **Project brief**: {{PROJECT_BRIEF}}
- **Project config**: {{CONFIG_PATH}}
- **Business goals**: {{BUSINESS_GOALS}}
- **Target audience**: {{TARGET_AUDIENCE}}

Read the project config first. It contains business goals, target audience personas, primary keywords, content types, publishing schedule, brand voice guidelines, and competitive URLs.

## Instructions

1. **Audience analysis**: Define detailed personas based on the target audience in the config. For each persona, document their role, pain points, content preferences, and decision triggers. If the config personas are vague, sharpen them.

2. **Keyword research**: Expand the primary keywords from the config into a full keyword map. For each keyword cluster, classify search intent and assess difficulty. Assign primary keywords to planned content pieces.

3. **Competitive analysis**: Analyze the competitive URLs from the config. Identify content gaps, format patterns, and opportunities for differentiation. Document what competitors do well and where they fall short.

4. **Content calendar**: Produce a publishing timeline that maps content pieces to keywords, personas, and dates. Respect the publishing schedule from the config. Note dependencies between pillar and cluster content.

## Rules

- **Strategy only. No content creation.** You may define what to write, for whom, and why. You may not write the actual content, research facts, or build outlines.
- **Ground everything in data.** Personas should reflect real audience signals. Keywords should have volume and intent context. Competitive analysis should reference specific URLs.
- **Be specific.** "Write blog posts about AI" is not a strategy. "Write a 2,000-word comparison guide targeting 'best AI writing tools' (informational intent, medium difficulty) for B2B marketing managers evaluating content automation" is a strategy.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

After completing the strategy phase, provide:

- Audience personas (detailed)
- Keyword map with clusters, intent, and assignments
- Competitive analysis summary
- Content calendar with titles, types, keywords, and dates
- Initial CRS assessment (Alignment score 1-10 with justification)
```

---

## Phase Checklist

Verify all items before marking Phase 1 complete:

- [ ] Audience personas defined with actionable specificity
- [ ] Keyword map complete with clusters, intent classifications, and difficulty assessments
- [ ] Every planned content piece has at least one primary keyword assigned
- [ ] Competitive landscape analyzed with gap identification
- [ ] Content calendar produced with titles, types, keywords, and target dates
- [ ] Strategy aligns with business goals from the project config
- [ ] CRS Alignment score recorded with justification
- [ ] No research, outlining, or content creation was performed
- [ ] Git commit created: `content: phase 1 strategy complete - <project>`

---

## Common Pitfalls

**Skipping persona specificity.** Generic personas produce generic content. "Small business owners" encompasses millions of people with wildly different needs. Force the strategist to narrow until the persona is someone you could write a letter to.

**Keyword vanity.** High-volume keywords are seductive but often unwinnable for new content programs. Prioritize keywords where the content can realistically rank -- lower difficulty terms with clear intent often outperform aspirational head terms.

**Competitive analysis as copying.** The goal is to understand the landscape, not replicate it. If every competitor writes 1,500-word listicles, the opportunity may be a 3,000-word definitive guide -- or a 500-word focused answer. Differentiation is strategy.

**Calendar without dependencies.** Publishing a cluster article before its pillar page exists wastes link equity and confuses site architecture. Map dependencies before dates.

**Strategy without constraints.** An unlimited content calendar is not a strategy -- it is a wish list. The publishing schedule in the config exists for a reason. Respect production capacity and publishing cadence.

---

*A strategy that cannot be explained in one sentence is not a strategy. It is a list of activities.*
