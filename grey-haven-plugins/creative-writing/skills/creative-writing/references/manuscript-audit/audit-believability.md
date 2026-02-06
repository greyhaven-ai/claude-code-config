# Audit: Believability Assessment

| Field | Value |
|-------|-------|
| **Agent** | believability-auditor (`creative-writing:writing-believability-auditor`) |
| **Execution** | Parallel -- runs simultaneously with prose-quality and world-consistency audits |
| **Mode** | Audit only -- no edits to the manuscript |
| **Output** | Believability score (0-100) plus detailed findings report |

---

## Objectives

The believability auditor examines the manuscript for verisimilitude, internal consistency, plausibility, and mimesis. In audit mode, the agent scores and reports -- it does not revise. Findings feed into the synthesis protocol where the audit lead cross-references them with prose quality and world consistency results.

### 1. Verisimilitude

Does the manuscript feel emotionally authentic and sensorially grounded?

- Characters react to events with emotional responses that feel earned and proportional
- Physical sensations are specific rather than generic ("her hands shook" vs. detailed physiological response)
- Social dynamics between characters follow recognizable human patterns
- The narrative voice commits to its reality rather than hedging with qualifiers

### 2. Internal Consistency

Are established rules applied uniformly throughout the manuscript?

- Character knowledge -- no character acts on information they have not received
- Character behavior -- actions align with established traits, motivations, and limitations
- Timeline integrity -- events occur in a coherent temporal sequence
- Cause and effect -- consequences follow logically from their causes

### 3. Plausibility

Are coincidences earned, stakes proportional, and consequences logical?

- Plot-critical coincidences have adequate setup or carry appropriate narrative cost
- Character decisions are motivated by established goals, fears, or values
- Consequences scale with the severity of the triggering event
- Resolution mechanisms are established before they are needed (no deus ex machina)

### 4. Mimesis

Does the world obey its own physics, and does human behavior ring true?

- The world's rules (whether realistic or fantastical) are applied consistently
- Characters make mistakes, misunderstand, and act on incomplete information as real people do
- Systems (social, economic, magical, technological) behave as their established logic demands
- The narrative does not break its own frame for convenience

---

## Agent Prompt Template

```
You are performing a believability audit as part of a manuscript audit team.
Three agents (including you) are auditing this manuscript simultaneously.
Your findings will be synthesized with prose quality and world consistency
results to produce an overall quality decision.

MANUSCRIPT PATH: {{MANUSCRIPT_PATH}}
CONFIG PATH: {{CONFIG_PATH}}
KNOWN WORLD RULES: {{KNOWN_WORLD_RULES}}
CHARACTER LIST: {{CHARACTER_LIST}}

## YOUR ROLE: AUDIT ONLY -- NO EDITS

You are scoring and analyzing. You do not modify the manuscript. Your output
is a structured findings report with a believability score.

## Tasks

### 1. Verisimilitude Assessment

Read the manuscript and evaluate emotional authenticity:

- Are character reactions proportional and earned by preceding events?
- Is sensory grounding specific rather than generic?
- Do social dynamics follow recognizable human patterns?
- Does the narrative voice commit to its reality?

Score verisimilitude on a 0-25 subscale.

### 2. Internal Consistency Check

Verify that the manuscript does not contradict itself:

- Track character knowledge across scenes. Flag any instance where a
  character acts on information they have not yet received.
- Check character behavior against established traits from {{CHARACTER_LIST}}.
  Flag personality breaks that are not narratively justified.
- Verify timeline integrity. Use {{KNOWN_WORLD_RULES}} and the config's
  timeline anchors as reference points.
- Trace cause-and-effect chains. Flag consequences without visible causes
  and causes without visible consequences.

Score internal consistency on a 0-25 subscale.

### 3. Plausibility Evaluation

Assess whether the plot mechanics hold together:

- Identify every significant coincidence. For each, determine whether it
  was adequately set up or whether it feels contrived.
- Check that character decisions are motivated by established goals, fears,
  or values -- not by plot convenience.
- Verify that consequences scale appropriately with their causes.
- Check that resolution mechanisms (skills, knowledge, tools, allies) are
  established before they are needed.

Score plausibility on a 0-25 subscale.

### 4. Mimesis Check

Evaluate whether the world and its inhabitants behave authentically:

- Do the world's rules (from {{KNOWN_WORLD_RULES}}) hold consistently?
- Do characters make realistic mistakes and act on incomplete information?
- Do systems (social, economic, magical, technological) behave according
  to their own established logic?
- Does the narrative maintain its frame without breaking for convenience?

Score mimesis on a 0-25 subscale.

### 5. Scoring and Report

Calculate the overall believability score:

**Believability Score** = Verisimilitude + Internal Consistency +
                          Plausibility + Mimesis (out of 100)

Produce a structured report:

1. **Overall Score**: X/100 with subscale breakdown
2. **Critical Issues**: Issues that would confuse or lose the reader
3. **Major Issues**: Issues a careful reader would notice
4. **Minor Issues**: Issues only visible on close re-reading
5. **Clean Areas**: Sections checked with no issues found
6. **Evidence**: For each issue, quote the relevant passage and explain
   the specific believability failure

For each issue, note the chapter/section location so the audit lead can
cross-reference with findings from the other two auditors.
```

---

## Phase Checklist

Before marking the believability audit complete, verify:

- [ ] Full manuscript has been read and evaluated
- [ ] Verisimilitude assessed and scored (0-25)
- [ ] Internal consistency checked against character list and timeline anchors
- [ ] Plausibility evaluated for all major plot mechanics
- [ ] Mimesis checked against known world rules
- [ ] Overall believability score calculated (0-100)
- [ ] All findings categorized by severity (Critical/Major/Minor/Clean)
- [ ] Each issue includes chapter/section location for cross-referencing
- [ ] Each issue includes quoted evidence from the manuscript
- [ ] Report is structured and ready for synthesis
- [ ] **No edits were made to the manuscript**

---

## Common Pitfalls

**Auditing genre conventions as believability failures.** A fantasy novel where characters cast spells is not an internal consistency failure -- it is a genre convention. The audit checks whether the *established* rules are followed, not whether those rules match reality. A character who casts a spell without the required physical contact (per the world's rules) is a failure. A character who casts a spell at all is not.

**Conflating character flaws with author mistakes.** A character who makes a bad decision is not an implausibility if the decision aligns with their established traits. A reckless character acting recklessly is consistent, even if the outcome is catastrophic. Only flag character decisions where the motivation is absent or contradicts established characterization.

**Over-weighting minor timeline ambiguities.** Not every temporal reference needs to resolve to a specific calendar date. "A few days later" is acceptable vagueness unless it contradicts a specific anchor elsewhere. Reserve timeline flags for genuine contradictions, not imprecision.

**Scoring based on personal taste rather than craft.** The believability score measures whether the manuscript works on its own terms, not whether the auditor enjoys the genre, agrees with the themes, or would have made different creative choices. A well-executed horror novel and a well-executed romance should both score high on believability if their internal logic holds.

---

*Believability is not about what is real. It is about what the story promised and whether it kept its word.*
