# Phase 2: Prose Craft

| Field | Value |
|-------|-------|
| **Phase** | 2 of 6 |
| **Name** | Prose Craft |
| **Agent** | editor-reviewer (`creative-writing:writing-editor-reviewer`) |
| **Expected Word Count Delta** | -5% to -15% |

---

## Objectives

Phase 2 is the deepest cutting phase in the pipeline. Where Phase 1 hunted mechanical patterns, Phase 2 addresses craft -- the difference between competent prose and prose that lives on the page. This phase requires judgment, not just pattern-matching.

### 1. Replace Perception Verbs with Direct Sensory Language

Perception verbs ("she saw," "he heard," "she noticed," "she felt," "he realized") insert the narrator between the reader and the experience. They tell the reader that a character perceived something instead of letting the reader perceive it directly.

- **Before**: "She saw the candle flicker in the window."
- **After**: "The candle flickered in the window."

- **Before**: "He heard footsteps on the stairs."
- **After**: "Footsteps on the stairs."

- **Before**: "She noticed the room had gone quiet."
- **After**: "The room had gone quiet."

The deep POV principle: if the reader is inside a character's head, everything on the page is already what that character perceives. The verb is redundant.

**Exception**: Perception verbs earn their place when the act of perceiving is itself the point -- when a character strains to hear, when noticing something is a revelation, when the gap between seeing and understanding matters.

### 2. Cut Over-Explanation

Over-explanation is the prose equivalent of explaining the joke. It occurs when the text does not trust the reader to connect the dots. Common forms:

- Narration that interprets a character's own actions ("She slammed the door. She was angry.")
- Dialogue followed by narration restating what the dialogue already communicated
- Subtext made text -- a meaningful silence explained, a loaded glance annotated
- Thematic statements that tell the reader what the scene means

**Fix**: Delete the explaining layer. If the showing is strong enough, the telling is redundant. If the showing is not strong enough, the fix is to strengthen the showing -- not to add explanation.

### 3. Add Sentence Variety

Monotonous rhythm lulls readers out of the prose. Check for:

- **Same-length sentences** in sequence (five medium sentences in a row)
- **Same-structure openings** (Subject-verb-object, Subject-verb-object, Subject-verb-object)
- **Missing fragments** -- sometimes a fragment lands harder than a full sentence
- **Missing long sentences** -- a well-constructed long sentence with internal rhythm creates a different reading experience than a string of short ones

Vary the architecture. Short. Then long, winding, building toward something the reader can feel gathering momentum before it lands. Then short again.

### 4. Inject Counterpoints Where Missing

A counterpoint is a moment that cuts against the prevailing emotional current. Prose without counterpoints becomes monotone:

- An entirely bleak scene needs one small grace note
- An entirely warm scene needs one edge of unease
- An entirely tense scene needs one beat of absurdity or tenderness

Counterpoints are not additions of new material. They are reframings: taking an existing detail and letting it cut a different direction. A character in grief who notices something absurd. A happy moment undercut by a detail that reminds the reader what is at stake.

### 5. Strengthen Metaphors

Weak metaphors dilute prose. Check for:

- **Dead metaphors**: So familiar they have lost their image ("heart of gold," "boiling with rage")
- **Mixed metaphors**: Two incompatible images colliding ("We need to get our ducks in a row before the ship sails")
- **Vague metaphors**: Images that gesture at meaning without landing ("It was like something had changed")
- **Domain violations**: A character using metaphors from another character's conceptual frame

**Fix**: Either sharpen the metaphor to make it vivid and specific, or cut it entirely. A direct statement beats a weak metaphor every time.

### 6. Convert Telling to Showing

Identify passages where the prose tells the reader about an emotion, state, or quality instead of rendering it through action, dialogue, sensory detail, or implication.

- **Before**: "He was exhausted."
- **After**: "He dropped into the chair and missed, catching himself on the armrest."

- **Before**: "The city was dangerous."
- **After**: "Three locks on every door, and still people slept with knives under their pillows."

