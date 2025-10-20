"""Analyzer for .claude directory structure."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def scan_claude_directory(base_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Scan the .claude directory for commands, agents, and hooks.

    Args:
        base_path: Base directory containing .claude folder

    Returns:
        Dictionary with commands, agents, and hooks lists
    """
    claude_path = os.path.join(base_path, ".claude")

    result = {
        "commands": [],
        "agents": [],
        "hooks": []
    }

    # Check if .claude directory exists
    if not os.path.exists(claude_path):
        return result

    # Analyze each component
    result["commands"] = analyze_commands(claude_path)
    result["agents"] = analyze_agents(claude_path)
    result["hooks"] = analyze_hooks(claude_path)

    return result


def analyze_commands(claude_path: str) -> List[Dict[str, Any]]:
    """
    Analyze command files in .claude/commands directory.

    Args:
        claude_path: Path to .claude directory

    Returns:
        List of command file information
    """
    commands = []
    commands_dir = os.path.join(claude_path, "commands")

    if not os.path.exists(commands_dir):
        return commands

    # Walk through commands directory
    for root, _, files in os.walk(commands_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, commands_dir)

                # Determine category from subdirectory
                path_parts = Path(relative_path).parts
                if len(path_parts) > 1:
                    category = str(Path(*path_parts[:-1]))
                else:
                    category = None

                commands.append({
                    "name": file,
                    "type": "command",
                    "path": file_path,
                    "category": category,
                    "size": os.path.getsize(file_path)
                })

    return commands


def analyze_agents(claude_path: str) -> List[Dict[str, Any]]:
    """
    Analyze agent files in .claude/agents directory.

    Args:
        claude_path: Path to .claude directory

    Returns:
        List of agent file information
    """
    agents = []
    agents_dir = os.path.join(claude_path, "agents")

    if not os.path.exists(agents_dir):
        return agents

    # Walk through agents directory
    for root, _, files in os.walk(agents_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, agents_dir)

                # Determine category from subdirectory
                path_parts = Path(relative_path).parts
                if len(path_parts) > 1:
                    category = str(Path(*path_parts[:-1]))
                else:
                    category = None

                agents.append({
                    "name": file,
                    "type": "agent",
                    "path": file_path,
                    "category": category,
                    "size": os.path.getsize(file_path)
                })

    return agents


def analyze_hooks(claude_path: str) -> List[Dict[str, Any]]:
    """
    Analyze hook files in .claude/hooks directory.

    Args:
        claude_path: Path to .claude directory

    Returns:
        List of hook file information
    """
    hooks = []
    hooks_dir = os.path.join(claude_path, "hooks")

    if not os.path.exists(hooks_dir):
        return hooks

    # Walk through hooks directory
    for root, _, files in os.walk(hooks_dir):
        for file in files:
            # Include all files in hooks directory (any extension or no extension)
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, hooks_dir)

            # Determine category from subdirectory
            path_parts = Path(relative_path).parts
            if len(path_parts) > 1:
                category = str(Path(*path_parts[:-1]))
            else:
                category = None

            hooks.append({
                "name": file,
                "type": "hook",
                "path": file_path,
                "category": category,
                "size": os.path.getsize(file_path)
            })

    return hooks


def categorize_by_subdirectory(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize items by their subdirectory.

    Args:
        items: List of items with category field

    Returns:
        Dictionary with categories as keys and lists of items as values
    """
    categorized = {}

    for item in items:
        category = item.get("category")
        if category is None:
            category = "root"

        if category not in categorized:
            categorized[category] = []

        categorized[category].append(item)

    return categorized