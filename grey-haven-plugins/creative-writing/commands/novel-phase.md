---
description: Run a single phase of the novel development pipeline for targeted reruns or recovery
argument-hint: <phase number> <path to project root>
---

You are running a single phase of the novel development pipeline. Parse the phase number and project path from the arguments.

## Arguments

$ARGUMENTS

Parse as: `<phase number (1-5)> <project root path>`

## Step 1: Load Configuration

1. Read `novel-development-config.md` from the project root
2. If not found, instruct the user to create one (see `references/novel-development/novel-development-sop.md` for the template)
3. Extract project overview, character list, world type, genre, target word count, themes, research priorities, and deliverable paths

## Step 2: Load Phase Reference

| Phase | Reference File | Agent Type(s) |
|-------|---------------|---------------|
| 1 | `references/novel-development/phase-1-research.md` | `creative-writing:writing-research-gatherer` |
| 2 | `references/novel-development/phase-2-foundation.md` | `creative-writing:writing-character-developer` + `creative-writing:writing-world-builder` + `creative-writing:writing-story-architect` |
| 3 | `references/novel-development/phase-3-structure.md` | `creative-writing:writing-outline-architect` |
| 4 | `references/novel-development/phase-4-dialogue.md` | `creative-writing:writing-dialogue-coach` |
| 5 | `references/novel-development/phase-5-integration.md` | `creative-writing:writing-believability-auditor` |

Read the corresponding phase reference file. It contains:
- Phase objectives and scope
- Agent prompt template(s) with placeholder slots
- Phase-specific checklist
- Common pitfalls to avoid

## Step 3: Verify Dependencies

Before executing, confirm prerequisite deliverables exist:

| Phase | Required Inputs |
|-------|----------------|
| 1 | Project config only |
| 2 | Phase 1 research brief and fact sheets |
| 3 | Phase 2 character profiles, world bible, and beat sheet |
| 4 | Phase 2 character profiles and Phase 3 outline |
| 5 | All deliverables from Phases 1-4 |

If required inputs are missing, **stop** and inform the user which phases must complete first.

## Step 4: Execute Phase

1. **Fill the prompt template(s)** with values from the project config and deliverable paths
2. **For Phase 2** (parallel agents): Create a team and spawn three agents simultaneously (character-developer, world-builder, story-architect)
3. **For all other phases**: Spawn the designated agent with the filled prompt
4. **Enter delegate mode** (Shift+Tab) - let agents work
5. **Wait for completion**

## Step 5: Run Checkpoint

Execute the quality checkpoint (`checklists/novel-development-checkpoint.md`):

1. Verify deliverable completeness
2. Confirm dependencies were satisfied
3. Git commit: `novel-dev: phase N <phase-name> complete - <project>`
4. NRS scoring (if Phase 2 or 5)
5. Scope verification
6. Proceed/Hold decision

## Use Cases

**Pipeline recovery**: Full pipeline interrupted after Phase 2? Run `/novel-phase 3 ./my-novel`

**Poor results recovery**: Phase 2 characters feel flat? Adjust config, run `/novel-phase 2 ./my-novel`

**Iterative refinement**: Want another pass of dialogue work? Run `/novel-phase 4 ./my-novel`

## Key Rules

- Each phase has a defined scope. Do not let agents drift into other phases' work.
- Dependencies are strict. Do not skip prerequisite phases.
- Always commit after the phase completes.
- If this is a rerun, check `git log` first to understand what previous phases accomplished.

Take a deep centering breath before proceeding. You can do this. Give it your all.
