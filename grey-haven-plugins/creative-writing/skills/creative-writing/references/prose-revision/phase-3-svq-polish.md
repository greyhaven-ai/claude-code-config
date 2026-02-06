# Phase 3: SVQ Polish

| Field | Value |
|-------|-------|
| **Phase** | 3 |
| **Name** | SVQ Polish |
| **Agent** | editor-reviewer (`creative-writing:writing-editor-reviewer`) |
| **Expected Delta** | -3% to -8% |

---

## Objectives

Phase 3 is a precision pass. Where Phase 2 made broad craft-level cuts, Phase 3 operates with a scalpel. The goals are narrow and specific:

1. **Targeted deletion of remaining over-explanation.** Phase 2 caught the obvious cases -- passages that told the reader what had just been shown. Phase 3 hunts the subtler survivors: the clarifying sentence after a strong image, the emotional label following a well-rendered reaction, the paragraph that restates what dialogue already conveyed. These are smaller cuts, often a single sentence or clause rather than an entire paragraph.

2. **Inject counterpoints.** Find moments where characters accept information, situations, or emotional states too easily. A character who never pushes back feels passive; a world where every revelation lands cleanly feels frictionless. Inject brief counterpoints: a character challenges an assumption, questions a conclusion, or contradicts their own initial reaction. These are not new scenes or subplots -- they are single beats of resistance that add depth.

3. **Drive SVQ improvement.** This phase exists to push the SVQ composite score upward from the Phase 2 checkpoint baseline. Every edit should be evaluated against that baseline: does this cut sharpen Style, Voice, or Quality? If the answer is unclear, leave the text alone.

The agent should load the SVQ baseline scores from the Phase 2 checkpoint before beginning work. These scores are the target to beat, not merely match.

---

## Agent Prompt Template

```markdown
You are performing Phase 3 (SVQ Polish) of the prose revision pipeline.

**Manuscript**: {{BOOK_PATH}}
**Project Config**: {{CONFIG_PATH}}
**SVQ Baseline (Phase 2 Checkpoint)**: {{SVQ_BASELINE}}

## Your Mission

Make surgical edits to improve prose quality as measured by SVQ scoring. You have two tools:

### Tool 1: Delete Remaining Over-Explanation

Hunt for passages where the text explains what it has already shown. These are the survivors of Phase 2 -- subtler than the obvious telling-after-showing, but still dragging prose quality down.

Targets:
- A clarifying sentence after a strong image or action
- An emotional label following a well-rendered physical reaction
- A restating summary after dialogue that already carried the meaning
- Transitional sentences that over-connect beats the reader can link themselves

Delete these. Do not replace them. Trust the reader.

### Tool 2: Inject Counterpoints

Find moments where a character accepts something too easily and add a brief beat of resistance. A counterpoint is:
- A character challenging an assumption they just heard
- A contradiction between what a character thinks and what they do
- A moment of skepticism before acceptance
- A flash of an opposing emotion before the dominant one wins

Counterpoints must be grounded in the character's established personality, domain, and worldview (see project config for character domains). A counterpoint that feels arbitrary is worse than none.

## Rules

- **Edit only.** Do not add new scenes, paragraphs, or dialogue beyond counterpoint injections.
- **Smaller cuts than Phase 2.** If you are deleting entire paragraphs, you are likely duplicating Phase 2 work.
- **Measure against SVQ baseline.** Every edit should demonstrably improve at least one of: Style, Voice, Quality.
- **Know when to stop.** Diminishing returns are real. If you are agonizing over single-word cuts, the phase is done.
- **Preserve the writer's voice.** You are sharpening, not rewriting.
- **Commit nothing.** The pipeline orchestrator handles git operations.

## Output

When complete, report:
1. Summary of changes (categories and counts)
2. Estimated word count delta
3. List of counterpoints injected (location and brief description)
4. Confidence assessment: did this phase meaningfully improve SVQ?
```

---

## Phase Checklist

- [ ] SVQ baseline scores from Phase 2 checkpoint loaded and recorded
- [ ] Cumulative word count delta checked against 30% ceiling before starting
- [ ] Over-explanation scan completed -- remaining tell-after-show instances identified and deleted
- [ ] Counterpoints injected where characters accepted situations too easily
- [ ] All counterpoints grounded in character personality and domain (cross-referenced with config)
- [ ] No new scenes, paragraphs, or plot-altering content added
- [ ] Cuts are sentence/clause-level, not paragraph-level (no Phase 2 duplication)
- [ ] Word count delta recorded and within expected range (-3% to -8%)
- [ ] Cumulative cuts across Phases 1-3 remain under 30% ceiling
- [ ] Changes reviewed for voice preservation -- prose still sounds like the writer
- [ ] Git commit created: `revision: phase 3 svq-polish complete - <book>`

---

## Common Pitfalls

### Diminishing Returns

Phase 3 sits at the point where cutting yields smaller and smaller improvements. The instinct to "find one more thing to cut" can lead to over-editing, where lean prose becomes skeletal prose. Set a threshold: if a pass through a chapter produces fewer than 2-3 meaningful edits, that chapter is done. Move on.

### Forced Counterpoints

A counterpoint must emerge from who the character is. If Marcus is an architect who thinks in structures, his skepticism should sound like structural analysis, not generic doubt. Counterpoints that feel bolted on -- where a character suddenly questions something for no in-character reason -- damage voice more than they add depth. When in doubt, skip the counterpoint. Absence of resistance is better than artificial resistance.

### Duplicating Phase 2 Work

Phase 3 targets are smaller than Phase 2 targets. If you find yourself deleting entire paragraphs of over-explanation, either Phase 2 missed them (unlikely if the checkpoint passed) or you are re-litigating Phase 2 decisions. Phase 3 cuts are the leftover fragments: the single sentence that lingers after the paragraph was already tightened, the clause that over-clarifies a connection. Stay in scope.

### Ignoring the 30% Ceiling

By Phase 3, cumulative cuts from Phases 1-2 may already be approaching the 30% ceiling defined in the SOP. Check the cumulative delta before starting. If Phases 1-2 have already cut 25%+, Phase 3 should be extremely conservative -- focus on counterpoint injection rather than further deletion. If the ceiling is already hit, skip Phase 3 cutting entirely and proceed to Phase 4.

---

*Precision is knowing which sentence to cut -- and which to leave standing.*
