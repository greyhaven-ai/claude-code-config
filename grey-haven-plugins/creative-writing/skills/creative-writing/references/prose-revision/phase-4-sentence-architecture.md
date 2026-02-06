# Phase 4: Sentence Architecture

| Field | Value |
|-------|-------|
| **Phase** | 4 |
| **Name** | Sentence Architecture |
| **Agent** | prose-style-analyst (`creative-writing:writing-prose-style-analyst`) |
| **Expected Delta** | -2% to +2% |

---

## Objectives

Phase 4 shifts from cutting to refinement. The manuscript has been tightened through three passes of deletion; now it needs its sentence-level craft polished. This phase uses the prose-style-analyst rather than the editor-reviewer because the work is analytical -- examining patterns, measuring densities, evaluating shapes -- rather than editorial.

The expected delta is near-zero. This phase replaces and reshapes rather than adds or removes. The word count should barely move.

1. **Reduce em-dash density.** Em-dashes are powerful punctuation -- when used sparingly. Overuse flattens their impact until they become visual noise. Target: a maximum of 2 em-dashes per page (approximately 250 words). Where em-dashes exceed this density, evaluate each one. Replace with commas, colons, semicolons, periods, or parentheses as the rhythm demands. Do not eliminate all em-dashes; eliminate the ones that have stopped earning their keep.

2. **Replace remaining perception verbs.** Phase 2 targeted the obvious filter words (saw, heard, felt, noticed, realized). Phase 4 catches the survivors and the subtler variants: "watched as," "could see that," "was aware of," "sensed that." Replace these with direct sensory presentation. Not "She noticed the light had changed" but "The light had changed." Not "He could hear footsteps" but "Footsteps echoed down the corridor."

3. **Vary sentence shapes.** Analyze sentence openings, lengths, and structures. Flag sequences where three or more consecutive sentences share the same opening pattern (subject-first, participial phrase, "The," a character name). Flag sequences where sentence length varies by fewer than 5 words across 4+ sentences. Reshape these passages to create rhythmic variety -- short sentences for impact, long sentences for immersion, varied openings to prevent monotony.

4. **Refine character-specific metaphors.** Each POV character should perceive the world through their own conceptual domain (defined in the project config). Audit figurative language to ensure metaphors and similes align with the character whose perspective is active. A musician should not think in architectural metaphors unless there is a deliberate reason. Replace misaligned figurative language with domain-consistent alternatives that preserve the original meaning and emotional register.

---

## Agent Prompt Template

```markdown
You are performing Phase 4 (Sentence Architecture) of the prose revision pipeline.

**Manuscript**: {{BOOK_PATH}}
**Project Config**: {{CONFIG_PATH}}
**Character Domains**: {{CHARACTER_DOMAINS}}
**Metaphor Patterns**: {{METAPHOR_PATTERNS}}

## Your Mission

Examine the prose at the sentence level and make targeted refinements to architecture, rhythm, and figurative language. This is analytical work -- you are identifying patterns and correcting misalignments, not rewriting for style preference.

### Analysis 1: Em-Dash Density

Scan the manuscript for em-dash usage. Calculate density per page (~250 words). Where density exceeds 2 per page:
- Evaluate each em-dash in the passage
- Keep the ones that create genuine interruption, dramatic pause, or appositive emphasis
- Replace the rest with the punctuation that best serves the sentence's rhythm:
  - Comma for light pauses
  - Colon for introduction/explanation
  - Semicolon for balanced clauses
  - Period for full stops that add weight
  - Parentheses for true asides

### Analysis 2: Remaining Perception Verbs

Search for filter words and perception verb constructions that survived Phase 2:
- "watched as," "could see," "could hear," "was aware of," "sensed that," "realized that"
- Constructions where the POV character is placed between the reader and the experience
- Replace with direct sensory presentation: remove the character as intermediary

### Analysis 3: Sentence Shape Variation

Analyze sentence patterns across each chapter:
- **Opening patterns**: Flag 3+ consecutive sentences starting the same way
- **Length uniformity**: Flag 4+ consecutive sentences within 5 words of the same length
- **Structure repetition**: Flag passages locked into the same sentence type (all simple, all compound)
- Reshape flagged passages to create rhythmic variety while preserving meaning and voice

### Analysis 4: Character Metaphor Consistency

For each POV section, cross-reference figurative language against the character's conceptual domain:
- Identify metaphors/similes that belong to a different character's domain
- Replace with domain-consistent alternatives that carry the same emotional weight
- Preserve any deliberate cross-domain metaphors (where a character is consciously adopting another's worldview)

## Rules

- **Refine, do not rewrite.** Your changes should be surgical -- a word here, punctuation there, a sentence restructured. If you are rewriting entire paragraphs, you have exceeded scope.
- **Near-zero word count delta.** Replacements, not additions or deletions. The word count should shift by no more than +/- 2%.
- **Preserve voice.** Sentence architecture changes must sound like the writer, not like a style-correcting algorithm.
- **Trust the earlier phases.** Do not re-litigate Phase 1-3 decisions. If something feels over-explained, it was left intentionally.
- **Commit nothing.** The pipeline orchestrator handles git operations.

## Output

When complete, report:
1. Em-dash density: before and after (manuscript-wide average per page)
2. Perception verbs replaced (count and examples)
3. Sentence pattern issues found and resolved (count per chapter)
4. Metaphor realignments made (list with character, original, replacement)
5. Word count delta (should be near zero)
6. Assessment: is the manuscript ready for SVQ checkpoint scoring?
```

