# Phase 4: Dialogue

| Field | Value |
|-------|-------|
| **Phase** | 4 of 5 |
| **Name** | Dialogue |
| **Agent** | dialogue-coach (`creative-writing:writing-dialogue-coach`) |
| **Expected Output** | Voice guides, sample dialogue, scene dialogue notes |

---

## Objectives

Phase 4 takes the character profiles from Phase 2 and the chapter outline from Phase 3 and develops the dialogue dimension of the novel. The dialogue-coach does not write the novel's actual dialogue -- it produces voice guides and sample exchanges that a writer uses during drafting. This phase bridges character psychology and story structure through the lens of how characters speak.

### 1. Voice Guides

For each POV and major supporting character, produce a dialogue voice guide:

- **Register**: Formal, casual, regional, technical, poetic -- the default mode
- **Vocabulary range**: Words they use, words they avoid, jargon they default to
- **Sentence structure**: Short and declarative, long and qualifying, fragmented, run-on
- **Verbal habits**: Catchphrases, filler words, interruption patterns, deflection strategies
- **Subtext patterns**: How they say one thing and mean another, what topics trigger indirection
- **Emotional modulation**: How their speech changes under stress, joy, anger, grief, deception

### 2. Voice Differentiation Matrix

Produce a cross-reference that verifies no two characters sound alike:

- Side-by-side comparison of speech patterns
- At least three distinguishing markers per character pair
- Blind test: could a reader identify the speaker without dialogue tags?

### 3. Scene Dialogue Notes

For each scene in the Phase 3 outline that contains significant dialogue:

- **Power dynamic**: Who has the upper hand in this conversation
- **Subtext layer**: What is being discussed beneath the surface
- **Information exchange**: What the reader learns through this dialogue that they cannot learn another way
- **Emotional trajectory**: Where each speaker starts emotionally and where they end
- **Key lines**: 2-3 sample exchanges that demonstrate the scene's dialogue tone

### 4. Dialogue-Driven Scene Identification

Identify scenes where dialogue is the primary vehicle for:

- Character revelation (a character reveals something through how they speak, not what they say)
- Conflict escalation (a conversation that starts civil and becomes confrontational)
- Relationship shift (the moment a relationship changes through dialogue)
- Thematic articulation (characters debate or embody a theme through conversation)

---

## Agent Prompt Template

Use the following prompt when dispatching the dialogue-coach agent for Phase 4. Replace placeholder values with project-specific paths.

```markdown
# Phase 4: Dialogue

You are performing Phase 4 of the novel development pipeline. Your role is to develop voice guides, sample dialogue, and scene dialogue notes based on the character profiles and chapter outline.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Character profiles**: {{CHARACTER_PROFILES_PATH}}
- **Chapter outline**: {{OUTLINE_PATH}}

Read the character profiles thoroughly before beginning. The voice profiles established in Phase 2 are your starting point -- you are deepening and operationalizing them for dialogue.

## Instructions

### 1. Voice Guides

For each POV character and major supporting character, produce a voice guide containing:

- Default register and how it shifts in different social contexts
- Vocabulary inventory (characteristic words, avoided words, jargon)
- Sentence structure patterns with examples
- Verbal habits (minimum 3 per character)
- Subtext strategies (how this character hides, deflects, or reveals through speech)
- Emotional modulation (how speech changes under stress, joy, anger, grief)
- A paragraph-length "voice sample" -- a monologue or dialogue excerpt that captures this character's sound

### 2. Voice Differentiation Matrix

Produce a comparison table:

| Feature | [Character A] | [Character B] | [Character C] |
|---------|--------------|--------------|--------------|
| Register | | | |
| Sentence length | | | |
| Verbal habit | | | |
| Under stress | | | |
| Deflection style | | | |

Verify that every character pair has at least 3 distinguishing features.

### 3. Scene Dialogue Notes

For each scene in the outline that contains dialogue between 2+ characters:

- Identify the power dynamic
- Note the subtext layer (what is really being discussed)
- Map the emotional trajectory of the conversation
- Provide 2-3 sample exchange lines that demonstrate tone and dynamic
- Flag scenes where dialogue carries exposition (these need extra care to avoid "as you know, Bob" patterns)

### 4. Key Dialogue Scenes

Identify the 10-15 most dialogue-critical scenes in the outline. For each:

- Why dialogue is the essential vehicle (not action, not narration)
- The specific challenge (e.g., "two characters who hate each other must cooperate")
- Extended sample exchange (5-8 lines) demonstrating how the scene's dialogue should feel

## Rules

- **Voice guides and samples only. No drafting.** You produce reference material for the writer, not manuscript text.
- **Ground in character profiles.** Every voice choice must be traceable to the character's psychology, background, and arc as defined in Phase 2.
- **Respect the outline.** Scene dialogue notes follow the Phase 3 structure. Do not suggest scene additions or restructuring.
- **Dialogue is character.** If a voice guide reads like it could belong to any character, it is not specific enough. Revise until each guide is unmistakably one person.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

- Individual voice guide per character
- Voice differentiation matrix
- Scene dialogue notes for all dialogue-heavy scenes
- Key dialogue scenes analysis with extended samples
- Flags for scenes with high exposition risk
```

---

## Phase Checklist

Verify all items before marking Phase 4 complete:

- [ ] Voice guide produced for every POV character
- [ ] Voice guide produced for every major supporting character
- [ ] Voice differentiation matrix shows at least 3 distinguishing features per character pair
- [ ] Scene dialogue notes cover all dialogue-heavy scenes in the outline
- [ ] Key dialogue scenes identified (10-15 most critical) with extended samples
- [ ] Sample exchanges demonstrate subtext, not just surface-level conversation
- [ ] Exposition-risk scenes flagged with mitigation notes
- [ ] Voice guides grounded in Phase 2 character profiles
- [ ] No manuscript text or draft prose produced
- [ ] No structural changes suggested to the Phase 3 outline
- [ ] Git commit created: `novel-dev: phase 4 dialogue complete - <project>`

---

## Common Pitfalls

**Generic voice guides.** A voice guide that says "speaks casually, uses short sentences" could describe half the characters in fiction. Effective voice guides are specific enough that a reader of the guide alone could identify the character. If you cannot hear the character's distinct sound, the guide needs more work.

**Ignoring subtext.** Real dialogue is rarely about what it appears to be about. A conversation about dinner plans can be about control. An argument about a broken fence can be about a broken marriage. Scene dialogue notes that only address surface content miss the dimension that makes dialogue compelling. Every significant dialogue scene should have an identified subtext layer.

**Sample exchanges that demonstrate the writer's voice, not the character's.** The dialogue-coach produces samples in the character's voice, not in a generic "good dialogue" style. If all sample exchanges sound like they were written by the same person regardless of which character is speaking, the differentiation work has failed.

**Over-prescribing dialogue beats.** Scene dialogue notes guide the writer; they do not script the conversation. Providing 2-3 key exchange lines gives the writer a tonal anchor. Providing 20 lines of scripted dialogue removes the writer's creative agency and produces stiff scenes during drafting.

**Disconnecting from the outline.** Dialogue development must follow the Phase 3 structure. A dialogue-coach who suggests "this scene needs to be split into two conversations" is overstepping into Phase 3 territory. Flag structural concerns; do not resolve them.

---

*Dialogue is not what characters say. It is who they reveal themselves to be when they open their mouths.*
