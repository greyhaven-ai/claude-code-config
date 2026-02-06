# Phase 1: Surface Cleanup

| Field | Value |
|-------|-------|
| **Phase** | 1 of 6 |
| **Name** | Surface Cleanup |
| **Agent** | editor-reviewer (`creative-writing:writing-editor-reviewer`) |
| **Expected Word Count Delta** | -5% to -10% |

---

## Objectives

Phase 1 is the first pass through the manuscript. Its scope is deliberately narrow: hunt mechanical patterns that weaken prose without touching deeper craft concerns. Resist the urge to rewrite -- that comes later.

### 1. Hunt Verbal Tics

Identify and remove or rephrase habitual filler words and distancing constructions:

- **just** -- filler that adds nothing ("She just wanted to leave" -> "She wanted to leave")
- **really** / **very** -- intensity hedges that dilute instead of amplify
- **that** -- often grammatically optional ("She knew that he was lying" -> "She knew he was lying")
- **seemed to** / **appeared to** -- distancing qualifiers that undermine commitment to the narrative
- **started to** / **began to** -- false-start constructions that delay the action ("He started to run" -> "He ran")
- **a little** / **a bit** -- hedging that weakens description
- **could feel** / **could see** / **could hear** -- filter words that insert the narrator between reader and experience

Not every instance is wrong. "Just" in dialogue may be intentional voice. "Seemed to" may reflect genuine uncertainty. The goal is to eliminate the unconscious, habitual uses while preserving the deliberate ones.

### 2. Fix Closing Spirals

A closing spiral occurs when a paragraph or scene ending re-explains what was just shown. The prose lands its moment, then keeps talking. Common patterns:

- A strong image followed by a sentence interpreting it
- Dialogue that makes a point, then narration restating the same point
- An emotional beat followed by "And that was when she realized..."
- Scene endings that summarize what the scene already demonstrated

**Fix**: Cut the explaining sentence. Trust the image, the dialogue, or the beat to carry its own weight.

### 3. Ensure Voice Differentiation

Each POV character should sound distinct on the page. Check that:

- Vocabulary aligns with the character's background and worldview
- Sentence rhythm shifts between POV characters (e.g., one character thinks in short bursts, another in flowing clauses)
- Metaphor domains stay consistent with each character's conceptual frame (as defined in the project config)
- Internal thought patterns differ -- not every character processes the world the same way

Phase 1 does not rewrite voice. It flags sections where voices blur and removes tics that homogenize distinct characters.

---

## Agent Prompt Template

Use the following prompt when dispatching the editor-reviewer agent for Phase 1. Replace placeholder values with project-specific paths and content.

```markdown
# Phase 1: Surface Cleanup

You are performing Phase 1 of the prose revision pipeline. Your scope is strictly limited to surface cleanup. Do not address prose craft, sentence architecture, or enrichment -- those are later phases.

## Inputs

- **Manuscript path**: {{BOOK_PATH}}
- **Project config**: {{CONFIG_PATH}}

Read the project config first. It contains character domains, POV conventions, and the verbal tic list for this project.

## Character Domains

{{CHARACTER_DOMAINS}}

## POV Conventions

{{POV_CONVENTIONS}}

## Verbal Tics to Hunt

{{VERBAL_TICS}}

## Instructions

Read every chapter in the manuscript directory sequentially. For each chapter:

1. **Verbal tic removal**: Find every instance of the listed verbal tics. For each one, decide:
   - Is this deliberate (dialogue voice, genuine uncertainty, rhythmic purpose)? If yes, keep it.
   - Is this habitual filler? If yes, cut it or rephrase the sentence without it.

2. **Closing spiral repair**: Identify paragraphs that re-explain what was just shown. Cut the explaining sentence(s). If the paragraph feels incomplete after the cut, tighten the preceding sentence to land harder -- do not add new material.

3. **Voice differentiation check**: Compare how different POV characters sound. Flag any passages where a character's vocabulary, sentence rhythm, or metaphor domain drifts toward another character's voice. When you can fix drift by removing a tic or cutting a spiral, do so. When the issue requires deeper rewriting, leave a `<!-- VOICE-DRIFT: [character] sounds like [other character] here -->` comment for Phase 2.

## Rules

- **Edits only. No additions.** You may cut words, cut sentences, rephrase for concision. You may not add new sentences, paragraphs, or scenes.
- **Use MultiEdit for all changes.** Batch your edits per file. Do not use Write to rewrite entire files.
- **Preserve the writer's voice.** When rephrasing, stay within the character's diction and rhythm.
- **Track your cuts.** After editing each chapter, note the approximate word count before and after.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

After completing all chapters, provide a summary:

- Total chapters processed
- Approximate words removed
- Most common tics found (with counts)
- Closing spirals fixed (with chapter locations)
- Voice drift flags placed (if any)
```

---

## Phase Checklist

Verify all items before marking Phase 1 complete:

- [ ] Every chapter in the manuscript has been processed
- [ ] Verbal tics removed or confirmed as intentional (no unconscious instances remain)
- [ ] Closing spirals identified and cut -- no paragraph re-explains what was just shown
- [ ] Voice differentiation checked across all POV characters
- [ ] Voice drift comments placed where deeper rewriting is needed
- [ ] Word count delta is within expected range (-5% to -10%)
- [ ] Cumulative cuts tracked and recorded
- [ ] No new sentences, paragraphs, or scenes were added
- [ ] All edits made via MultiEdit (no full-file rewrites)
- [ ] Git commit created: `revision: phase 1 surface-cleanup complete - <book>`

---

## Common Pitfalls

**Over-cutting dialogue tics.** Characters in dialogue should sound like people, not prose. "Just" and "really" in dialogue may be intentional voice markers. Cut narration tics aggressively; cut dialogue tics cautiously.

**Confusing voice differentiation with voice rewriting.** Phase 1 flags voice drift and fixes it only where a tic removal or spiral cut naturally resolves the issue. It does not rewrite passages to create voice distinction -- that requires the craft-level work of Phase 2.

**Treating the tic list as a kill list.** The verbal tic list is a hunting guide, not a death warrant. Each instance needs judgment. A manuscript with zero instances of "just" reads as unnaturally scrubbed. The goal is reduction of unconscious habit, not total elimination.

**Editing for style instead of surface.** It is tempting to improve a weak metaphor or tighten a flabby paragraph while hunting tics. Resist. Style improvements belong to Phase 2. Mixing scopes produces unpredictable word count deltas and defeats the checkpoint system.

**Ignoring the 30% ceiling.** Phase 1 rarely approaches the cumulative 30% cut threshold on its own, but an aggressive pass on a tic-heavy manuscript can reach -10%. Track your delta and leave room for Phases 2-4.

---

*The cleanest prose is not the prose with the fewest words. It is the prose where every remaining word was chosen, not inherited.*
