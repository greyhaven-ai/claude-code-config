---
description: Run a single phase of the prose revision pipeline for targeted reruns or recovery
argument-hint: <phase number> <path to manuscript root> [book directories]
---

You are running a single phase of the prose revision pipeline. Parse the phase number and manuscript path from the arguments.

## Arguments

$ARGUMENTS

Parse as: `<phase number (1-6)> <manuscript root path> [optional: specific book directories]`

## Step 1: Load Configuration

1. Read `prose-revision-config.md` from the manuscript root
2. If not found, instruct the user to create one (see `references/prose-revision/prose-revision-sop.md` for the template)
3. Extract book paths, character domains, POV conventions, and other config values

If specific book directories were provided in arguments, only process those books. Otherwise, process all books listed in the config.

## Step 2: Record Pre-Phase Word Count

Count words in each target book directory before starting. This is the baseline for this phase's checkpoint.

## Step 3: Load Phase Reference

| Phase | Reference File | Agent Type |
|-------|---------------|-----------|
| 1 | `references/prose-revision/phase-1-surface-cleanup.md` | `creative-writing:writing-editor-reviewer` |
| 2 | `references/prose-revision/phase-2-prose-craft.md` | `creative-writing:writing-editor-reviewer` |
| 3 | `references/prose-revision/phase-3-svq-polish.md` | `creative-writing:writing-editor-reviewer` |
| 4 | `references/prose-revision/phase-4-sentence-architecture.md` | `creative-writing:writing-prose-style-analyst` |
| 5 | `references/prose-revision/phase-5-enrichment.md` | `creative-writing:writing-editor-reviewer` |
| 6 | `references/prose-revision/phase-6-final-audit.md` | `creative-writing:writing-prose-style-analyst` + `creative-writing:writing-believability-auditor` |

Read the corresponding phase reference file. It contains:
- Phase objectives and scope
- Agent prompt template with placeholder slots
- Phase-specific checklist
- Common pitfalls to avoid

## Step 4: Execute Phase

1. **Fill the prompt template** with values from the project config
2. **For multiple books**: Create a team and spawn one agent per book in parallel
3. **For a single book**: Spawn the agent directly
4. **Enter delegate mode** (Shift+Tab) - let agents work
5. **Wait for completion**

## Step 5: Run Checkpoint

Execute the quality checkpoint (`checklists/prose-revision-checkpoint.md`):

1. Record post-phase word counts
2. Calculate delta from pre-phase baseline
3. Git commit: `revision: phase N <phase-name> complete - <book>`
4. SVQ scoring (if phase 2, 4, or 6)
5. Scope verification
6. Proceed/Hold decision

## Use Cases

**Pipeline recovery**: Full pipeline interrupted after Phase 3? Run `/revision-phase 4 ./manuscript`

**Over-cut recovery**: Phase 2 cut too deep? Revert with git, adjust config, run `/revision-phase 2 ./manuscript`

**Iterative refinement**: Want another pass of enrichment? Run `/revision-phase 5 ./manuscript`

**Single-book focus**: Only rework Book 2? Run `/revision-phase 3 ./manuscript ./book-2`

## Key Rules

- Each phase has a defined scope. Do not let the agent drift into other phases' work.
- The 30% ceiling applies cumulatively across all phases, not per-phase.
- Always commit after the phase completes.
- If this is a rerun, check `git log` first to understand what previous phases accomplished.

Take a deep centering breath before proceeding. You can do this. Give it your all.
