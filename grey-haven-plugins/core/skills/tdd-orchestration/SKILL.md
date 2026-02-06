---
name: grey-haven-tdd-orchestration
description: "Master TDD orchestration with multi-agent coordination, strict red-green-refactor enforcement, automated test generation, coverage tracking, and >90% coverage quality gates. Supports Claude Teams for parallel TDD workflows with plan approval gates, or falls back to sequential subagent coordination. Coordinates tdd-python, tdd-typescript, and test-generator agents. Use when implementing features with TDD workflow, coordinating multiple TDD agents, enforcing test-first development, orchestrating TDD teams, or when user mentions 'TDD workflow', 'test-first', 'TDD orchestration', 'multi-agent TDD', 'test coverage', or 'red-green-refactor'."
# v2.0.43: Skills to auto-load for subagents (TDD language specialists)
skills:
  - grey-haven-tdd-typescript
  - grey-haven-tdd-python
  - grey-haven-test-generation
  - grey-haven-code-quality-analysis
# v2.0.74: Orchestrator needs full tool access for coordination
# v2.1.0: Added team tools for Claude Teams support
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
  - Teammate
  - SendMessage
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
---

# TDD Orchestration Skill

Master TDD orchestrator ensuring strict red-green-refactor discipline with multi-agent coordination and comprehensive metrics. Supports dual-mode operation: Claude Teams (preferred) with parallel task execution and plan approval, or sequential subagent delegation (fallback).

## Description

Orchestrates Test-Driven Development workflows with automated test generation, implementation coordination, coverage tracking, and quality gates. In team mode, spawns specialist teammates (test-writer, implementer, quality reviewer) with file ownership boundaries and layered task dependencies for parallel TDD execution.

## What's Included

- **Examples**: Multi-agent TDD workflows, feature implementation with TDD, team-mode orchestration
- **Reference**: TDD best practices, red-green-refactor patterns, coverage strategies
- **Templates**: TDD workflow templates, test planning structures, team task boards
- **Checklists**: TDD verification, coverage validation, plan approval criteria

## Use This Skill When

- Implementing features with strict TDD methodology
- Coordinating multiple agents in TDD workflow
- Enforcing test-first development
- Achieving >90% test coverage
- Orchestrating TDD teams with parallel component work
- Managing plan approval gates for TDD compliance

## Related Agents

- `tdd-orchestrator` - Multi-agent TDD coordinator (team + subagent modes)
- `tdd-typescript-implementer` - TypeScript/JavaScript TDD
- `tdd-python-implementer` - Python TDD
- `test-generator` - Automated test creation
- `code-quality-analyzer` - Code quality review

---

**Skill Version**: 2.0
