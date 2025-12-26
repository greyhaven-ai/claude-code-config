# Evaluation Setup Checklist

Complete before running LLM evaluations.

## Phase 1: Rubric Preparation (Score: /25)

- [ ] **Dimensions defined** - 3-7 evaluation dimensions identified (5 pts)
- [ ] **Weights assigned** - Weights sum to 1.0, reflect importance (5 pts)
- [ ] **Criteria written** - Each dimension has 5-point criteria (5 pts)
- [ ] **Anchors provided** - Example outputs for at least 5, 3, and 1 scores (5 pts)
- [ ] **Rubric reviewed** - Another person validated the rubric (5 pts)

## Phase 2: Test Cases (Score: /25)

- [ ] **Cases created** - Minimum 10 test cases per task type (5 pts)
- [ ] **Difficulty spread** - Mix of easy, medium, and hard cases (5 pts)
- [ ] **Edge cases included** - Empty input, long input, adversarial (5 pts)
- [ ] **Expected behavior documented** - Clear success criteria per case (5 pts)
- [ ] **Ground truth available** - Reference answers for at least 50% (5 pts)

## Phase 3: Judge Configuration (Score: /20)

- [ ] **Model selected** - Judge model ≥ test model capability (5 pts)
- [ ] **Prompt tested** - Judge prompt produces structured output (5 pts)
- [ ] **Temperature set** - Using temperature=0 for reproducibility (5 pts)
- [ ] **Parsing validated** - JSON extraction works reliably (5 pts)

## Phase 4: Calibration (Score: /15)

- [ ] **Calibration set created** - 5-10 cases with pre-scored outputs (5 pts)
- [ ] **Judge accuracy tested** - Judge scores within ±1 of expected (5 pts)
- [ ] **Bias checks passed** - Position bias test on pairwise comparisons (5 pts)

## Phase 5: Infrastructure (Score: /15)

- [ ] **Runs configured** - Multiple runs per test (3-5 recommended) (5 pts)
- [ ] **Logging enabled** - All inputs, outputs, and scores logged (5 pts)
- [ ] **Baseline captured** - Current performance documented (5 pts)

---

## Scoring Guide

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Ready | Proceed with evaluation |
| 75-89 | Almost Ready | Address gaps before full run |
| 60-74 | Not Ready | Significant prep needed |
| <60 | Critical | Major setup required |

---

## Quick Validation Questions

Before running evaluation, confirm:

1. **Can you clearly explain what each rubric dimension measures?**
   - If no → Clarify criteria

2. **Would two evaluators score the same output similarly?**
   - If uncertain → Add anchor examples

3. **Are test cases representative of real usage?**
   - If no → Add more realistic cases

4. **Do you have a baseline to compare against?**
   - If no → Run initial evaluation first

5. **Is the evaluation cost acceptable?**
   - Calculate: `(test_cases × runs × cost_per_call)`

---

## Common Setup Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| No anchor examples | Low inter-rater reliability | Add 3+ anchors per dimension |
| Single run per case | Noise in results | Run 3-5 times, report variance |
| Weak model as judge | Poor evaluation quality | Use stronger model |
| No calibration | Biased scores | Validate with pre-scored cases |
| Missing edge cases | False confidence | Add adversarial test cases |
| No baseline | Can't measure improvement | Capture before changes |

---

## Pre-Flight Check

Final check before running:

```
□ Rubric loaded and valid
□ Test cases loaded and valid
□ Judge model configured
□ Temperature = 0
□ Logging enabled
□ Cost estimate acceptable
□ Baseline documented
□ Output directory created
```

**If all checked → Ready to run evaluation**

---

*Thorough setup prevents wasted time and unreliable results*
