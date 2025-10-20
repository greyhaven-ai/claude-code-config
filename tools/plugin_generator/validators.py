"""Validators for plugin manifests."""

import re
from typing import Any, Dict


def validate_marketplace_manifest(manifest: Dict[str, Any]) -> bool:
    """
    Validate a marketplace.json manifest.

    Args:
        manifest: Dictionary containing the marketplace manifest data

    Returns:
        True if valid

    Raises:
        ValueError: If required fields are missing or invalid
        TypeError: If field types are incorrect
    """
    # Check required top-level fields
    if "name" not in manifest:
        raise ValueError("Missing required field: name")

    if "owner" not in manifest:
        raise ValueError("Missing required field: owner")

    if "plugins" not in manifest:
        raise ValueError("Missing required field: plugins")

    # Validate owner structure
    if "name" not in manifest["owner"]:
        raise ValueError("Owner must have a 'name' field")

    # Validate plugins is an array
    if not isinstance(manifest["plugins"], list):
        raise TypeError("Plugins must be an array")

    # Validate each plugin
    for plugin in manifest["plugins"]:
        if "name" not in plugin:
            raise ValueError("Plugin missing required field: name")

        if "source" not in plugin:
            raise ValueError("Plugin missing required field: source")

        if "description" not in plugin:
            raise ValueError("Plugin missing required field: description")

    return True


def validate_plugin_manifest(manifest: Dict[str, Any]) -> bool:
    """
    Validate a plugin.json manifest.

    Args:
        manifest: Dictionary containing the plugin manifest data

    Returns:
        True if valid

    Raises:
        ValueError: If required fields are missing or invalid
        TypeError: If field types are incorrect
    """
    # Check required fields
    if "name" not in manifest:
        raise ValueError("Missing required field: name")

    if "description" not in manifest:
        raise ValueError("Missing required field: description")

    if "version" not in manifest:
        raise ValueError("Missing required field: version")

    if "author" not in manifest:
        raise ValueError("Missing required field: author")

    # Validate author structure
    if "name" not in manifest["author"]:
        raise ValueError("Author must have a 'name' field")

    # Validate semantic version (matches x.y.z pattern)
    version_pattern = r"^\d+\.\d+\.\d+$"
    if not re.match(version_pattern, manifest["version"]):
        raise ValueError("Version must follow semantic versioning (e.g., '1.0.0')")

    # Validate optional fields if present
    if "keywords" in manifest:
        if not isinstance(manifest["keywords"], list):
            raise TypeError("Keywords must be an array")

    if "license" in manifest:
        if not isinstance(manifest["license"], str):
            raise TypeError("License must be a string")

    return True