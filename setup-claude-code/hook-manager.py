#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["typer", "rich", "jsonschema"]
# ///
"""
Claude Code Hook Manager
========================
Advanced hook management CLI for Claude Code settings.

This tool provides programmatic access to hook configuration,
allowing you to add, remove, and manage hooks without manual editing.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

import typer
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

app = typer.Typer(help="Claude Code Hook Manager - Manage hooks programmatically")
console = Console()


class HookEvent(str, Enum):
    """Valid hook event types"""
    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    NOTIFICATION = "Notification"
    STOP = "Stop"
    SUBAGENT_STOP = "SubagentStop"
    SESSION_START = "SessionStart"
    SESSION_END = "SessionEnd"
    PRE_COMPACT = "PreCompact"


class SettingsLocation(str, Enum):
    """Settings file locations"""
    USER = "user"
    PROJECT = "project"
    LOCAL = "local"


class HookManager:
    """Manages Claude Code hook configurations"""
    
    def __init__(self):
        self.user_settings = Path.home() / ".claude" / "settings.json"
        self.project_settings = Path(".claude") / "settings.json"
        self.local_settings = Path(".claude") / "settings.local.json"
        
    def get_settings_path(self, location: SettingsLocation) -> Path:
        """Get the path for a settings location"""
        paths = {
            SettingsLocation.USER: self.user_settings,
            SettingsLocation.PROJECT: self.project_settings,
            SettingsLocation.LOCAL: self.local_settings,
        }
        return paths[location]
    
    def load_settings(self, location: SettingsLocation) -> Dict:
        """Load settings from a file"""
        path = self.get_settings_path(location)
        
        if not path.exists():
            return {"hooks": {}}
        
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            console.print(f"[red]Error: Invalid JSON in {path}[/red]")
            return {"hooks": {}}
    
    def save_settings(self, location: SettingsLocation, settings: Dict) -> bool:
        """Save settings to a file"""
        path = self.get_settings_path(location)
        
        # Create parent directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            console.print(f"[red]Error saving settings: {e}[/red]")
            return False
    
    def add_hook(
        self,
        location: SettingsLocation,
        event: HookEvent,
        command: str,
        matcher: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> bool:
        """Add a hook to settings"""
        settings = self.load_settings(location)
        
        if "hooks" not in settings:
            settings["hooks"] = {}
        
        if event not in settings["hooks"]:
            settings["hooks"][event] = []
        
        # Build hook configuration
        hook_config = {
            "hooks": [{
                "type": "command",
                "command": command
            }]
        }
        
        if timeout:
            hook_config["hooks"][0]["timeout"] = timeout
        
        if matcher and event in [HookEvent.PRE_TOOL_USE, HookEvent.POST_TOOL_USE]:
            hook_config["matcher"] = matcher
        
        # Check for duplicates
        for existing in settings["hooks"][event]:
            if existing.get("hooks", [{}])[0].get("command") == command:
                console.print(f"[yellow]Hook already exists for {event}[/yellow]")
                return False
        
        settings["hooks"][event].append(hook_config)
        
        if self.save_settings(location, settings):
            console.print(f"[green]✓ Hook added to {event}[/green]")
            return True
        return False
    
    def remove_hook(
        self,
        location: SettingsLocation,
        event: HookEvent,
        command: str
    ) -> bool:
        """Remove a hook from settings"""
        settings = self.load_settings(location)
        
        if event not in settings.get("hooks", {}):
            console.print(f"[yellow]No hooks found for {event}[/yellow]")
            return False
        
        original_count = len(settings["hooks"][event])
        settings["hooks"][event] = [
            hook for hook in settings["hooks"][event]
            if hook.get("hooks", [{}])[0].get("command") != command
        ]
        
        if len(settings["hooks"][event]) < original_count:
            # Remove empty event entries
            if not settings["hooks"][event]:
                del settings["hooks"][event]
            
            if self.save_settings(location, settings):
                console.print(f"[green]✓ Hook removed from {event}[/green]")
                return True
        else:
            console.print(f"[yellow]Hook not found in {event}[/yellow]")
        
        return False
    
    def list_hooks(self, location: SettingsLocation) -> Dict:
        """List all hooks in a settings file"""
        settings = self.load_settings(location)
        return settings.get("hooks", {})


# CLI Commands
manager = HookManager()


@app.command()
def add(
    event: HookEvent = typer.Argument(..., help="Hook event type"),
    command: str = typer.Argument(..., help="Command to execute"),
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
    matcher: Optional[str] = typer.Option(None, "--matcher", "-m", help="Tool matcher pattern (for Pre/PostToolUse)"),
    timeout: Optional[int] = typer.Option(None, "--timeout", "-t", help="Command timeout in seconds"),
):
    """Add a new hook to settings"""
    manager.add_hook(location, event, command, matcher, timeout)


@app.command()
def remove(
    event: HookEvent = typer.Argument(..., help="Hook event type"),
    command: str = typer.Argument(..., help="Command to remove"),
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
):
    """Remove a hook from settings"""
    manager.remove_hook(location, event, command)


@app.command()
def list(
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
    event: Optional[HookEvent] = typer.Option(None, "--event", "-e", help="Filter by event type"),
):
    """List all configured hooks"""
    hooks = manager.list_hooks(location)
    
    if not hooks:
        console.print(f"[yellow]No hooks configured in {location.value} settings[/yellow]")
        return
    
    # Create table
    table = Table(title=f"Hooks in {location.value} settings")
    table.add_column("Event", style="cyan")
    table.add_column("Matcher", style="yellow")
    table.add_column("Command", style="green")
    table.add_column("Timeout", style="magenta")
    
    for hook_event, hook_list in hooks.items():
        if event and hook_event != event:
            continue
        
        for hook_config in hook_list:
            matcher = hook_config.get("matcher", "-")
            for hook in hook_config.get("hooks", []):
                command = hook.get("command", "")
                timeout = str(hook.get("timeout", "-"))
                
                # Truncate long commands
                if len(command) > 50:
                    command = command[:47] + "..."
                
                table.add_row(hook_event, matcher, command, timeout)
    
    console.print(table)


@app.command()
def show(
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
):
    """Show the full settings file with syntax highlighting"""
    path = manager.get_settings_path(location)
    
    if not path.exists():
        console.print(f"[yellow]Settings file not found: {path}[/yellow]")
        return
    
    with open(path, 'r') as f:
        content = f.read()
    
    syntax = Syntax(content, "json", theme="monokai", line_numbers=True)
    console.print(syntax)


@app.command()
def quick_install():
    """Quick install common hooks"""
    console.print("[bold cyan]Quick Hook Installation[/bold cyan]")
    
    presets = {
        "1": {
            "name": "Basic Linting",
            "hooks": [
                (HookEvent.POST_TOOL_USE, "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh", "Edit|Write|MultiEdit", 30),
            ]
        },
        "2": {
            "name": "Quality Assurance",
            "hooks": [
                (HookEvent.POST_TOOL_USE, "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh", "Edit|Write|MultiEdit", 30),
                (HookEvent.POST_TOOL_USE, "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/auto-formatter.sh", "Edit|Write|MultiEdit", 20),
                (HookEvent.STOP, "$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py", None, 20),
            ]
        },
        "3": {
            "name": "Smart Context",
            "hooks": [
                (HookEvent.SESSION_START, "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/branch-context-loader.sh", None, 10),
                (HookEvent.USER_PROMPT_SUBMIT, "$CLAUDE_PROJECT_DIR/.claude/hooks/python/prompt-enhancer.py", None, 10),
            ]
        },
        "4": {
            "name": "Subagent Support",
            "hooks": [
                (HookEvent.PRE_TOOL_USE, "$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-context-preparer.py", "Task", 10),
                (HookEvent.SUBAGENT_STOP, "$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-work-validator.py", None, 15),
            ]
        },
    }
    
    console.print("\n[bold]Available Presets:[/bold]")
    for key, preset in presets.items():
        console.print(f"  {key}. {preset['name']}")
    
    choice = Prompt.ask("\nSelect preset", choices=list(presets.keys()))
    location_str = Prompt.ask("Install to", choices=["user", "project", "local"], default="local")
    location = SettingsLocation(location_str)
    
    preset = presets[choice]
    console.print(f"\n[cyan]Installing {preset['name']} hooks...[/cyan]")
    
    for event, command, matcher, timeout in preset['hooks']:
        manager.add_hook(location, event, command, matcher, timeout)
    
    console.print(f"\n[green]✓ {preset['name']} hooks installed![/green]")


@app.command()
def validate(
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
):
    """Validate hooks configuration"""
    settings = manager.load_settings(location)
    hooks = settings.get("hooks", {})
    
    if not hooks:
        console.print(f"[yellow]No hooks configured in {location.value} settings[/yellow]")
        return
    
    issues = []
    warnings = []
    
    for event, hook_list in hooks.items():
        # Check valid event names
        if event not in [e.value for e in HookEvent]:
            issues.append(f"Invalid event type: {event}")
        
        for hook_config in hook_list:
            # Check for matcher on non-tool events
            if "matcher" in hook_config and event not in ["PreToolUse", "PostToolUse"]:
                warnings.append(f"Matcher ignored for {event} event")
            
            # Check hook commands exist
            for hook in hook_config.get("hooks", []):
                command = hook.get("command", "")
                if command.startswith("$CLAUDE_PROJECT_DIR"):
                    # Check if file exists in project
                    file_path = command.replace("$CLAUDE_PROJECT_DIR", ".")
                    if not Path(file_path).exists():
                        warnings.append(f"Hook file not found: {file_path}")
                
                # Check timeout values
                timeout = hook.get("timeout")
                if timeout and (timeout < 1 or timeout > 600):
                    warnings.append(f"Unusual timeout value: {timeout}s")
    
    if issues:
        console.print("[red]Issues found:[/red]")
        for issue in issues:
            console.print(f"  ✗ {issue}")
    
    if warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for warning in warnings:
            console.print(f"  ⚠ {warning}")
    
    if not issues and not warnings:
        console.print("[green]✓ All hooks are valid![/green]")


@app.command()
def export(
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
    output: Path = typer.Argument(..., help="Output file path"),
):
    """Export hooks configuration to a file"""
    settings = manager.load_settings(location)
    
    with open(output, 'w') as f:
        json.dump(settings, f, indent=2)
    
    console.print(f"[green]✓ Exported settings to {output}[/green]")


@app.command()
def import_hooks(
    input_file: Path = typer.Argument(..., help="Input file path"),
    location: SettingsLocation = typer.Option(SettingsLocation.LOCAL, "--location", "-l", help="Settings file location"),
    merge: bool = typer.Option(False, "--merge", "-m", help="Merge with existing hooks"),
):
    """Import hooks configuration from a file"""
    if not input_file.exists():
        console.print(f"[red]File not found: {input_file}[/red]")
        return
    
    try:
        with open(input_file, 'r') as f:
            new_settings = json.load(f)
    except json.JSONDecodeError:
        console.print(f"[red]Invalid JSON in {input_file}[/red]")
        return
    
    if merge:
        current_settings = manager.load_settings(location)
        # Merge hooks
        for event, hooks in new_settings.get("hooks", {}).items():
            if event not in current_settings.get("hooks", {}):
                current_settings.setdefault("hooks", {})[event] = []
            current_settings["hooks"][event].extend(hooks)
        new_settings = current_settings
    
    if manager.save_settings(location, new_settings):
        console.print(f"[green]✓ Imported settings to {location.value}[/green]")


if __name__ == "__main__":
    app()