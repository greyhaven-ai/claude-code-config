# Phase 2: Foundation

| Field | Value |
|-------|-------|
| **Phase** | 2 of 5 |
| **Name** | Foundation |
| **Agents** | character-developer (`creative-writing:writing-character-developer`) + world-builder (`creative-writing:writing-world-builder`) + story-architect (`creative-writing:writing-story-architect`) |
| **Execution** | Three agents run **in parallel** |
| **Expected Output** | Character profiles, world bible, beat sheet |

---

## Objectives

Phase 2 is where the novel's foundation takes shape. Three specialized agents work simultaneously from the same research brief, each building their domain independently. This is not redundant -- character, world, and story are genuinely separable concerns at the foundation stage. Integration happens in Phase 3 when the outline-architect weaves all three together.

### 1. Character Development

The character-developer produces comprehensive profiles for all named characters:

- **Psychology**: Motivations, fears, desires, internal contradictions, worldview
- **Arc trajectory**: Where the character starts emotionally/psychologically and where they end
- **Voice distinctiveness**: Speech patterns, vocabulary, rhythm, verbal habits that distinguish this character from others
- **Relationships**: How each character relates to others in the ensemble -- alliances, tensions, dependencies
- **Backstory**: Relevant history that shapes present behavior (only what the story needs, not exhaustive biography)

### 2. World Building

The world-builder produces the world bible:

- **Physical environment**: Geography, climate, architecture, spatial relationships
- **Social systems**: Government, economy, class structure, power dynamics
- **Cultural fabric**: Customs, beliefs, rituals, taboos, art, food, daily life
- **Rules and constraints**: Laws of magic, technology limits, physical rules that differ from reality (if any)
- **Internal consistency**: Every element must be compatible with every other element

### 3. Story Architecture

The story-architect produces the beat sheet:

- **Three-act structure** (or genre-appropriate alternative): Setup, confrontation, resolution
- **Key beats**: Inciting incident, plot points, midpoint, crisis, climax, denouement
- **Stakes escalation**: How stakes increase across the narrative arc
- **Conflict layers**: External conflict, interpersonal conflict, internal conflict
- **Pacing plan**: Where the story accelerates, where it breathes, where tension peaks

### 4. NRS Scoring

After all three agents complete, the first NRS (Narrative Readiness Score) is calculated:

- **C** (Character): Based on character profiles -- depth, distinctiveness, arc clarity
- **W** (World): Based on world bible -- consistency, richness, rule clarity
- **S** (Structure): Based on beat sheet -- pacing, stakes, conflict integrity

This baseline NRS establishes the quality floor. Phase 5 must match or exceed it.

---

## Agent Prompt Templates

### Character Developer

```markdown
# Phase 2: Foundation -- Character Development

You are performing the character development portion of Phase 2 in the novel development pipeline. You work in parallel with the world-builder and story-architect. Your scope is characters only.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Research output**: {{RESEARCH_OUTPUT}}
- **Character list**: {{CHARACTER_LIST}}
- **POV conventions**: {{POV_CONVENTIONS}}

Read the project config and research output first. The config contains the character list and POV conventions. The research brief provides factual context that should inform character development.

## Instructions

For each character listed in the project config:

### 1. Psychology Profile

- Core motivation (what drives them)
- Core fear (what they avoid)
- Internal contradiction (the tension between who they are and who they want to be)
- Worldview (how they interpret events and other people)
- Emotional baseline (their default state and what disrupts it)

### 2. Arc Trajectory

- Starting state (who they are at page one)
- Key transformation points (what changes them)
- Ending state (who they become)
- The lie they believe / the truth they learn (if applicable)

### 3. Voice Profile

- Vocabulary level and register (formal, casual, technical, poetic)
- Sentence rhythm (short and clipped, flowing and complex, variable)
- Verbal habits and tics (words or phrases they overuse)
- What they talk about vs. what they avoid discussing
- How they sound different from every other character

### 4. Relationship Map

For each significant relationship:
- Nature of the relationship (ally, antagonist, mentor, romantic, complicated)
- Power dynamic (who has leverage, who defers)
- Source of tension (what creates friction)
- Evolution (how the relationship changes across the story)

### 5. Backstory (Story-Relevant Only)

- Key events that shaped who they are now
- Secrets or hidden knowledge
- Skills, expertise, or limitations relevant to the plot

## Rules

- **Profiles only. No prose.** You produce character documents, not sample scenes or dialogue.
- **Ground in research.** Use the Phase 1 research brief to ensure characters are plausible within the established setting and genre.
- **Respect POV conventions.** Character voice profiles must be compatible with the declared POV approach.
- **Flag conflicts.** If two characters' arcs contradict or a character's psychology is inconsistent with their listed role, flag it for resolution.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

- Individual character profile document per character
- Ensemble relationship map
- Voice differentiation summary (how each POV character sounds distinct)
- Flags and open questions for the writer
```

