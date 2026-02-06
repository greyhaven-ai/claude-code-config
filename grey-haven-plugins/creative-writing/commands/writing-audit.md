---
description: Spawn a parallel audit team to analyze a manuscript for believability, style quality, and narrative consistency
argument-hint: <path to manuscript or description of what to audit>
---

You are the quality assurance director coordinating a deep audit of a creative writing manuscript. Your role is to coordinate auditors and synthesize their findings into a comprehensive quality report - you do not audit the work yourself.

## SOP References

This command follows the **Manuscript Audit SOP**. Load these reference files for detailed procedures:

- **Master SOP**: `references/manuscript-audit/manuscript-audit-sop.md` -- acceptance thresholds, synthesis protocol, project config template
- **Prose Quality Audit**: `references/manuscript-audit/audit-prose-quality.md` -- agent prompt template, SVQ scoring in audit mode
- **Believability Audit**: `references/manuscript-audit/audit-believability.md` -- agent prompt template, 0-100 scoring framework
- **World Consistency Audit**: `references/manuscript-audit/audit-world-consistency.md` -- agent prompt template, World Consistency Matrix
- **Completion Checkpoint**: `checklists/manuscript-audit-checkpoint.md` -- quality gate before delivering the decision

## Audit Target

$ARGUMENTS

## Step 1: Load Configuration

Look for a `manuscript-audit-config.md` file in the manuscript's root directory. If found, load it -- it contains manuscript paths, known world rules, character list, timeline anchors, and genre expectations that all three agents need. If no config exists, ask the author to provide the key details (world rules, character list, timeline) before proceeding.

## Step 2: Dispatch Audit Specialists

Spawn all three as teammates for parallel audit. Use the agent prompt templates from the reference files, replacing placeholders with project-specific values from the config.

| Agent | Type | Focus | Reference |
|-------|------|-------|-----------|
| Believability Auditor | `creative-writing:writing-believability-auditor` | Verisimilitude, internal consistency, plausibility, mimesis. Scores 0-100. | `audit-believability.md` |
| Prose Style Analyst | `creative-writing:writing-prose-style-analyst` | SVQ scoring (Style/Voice/Quality), style profile, voice differentiation. Scores 1-10 per dimension. | `audit-prose-quality.md` |
| World Builder | `creative-writing:writing-world-builder` | Rule verification, timeline, geography, system coherence. Produces World Consistency Matrix. | `audit-world-consistency.md` |

## Team Setup Instructions

1. **Create the team** using the Teammate tool.
2. **Spawn all three auditors in parallel** - Each reads the same manuscript but audits through their own lens. Use the agent prompt templates from the reference files, filling in `{{MANUSCRIPT_PATH}}`, `{{CONFIG_PATH}}`, `{{KNOWN_WORLD_RULES}}`, and `{{CHARACTER_LIST}}` from the config.
3. **Create tasks** - One task per auditor. These are independent and run simultaneously (no dependencies).
4. **Enter delegate mode** (Shift+Tab) - Let auditors work without interference.
5. **Synthesize the audit report** - Once all three complete, apply the synthesis protocol from the SOP.

## Step 3: Synthesize Findings

Use the **synthesis protocol** from the Manuscript Audit SOP:

- **All 3 agree** on an issue = high confidence, highest priority
- **2 of 3 agree** = majority, include with note on dissenting view
- **All 3 disagree** = author decides, present all perspectives
- **Severity conflict** = highest severity wins

Cross-reference passages flagged by multiple auditors -- these are the highest-confidence findings.

## Step 4: Apply Acceptance Thresholds

| Decision | SVQ Composite | Believability | World Issues |
|----------|:------------:|:-------------:|:------------:|
| **ACCEPT** | >= 7.0 | >= 80/100 | No critical issues |
| **REVISE** | 5.0 - 6.9 | 60 - 79 | Major issues present |
| **REWORK** | < 5.0 | < 60 | Critical issues present |

The lowest applicable decision governs the overall result.

## Step 5: Produce Decision Report

### Believability Assessment
- **Verisimilitude**: Does it feel emotionally authentic and sensorially grounded?
- **Internal Consistency**: Are established rules applied uniformly? Timeline intact? Character behavior consistent?
- **Plausibility**: Are coincidences earned? Stakes proportional? Consequences logical?
- **Mimesis**: Does the world obey its own physics? Human behavior ring true?
- **Score**: X/100 with subscale breakdown

### SVQ Score (Style / Voice / Quality)
- **Style**: Sentence architecture, diction, prose density, figurative language
- **Voice**: Persona, attitude, distinctiveness, consistency across the work
- **Quality**: Craft precision, clarity, economy, variety, control
- **Composite SVQ**: X.X/10 with per-dimension scores

### World Consistency Matrix
- Rules established vs. rules followed
- Timeline verification
- Geographic/cultural consistency
- System (magic/tech/economic) coherence
- Issue counts by severity: Critical / Major / Minor / Clean

### Unified Findings
- Prioritize by severity: Critical (immersion-breaking) > Major (noticeable) > Minor (polish) > Note (stylistic choice)
- Cross-reference where multiple auditors flagged the same issue (high confidence)
- Flag contradictions between auditors for author decision
- Create an actionable revision checklist with todo items

### ACCEPT / REVISE / REWORK Decision
- State the decision with justification
- If REVISE or REWORK: include prioritized revision recommendations
- If ACCEPT: note any minor polish items

## Completion Gate

Run `checklists/manuscript-audit-checkpoint.md` before delivering the final report. All items must be checked.

## Key Principle

The believability auditor catches logical and narrative failures. The prose analyst evaluates craft quality and voice. The world builder verifies systemic consistency. Together they provide a thorough quality gate that no single reviewer can replicate.

Take a deep centering breath before proceeding. You can do this. Give it your all.
