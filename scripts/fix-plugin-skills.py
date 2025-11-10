#!/usr/bin/env python3
"""
Fix plugin.json files by automatically adding all skills from skills/ directory.

Usage:
    python scripts/fix-plugin-skills.py [--dry-run]
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def find_plugins(base_dir: Path) -> List[Path]:
    """Find all plugin directories."""
    plugins = []
    if not base_dir.exists():
        print(f"{RED}Error: {base_dir} does not exist{RESET}")
        return plugins

    for item in base_dir.iterdir():
        if item.is_dir():
            plugin_json = item / '.claude-plugin' / 'plugin.json'
            if plugin_json.exists():
                plugins.append(item)

    return sorted(plugins)


def get_actual_skills(plugin_dir: Path) -> List[str]:
    """Get list of actual skills in the skills/ directory."""
    skills_dir = plugin_dir / 'skills'
    if not skills_dir.exists():
        return []

    skills = []
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            skill_md = item / 'SKILL.md'
            if skill_md.exists():
                skills.append(f"./skills/{item.name}")

    return skills


def get_declared_skills(plugin_json_path: Path) -> Tuple[List[str], Dict]:
    """Get list of skills declared in plugin.json and return the full config."""
    with open(plugin_json_path, 'r') as f:
        config = json.load(f)

    declared = config.get('skills', [])
    return declared, config


def update_plugin_json(plugin_json_path: Path, actual_skills: List[str], dry_run: bool = False) -> bool:
    """Update plugin.json with actual skills."""
    with open(plugin_json_path, 'r') as f:
        config = json.load(f)

    old_skills = config.get('skills', [])

    # Only update if there's a change
    if set(old_skills) == set(actual_skills):
        return False

    # Update skills array
    if actual_skills:
        config['skills'] = actual_skills
    elif 'skills' in config:
        # Remove empty skills array
        del config['skills']

    if not dry_run:
        with open(plugin_json_path, 'w') as f:
            json.dump(config, f, indent=4)
            f.write('\n')  # Add trailing newline

    return True


def main():
    dry_run = '--dry-run' in sys.argv

    print(f"{BOLD}=== Plugin Skills Fix Tool ==={RESET}\n")

    if dry_run:
        print(f"{YELLOW}Running in DRY RUN mode - no files will be modified{RESET}\n")

    # Find the plugins directory
    base_dir = Path(__file__).parent.parent / 'grey-haven-plugins'

    if not base_dir.exists():
        print(f"{RED}Error: grey-haven-plugins directory not found at {base_dir}{RESET}")
        sys.exit(1)

    plugins = find_plugins(base_dir)

    if not plugins:
        print(f"{RED}No plugins found in {base_dir}{RESET}")
        sys.exit(1)

    print(f"Found {len(plugins)} plugins\n")

    fixed_count = 0
    up_to_date_count = 0

    for plugin_dir in plugins:
        plugin_name = plugin_dir.name
        plugin_json_path = plugin_dir / '.claude-plugin' / 'plugin.json'

        # Get actual skills in directory
        actual_skills = get_actual_skills(plugin_dir)

        # Get declared skills in plugin.json
        declared_skills, config = get_declared_skills(plugin_json_path)

        # Calculate differences
        missing = set(actual_skills) - set(declared_skills)
        extra = set(declared_skills) - set(actual_skills)

        if not missing and not extra:
            print(f"{GREEN}✓{RESET} {BOLD}{plugin_name}{RESET}")
            print(f"  Skills: {len(actual_skills)} (up to date)")
            up_to_date_count += 1
        else:
            print(f"{YELLOW}⚠{RESET} {BOLD}{plugin_name}{RESET}")
            print(f"  Declared: {len(declared_skills)} | Actual: {len(actual_skills)}")

            if missing:
                print(f"  {RED}Missing from plugin.json:{RESET}")
                for skill in sorted(missing):
                    print(f"    + {skill}")

            if extra:
                print(f"  {YELLOW}Extra in plugin.json (not found):{RESET}")
                for skill in sorted(extra):
                    print(f"    - {skill}")

            # Fix the plugin.json
            if update_plugin_json(plugin_json_path, actual_skills, dry_run):
                if dry_run:
                    print(f"  {BLUE}Would update plugin.json{RESET}")
                else:
                    print(f"  {GREEN}Updated plugin.json{RESET}")
                fixed_count += 1

        print()

    # Summary
    print(f"{BOLD}=== Summary ==={RESET}")
    print(f"Total plugins: {len(plugins)}")
    print(f"{GREEN}Up to date: {up_to_date_count}{RESET}")
    print(f"{YELLOW}Fixed: {fixed_count}{RESET}")

    if dry_run and fixed_count > 0:
        print(f"\n{BLUE}Run without --dry-run to apply changes{RESET}")
    elif fixed_count > 0:
        print(f"\n{GREEN}All plugin.json files updated successfully!{RESET}")
    else:
        print(f"\n{GREEN}All plugins are already up to date!{RESET}")


if __name__ == '__main__':
    main()
