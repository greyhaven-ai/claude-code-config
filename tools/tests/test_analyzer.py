"""Tests for .claude directory analyzer."""

import os
import tempfile
import shutil
from pathlib import Path

import pytest
from plugin_generator.analyzer import (
    scan_claude_directory,
    categorize_by_subdirectory,
    analyze_commands,
    analyze_agents,
    analyze_hooks
)


class TestClaudeAnalyzer:
    """Test cases for .claude directory analysis."""

    def setup_method(self):
        """Create a temporary directory with sample .claude structure."""
        self.test_dir = tempfile.mkdtemp()
        self.claude_dir = os.path.join(self.test_dir, ".claude")
        os.makedirs(self.claude_dir)

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scan_empty_claude_directory(self):
        """Test scanning an empty .claude directory."""
        result = scan_claude_directory(self.test_dir)

        assert result is not None
        assert "commands" in result
        assert "agents" in result
        assert "hooks" in result
        assert len(result["commands"]) == 0
        assert len(result["agents"]) == 0
        assert len(result["hooks"]) == 0

    def test_analyze_commands(self):
        """Test analyzing command files."""
        # Create commands directory
        commands_dir = os.path.join(self.claude_dir, "commands")
        os.makedirs(commands_dir)

        # Create sample command files
        with open(os.path.join(commands_dir, "test-command.md"), "w") as f:
            f.write("# Test Command\nThis is a test command.")

        with open(os.path.join(commands_dir, "another-command.md"), "w") as f:
            f.write("# Another Command\nAnother test command.")

        # Create non-markdown file (should be ignored)
        with open(os.path.join(commands_dir, "config.json"), "w") as f:
            f.write("{}")

        commands = analyze_commands(self.claude_dir)

        assert len(commands) == 2
        assert any(cmd["name"] == "test-command.md" for cmd in commands)
        assert any(cmd["name"] == "another-command.md" for cmd in commands)
        assert all(cmd["type"] == "command" for cmd in commands)
        assert all("path" in cmd for cmd in commands)

    def test_analyze_agents(self):
        """Test analyzing agent files."""
        # Create agents directory
        agents_dir = os.path.join(self.claude_dir, "agents")
        os.makedirs(agents_dir)

        # Create sample agent files
        with open(os.path.join(agents_dir, "test-agent.md"), "w") as f:
            f.write("# Test Agent\nThis is a test agent.")

        with open(os.path.join(agents_dir, "helper-agent.md"), "w") as f:
            f.write("# Helper Agent\nA helper agent.")

        agents = analyze_agents(self.claude_dir)

        assert len(agents) == 2
        assert any(agent["name"] == "test-agent.md" for agent in agents)
        assert any(agent["name"] == "helper-agent.md" for agent in agents)
        assert all(agent["type"] == "agent" for agent in agents)
        assert all("path" in agent for agent in agents)

    def test_analyze_hooks(self):
        """Test analyzing hook files."""
        # Create hooks directory
        hooks_dir = os.path.join(self.claude_dir, "hooks")
        os.makedirs(hooks_dir)

        # Create sample hook files (various extensions)
        with open(os.path.join(hooks_dir, "pre-commit.py"), "w") as f:
            f.write("# Python hook")

        with open(os.path.join(hooks_dir, "post-edit.js"), "w") as f:
            f.write("// JavaScript hook")

        with open(os.path.join(hooks_dir, "validate.sh"), "w") as f:
            f.write("#!/bin/bash\n# Shell hook")

        hooks = analyze_hooks(self.claude_dir)

        assert len(hooks) == 3
        assert any(hook["name"] == "pre-commit.py" for hook in hooks)
        assert any(hook["name"] == "post-edit.js" for hook in hooks)
        assert any(hook["name"] == "validate.sh" for hook in hooks)
        assert all(hook["type"] == "hook" for hook in hooks)
        assert all("path" in hook for hook in hooks)

    def test_categorize_by_subdirectory(self):
        """Test categorization by subdirectory."""
        # Create subdirectories with commands
        linear_dir = os.path.join(self.claude_dir, "commands", "linear")
        security_dir = os.path.join(self.claude_dir, "commands", "security")
        os.makedirs(linear_dir)
        os.makedirs(security_dir)

        # Create commands in subdirectories
        with open(os.path.join(linear_dir, "create-issue.md"), "w") as f:
            f.write("# Create Issue")

        with open(os.path.join(linear_dir, "update-issue.md"), "w") as f:
            f.write("# Update Issue")

        with open(os.path.join(security_dir, "scan.md"), "w") as f:
            f.write("# Security Scan")

        # Create command in root commands directory
        with open(os.path.join(self.claude_dir, "commands", "general.md"), "w") as f:
            f.write("# General Command")

        result = scan_claude_directory(self.test_dir)
        categorized = categorize_by_subdirectory(result["commands"])

        assert "linear" in categorized
        assert "security" in categorized
        assert "root" in categorized  # For files in root commands directory

        assert len(categorized["linear"]) == 2
        assert len(categorized["security"]) == 1
        assert len(categorized["root"]) == 1

        # Check specific commands are in correct categories
        linear_names = [cmd["name"] for cmd in categorized["linear"]]
        assert "create-issue.md" in linear_names
        assert "update-issue.md" in linear_names

        security_names = [cmd["name"] for cmd in categorized["security"]]
        assert "scan.md" in security_names

        root_names = [cmd["name"] for cmd in categorized["root"]]
        assert "general.md" in root_names

    def test_scan_complete_structure(self):
        """Test scanning a complete .claude directory structure."""
        # Create commands
        commands_dir = os.path.join(self.claude_dir, "commands")
        os.makedirs(commands_dir)
        with open(os.path.join(commands_dir, "cmd1.md"), "w") as f:
            f.write("Command 1")

        # Create agents
        agents_dir = os.path.join(self.claude_dir, "agents")
        os.makedirs(agents_dir)
        with open(os.path.join(agents_dir, "agent1.md"), "w") as f:
            f.write("Agent 1")

        # Create hooks
        hooks_dir = os.path.join(self.claude_dir, "hooks")
        os.makedirs(hooks_dir)
        with open(os.path.join(hooks_dir, "hook1.py"), "w") as f:
            f.write("# Hook 1")

        result = scan_claude_directory(self.test_dir)

        assert len(result["commands"]) == 1
        assert len(result["agents"]) == 1
        assert len(result["hooks"]) == 1

        assert result["commands"][0]["name"] == "cmd1.md"
        assert result["agents"][0]["name"] == "agent1.md"
        assert result["hooks"][0]["name"] == "hook1.py"

    def test_scan_nonexistent_claude_directory(self):
        """Test scanning when .claude directory doesn't exist."""
        # Remove the .claude directory
        shutil.rmtree(self.claude_dir)

        result = scan_claude_directory(self.test_dir)

        assert result is not None
        assert len(result["commands"]) == 0
        assert len(result["agents"]) == 0
        assert len(result["hooks"]) == 0

    def test_analyze_nested_subdirectories(self):
        """Test analyzing deeply nested subdirectories."""
        # Create nested structure
        deep_dir = os.path.join(self.claude_dir, "commands", "tools", "testing", "unit")
        os.makedirs(deep_dir)

        with open(os.path.join(deep_dir, "test-runner.md"), "w") as f:
            f.write("# Test Runner")

        result = scan_claude_directory(self.test_dir)
        categorized = categorize_by_subdirectory(result["commands"])

        assert "tools/testing/unit" in categorized
        assert len(categorized["tools/testing/unit"]) == 1
        assert categorized["tools/testing/unit"][0]["name"] == "test-runner.md"

    def test_file_metadata(self):
        """Test that file metadata is included in analysis."""
        commands_dir = os.path.join(self.claude_dir, "commands")
        os.makedirs(commands_dir)

        test_file = os.path.join(commands_dir, "test.md")
        with open(test_file, "w") as f:
            f.write("# Test Command\nThis is a longer description.")

        commands = analyze_commands(self.claude_dir)

        assert len(commands) == 1
        cmd = commands[0]

        # Check metadata fields
        assert "size" in cmd
        assert cmd["size"] > 0
        assert "category" in cmd
        assert cmd["category"] is None or isinstance(cmd["category"], str)

    def test_mixed_file_types_in_hooks(self):
        """Test that various hook file extensions are recognized."""
        hooks_dir = os.path.join(self.claude_dir, "hooks")
        os.makedirs(hooks_dir)

        # Create various hook files
        extensions = [".py", ".js", ".ts", ".sh", ".rb", ".go"]
        for i, ext in enumerate(extensions):
            with open(os.path.join(hooks_dir, f"hook{i}{ext}"), "w") as f:
                f.write(f"Hook {i}")

        # Create a file without extension (should still be included)
        with open(os.path.join(hooks_dir, "executable_hook"), "w") as f:
            f.write("Executable hook")

        hooks = analyze_hooks(self.claude_dir)

        # Should find all hook files
        assert len(hooks) >= len(extensions) + 1  # Plus the no-extension file

        # Check that various extensions are included
        hook_names = [h["name"] for h in hooks]
        for i, ext in enumerate(extensions):
            assert f"hook{i}{ext}" in hook_names
        assert "executable_hook" in hook_names