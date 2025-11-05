#!/usr/bin/env python3
import json
from pathlib import Path

def update_plugin_json_names():
    """Update plugin.json name fields to remove grey-haven- prefix"""
    plugins_dir = Path("grey-haven-plugins")
    updated = []

    for plugin_dir in plugins_dir.glob("*/"):
        if plugin_dir.name == "plugins":  # Skip sample plugins directory
            continue

        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            continue

        with open(plugin_json, 'r') as f:
            data = json.load(f)

        old_name = data.get('name', '')
        if old_name.startswith('grey-haven-'):
            new_name = old_name.replace('grey-haven-', '')
            data['name'] = new_name

            with open(plugin_json, 'w') as f:
                json.dump(data, f, indent=4)
                f.write('\n')

            updated.append(f"{old_name} → {new_name}")
            print(f"✓ {plugin_dir.name}: {old_name} → {new_name}")

    return updated

def update_marketplace_json():
    """Update marketplace.json to remove grey-haven- prefix from names and update paths"""
    marketplace_json = Path(".claude-plugin/marketplace.json")

    with open(marketplace_json, 'r') as f:
        data = json.load(f)

    for plugin in data['plugins']:
        # Update name
        old_name = plugin['name']
        if old_name.startswith('grey-haven-'):
            plugin['name'] = old_name.replace('grey-haven-', '')
            print(f"✓ Marketplace: {old_name} → {plugin['name']}")

        # Update source path
        old_source = plugin['source']
        if '/grey-haven-' in old_source:
            plugin['source'] = old_source.replace('/grey-haven-', '/')
            print(f"  Updated path: {old_source} → {plugin['source']}")

    with open(marketplace_json, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')

    print(f"\n✅ Updated marketplace.json with {len(data['plugins'])} plugins")

if __name__ == "__main__":
    print("=== Updating plugin.json files ===")
    updated = update_plugin_json_names()
    print(f"\n✅ Updated {len(updated)} plugin.json files\n")

    print("=== Updating marketplace.json ===")
    update_marketplace_json()
