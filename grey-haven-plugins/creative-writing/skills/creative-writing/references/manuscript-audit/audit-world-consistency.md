# Audit: World Consistency Assessment

| Field | Value |
|-------|-------|
| **Agent** | world-builder (`creative-writing:writing-world-builder`) |
| **Execution** | Parallel -- runs simultaneously with prose-quality and believability audits |
| **Mode** | Audit only -- consistency verification, not world creation |
| **Output** | World Consistency Matrix plus detailed findings report |

---

## Objectives

The world-builder in audit mode verifies that the manuscript's world-building is internally consistent. This is verification, not creation -- the agent checks existing rules, systems, and facts against how they appear throughout the manuscript. It does not invent new world elements or suggest expansions. Findings feed into the synthesis protocol where the audit lead cross-references them with prose quality and believability results.

### 1. Rule Verification

Check every established world rule against its application in the manuscript:

- Rules defined in the config's "Known World Rules" section are applied uniformly
- Rules established in early chapters are not violated in later chapters
- Exceptions to rules are narratively justified and consistent with the system's logic
- No rule is applied inconsistently between characters without explanation

### 2. Timeline Verification

Confirm that temporal references form a coherent sequence:

- Events referenced in the config's "Timeline Anchors" occur where and when expected
- Duration references ("three days later," "by morning," "the following week") add up correctly
- Character ages, seasons, and calendar references remain consistent
- Flashbacks and memories reference events that actually occurred as described

### 3. Geographic and Spatial Consistency

Verify that the physical world holds together:

- Travel times between locations are consistent across the manuscript
- Spatial relationships (north/south, upstairs/downstairs, near/far) do not shift
- Descriptions of the same location are consistent across scenes
- Characters do not appear in impossible locations given established travel constraints

### 4. System Coherence

Check that the manuscript's systems (magic, technology, economy, politics) behave according to their established rules:

- Magic or technology systems follow their defined costs, limitations, and mechanics
- Economic references (prices, trade, wealth) are internally consistent
- Political structures (hierarchies, laws, customs) behave as established
- Social systems (class, culture, religion) are applied uniformly across characters and situations

---

## Agent Prompt Template

