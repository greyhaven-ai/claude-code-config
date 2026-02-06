# Content Production SOP

Standard Operating Procedure for systematic content production using the 4-phase pipeline.

## CRS Scoring Framework

The pipeline uses **CRS scoring** (Content Readiness Score) as the primary quality metric for production readiness.

| Dimension | What It Measures | Scale |
|-----------|-----------------|-------|
| **A** (Alignment) | Strategic fit, audience targeting, keyword coverage | 1-10 |
| **R** (Research) | Source quality, depth, factual accuracy | 1-10 |
| **S** (Structure) | Outline completeness, logical flow, word count allocation | 1-10 |

**Composite CRS** = (A + R + S) / 3

| Composite | Interpretation |
|-----------|---------------|
| 9-10 | Production-ready, launch immediately |
| 7-8 | Strong foundation, minor gaps to address |
| 5-6 | Solid start, notable gaps in strategy, research, or structure |
| 3-4 | Significant development needed before production |
| 1-2 | Fundamental strategic work required |

CRS scoring is performed at checkpoints after Phase 1 (strategy baseline) and Phase 4 (final readiness). The goal is monotonic improvement: the Phase 4 score should meet or exceed the Phase 1 score.

## 4-Phase Pipeline Overview

| Phase | Name | Agent | Objective | Key Output |
|-------|------|-------|-----------|------------|
| 1 | Strategy | content-strategist | Audience analysis, keyword research, competitive landscape, content calendar | Content strategy document, personas, keywords |
| 2 | Research | research-gatherer | Factual research per content piece, source gathering, statistics | Research briefs per content piece |
| 3 | Outline | outline-architect | Production-ready outlines mapped to keywords and research | Detailed outlines with section allocations |
| 4 | Production Readiness | Lead synthesis | Verification, CRS scoring, package assembly | Content Production Package |

**Phases 1-2**: Discovery and intelligence gathering
**Phase 3**: Structural planning
**Phase 4**: Verification and packaging (no new content created)

## Operational Rules

These rules emerged from real content production work. Violating them leads to predictable failures.

### Strategy-First Rule

No content piece proceeds to research or outlining without a validated strategy. Strategy defines:
- Who the audience is (personas)
- What keywords to target
- Where the content fits in the competitive landscape
- When it publishes (calendar)

Research without strategy produces interesting but unfocused material. Outlines without strategy produce structures that serve no business goal.

### Research Validates Strategy

Research does not replace strategy -- it validates and enriches it. For each content piece, research should:
- Confirm that the strategic angle has factual support
- Identify statistics and sources that strengthen the argument
- Surface gaps in the strategy that need addressing before outlining

If research contradicts the strategy, escalate to the lead. Do not silently adjust the strategy.

### Outlines Must Map to Keywords

Every outline section should trace back to a keyword or keyword cluster from the strategy phase. Sections that serve no keyword purpose may still be valid (introductions, conclusions, transitions), but the core argument sections must align with search intent.

### Git Safety Net

**Commit between every phase.** This is non-negotiable.

- Commit message format: `content: phase N <phase-name> complete - <project>`
- If a phase goes wrong, `git diff` shows exactly what changed
- The commit history becomes the production audit trail

### One Phase at a Time

Do not combine phases. Each phase has a distinct lens:
- Phase 1 defines strategy. It does not research facts.
- Phase 2 gathers research. It does not build outlines.
- Phase 3 builds outlines. It does not evaluate readiness.
- Phase 4 evaluates. It does not create new content.

Mixing scopes produces unpredictable results and defeats the checkpoint system.

## Quality Checkpoint Protocol

Run the `checklists/content-production-checkpoint.md` checklist between every phase.

**Full CRS scoring** at these checkpoints:
- After Phase 1 (strategy baseline)
- After Phase 4 (final readiness)

**Proceed/Hold decision**:
- **PROCEED** if deliverables are complete AND CRS has not dropped
- **HOLD** if strategy gaps remain -- address before advancing
- **HOLD** if research contradicts strategy -- escalate and resolve
- **RERUN** the phase with tighter constraints if scope was violated

## Project Configuration

Each content project should have a `content-production-config.md` file in its root directory. This file provides project-specific context that agents load before each phase.

### Config Template

Create `content-production-config.md` in your project root:

```markdown
# Content Production Config

## Business Goals

- Primary objective: (e.g., organic traffic growth, thought leadership, lead generation)
- Secondary objective: (e.g., brand awareness, community building)
- Success metrics: (e.g., target traffic, conversion rate, engagement)

## Target Audience

| Persona | Role | Pain Points | Content Preferences |
|---------|------|------------|-------------------|
| Persona 1 | | | |
| Persona 2 | | | |

## Primary Keywords

| Keyword / Cluster | Search Volume | Difficulty | Intent | Priority |
|-------------------|--------------|-----------|--------|----------|
| | | | | |

## Content Types

- [ ] Blog posts (target word count: )
- [ ] Long-form articles (target word count: )
- [ ] Landing pages
- [ ] Email sequences
- [ ] Social media content
- [ ] Whitepapers / Guides

## Publishing Schedule

| Cadence | Content Type | Channel |
|---------|-------------|---------|
| | | |

## Brand Voice Guidelines

- Tone: (e.g., authoritative but approachable)
- POV: (e.g., first person plural "we", second person "you")
- Jargon level: (e.g., industry-standard terminology, plain language)
- Avoid: (e.g., buzzwords, passive voice, hedging)

## Competitive URLs

| Competitor | URL | Notes |
|-----------|-----|-------|
| | | |
```

Agents reference this config via the `{{CONFIG_PATH}}` placeholder in their prompt templates. The pipeline orchestrator passes the actual path when dispatching agents.

## Multi-Piece Parallelism

When producing a content series or calendar:

1. **Phase 1 (Strategy)** covers the entire series -- one strategy pass for all pieces
2. **Phase 2 (Research)** can run in parallel across content pieces (one agent per piece)
3. **Phase 3 (Outline)** can run in parallel across content pieces (one agent per piece)
4. Phase boundaries are synchronization points -- all pieces must reach the checkpoint before the next phase begins

This ensures consistent strategic alignment across the entire content program.

## Pipeline Recovery

If the pipeline is interrupted:

1. Check `git log` for the last completed phase
2. Review the checkpoint metrics tracker for the last recorded state
3. Resume from the next incomplete phase

If a phase produced poor results:

1. `git checkout` to recover the pre-phase state
2. Adjust the config (e.g., refine personas, update keyword targets, tighten research scope)
3. Rerun the phase

---

*Strategy without research is guesswork. Research without strategy is trivia. Structure unites them into something publishable.*