Not all telling is bad -- see the editor-reviewer agent's guidelines on when telling works (transitions, pacing, minor details). The goal is to convert the high-impact telling passages where showing would land harder.

---

## Agent Prompt Template

Use the following prompt when dispatching the editor-reviewer agent for Phase 2. Replace placeholder values with project-specific paths and content.

```markdown
# Phase 2: Prose Craft

You are performing Phase 2 of the prose revision pipeline. Phase 1 (surface cleanup) is complete. Your scope is prose craft: making the writing vivid, direct, varied, and trusting of the reader. Do not address sentence architecture or enrichment -- those are later phases.

## Inputs

- **Manuscript path**: {{BOOK_PATH}}
- **Project config**: {{CONFIG_PATH}}

Read the project config first. It contains character domains, sensory preferences, and POV conventions.

## Character Domains and Metaphor Patterns

{{CHARACTER_DOMAINS}}

Reference metaphor patterns:
{{METAPHOR_PATTERNS}}

## Instructions

Read every chapter in the manuscript directory sequentially. For each chapter, make the following passes:

### Pass 1: Perception Verb Replacement

Find every instance of perception verbs: saw, heard, felt, noticed, realized, watched, observed, sensed, smelled, tasted. For each one:
- If the character is in deep POV, remove the perception verb and present the sensory experience directly.
- If the act of perceiving is itself meaningful (straining to hear, sudden noticing as revelation), keep the verb.
- Do not add new sensory detail. Rephrase to let the existing detail speak for itself.

### Pass 2: Over-Explanation Cuts

Find passages where the prose explains what it has already shown:
- Narration interpreting a character's visible action or dialogue
- Subtext made explicit
- Thematic statements telling the reader what to think
- Emotional labels after a scene has already rendered the emotion

Cut the explaining layer. If the showing is insufficient without the explanation, flag it with `<!-- NEEDS-STRONGER-SHOWING -->` for Phase 5 enrichment -- do not add material in this phase.

### Pass 3: Sentence Variety

Review paragraph rhythm. Where you find monotonous patterns:
- Break long sequences of same-length sentences by combining two into one longer sentence, or splitting one into a fragment and a sentence.
- Vary sentence openings -- not every sentence should begin with a subject.
- Use punctuation for rhythm: em-dashes for interruption, semicolons for balance, periods for finality.
- Do not manufacture artificial variety. The rhythm should serve the content.

### Pass 4: Counterpoint Check

Review emotional arcs within each scene. Where a scene runs on a single emotional frequency without relief:
- Find an existing detail that could be reframed to cut against the grain.
- Adjust phrasing to let the counterpoint emerge -- a word choice, a reordering, a juxtaposition.
- Counterpoints must be grounded in the POV character's perspective and domain. Do not insert authorial commentary.
- If no natural counterpoint exists and the scene genuinely needs one, flag it with `<!-- NEEDS-COUNTERPOINT -->` for Phase 5.

### Pass 5: Metaphor Audit

Review all figurative language:
- Replace dead metaphors with fresh, specific images drawn from the POV character's domain.
- Fix mixed metaphors by committing to one image.
- Cut vague metaphors that gesture without landing.
- Verify metaphor domains match the POV character (per project config).

### Pass 6: Telling to Showing Conversion

Identify high-impact telling passages -- emotional states, character descriptions, atmosphere -- where showing would be more powerful:
- Convert by rendering through action, sensory detail, or dialogue.
- Keep telling for transitions, minor details, and pacing beats where showing would slow the narrative.
- Conversions must stay within the scene's existing material. Rephrase and restructure, but do not invent new events or details.

## Rules

- **Edits only. No additions.** You may rephrase, restructure, cut, and convert. You may not add new scenes, characters, events, or plot points. Counterpoints and showing conversions use existing material.
- **Use MultiEdit for all changes.** Batch your edits per file.
- **Preserve the writer's voice.** Your job is to sharpen their voice, not replace it with yours.
- **Track your cuts.** After editing each chapter, note the approximate word count before and after.
- **Respect the 30% ceiling.** Check cumulative cuts (Phase 1 + Phase 2). If you approach 25%, reduce the aggressiveness of remaining cuts. If you reach 30%, stop cutting.
- **Commit nothing.** The pipeline orchestrator handles git commits.

## Output

After completing all chapters, provide a summary:

- Total chapters processed
- Approximate words removed (this phase only)
- Cumulative cut percentage (Phase 1 + Phase 2)
- Perception verbs removed vs. kept (with reasoning for kept instances)
- Over-explanation passages cut (with chapter locations)
- Sentence variety changes (notable examples)
- Counterpoints adjusted or flagged
- Metaphors replaced or cut (with examples)
- Telling-to-showing conversions (with examples)
- Flags placed for Phase 5 enrichment
```

