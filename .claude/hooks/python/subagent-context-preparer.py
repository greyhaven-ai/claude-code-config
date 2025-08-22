#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pygments"]
# ///
"""
Subagent Context Preparer Hook
==============================
Type: PreToolUse (Task)
Description: Prepares optimal context for subagent tasks

This hook analyzes the task description and injects relevant context
to help subagents complete their work independently and correctly.
"""

import json
import sys
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set


class SubagentContextPreparer:
    def __init__(self, project_dir: str, task_description: str):
        self.project_dir = Path(project_dir)
        self.task = task_description.lower()
        self.context_items = []
        
    def detect_task_type(self) -> Dict[str, bool]:
        """Detect what type of task the subagent will perform"""
        return {
            'research': any(word in self.task for word in ['research', 'find', 'search', 'analyze', 'investigate']),
            'implementation': any(word in self.task for word in ['implement', 'create', 'build', 'add', 'write']),
            'refactoring': any(word in self.task for word in ['refactor', 'optimize', 'improve', 'clean', 'reorganize']),
            'testing': any(word in self.task for word in ['test', 'spec', 'coverage', 'unit test', 'integration']),
            'debugging': any(word in self.task for word in ['debug', 'fix', 'bug', 'error', 'issue']),
            'documentation': any(word in self.task for word in ['document', 'docs', 'readme', 'comment', 'explain']),
            'review': any(word in self.task for word in ['review', 'check', 'validate', 'verify', 'audit']),
        }
    
    def get_project_structure_context(self) -> Optional[str]:
        """Provide project structure overview"""
        context = ["=== Project Structure Overview ==="]
        
        # Get main directories
        important_dirs = []
        for pattern in ['src', 'lib', 'app', 'components', 'pages', 'api', 'tests', 'docs']:
            dir_path = self.project_dir / pattern
            if dir_path.exists() and dir_path.is_dir():
                important_dirs.append(pattern)
        
        if important_dirs:
            context.append(f"Key directories: {', '.join(important_dirs)}")
        
        # Detect project type
        project_types = []
        if (self.project_dir / 'package.json').exists():
            project_types.append('Node.js/JavaScript')
        if (self.project_dir / 'pyproject.toml').exists() or (self.project_dir / 'setup.py').exists():
            project_types.append('Python')
        if (self.project_dir / 'go.mod').exists():
            project_types.append('Go')
        if (self.project_dir / 'Cargo.toml').exists():
            project_types.append('Rust')
        
        if project_types:
            context.append(f"Project type: {', '.join(project_types)}")
        
        # Get file count by extension
        extensions = {}
        for ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java']:
            count = len(list(self.project_dir.rglob(f'*{ext}')))
            if count > 0:
                extensions[ext] = count
        
        if extensions:
            context.append("File distribution:")
            for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:5]:
                context.append(f"  {ext}: {count} files")
        
        return "\n".join(context) if len(context) > 1 else None
    
    def get_coding_standards(self) -> Optional[str]:
        """Extract coding standards from config files"""
        context = ["=== Coding Standards ==="]
        found_standards = False
        
        # Check for linter configs
        if (self.project_dir / 'pyproject.toml').exists():
            try:
                with open(self.project_dir / 'pyproject.toml', 'r') as f:
                    content = f.read()
                    if '[tool.ruff]' in content:
                        context.append("Python: Using ruff (see pyproject.toml)")
                        # Extract key settings
                        if 'line-length' in content:
                            match = re.search(r'line-length\s*=\s*(\d+)', content)
                            if match:
                                context.append(f"  - Line length: {match.group(1)}")
                        found_standards = True
            except:
                pass
        
        if (self.project_dir / 'eslint.config.js').exists() or (self.project_dir / '.eslintrc.js').exists():
            context.append("JavaScript: Using ESLint (see eslint config)")
            found_standards = True
        
        if (self.project_dir / '.prettierrc').exists() or (self.project_dir / 'prettier.config.js').exists():
            context.append("Formatting: Using Prettier")
            found_standards = True
        
        # Check for editor config
        if (self.project_dir / '.editorconfig').exists():
            context.append("Editor: Using .editorconfig")
            found_standards = True
        
        return "\n".join(context) if found_standards else None
    
    def get_similar_implementations(self) -> Optional[str]:
        """Find similar implementations in the codebase"""
        context = ["=== Similar Implementations ==="]
        
        # Extract key terms from task
        key_terms = re.findall(r'\b[A-Z][a-z]+|[a-z]+', self.task)
        key_terms = [term for term in key_terms if len(term) > 3 and term not in 
                    ['that', 'this', 'with', 'from', 'into', 'have', 'been', 'will']]
        
        if not key_terms:
            return None
        
        # Search for files containing these terms
        similar_files = set()
        for term in key_terms[:3]:  # Limit to first 3 terms
            try:
                result = subprocess.run(
                    ['grep', '-l', '-r', '-i', term, str(self.project_dir),
                     '--include=*.py', '--include=*.js', '--include=*.ts'],
                    capture_output=True, text=True, timeout=2
                )
                if result.stdout:
                    files = result.stdout.strip().split('\n')[:5]
                    similar_files.update(files)
            except:
                pass
        
        if similar_files:
            context.append("Files with potentially similar logic:")
            for file in list(similar_files)[:5]:
                try:
                    relative_path = Path(file).relative_to(self.project_dir)
                    context.append(f"  - {relative_path}")
                except:
                    pass
            
            return "\n".join(context)
        
        return None
    
    def get_test_examples(self) -> Optional[str]:
        """Provide test examples if task involves testing"""
        context = ["=== Test Examples ==="]
        
        # Find existing test files
        test_files = []
        for pattern in ['**/*.test.*', '**/*.spec.*', '**/test_*.py']:
            test_files.extend(self.project_dir.glob(pattern))
        
        if not test_files:
            return None
        
        # Get a sample test file structure
        sample_test = test_files[0]
        context.append(f"Example test structure from {sample_test.name}:")
        
        try:
            with open(sample_test, 'r') as f:
                lines = f.readlines()[:30]  # First 30 lines
                
            # Extract test structure
            for line in lines:
                if any(pattern in line for pattern in ['describe(', 'it(', 'test(', 'def test_', 'class Test']):
                    context.append(f"  {line.strip()[:60]}...")
        except:
            pass
        
        return "\n".join(context) if len(context) > 1 else None
    
    def get_recent_patterns(self) -> Optional[str]:
        """Get recently used patterns from git history"""
        context = ["=== Recent Code Patterns ==="]
        
        try:
            # Get files changed in last 10 commits
            result = subprocess.run(
                ['git', 'log', '--name-only', '--pretty=format:', '-10'],
                capture_output=True, text=True, cwd=self.project_dir
            )
            
            if result.stdout:
                changed_files = [f for f in result.stdout.strip().split('\n') if f]
                file_types = {}
                for file in changed_files:
                    ext = Path(file).suffix
                    if ext:
                        file_types[ext] = file_types.get(ext, 0) + 1
                
                if file_types:
                    context.append("Recently modified file types:")
                    for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:5]:
                        context.append(f"  {ext}: {count} changes")
                    
                    return "\n".join(context)
        except:
            pass
        
        return None
    
    def get_performance_guidelines(self) -> Optional[str]:
        """Provide performance guidelines if relevant"""
        task_type = self.detect_task_type()
        
        if not (task_type['implementation'] or task_type['refactoring']):
            return None
        
        context = ["=== Performance Guidelines ==="]
        
        # Language-specific guidelines
        if (self.project_dir / 'package.json').exists():
            context.extend([
                "JavaScript/TypeScript:",
                "  - Prefer async/await over callbacks",
                "  - Use appropriate data structures (Map/Set vs Object)",
                "  - Minimize bundle size for frontend code",
                "  - Consider memoization for expensive computations"
            ])
        
        if (self.project_dir / 'pyproject.toml').exists():
            context.extend([
                "Python:",
                "  - Use generators for large datasets",
                "  - Prefer list comprehensions over loops where readable",
                "  - Consider using dataclasses or Pydantic for data models",
                "  - Profile before optimizing"
            ])
        
        return "\n".join(context) if len(context) > 1 else None
    
    def prepare_context(self) -> str:
        """Prepare complete context for subagent"""
        task_type = self.detect_task_type()
        contexts = []
        
        # Always provide project structure
        project_context = self.get_project_structure_context()
        if project_context:
            contexts.append(project_context)
        
        # Always provide coding standards
        standards = self.get_coding_standards()
        if standards:
            contexts.append(standards)
        
        # Task-specific context
        if task_type['implementation'] or task_type['refactoring']:
            similar = self.get_similar_implementations()
            if similar:
                contexts.append(similar)
            
            perf = self.get_performance_guidelines()
            if perf:
                contexts.append(perf)
        
        if task_type['testing']:
            test_examples = self.get_test_examples()
            if test_examples:
                contexts.append(test_examples)
        
        # Recent patterns for any task
        patterns = self.get_recent_patterns()
        if patterns:
            contexts.append(patterns)
        
        # Add task-specific tips
        contexts.append("=== Task Guidelines ===")
        if task_type['research']:
            contexts.append("Research task: Be thorough and provide sources for findings")
        if task_type['implementation']:
            contexts.append("Implementation task: Follow existing patterns and test your code")
        if task_type['testing']:
            contexts.append("Testing task: Aim for comprehensive coverage including edge cases")
        if task_type['debugging']:
            contexts.append("Debugging task: Identify root cause, not just symptoms")
        if task_type['documentation']:
            contexts.append("Documentation task: Be clear, concise, and include examples")
        
        return "\n\n".join(contexts)


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    tool_name = input_data.get('tool_name', '')
    
    # Only process Task tool calls
    if tool_name != 'Task':
        sys.exit(0)
    
    tool_input = input_data.get('tool_input', {})
    task_description = tool_input.get('prompt', '')
    project_dir = input_data.get('cwd', '.')
    
    if not task_description:
        sys.exit(0)
    
    preparer = SubagentContextPreparer(project_dir, task_description)
    context = preparer.prepare_context()
    
    # Inject context into the task description
    enhanced_prompt = f"""[Subagent Context]
{context}

[Original Task]
{task_description}

Remember to:
1. Follow the project's coding standards
2. Use similar implementations as reference
3. Test your changes if implementing code
4. Update documentation if needed
5. Consider performance implications"""
    
    # Modify the tool input to include enhanced context
    tool_input['prompt'] = enhanced_prompt
    
    # Auto-approve with enhanced context
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Task enhanced with project context"
        },
        "suppressOutput": True
    }
    
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()