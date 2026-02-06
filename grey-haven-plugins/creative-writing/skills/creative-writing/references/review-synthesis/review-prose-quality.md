# Review: Prose Quality

| Field | Value |
|-------|-------|
| **Agent** | prose-style-analyst |
| **Agent Type** | `creative-writing:writing-prose-style-analyst` |
| **Execution** | Parallel (simultaneous with editorial and dialogue reviewers) |
| **Focus** | Style, voice, quality, SVQ scoring, sentence architecture, diction, rhythm |

---

## Objectives

The prose-style-analyst examines the manuscript's craft at the sentence and paragraph level. Its primary output is an SVQ score that becomes the pre-revision baseline. Beyond scoring, it produces a detailed style profile and severity-tagged findings on prose quality.

### 1. SVQ Scoring

The cornerstone of the prose quality review. Score each dimension on the 1-10 scale:

- **S (Style)**: Sentence architecture, diction, prose density, figurative language. Does the prose have shape and texture? Are word choices precise or habitual?
- **V (Voice)**: Persona, attitude, distinctiveness, consistency. Does the prose sound like a specific writer, or could anyone have written it? Is voice sustained across the manuscript?
- **Q (Quality)**: Craft precision, clarity, economy, variety, control. Is the writing clean? Does it achieve its effects efficiently? Is there range in sentence construction?

**Composite SVQ** = (S + V + Q) / 3

This score becomes the baseline for any subsequent prose revision pipeline work.

### 2. Style Profile

A qualitative assessment of the manuscript's prose characteristics:

- **Sentence patterns**: Dominant sentence shapes, variety (or lack thereof), rhythm tendencies
- **Diction register**: Formal/informal range, vocabulary density, precision of word choice
- **Figurative language**: Metaphor frequency and quality, simile usage, imagery patterns
- **Prose density**: Ratio of showing to telling, compression vs. expansion, narrative pace at sentence level
- **Distinctive features**: What makes this writer's prose identifiable -- their signature moves

### 3. Severity-Tagged Findings

Every finding must be tagged with a severity level:

- **Critical**: Prose issues that break immersion or comprehension (e.g., sustained purple prose that obscures meaning, voice collapse across multiple chapters)
- **Major**: Craft weaknesses a reader would feel even if they cannot name (e.g., monotonous sentence rhythm, over-reliance on a single figurative pattern)
- **Minor**: Craft opportunities that would elevate already-functional prose (e.g., occasional weak verb choice, paragraph that could be tighter)
- **Note**: Observations about style that are not problems (e.g., "the author's em-dash usage is a deliberate stylistic signature, not a tic")

### 4. Pattern Analysis

Identify recurring prose patterns across the manuscript:

- **Verbal tics**: Habitual words or constructions that appear disproportionately
- **Sentence shape repetition**: Consistent default sentence structures (e.g., always opening with a participial phrase)
- **Metaphor domain drift**: Characters whose figurative language does not stay consistent with their conceptual frame
- **Energy distribution**: Where the prose is most alive vs. where it goes flat

---

## Agent Prompt Template

Use the following prompt when dispatching the prose-style-analyst for the review synthesis pipeline. Replace placeholder values with project-specific paths and content.

