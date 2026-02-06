# Phase 3: Structure

| Field | Value |
|-------|-------|
| **Phase** | 3 of 5 |
| **Name** | Structure |
| **Agent** | outline-architect (`creative-writing:writing-outline-architect`) |
| **Expected Output** | Chapter-by-chapter outline with scene breakdowns |

---

## Objectives

Phase 3 is the integration point. The outline-architect takes three independent deliverables -- character profiles, world bible, and beat sheet -- and weaves them into a chapter-by-chapter outline with scene breakdowns. This is where the novel's structure becomes concrete: abstract beats become specific scenes with specific characters in specific locations.

### 1. Beat-to-Chapter Translation

Convert the beat sheet from Phase 2 into a chapter structure:

- Map each structural beat to one or more chapters
- Determine chapter length targets based on the pacing plan
- Identify which chapters are single-scene and which are multi-scene
- Ensure act boundaries fall at natural chapter breaks

### 2. Scene Breakdown

For each chapter, define its constituent scenes:

- **POV character**: Who experiences this scene
- **Location**: Where it takes place (from the world bible)
- **Scene goal**: What the POV character wants in this scene
- **Conflict**: What opposes the scene goal
- **Outcome**: How the scene resolves (yes-but, no-and, or revelation)
- **Narrative function**: Why this scene exists in the story (advances plot, develops character, builds world, raises stakes)

### 3. Character Threading

Verify that each character's arc is properly distributed across the outline:

- Every character arc beat from Phase 2 has a corresponding scene
- No character disappears for too long without narrative justification
- POV distribution is balanced (or intentionally imbalanced)
- Relationship dynamics evolve progressively -- no sudden jumps in how characters relate

### 4. World Integration

Verify that the outline makes full use of the world bible:

- Key locations appear in scenes that leverage their specific qualities
- World rules are demonstrated through action, not exposition
- Cultural elements are woven into character behavior and scene texture
- No scene takes place in a location not established in the world bible (or flag it as needing addition)

---

## Agent Prompt Template

Use the following prompt when dispatching the outline-architect agent for Phase 3. Replace placeholder values with project-specific paths.

```markdown
# Phase 3: Structure

You are performing Phase 3 of the novel development pipeline. Your role is to synthesize the character profiles, world bible, and beat sheet from Phase 2 into a chapter-by-chapter outline with scene breakdowns.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Character profiles**: {{CHARACTER_PROFILES_PATH}}
- **World bible**: {{WORLD_BIBLE_PATH}}
- **Beat sheet**: {{BEAT_SHEET_PATH}}

Read all inputs before beginning. You are integrating three independent deliverables into a unified structure.

## Instructions

### 1. Chapter Outline

For each chapter, provide:

- **Chapter number and working title**
- **Act position** (Act I / II / III and approximate percentage through the story)
- **Target word count** (based on pacing plan from beat sheet)
- **Summary** (2-3 sentences describing what happens)
- **Structural beat(s)** this chapter serves

### 2. Scene Breakdowns

For each scene within each chapter:

- **POV**: Which character experiences this scene
- **Location**: Where (reference world bible location name)
- **Time**: When (relative to story timeline)
- **Scene goal**: What the POV character wants
- **Conflict source**: What opposes the goal
- **Outcome**: Yes-but / No-and / Revelation
- **Function**: Plot / Character / World / Stakes (primary purpose)
- **Characters present**: Who is in the scene

### 3. Character Arc Verification

After completing the outline, verify:

- Every character's arc trajectory (from Phase 2 profiles) has corresponding scenes
- Arc beats are distributed progressively -- no sudden leaps in development
- POV rotation follows the project's conventions
- No character vanishes for more than [appropriate number] chapters without reason

### 4. World Integration Check

Verify:

- Every key location from the world bible is used at least once
- World rules are demonstrated through scene action, not info-dumps
- Cultural elements appear naturally through character behavior
- Flag any scene that requires a location or world element not in the bible

### 5. Continuity Timeline

Produce a simple timeline showing:

- Day/time progression across the outline
- Travel time between locations (consistent with world bible distances)
- Parallel storylines synchronized correctly
- No temporal impossibilities

## Rules

- **Outline only. No prose.** You produce structural documents with scene breakdowns. You do not write sample text.
- **Integrate, do not override.** If the beat sheet conflicts with a character arc or world constraint, flag the conflict rather than silently choosing one over the other.
- **Every scene earns its place.** If a scene does not advance plot, develop character, build world, or raise stakes, it does not belong in the outline. Flag questionable scenes.
- **Respect the word count target.** The sum of chapter targets should approximate the project's target word count.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

- Chapter-by-chapter outline with scene breakdowns
- Character arc distribution map
- Continuity timeline
- Integration flags (conflicts between character, world, and structure)
- Suggested additions to the world bible (if scenes need locations not yet defined)
```

---

## Phase Checklist

Verify all items before marking Phase 3 complete:

- [ ] Every beat from the Phase 2 beat sheet has been mapped to at least one chapter
- [ ] Every chapter has a scene breakdown with POV, location, goal, conflict, outcome
- [ ] Character arcs are distributed progressively across the outline
- [ ] No character disappears without narrative justification
- [ ] POV distribution follows project conventions
- [ ] All key locations from the world bible are utilized
- [ ] World rules are demonstrated through action, not exposition
- [ ] Continuity timeline is internally consistent
- [ ] Chapter word count targets sum to approximately the target word count
- [ ] Integration flags documented (any conflicts between character, world, and structure)
- [ ] No prose or draft text produced (structural documents only)
- [ ] Git commit created: `novel-dev: phase 3 structure complete - <project>`

---

## Common Pitfalls

**Ignoring world constraints.** The outline-architect may place a scene in a location that contradicts the world bible's geography or travel times. A character cannot be in two distant cities on the same day unless the world has fast travel. Check the world bible's spatial relationships before finalizing scene sequences.

**Front-loading character introductions.** A common structural mistake is introducing all characters in Act I, creating a crowded opening that overwhelms the reader. Stagger introductions. Let the reader bond with the protagonist before expanding the ensemble.

**Scenes without conflict.** Every scene needs opposition to the POV character's goal. A scene where a character walks through a market "to show the world" has no conflict and will read as a tour guide passage. If the scene exists for world-building, the character must want something the market complicates.

**Beat sheet worship.** The beat sheet is a guide, not a cage. If integrating character arcs and world constraints reveals that a beat should shift, flag it rather than forcing the outline to match the beat sheet exactly. The outline is the more integrated document and should take precedence where conflicts arise.

**Outline-as-synopsis.** An outline that reads like a plot summary ("and then... and then... and then...") is missing the scene-level granularity that Phase 4 needs. The dialogue-coach cannot do meaningful work without knowing who is in each scene, what they want, and what opposes them. Invest in the scene breakdowns.

---

*Structure is not a cage. It is the skeleton that lets the body move.*