---

## Phase Checklist

Verify all items before marking Phase 2 complete:

- [ ] Every chapter in the manuscript has been processed
- [ ] Perception verbs replaced with direct sensory language (deliberate uses retained)
- [ ] Over-explanation passages identified and cut
- [ ] Sentence variety improved -- no monotonous rhythm stretches remain
- [ ] Counterpoints checked in every scene; flags placed where needed
- [ ] Metaphors audited: dead metaphors replaced, mixed metaphors fixed, domains verified
- [ ] High-impact telling converted to showing
- [ ] Word count delta is within expected range (-5% to -15%)
- [ ] Cumulative cuts (Phase 1 + Phase 2) do not exceed 30%
- [ ] `<!-- NEEDS-STRONGER-SHOWING -->` flags placed where showing was insufficient
- [ ] `<!-- NEEDS-COUNTERPOINT -->` flags placed where scenes lack emotional relief
- [ ] No new scenes, events, or plot points were added
- [ ] All edits made via MultiEdit (no full-file rewrites)
- [ ] SVQ scoring performed (first scoring checkpoint)
- [ ] Git commit created: `revision: phase 2 prose-craft complete - <book>`

---

## Common Pitfalls

**Over-cutting leads to skeletal prose.** Phase 2 is the most aggressive cutting phase. It is easy to chase concision past the point of diminishing returns, producing prose that is technically tight but emotionally hollow. Lean prose is not the same as starved prose. If a paragraph feels emptied rather than sharpened, you have gone too far.

**Removing ALL perception verbs makes prose feel disconnected.** The deep POV principle is a guideline, not a law. A character who never "hears" or "sees" anything begins to feel disembodied. Keep perception verbs when the act of perceiving matters -- when a character strains, startles, or processes. The goal is to eliminate the reflexive, unconscious ones.

**Counterpoints need character grounding.** A counterpoint that comes from the author rather than the character breaks POV and feels imposed. The moment of levity in a dark scene must arise from how this specific character would perceive it, filtered through their domain and personality. Authorial counterpoints read as tonal whiplash.

**Manufacturing sentence variety creates worse problems than monotony.** Artificial variety -- fragments for the sake of fragments, long sentences for the sake of long sentences -- calls attention to itself. The reader should feel the rhythm shift without noticing it. If a revision reads as "writerly," it has overcorrected.

**Confusing subtext removal with over-explanation cutting.** Not all explicit statement is over-explanation. Sometimes a character's internal narration explicitly naming an emotion is the right choice for voice or pacing. The test is not "is this explicit?" but "has this already been shown?" Cut the redundant layer, not the first statement.

**Ignoring the cumulative cut ceiling.** Phase 2 can easily produce a -15% delta on its own. Combined with Phase 1's cuts, that may push cumulative reduction toward 25-30%. Track the running total. If Phase 1 cut -10%, Phase 2 should aim for -5% to -10% to stay under the ceiling, even if more could be cut. Leave headroom for Phases 3-4.

---

*Craft is not decoration. It is the difference between prose the reader endures and prose the reader inhabits.*
