---
name: tdd-orchestration
description: "Master TDD orchestration with multi-agent coordination, strict red-green-refactor enforcement, a Layer-0 domain-modeling gate (DDD) that blocks Red until concepts are named in domain vocabulary and primitives promoted to types, and principled DRY enforcement at Refactor (same-concept repetition ≥3 sites only). Automated test generation, coverage tracking, >90% coverage quality gates. Supports Claude Teams for parallel TDD workflows with plan approval gates, or falls back to sequential subagent coordination. Use when implementing features with TDD workflow, coordinating multiple TDD agents, enforcing test-first development, modeling a domain, orchestrating TDD teams, or when user mentions 'TDD workflow', 'test-first', 'TDD orchestration', 'multi-agent TDD', 'domain modeling', 'value object', 'ubiquitous language', 'DRY', 'test coverage', or 'red-green-refactor'."
# v2.0.43: Skills to auto-load for subagents (TDD language specialists)
skills:
  - tdd-typescript
  - tdd-python
  - test-generation
  - code-quality-analysis
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

Master TDD orchestrator ensuring strict red-green-refactor discipline with multi-agent coordination, a Layer-0 domain-modeling gate, and principled DRY enforcement at Refactor. Dual-mode: Claude Teams (preferred) for parallel work with plan approval, or sequential subagent delegation (fallback).

## Description

Orchestrates Test-Driven Development workflows sharpened by two lenses that never displace red-green-refactor — they gate it at plan review:

- **DDD at Layer 0** blocks Red until a Domain Model Plan is approved (concepts named in business vocabulary, entity vs. value object decided, primitive obsession audited, domain/infrastructure boundary drawn, test-name shapes using ubiquitous language).
- **DRY at Refactor** rejects extractions of ≤2 occurrences or of accidentally-similar syntax; deduplication is reserved for same-concept repetition at ≥3 sites.

## Discipline Layering (the task board)

```
Layer 0: Domain Model  — specialist plans concepts, types, boundaries; BLOCKS all Red
Layer 1: Red           — test-writer writes failing tests using domain vocabulary
Layer 2: Green         — implementer passes tests; domain types preserved
Layer 3: Refactor      — DRY discipline; promote primitives to value objects
Layer 4: Quality       — review
Layer 5: Integration   — integration tests
Layer 6: Synthesis     — final report
```

The orchestrator enforces both lenses at plan review — implementers apply them, the orchestrator validates them.

## What's Included

- **Examples**: Multi-agent TDD workflows with the Layer 0 gate, team-mode orchestration, Domain Model Plan samples
- **Reference**: TDD best practices, red-green-refactor patterns, coverage strategies, DDD building blocks
- **Templates**: Task board templates (Layers 0–6), test planning structures, Domain Model Plan template
- **Checklists**: Domain Model plan approval, Red/Green/Refactor review, DRY discipline, coverage validation

## Use This Skill When

- Implementing features with strict TDD methodology
- Modeling a domain before the first test (entities, value objects, aggregates)
- Coordinating multiple agents in TDD workflow
- Enforcing test-first development with ubiquitous language
- Achieving >90% test coverage
- Refactoring with principled DRY (avoiding premature abstractions)
- Orchestrating TDD teams with parallel component work
- Managing plan approval gates for TDD + DDD compliance

## Related Agents

- `tdd-orchestrator` - Multi-agent TDD coordinator (team + subagent modes, Layer-0 gate)
- `tdd-typescript-implementer` - TypeScript/JavaScript TDD with branded types
- `tdd-python-implementer` - Python TDD with Pydantic / NewType / frozen dataclasses
- `test-generator` - Automated test creation
- `code-quality-analyzer` - Code quality review

---

**Skill Version**: 2.1
