---
name: tdd-typescript
description: "TypeScript/JavaScript Test-Driven Development with Vitest, strict red-green-refactor methodology, domain-first modeling (DDD) via branded types, principled DRY discipline, React component testing, and comprehensive coverage patterns. Use when implementing TypeScript features with TDD, writing Vitest tests, testing React components, developing with test-first approach, modeling domain concepts, refactoring duplication, or when user mentions 'TypeScript TDD', 'Vitest', 'React testing', 'JavaScript TDD', 'red-green-refactor', 'TypeScript unit tests', 'branded types', 'value object', 'ubiquitous language', 'DRY', or 'test-driven TypeScript'."
# v2.0.43: Skills to auto-load for subagents spawned from this skill
skills:
  - code-style
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

# TDD TypeScript Skill

TypeScript/JavaScript TDD using strict red-green-refactor with Vitest — sharpened by **DDD at Red** (model the domain with branded types) and **DRY at Refactor** (deduplicate same-concept repetition only).

## Description

Implement features by writing failing tests first, minimal code to pass, then refactoring. Types *are* the first test; branded types extend that to catch domain errors the compiler wouldn't otherwise see.

## Discipline Layering

- **Before Red — Model the Domain**: Name the entity, value object, or aggregate in the business's language. Use **branded types** for primitives that carry rules (`type EmailAddress = string & { readonly __brand: 'EmailAddress' }`). Prefer `readonly` classes or frozen records for multi-field value objects. Zod/Valibot schemas inferred into branded types give runtime + compile-time safety.
- **Red**: Write a failing test. Name it in domain terms (`it('rejects refund when amount exceeds daily limit')`) — not mechanical (`it('returns false')`).
- **Green**: Minimal code to pass.
- **Refactor — DRY with discipline**: Deduplicate only when the *same domain concept* appears ≥3 times with the same meaning. Distinguish true DRY from accidental similarity (same shape, different meaning). Promote recurring primitives to branded types. Keep domain logic out of components, routes, and stores.

## What's Included

- **Examples**: TDD cycles, React component TDD, branded-type value objects, utility function TDD
- **Reference**: Red-green-refactor patterns, Vitest best practices, branded-type idioms
- **Templates**: Test templates, implementation workflows

## Use When

- Implementing TypeScript features with TDD
- Modeling domain concepts (entities, value objects, aggregates) with branded types
- React component development (keeping domain logic out of components)
- Refactoring duplication after a green test
- Ensuring high test coverage

## Related Agents

- `tdd-typescript-implementer`

**Skill Version**: 1.1
