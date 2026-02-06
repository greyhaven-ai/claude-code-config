# Manuscript Audit SOP

Standard Operating Procedure for comprehensive manuscript quality assessment using parallel agent dispatch.

## Audit Architecture

The manuscript audit is a **parallel dispatch** operation, not a phased pipeline. Three specialized agents examine the manuscript simultaneously through different analytical lenses. Their independent findings are then synthesized by the audit lead into a unified quality report with an ACCEPT/REVISE/REWORK decision.

```
                    +---------------------------+
                    |       Audit Lead          |
                    |  (dispatch & synthesize)  |
                    +---------------------------+
                       /         |         \
                      /          |          \
               +----------+ +----------+ +----------+
               |  Prose   | | Believe- | |  World   |
               |  Style   | | ability  | |  Builder |
               | Analyst  | | Auditor  | |  (audit) |
               +----------+ +----------+ +----------+
                      \          |          /
                       \         |         /
                    +---------------------------+
                    |    Synthesis & Decision    |
                    +---------------------------+
```

All three agents run **simultaneously**. There are no dependencies between them. Each reads the same manuscript but evaluates it through its own lens.

## Quality Metrics

Each agent produces a score or matrix using its existing assessment framework. The audit applies thresholds to these scores for a structured decision.

### SVQ Score (Prose Style Analyst)

The prose-style-analyst produces an SVQ composite score (Style, Voice, Quality), each on a 1-10 scale. See the prose revision SOP for the full SVQ framework.

### Believability Score (Believability Auditor)

The believability-auditor produces a score on a 0-100 scale covering verisimilitude, internal consistency, plausibility, and mimesis.

### World Consistency Matrix (World Builder)

The world-builder in audit mode produces a consistency matrix cataloguing issues by severity: Critical, Major, Minor, or Clean.

## Acceptance Thresholds

| Decision | SVQ Composite | Believability | World Issues | Interpretation |
|----------|:------------:|:-------------:|:------------:|----------------|
| **ACCEPT** | >= 7.0 | >= 80/100 | No critical issues | Manuscript meets quality bar. Proceed to publication or next pipeline stage. |
| **REVISE** | 5.0 - 6.9 | 60 - 79 | Major issues present | Targeted revision needed. Use findings to scope revision work. |
| **REWORK** | < 5.0 | < 60 | Critical issues present | Fundamental quality concerns. Requires substantial rework before re-audit. |

**Threshold logic**: A manuscript receives the *lowest* applicable decision. If SVQ is 7.5 (ACCEPT) but Believability is 55 (REWORK), the overall decision is REWORK. One failing dimension pulls the whole decision down.

## Synthesis Protocol

When the three agents return their findings, the audit lead synthesizes using these rules:

### Agreement Rules

| Condition | Confidence | Action |
|-----------|-----------|--------|
| All 3 agents flag the same issue | **High confidence** | Include in revision list at highest priority |
| 2 of 3 agents flag the same issue | **Majority** | Include with note on the dissenting view |
| All 3 agents disagree | **Author decides** | Present all three perspectives and flag for discussion |

### Severity Escalation

When multiple agents flag the same passage but at different severity levels, **highest severity wins**. If the prose-style-analyst calls a passage "minor" but the believability-auditor calls it "critical," it is critical.

### Cross-Reference Prioritization

Issues flagged by multiple auditors from different angles are the highest-confidence findings:

- A passage flagged for both weak prose (style) and implausible dialogue (believability) is a stronger signal than either alone
- A world-building inconsistency that also breaks character knowledge is more urgent than an isolated continuity error
- Cross-referenced issues should appear first in the revision recommendations

## Project Configuration

Each manuscript project should have a `manuscript-audit-config.md` file in its root directory. This file provides project-specific context that all three agents load before beginning their audit.

### Config Template

Create `manuscript-audit-config.md` in your manuscript root:

```markdown
# Manuscript Audit Config

## Manuscript Paths

| Item | Path | Approximate Word Count |
|------|------|----------------------:|
| Manuscript | ./manuscript/ | 85,000 |
| Outline (if available) | ./outline.md | — |

## Known World Rules

Established rules that the world-builder should verify are applied consistently:

- [Rule 1: e.g., "Magic requires physical contact with the source element"]
- [Rule 2: e.g., "Faster-than-light travel takes exactly 3 days per jump"]
- [Rule 3: e.g., "The dead cannot be resurrected under any circumstances"]

## Character List

| Character | Role | Key Traits | Domain |
|-----------|------|-----------|--------|
| [Name] | [POV/Supporting/Antagonist] | [2-3 defining traits] | [Metaphor domain] |

## Timeline Anchors

Key dates and sequences that must remain consistent:

- [Event 1: e.g., "The siege begins on the autumn equinox"]
- [Event 2: e.g., "Elena arrives in the capital three days after the siege"]
- [Event 3: e.g., "The betrayal happens before the winter solstice"]

## Genre Expectations

- **Genre**: [e.g., Epic Fantasy, Literary Fiction, Thriller]
- **Tone**: [e.g., Dark and atmospheric, Wry and conversational]
- **Audience**: [e.g., Adult, YA, Middle Grade]
- **Comparable titles**: [e.g., "The Name of the Wind meets A Gentleman in Moscow"]
```

Agents reference this config via the `{{CONFIG_PATH}}` placeholder in their prompt templates. The audit lead passes the actual path when dispatching agents.

## Audit Execution

### Step 1: Load Configuration

Read the project's `manuscript-audit-config.md`. If no config exists, prompt the author to create one before proceeding. The config provides critical context that all three agents need.

### Step 2: Dispatch Agents in Parallel

Spawn all three agents simultaneously. Each receives:
- The manuscript path
- The config path
- Their specific audit prompt (from the agent reference files)

### Step 3: Collect Reports

Wait for all three agents to complete. Do not begin synthesis until all reports are in.

### Step 4: Synthesize Findings

Apply the agreement rules, severity escalation, and cross-reference prioritization from the synthesis protocol above. Produce the unified findings report.

### Step 5: Apply Acceptance Thresholds

Using the scores from all three agents, determine the ACCEPT/REVISE/REWORK decision per the thresholds table.

### Step 6: Produce Decision Report

Output the structured decision report with:
- Individual agent scores and summaries
- Cross-referenced findings (highest priority first)
- ACCEPT/REVISE/REWORK decision with justification
- Revision recommendations (if REVISE or REWORK)

## Agent Reference Files

Detailed prompts and checklists for each agent are in the companion reference files:

- `audit-prose-quality.md` -- Prose Style Analyst in audit mode
- `audit-believability.md` -- Believability Auditor
- `audit-world-consistency.md` -- World Builder in audit mode

## Quality Checkpoint

Use `checklists/manuscript-audit-checkpoint.md` to verify the audit is complete before delivering the decision report.

---

*An audit does not judge the manuscript. It gives the author the information to judge it themselves.*
