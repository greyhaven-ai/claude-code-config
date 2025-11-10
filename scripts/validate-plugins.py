#!/usr/bin/env python3
"""
Validate plugins against Claude Code best practices.

Checks:
- Plugin structure (directories, plugin.json)
- Skills array completeness
- Agent descriptions and frontmatter
- Skill descriptions and triggers
- Command structure
- File naming conventions
- Tool access patterns
- Documentation quality (NEW!)
- Cross-reference validation (NEW!)

Usage:
    python scripts/validate-plugins.py [--verbose] [--plugin=NAME] [--json]

Options:
    --verbose, -v    Show detailed validation results
    --plugin=NAME    Validate specific plugin only
    --json           Output results in JSON format (for CI/CD)
"""

import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


class ValidationResult:
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def add_error(self, message: str):
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_pass(self, message: str):
        self.passed.append(message)

    @property
    def score(self) -> int:
        """Calculate score: 0 (worst) to 100 (perfect)."""
        total = len(self.errors) + len(self.warnings) + len(self.passed)
        if total == 0:
            return 0
        points = len(self.passed) - len(self.errors) * 2 - len(self.warnings)
        return max(0, min(100, int((points / total) * 100)))

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "plugin": self.plugin_name,
            "score": self.score,
            "errors": self.errors,
            "warnings": self.warnings,
            "passed": self.passed,
            "totals": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "passed": len(self.passed)
            }
        }

    def print_results(self, verbose: bool = False):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}Plugin: {self.plugin_name}{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        if self.errors:
            print(f"\n{RED}{BOLD}❌ Errors ({len(self.errors)}):{RESET}")
            for error in self.errors:
                print(f"  {RED}•{RESET} {error}")

        if self.warnings:
            print(f"\n{YELLOW}{BOLD}⚠️  Warnings ({len(self.warnings)}):{RESET}")
            for warning in self.warnings:
                print(f"  {YELLOW}•{RESET} {warning}")

        if verbose and self.passed:
            print(f"\n{GREEN}{BOLD}✓ Passed ({len(self.passed)}):{RESET}")
            for passed in self.passed:
                print(f"  {GREEN}•{RESET} {passed}")

        # Score
        score = self.score
        if score >= 90:
            color = GREEN
        elif score >= 70:
            color = YELLOW
        else:
            color = RED

        print(f"\n{BOLD}Score: {color}{score}/100{RESET}")


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter, body
    except yaml.YAMLError:
        return None, content


def validate_plugin_structure(plugin_dir: Path, result: ValidationResult):
    """Validate basic plugin structure."""
    # Check .claude-plugin directory
    claude_plugin_dir = plugin_dir / '.claude-plugin'
    if not claude_plugin_dir.exists():
        result.add_error(".claude-plugin directory missing")
        return
    result.add_pass(".claude-plugin directory exists")

    # Check plugin.json
    plugin_json_path = claude_plugin_dir / 'plugin.json'
    if not plugin_json_path.exists():
        result.add_error("plugin.json missing")
        return
    result.add_pass("plugin.json exists")

    # Validate plugin.json is valid JSON
    try:
        with open(plugin_json_path, 'r') as f:
            config = json.load(f)
        result.add_pass("plugin.json is valid JSON")
    except json.JSONDecodeError as e:
        result.add_error(f"plugin.json is invalid JSON: {e}")
        return

    # Check required fields
    if 'name' not in config:
        result.add_error("plugin.json missing 'name' field")
    else:
        name = config['name']
        if not re.match(r'^[a-z0-9-]+$', name):
            result.add_error(f"plugin.json name '{name}' should be kebab-case")
        else:
            result.add_pass(f"plugin.json name '{name}' is kebab-case")

    if 'description' not in config:
        result.add_warning("plugin.json missing 'description' field")
    else:
        result.add_pass("plugin.json has description")

    if 'version' not in config:
        result.add_warning("plugin.json missing 'version' field")
    else:
        version = config['version']
        if not re.match(r'^\d+\.\d+\.\d+', version):
            result.add_warning(f"version '{version}' should follow semver (e.g., 1.0.0)")
        else:
            result.add_pass(f"version '{version}' follows semver")

    return config


def validate_skills_array(plugin_dir: Path, config: Dict, result: ValidationResult):
    """Validate skills array matches actual skills directory."""
    skills_dir = plugin_dir / 'skills'

    # Get actual skills
    actual_skills = []
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir():
                skill_md = item / 'SKILL.md'
                if skill_md.exists():
                    actual_skills.append(f"./skills/{item.name}")

    # Get declared skills
    declared_skills = config.get('skills', [])

    if not actual_skills and not declared_skills:
        result.add_pass("No skills (intentional)")
        return

    if not actual_skills and declared_skills:
        result.add_error(f"plugin.json declares {len(declared_skills)} skills but skills/ directory is empty or missing")
        return

    if actual_skills and not declared_skills:
        result.add_error(f"Found {len(actual_skills)} skills in skills/ but none declared in plugin.json")
        return

    # Check for mismatches
    missing = set(actual_skills) - set(declared_skills)
    extra = set(declared_skills) - set(actual_skills)

    if missing:
        result.add_error(f"Skills missing from plugin.json: {', '.join(sorted(missing))}")

    if extra:
        result.add_error(f"Skills in plugin.json but not found: {', '.join(sorted(extra))}")

    if not missing and not extra:
        result.add_pass(f"All {len(actual_skills)} skills properly declared")


def validate_agent(agent_path: Path, result: ValidationResult):
    """Validate an individual agent file."""
    with open(agent_path, 'r') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        result.add_warning(f"Agent {agent_path.name} missing frontmatter")
        return

    # Check required fields
    if 'name' not in frontmatter:
        result.add_error(f"Agent {agent_path.name} missing 'name' field")
    else:
        result.add_pass(f"Agent {agent_path.name} has name")

    if 'description' not in frontmatter:
        result.add_error(f"Agent {agent_path.name} missing 'description' field")
    else:
        desc = frontmatter['description']

        # Check for trigger phrases
        trigger_patterns = [
            r'use\s+(when|after|before|proactively)',
            r'must\s+be\s+used',
            r'automatically\s+invoked',
            r'use\s+for'
        ]

        has_trigger = any(re.search(pattern, desc.lower()) for pattern in trigger_patterns)

        if not has_trigger:
            result.add_warning(f"Agent {agent_path.name} description lacks clear trigger phrases (e.g., 'Use when...', 'Use PROACTIVELY...')")
        else:
            result.add_pass(f"Agent {agent_path.name} has trigger phrases")

    # Check if agent is too long
    line_count = len(body.split('\n'))
    if line_count > 300:
        result.add_warning(f"Agent {agent_path.name} is {line_count} lines (consider splitting if > 300)")

    # Check for model specification
    if 'model' not in frontmatter:
        result.add_warning(f"Agent {agent_path.name} missing 'model' field (consider adding opus/haiku)")


def validate_agents(plugin_dir: Path, result: ValidationResult, verbose: bool = False):
    """Validate all agents in the plugin."""
    agents_dir = plugin_dir / 'agents'

    if not agents_dir.exists():
        result.add_pass("No agents directory (optional)")
        return

    agent_files = list(agents_dir.glob('*.md'))

    if not agent_files:
        result.add_warning("agents/ directory exists but is empty")
        return

    # Check for old files
    old_files = [f for f in agent_files if '-old' in f.stem]
    if old_files:
        result.add_warning(f"Found {len(old_files)} old agent files: {', '.join(f.name for f in old_files)}")

    # Validate each agent
    active_agents = [f for f in agent_files if '-old' not in f.stem]

    if verbose:
        for agent_file in active_agents:
            validate_agent(agent_file, result)
    else:
        result.add_pass(f"Found {len(active_agents)} agent(s)")


def validate_skill(skill_dir: Path, result: ValidationResult):
    """Validate an individual skill."""
    skill_md = skill_dir / 'SKILL.md'

    if not skill_md.exists():
        result.add_error(f"Skill {skill_dir.name} missing SKILL.md")
        return

    with open(skill_md, 'r') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        result.add_error(f"Skill {skill_dir.name} missing frontmatter")
        return

    # Check required fields
    if 'name' not in frontmatter:
        result.add_error(f"Skill {skill_dir.name} missing 'name' field")
    else:
        name = frontmatter['name']
        if len(name) > 64:
            result.add_error(f"Skill {skill_dir.name} name too long (>{64} chars)")
        if not re.match(r'^[a-z0-9-]+$', name):
            result.add_warning(f"Skill {skill_dir.name} name should be lowercase kebab-case")

    if 'description' not in frontmatter:
        result.add_error(f"Skill {skill_dir.name} missing 'description' field")
    else:
        desc = frontmatter['description']

        if len(desc) > 1024:
            result.add_error(f"Skill {skill_dir.name} description too long (>{1024} chars)")

        # Check for trigger phrases
        trigger_keywords = ['use when', 'when user', 'when working', 'when mentioned', 'mentions']
        has_trigger = any(keyword in desc.lower() for keyword in trigger_keywords)

        if not has_trigger:
            result.add_warning(f"Skill {skill_dir.name} description should include activation triggers")


def validate_skills(plugin_dir: Path, result: ValidationResult, verbose: bool = False):
    """Validate all skills in the plugin."""
    skills_dir = plugin_dir / 'skills'

    if not skills_dir.exists():
        result.add_pass("No skills directory (optional)")
        return

    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]

    if not skill_dirs:
        result.add_warning("skills/ directory exists but is empty")
        return

    if verbose:
        for skill_dir in skill_dirs:
            validate_skill(skill_dir, result)
    else:
        result.add_pass(f"Found {len(skill_dirs)} skill(s)")


