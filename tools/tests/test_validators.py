"""Tests for manifest validators."""

import pytest
from plugin_generator.validators import (
    validate_marketplace_manifest,
    validate_plugin_manifest
)


class TestMarketplaceValidator:
    """Test cases for marketplace.json validation."""

    def test_valid_marketplace_manifest(self):
        """Test that a valid marketplace manifest passes validation."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {
                "name": "John Doe"
            },
            "plugins": [
                {
                    "name": "example-plugin",
                    "source": "./plugins/example",
                    "description": "An example plugin"
                }
            ]
        }

        result = validate_marketplace_manifest(manifest)
        assert result is True

    def test_marketplace_missing_name(self):
        """Test that marketplace manifest without name fails validation."""
        manifest = {
            "owner": {
                "name": "John Doe"
            },
            "plugins": []
        }

        with pytest.raises(ValueError, match="Missing required field: name"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_missing_owner(self):
        """Test that marketplace manifest without owner fails validation."""
        manifest = {
            "name": "My Plugin Collection",
            "plugins": []
        }

        with pytest.raises(ValueError, match="Missing required field: owner"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_owner_missing_name(self):
        """Test that owner without name field fails validation."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {},
            "plugins": []
        }

        with pytest.raises(ValueError, match="Owner must have a 'name' field"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_missing_plugins(self):
        """Test that marketplace manifest without plugins fails validation."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {
                "name": "John Doe"
            }
        }

        with pytest.raises(ValueError, match="Missing required field: plugins"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_plugins_not_array(self):
        """Test that plugins field must be an array."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {
                "name": "John Doe"
            },
            "plugins": "not-an-array"
        }

        with pytest.raises(TypeError, match="Plugins must be an array"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_plugin_missing_name(self):
        """Test that plugin without name fails validation."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {
                "name": "John Doe"
            },
            "plugins": [
                {
                    "source": "./plugins/example",
                    "description": "An example plugin"
                }
            ]
        }

        with pytest.raises(ValueError, match="Plugin missing required field: name"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_plugin_missing_source(self):
        """Test that plugin without source fails validation."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {
                "name": "John Doe"
            },
            "plugins": [
                {
                    "name": "example-plugin",
                    "description": "An example plugin"
                }
            ]
        }

        with pytest.raises(ValueError, match="Plugin missing required field: source"):
            validate_marketplace_manifest(manifest)

    def test_marketplace_plugin_missing_description(self):
        """Test that plugin without description fails validation."""
        manifest = {
            "name": "My Plugin Collection",
            "owner": {
                "name": "John Doe"
            },
            "plugins": [
                {
                    "name": "example-plugin",
                    "source": "./plugins/example"
                }
            ]
        }

        with pytest.raises(ValueError, match="Plugin missing required field: description"):
            validate_marketplace_manifest(manifest)


class TestPluginValidator:
    """Test cases for plugin.json validation."""

    def test_valid_plugin_manifest(self):
        """Test that a valid plugin manifest passes validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {
                "name": "John Doe"
            }
        }

        result = validate_plugin_manifest(manifest)
        assert result is True

    def test_plugin_with_optional_fields(self):
        """Test that plugin manifest with optional fields passes validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {
                "name": "John Doe"
            },
            "keywords": ["test", "example"],
            "license": "MIT"
        }

        result = validate_plugin_manifest(manifest)
        assert result is True

    def test_plugin_missing_name(self):
        """Test that plugin manifest without name fails validation."""
        manifest = {
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {
                "name": "John Doe"
            }
        }

        with pytest.raises(ValueError, match="Missing required field: name"):
            validate_plugin_manifest(manifest)

    def test_plugin_missing_description(self):
        """Test that plugin manifest without description fails validation."""
        manifest = {
            "name": "my-plugin",
            "version": "1.0.0",
            "author": {
                "name": "John Doe"
            }
        }

        with pytest.raises(ValueError, match="Missing required field: description"):
            validate_plugin_manifest(manifest)

    def test_plugin_missing_version(self):
        """Test that plugin manifest without version fails validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "author": {
                "name": "John Doe"
            }
        }

        with pytest.raises(ValueError, match="Missing required field: version"):
            validate_plugin_manifest(manifest)

    def test_plugin_missing_author(self):
        """Test that plugin manifest without author fails validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0.0"
        }

        with pytest.raises(ValueError, match="Missing required field: author"):
            validate_plugin_manifest(manifest)

    def test_plugin_author_missing_name(self):
        """Test that author without name field fails validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {}
        }

        with pytest.raises(ValueError, match="Author must have a 'name' field"):
            validate_plugin_manifest(manifest)

    def test_plugin_invalid_semantic_version(self):
        """Test that invalid semantic version fails validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0",  # Missing patch version
            "author": {
                "name": "John Doe"
            }
        }

        with pytest.raises(ValueError, match="Version must follow semantic versioning"):
            validate_plugin_manifest(manifest)

    def test_plugin_version_with_prefix(self):
        """Test that version with 'v' prefix fails validation."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "v1.0.0",  # Has 'v' prefix
            "author": {
                "name": "John Doe"
            }
        }

        with pytest.raises(ValueError, match="Version must follow semantic versioning"):
            validate_plugin_manifest(manifest)

    def test_plugin_keywords_not_array(self):
        """Test that keywords field must be an array."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {
                "name": "John Doe"
            },
            "keywords": "not-an-array"
        }

        with pytest.raises(TypeError, match="Keywords must be an array"):
            validate_plugin_manifest(manifest)

    def test_plugin_license_not_string(self):
        """Test that license field must be a string."""
        manifest = {
            "name": "my-plugin",
            "description": "A sample plugin",
            "version": "1.0.0",
            "author": {
                "name": "John Doe"
            },
            "license": ["MIT"]  # Should be a string
        }

        with pytest.raises(TypeError, match="License must be a string"):
            validate_plugin_manifest(manifest)