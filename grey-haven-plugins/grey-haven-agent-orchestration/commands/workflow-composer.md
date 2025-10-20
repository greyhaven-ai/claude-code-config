---
name: workflow-composer
description: Compose multi-agent workflows with explicit phase definitions, agent sequences, and handoff criteria. Define complex orchestration patterns declaratively.
---

# Workflow Composer - Multi-Agent Orchestration

Design and execute multi-agent workflows with explicit coordination.

## Usage

```bash
/workflow-composer [workflow-definition-file or inline-description]
```

## Workflow Definition Format

```yaml
name: feature-development
description: End-to-end feature implementation workflow

phases:
  - name: requirements
    agents: [product-manager, backend-architect]
    outputs: [requirements.md, api-spec.yaml]
    
  - name: implementation
    agents: [tdd-python-implementer, frontend-developer]
    dependencies: [requirements]
    parallel: true
    
  - name: review
    agents: [code-quality-analyzer, security-analyzer]
    dependencies: [implementation]
    
  - name: deployment
    agents: [devops-engineer]
    dependencies: [review]

handoff_criteria:
  - from: requirements
    to: implementation
    condition: "API spec approved"
    
  - from: implementation
    to: review
    condition: "All tests passing"
```

## Features

- **Phase sequencing:** Define order and dependencies
- **Parallel execution:** Run multiple agents concurrently
- **Conditional handoffs:** Gate progression on criteria
- **Context preservation:** Auto-save at phase boundaries
- **Error recovery:** Checkpoint and rollback support

## Example

```bash
/workflow-composer feature-auth-api.yaml
```

Executes multi-phase workflow with automatic agent coordination and context handoff.

## Built-in Templates

- `/workflow-composer templates list` - Show available templates
- `/workflow-composer templates feature` - Full-stack feature template
- `/workflow-composer templates bugfix` - Debug and fix template
- `/workflow-composer templates refactor` - Code refactoring template
