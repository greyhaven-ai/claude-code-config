#!/usr/bin/env python3
"""
Main script for the plugin migration tool.

Usage:
    python main.py analyze [path]  - Analyze .claude/ directory
    python main.py validate-marketplace <file>  - Validate marketplace.json
    python main.py validate-plugin <file>  - Validate plugin.json
    python main.py generate <path> <name>  - Generate plugin structure
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from plugin_generator import analyzer, generator, validators


def analyze_claude_structure(path: str) -> None:
    """Analyze and display .claude directory structure."""
    print(f"Analyzing .claude directory in: {path}")
    print("-" * 50)

    result = analyzer.scan_claude_directory(path)

    # Display commands
    print(f"\nCommands found: {len(result['commands'])}")
    if result['commands']:
        categorized = analyzer.categorize_by_subdirectory(result['commands'])
        for category, items in categorized.items():
            print(f"  [{category}]")
            for item in items:
                print(f"    - {item['name']} ({item['size']} bytes)")

    # Display agents
    print(f"\nAgents found: {len(result['agents'])}")
    for agent in result['agents']:
        print(f"  - {agent['name']} ({agent['size']} bytes)")

    # Display hooks
    print(f"\nHooks found: {len(result['hooks'])}")
    for hook in result['hooks']:
        print(f"  - {hook['name']} ({hook['size']} bytes)")


def validate_marketplace(file_path: str) -> None:
    """Validate a marketplace.json file."""
    print(f"Validating marketplace manifest: {file_path}")

    try:
        with open(file_path, 'r') as f:
            manifest = json.load(f)

        validators.validate_marketplace_manifest(manifest)
        print("✓ Marketplace manifest is valid!")

    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"✗ Validation failed: {e}")
        sys.exit(1)


def validate_plugin(file_path: str) -> None:
    """Validate a plugin.json file."""
    print(f"Validating plugin manifest: {file_path}")

    try:
        with open(file_path, 'r') as f:
            manifest = json.load(f)

        validators.validate_plugin_manifest(manifest)
        print("✓ Plugin manifest is valid!")

    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"✗ Validation failed: {e}")
        sys.exit(1)


def generate_structure(path: str, name: str) -> None:
    """Generate a plugin marketplace structure."""
    print(f"Generating marketplace structure at: {path}")
    print(f"Marketplace name: {name}")

    # Create marketplace structure
    generator.create_marketplace_structure(path)

    # Generate marketplace manifest
    marketplace_data = {
        "name": name,
        "owner": {
            "name": "Plugin Owner"
        },
        "plugins": []
    }
    generator.generate_marketplace_manifest(path, marketplace_data)

    # Create a sample plugin
    sample_plugin_data = {
        "name": "sample-plugin",
        "description": "A sample plugin to demonstrate structure",
        "version": "1.0.0",
        "author": {
            "name": "Plugin Author"
        }
    }
    plugin_path = generator.create_plugin_directory(path, "sample-plugin", sample_plugin_data)

    print(f"\n✓ Marketplace structure created successfully!")
    print(f"  - Marketplace: {path}")
    print(f"  - Plugin config: {path}/.claude-plugin/marketplace.json")
    print(f"  - Sample plugin: {plugin_path}")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Plugin Migration Tool for Claude Code")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze .claude directory structure')
    analyze_parser.add_argument('path', nargs='?', default='.', help='Path to analyze (default: current directory)')

    # Validate marketplace command
    validate_mp_parser = subparsers.add_parser('validate-marketplace', help='Validate marketplace.json file')
    validate_mp_parser.add_argument('file', help='Path to marketplace.json file')

    # Validate plugin command
    validate_plugin_parser = subparsers.add_parser('validate-plugin', help='Validate plugin.json file')
    validate_plugin_parser.add_argument('file', help='Path to plugin.json file')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate plugin marketplace structure')
    generate_parser.add_argument('path', help='Path where to create marketplace')
    generate_parser.add_argument('name', help='Name of the marketplace')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'analyze':
        analyze_claude_structure(args.path)
    elif args.command == 'validate-marketplace':
        validate_marketplace(args.file)
    elif args.command == 'validate-plugin':
        validate_plugin(args.file)
    elif args.command == 'generate':
        generate_structure(args.path, args.name)


if __name__ == '__main__':
    main()