```
You are performing a world consistency audit as part of a manuscript audit
team. Three agents (including you) are auditing this manuscript simultaneously.
Your findings will be synthesized with prose quality and believability results
to produce an overall quality decision.

MANUSCRIPT PATH: {{MANUSCRIPT_PATH}}
CONFIG PATH: {{CONFIG_PATH}}
KNOWN WORLD RULES: {{KNOWN_WORLD_RULES}}

## YOUR ROLE: AUDIT ONLY -- NO EDITS, NO WORLD CREATION

You are verifying consistency. You do not modify the manuscript. You do not
create new world elements, expand the world-building, or suggest additions.
Your output is a World Consistency Matrix with a detailed findings report.

## Tasks

### 1. Build the Rule Registry

Before auditing, compile a comprehensive list of world rules from two sources:

- **Explicit rules** from {{KNOWN_WORLD_RULES}} in the config
- **Implicit rules** established in the manuscript text (e.g., a character
  demonstrates that magic requires line of sight in Chapter 2)

For each rule, record:
- The rule statement
- Where it is first established (chapter/section)
- The source (config or manuscript text with quote)

### 2. Rule Application Audit

For each rule in the registry, trace its application through the manuscript:

- Does the rule hold in every instance?
- Are there violations? If so, are they acknowledged in-narrative (a
  character breaking a rule with consequences) or are they unintentional
  contradictions?
- Are exceptions justified within the system's logic?

Classify each rule as:
- **Consistent**: Applied uniformly throughout
- **Minor inconsistency**: Small deviation, easily fixed
- **Major inconsistency**: Notable contradiction a careful reader would catch
- **Critical inconsistency**: Fundamental break that undermines the system

### 3. Timeline Audit

Using the config's timeline anchors as reference points:

- Map the manuscript's chronology from beginning to end
- Verify that duration references ("three days," "a week later") produce
  a coherent timeline
- Check that character ages remain consistent
- Verify seasonal and calendar references align
- Flag any temporal impossibilities

### 4. Spatial Audit

Map the manuscript's geography and spatial relationships:

- Verify that travel times between locations are consistent
- Check that spatial descriptions of the same location do not contradict
  across scenes
- Confirm that characters cannot appear in impossible locations given
  established distances and travel methods
- Flag descriptions that contradict established geography

### 5. System Audit

For each system in the manuscript (magic, technology, economy, politics,
social structures):

- Verify the system behaves according to its established rules
- Check that costs, limitations, and mechanics are applied uniformly
- Flag any instance where a system behaves differently for plot convenience
- Note systems that are well-established vs. underspecified

### 6. World Consistency Matrix

Produce the matrix organizing findings by category and severity:

| Category | Critical | Major | Minor | Clean |
|----------|----------|-------|-------|-------|
| World Rules | X | X | X | X |
| Timeline | X | X | X | X |
| Geography/Spatial | X | X | X | X |
| Systems | X | X | X | X |

For each issue, provide:
- **Location**: Chapter/section where the inconsistency appears
- **Rule**: Which established rule is violated
- **Evidence**: Quoted passages showing the contradiction
- **Established in**: Where the rule was originally defined

### 7. Report

Produce a structured report:

1. **World Consistency Matrix**: Summary table with counts per category
2. **Rule Registry**: Complete list of rules tracked (explicit and implicit)
3. **Critical Issues**: Full detail on any critical inconsistencies
4. **Major Issues**: Full detail on major inconsistencies
5. **Minor Issues**: List with brief descriptions
6. **Clean Areas**: Categories and sections verified with no issues
7. **System Assessment**: Brief evaluation of each system's coherence

For each issue, note the chapter/section location so the audit lead can
cross-reference with findings from the other two auditors.
```

---

## Phase Checklist

Before marking the world consistency audit complete, verify:

- [ ] Full manuscript has been read and evaluated
- [ ] Rule registry compiled from config and manuscript text
- [ ] Every rule in registry traced through the manuscript
- [ ] Timeline verified against config anchors and internal references
- [ ] Geographic and spatial consistency checked
- [ ] All systems (magic, technology, economy, politics, social) audited
- [ ] World Consistency Matrix produced with severity counts
- [ ] All findings include chapter/section location for cross-referencing
- [ ] All findings include quoted evidence from the manuscript
- [ ] Report is structured and ready for synthesis
- [ ] **No edits were made to the manuscript**
- [ ] **No new world elements were created or suggested**

---

## Common Pitfalls

**Creating world-building instead of auditing it.** The world-builder in audit mode is not building -- it is verifying. Do not suggest new rules, expand existing systems, or fill gaps in the world-building. If the manuscript's magic system is underspecified, note that as an observation, not as an opportunity to define it.

**Treating genre flexibility as inconsistency.** Some genres permit looser world-building than others. A literary novel set in a real city does not need the same geographic precision as a hard science fiction novel. Calibrate expectations to the manuscript's genre (from the config's "Genre Expectations" section).

**Flagging intentional ambiguity as error.** Authors sometimes leave world elements deliberately ambiguous for thematic or narrative reasons. A magic system whose limits are unclear may be intentionally mysterious rather than poorly defined. Flag it as "underspecified" rather than "inconsistent" unless there is a direct contradiction.

**Missing implicit rules.** The config's "Known World Rules" list is a starting point, not a complete registry. The manuscript itself establishes many rules through narrative (a character demonstrates a limitation, a scene establishes a travel time). The audit must capture these implicit rules as well, or it will miss inconsistencies that only exist between the text and itself.

**Over-mapping minor details.** Not every spatial reference needs to resolve to an exact coordinate. "Across town" does not need to be measured against established walking speeds unless a later scene's timing depends on it. Focus audit depth on details that other scenes depend on.

---

*A world that forgets its own rules asks the reader to forget them too. The reader will not.*
