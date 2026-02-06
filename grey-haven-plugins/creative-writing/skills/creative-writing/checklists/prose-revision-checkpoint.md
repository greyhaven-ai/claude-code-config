# Prose Revision Checkpoint

Inter-phase quality gate for the prose revision pipeline. Run this checklist between every phase.

## Metrics Tracker

Record values at each checkpoint to track pipeline progress:

| Checkpoint | Word Count | Delta | Cumulative % | SVQ (S/V/Q) | Decision |
|------------|-----------|------:|-------------:|-------------|----------|
| Original   |           |     — |            — | —           | —        |
| Phase 1    |           |       |              | —           |          |
| Phase 2    |           |       |              |   /  /      |          |
| Phase 3    |           |       |              | —           |          |
| Phase 4    |           |       |              |   /  /      |          |
| Phase 5    |           |       |              | —           |          |
| Phase 6    |           |       |              |   /  /      |          |

---

## Step 1: Word Count Verification

- [ ] Record current word count for each book
- [ ] Calculate delta from previous checkpoint
- [ ] Calculate cumulative percentage change from original
- [ ] Verify cumulative cuts do not exceed **30% ceiling**

### If 30% Ceiling Reached

Stop cutting. If you are at Phase 3 or earlier:
- Skip remaining cutting phases
- Proceed directly to Phase 5 (Enrichment)
- Document the skip in the metrics tracker

---

## Step 2: Git Commit

- [ ] Stage all changed files for this phase
- [ ] Commit with message: `revision: phase N <phase-name> complete - <book>`
- [ ] Verify commit succeeded with `git log --oneline -1`

### Commit Message Examples

```
revision: phase 1 surface cleanup complete - Book 1
revision: phase 2 prose craft complete - Book 2
revision: phase 5 enrichment complete - Book 1
```

---

## Step 3: SVQ Scoring (Phases 2, 4, 6 Only)

Skip this step for Phases 1, 3, and 5.

- [ ] Run prose-style-analyst on representative sample (2-3 chapters)
- [ ] Record Style score (1-10)
- [ ] Record Voice score (1-10)
- [ ] Record Quality score (1-10)
- [ ] Calculate composite: (S + V + Q) / 3
- [ ] Compare to previous SVQ checkpoint

### SVQ Interpretation

| Trend | Meaning | Action |
|-------|---------|--------|
| Scores improved | Pipeline working as intended | PROCEED |
| Scores stable | No regression, acceptable | PROCEED |
| S dropped | Style damage (sentence variety, diction) | HOLD - investigate |
| V dropped | Voice erosion (cuts removed character) | HOLD - investigate |
| Q dropped | Quality regression (clarity, economy) | HOLD - investigate |

---

## Step 4: Phase Scope Verification

- [ ] Review a sample of changes (`git diff HEAD~1`) to verify edits match phase scope
- [ ] Phase 1: Only tic removal, spiral fixes, voice checks (no craft rewrites)
- [ ] Phase 2: Only craft improvements (no structural changes)
- [ ] Phase 3: Only over-explanation cuts and counterpoints (no broad edits)
- [ ] Phase 4: Only sentence-level architecture (no content changes)
- [ ] Phase 5: Only additions (no deletions)
- [ ] Phase 6: No edits at all (audit only)

### If Scope Was Violated

The agent did work belonging to a different phase. Options:
- If minor: Note it and proceed (the work is done)
- If significant: Revert with `git checkout HEAD~1` and rerun with stricter instructions

---

## Step 5: Proceed / Hold Decision

### PROCEED If

- [ ] Word count delta is within expected range for this phase
- [ ] Cumulative cuts are under 30% ceiling
- [ ] SVQ has not dropped (at scoring checkpoints)
- [ ] Phase scope was respected
- [ ] No obvious quality issues in spot-check

### HOLD If

- [ ] Cumulative cuts exceed 30% -- skip to Phase 5
- [ ] SVQ score dropped -- investigate before continuing
- [ ] Phase scope was significantly violated -- consider revert and rerun
- [ ] Spot-check reveals unexpected damage to prose quality

### RERUN If

- [ ] Phase produced clearly inferior results
- [ ] Agent misunderstood the brief
- [ ] Technical issues (partial edits, corrupted files)

Record decision in the metrics tracker before proceeding.

---

*Every checkpoint is a decision point, not a formality.*
