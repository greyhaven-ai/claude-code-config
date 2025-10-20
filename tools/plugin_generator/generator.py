"""Generator for plugin directory structures."""

import json
import os
from pathlib import Path
from typing import Any, Dict


def create_marketplace_structure(marketplace_path: str) -> None:
    """
    Create the marketplace directory structure.

    Args:
        marketplace_path: Path where marketplace should be created
    """
    # Create main marketplace directory
    os.makedirs(marketplace_path, exist_ok=True)

    # Create .claude-plugin subdirectory
    plugin_dir = os.path.join(marketplace_path, ".claude-plugin")
    os.makedirs(plugin_dir, exist_ok=True)


def generate_marketplace_manifest(marketplace_path: str, manifest_data: Dict[str, Any]) -> None:
    """
    Generate marketplace.json file.

    Args:
        marketplace_path: Path to the marketplace directory
        manifest_data: Dictionary containing marketplace manifest data
    """
    manifest_path = os.path.join(marketplace_path, ".claude-plugin", "marketplace.json")

    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=4)


def generate_plugin_manifest(plugin_path: str, manifest_data: Dict[str, Any]) -> None:
    """
    Generate plugin.json file.

    Args:
        plugin_path: Path to the plugin directory
        manifest_data: Dictionary containing plugin manifest data
    """
    manifest_path = os.path.join(plugin_path, "plugin.json")

    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=4)


def create_plugin_directory(marketplace_path: str, plugin_name: str, plugin_data: Dict[str, Any]) -> str:
    """
    Create an individual plugin directory with its manifest.

    Args:
        marketplace_path: Path to the marketplace directory
        plugin_name: Name of the plugin
        plugin_data: Dictionary containing plugin manifest data

    Returns:
        Path to the created plugin directory
    """
    # Create plugins directory if it doesn't exist
    plugins_dir = os.path.join(marketplace_path, "plugins")
    os.makedirs(plugins_dir, exist_ok=True)

    # Create specific plugin directory
    plugin_path = os.path.join(plugins_dir, plugin_name)
    os.makedirs(plugin_path, exist_ok=True)

    # Generate plugin.json
    generate_plugin_manifest(plugin_path, plugin_data)

    return plugin_path