def validate_commands(plugin_dir: Path, result: ValidationResult):
    """Validate commands in the plugin."""
    commands_dir = plugin_dir / 'commands'

    if not commands_dir.exists():
        result.add_pass("No commands directory (optional)")
        return

    # Commands can be either .md files or directories with .md files
    command_files = list(commands_dir.glob('*.md'))
    command_dirs = [d for d in commands_dir.iterdir() if d.is_dir()]

    # For directories, look for the main .md file
    for cmd_dir in command_dirs:
        main_md = cmd_dir / f"{cmd_dir.name}.md"
        if main_md.exists():
            command_files.append(main_md)

    if not command_files:
        result.add_warning("commands/ directory exists but no command files found")
        return

    result.add_pass(f"Found {len(command_files)} command(s)")


def validate_skill_documentation(skill_dir: Path, result: ValidationResult):
    """Validate skill documentation structure and completeness."""
    skill_name = skill_dir.name

    # Check for standard documentation directories
    standard_dirs = ['examples', 'reference', 'templates', 'checklists']
    found_dirs = []

    for dir_name in standard_dirs:
        if (skill_dir / dir_name).exists():
            found_dirs.append(dir_name)

    if not found_dirs:
        result.add_warning(f"Skill {skill_name}: No documentation directories (consider adding examples/, reference/)")
        return

    # Validate each documentation directory
    for dir_name in found_dirs:
        doc_dir = skill_dir / dir_name

        # Check for INDEX.md
        index_md = doc_dir / 'INDEX.md'
        if not index_md.exists():
            result.add_warning(f"Skill {skill_name}: {dir_name}/ missing INDEX.md")
        else:
            result.add_pass(f"Skill {skill_name}: {dir_name}/ has INDEX.md")

        # Check for actual content files
        md_files = list(doc_dir.glob('*.md'))
        if dir_name != 'templates':  # Templates can be various formats
            content_files = [f for f in md_files if f.name != 'INDEX.md']

            if not content_files:
                result.add_warning(f"Skill {skill_name}: {dir_name}/ has INDEX.md but no content files")
            else:
                result.add_pass(f"Skill {skill_name}: {dir_name}/ has {len(content_files)} content file(s)")

    # Check for checklists in high-value categories
    high_value_keywords = ['security', 'authentication', 'validation', 'profiling', 'observability', 'quality', 'performance', 'tdd']
    is_high_value = any(keyword in skill_name.lower() for keyword in high_value_keywords)

    if is_high_value and 'checklists' not in found_dirs:
        result.add_warning(f"Skill {skill_name}: High-value skill should have checklists/")


