---
name: context-save
description: Save current workflow context for later restoration or agent handoff. Preserves task state, modified files, decisions, and pending actions.
---

# Context Save - Workflow State Persistence

Save current conversation and task context to `.claude/context/` for resumption or handoff.

## Usage

```bash
/context-save [workflow-name]
```

## What Gets Saved

- Modified files and their states
- Current task list and completion status
- Decisions made during workflow
- Pending actions and next steps
- Active agent and suggested next agent
- Timestamp and session metadata

## Output Location

`.claude/context/{workflow-name}-{timestamp}.json`

## Example

```bash
/context-save feature-auth-api
```

Creates: `.claude/context/feature-auth-api-20250113-154530.json`
