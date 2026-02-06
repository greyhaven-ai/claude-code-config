# Phase 6: Final Audit

| Field | Value |
|-------|-------|
| **Phase** | 6 |
| **Name** | Final Audit |
| **Agents** | prose-style-analyst (`creative-writing:writing-prose-style-analyst`) + believability-auditor (`creative-writing:writing-believability-auditor`) |
| **Execution** | Two agents run **in parallel** |
| **Expected Delta** | 0% (audit only -- no edits) |

---

## Objectives

Phase 6 is verification, not revision. The manuscript is not touched. Two specialized agents examine the post-revision text from different analytical angles and produce a final report. Their findings inform whether the pipeline output is accepted or whether specific phases need to be rerun.

### 1. Automated Verification Checks

Mechanical checks that produce hard numbers:

- **Word count vs. 30% ceiling**: Confirm total cumulative cuts from Phases 1-4 did not exceed 30% of the original word count. If they did and Phase 5 did not compensate sufficiently, flag for review.
- **Verbal tic residual counts**: Re-scan for the project's verbal tic list from the config. Phase 1 targeted these -- how many survived the full pipeline? Report absolute counts and per-10,000-word density.
- **Em-dash density**: Phase 4 addressed em-dash overuse. Report final density (em-dashes per 1,000 words) and compare against the pre-Phase-4 baseline.

### 2. Final SVQ Scoring

The prose-style-analyst produces the third and final SVQ checkpoint score:

- Score each dimension (Style, Voice, Quality) on the 1-10 scale
- Calculate the composite SVQ score
- Compare against the Phase 2 baseline and the Phase 4 midpoint score
- SVQ must show **monotonic improvement** or remain stable -- any drop requires investigation
- Flag specific dimensions that declined, with quoted evidence of where quality degraded

### 3. Consistency Check via Believability Auditor

The believability-auditor examines the manuscript for issues introduced *during* revision:

- **Timeline consistency**: Did cutting or rearranging break temporal logic?
- **Character consistency**: Did voice differentiation work (Phase 1) or enrichment (Phase 5) alter a character's established behavior or knowledge?
- **World rules**: Did any revision phase inadvertently contradict established world-building?
- **Cause-and-effect chains**: Did cutting explanatory passages (Phases 2-3) remove necessary causal links?

This is not a full believability audit of the original manuscript. The scope is narrower: **what did the revision pipeline break?**

### 4. Final Report Generation

Produce a consolidated report comparing pre-revision and post-revision metrics:

```
| Metric                  | Pre-Revision | Post-Revision | Delta     |
|-------------------------|-------------|---------------|-----------|
| Word Count              | X           | X             | -X%       |
| SVQ Composite           | X.X         | X.X           | +X.X      |
| S (Style)               | X           | X             | +/-X      |
| V (Voice)               | X           | X             | +/-X      |
| Q (Quality)             | X           | X             | +/-X      |
| Verbal Tic Density      | X/10k       | X/10k         | -X%       |
| Em-Dash Density         | X/1k        | X/1k          | -X%       |
| Believability Issues    | N/A         | X found       | --        |
```

---

## Agent Prompt Templates

### Prose Style Analyst

```
You are performing the prose-style-analyst portion of Phase 6 (Final Audit)
in the prose revision pipeline.

BOOK PATH: {{BOOK_PATH}}
CONFIG PATH: {{CONFIG_PATH}}
ORIGINAL WORD COUNT: {{ORIGINAL_WORD_COUNT}}
SVQ BASELINE (Phase 2): {{SVQ_BASELINE}}

## YOUR ROLE: AUDIT ONLY -- NO EDITS

You are scoring and measuring. You do not modify the manuscript. Your output
is a report.

## Tasks

### 1. SVQ Scoring

Perform a full SVQ analysis of the post-revision manuscript:

- **S (Style)**: Sentence architecture, diction, prose density, figurative
  language. Score 1-10.
- **V (Voice)**: Persona, attitude, distinctiveness, consistency. Score 1-10.
- **Q (Quality)**: Craft precision, clarity, economy, variety, control.
  Score 1-10.
- **Composite**: (S + V + Q) / 3.

Compare each dimension against the Phase 2 baseline ({{SVQ_BASELINE}}).
Flag any dimension that dropped. For each drop, quote specific passages that
demonstrate the regression and identify which revision phase likely caused it.

### 2. Automated Metrics

Calculate and report:

- **Final word count** and cumulative delta from original ({{ORIGINAL_WORD_COUNT}})
- **Verbal tic residuals**: Scan for the verbal tic list in {{CONFIG_PATH}}.
  Report absolute count and per-10,000-word density.
- **Em-dash density**: Count em-dashes. Report per-1,000-word density.
- **Sentence length variation**: Standard deviation of sentence lengths across
  a representative sample.

### 3. Sample Verification

Select 3-5 passages (one from the opening, middle, and closing sections at
minimum) and perform close reading analysis. Confirm that:

- The writer's original voice is preserved
- Sentence variety is present
- Prose feels lean but not skeletal
- Enrichment additions (Phase 5) blend seamlessly

### 4. Report

Produce the final metrics comparison table and a narrative summary of findings.
Include specific recommendations only if SVQ dropped or if metrics fall outside
expected ranges.
```