### World Builder

```markdown
# Phase 2: Foundation -- World Building

You are performing the world-building portion of Phase 2 in the novel development pipeline. You work in parallel with the character-developer and story-architect. Your scope is the world only.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Research output**: {{RESEARCH_OUTPUT}}
- **World type**: {{WORLD_TYPE}}
- **Genre**: {{GENRE}}

Read the project config and research output first. The config contains the world type and genre. The research brief provides factual context and the accuracy assessment (hard constraints, soft constraints, creative license zones).

## Instructions

### 1. Physical Environment

- Geography and climate relevant to the story
- Key locations where scenes will take place
- Spatial relationships between locations (distances, travel times, accessibility)
- Architecture and built environment
- Sensory environment (what characters see, hear, smell, feel in each setting)

### 2. Social Systems

- Government and power structures
- Economic systems and class divisions
- Law and justice (formal and informal)
- Education and knowledge systems
- Military or defense (if relevant)

### 3. Cultural Fabric

- Daily life rhythms (meals, work, leisure, sleep)
- Customs, rituals, and celebrations
- Beliefs, religion, or philosophy
- Art, music, literature within the world
- Food, clothing, and material culture
- Taboos and social boundaries

### 4. Rules and Constraints

- What works differently from reality (magic, technology, physics, biology)
- Hard limits on these systems (what they cannot do)
- Costs or consequences of using these systems
- How ordinary people interact with extraordinary elements
- Internal consistency checks (no rule contradicts another)

### 5. Consistency Matrix

Produce a cross-reference that verifies:
- Each social system is compatible with the physical environment
- Cultural elements are consistent with the social systems
- Rules and constraints do not create logical paradoxes
- The world can sustain the kind of story being told

## Rules

- **World bible only. No prose.** You produce reference documents, not narrative descriptions.
- **Respect the accuracy assessment.** Hard constraints from Phase 1 research are non-negotiable. Soft constraints allow adaptation. Creative license zones allow invention.
- **Genre-appropriate depth.** A contemporary realistic novel needs less world-building than a secondary fantasy. Scale your output to what the story requires.
- **Flag impossibilities.** If the project config describes a world that contains internal contradictions, flag them for resolution rather than papering over them.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

- World bible document organized by section (physical, social, cultural, rules)
- Key locations reference (one-page summaries per major setting)
- Consistency matrix
- Flags and open questions for the writer
```

### Story Architect

