# Novel Development Checkpoint

Inter-phase quality gate for the novel development pipeline. Run this checklist between every phase.

## Metrics Tracker

Record values at each checkpoint to track pipeline progress:

| Checkpoint | Deliverables Complete | NRS (C/W/S) | Issues Found | Decision |
|------------|----------------------|-------------|-------------|----------|
| Phase 1    |                      | —           | —           |          |
| Phase 2    |                      |   /  /      |             |          |
| Phase 3    |                      | —           |             |          |
| Phase 4    |                      | —           |             |          |
| Phase 5    |                      |   /  /      |             |          |

---

## Step 1: Deliverable Completeness Check

- [ ] All expected deliverables for this phase have been produced
- [ ] Each deliverable is substantive (not a placeholder or skeleton)
- [ ] Deliverables are organized in the correct output directories

### Expected Deliverables by Phase

| Phase | Expected Deliverables |
|-------|----------------------|
| 1 | Research brief, fact sheets, genre conventions, accuracy assessment |
| 2 | Character profiles, relationship map, world bible, consistency matrix, beat sheet, stakes map, pacing plan |
| 3 | Chapter outline, scene breakdowns, character arc distribution, continuity timeline |
| 4 | Voice guides, differentiation matrix, scene dialogue notes, key dialogue scenes |
| 5 | Consistency audit report, NRS scores, Novel Foundation Package, readiness assessment |

---

## Step 2: Dependency Verification

- [ ] All prerequisite phases are complete before this phase began
- [ ] This phase's agents had access to all required input deliverables
- [ ] No deliverable references information from a phase that has not yet run

### Dependency Chain

```
Phase 1 (Research) → Phase 2 (Foundation: 3 agents parallel)
Phase 2 (all 3 complete) → Phase 3 (Structure)
Phase 2 (characters) + Phase 3 → Phase 4 (Dialogue)
Phase 4 → Phase 5 (Integration)
```

---

## Step 3: Git Commit

- [ ] Stage all deliverable files for this phase
- [ ] Commit with message: `novel-dev: phase N <phase-name> complete - <project>`
- [ ] Verify commit succeeded with `git log --oneline -1`

### Commit Message Examples

```
novel-dev: phase 1 research complete - The Azure Rebellion
novel-dev: phase 2 foundation complete - The Azure Rebellion
novel-dev: phase 3 structure complete - The Azure Rebellion
novel-dev: phase 4 dialogue complete - The Azure Rebellion
novel-dev: phase 5 integration complete - The Azure Rebellion
```

---

## Step 4: NRS Scoring (Phases 2 and 5 Only)

Skip this step for Phases 1, 3, and 4.

- [ ] Score **C** (Character): Depth, arcs, voice distinctiveness, ensemble dynamics (1-10)
- [ ] Score **W** (World): Internal consistency, systems, rules, culture (1-10)
- [ ] Score **S** (Structure): Plot integrity, pacing, beats, stakes, conflict (1-10)
- [ ] Calculate composite: (C + W + S) / 3
- [ ] Compare to previous NRS checkpoint (Phase 5 only)

### NRS Interpretation

| Trend | Meaning | Action |
|-------|---------|--------|
| Scores improved | Pipeline strengthening foundation | PROCEED |
| Scores stable | No regression, acceptable | PROCEED |
| C dropped | Character development weakened | HOLD - investigate |
| W dropped | World consistency degraded | HOLD - investigate |
| S dropped | Structural integrity compromised | HOLD - investigate |

---

## Step 5: Phase Scope Verification

- [ ] Review deliverables to verify work matches phase scope
- [ ] Phase 1: Research only (no creative decisions)
- [ ] Phase 2: Foundation building (no outline, no dialogue)
- [ ] Phase 3: Structure only (no new characters, no voice work)
- [ ] Phase 4: Dialogue only (no structural changes)
- [ ] Phase 5: Audit and synthesis only (no new creative content)

### If Scope Was Violated

The agent did work belonging to a different phase. Options:
- If minor: Note it and proceed (the work is done)
- If significant: Discard the out-of-scope work and rerun with stricter instructions

---

## Step 6: Proceed / Hold Decision

### PROCEED If

- [ ] All expected deliverables are complete and substantive
- [ ] Dependencies were satisfied
- [ ] NRS has not dropped (at scoring checkpoints)
- [ ] Phase scope was respected
- [ ] No critical quality issues in spot-check

### HOLD If

- [ ] Key deliverables are missing or skeletal
- [ ] NRS score dropped -- investigate before continuing
- [ ] Phase scope was significantly violated
- [ ] Spot-check reveals deliverables that are internally inconsistent

### RERUN If

- [ ] Phase produced clearly inadequate results
- [ ] Agent misunderstood the brief
- [ ] Technical issues (partial output, corrupted files)

Record decision in the metrics tracker before proceeding.

---

*Every checkpoint is a decision point, not a formality.*
