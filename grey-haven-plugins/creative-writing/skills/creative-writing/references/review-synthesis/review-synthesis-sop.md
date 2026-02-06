# Review Synthesis SOP

Standard Operating Procedure for parallel multi-agent manuscript review with synthesis.

## Overview

The Review Synthesis pipeline dispatches three specialized agents simultaneously to review a manuscript from different analytical angles. Their independent findings are then synthesized into a unified, severity-prioritized revision list for the author.

Unlike the prose revision pipeline (which runs 6 sequential phases), Review Synthesis is **parallel dispatch with synthesis** -- all three reviewers work at the same time, and the orchestrator reconciles their findings afterward.

## Review Focus Mapping

Each agent reviews the manuscript through a distinct lens. There is deliberate overlap at the boundaries, which the synthesis protocol uses to identify high-confidence findings.

| Focus Area | Agent | Agent Type | Covers |
|-----------|-------|-----------|--------|
| Editorial | editor-reviewer | `creative-writing:writing-editor-reviewer` | Structure, clarity, pacing, developmental feedback, line editing, copy editing |
| Prose Quality | prose-style-analyst | `creative-writing:writing-prose-style-analyst` | Style, voice, quality, SVQ scoring, sentence architecture, diction, rhythm |
| Dialogue | dialogue-coach | `creative-writing:writing-dialogue-coach` | Voice differentiation, subtext, authenticity, speech patterns, naturalism |

## Severity Levels

All agents tag their findings with severity. The synthesis protocol uses these to prioritize the final revision list.

| Severity | Definition | Examples |
|----------|-----------|----------|
| **Critical** | Issues that would confuse or lose the reader | Broken causality, contradictory character action, incomprehensible passage |
| **Major** | Issues a careful reader would notice | Pacing drag, voice inconsistency across scenes, flat dialogue in key moment |
| **Minor** | Issues only on close re-reading | Slight verbal tic pattern, minor rhythm hiccup, attributable dialogue that could be cleaner |
| **Note** | Not a problem, but an observation or opportunity | Style choice the author may want to reconsider, alternative approach worth exploring |

## Synthesis Protocol

After all three agents complete their reviews, the orchestrator synthesizes findings using these rules:

### Agreement Rules

| Agreement Level | Confidence | Action |
|----------------|-----------|--------|
| All 3 agree | High | Include in revision list, highest priority within its severity level |
| 2 of 3 agree | Majority | Include with note identifying the dissenting perspective |
| All 3 disagree | Low | Present all three perspectives, flag for author decision |

### Severity Escalation

When multiple agents flag the same issue at different severity levels, **the highest severity wins**. If the editor-reviewer calls a pacing issue "Minor" but the prose-style-analyst calls it "Major," the synthesized finding is Major.

### Contradiction Handling

When agents give contradictory advice on the same passage (not just different severity, but opposite recommendations):

1. Document both positions with their reasoning
2. Flag explicitly as a contradiction requiring author decision
3. Do not attempt to resolve -- the author's creative intent is the tiebreaker
4. Place contradictions in a dedicated section of the synthesis report

### Cross-Reference Identification

The orchestrator identifies passages flagged by multiple agents:

- Same passage, same concern = **convergent finding** (strongest signal)
- Same passage, different concerns = **compound finding** (multiple issues in one location)
- Different passages, same pattern = **systemic finding** (recurring issue across the manuscript)

## Project Configuration

Each manuscript project should have a `review-config.md` file in its root directory. This file provides project-specific context that all three agents load before reviewing.

### Config Template

Create `review-config.md` in your manuscript root:

```markdown
# Review Config

## Manuscript

| Field | Value |
|-------|-------|
| Path | ./manuscript/ |
| Draft Number | 1 |
| Approximate Word Count | 85,000 |

## Focus Areas

Specific areas the author wants reviewers to pay extra attention to:

- Pacing in the middle act (chapters 8-14)
- Voice consistency for the secondary POV character
- Dialogue naturalism in the confrontation scenes

## Author Context

### Known Strengths
- Strong opening hooks
- Vivid sensory detail
- Distinctive protagonist voice

### Known Weaknesses
- Tendency toward over-explanation after emotional beats
- Dialogue tags that over-direct reader interpretation
- Pacing sag in transition chapters

### Specific Concerns
- Does the subplot in chapters 5-7 feel earned by the end?
- Is the antagonist's motivation clear enough without being heavy-handed?
- Are the two POV voices distinct enough?

## Character List

| Character | Role | Voice Notes |
|-----------|------|------------|
| Elena | Protagonist (POV) | Internal, musical metaphors, short sentences under stress |
| Marcus | Secondary POV | Analytical, architectural metaphors, longer complex sentences |
| River | Antagonist | Sparse, evasive, speaks in questions |

## POV Conventions

- POV: Third person limited
- Tense: Past
- Head-hopping: Never within a scene
- Scene breaks: ### between POV shifts
```

Agents reference this config via the `{{CONFIG_PATH}}` placeholder in their prompt templates. The orchestrator passes the actual path when dispatching agents.

## Execution Model

### Dispatch

All three agents are dispatched simultaneously with:
- The manuscript path
- The config path
- Agent-specific focus instructions (from their reference files)

No agent waits for another. They work independently and produce independent reports.

### Collection

The orchestrator waits for all three reports before beginning synthesis. If one agent takes significantly longer, the orchestrator waits -- partial synthesis defeats the purpose.

### Synthesis

The orchestrator applies the agreement rules, severity escalation, and cross-referencing to produce:

1. **Severity-prioritized revision list** -- every finding, ordered Critical > Major > Minor > Note
2. **Convergence map** -- which findings were flagged by multiple agents
3. **Contradiction log** -- opposite recommendations requiring author decision
4. **SVQ baseline** -- the prose-style-analyst's SVQ score, recorded as the pre-revision baseline

### Delivery

The synthesized report is the pipeline's output. The author uses it to guide revision -- either manually or as input to the prose revision pipeline.

## Integration with Prose Revision

The Review Synthesis pipeline is often the **entry point** before prose revision:

1. Run Review Synthesis to identify what needs work
2. Author reviews the synthesized findings and decides what to address
3. Run the prose revision pipeline on the manuscript, informed by the review findings
4. Optionally, run Review Synthesis again on the revised manuscript to verify improvement

The SVQ score from Review Synthesis becomes the pre-revision baseline for the prose revision pipeline's checkpoint system.

---

*Three lenses on the same page reveal what one pair of eyes never could.*
