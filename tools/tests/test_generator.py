"""Tests for plugin structure generator."""

import json
import os
import tempfile
import shutil
from pathlib import Path

import pytest
from plugin_generator.generator import (
    create_marketplace_structure,
    generate_marketplace_manifest,
    generate_plugin_manifest,
    create_plugin_directory
)


class TestDirectoryGenerator:
    """Test cases for directory structure generation."""

    def setup_method(self):
        """Create a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_marketplace_structure(self):
        """Test creation of marketplace directory structure."""
        marketplace_path = os.path.join(self.test_dir, "my-marketplace")

        create_marketplace_structure(marketplace_path)

        # Check main directory exists
        assert os.path.exists(marketplace_path)
        assert os.path.isdir(marketplace_path)

        # Check .claude-plugin subdirectory exists
        plugin_dir = os.path.join(marketplace_path, ".claude-plugin")
        assert os.path.exists(plugin_dir)
        assert os.path.isdir(plugin_dir)

    def test_create_marketplace_structure_existing_directory(self):
        """Test that creating structure in existing directory works."""
        marketplace_path = os.path.join(self.test_dir, "existing-marketplace")
        os.makedirs(marketplace_path)

        # Should not raise an error
        create_marketplace_structure(marketplace_path)

        plugin_dir = os.path.join(marketplace_path, ".claude-plugin")
        assert os.path.exists(plugin_dir)

    def test_generate_marketplace_manifest(self):
        """Test generation of marketplace.json file."""
        marketplace_path = os.path.join(self.test_dir, "test-marketplace")
        create_marketplace_structure(marketplace_path)

        manifest_data = {
            "name": "Test Marketplace",
            "owner": {
                "name": "Test Owner"
            },
            "plugins": [
                {
                    "name": "test-plugin",
                    "source": "./plugins/test",
                    "description": "A test plugin"
                }
            ]
        }

        generate_marketplace_manifest(marketplace_path, manifest_data)

        # Check file exists
        manifest_path = os.path.join(marketplace_path, ".claude-plugin", "marketplace.json")
        assert os.path.exists(manifest_path)

        # Check content is correct
        with open(manifest_path, "r") as f:
            loaded_data = json.load(f)
        assert loaded_data == manifest_data

    def test_generate_plugin_manifest(self):
        """Test generation of plugin.json file."""
        plugin_path = os.path.join(self.test_dir, "test-plugin")
        os.makedirs(plugin_path)

        manifest_data = {
            "name": "test-plugin",
            "description": "A test plugin",
            "version": "1.0.0",
            "author": {
                "name": "Test Author"
            }
        }

        generate_plugin_manifest(plugin_path, manifest_data)

        # Check file exists
        manifest_path = os.path.join(plugin_path, "plugin.json")
        assert os.path.exists(manifest_path)

        # Check content is correct
        with open(manifest_path, "r") as f:
            loaded_data = json.load(f)
        assert loaded_data == manifest_data

    def test_create_plugin_directory(self):
        """Test creation of individual plugin directory with manifest."""
        marketplace_path = os.path.join(self.test_dir, "marketplace")
        create_marketplace_structure(marketplace_path)

        plugin_data = {
            "name": "sample-plugin",
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {
                "name": "Plugin Author"
            }
        }

        plugin_path = create_plugin_directory(marketplace_path, "sample-plugin", plugin_data)

        # Check plugin directory exists
        expected_path = os.path.join(marketplace_path, "plugins", "sample-plugin")
        assert plugin_path == expected_path
        assert os.path.exists(plugin_path)
        assert os.path.isdir(plugin_path)

        # Check plugin.json exists
        manifest_path = os.path.join(plugin_path, "plugin.json")
        assert os.path.exists(manifest_path)

        # Check content is correct
        with open(manifest_path, "r") as f:
            loaded_data = json.load(f)
        assert loaded_data == plugin_data

    def test_create_multiple_plugins(self):
        """Test creation of multiple plugin directories."""
        marketplace_path = os.path.join(self.test_dir, "marketplace")
        create_marketplace_structure(marketplace_path)

        plugins = [
            {
                "name": "plugin-1",
                "description": "First plugin",
                "version": "1.0.0",
                "author": {"name": "Author 1"}
            },
            {
                "name": "plugin-2",
                "description": "Second plugin",
                "version": "2.0.0",
                "author": {"name": "Author 2"}
            }
        ]

        for plugin_data in plugins:
            plugin_path = create_plugin_directory(
                marketplace_path,
                plugin_data["name"],
                plugin_data
            )

            # Check each plugin directory and manifest
            assert os.path.exists(plugin_path)
            manifest_path = os.path.join(plugin_path, "plugin.json")
            assert os.path.exists(manifest_path)

            with open(manifest_path, "r") as f:
                loaded_data = json.load(f)
            assert loaded_data == plugin_data

    def test_marketplace_manifest_formatting(self):
        """Test that marketplace.json is formatted with proper indentation."""
        marketplace_path = os.path.join(self.test_dir, "formatted-marketplace")
        create_marketplace_structure(marketplace_path)

        manifest_data = {
            "name": "Formatted Marketplace",
            "owner": {
                "name": "Test Owner"
            },
            "plugins": []
        }

        generate_marketplace_manifest(marketplace_path, manifest_data)

        manifest_path = os.path.join(marketplace_path, ".claude-plugin", "marketplace.json")
        with open(manifest_path, "r") as f:
            content = f.read()

        # Check for proper formatting (indented JSON)
        assert "    " in content  # Should have indentation
        assert content.startswith("{\n")  # Should start with opening brace and newline