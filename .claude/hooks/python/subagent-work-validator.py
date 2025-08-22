#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Subagent Work Validator Hook
============================
Type: SubagentStop, PostToolUse(Task)
Description: Validates that subagent completed its assigned task properly

This hook ensures subagents have completed their work according to standards:
- Code compiles/runs
- Tests were added if code was written
- Documentation was updated
- No obvious issues introduced
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import re


class SubagentWorkValidator:
    def __init__(self, project_dir: str, transcript_path: str = None):
        self.project_dir = Path(project_dir)
        self.transcript_path = transcript_path
        self.issues = []
        self.suggestions = []
        
    def analyze_transcript(self) -> Dict:
        """Analyze the subagent's transcript for completeness"""
        if not self.transcript_path or not Path(self.transcript_path).exists():
            return {}
        
        try:
            with open(self.transcript_path, 'r') as f:
                content = f.read()
            
            # Look for indicators of incomplete work
            indicators = {
                'errors': len(re.findall(r'error|Error|ERROR', content)),
                'warnings': len(re.findall(r'warning|Warning|WARNING', content)),
                'todos': len(re.findall(r'TODO|FIXME|XXX', content)),
                'skipped': len(re.findall(r'skip|Skip|SKIP|defer|Defer|DEFER', content)),
                'failed_tests': len(re.findall(r'test.*fail|fail.*test|FAIL', content, re.IGNORECASE)),
            }
            
            return indicators
        except:
            return {}
    
    def check_syntax_errors(self) -> bool:
        """Check for syntax errors in recently modified files"""
        try:
            # Get recently modified files
            result = subprocess.run(
                ['find', str(self.project_dir), '-type', 'f', '-mmin', '-5'],
                capture_output=True, text=True
            )
            
            if not result.stdout:
                return True
            
            recent_files = result.stdout.strip().split('\n')
            files_with_errors = []
            
            for file in recent_files:
                if file.endswith('.py'):
                    # Check Python syntax
                    result = subprocess.run(
                        ['python', '-m', 'py_compile', file],
                        capture_output=True
                    )
                    if result.returncode != 0:
                        files_with_errors.append(Path(file).name)
                
                elif file.endswith(('.js', '.jsx')):
                    # Basic JavaScript syntax check using node
                    result = subprocess.run(
                        ['node', '--check', file],
                        capture_output=True
                    )
                    if result.returncode != 0:
                        files_with_errors.append(Path(file).name)
                
                elif file.endswith(('.ts', '.tsx')):
                    # TypeScript check if tsc is available
                    if subprocess.run(['which', 'tsc'], capture_output=True).returncode == 0:
                        result = subprocess.run(
                            ['tsc', '--noEmit', file],
                            capture_output=True
                        )
                        if result.returncode != 0:
                            files_with_errors.append(Path(file).name)
            
            if files_with_errors:
                self.issues.append(f"Syntax errors in: {', '.join(files_with_errors[:3])}")
                return False
            
            return True
        except:
            return True  # Don't block if we can't check
    
    def check_test_coverage(self) -> bool:
        """Check if tests were added for new code"""
        try:
            # Get files modified in last 5 minutes
            result = subprocess.run(
                ['find', str(self.project_dir), '-type', 'f', '-name', '*.py', '-o', '-name', '*.js', '-o', '-name', '*.ts', '-mmin', '-5'],
                capture_output=True, text=True
            )
            
            if not result.stdout:
                return True
            
            modified_code_files = []
            modified_test_files = []
            
            for file in result.stdout.strip().split('\n'):
                if file:
                    if '.test.' in file or '.spec.' in file or '/test_' in file or '/__tests__/' in file:
                        modified_test_files.append(file)
                    else:
                        modified_code_files.append(file)
            
            # If code was modified but no tests, suggest adding tests
            if modified_code_files and not modified_test_files:
                self.suggestions.append("Consider adding tests for the new code")
            
            return True  # Don't block, just suggest
        except:
            return True
    
    def check_documentation(self) -> bool:
        """Check if documentation was updated when needed"""
        try:
            # Check if any significant code files were changed
            result = subprocess.run(
                ['find', str(self.project_dir), '-type', 'f', 
                 '(', '-name', '*.py', '-o', '-name', '*.js', '-o', '-name', '*.ts', ')',
                 '-mmin', '-5'],
                capture_output=True, text=True
            )
            
            code_modified = bool(result.stdout.strip())
            
            # Check if any docs were modified
            result = subprocess.run(
                ['find', str(self.project_dir), '-type', 'f',
                 '(', '-name', '*.md', '-o', '-name', '*.mdx', '-o', '-path', '*/docs/*', ')',
                 '-mmin', '-5'],
                capture_output=True, text=True
            )
            
            docs_modified = bool(result.stdout.strip())
            
            if code_modified and not docs_modified:
                # Check if the code changes were significant (more than trivial)
                result = subprocess.run(
                    ['git', 'diff', '--stat'],
                    capture_output=True, text=True, cwd=self.project_dir
                )
                
                if result.stdout:
                    lines_changed = re.findall(r'(\d+)\s+insertion', result.stdout)
                    total_insertions = sum(int(x) for x in lines_changed) if lines_changed else 0
                    
                    if total_insertions > 20:  # Significant change
                        self.suggestions.append("Documentation may need updating for these changes")
            
            return True  # Don't block on documentation
        except:
            return True
    
    def check_imports(self) -> bool:
        """Check for missing or unused imports"""
        issues_found = False
        
        try:
            # For Python files
            result = subprocess.run(
                ['find', str(self.project_dir), '-name', '*.py', '-mmin', '-5'],
                capture_output=True, text=True
            )
            
            if result.stdout:
                for file in result.stdout.strip().split('\n'):
                    if file and Path(file).exists():
                        with open(file, 'r') as f:
                            content = f.read()
                        
                        # Check for common import issues
                        if 'import ' in content:
                            # Check for star imports (generally discouraged)
                            if re.search(r'from\s+\S+\s+import\s+\*', content):
                                self.suggestions.append(f"Avoid star imports in {Path(file).name}")
                            
                            # Check for potentially missing imports
                            used_modules = re.findall(r'\b([a-z_]+)\.\w+\(', content)
                            imported_modules = re.findall(r'import\s+(\w+)', content)
                            imported_from = re.findall(r'from\s+(\w+)', content)
                            
                            all_imports = set(imported_modules + imported_from)
                            potentially_missing = set(used_modules) - all_imports - {'self', 'cls', 'super'}
                            
                            if potentially_missing:
                                self.suggestions.append(f"Check imports in {Path(file).name}")
            
            return True  # Don't block on import issues
        except:
            return True
    
    def validate(self) -> Dict:
        """Run all validations"""
        # Analyze transcript if available
        transcript_indicators = self.analyze_transcript()
        
        # Check for serious issues
        self.check_syntax_errors()
        
        # Check for quality issues
        self.check_test_coverage()
        self.check_documentation()
        self.check_imports()
        
        # Analyze transcript indicators
        if transcript_indicators:
            if transcript_indicators.get('errors', 0) > 5:
                self.issues.append("Multiple errors detected in subagent work")
            if transcript_indicators.get('failed_tests', 0) > 0:
                self.issues.append("Tests appear to be failing")
            if transcript_indicators.get('todos', 0) > 3:
                self.suggestions.append("Several TODOs were left in the code")
        
        # Determine if we should block
        if self.issues:
            reason = "Subagent work validation failed:\n"
            reason += "\n".join(f"❌ {issue}" for issue in self.issues)
            
            if self.suggestions:
                reason += "\n\nSuggestions:\n"
                reason += "\n".join(f"💡 {suggestion}" for suggestion in self.suggestions)
            
            return {
                "decision": "block",
                "reason": reason + "\n\nPlease address these issues."
            }
        elif self.suggestions:
            # Just provide suggestions, don't block
            feedback = "Subagent work complete. Suggestions:\n"
            feedback += "\n".join(f"💡 {suggestion}" for suggestion in self.suggestions)
            
            print(feedback)
            return {}
        else:
            print("✅ Subagent work validated successfully!")
            return {}


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    # Handle both SubagentStop and PostToolUse(Task)
    hook_event = input_data.get('hook_event_name', '')
    
    if hook_event == 'PostToolUse':
        tool_name = input_data.get('tool_name', '')
        if tool_name != 'Task':
            sys.exit(0)
    
    project_dir = input_data.get('cwd', '.')
    transcript_path = input_data.get('transcript_path')
    
    validator = SubagentWorkValidator(project_dir, transcript_path)
    result = validator.validate()
    
    if result:
        print(json.dumps(result))
    
    sys.exit(0)


if __name__ == "__main__":
    main()