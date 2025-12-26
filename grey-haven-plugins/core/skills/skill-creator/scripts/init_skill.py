#!/usr/bin/env python3
"""
Grey Haven Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path grey-haven-plugins/core/skills
    init_skill.py api-helper --path grey-haven-plugins/developer-experience/skills
"""

import sys
from pathlib import Path
from datetime import datetime

SKILL_TEMPLATE = """---
name: grey-haven-{skill_name}
description: "[TODO: What this skill does. When to use it. Include trigger phrases like: 'Triggers: phrase1, phrase2, phrase3'.]"
# v2.0.43: Skills to auto-load when this skill activates
skills:
  - grey-haven-code-style
# v2.0.74: Tools available when skill is active
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# {skill_title}

[TODO: 1-2 sentence overview of what this skill enables]

## Overview

[TODO: Brief description of the skill's purpose and capabilities]

## What's Included

### Examples (`examples/`)
- [TODO: List example files and what they demonstrate]

### Reference Guides (`reference/`)
- [TODO: List reference files and when to use them]

### Templates (`templates/`)
- [TODO: List template files if applicable]

### Checklists (`checklists/`)
- [TODO: List checklist files if applicable]

## Key Concepts

[TODO: Core concepts the skill teaches or implements]

## Workflow

[TODO: Step-by-step workflow for using this skill]

1. Step one
2. Step two
3. Step three

## Use This Skill When

- [TODO: Trigger scenario 1]
- [TODO: Trigger scenario 2]
- [TODO: Trigger scenario 3]

## Related Skills

- [TODO: Related skill 1]
- [TODO: Related skill 2]

## Quick Start

```bash
# TODO: Add quick start commands
cat examples/basic-example.md
```

---

**Skill Version**: 1.0
**Last Updated**: {date}
"""

EXAMPLE_FILE = """# Example: Basic Usage

This example demonstrates the core functionality of {skill_title}.

## Scenario

[TODO: Describe the scenario]

## Input

```
[TODO: Example input]
```

## Expected Output

```
[TODO: Expected output]
```

## Key Points

- [TODO: Key point 1]
- [TODO: Key point 2]
"""

REFERENCE_FILE = """# Reference Guide

Detailed documentation for {skill_title}.

## Table of Contents

1. [Overview](#overview)
2. [Configuration](#configuration)
3. [API Reference](#api-reference)
4. [Troubleshooting](#troubleshooting)

## Overview

[TODO: Detailed overview]

## Configuration

[TODO: Configuration options]

## API Reference

[TODO: API details if applicable]

## Troubleshooting

[TODO: Common issues and solutions]
"""

CHECKLIST_FILE = """# {skill_title} Checklist

Validation checklist for quality assurance.

## Pre-Flight Checks (Score: /25)

- [ ] [TODO: Check 1] (5 pts)
- [ ] [TODO: Check 2] (5 pts)
- [ ] [TODO: Check 3] (5 pts)
- [ ] [TODO: Check 4] (5 pts)
- [ ] [TODO: Check 5] (5 pts)

## Quality Validation (Score: /25)

- [ ] [TODO: Quality check 1] (5 pts)
- [ ] [TODO: Quality check 2] (5 pts)
- [ ] [TODO: Quality check 3] (5 pts)
- [ ] [TODO: Quality check 4] (5 pts)
- [ ] [TODO: Quality check 5] (5 pts)

---

## Scoring Guide

| Score | Rating | Action |
|-------|--------|--------|
| 45-50 | Excellent | Ready for use |
| 35-44 | Good | Minor improvements needed |
| 25-34 | Needs Work | Address gaps |
| <25 | Critical | Major rework required |
"""


def title_case(skill_name: str) -> str:
    """Convert hyphenated skill name to Title Case."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name: str, path: str) -> Path | None:
    """
    Initialize a new Grey Haven skill directory.

    Args:
        skill_name: Name of the skill (hyphen-case)
        path: Path where skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    skill_dir = Path(path).resolve() / skill_name

    # Check if exists
    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case(skill_name)
    date = datetime.now().strftime("%Y-%m-%d")

    # Create SKILL.md
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
        date=date
    )

    try:
        (skill_dir / 'SKILL.md').write_text(skill_content)
        print("Created SKILL.md")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # examples/
        examples_dir = skill_dir / 'examples'
        examples_dir.mkdir(exist_ok=True)
        (examples_dir / 'basic-example.md').write_text(
            EXAMPLE_FILE.format(skill_title=skill_title)
        )
        print("Created examples/basic-example.md")

        # reference/
        reference_dir = skill_dir / 'reference'
        reference_dir.mkdir(exist_ok=True)
        (reference_dir / 'reference-guide.md').write_text(
            REFERENCE_FILE.format(skill_title=skill_title)
        )
        print("Created reference/reference-guide.md")

        # checklists/
        checklists_dir = skill_dir / 'checklists'
        checklists_dir.mkdir(exist_ok=True)
        (checklists_dir / 'validation-checklist.md').write_text(
            CHECKLIST_FILE.format(skill_title=skill_title)
        )
        print("Created checklists/validation-checklist.md")

    except Exception as e:
        print(f"Error creating resource directories: {e}")
        return None

    print(f"\nSkill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md - complete all TODO items")
    print("2. Update the description with trigger phrases")
    print("3. Customize or delete example files")
    print("4. Add skill to plugin.json")
    print(f"   \"./skills/{skill_name}\"")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("\nSkill name requirements:")
        print("  - Hyphen-case (e.g., 'data-analyzer')")
        print("  - Lowercase letters, digits, hyphens")
        print("  - Max 40 characters")
        print("\nExamples:")
        print("  init_skill.py my-skill --path grey-haven-plugins/core/skills")
        print("  init_skill.py api-helper --path grey-haven-plugins/developer-experience/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"Initializing Grey Haven skill: {skill_name}")
    print(f"Location: {path}\n")

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
