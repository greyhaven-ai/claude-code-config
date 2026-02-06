# Phase 5: Integration

| Field | Value |
|-------|-------|
| **Phase** | 5 of 5 |
| **Name** | Integration |
| **Agents** | believability-auditor (`creative-writing:writing-believability-auditor`) + lead synthesis |
| **Execution** | Believability audit first, then lead synthesizes all deliverables |
| **Expected Output** | Novel Foundation Package |

---

## Objectives

Phase 5 is verification and synthesis, not creation. No new characters, world elements, plot beats, or dialogue are invented here. The believability-auditor checks the accumulated deliverables for consistency, and the pipeline lead assembles everything into the Novel Foundation Package -- the single document a writer takes into drafting.

### 1. Pre-Draft Consistency Check

The believability-auditor examines all deliverables for cross-cutting issues:

- **Character-world consistency**: Do character backstories align with the world's history and social systems? Can characters plausibly have the skills, knowledge, and attitudes their profiles claim given the world they inhabit?
- **Character-structure consistency**: Does the outline give every character enough scenes to complete their arc? Are characters asked to do things their profiles say they cannot or would not do?
- **World-structure consistency**: Do scenes take place in locations that exist in the world bible? Does the timeline respect the world's geography and travel constraints? Do scenes rely on world rules that are consistently applied?
- **Dialogue-character consistency**: Do voice guides align with character psychology? Do sample exchanges reflect the power dynamics and relationships established in the profiles?
- **Thematic coherence**: Are the project's themes woven through character arcs, world design, and structural beats, or are they isolated to one dimension?

### 2. NRS Scoring (Final)

The second and final NRS scoring:

- **C** (Character): Re-evaluate with the benefit of dialogue development and outline integration
- **W** (World): Re-evaluate after seeing how the world bible interacts with the structure
- **S** (Structure): Re-evaluate the outline's integrity now that character and dialogue layers are complete

Compare against the Phase 2 baseline. NRS should be stable or improved. Any dimension that dropped requires investigation.

### 3. Novel Foundation Package Assembly

The pipeline lead compiles all deliverables into a single foundation package:

```
## Novel Foundation Package

### Project Summary
[Config overview: title, genre, word count target, POV, tense]

### Research Summary
[Key findings from Phase 1, organized by relevance]

### Character Profiles
[Consolidated profiles with voice guides integrated]

### World Bible
[Consolidated world reference with consistency matrix]

### Story Structure
[Beat sheet + chapter outline with scene breakdowns]

### Dialogue Reference
[Voice differentiation matrix + key scene dialogue notes]

### Consistency Audit Results
[Believability auditor findings and resolutions]

### NRS Scores
[Phase 2 baseline and Phase 5 final, with commentary]

### Open Questions
[Unresolved flags from all phases, compiled for writer review]
```

### 4. Readiness Assessment

Based on the NRS scores and consistency audit, declare one of:

- **READY**: NRS composite >= 7, no critical consistency issues. The foundation supports drafting.
- **CONDITIONAL**: NRS composite 5-6, or minor consistency issues. Drafting can proceed with noted caveats.
- **HOLD**: NRS composite < 5, or critical consistency issues. Specific phases should be rerun before drafting begins.

---

## Agent Prompt Template

### Believability Auditor

