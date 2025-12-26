# Rubric Design Guide

Create effective multi-dimensional rubrics for LLM evaluation.

## Rubric Structure

### Dimensions

A good rubric has 3-7 dimensions covering different quality aspects:

| Dimension | What It Measures | Common Weight |
|-----------|------------------|---------------|
| Accuracy | Factual correctness | 25-35% |
| Completeness | Coverage of requirements | 20-30% |
| Clarity | Readability, organization | 15-25% |
| Conciseness | No unnecessary content | 10-20% |
| Format | Structure compliance | 5-15% |
| Tone | Appropriate voice/style | 5-15% |

### Scoring Scale

Use 5-point scales with clear criteria:

```yaml
scale:
  5: "Excellent - Exceeds expectations, exemplary"
  4: "Good - Meets expectations, minor issues"
  3: "Acceptable - Partially meets, some issues"
  2: "Poor - Below expectations, significant issues"
  1: "Failing - Does not meet requirements"
```

### Anchor Examples

Each score level should have examples:

```yaml
dimension: accuracy
anchors:
  5:
    description: "All facts correct, properly sourced"
    example: "Python was created by Guido van Rossum in 1991..."
  3:
    description: "Mostly correct with minor errors"
    example: "Python was created in the late 1980s..." # (Minor date error)
  1:
    description: "Major factual errors or hallucinations"
    example: "Python was created by Linus Torvalds..." # (Wrong person)
```

## Rubric Templates

### Code Generation Rubric

```yaml
name: code-generation
dimensions:
  - name: correctness
    weight: 0.35
    criteria:
      5: "Code works perfectly for all inputs, handles edge cases"
      4: "Code works for main cases, minor edge case issues"
      3: "Code works for simple cases, fails on complex inputs"
      2: "Code has bugs affecting main functionality"
      1: "Code doesn't run or is completely wrong"

  - name: style
    weight: 0.20
    criteria:
      5: "Follows all style guidelines, excellent naming"
      4: "Mostly follows guidelines, good naming"
      3: "Some style issues, acceptable naming"
      2: "Many style violations, poor naming"
      1: "Ignores style guidelines entirely"

  - name: efficiency
    weight: 0.20
    criteria:
      5: "Optimal algorithm, O(n) or better where possible"
      4: "Good algorithm, reasonable complexity"
      3: "Works but suboptimal complexity"
      2: "Inefficient, obvious improvements possible"
      1: "Extremely inefficient or doesn't terminate"

  - name: documentation
    weight: 0.15
    criteria:
      5: "Clear docstring, explains purpose and parameters"
      4: "Good docstring, covers main points"
      3: "Basic docstring or comments"
      2: "Minimal or unclear documentation"
      1: "No documentation"

  - name: safety
    weight: 0.10
    criteria:
      5: "Handles all errors, no security issues"
      4: "Handles common errors, generally safe"
      3: "Some error handling, potential issues"
      2: "Poor error handling, some risks"
      1: "No error handling, security vulnerabilities"
```

### Content Writing Rubric

```yaml
name: content-writing
dimensions:
  - name: accuracy
    weight: 0.30
    criteria:
      5: "All information factually correct and verifiable"
      4: "Mostly accurate, minor details may be imprecise"
      3: "Generally accurate, some questionable claims"
      2: "Several inaccuracies or unsupported claims"
      1: "Major factual errors or misinformation"

  - name: relevance
    weight: 0.25
    criteria:
      5: "Directly addresses topic, no tangents"
      4: "Mostly on-topic, brief diversions"
      3: "Covers topic but with unnecessary content"
      2: "Partially addresses topic, much irrelevant content"
      1: "Does not address the requested topic"

  - name: clarity
    weight: 0.25
    criteria:
      5: "Crystal clear, well-organized, easy to follow"
      4: "Clear with good structure"
      3: "Understandable but could be clearer"
      2: "Confusing in places, poor organization"
      1: "Very difficult to understand"

  - name: engagement
    weight: 0.20
    criteria:
      5: "Compelling, interesting, holds attention"
      4: "Engaging, good flow"
      3: "Adequate, somewhat dry"
      2: "Boring, hard to stay focused"
      1: "Completely unengaging"
```

### Task Completion Rubric

```yaml
name: task-completion
dimensions:
  - name: completeness
    weight: 0.35
    criteria:
      5: "All requirements addressed, nothing missing"
      4: "Main requirements met, minor omissions"
      3: "Most requirements addressed, some gaps"
      2: "Several requirements not addressed"
      1: "Task not completed or mostly missing"

  - name: correctness
    weight: 0.30
    criteria:
      5: "All outputs correct and functional"
      4: "Outputs mostly correct, minor issues"
      3: "Some outputs correct, some errors"
      2: "Many errors in outputs"
      1: "Outputs incorrect or non-functional"

  - name: approach
    weight: 0.20
    criteria:
      5: "Optimal approach, best practices followed"
      4: "Good approach, reasonable choices"
      3: "Acceptable approach, some suboptimal choices"
      2: "Poor approach, many questionable choices"
      1: "Wrong approach entirely"

  - name: format
    weight: 0.15
    criteria:
      5: "Perfect format compliance"
      4: "Mostly follows format"
      3: "Some format deviations"
      2: "Significant format issues"
      1: "Ignores format requirements"
```

## Calibration

### Inter-Rater Agreement

When multiple evaluators (human or LLM):

1. **Train on examples** - All evaluators score same examples first
2. **Discuss disagreements** - Align on criteria interpretation
3. **Calculate agreement** - Target Cohen's kappa > 0.7
4. **Recalibrate** - Adjust rubric if agreement is low

### LLM Judge Calibration

```yaml
calibration_set:
  - input: "Example input 1"
    output: "Example output 1"
    expected_scores:
      accuracy: 5
      completeness: 4
      clarity: 4

  - input: "Example input 2"
    output: "Example output 2"
    expected_scores:
      accuracy: 2
      completeness: 3
      clarity: 4
```

Run calibration before production evaluation:
```
If |judge_score - expected| > 1 for >20% of cases:
  → Rubric needs clarification
  → Or judge prompt needs improvement
```

## Common Mistakes

### 1. Vague Criteria

**Bad**:
```yaml
5: "Good"
3: "Okay"
1: "Bad"
```

**Good**:
```yaml
5: "All requirements met with no errors"
3: "Most requirements met, 1-2 minor issues"
1: "Fails to meet core requirements"
```

### 2. Overlapping Dimensions

**Bad**:
```yaml
- name: clarity
- name: readability  # Overlaps with clarity
- name: understandability  # Also overlaps
```

**Good**:
```yaml
- name: clarity  # Single dimension covering readability
```

### 3. Uneven Weights

**Bad**:
```yaml
- name: format
  weight: 0.50  # Too high for formatting
- name: accuracy
  weight: 0.10  # Too low for accuracy
```

**Good**:
```yaml
- name: accuracy
  weight: 0.35
- name: format
  weight: 0.10
```

### 4. Missing Anchors

**Bad**:
```yaml
5: "Excellent"
4: "Good"
# No examples of what excellent/good means
```

**Good**:
```yaml
5:
  description: "Excellent"
  example: "Returns valid JSON with all fields populated..."
```

---

*Well-designed rubrics are essential for consistent, meaningful evaluation*
