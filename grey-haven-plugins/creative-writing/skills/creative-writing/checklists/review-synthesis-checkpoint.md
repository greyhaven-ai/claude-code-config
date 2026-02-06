# Review Synthesis Checkpoint

Synthesis gate for the parallel review pipeline. Run this checklist after all three reviewers have submitted their reports.

## Reviewer Status Tracker

Record completion status for each reviewer:

| Reviewer | Agent Type | Report Received | Finding Count | Top Severity |
|----------|-----------|:--------------:|:-------------:|:------------:|
| Editor-Reviewer | `creative-writing:writing-editor-reviewer` | [ ] | | |
| Prose Style Analyst | `creative-writing:writing-prose-style-analyst` | [ ] | | |
| Dialogue Coach | `creative-writing:writing-dialogue-coach` | [ ] | | |

---

## Step 1: Report Collection

- [ ] Editor-reviewer report received and complete
- [ ] Prose-style-analyst report received and complete (includes SVQ score)
- [ ] Dialogue-coach report received and complete
- [ ] All three reports use consistent severity tagging (Critical/Major/Minor/Note)

### If a Report Is Missing or Incomplete

Do not proceed with partial synthesis. Either:
- Wait for the missing report
- Re-dispatch the agent that failed to complete
- If re-dispatch fails, synthesize with two reports and document the gap

---

## Step 2: SVQ Baseline Recording

- [ ] Record SVQ scores from the prose-style-analyst report:

| Dimension | Score | Evidence Provided |
|-----------|:-----:|:-----------------:|
| S (Style) | | [ ] |
| V (Voice) | | [ ] |
| Q (Quality) | | [ ] |
| **Composite** | | -- |

- [ ] Composite SVQ calculated: (S + V + Q) / 3
- [ ] SVQ baseline documented for future prose revision pipeline use

---

## Step 3: Cross-Reference Identification

- [ ] Identify passages flagged by multiple reviewers
- [ ] Classify cross-references:

| Type | Count | Description |
|------|:-----:|-------------|
| Convergent | | Same passage, same concern (multiple agents) |
| Compound | | Same passage, different concerns |
| Systemic | | Different passages, same recurring pattern |

- [ ] Convergent findings marked as highest priority within their severity level

---

## Step 4: Contradiction Identification

- [ ] Identify cases where reviewers give contradictory recommendations
- [ ] Document each contradiction:
  - Which agents disagree
  - What each agent recommends
  - The passage in question
- [ ] Contradictions flagged for author decision (not resolved by synthesis)

---

## Step 5: Severity Synthesis

- [ ] Apply severity escalation rule: when agents disagree on severity, highest wins
- [ ] Compile severity-prioritized revision list:

| Severity | Count | Convergent | Majority | Author-Decide |
|----------|:-----:|:----------:|:--------:|:--------------:|
| Critical | | | | |
| Major | | | | |
| Minor | | | | |
| Note | | | | |

- [ ] Every finding in the revision list has: location, severity, source agent(s), description, recommendation

---

## Step 6: Synthesis Decision

### READY If

- [ ] All 3 reviewer reports received and complete
- [ ] Cross-references identified and classified
- [ ] Contradictions documented and flagged for author
- [ ] Severity-prioritized revision list compiled
- [ ] SVQ baseline recorded
- [ ] Synthesis report is coherent and actionable

### NOT READY If

- [ ] A reviewer report is missing -- wait or re-dispatch
- [ ] Severity tags are inconsistent across reports -- normalize before synthesizing
- [ ] Critical findings are ambiguous or lack sufficient evidence -- request clarification from the originating agent

Record decision before delivering the synthesis report to the author.

---

*Synthesis is not averaging opinions. It is finding the signal where multiple lenses converge.*