```markdown
# Phase 5: Integration -- Consistency Check

You are performing the believability-auditor portion of Phase 5 in the novel development pipeline.

## Inputs

- **Project config**: {{CONFIG_PATH}}
- **All deliverables**: {{ALL_DELIVERABLES_PATH}}

Read all deliverables from Phases 1-4 before beginning your audit.

## YOUR ROLE: AUDIT ONLY -- NO CREATION

You are checking for consistency across all pipeline deliverables. You do not create new characters, world elements, plot points, or dialogue. Your output is a report.

## Tasks

### 1. Character-World Consistency

- Do character backstories fit the world's history and social systems?
- Can characters plausibly have the skills and knowledge their profiles claim?
- Are character attitudes consistent with their position in the world's social structure?

### 2. Character-Structure Consistency

- Does every character's arc have sufficient scenes in the outline?
- Are characters asked to act contrary to their established psychology without narrative justification?
- Does the POV distribution serve each character's arc adequately?

### 3. World-Structure Consistency

- Do all scenes take place in locations that exist in the world bible?
- Does the timeline respect travel distances and world geography?
- Are world rules applied consistently across all scenes?
- Does any scene rely on a world element not established in the bible?

### 4. Dialogue-Character Consistency

- Do voice guides match character psychology profiles?
- Do sample exchanges reflect the correct power dynamics?
- Are verbal habits consistent with character backgrounds?

### 5. Thematic Coherence

- Are the project's themes present in character arcs?
- Are the themes reflected in the world's design?
- Are the themes embedded in the structural beats?
- Or are themes isolated to one dimension only?

### 6. NRS Scoring

Score each dimension:

- **C** (Character): Depth, arcs, voice distinctiveness, ensemble dynamics (1-10)
- **W** (World): Internal consistency, systems, rules, culture (1-10)
- **S** (Structure): Plot integrity, pacing, beats, stakes, conflict (1-10)
- **Composite NRS**: (C + W + S) / 3

Compare against Phase 2 baseline. Flag any dimension that dropped.

## Report Format

Organize findings by severity:

- **Critical**: Issues that would undermine the novel's foundation
- **Major**: Issues a writer would encounter during drafting
- **Minor**: Issues that could be resolved during drafting
- **Clean**: Areas checked with no issues found

For each issue, identify:
- Which deliverable(s) are involved
- Which phase produced the inconsistency
- Suggested resolution (minimal fix, not a rewrite)
```

---

## Phase Checklist

Verify all items before marking Phase 5 complete:

- [ ] Believability-auditor has completed the full consistency check
- [ ] Character-world consistency verified
- [ ] Character-structure consistency verified
- [ ] World-structure consistency verified
- [ ] Dialogue-character consistency verified
- [ ] Thematic coherence assessed
- [ ] NRS scoring completed (C, W, S, composite)
- [ ] NRS compared against Phase 2 baseline -- no unexplained drops
- [ ] All critical consistency issues resolved or documented with resolution plan
- [ ] Novel Foundation Package assembled with all sections
- [ ] Open questions compiled from all phases
- [ ] Readiness assessment declared (READY / CONDITIONAL / HOLD)
- [ ] **No new creative content produced during this phase**
- [ ] Git commit created: `novel-dev: phase 5 integration complete - <project>`

---

## Common Pitfalls

**Creating instead of auditing.** The believability-auditor may be tempted to "fix" inconsistencies by inventing new character traits, world rules, or plot solutions. Its role is to identify and report -- not to create. Fixes should be flagged for the relevant phase to address via `/novel-phase` rerun.

**Superficial consistency checks.** Verifying that a location name appears in both the world bible and the outline is necessary but not sufficient. Deeper consistency means checking that the location's described qualities (size, atmosphere, accessibility) match how scenes use it. A "cramped apartment" that hosts a 20-person confrontation scene has a consistency problem that name-matching alone will not catch.

**Ignoring thematic coherence.** Themes are easy to deprioritize because they feel abstract compared to character-world-structure consistency. But a novel whose themes exist only in the project config and not in the actual deliverables has a foundation problem. The audit must verify that themes are operationalized, not just declared.

**Overweighting NRS drops.** A small NRS drop (0.5 points) in one dimension may simply reflect the auditor's fresh perspective versus the Phase 2 scorer's. Investigate drops, but do not panic over marginal changes. Focus on dimensions that dropped by 2+ points or critical consistency issues.

**Assembling the package without reading it.** The Novel Foundation Package is not a stapled collection of deliverables. The lead should read through the assembled package as a coherent document and verify that it tells a consistent story about the novel being developed. Contradiction between sections that were produced independently is expected and must be resolved at assembly time.

---

*Integration reveals what parallel work conceals: the gaps between the pillars.*