def validate_documentation_links(file_path: Path, result: ValidationResult):
    """Validate that links in documentation point to existing files."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except:
        return

    # Find markdown links [text](path)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, content)

    broken_links = []
    for text, link in matches:
        # Skip external links (http, https, mailto)
        if link.startswith(('http://', 'https://', 'mailto:', '#')):
            continue

        # Resolve relative path
        link_path = (file_path.parent / link).resolve()

        if not link_path.exists():
            broken_links.append(f"{text} -> {link}")

    if broken_links:
        result.add_warning(f"{file_path.name}: {len(broken_links)} broken link(s): {', '.join(broken_links[:3])}")


def validate_documentation_quality(plugin_dir: Path, result: ValidationResult, verbose: bool = False):
    """Validate documentation quality for all skills."""
    skills_dir = plugin_dir / 'skills'

    if not skills_dir.exists():
        return

    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]

    for skill_dir in skill_dirs:
        if verbose:
            validate_skill_documentation(skill_dir, result)

            # Check links in SKILL.md
            skill_md = skill_dir / 'SKILL.md'
            if skill_md.exists():
                validate_documentation_links(skill_md, result)

            # Check links in documentation files
            for doc_dir_name in ['examples', 'reference', 'checklists']:
                doc_dir = skill_dir / doc_dir_name
                if doc_dir.exists():
                    for md_file in doc_dir.glob('*.md'):
                        validate_documentation_links(md_file, result)


def validate_plugin(plugin_dir: Path, verbose: bool = False) -> ValidationResult:
    """Run all validations on a plugin."""
    result = ValidationResult(plugin_dir.name)

    # 1. Validate structure
    config = validate_plugin_structure(plugin_dir, result)
    if config is None:
        return result

    # 2. Validate skills array
    validate_skills_array(plugin_dir, config, result)

    # 3. Validate agents
    validate_agents(plugin_dir, result, verbose)

    # 4. Validate skills
    validate_skills(plugin_dir, result, verbose)

    # 5. Validate commands
    validate_commands(plugin_dir, result)

    # 6. Validate documentation quality (new!)
    validate_documentation_quality(plugin_dir, result, verbose)

    return result


def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    json_output = '--json' in sys.argv
    specific_plugin = None

    for arg in sys.argv[1:]:
        if arg.startswith('--plugin='):
            specific_plugin = arg.split('=')[1]

    if not json_output:
        print(f"{BOLD}=== Claude Code Plugin Validator ==={RESET}\n")

    # Find the plugins directory
    base_dir = Path(__file__).parent.parent / 'grey-haven-plugins'

    if not base_dir.exists():
        if json_output:
            print(json.dumps({"error": "grey-haven-plugins directory not found"}, indent=2))
        else:
            print(f"{RED}Error: grey-haven-plugins directory not found at {base_dir}{RESET}")
        sys.exit(1)

    # Get plugins to validate
    if specific_plugin:
        plugin_dir = base_dir / specific_plugin
        if not plugin_dir.exists():
            if json_output:
                print(json.dumps({"error": f"Plugin '{specific_plugin}' not found"}, indent=2))
            else:
                print(f"{RED}Error: Plugin '{specific_plugin}' not found{RESET}")
            sys.exit(1)
        plugins = [plugin_dir]
    else:
        plugins = sorted([d for d in base_dir.iterdir() if d.is_dir() and (d / '.claude-plugin').exists()])

    if not plugins:
        if json_output:
            print(json.dumps({"error": "No plugins found"}, indent=2))
        else:
            print(f"{RED}No plugins found{RESET}")
        sys.exit(1)

    if not json_output:
        print(f"Validating {len(plugins)} plugin(s)...\n")

    results = []
    for plugin_dir in plugins:
        result = validate_plugin(plugin_dir, verbose)
        results.append(result)
        if not json_output:
            result.print_results(verbose)

    # Calculate summary
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    avg_score = sum(r.score for r in results) / len(results) if results else 0

    if json_output:
        # JSON output for CI/CD
        output = {
            "summary": {
                "total_plugins": len(results),
                "total_errors": total_errors,
                "total_warnings": total_warnings,
                "average_score": round(avg_score, 1)
            },
            "plugins": [r.to_dict() for r in results]
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable summary
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}Overall Summary{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")

        print(f"Total Plugins: {len(results)}")
        print(f"{RED}Total Errors: {total_errors}{RESET}")
        print(f"{YELLOW}Total Warnings: {total_warnings}{RESET}")
        print(f"Average Score: {avg_score:.1f}/100")

        # List plugins by score
        print(f"\n{BOLD}Plugins by Score:{RESET}")
        sorted_results = sorted(results, key=lambda r: r.score, reverse=True)

        for result in sorted_results:
            score = result.score
            if score >= 90:
                color = GREEN
                icon = "🟢"
            elif score >= 70:
                color = YELLOW
                icon = "🟡"
            else:
                color = RED
                icon = "🔴"

            print(f"  {icon} {result.plugin_name:30} {color}{score:3d}/100{RESET}")

    # Exit code
    if total_errors > 0:
        sys.exit(1)
    elif total_warnings > 0:
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
