---
name: tdd-python
description: "Python Test-Driven Development expertise with pytest, strict red-green-refactor methodology, domain-first modeling (DDD), principled DRY discipline, FastAPI testing patterns, and Pydantic model testing. Use when implementing Python features with TDD, writing pytest tests, testing FastAPI endpoints, developing with test-first approach, modeling domain concepts, refactoring duplication, or when user mentions 'Python TDD', 'pytest', 'FastAPI testing', 'red-green-refactor', 'Python unit tests', 'test-driven Python', 'domain modeling', 'value object', 'ubiquitous language', 'DRY', or 'Python test coverage'."
# v2.0.43: Skills to auto-load for subagents spawned from this skill
skills:
  - code-style
  - api-design-standards
  - test-generation
# v2.0.74: Restrict tools available when this skill is active
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# TDD Python Skill

Python Test-Driven Development following strict red-green-refactor cycle with pytest — sharpened by **DDD at Red** (model the domain first) and **DRY at Refactor** (deduplicate same-concept repetition only).

## Description

Systematic Python implementation using TDD methodology. Tests are written first and drive design; domain vocabulary drives the tests; duplication is removed only when the *same concept* repeats, not when syntax coincidentally looks alike.

## Discipline Layering

- **Before Red — Model the Domain**: Name the entity, value object, or aggregate in the business's language. Decide entity vs. value object. Reject primitive obsession — wrap `str`/`int` in `EmailAddress`, `Money`, `NewType`, or `pydantic.BaseModel` when they carry rules. Keep domain logic out of FastAPI routes.
- **Red**: Write a failing test. Name it in domain terms (`test_rejects_refund_when_amount_exceeds_daily_limit`) — never mechanical (`test_returns_false`).
- **Green**: Minimal code to pass. No speculative abstractions.
- **Refactor — DRY with discipline**: Deduplicate only when the *same domain concept* appears ≥3 times with the same meaning. Three similar lines beats a premature abstraction. Promote recurring primitives to value objects. When uncertain, inline.

## What's Included

- **Examples**: Python TDD cycles, FastAPI TDD, Pydantic model TDD, value-object modeling
- **Reference**: pytest patterns, Python testing best practices, branded-type idioms (`NewType`, `frozen=True`)
- **Templates**: pytest templates, TDD workflows

## Use When

- Implementing Python features with TDD
- Modeling domain concepts (entities, value objects, aggregates)
- FastAPI endpoint development (keeping domain rules out of routes)
- Pydantic model development
- Refactoring duplication after a green test

## Related Agents

- `tdd-python-implementer`

**Skill Version**: 1.1
