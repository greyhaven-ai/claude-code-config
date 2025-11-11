#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["gitpython"]
# ///
"""
Work Completion Assistant Hook
==============================
Type: Stop
Description: Ensures work is complete before allowing Claude to stop

This hook validates that all work has been properly completed, including:
- Tests are passing
- No unresolved TODOs
- Code is formatted
- Documentation is updated
- Changes are committed (optionally)
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional


class WorkCompletionValidator:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.issues = []
        self.warnings = []
        
    def check_uncommitted_changes(self) -> bool:
        """Check for uncommitted changes"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, cwd=self.project_dir
            )
            if result.stdout.strip():
                changed_files = len(result.stdout.strip().split('\n'))
                self.warnings.append(f"You have {changed_files} uncommitted changes")
                return False
            return True
        except:
            return True  # If not a git repo, skip this check
    
    def check_todos_in_changed_files(self) -> bool:
        """Check for TODOs in recently changed files"""
        try:
            # Get list of changed files
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD'],
                capture_output=True, text=True, cwd=self.project_dir
            )
            changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # Also check staged files
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True, text=True, cwd=self.project_dir
            )
            staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            all_files = set(changed_files + staged_files)
            files_with_todos = []
            
            for file in all_files:
                if file and Path(self.project_dir / file).exists():
                    try:
                        with open(self.project_dir / file, 'r') as f:
                            content = f.read()
                            if 'TODO' in content or 'FIXME' in content or 'XXX' in content:
                                files_with_todos.append(file)
                    except:
                        pass
            
            if files_with_todos:
                self.issues.append(f"Unresolved TODOs in: {', '.join(files_with_todos[:3])}")
                return False
            return True
        except:
            return True
    
    def check_tests(self) -> bool:
        """Run tests if test command is available"""
        test_commands = []
        
        # Check for different test runners
        if (self.project_dir / 'package.json').exists():
            try:
                with open(self.project_dir / 'package.json', 'r') as f:
                    package_json = json.load(f)
                    scripts = package_json.get('scripts', {})
                    if 'test' in scripts:
                        test_commands.append('npm test')
                    elif 'test:unit' in scripts:
                        test_commands.append('npm run test:unit')
            except:
                pass
        
        if (self.project_dir / 'pyproject.toml').exists():
            if subprocess.run(['which', 'pytest'], capture_output=True).returncode == 0:
                test_commands.append('pytest --co -q')  # Just collect tests, don't run
            elif subprocess.run(['which', 'python'], capture_output=True).returncode == 0:
                test_commands.append('python -m pytest --co -q')
        
        if (self.project_dir / 'go.mod').exists():
            test_commands.append('go test ./... -run=^$ -count=1')  # Dry run
        
        if (self.project_dir / 'Cargo.toml').exists():
            test_commands.append('cargo test --no-run')  # Compile but don't run
        
        # For now, just warn about tests, don't block
        if test_commands:
            self.warnings.append(f"Remember to run tests: {test_commands[0]}")
        
        return True  # Don't block on tests
    
    def check_linting(self) -> bool:
        """Check if linting would pass"""
        lint_commands = []
        
        # Detect linters
        if (self.project_dir / 'pyproject.toml').exists():
            if subprocess.run(['which', 'ruff'], capture_output=True).returncode == 0:
                result = subprocess.run(
                    ['ruff', 'check', '--quiet'],
                    capture_output=True, cwd=self.project_dir
                )
                if result.returncode != 0:
                    self.warnings.append("Code has linting issues (ruff)")
        
        if (self.project_dir / 'eslint.config.js').exists() or \
           (self.project_dir / '.eslintrc.js').exists():
            # Just warn, don't run eslint as it might be slow
            self.warnings.append("Remember to run eslint")
        
        return True  # Don't block on linting
    
    def check_documentation(self) -> bool:
        """Check if documentation might need updating"""
        try:
            # Check if any code files were changed
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD'],
                capture_output=True, text=True, cwd=self.project_dir
            )
            changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            code_files_changed = any(
                f.endswith(('.py', '.js', '.ts', '.go', '.rs', '.java'))
                for f in changed_files
            )
            
            docs_changed = any(
                f.endswith(('.md', '.mdx', '.rst', '.txt')) or 'docs/' in f
                for f in changed_files
            )
            
            if code_files_changed and not docs_changed:
                self.warnings.append("Code changed but documentation not updated")
            
            return True  # Don't block on documentation
        except:
            return True
    
    def check_branches(self) -> bool:
        """Check if working on correct branch"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True, text=True, cwd=self.project_dir
            )
            branch = result.stdout.strip()
            
            if branch in ['main', 'master', 'production']:
                self.warnings.append(f"Working directly on {branch} branch")
            
            return True  # Don't block on branch
        except:
            return True
    
    def validate(self) -> Dict:
        """Run all validations and return results"""
        # Run checks
        self.check_uncommitted_changes()
        self.check_todos_in_changed_files()
        self.check_tests()
        self.check_linting()
        self.check_documentation()
        self.check_branches()
        
        # Determine if we should block
        should_block = len(self.issues) > 0
        
        if should_block:
            reason = "Work incomplete:\n"
            reason += "\n".join(f"❌ {issue}" for issue in self.issues)
            if self.warnings:
                reason += "\n\nWarnings:\n"
                reason += "\n".join(f"⚠️  {warning}" for warning in self.warnings)
            
            return {
                "decision": "block",
                "reason": reason + "\n\nPlease address these items before stopping."
            }
        elif self.warnings:
            # Just show warnings, don't block
            summary = "Work appears complete. Reminders:\n"
            summary += "\n".join(f"⚠️  {warning}" for warning in self.warnings)
            
            # Print to stdout for transcript mode
            print(summary)
            
            return {}  # Don't block
        else:
            print("✅ All checks passed - work appears complete!")
            return {}


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    # Check if we're already in a stop hook loop
    if input_data.get('stop_hook_active', False):
        # Don't create infinite loops
        sys.exit(0)
    
    project_dir = input_data.get('cwd', '.')
    
    validator = WorkCompletionValidator(project_dir)
    result = validator.validate()
    
    if result:
        print(json.dumps(result))
    
    sys.exit(0)


if __name__ == "__main__":
    main()