```markdown
# Phase 2: Foundation -- Story Architecture

You are performing the story architecture portion of Phase 2 in the novel development pipeline. You work in parallel with the character-developer and world-builder. Your scope is plot and structure only.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **Research output**: {{RESEARCH_OUTPUT}}
- **Genre**: {{GENRE}}
- **Target word count**: {{TARGET_WORD_COUNT}}

Read the project config and research output first. The config contains the genre, target word count, and themes. The research brief provides genre conventions and structural norms.

## Instructions

### 1. Structural Framework

Based on the genre ({{GENRE}}) and target word count ({{TARGET_WORD_COUNT}}):

- Select the appropriate structural model (three-act, hero's journey, mystery structure, romance beats, etc.)
- Define act boundaries with approximate word count targets
- Identify the major structural beats and their placement

### 2. Beat Sheet

Produce a detailed beat sheet including:

- **Opening image**: The world before the story changes it
- **Inciting incident**: The event that disrupts equilibrium
- **First plot point**: The point of no return
- **Rising action beats**: Key events that escalate stakes and complicate the situation
- **Midpoint**: The shift in the protagonist's approach or understanding
- **Second plot point**: The crisis that forces the final confrontation
- **Climax**: The decisive moment
- **Resolution**: The new equilibrium
- **Closing image**: The world after the story changed it

### 3. Stakes Escalation

Map how stakes increase across the narrative:

- Personal stakes (what the protagonist stands to lose)
- Interpersonal stakes (what relationships are at risk)
- External stakes (what larger consequences loom)
- How each act raises the stakes from the previous one

### 4. Conflict Layers

Identify and map:

- External conflict (protagonist vs. antagonist/obstacle)
- Interpersonal conflict (between characters who share goals but disagree on methods)
- Internal conflict (within the protagonist)
- How these layers interact and reinforce each other

### 5. Pacing Plan

Based on the target word count:

- Which sections move fast (action, revelation, confrontation)
- Which sections breathe (reflection, relationship building, world exploration)
- Where tension peaks and valleys fall
- Chapter length variation strategy

## Rules

- **Beat sheet only. No prose.** You produce structural documents, not narrative text.
- **Respect genre conventions.** The genre research from Phase 1 identifies reader expectations. Your structure should satisfy or deliberately subvert them -- never ignore them.
- **Scale to word count.** A 60,000-word thriller has different structural needs than a 120,000-word epic fantasy. Your beat placement must reflect the target scope.
- **Flag theme-structure misalignment.** If the themes in the config do not naturally map to the structural beats, flag it for discussion.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

- Beat sheet with timing/placement notes
- Stakes escalation map
- Conflict layer diagram
- Pacing plan with approximate word count per section
- Flags and open questions for the writer
```

---

## Phase Checklist

Verify all items before marking Phase 2 complete:

- [ ] All three agents (character-developer, world-builder, story-architect) have completed
- [ ] Character profiles produced for every listed character
- [ ] Ensemble relationship map created
- [ ] Voice differentiation summary produced for POV characters
- [ ] World bible covers physical, social, cultural, and rules sections
- [ ] Consistency matrix verifies world coherence
- [ ] Beat sheet produced with structural beats and timing
- [ ] Stakes escalation mapped across the narrative arc
- [ ] Conflict layers identified (external, interpersonal, internal)
- [ ] Pacing plan aligns with target word count
- [ ] All deliverables grounded in Phase 1 research
- [ ] No prose or draft text produced (documents and profiles only)
- [ ] Flags and open questions compiled from all three agents
- [ ] NRS scoring performed: C (Character), W (World), S (Structure)
- [ ] NRS baseline recorded in checkpoint tracker
- [ ] Git commit created: `novel-dev: phase 2 foundation complete - <project>`

---

## Common Pitfalls

**Starting without Phase 1 research.** The parallel agents in Phase 2 all depend on the research brief. Running them without it produces character profiles ungrounded in the setting, a world bible that contradicts factual constraints, and a beat sheet that ignores genre conventions. Phase 1 is the non-negotiable prerequisite.

**Agents overstepping their scope.** The character-developer may want to define world elements. The world-builder may want to suggest plot implications. The story-architect may want to develop character arcs. Each agent must stay in their lane. Integration is Phase 3's job. Cross-contamination in Phase 2 creates conflicting assumptions that the outline-architect must then untangle.

**Treating the beat sheet as an outline.** The story-architect produces a beat sheet -- structural beats with timing. This is not a chapter outline. The outline-architect in Phase 3 translates beats into chapters using character profiles and the world bible. Confusing beats with chapters produces a structure that has not yet been informed by character or world constraints.

**Shallow character profiles.** A character profile that lists traits without exploring contradictions, fears, and voice is a character sheet, not a foundation. Phase 4's dialogue work depends on genuine voice distinctiveness established here. A flat profile produces flat dialogue downstream.

**World-building beyond story needs.** A world bible should be deep where the story goes and shallow where it does not. Comprehensive economic systems for a world the protagonist never interacts with economically are wasted effort. Build what the story needs, flag what it might need, and leave the rest.

---

*Three pillars built in parallel. Integration is the arch that holds them together.*
