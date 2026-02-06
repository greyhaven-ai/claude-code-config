# Audit: Prose Quality Assessment

| Field | Value |
|-------|-------|
| **Agent** | prose-style-analyst (`creative-writing:writing-prose-style-analyst`) |
| **Execution** | Parallel -- runs simultaneously with believability and world-consistency audits |
| **Mode** | Audit only -- scoring and assessment, not revision |
| **Output** | SVQ score (Style/Voice/Quality) plus style profile |

---

## Objectives

The prose-style-analyst in audit mode evaluates the craft quality of the manuscript through the SVQ scoring framework. This is assessment, not revision -- the agent scores, profiles, and reports. It does not suggest rewrites or make edits. Findings feed into the synthesis protocol where the audit lead cross-references them with believability and world consistency results.

### 1. Style Assessment

Evaluate sentence-level architecture and diction:

- **Sentence variety**: Mix of lengths, structures, and rhythms. Flag monotonous stretches where every sentence follows the same pattern.
- **Diction**: Word choices are precise, evocative, and appropriate to the narrative register. Flag generic or imprecise language.
- **Prose density**: Information per sentence is well-calibrated -- neither bloated nor skeletal.
- **Figurative language**: Metaphors, similes, and imagery are fresh, consistent with character domains, and load-bearing (not decorative).

### 2. Voice Assessment

Evaluate persona, attitude, and consistency:

- **Persona**: The narrative voice has a recognizable identity that persists across the manuscript.
- **Attitude**: The narrator's relationship to the material (ironic, intimate, detached, urgent) is clear and sustained.
- **Distinctiveness**: POV characters sound different from each other in narration, not just in dialogue.
- **Consistency**: Voice does not drift between chapters or lose its character under pressure (action scenes, emotional peaks).

### 3. Quality Assessment

Evaluate craft precision and control:

- **Clarity**: The reader always knows what is happening, who is speaking, and where they are.
- **Economy**: Every sentence earns its place. No redundancy, no over-explanation, no closing spirals.
- **Variety**: The manuscript avoids repetitive patterns at every level -- word, sentence, paragraph, scene.
- **Control**: The author demonstrates intentional choices rather than habitual patterns. Stylistic risks (fragments, run-ons, unconventional punctuation) are deliberate and effective.

---

## Agent Prompt Template

