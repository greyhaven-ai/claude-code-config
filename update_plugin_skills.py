#!/usr/bin/env python3
import json
from pathlib import Path

# Define skills for each plugin
plugin_skills = {
    "grey-haven-core": [
        "./skills/code-style",
        "./skills/commit-format",
        "./skills/pr-template",
        "./skills/testing-strategy"
    ],
    "grey-haven-developer-experience": [
        "./skills/code-style",
        "./skills/pr-template",
        "./skills/project-structure",
        "./skills/api-design-standards",
        "./skills/ontological-documentation"
    ],
    "grey-haven-testing": [
        "./skills/testing-strategy"
    ],
    "grey-haven-security": [
        "./skills/security-practices",
        "./skills/authentication-patterns"
    ],
    "grey-haven-observability": [
        "./skills/observability-monitoring",
        "./skills/performance-optimization"
    ],
    "grey-haven-deployment": [
        "./skills/deployment-cloudflare"
    ],
    "grey-haven-data-quality": [
        "./skills/database-conventions",
        "./skills/data-modeling"
    ],
    "grey-haven-linear": [
        "./skills/linear-workflow",
        "./skills/commit-format"
    ],
    "grey-haven-research": [
        "./skills/tanstack-patterns"
    ]
}

def update_plugin_json(plugin_name, skills):
    """Update plugin.json with skills array"""
    plugin_json_path = Path(f"grey-haven-plugins/{plugin_name}/.claude-plugin/plugin.json")

    with open(plugin_json_path, 'r') as f:
        data = json.load(f)

    # Add skills array
    data['skills'] = skills

    with open(plugin_json_path, 'w') as f:
        json.dump(data, f, indent=4)
        f.write('\n')

    print(f"✓ Updated {plugin_name} with {len(skills)} skills")

def main():
    for plugin_name, skills in plugin_skills.items():
        update_plugin_json(plugin_name, skills)

    print(f"\n✅ Updated {len(plugin_skills)} plugins with skills arrays")

if __name__ == "__main__":
    main()
