# Phase 5: Enrichment

| Field | Value |
|-------|-------|
| **Phase** | 5 |
| **Name** | Enrichment |
| **Agent** | editor-reviewer (`creative-writing:writing-editor-reviewer`) |
| **Expected Delta** | +3% to +8% |
| **Mode** | ADDITIONS ONLY -- no deletions permitted |

---

## Objectives

Phase 5 reverses the direction of the pipeline. Phases 1-4 cut; Phase 5 adds. The manuscript has been stripped lean. Now it needs new muscle -- sensory texture, physical presence, and the small human details that make prose feel inhabited rather than summarized.

All additions must be inserted **between existing lines**. No existing text is modified or removed.

### 1. Sensory Anchoring

Ground abstract emotional or intellectual moments in physical sensation. When a character feels dread, the reader should taste metal or feel cold tile underfoot. Abstract states become concrete through the body.

- Identify passages where emotion is named but not felt
- Insert sensory details that externalize the internal state
- Anchor abstract moments to the POV character's primary and secondary senses (per config)

### 2. Counterpoints

Add moments where characters push back -- questioning, challenging, contradicting. Scenes where everyone agrees flatten tension. Counterpoints restore friction.

- Look for scenes where consensus arrives too easily
- Insert dialogue or internal objection that complicates the moment
- Ensure counterpoints come from character-consistent reasoning, not arbitrary disagreement

### 3. Body Moments

Add physical reactions, gestures, and unconscious movements. Characters exist in bodies. Without physicality, dialogue floats in white space and thought becomes disembodied.

- Insert body language between dialogue lines
- Add involuntary physical responses (breath catching, muscles tensing, hands moving without permission)
- Vary the body vocabulary -- avoid defaulting to the same gestures across characters

### 4. Dialogue Beats

Replace dialogue tags with action beats where appropriate. "She said" conveys attribution; a physical beat conveys attribution *and* character.

- Identify runs of dialogue with only said-tags or no beats at all
- Insert small actions between lines of dialogue
- Use beats that reveal character state rather than generic filler

### 5. Texture

Add specific details that make scenes feel lived-in. The scratch on a table. The particular brand of coffee. The way light falls at a specific time of day. Texture is the difference between a set and a place.

- Look for scenes that read as generic (a room, a street, a meal)
- Insert concrete, particular details drawn from the POV character's awareness
- Prefer details the character would actually notice given their background and domain

---

## Agent Prompt Template

```
You are performing Phase 5 (Enrichment) of the prose revision pipeline.

BOOK PATH: {{BOOK_PATH}}
CONFIG PATH: {{CONFIG_PATH}}
CHARACTER DOMAINS: {{CHARACTER_DOMAINS}}
SENSORY PREFERENCES: {{SENSORY_PREFERENCES}}

## CRITICAL CONSTRAINT: ADDITIONS ONLY

You must NOT delete or modify any existing text. Every edit in this phase is an
insertion. You are adding new material between existing lines.

Use MultiEdit to add without removing. Every edit operation must insert text --
never replace or delete.

If you encounter a line that needs rewording, SKIP IT. Rewording is modification,
not addition. Your only tool in this phase is the space between lines.

## What to Add

1. **Sensory anchoring**: Ground abstract moments in physical sensation. Use
   each POV character's primary and secondary senses from the config.

2. **Counterpoints**: Add pushback -- characters questioning, challenging,
   contradicting. Restore friction where consensus came too easily.

3. **Body moments**: Insert physical reactions, gestures, unconscious movements.
   Characters exist in bodies. Vary the vocabulary -- not every character
   clenches their jaw.

4. **Dialogue beats**: Replace silence between dialogue lines with small actions.
   Action beats convey attribution and character simultaneously.

5. **Texture**: Add specific, concrete details that make scenes feel inhabited.
   The details should align with what the POV character would notice.

## Constraints

- Target +3% to +8% word count growth. Do not exceed +8%.
- Additions must match the POV character's perception domain and sensory profile.
- Do not add new scenes, new plot points, or new characters.
- Do not rewrite existing sentences in your own voice.
- Every insertion should feel like it was always there -- invisible stitching.
- Commit after completing each chapter or section.

## Process

1. Read the config file at {{CONFIG_PATH}} for character domains and sensory
   preferences.
2. Work through each chapter sequentially.
3. For each chapter:
   a. Identify passages that are abstract, disembodied, or generic.
   b. Insert sensory, physical, and textural additions.
   c. Track word count growth -- stop if approaching +8%.
4. After all chapters, report total word count delta.
```

---

## Phase Checklist

Before marking Phase 5 complete, verify all of the following:

- [ ] Word count growth is between +3% and +8% relative to Phase 4 output
- [ ] Word count growth does not exceed +8% under any circumstances
- [ ] **No deletions occurred** -- diff shows only additions (lines added, no lines removed)
- [ ] All additions are insertions between existing lines, not replacements
- [ ] Sensory details align with each POV character's primary/secondary senses from the config
- [ ] Body moments use varied physical vocabulary (no repetitive tics across characters)
- [ ] Dialogue beats replace silence, not existing tags
- [ ] Texture details match what the POV character would plausibly notice
- [ ] Counterpoints arise from character-consistent reasoning
- [ ] No new scenes, plot points, or characters were introduced
- [ ] Each chapter/section was committed to git after completion
- [ ] The writer's voice has been preserved -- additions feel native to the prose

---

## Common Pitfalls

### Bloating Beyond the +8% Ceiling

Enrichment is additive by design, which makes overshoot the primary risk. Writers and agents alike tend to keep finding "one more place" that needs texture. Set a hard word-count checkpoint at the halfway mark. If growth is already at +5% with half the manuscript remaining, tighten the filter -- only add where the prose actively feels skeletal.

### Texture That Violates POV Awareness

A character who grew up in a landlocked farming village should not notice the specific species of seabird outside a coastal window unless the story has established that knowledge. Every sensory detail and texture addition must pass through the filter of what the POV character would plausibly perceive. Check the character domains in the config before adding metaphors or specialized observations.

### Repetitive Body Tics

Characters clenching jaws. Characters raising eyebrows. Characters letting out breaths they didn't know they were holding. When body moments default to the same small set of gestures, physicality becomes wallpaper rather than characterization. Track which gestures you've already used for each character. If a character has clenched their jaw once in a chapter, find a different physical expression for the next moment of tension.

### Counterpoints That Feel Artificial

Adding disagreement for the sake of friction produces scenes where characters argue about nothing. Counterpoints must arise from genuine differences in values, knowledge, or priorities that the characters already possess. If the config establishes that Marcus thinks in structural terms and Elena in musical ones, their disagreement should stem from those different lenses -- not from one of them arbitrarily playing devil's advocate.

### Additions That Sound Like the Agent, Not the Writer

The most dangerous pitfall in an additive phase. New material must match the existing prose's diction, rhythm, and register. Before inserting a line, read the two lines that will surround it. The insertion should be indistinguishable from its neighbors. If the writer favors short declarative sentences, do not insert a long subordinate clause. If the prose is spare, do not add lush description.

---

*Enrichment is not decoration. It is restoration -- returning the breath and blood that revision necessarily stripped away.*
