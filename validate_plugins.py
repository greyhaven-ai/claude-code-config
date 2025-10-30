#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def validate_plugins():
    plugins_dir = Path("grey-haven-plugins")
    issues = []

    for plugin_dir in sorted(plugins_dir.glob("grey-haven-*")):
        plugin_name = plugin_dir.name
        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"

        if not plugin_json.exists():
            issues.append(f"❌ {plugin_name}: Missing .claude-plugin/plugin.json")
            continue

        with open(plugin_json) as f:
            data = json.load(f)

        print(f"\n✓ {plugin_name}")

        # Check required fields
        for field in ["name", "version", "description", "license", "category"]:
            if field not in data:
                issues.append(f"  ❌ Missing '{field}' field")
                print(f"  ❌ Missing '{field}' field")
            else:
                print(f"  ✓ {field}: {data[field]}")

        # Check author format
        author = data.get("author")
        if not author:
            issues.append(f"  ❌ {plugin_name}: Missing 'author' field")
            print(f"  ❌ Missing 'author' field")
        elif isinstance(author, str):
            issues.append(f"  ❌ {plugin_name}: 'author' should be object, not string")
            print(f"  ❌ 'author' is string (should be object)")
        elif isinstance(author, dict):
            print(f"  ✓ author: {author.get('name', 'MISSING NAME')}")

        # Show resource counts
        if "commands" in data:
            print(f"  ℹ️  commands: {len(data['commands'])} entries")
        if "skills" in data:
            print(f"  ℹ️  skills: {len(data['skills'])} entries")
        if "hooks" in data:
            print(f"  ℹ️  hooks: {len(data['hooks'])} entries")

    if issues:
        print("\n\n=== ISSUES FOUND ===")
        for issue in issues:
            print(issue)
        return 1
    else:
        print("\n\n✅ All plugins validated successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(validate_plugins())
