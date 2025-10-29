---
name: context-restore
description: Restore previously saved workflow context to resume interrupted tasks or continue from agent handoff.
---

# Context Restore - Workflow Resumption

Restore saved context from `.claude/context/` to resume workflow.

## Usage

```bash
/context-restore [workflow-name or context-file]
```

## What Gets Restored

- File references and modification history
- Task list with current progress
- Historical decisions and rationale
- Pending actions queue
- Recommended next agent
- Original workflow metadata

## Example

```bash
/context-restore feature-auth-api-20250113-154530
```

Loads context and displays:
- Workflow summary
- Current phase
- Modified files
- Next steps
- Suggested agent
