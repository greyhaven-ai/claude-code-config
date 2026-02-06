# Phase 1: Research

| Field | Value |
|-------|-------|
| **Phase** | 1 of 5 |
| **Name** | Research |
| **Agent** | research-gatherer (`creative-writing:writing-research-gatherer`) |
| **Expected Output** | Research brief, fact sheets, source annotations |

---

## Objectives

Phase 1 is the foundation beneath the foundation. Its scope is gathering and organizing the factual, contextual, and genre-level knowledge that all subsequent phases depend on. No creative decisions are made here -- only research.

### 1. Genre Conventions

Identify the conventions, expectations, and reader assumptions of the target genre:

- **Structural norms**: Typical plot structures, act breaks, pacing patterns
- **Character archetypes**: Common roles and how the genre subverts or embraces them
- **Tone expectations**: What readers of this genre expect in terms of darkness, humor, romance, tension
- **Market positioning**: Where this project sits relative to comparable titles

Genre research is not prescriptive. It maps the landscape so the writer can make informed choices about which conventions to follow and which to break.

### 2. Setting Research

Build the factual foundation for the world:

- **Historical context**: If the setting has a real-world basis, gather period-accurate details (technology, social norms, daily life, language)
- **Geographic specifics**: Physical environment, climate, landmarks, spatial relationships
- **Cultural elements**: Customs, beliefs, social hierarchies, power structures
- **Technical domains**: Any specialized knowledge the story requires (medicine, law, military, science, trade, craft)

### 3. Thematic Context

Research the themes the project will explore:

- **Literary precedent**: How other works have handled similar themes
- **Real-world grounding**: Factual context that gives thematic exploration authenticity
- **Philosophical dimensions**: Key arguments, counterarguments, and nuances within each theme
- **Symbolic vocabulary**: Objects, places, or actions traditionally associated with these themes

### 4. Accuracy Needs Assessment

Identify areas where factual accuracy is critical versus areas where creative license is appropriate:

- **Hard constraints**: Facts the story cannot contradict without breaking reader trust (historical dates, physical laws, cultural realities)
- **Soft constraints**: Areas where approximation is acceptable (fictional locations based on real ones, composite cultures)
- **Creative license zones**: Areas explicitly marked for invention (speculative elements, fictional technologies, imagined histories)

---

## Agent Prompt Template

Use the following prompt when dispatching the research-gatherer agent for Phase 1. Replace placeholder values with project-specific content.

```markdown
# Phase 1: Research

You are performing Phase 1 of the novel development pipeline. Your scope is strictly limited to research and information gathering. Do not make creative decisions -- gather the raw material that later phases will use.

## Inputs

- **Project brief**: {{PROJECT_BRIEF}}
- **Project config**: {{CONFIG_PATH}}
- **Genre**: {{GENRE}}
- **World type**: {{WORLD_TYPE}}

Read the project config first. It contains the project overview, character list, world type, themes, and research priorities.

## Research Priorities

Focus your research on the priorities listed in the project config. These are the areas the writer has identified as needing factual grounding.

## Instructions

### 1. Genre Landscape

Research the target genre ({{GENRE}}):

- Identify 5-10 comparable titles and their structural approaches
- Map common plot structures and reader expectations
- Note conventions this project might follow or subvert
- Document typical word count ranges and pacing patterns

### 2. Setting and World

Research the setting based on world type ({{WORLD_TYPE}}):

- Gather period/location-specific details relevant to the story
- Document cultural norms, social structures, and daily life
- Identify technical domains requiring specialized knowledge
- Create fact sheets for each major research area

### 3. Thematic Research

For each theme listed in the project config:

- Find literary precedents and how they handled the theme
- Gather real-world context that grounds the theme
- Note philosophical dimensions and nuances
- Identify symbolic vocabulary associated with the theme

### 4. Accuracy Assessment

Produce a clear classification:

- **Hard constraints**: Facts the story must respect
- **Soft constraints**: Areas allowing approximation
- **Creative license**: Areas marked for invention

## Rules

- **Research only. No creative decisions.** You gather and organize information. You do not suggest plot points, character traits, or world-building elements.
- **Cite or attribute** where possible. Future phases need to know where information came from.
- **Organize by topic.** Produce separate fact sheets for distinct research areas rather than one monolithic document.
- **Flag gaps.** If a research priority cannot be adequately addressed, flag it clearly so the writer can provide additional direction.
- **Commit nothing.** The pipeline orchestrator handles git commits between phases.

## Output

After completing research, provide:

- Research brief (executive summary of findings)
- Individual fact sheets per research area
- Genre conventions document
- Accuracy assessment (hard constraints, soft constraints, creative license)
- Gaps and open questions requiring writer input
```

---

## Phase Checklist

Verify all items before marking Phase 1 complete:

- [ ] Genre conventions researched and documented
- [ ] Setting/world research gathered with fact sheets per topic
- [ ] Thematic context researched for all listed themes
- [ ] Accuracy assessment produced (hard constraints, soft constraints, creative license)
- [ ] Research organized into separate, clearly labeled documents
- [ ] Research gaps and open questions flagged for the writer
- [ ] All research priorities from the project config addressed
- [ ] No creative decisions made (no plot suggestions, no character development)
- [ ] Research brief (executive summary) produced
- [ ] Git commit created: `novel-dev: phase 1 research complete - <project>`

---

## Common Pitfalls

**Researching too broadly.** The research priorities in the project config exist for a reason. A novel set in 1920s Chicago needs speakeasy culture and jazz, not a comprehensive history of Illinois. Stay focused on what the story actually needs. Breadth without relevance wastes time and produces noise that later phases must filter.

**Making creative decisions during research.** It is tempting to suggest "this historical event would make a great plot point" or "this cultural practice could define a character." Resist. Phase 1 gathers raw material. Phases 2 and 3 make creative decisions informed by that material. Premature creative choices constrain later phases unnecessarily.

**Under-researching speculative elements.** Even fantasy and science fiction have research needs. A magic system benefits from understanding real-world mythological traditions. A fictional technology benefits from understanding the real science it extrapolates from. "Made up" does not mean "uninformed."

**Producing unstructured dumps.** A wall of research text is nearly as useless as no research. Organize findings into discrete fact sheets with clear headings. The character-developer, world-builder, and story-architect in Phase 2 each need to find their relevant material quickly.

**Ignoring the accuracy assessment.** The distinction between hard constraints, soft constraints, and creative license zones is critical for Phase 2 agents. Without it, the world-builder does not know which details must be preserved and which can be adapted. The accuracy assessment is not optional -- it is a key Phase 1 deliverable.

---

*Research does not constrain creativity. It gives creativity solid ground to stand on.*
