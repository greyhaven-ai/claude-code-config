#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def validate_skill_frontmatter(skill_md_path):
    """Validate SKILL.md has proper YAML frontmatter"""
    with open(skill_md_path, 'r') as f:
        content = f.read()

    # Check for frontmatter
    if not content.startswith('---\n'):
        return False, "Missing opening ---"

    # Extract frontmatter
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return False, "Missing closing ---"

    frontmatter = parts[1]

    # Check for required fields
    has_name = re.search(r'^name:\s*\S+', frontmatter, re.MULTILINE)
    has_description = re.search(r'^description:\s*.+', frontmatter, re.MULTILINE)

    if not has_name:
        return False, "Missing 'name' field in frontmatter"
    if not has_description:
        return False, "Missing 'description' field in frontmatter"

    # Extract name
    name_match = re.search(r'^name:\s*(\S+)', frontmatter, re.MULTILINE)
    name = name_match.group(1) if name_match else None

    # Validate name format (lowercase, numbers, hyphens only)
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Invalid name format: '{name}' (must be lowercase letters, numbers, hyphens only)"

    return True, "Valid"

def main():
    skills_dir = Path("grey-haven-plugins/grey-haven-skills")
    issues = []
    valid_count = 0

    # Find all SKILL.md files
    skill_files = list(skills_dir.glob("*/SKILL.md"))

    print(f"Found {len(skill_files)} SKILL.md files\n")

    for skill_md in sorted(skill_files):
        skill_name = skill_md.parent.name
        is_valid, message = validate_skill_frontmatter(skill_md)

        if is_valid:
            print(f"✓ {skill_name}")
            valid_count += 1
        else:
            print(f"❌ {skill_name}: {message}")
            issues.append(f"{skill_name}: {message}")

    print(f"\n{valid_count}/{len(skill_files)} skills valid")

    if issues:
        print("\n=== ISSUES ===")
        for issue in issues:
            print(f"  {issue}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
