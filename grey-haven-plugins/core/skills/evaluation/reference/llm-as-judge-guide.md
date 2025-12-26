# LLM-as-Judge Guide

Using LLMs to evaluate LLM outputs systematically.

## The Pattern

```
┌─────────────────────────────────────────────────────────┐
│                   Evaluation Flow                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Input ──▶ Test LLM ──▶ Output                          │
│                            │                             │
│                            ▼                             │
│              ┌─────────────────────────┐                │
│              │     Judge LLM Call      │                │
│              │   - Original input      │                │
│              │   - Generated output    │                │
│              │   - Rubric criteria     │                │
│              │   - (Optional: ground   │                │
│              │     truth)              │                │
│              └─────────────────────────┘                │
│                            │                             │
│                            ▼                             │
│              ┌─────────────────────────┐                │
│              │   Structured Scores     │                │
│              │   - Per dimension       │                │
│              │   - With justification  │                │
│              └─────────────────────────┘                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Model Selection

### Judge Model Recommendations

| Test Model | Judge Model | Rationale |
|------------|-------------|-----------|
| Haiku | Sonnet | Cost-effective, good judgment |
| Sonnet | Opus or Sonnet | Opus for critical, Sonnet for routine |
| Opus | Opus | Self-evaluation or human review |

### Key Principle

**Use a stronger model as judge** when possible. Judges need to recognize quality they might not produce themselves.

## Judge Prompt Template

### Basic Template

```
You are an expert evaluator. Assess the following output based on the given rubric.

## Original Input
{input}

## Output to Evaluate
{output}

## Rubric
{rubric}

## Instructions
For each dimension in the rubric:
1. Assign a score (1-5)
2. Provide brief justification (1-2 sentences)

I will parse this programmatically. Respond with valid JSON:
{
  "scores": {
    "dimension_name": {
      "score": 1-5,
      "justification": "Brief explanation"
    }
  },
  "overall_score": weighted average,
  "summary": "One sentence overall assessment"
}
```

### With Ground Truth

```
You are an expert evaluator comparing output to a reference answer.

## Original Input
{input}

## Reference Answer (Ground Truth)
{ground_truth}

## Output to Evaluate
{output}

## Rubric
{rubric}

## Instructions
Compare the output to the reference answer and score each dimension.
Note: The output doesn't need to match exactly - it should achieve the same goals.

[Same JSON format as above]
```

### Pairwise Comparison

```
You are an expert evaluator comparing two outputs.

## Original Input
{input}

## Output A
{output_a}

## Output B
{output_b}

## Rubric
{rubric}

## Instructions
For each dimension, determine which output is better or if they're equal.

I will parse this programmatically. Respond with valid JSON:
{
  "comparisons": {
    "dimension_name": {
      "winner": "A" | "B" | "tie",
      "justification": "Brief explanation"
    }
  },
  "overall_winner": "A" | "B" | "tie",
  "summary": "One sentence comparison"
}
```

## Handling Non-Determinism

### Strategy 1: Multiple Judge Runs

```python
def evaluate_with_consensus(output: str, rubric: dict, runs: int = 3) -> dict:
    scores = []
    for _ in range(runs):
        score = judge_evaluate(output, rubric)
        scores.append(score)

    # Aggregate
    return {
        "mean_score": mean(s["overall_score"] for s in scores),
        "std_dev": std(s["overall_score"] for s in scores),
        "consensus": mode(s["verdict"] for s in scores),
        "all_runs": scores
    }
```

### Strategy 2: Temperature Control

```python
# For reproducible judgments
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    temperature=0,  # Deterministic
    messages=[{"role": "user", "content": judge_prompt}]
)
```

### Strategy 3: Confidence Thresholds

```python
def evaluate_with_confidence(output: str, rubric: dict) -> dict:
    result = judge_evaluate(output, rubric)

    # Flag low-confidence cases for human review
    if result["score_variance"] > 0.5:
        result["needs_human_review"] = True
        result["review_reason"] = "High score variance across dimensions"

    return result
```

## Bias Mitigation

### Position Bias

In pairwise comparisons, LLMs may favor the first option.

**Mitigation**: Run twice with swapped positions:

```python
def unbiased_comparison(output_a: str, output_b: str) -> str:
    result1 = compare(a=output_a, b=output_b)  # A first
    result2 = compare(a=output_b, b=output_a)  # B first

    # If results disagree, it's a tie
    if result1["winner"] == "A" and result2["winner"] == "A":
        return "B"  # B won when it was second in both
    elif result1["winner"] == "B" and result2["winner"] == "B":
        return "A"  # A won when it was second in both
    else:
        return "tie"
```

### Length Bias

Longer outputs often score higher even when unnecessary.

**Mitigation**: Include conciseness in rubric with appropriate weight.

### Self-Preference Bias

Models may prefer outputs similar to their own style.

**Mitigation**: Use different model families when possible (e.g., Claude judging GPT).

## Implementation Example

### Python Implementation

```python
from anthropic import Anthropic
from pydantic import BaseModel

class DimensionScore(BaseModel):
    score: int
    justification: str

class EvaluationResult(BaseModel):
    scores: dict[str, DimensionScore]
    overall_score: float
    summary: str

def evaluate_output(
    input_text: str,
    output_text: str,
    rubric: dict,
    model: str = "claude-sonnet-4-20250514"
) -> EvaluationResult:
    client = Anthropic()

    prompt = f"""You are an expert evaluator.

## Original Input
{input_text}

## Output to Evaluate
{output_text}

## Rubric
{format_rubric(rubric)}

Score each dimension 1-5 with justification.
Return valid JSON matching this schema:
{{
  "scores": {{"dimension": {{"score": int, "justification": str}}}},
  "overall_score": float,
  "summary": str
}}"""

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    return EvaluationResult.model_validate_json(
        extract_json(response.content[0].text)
    )
```

### TypeScript Implementation

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

const EvaluationResultSchema = z.object({
  scores: z.record(z.object({
    score: z.number().min(1).max(5),
    justification: z.string()
  })),
  overall_score: z.number(),
  summary: z.string()
});

async function evaluateOutput(
  input: string,
  output: string,
  rubric: Rubric,
  model = "claude-sonnet-4-20250514"
): Promise<z.infer<typeof EvaluationResultSchema>> {
  const client = new Anthropic();

  const prompt = `You are an expert evaluator...`;  // Same as Python

  const response = await client.messages.create({
    model,
    max_tokens: 1024,
    temperature: 0,
    messages: [{ role: "user", content: prompt }]
  });

  const json = extractJson(response.content[0].text);
  return EvaluationResultSchema.parse(JSON.parse(json));
}
```

## Cost Considerations

| Evaluation Type | Tokens/Eval | Cost (Sonnet) | Cost (Opus) |
|-----------------|-------------|---------------|-------------|
| Single dimension | ~500 | ~$0.004 | ~$0.02 |
| Full rubric (5 dim) | ~1000 | ~$0.008 | ~$0.04 |
| Pairwise comparison | ~1500 | ~$0.012 | ~$0.06 |
| With ground truth | ~1200 | ~$0.010 | ~$0.05 |

**At scale** (1000 evaluations):
- Sonnet: $8-12
- Opus: $40-60

---

*LLM-as-judge enables scalable, consistent evaluation when properly calibrated*