---

## Phase Checklist

- [ ] Cumulative word count delta checked -- if already at 30% ceiling, skip any cutting and focus on reshaping only
- [ ] Em-dash density analyzed across full manuscript
- [ ] Em-dash density reduced to maximum 2 per page where exceeding threshold
- [ ] Remaining perception verbs identified and replaced with direct sensory presentation
- [ ] Sentence opening patterns analyzed -- no 3+ consecutive same-pattern openings remain
- [ ] Sentence length variation analyzed -- no 4+ consecutive uniform-length sequences remain
- [ ] Character metaphors audited against domain map from project config
- [ ] Misaligned metaphors replaced with domain-consistent alternatives
- [ ] Deliberate cross-domain metaphors preserved (verified as intentional)
- [ ] Word count delta recorded and within expected range (-2% to +2%)
- [ ] SVQ checkpoint scoring performed (Phase 4 is a scoring checkpoint)
- [ ] SVQ scores recorded and compared against Phase 2 baseline -- must not have dropped
- [ ] Git commit created: `revision: phase 4 sentence-architecture complete - <book>`

---

## Common Pitfalls

### Rewriting Instead of Refining

The prose-style-analyst agent has deep knowledge of what "good prose" looks like, which creates a temptation to rewrite passages in a more polished style. This destroys voice. Phase 4 changes should be invisible to a casual reader -- the prose should feel like itself, only smoother. If a before/after comparison of a paragraph shows more than 3-4 word-level changes, the edit has gone too far. Pull back.

### Eliminating All Em-Dashes

The goal is density reduction, not elimination. Em-dashes serve real purposes: they create dramatic interruption, set off appositives with more emphasis than commas, and signal a shift in thought mid-sentence. A manuscript with zero em-dashes has lost a useful tool. The target is restraint, not absence. Keep the em-dashes that earn their visual weight; replace only the ones that have become a default punctuation habit.

### Over-Homogenizing Sentence Length

"Variety" does not mean mechanical alternation (short-long-short-long). Natural prose has clusters -- a run of short punchy sentences during action, a long flowing sentence that carries a description, a medium-paced sequence for dialogue. The goal is to break monotonous sequences, not to impose an artificial pattern. After reshaping, read the passage aloud. If it sounds like a metronome, the variety is itself monotonous.

### Metaphor Over-Correction

Not every figurative expression needs to map perfectly to a character's domain. Common metaphors ("a wave of relief," "the weight of silence") are invisible to readers regardless of whose POV they appear in. Reserve domain-correction for distinctive, extended, or vivid metaphors -- the ones that actually shape how the reader perceives the character's mind. Over-correcting everyday figurative language makes the domain system feel forced rather than organic.

### Ignoring the SVQ Checkpoint

Phase 4 is a scoring checkpoint. Do not skip the SVQ assessment. The checkpoint after Phase 4 compares against the Phase 2 baseline and determines whether the cutting phases (1-4) have improved prose quality. A drop in SVQ at this checkpoint signals that refinement has damaged something -- investigate before proceeding to Phase 5.

---

*The architecture of a sentence is the architecture of thought -- reshape the container and you reshape the meaning.*
