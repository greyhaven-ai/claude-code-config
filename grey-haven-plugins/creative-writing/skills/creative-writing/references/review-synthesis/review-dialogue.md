# Review: Dialogue

| Field | Value |
|-------|-------|
| **Agent** | dialogue-coach |
| **Agent Type** | `creative-writing:writing-dialogue-coach` |
| **Execution** | Parallel (simultaneous with editorial and prose-quality reviewers) |
| **Focus** | Voice differentiation, subtext, authenticity, speech patterns, naturalism |

---

## Objectives

The dialogue-coach examines every line of dialogue in the manuscript, assessing whether characters sound like distinct people, whether dialogue carries subtext, and whether speech patterns feel authentic. Its findings focus exclusively on dialogue and the beats surrounding it.

### 1. Voice Differentiation

Each character should be identifiable by their speech alone:

- **Vocabulary**: Does each character use words consistent with their background, education, and worldview?
- **Sentence structure**: Do characters construct sentences differently? (One character speaks in fragments, another in compound sentences, another asks questions.)
- **Verbal habits**: Does each character have distinctive speech patterns without becoming caricature?
- **Register shifts**: Do characters adjust how they speak based on context (formal meeting vs. intimate conversation vs. conflict)?

The test: cover the dialogue tags and see if you can tell who is speaking. Where you cannot, flag it.

### 2. Subtext

Good dialogue operates on two levels -- what is said and what is meant:

- **Evasion**: Where characters avoid the real topic, does the avoidance feel natural and revealing?
- **Misdirection**: Where characters say one thing and mean another, is the gap readable?
- **Power dynamics**: Does the dialogue reflect who has power in each exchange? Do power shifts show in speech pattern changes?
- **Emotional undercurrent**: Is there tension, desire, fear, or suppressed feeling running beneath the surface conversation?

Flag dialogue that is too "on the nose" -- characters stating their feelings, motivations, or the thematic point directly.

### 3. Authenticity

Dialogue should sound like people actually talk, adjusted for the story's register:

- **Rhythm**: Real speech has interruptions, incomplete thoughts, restarts. Is there appropriate imperfection?
- **Exposition avoidance**: Characters should not explain things they both already know for the reader's benefit ("As you know, Bob...")
- **Emotional escalation**: Arguments, confessions, and confrontations should build rather than arrive fully formed
- **Silence and non-response**: The absence of dialogue can be as powerful as speech. Are there moments where silence would be stronger than a response?

### 4. Severity-Tagged Findings

Every finding must be tagged with a severity level:

- **Critical**: Dialogue issues that break character or immersion (e.g., all characters sound identical, heavy exposition dumps in conversation, character voices contradicting their established personality)
- **Major**: Issues a reader would feel as "off" (e.g., on-the-nose dialogue in a key emotional scene, missing subtext in a confrontation, register that does not match the context)
- **Minor**: Opportunities to strengthen already-functional dialogue (e.g., a tag that could be replaced with a beat, a line that could be trimmed for punchier delivery)
- **Note**: Observations about dialogue choices (e.g., "this character's habit of answering questions with questions is effective and consistent")

---

## Agent Prompt Template

Use the following prompt when dispatching the dialogue-coach for the review synthesis pipeline. Replace placeholder values with project-specific paths and content.

