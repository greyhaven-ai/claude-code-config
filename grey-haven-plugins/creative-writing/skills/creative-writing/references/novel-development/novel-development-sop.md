# Novel Development SOP

Standard Operating Procedure for systematic novel pre-production using the 5-phase pipeline.

## NRS Scoring Framework

The pipeline uses **NRS scoring** (Narrative Readiness Score) as the primary quality metric for assessing whether a novel's foundation is ready for drafting.

| Dimension | What It Measures | Scale |
|-----------|-----------------|-------|
| **C** (Character) | Depth, arcs, voice distinctiveness, ensemble dynamics | 1-10 |
| **W** (World) | Internal consistency, systems, rules, culture | 1-10 |
| **S** (Structure) | Plot integrity, pacing, beats, stakes, conflict | 1-10 |

**Composite NRS** = (C + W + S) / 3

| Composite | Interpretation |
|-----------|---------------|
| 9-10 | Draft-ready, exceptional foundation |
| 7-8 | Strong foundation, minor gaps to address |
| 5-6 | Solid start, development needed before drafting |
| 3-4 | Significant foundation work required |
| 1-2 | Fundamental development needed |

NRS scoring is performed at checkpoints after Phases 2 and 5. The goal is monotonic improvement: the Phase 5 score should equal or exceed the Phase 2 score.

## 5-Phase Pipeline Overview

| Phase | Name | Agent(s) | Dependency | Output |
|-------|------|----------|------------|--------|
| 1 | Research | research-gatherer | None | Research brief, fact sheets |
| 2 | Foundation | character-developer + world-builder + story-architect (parallel) | Phase 1 | Character profiles, world bible, beat sheet |
| 3 | Structure | outline-architect | Phase 2 (all 3) | Chapter-by-chapter outline with scene breakdowns |
| 4 | Dialogue | dialogue-coach | Phase 2 (characters) + Phase 3 | Voice guides, sample dialogue, scene dialogue notes |
| 5 | Integration | believability-auditor + lead synthesis | Phase 4 | Novel Foundation Package |

**Phases 1-2**: Research and parallel foundation building
**Phases 3-4**: Sequential structure and dialogue layering
**Phase 5**: Verification and synthesis (no new creation)

## Operational Rules

These rules emerged from real novel development work. Violating them leads to predictable failures.

### Research-First Rule

No character, world, or plot development begins before Phase 1 research is complete. Agents building on unresearched foundations produce work that must be discarded when reality contradicts assumption. The research brief is the bedrock -- everything else rests on it.

### Parallel Foundation Rule

Phase 2 runs three agents in parallel: character-developer, world-builder, and story-architect. They work from the same research brief but produce independent deliverables. This is not a shortcut -- it reflects how these concerns are genuinely separable at the foundation stage. Integration happens in Phase 3 when the outline-architect weaves all three together.

### Dependency Enforcement

Phase boundaries are strict:
- Phase 2 does not begin until Phase 1 deliverables exist
- Phase 3 does not begin until all three Phase 2 agents have completed
- Phase 4 does not begin until Phase 3 is complete
- Phase 5 does not begin until Phase 4 is complete

No phase skipping. No partial starts. The dependency chain exists because later phases consume earlier phases' output.

### No Drafting During Development

The novel development pipeline produces a **foundation package**, not prose. No agent writes manuscript text. No agent produces sample chapters. The pipeline's output is the blueprint that a writer (human or agent) uses to draft. Mixing development and drafting produces neither a solid foundation nor a quality draft.

### Git Safety Net

**Commit between every phase.** This is non-negotiable.

- Commit message format: `novel-dev: phase N <phase-name> complete - <project>`
- If a phase produces poor results, `git diff` shows exactly what changed
- The commit history becomes the development audit trail

## Project Configuration

Each novel project should have a `novel-development-config.md` file in its root directory. This file provides project-specific context that agents load before each phase.

### Config Template

Create `novel-development-config.md` in your project root:

```markdown
# Novel Development Config

## Project Overview

- **Title**: [Working title]
- **Genre**: [Primary genre / subgenre]
- **Target Word Count**: [Approximate target, e.g., 90,000]
- **POV**: [First person / Third limited / Third omniscient / Multiple]
- **Tense**: [Past / Present]

## Characters

| Character | Role | Brief Description |
|-----------|------|-------------------|
| [Name] | Protagonist | [One-line description] |
| [Name] | Antagonist | [One-line description] |
| [Name] | Supporting | [One-line description] |

## World Type

[Contemporary realistic / Historical / Secondary fantasy / Science fiction / etc.]

Brief description of the setting and any speculative elements.

## Themes

- [Primary theme]
- [Secondary theme]
- [Tertiary theme]

## Research Priorities

Areas requiring factual grounding:

- [Topic 1: e.g., 1920s Chicago speakeasy culture]
- [Topic 2: e.g., jazz music terminology and performance]
- [Topic 3: e.g., Prohibition-era law enforcement]

## Deliverable Paths

| Deliverable | Path |
|-------------|------|
| Research Brief | ./research/ |
| Character Profiles | ./characters/ |
| World Bible | ./world/ |
| Beat Sheet | ./structure/beat-sheet.md |
| Outline | ./structure/outline.md |
| Voice Guides | ./dialogue/ |
| Foundation Package | ./foundation-package.md |
```

Agents reference this config via the `{{CONFIG_PATH}}` placeholder in their prompt templates. The pipeline orchestrator passes the actual path when dispatching agents.

## Multi-Novel Parallelism

When developing multiple novels in a series:

1. **Within each phase**, all novels can be developed in parallel (one agent set per novel)
2. **Between phases**, all novels must reach the checkpoint before the next phase begins
3. Phase boundaries are synchronization points -- no novel proceeds ahead of others
4. Series-level consistency checks happen at Phase 5 across all novels

This ensures consistent quality gates across the entire series.

## Pipeline Recovery

If the pipeline is interrupted:

1. Check `git log` for the last completed phase
2. Use `/novel-phase <next-phase-number> <project-root>` to resume
3. The single-phase runner handles one phase at a time with its own checkpoint

If a phase produced poor results:

1. `git checkout` to recover the pre-phase state
2. Adjust the config (e.g., refine research priorities, add character detail)
3. Rerun with `/novel-phase`

---

*Development is not drafting. It is building the foundation that makes drafting possible.*