```
You are performing a prose quality audit as part of a manuscript audit team.
Three agents (including you) are auditing this manuscript simultaneously.
Your findings will be synthesized with believability and world consistency
results to produce an overall quality decision.

MANUSCRIPT PATH: {{MANUSCRIPT_PATH}}
CONFIG PATH: {{CONFIG_PATH}}

## YOUR ROLE: AUDIT ONLY -- NO EDITS

You are scoring and profiling. You do not modify the manuscript. You do not
suggest specific rewrites. Your output is an SVQ score with a detailed
style profile.

## Tasks

### 1. SVQ Scoring

Read the manuscript and score each dimension on a 1-10 scale:

- **S (Style)**: Sentence architecture, diction, prose density, figurative
  language. Evaluate variety, precision, and calibration.
- **V (Voice)**: Persona, attitude, distinctiveness, consistency. Evaluate
  whether the narrative voice is identifiable and sustained.
- **Q (Quality)**: Craft precision, clarity, economy, variety, control.
  Evaluate whether every sentence earns its place.

**Composite SVQ** = (S + V + Q) / 3

| Composite | Interpretation |
|-----------|---------------|
| 9-10 | Publication-ready, exceptional craft |
| 7-8 | Strong work, minor polish needed |
| 5-6 | Solid foundation, revision opportunities |
| 3-4 | Significant development needed |
| 1-2 | Fundamental craft work required |

For each dimension, provide:
- The numeric score
- A 2-3 sentence justification
- One quoted passage that exemplifies the score (strong or weak)

### 2. Style Profile

Characterize the manuscript's prose style:

- **Sentence length distribution**: Short/medium/long ratio. Flag if
  heavily skewed toward one length.
- **Paragraph rhythm**: How paragraphs build and release tension. Flag
  if monotonous.
- **Diction register**: Formal, conversational, lyrical, spare, dense.
  Note any shifts between registers and whether they are intentional.
- **Signature patterns**: Recurring techniques the author uses well
  (or overuses). Em-dash frequency, fragment usage, list structures,
  parallel constructions.

### 3. Voice Differentiation Check

If the manuscript has multiple POV characters:

- Evaluate whether each POV character's narration sounds distinct
- Identify specific markers that differentiate voices (vocabulary,
  sentence rhythm, metaphor domain, thought patterns)
- Flag any POV characters whose voices blur together
- Note chapters or sections where voice is strongest and weakest

### 4. Craft Observations

Note significant patterns that affect overall quality:

- **Verbal tics**: Repeated words or constructions that suggest habit
  rather than intention (with counts and density)
- **Over-explanation**: Passages that tell what was already shown
- **Under-writing**: Passages that need more grounding, sensory detail,
  or emotional specificity
- **Pacing indicators**: Sections that drag (over-described) or rush
  (under-developed)

### 5. Report

Produce a structured report:

1. **SVQ Score**: Composite and individual dimensions with justification
2. **Style Profile**: Characterization of the manuscript's prose identity
3. **Voice Report**: Differentiation assessment (if multiple POVs)
4. **Strengths**: What the prose does well (with quoted evidence)
5. **Opportunities**: Patterns that could be improved (with quoted evidence)
6. **Craft Observations**: Tic counts, pacing notes, economy assessment

For each observation, note the chapter/section location so the audit lead
can cross-reference with findings from the other two auditors.
```

---

## Phase Checklist

Before marking the prose quality audit complete, verify:

- [ ] Full manuscript has been read and evaluated
- [ ] Style scored (1-10) with justification and quoted evidence
- [ ] Voice scored (1-10) with justification and quoted evidence
- [ ] Quality scored (1-10) with justification and quoted evidence
- [ ] Composite SVQ calculated
- [ ] Style profile produced (sentence lengths, paragraph rhythm, diction, signatures)
- [ ] Voice differentiation checked across POV characters (if applicable)
- [ ] Verbal tic counts and densities recorded
- [ ] Craft observations documented with chapter/section locations
- [ ] Report is structured and ready for synthesis
- [ ] **No edits were made to the manuscript**

---

## Common Pitfalls

**Scoring style preferences as quality deficits.** Spare, minimalist prose is not inherently lower quality than lush, lyrical prose. The SVQ framework measures craft within the author's chosen register, not adherence to a preferred style. A Hemingway-influenced manuscript scores high on Quality if its economy is precise and intentional, even if the Style score reflects a deliberately narrow palette.

**Conflating voice consistency with voice quality.** A consistent voice that is flat and generic should not score high on Voice simply because it does not waver. Consistency is necessary but not sufficient -- the voice must also be distinctive and purposeful.

**Over-counting intentional repetition as tics.** Authors sometimes repeat words or structures for rhythmic, thematic, or emphatic effect. Before counting a repetition as a verbal tic, check whether it serves a craft purpose. Anaphora is a technique, not a tic.

**Letting a strong opening bias the full score.** Manuscripts often have their strongest prose in the opening chapters (most revised) and their weakest in the middle (least revised). Score the whole manuscript, not just the sections that made the strongest first impression. Sample from the opening, middle, and closing sections at minimum.

**Providing revision suggestions instead of assessment.** The audit agent scores and reports. It does not say "change this sentence to..." or "consider rephrasing..." Revision is a separate pipeline with its own agents. The audit's job is to describe the current state with evidence, not to prescribe fixes.

---

*The analyst's craft is seeing clearly. The reviser's craft is acting on what was seen.*