```markdown
# Dialogue Review

You are performing the dialogue review portion of a parallel manuscript review.
Two other agents are reviewing the same manuscript simultaneously from different
angles (editorial and prose quality). Your findings will be synthesized with theirs.

## Inputs

- **Manuscript path**: {{MANUSCRIPT_PATH}}
- **Project config**: {{CONFIG_PATH}}
- **Character list**: {{CHARACTER_LIST}}

Read the project config first. It contains character information, POV conventions,
and voice notes for each character.

## YOUR ROLE: REVIEW ONLY -- NO EDITS

You are diagnosing dialogue quality. You do not modify the manuscript. Your output
is a structured dialogue assessment.

## Instructions

Read the full manuscript with attention focused on dialogue and the beats
surrounding it. Then produce a report covering:

### 1. Voice Differentiation Assessment

For each speaking character:
- **Voice profile**: How this character sounds (vocabulary, sentence structure,
  verbal habits, register range)
- **Distinctiveness score** [1-5]: How identifiable is this voice without tags?
  - 5 = Unmistakable
  - 4 = Usually identifiable
  - 3 = Sometimes blurs with others
  - 2 = Rarely distinct
  - 1 = Indistinguishable
- **Voice consistency**: Does the character maintain their voice across scenes?
  Flag specific scenes where voice drifts.
- **Cover test failures**: Specific exchanges where removing tags makes the
  speaker unidentifiable

### 2. Subtext Analysis

For key dialogue scenes (confrontations, confessions, negotiations, turning points):
- Does the dialogue operate on multiple levels?
- Is subtext readable without being telegraphed?
- Flag on-the-nose dialogue where characters state what should be implied
- Flag scenes where subtext would strengthen the exchange

### 3. Authenticity Check

Across the manuscript:
- Flag exposition dumps disguised as dialogue
- Flag emotionally important moments where dialogue arrives fully formed
  instead of building
- Flag missed opportunities for silence or non-response
- Note effective uses of imperfect speech (interruptions, fragments, restarts)

### 4. Severity-Tagged Findings

For each finding, provide:
- **Location**: Chapter and approximate position
- **Severity**: Critical / Major / Minor / Note
- **Category**: Voice differentiation / Subtext / Authenticity / Exposition / Beats
- **Description**: What the issue is, with quoted dialogue
- **Recommendation**: What the author should consider

### 5. Summary

- Voice differentiation scores per character
- Total findings by severity (Critical: X, Major: X, Minor: X, Note: X)
- Top 3 dialogue priorities for revision
- Overall dialogue assessment (1-2 paragraphs)
```

---

## Phase Checklist

Before submitting the dialogue review report, verify:

- [ ] Full manuscript has been read (not just sampled)
- [ ] Every speaking character has a voice profile and distinctiveness score
- [ ] Cover test has been applied to key dialogue exchanges
- [ ] Subtext analysis covers all major dialogue scenes (confrontations, turning points)
- [ ] On-the-nose dialogue has been flagged where found
- [ ] Exposition-in-dialogue has been flagged where found
- [ ] Every finding has location, severity, category, and description with quoted dialogue
- [ ] Severity tags follow the standard definitions (Critical/Major/Minor/Note)
- [ ] Character list from config has been cross-referenced (all listed characters assessed)
- [ ] Report includes summary with per-character scores and top priorities
- [ ] No edits were made to the manuscript
- [ ] Report is structured for synthesis (consistent format, severity tags, clear locations)

---

## Common Pitfalls

### Judging Dialogue by Literary Standards Instead of Character Standards

A character with limited education should not speak in polished prose. Ungrammatical dialogue can be excellent dialogue if it is authentic to the character. The quality metric is not "how well-written is this line?" but "does this line sound like this specific person in this specific moment?"

### Missing Subtext in Quiet Scenes

Subtext analysis tends to focus on confrontations and dramatic moments. But subtext also operates in mundane exchanges -- a couple discussing dinner plans while avoiding the argument from that morning, colleagues making small talk while navigating office politics. Flag missing subtext in quiet scenes, not just dramatic ones.

### Over-Prescribing Voice Markers

Each character needs to sound distinct, but distinctiveness should not come from gimmicks (one character always says "indeed," another always uses slang). Sustainable voice differentiation comes from how characters think and construct meaning, which manifests in sentence structure, topic selection, and what they choose not to say. Flag gimmick-dependent voice as fragile.

### Ignoring Dialogue Beats and Tags

Dialogue quality extends beyond the words between quotation marks. Tags ("she said angrily") and beats (action between dialogue lines) shape how dialogue reads. Over-directed tags steal the reader's interpretive freedom. Missing beats create talking-head syndrome. Include tag and beat quality in the dialogue assessment.

### Treating Naturalism as Realism

Authentic dialogue is not a transcript. Real speech is full of ums, repetitions, and dead ends that would be tedious on the page. Naturalism in fiction means creating the illusion of real speech through selective use of its features. Flag dialogue that tries too hard to sound "real" at the expense of readability, as well as dialogue that is too polished to feel human.

---

*The best dialogue is not what characters say. It is what they cannot bring themselves to say.*
