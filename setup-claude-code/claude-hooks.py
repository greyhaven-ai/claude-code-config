#!/usr/bin/env python3
"""
Claude Hooks CLI - Manage Claude Code hooks from the command line

This tool provides a simple interface to manage hooks without using the /hooks menu.
It directly modifies the appropriate settings files.

Usage:
    claude-hooks add <event> <command> [--matcher PATTERN] [--timeout SECONDS] [--location local|project|user]
    claude-hooks remove <event> <command> [--location local|project|user]
    claude-hooks list [--location local|project|user]
    claude-hooks install <preset> [--location local|project|user]
    
Examples:
    # Add a logging hook for bash commands
    claude-hooks add PreToolUse 'echo "$CLAUDE_PROJECT_DIR" >> log.txt' --matcher Bash
    
    # Install a preset configuration
    claude-hooks install quality
    
    # List all hooks in local settings
    claude-hooks list --location local
"""

import json
import sys
import os
from pathlib import Path
import argparse
from typing import Dict, List, Optional


class ClaudeHooksManager:
    """Manage Claude Code hooks programmatically"""
    
    # Hook presets for quick installation
    PRESETS = {
        'logging': {
            'name': 'Command Logging',
            'hooks': [
                {
                    'event': 'PreToolUse',
                    'matcher': 'Bash',
                    'command': 'jq -r "\\(.tool_input.command) - \\(.tool_input.description // \\"No description\\")" >> ~/.claude/bash-command-log.txt',
                    'timeout': None
                }
            ]
        },
        'quality': {
            'name': 'Quality Assurance',
            'hooks': [
                {
                    'event': 'PostToolUse',
                    'matcher': 'Edit|Write|MultiEdit',
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh',
                    'timeout': 30
                },
                {
                    'event': 'PostToolUse',
                    'matcher': 'Edit|Write|MultiEdit', 
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/bash/auto-formatter.sh',
                    'timeout': 20
                },
                {
                    'event': 'Stop',
                    'matcher': None,
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py',
                    'timeout': 20
                }
            ]
        },
        'context': {
            'name': 'Smart Context',
            'hooks': [
                {
                    'event': 'SessionStart',
                    'matcher': None,
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/bash/branch-context-loader.sh',
                    'timeout': 10
                },
                {
                    'event': 'UserPromptSubmit',
                    'matcher': None,
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/python/prompt-enhancer.py',
                    'timeout': 10
                }
            ]
        },
        'subagent': {
            'name': 'Subagent Support',
            'hooks': [
                {
                    'event': 'PreToolUse',
                    'matcher': 'Task',
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-context-preparer.py',
                    'timeout': 10
                },
                {
                    'event': 'SubagentStop',
                    'matcher': None,
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-work-validator.py',
                    'timeout': 15
                }
            ]
        },
        'testing': {
            'name': 'Automated Testing',
            'hooks': [
                {
                    'event': 'PostToolUse',
                    'matcher': 'Edit|Write',
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/bash/smart-test-runner.sh',
                    'timeout': 60
                },
                {
                    'event': 'PostToolUse',
                    'matcher': 'Edit|Write',
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/python/coverage-gap-finder.py',
                    'timeout': 30
                }
            ]
        },
        'minimal': {
            'name': 'Minimal Setup',
            'hooks': [
                {
                    'event': 'PostToolUse',
                    'matcher': 'Edit|Write|MultiEdit',
                    'command': '$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh',
                    'timeout': 30
                }
            ]
        }
    }
    
    def __init__(self, location='local'):
        self.location = location
        self.settings_path = self._get_settings_path(location)
    
    def _get_settings_path(self, location):
        """Get the path to the settings file based on location"""
        if location == 'user':
            return Path.home() / '.claude' / 'settings.json'
        elif location == 'project':
            return Path('.claude') / 'settings.json'
        else:  # local
            return Path('.claude') / 'settings.local.json'
    
    def load_settings(self):
        """Load current settings or create empty structure"""
        if self.settings_path.exists():
            with open(self.settings_path, 'r') as f:
                return json.load(f)
        return {'hooks': {}}
    
    def save_settings(self, settings):
        """Save settings to file"""
        # Create directory if needed
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"✓ Settings saved to {self.settings_path}")
    
    def add_hook(self, event, command, matcher=None, timeout=None):
        """Add a hook to the settings"""
        settings = self.load_settings()
        
        # Initialize hooks structure if needed
        if 'hooks' not in settings:
            settings['hooks'] = {}
        if event not in settings['hooks']:
            settings['hooks'][event] = []
        
        # Build hook configuration
        hook_config = {
            'hooks': [{
                'type': 'command',
                'command': command
            }]
        }
        
        if timeout:
            hook_config['hooks'][0]['timeout'] = timeout
        
        # Add matcher for Pre/PostToolUse events
        if matcher and event in ['PreToolUse', 'PostToolUse']:
            hook_config['matcher'] = matcher
        
        # Check for duplicates
        for existing in settings['hooks'][event]:
            existing_command = existing.get('hooks', [{}])[0].get('command')
            if existing_command == command:
                print(f"⚠ Hook already exists for {event}")
                return False
        
        # Add the hook
        settings['hooks'][event].append(hook_config)
        self.save_settings(settings)
        print(f"✓ Added hook to {event}")
        
        if matcher:
            print(f"  Matcher: {matcher}")
        print(f"  Command: {command}")
        if timeout:
            print(f"  Timeout: {timeout}s")
        
        return True
    
    def remove_hook(self, event, command):
        """Remove a hook from the settings"""
        settings = self.load_settings()
        
        if event not in settings.get('hooks', {}):
            print(f"⚠ No hooks found for {event}")
            return False
        
        original_count = len(settings['hooks'][event])
        settings['hooks'][event] = [
            hook for hook in settings['hooks'][event]
            if hook.get('hooks', [{}])[0].get('command') != command
        ]
        
        if len(settings['hooks'][event]) < original_count:
            # Remove empty event entries
            if not settings['hooks'][event]:
                del settings['hooks'][event]
            
            self.save_settings(settings)
            print(f"✓ Removed hook from {event}")
            return True
        else:
            print(f"⚠ Hook not found in {event}")
            return False
    
    def list_hooks(self):
        """List all configured hooks"""
        settings = self.load_settings()
        hooks = settings.get('hooks', {})
        
        if not hooks:
            print(f"No hooks configured in {self.location} settings")
            return
        
        print(f"\nHooks in {self.location} settings ({self.settings_path}):")
        print("=" * 60)
        
        for event, hook_list in hooks.items():
            print(f"\n{event}:")
            for hook_config in hook_list:
                matcher = hook_config.get('matcher', '')
                if matcher:
                    print(f"  Matcher: {matcher}")
                
                for hook in hook_config.get('hooks', []):
                    command = hook.get('command', '')
                    timeout = hook.get('timeout', '')
                    
                    # Truncate long commands for display
                    display_command = command
                    if len(command) > 50:
                        display_command = command[:47] + "..."
                    
                    print(f"    Command: {display_command}")
                    if timeout:
                        print(f"    Timeout: {timeout}s")
    
    def install_preset(self, preset_name):
        """Install a preset configuration"""
        if preset_name not in self.PRESETS:
            print(f"❌ Unknown preset: {preset_name}")
            print(f"Available presets: {', '.join(self.PRESETS.keys())}")
            return False
        
        preset = self.PRESETS[preset_name]
        print(f"\nInstalling {preset['name']} hooks...")
        
        for hook in preset['hooks']:
            self.add_hook(
                hook['event'],
                hook['command'],
                hook.get('matcher'),
                hook.get('timeout')
            )
        
        print(f"\n✓ {preset['name']} hooks installed successfully!")
        return True
    
    def show_presets(self):
        """Show available presets"""
        print("\nAvailable Hook Presets:")
        print("=" * 60)
        
        for key, preset in self.PRESETS.items():
            print(f"\n{key}: {preset['name']}")
            for hook in preset['hooks']:
                print(f"  - {hook['event']}", end='')
                if hook.get('matcher'):
                    print(f" ({hook['matcher']})", end='')
                print()