```markdown
# Prose Quality Review

You are performing the prose quality review portion of a parallel manuscript review.
Two other agents are reviewing the same manuscript simultaneously from different
angles (editorial and dialogue). Your findings will be synthesized with theirs.

## Inputs

- **Manuscript path**: {{MANUSCRIPT_PATH}}
- **Project config**: {{CONFIG_PATH}}

Read the project config first. It contains character information, POV conventions,
and the author's known strengths and weaknesses.

## YOUR ROLE: REVIEW ONLY -- NO EDITS

You are scoring, profiling, and diagnosing. You do not modify the manuscript. Your
output is a structured prose quality assessment.

## Instructions

Read the full manuscript. Then produce a report covering:

### 1. SVQ Scoring

Score each dimension with evidence:

- **S (Style)** [1-10]: Sentence architecture, diction, prose density, figurative
  language. Quote 2-3 passages that exemplify the score.
- **V (Voice)** [1-10]: Persona, attitude, distinctiveness, consistency. Quote
  passages showing voice at its strongest and weakest.
- **Q (Quality)** [1-10]: Craft precision, clarity, economy, variety, control.
  Quote passages demonstrating the score.
- **Composite SVQ**: (S + V + Q) / 3

### 2. Style Profile

Characterize the manuscript's prose:

- Dominant sentence patterns and variety
- Diction register and vocabulary range
- Figurative language usage (frequency, quality, patterns)
- Prose density and showing/telling balance
- Distinctive features (the writer's signature moves)

### 3. Severity-Tagged Findings

For each finding, provide:
- **Location**: Chapter and approximate position
- **Severity**: Critical / Major / Minor / Note
- **Category**: Sentence architecture / Diction / Voice / Rhythm / Figurative language / Economy
- **Description**: What the issue is, with quoted evidence
- **Recommendation**: What the author should consider

### 4. Pattern Analysis

Identify manuscript-wide patterns:
- Verbal tic candidates (with frequency counts)
- Recurring sentence shapes
- Metaphor domain consistency per POV character
- Energy map (strongest and weakest prose sections)

### 5. Summary

- SVQ score with brief justification for each dimension
- Total findings by severity (Critical: X, Major: X, Minor: X, Note: X)
- Top 3 prose-level priorities for revision
- Overall craft assessment (1-2 paragraphs)
```

---

## Phase Checklist

Before submitting the prose quality review report, verify:

- [ ] Full manuscript has been read (not just sampled)
- [ ] SVQ score has all three dimensions with quoted evidence
- [ ] Composite SVQ has been calculated
- [ ] Style profile covers sentence patterns, diction, figurative language, density, and distinctive features
- [ ] Every finding has location, severity, category, and description with quoted evidence
- [ ] Severity tags follow the standard definitions (Critical/Major/Minor/Note)
- [ ] Pattern analysis includes verbal tic candidates with frequency data
- [ ] Pattern analysis covers metaphor domain consistency per POV character
- [ ] Energy map identifies strongest and weakest prose sections
- [ ] Report includes summary with SVQ justification and top priorities
- [ ] No edits were made to the manuscript
- [ ] Report is structured for synthesis (consistent format, severity tags, clear locations)

---

## Common Pitfalls

### Scoring Without Evidence

An SVQ score without quoted passages is an opinion, not an assessment. Every dimension score must be grounded in specific textual evidence. The synthesis protocol needs to compare the prose-style-analyst's evidence against the other reviewers' findings -- unsupported scores cannot be cross-referenced.

### Confusing Complexity with Quality

Dense, ornate prose is not automatically higher quality than spare, clean prose. The Quality dimension measures craft control -- how well the writer achieves their intended effect -- not how many literary devices per paragraph. A minimalist style executed with precision scores higher than a baroque style that loses control.

### Ignoring Voice Consistency Across POV Characters

The Voice dimension applies per-character in multi-POV manuscripts. A manuscript can have strong voice for one POV character and weak voice for another. Report Voice scores per character when they differ significantly, and flag transitions where voice blurs between characters.

### Over-Counting Stylistic Signatures as Tics

Not every repeated pattern is a verbal tic. If the author uses em-dashes frequently but each use serves a clear rhythmic purpose, that is a stylistic signature, not a tic. The distinction: tics are unconscious and habitual; signatures are deliberate and functional. Tag signatures as Notes, not findings.

### Letting the Energy Map Become a Plot Summary

The energy map tracks prose quality, not narrative excitement. A quiet, introspective scene can have the most alive prose in the manuscript. A dramatic action sequence can have flat, functional writing. Map craft energy, not plot energy.

---

*Style is not decoration. It is the writer's fingerprint on every sentence.*
