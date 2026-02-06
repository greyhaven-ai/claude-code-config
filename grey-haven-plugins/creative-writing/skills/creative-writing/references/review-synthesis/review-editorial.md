# Review: Editorial

| Field | Value |
|-------|-------|
| **Agent** | editor-reviewer |
| **Agent Type** | `creative-writing:writing-editor-reviewer` |
| **Execution** | Parallel (simultaneous with prose-quality and dialogue reviewers) |
| **Focus** | Structure, clarity, pacing, developmental feedback, line editing |

---

## Objectives

The editor-reviewer examines the manuscript from a traditional editorial perspective. In the review context, the agent produces a diagnostic report -- it does not make edits. Its findings feed into the synthesis protocol alongside the other two reviewers.

### 1. Developmental Feedback

Big-picture structural assessment:

- **Arc structure**: Does the narrative arc function? Are there missing beats, sagging middles, rushed resolutions?
- **Pacing**: Where does the story drag? Where does it rush? Are scene lengths proportional to their dramatic weight?
- **Scene function**: Does every scene advance plot, character, or theme? Flag scenes that exist only to convey information.
- **Stakes escalation**: Do stakes build progressively, or do they plateau or regress?

### 2. Line Editing

Sentence-level craft evaluation:

- **Clarity**: Passages where meaning is ambiguous or requires re-reading
- **Economy**: Passages that take too many words to make their point
- **Transitions**: Scene and chapter transitions that jar or confuse
- **Repetition**: Unintentional repetition of ideas, images, or phrasing across scenes

### 3. Copy Editing Flags

Mechanical issues worth noting (not the primary focus, but captured when encountered):

- Inconsistent formatting (scene breaks, internal thought conventions)
- Continuity errors (character details, timeline, spatial logic)
- Factual inconsistencies within the world's established rules

### 4. Severity-Tagged Findings

Every finding must be tagged with a severity level:

- **Critical**: Structural issues that undermine the narrative
- **Major**: Issues a careful reader would notice and be bothered by
- **Minor**: Issues that weaken the prose but do not break the reading experience
- **Note**: Observations and opportunities, not problems

---

## Agent Prompt Template

Use the following prompt when dispatching the editor-reviewer for the review synthesis pipeline. Replace placeholder values with project-specific paths and content.

```markdown
# Editorial Review

You are performing the editorial review portion of a parallel manuscript review.
Two other agents are reviewing the same manuscript simultaneously from different
angles (prose quality and dialogue). Your findings will be synthesized with theirs.

## Inputs

- **Manuscript path**: {{MANUSCRIPT_PATH}}
- **Project config**: {{CONFIG_PATH}}
- **Focus areas**: {{FOCUS_AREAS}}
- **Draft number**: {{DRAFT_NUMBER}}

Read the project config first. It contains character information, POV conventions,
the author's known strengths and weaknesses, and specific concerns to address.

## YOUR ROLE: REVIEW ONLY -- NO EDITS

You are producing a diagnostic report. You do not modify the manuscript. Your output
is a structured editorial assessment.

## Instructions

Read the full manuscript. Then produce a report covering:

### 1. Developmental Assessment

- Overall arc structure: does it work? Where does it falter?
- Pacing map: flag specific chapters/scenes that drag or rush
- Scene audit: flag any scene that does not advance plot, character, or theme
- Stakes trajectory: does tension build appropriately?

Address any specific concerns from the project config.

### 2. Line-Level Findings

For each finding, provide:
- **Location**: Chapter and approximate position
- **Severity**: Critical / Major / Minor / Note
- **Category**: Clarity / Economy / Transition / Repetition
- **Description**: What the issue is
- **Recommendation**: What the author should consider

### 3. Copy Editing Flags

Note any mechanical issues encountered during reading. These are secondary to
the editorial assessment but valuable for the synthesis.

### 4. Summary

- Total findings by severity (Critical: X, Major: X, Minor: X, Note: X)
- Top 3 priorities for revision
- Overall editorial assessment (1-2 paragraphs)
```

---

## Phase Checklist

Before submitting the editorial review report, verify:

- [ ] Full manuscript has been read (not just sampled)
- [ ] Developmental assessment covers arc, pacing, scene function, and stakes
- [ ] Every line-level finding has location, severity, category, and description
- [ ] Severity tags follow the standard definitions (Critical/Major/Minor/Note)
- [ ] Author's specific concerns from the config have been addressed
- [ ] Focus areas from the config have received extra attention
- [ ] Report includes a summary with finding counts and top priorities
- [ ] No edits were made to the manuscript
- [ ] Report is structured for synthesis (consistent format, severity tags, clear locations)

---

## Common Pitfalls

### Editing Instead of Reviewing

The editor-reviewer agent is accustomed to making edits in the prose revision pipeline. In review mode, it must only diagnose and report. If the agent starts producing revised text instead of findings, redirect it to reporting mode. The output is a report, not a marked-up manuscript.

### Overwhelming the Author with Minor Findings

A thorough editorial review can produce hundreds of Minor findings. This volume obscures the important issues. Limit Minor findings to patterns (e.g., "chapters 3, 7, and 12 all have the same transition problem") rather than exhaustive per-instance listings. Reserve detailed per-instance reporting for Critical and Major findings.

### Ignoring the Author's Focus Areas

The config contains focus areas for a reason -- the author already suspects these areas need work. If the review does not address the author's stated concerns, even to say "this area is actually working well," the author will feel unheard. Always address every focus area explicitly.

### Conflating Personal Preference with Craft Issues

Editorial feedback must distinguish between craft problems (this does not work) and stylistic preferences (I would do this differently). Tag preference-based observations as Notes, not as Major or Critical findings. The author's creative choices are not errors unless they demonstrably fail on the page.

---

*A good editor sees what the writer intended and measures the gap between intention and execution.*
