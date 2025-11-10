#!/usr/bin/env python3
"""
Find agents without model specifications and suggest appropriate models.
"""

import re
from pathlib import Path

def has_model_field(file_path):
    """Check if agent has model field in frontmatter."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Check for frontmatter
    if not content.startswith('---'):
        return False, False

    # Extract frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, False

    frontmatter = parts[1]
    has_model = bool(re.search(r'^model:', frontmatter, re.MULTILINE))

    return True, has_model

def suggest_model(file_path):
    """Suggest appropriate model based on agent name and description."""
    name = file_path.stem.lower()

    # Complex agents should use opus or sonnet
    complex_patterns = [
        'orchestrat', 'architect', 'analyzer', 'implementer',
        'optimizer', 'coordinator', 'engineer', 'troubleshooter'
    ]

    # Simple agents can use haiku
    simple_patterns = [
        'creator', 'maintainer', 'generator'
    ]

    if any(pattern in name for pattern in complex_patterns):
        return 'sonnet'
    elif any(pattern in name for pattern in simple_patterns):
        return 'haiku'
    else:
        return 'sonnet'  # Default to sonnet for uncertain cases

# Find all agents
base_dir = Path(__file__).parent.parent / 'grey-haven-plugins'
agents = []

for plugin_dir in base_dir.iterdir():
    if not plugin_dir.is_dir():
        continue

    agents_dir = plugin_dir / 'agents'
    if not agents_dir.exists():
        continue

    for agent_file in agents_dir.glob('*.md'):
        if '-old' in agent_file.stem:
            continue

        has_frontmatter, has_model = has_model_field(agent_file)

        if has_frontmatter and not has_model:
            suggested_model = suggest_model(agent_file)
            plugin_name = plugin_dir.name
            agents.append({
                'path': agent_file,
                'plugin': plugin_name,
                'name': agent_file.stem,
                'suggested_model': suggested_model
            })

print(f"Found {len(agents)} agents without model specifications:\n")

# Group by suggested model
by_model = {'opus': [], 'sonnet': [], 'haiku': []}
for agent in agents:
    by_model[agent['suggested_model']].append(agent)

for model in ['opus', 'sonnet', 'haiku']:
    if by_model[model]:
        print(f"\n{model.upper()} ({len(by_model[model])} agents):")
        for agent in by_model[model]:
            print(f"  {agent['plugin']:30} {agent['name']}")

print(f"\n\nTotal: {len(agents)} agents need model specifications")
