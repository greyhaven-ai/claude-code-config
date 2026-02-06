# Content Production Checkpoint

Inter-phase quality gate for the content production pipeline. Run this checklist between every phase.

## Metrics Tracker

Record values at each checkpoint to track pipeline progress:

| Checkpoint | Deliverables Complete | CRS (A/R/S) | Decision |
|------------|----------------------|-------------|----------|
| Phase 1    |                      |   /  /      |          |
| Phase 2    |                      | —           |          |
| Phase 3    |                      | —           |          |
| Phase 4    |                      |   /  /      |          |

---

## Step 1: Deliverable Completeness Check

- [ ] All expected outputs for this phase have been produced
- [ ] Outputs cover every content piece in the strategy (no pieces skipped)
- [ ] Output format matches the expected structure (briefs, outlines, etc.)
- [ ] Output quality is sufficient (not placeholder or skeletal content)

### Phase-Specific Deliverables

**Phase 1 (Strategy)**:
- [ ] Audience personas defined
- [ ] Keyword map with clusters and intent
- [ ] Competitive analysis summary
- [ ] Content calendar with titles, types, keywords, dates

**Phase 2 (Research)**:
- [ ] Research brief per content piece
- [ ] Source library with credibility assessment
- [ ] Statistics with attribution and dates
- [ ] Research gaps documented

**Phase 3 (Outline)**:
- [ ] Hierarchical outline per content piece
- [ ] Keyword placement map
- [ ] Word count allocation table
- [ ] Research integration notes

**Phase 4 (Production Readiness)**:
- [ ] All verification checklists completed
- [ ] Content Production Package assembled
- [ ] CRS scored and recorded

---

## Step 2: Dependency Verification

- [ ] This phase received all required inputs from previous phases
- [ ] Inputs were used (not ignored or contradicted)
- [ ] No phase scope was violated (no work belonging to other phases)

### Dependency Map

| Phase | Requires |
|-------|----------|
| Phase 1 | Project config only |
| Phase 2 | Phase 1 strategy output |
| Phase 3 | Phase 1 strategy + Phase 2 research |
| Phase 4 | Phases 1 + 2 + 3 outputs |

If a dependency was not available or was incomplete, the phase output is suspect. Hold and resolve the dependency before proceeding.

---

## Step 3: CRS Scoring (Phases 1 and 4 Only)

Skip this step for Phases 2 and 3.

- [ ] Score Alignment (A): Strategic fit, audience targeting, keyword coverage (1-10)
- [ ] Score Research (R): Source quality, depth, factual accuracy (1-10)
- [ ] Score Structure (S): Outline completeness, logical flow, word count allocation (1-10)
- [ ] Calculate composite: (A + R + S) / 3
- [ ] Compare to previous CRS checkpoint (Phase 4 vs Phase 1)

### CRS Interpretation

| Trend | Meaning | Action |
|-------|---------|--------|
| Scores improved | Pipeline working as intended | PROCEED |
| Scores stable | No regression, acceptable | PROCEED |
| A dropped | Strategy drift (audience or keyword misalignment) | HOLD - investigate |
| R dropped | Research degradation (gaps, stale sources) | HOLD - investigate |
| S dropped | Structural regression (outlines not serving strategy) | HOLD - investigate |

### CRS Thresholds

| Composite | Readiness |
|-----------|-----------|
| 8-10 | Production-ready |
| 6-7 | Acceptable with noted caveats |
| 4-5 | Hold -- address gaps before proceeding |
| 1-3 | Return to earlier phase |

---

## Step 4: Git Commit

- [ ] Stage all outputs for this phase
- [ ] Commit with message: `content: phase N <phase-name> complete - <project>`
- [ ] Verify commit succeeded with `git log --oneline -1`

### Commit Message Examples

```
content: phase 1 strategy complete - Q1 Blog Series
content: phase 2 research complete - Q1 Blog Series
content: phase 3 outline complete - Q1 Blog Series
content: phase 4 production-readiness complete - Q1 Blog Series
```

---

## Step 5: Proceed / Hold Decision

### PROCEED If

- [ ] All deliverables for this phase are complete
- [ ] Dependencies from previous phases were properly consumed
- [ ] CRS has not dropped (at scoring checkpoints)
- [ ] Phase scope was respected (no work from other phases)
- [ ] No outstanding gaps or conflicts requiring resolution

### HOLD If

- [ ] Deliverables are incomplete -- finish before advancing
- [ ] Research contradicts strategy -- escalate and resolve
- [ ] CRS score dropped -- investigate what caused regression
- [ ] Phase scope was violated -- assess impact and consider rerun

### RERUN If

- [ ] Phase produced clearly inadequate results
- [ ] Agent misunderstood the brief or ignored inputs
- [ ] Technical issues (partial outputs, missing content pieces)

Record decision in the metrics tracker before proceeding.

---

*Every checkpoint is a decision point, not a formality.*
