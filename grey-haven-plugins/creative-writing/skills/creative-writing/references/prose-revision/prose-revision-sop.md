# Prose Revision SOP

Standard Operating Procedure for systematic manuscript revision using the 6-phase pipeline.

## SVQ Scoring Framework

The pipeline uses **SVQ scoring** (Style, Voice, Quality) from the prose-style-analyst agent as the primary quality metric.

| Dimension | What It Measures | Scale |
|-----------|-----------------|-------|
| **S** (Style) | Sentence architecture, diction, prose density, figurative language | 1-10 |
| **V** (Voice) | Persona, attitude, distinctiveness, consistency | 1-10 |
| **Q** (Quality) | Craft precision, clarity, economy, variety, control | 1-10 |

**Composite SVQ** = (S + V + Q) / 3

| Composite | Interpretation |
|-----------|---------------|
| 9-10 | Publication-ready, exceptional craft |
| 7-8 | Strong work, minor polish needed |
| 5-6 | Solid foundation, revision opportunities |
| 3-4 | Significant development needed |
| 1-2 | Fundamental craft work required |

SVQ scoring is performed at checkpoints after Phases 2, 4, and 6. The goal is monotonic improvement: each checkpoint should score equal to or higher than the previous.

## 6-Phase Pipeline Overview

| Phase | Name | Agent | Objective | Expected Delta |
|-------|------|-------|-----------|---------------|
| 1 | Surface Cleanup | editor-reviewer | Verbal tics, closing spirals, voice differentiation | -5% to -10% |
| 2 | Prose Craft | editor-reviewer | Perception verbs, over-explanation, sentence variety, showing | -5% to -15% |
| 3 | SVQ Polish | editor-reviewer | Targeted over-explanation deletion, counterpoint injection | -3% to -8% |
| 4 | Sentence Architecture | prose-style-analyst | Em-dash density, sentence shapes, character metaphors | -2% to +2% |
| 5 | Enrichment | editor-reviewer | Sensory anchoring, body moments, dialogue beats, texture | +3% to +8% |
| 6 | Final Audit | prose-style-analyst + believability-auditor | Automated checks, SVQ scoring, consistency verification | 0% (audit only) |

**Phases 1-4**: Cutting and refining (net reduction)
**Phase 5**: Adding (net growth)
**Phase 6**: Verification (no changes)

## Operational Lessons

These rules emerged from real revision work. Violating them leads to predictable failures.

### Edit-Only Rule

Agents performing revision work must **only edit existing text**. They must not:
- Add new scenes, paragraphs, or dialogue (except Phase 5)
- Restructure chapter order
- Change plot points
- Alter character arcs
- Rewrite passages in the agent's own voice

The writer's voice is sacred. Revision sharpens it; it does not replace it.

### 30% Ceiling

Total cumulative cuts across Phases 1-4 must not exceed **30% of original word count**. Beyond this threshold:
- Voice erosion becomes likely
- Prose feels skeletal rather than lean
- Recovery in Phase 5 cannot compensate

If you reach 30% after Phase 3, **skip Phase 4 cutting** and proceed to Phase 5 enrichment.

### Git Safety Net

**Commit between every phase.** This is non-negotiable.

- Commit message format: `revision: phase N <phase-name> complete - <book>`
- If a phase goes wrong, `git diff` shows exactly what changed
- If cuts go too deep, `git checkout` recovers the previous phase's output
- The commit history becomes the revision audit trail

### Word Count Tracking

Record word counts at every checkpoint:

```
| Checkpoint | Word Count | Delta from Original | Cumulative % |
|------------|-----------|--------------------:|-------------:|
| Original   | 85,000    |                   — |            — |
| Phase 1    | 79,000    |              -6,000 |        -7.1% |
| Phase 2    | 70,000    |             -15,000 |       -17.6% |
| Phase 3    | 66,000    |             -19,000 |       -22.4% |
| Phase 4    | 66,500    |             -18,500 |       -21.8% |
| Phase 5    | 71,000    |             -14,000 |       -16.5% |
| Phase 6    | 71,000    |             -14,000 |       -16.5% |
```

A typical full-pipeline result lands at **-10% to -20%** net change.

### One Phase at a Time

Do not combine phases. Each phase has a distinct lens:
- Phase 1 hunts tics. It does not rewrite sentences.
- Phase 2 attacks craft. It does not add sensory detail.
- Phase 5 adds. It does not cut.

Mixing scopes produces unpredictable results and defeats the checkpoint system.

## Quality Checkpoint Protocol

Run the `checklists/prose-revision-checkpoint.md` checklist between every phase.

**Full SVQ scoring** at these checkpoints:
- After Phase 2 (first craft pass complete)
- After Phase 4 (sentence-level refinement complete)
- After Phase 6 (final audit)

**Proceed/Hold decision**:
- **PROCEED** if word count delta is within expected range AND SVQ has not dropped
- **HOLD** if cumulative cuts exceed 30% — skip to Phase 5
- **HOLD** if SVQ dropped — investigate what the phase damaged before continuing
- **RERUN** the phase with tighter constraints if scope was violated

## Project Configuration

Each manuscript project should have a `prose-revision-config.md` file in its root directory. This file provides project-specific context that agents load before each phase.

### Config Template

Create `prose-revision-config.md` in your manuscript root:

```markdown
# Prose Revision Config

## Book Paths

| Book | Path | Approximate Word Count |
|------|------|----------------------:|
| Book 1 | ./book-1/ | 85,000 |
| Book 2 | ./book-2/ | 92,000 |

## Character Domains

Map each POV character to their conceptual domain. Agents use this to keep metaphors
consistent with how each character perceives the world.

| Character | Domain | Metaphor Pattern |
|-----------|--------|-----------------|
| Elena | Music/Sound | Thoughts as melodies, conflict as dissonance |
| Marcus | Architecture | Problems as structures, solutions as foundations |
| River | Water/Nature | Emotions as currents, change as seasons |

## POV Conventions

- POV: Third person limited
- Tense: Past
- Head-hopping: Never within a scene
- Scene breaks: ### between POV shifts
- Internal thought: Italics, no tags

## Verbal Tics to Hunt

Project-specific words/patterns to flag in Phase 1:

- "just" (overused filler)
- "seemed to" (distancing)
- "a little" / "a bit" (hedging)
- "started to" / "began to" (false starts)
- "could feel" / "could see" (filter words)

## Sensory Preferences

Which senses each POV character notices first:

| Character | Primary Sense | Secondary Sense |
|-----------|--------------|----------------|
| Elena | Sound | Touch |
| Marcus | Sight | Smell |
| River | Touch | Taste |
```

Agents reference this config via the `{{CONFIG_PATH}}` placeholder in their prompt templates. The pipeline orchestrator passes the actual path when dispatching agents.

## Multi-Book Parallelism

When revising a multi-book series:

1. **Within each phase**, all books can be revised in parallel (one agent per book)
2. **Between phases**, all books must reach the checkpoint before the next phase begins
3. Phase boundaries are synchronization points — no book proceeds ahead of others

This ensures consistent quality gates across the entire series.

## Pipeline Recovery

If the pipeline is interrupted:

1. Check `git log` for the last completed phase
2. Use `/revision-phase <next-phase-number> <manuscript-root>` to resume
3. The single-phase runner handles one phase at a time with its own checkpoint

If a phase produced poor results:

1. `git checkout` to recover the pre-phase state
2. Adjust the config (e.g., tighten verbal tic list, loosen cut thresholds)
3. Rerun with `/revision-phase`

---

*Revision is not rewriting. It is sharpening what is already there.*