### Believability Auditor

```
You are performing the believability-auditor portion of Phase 6 (Final Audit)
in the prose revision pipeline.

BOOK PATH: {{BOOK_PATH}}
CONFIG PATH: {{CONFIG_PATH}}
ORIGINAL WORD COUNT: {{ORIGINAL_WORD_COUNT}}
SVQ BASELINE (Phase 2): {{SVQ_BASELINE}}

## YOUR ROLE: AUDIT ONLY -- NO EDITS

You are checking for consistency issues INTRODUCED BY THE REVISION PROCESS.
This is not a full believability audit of the original work. Your scope is
narrow: what did the pipeline break?

## Tasks

### 1. Timeline Consistency

Check that cutting and rearranging did not create temporal contradictions:

- Verify day/time references still form a coherent sequence
- Check that "earlier" and "later" references still point correctly
- Confirm that removed passages did not contain time anchors that other
  passages depend on

### 2. Character Consistency

Check that revision work preserved character integrity:

- Voice differentiation (Phase 1) did not flatten distinct speech patterns
  into uniformity
- Cutting over-explanation (Phases 2-3) did not remove character motivation
  that later scenes depend on
- Enrichment additions (Phase 5) are consistent with established character
  traits, knowledge, and domain

### 3. World Rules

Check that no revision phase contradicted established world-building:

- Rules referenced in cut passages are still established elsewhere
- Enrichment details do not introduce contradictions with the world's
  established logic
- Spatial and geographical references remain consistent

### 4. Cause-and-Effect Chains

Check that cutting did not sever necessary causal links:

- Consequences still have visible causes
- Character decisions still have visible motivations
- Plot developments still have adequate setup

### 5. Report

Produce a findings report organized by severity:

- **Critical**: Issues that would confuse or lose the reader
- **Major**: Issues a careful reader would notice
- **Minor**: Issues only on close re-reading
- **Clean**: Areas checked with no issues found

For each issue, identify which revision phase likely introduced it and
suggest the minimal fix needed.
```

---

## Phase Checklist

Before marking Phase 6 complete, verify all of the following:

- [ ] Prose-style-analyst has produced a complete SVQ score with all three dimensions
- [ ] SVQ composite is equal to or higher than the Phase 2 baseline
- [ ] No individual SVQ dimension (S, V, or Q) dropped by more than 1 point from baseline
- [ ] Final word count delta from original is within the -10% to -20% expected range
- [ ] Cumulative Phase 1-4 cuts did not exceed the 30% ceiling
- [ ] Verbal tic residual density is measurably lower than pre-Phase-1 levels
- [ ] Em-dash density is within acceptable range (reduced from pre-Phase-4 levels)
- [ ] Believability-auditor found no critical consistency issues
- [ ] Any major consistency issues have been documented with the likely causal phase
- [ ] Sample passages confirm the writer's voice is preserved
- [ ] Final metrics comparison table has been generated
- [ ] Both agent reports have been consolidated into a single final audit document
- [ ] **No edits were made to the manuscript during this phase**

---

## Common Pitfalls

### Accepting Score Improvement Without Reading Samples

Numbers can improve while prose degrades. A higher SVQ composite does not guarantee the manuscript reads well. Agents can optimize for measurable qualities (sentence variety, vocabulary diversity) at the expense of feel. Always pair quantitative scoring with close reading of actual passages. If the numbers say "improved" but the sample passages feel wrong, trust the reading over the score.

### Missing Consistency Issues from Phase 5

The enrichment phase is the most likely source of consistency breaks. New sensory details may contradict established world-building. New body moments may give a character knowledge they should not have (a character noticing a detail in a room they have not yet entered). New counterpoints may create character positions that contradict later scenes. The believability auditor should weight Phase 5 additions heavily in its consistency check.

### Over-Auditing Stable Prose

Not every passage needs forensic examination. If Phases 1-4 made minimal changes to a chapter (the verbal tic count was already low, the prose was already lean), that chapter needs proportionally less audit time. Focus audit depth on the chapters that experienced the heaviest revision. The word-count delta per chapter is a reliable proxy for revision intensity -- audit the high-delta chapters first and most thoroughly.

### Conflating Pre-Existing Issues with Pipeline Damage

The believability auditor's scope is issues *introduced by revision*. If the original manuscript had a timeline inconsistency that survived all six phases untouched, that is worth noting but is not a pipeline failure. Distinguish between inherited issues and introduced issues in the report. Mixing them produces a misleading assessment of the pipeline's performance.

### Skipping the Report When Everything Looks Clean

A clean audit is still a report. The absence of issues is a finding that needs to be documented. Future pipeline runs on other books benefit from seeing what a clean Phase 6 looks like. Record the metrics, note the clean bill, and close the phase formally. The audit trail is part of the pipeline's value.

---

*The final audit does not improve the prose. It proves that the pipeline did.*