def main():
    parser = argparse.ArgumentParser(
        description='Manage Claude Code hooks from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a simple logging hook
  %(prog)s add PreToolUse 'echo "Command run" >> log.txt' --matcher Bash
  
  # Install quality assurance preset
  %(prog)s install quality
  
  # List all hooks in local settings
  %(prog)s list
  
  # Remove a specific hook
  %(prog)s remove PostToolUse '$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh'
  
  # Show available presets
  %(prog)s presets
        """
    )
    
    parser.add_argument('--location', choices=['local', 'project', 'user'], 
                       default='local', help='Settings file location')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new hook')
    add_parser.add_argument('event', help='Hook event (e.g., PreToolUse, PostToolUse, Stop)')
    add_parser.add_argument('command', help='Command to execute')
    add_parser.add_argument('--matcher', '-m', help='Tool matcher pattern (for Pre/PostToolUse)')
    add_parser.add_argument('--timeout', '-t', type=int, help='Command timeout in seconds')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a hook')
    remove_parser.add_argument('event', help='Hook event')
    remove_parser.add_argument('command', help='Command to remove')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all hooks')
    
    # Install preset command
    install_parser = subparsers.add_parser('install', help='Install a preset configuration')
    install_parser.add_argument('preset', help='Preset name (e.g., quality, context, testing)')
    
    # Show presets command
    presets_parser = subparsers.add_parser('presets', help='Show available presets')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = ClaudeHooksManager(args.location)
    
    if args.command == 'add':
        manager.add_hook(args.event, args.command, args.matcher, args.timeout)
    elif args.command == 'remove':
        manager.remove_hook(args.event, args.command)
    elif args.command == 'list':
        manager.list_hooks()
    elif args.command == 'install':
        manager.install_preset(args.preset)
    elif args.command == 'presets':
        manager.show_presets()


if __name__ == '__main__':
    main()