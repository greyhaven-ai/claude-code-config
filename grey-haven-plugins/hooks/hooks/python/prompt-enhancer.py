#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["pygments", "networkx"]
# ///
"""
Prompt Enhancer Hook
====================
Type: UserPromptSubmit
Description: Intelligently enhances user prompts with relevant context

This hook analyzes user prompts and automatically injects relevant context
like documentation, test coverage, dependency graphs, and recent changes.
"""

import json
import sys
import re
from pathlib import Path
import subprocess
from typing import Dict, List, Set, Optional


class PromptEnhancer:
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.context_additions = []
        
    def detect_intent(self, prompt: str) -> Dict[str, bool]:
        """Detect user intent from prompt keywords"""
        prompt_lower = prompt.lower()
        
        return {
            'testing': any(word in prompt_lower for word in ['test', 'spec', 'coverage', 'jest', 'pytest']),
            'debugging': any(word in prompt_lower for word in ['bug', 'fix', 'error', 'issue', 'debug']),
            'feature': any(word in prompt_lower for word in ['implement', 'add', 'create', 'feature', 'build']),
            'refactor': any(word in prompt_lower for word in ['refactor', 'optimize', 'improve', 'clean']),
            'documentation': any(word in prompt_lower for word in ['document', 'docs', 'readme', 'comment']),
            'api': any(word in prompt_lower for word in ['api', 'endpoint', 'route', 'request', 'response']),
            'database': any(word in prompt_lower for word in ['database', 'query', 'sql', 'migration', 'schema']),
            'security': any(word in prompt_lower for word in ['security', 'auth', 'permission', 'vulnerability']),
            'performance': any(word in prompt_lower for word in ['performance', 'speed', 'optimize', 'slow']),
        }
    
    def extract_file_references(self, prompt: str) -> List[str]:
        """Extract file paths mentioned in the prompt"""
        files = []
        
        # Common file patterns
        patterns = [
            r'[./\w-]+\.\w+',  # Files with extensions
            r'`([^`]+)`',  # Backtick references
            r'"([^"]+)"',  # Quoted references
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, prompt)
            for match in matches:
                if '.' in match and '/' not in match[:2]:  # Likely a file
                    # Search for the file
                    result = subprocess.run(
                        ['find', str(self.project_dir), '-name', match],
                        capture_output=True, text=True
                    )
                    if result.stdout.strip():
                        files.extend(result.stdout.strip().split('\n'))
                elif Path(self.project_dir / match).exists():
                    files.append(str(self.project_dir / match))
        
        return list(set(files))
    
    def get_test_coverage_context(self, files: List[str]) -> Optional[str]:
        """Get test coverage for mentioned files"""
        if not files:
            return None
            
        context = []
        for file in files[:3]:  # Limit to first 3 files
            # Check for corresponding test file
            base_path = Path(file)
            test_patterns = [
                base_path.parent / f"{base_path.stem}.test{base_path.suffix}",
                base_path.parent / f"{base_path.stem}.spec{base_path.suffix}",
                base_path.parent / "__tests__" / f"{base_path.stem}.test{base_path.suffix}",
            ]
            
            for test_path in test_patterns:
                if test_path.exists():
                    context.append(f"Test file exists: {test_path.relative_to(self.project_dir)}")
                    break
            else:
                context.append(f"No test file found for: {Path(file).relative_to(self.project_dir)}")
        
        return "\n".join(context) if context else None
    
    def get_recent_changes_context(self, files: List[str]) -> Optional[str]:
        """Get recent git changes for mentioned files"""
        if not files:
            return None
            
        context = []
        for file in files[:3]:
            try:
                # Get last 3 commits for this file
                result = subprocess.run(
                    ['git', 'log', '--oneline', '-3', '--', file],
                    capture_output=True, text=True, cwd=self.project_dir
                )
                if result.stdout.strip():
                    relative_path = Path(file).relative_to(self.project_dir)
                    context.append(f"Recent changes to {relative_path}:")
                    context.append(result.stdout.strip())
            except:
                pass
        
        return "\n".join(context) if context else None
    
    def get_dependency_context(self, files: List[str]) -> Optional[str]:
        """Get import/dependency information for mentioned files"""
        if not files:
            return None
            
        context = []
        for file in files[:2]:
            if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                try:
                    with open(file, 'r') as f:
                        lines = f.readlines()[:50]  # Check first 50 lines
                    
                    imports = []
                    for line in lines:
                        if file.endswith('.py'):
                            if line.strip().startswith(('import ', 'from ')):
                                imports.append(line.strip())
                        else:  # JavaScript/TypeScript
                            if 'import' in line or 'require(' in line:
                                imports.append(line.strip())
                    
                    if imports:
                        relative_path = Path(file).relative_to(self.project_dir)
                        context.append(f"Dependencies in {relative_path}:")
                        context.extend(imports[:5])  # First 5 imports
                except:
                    pass
        
        return "\n".join(context) if context else None
    
    def get_api_context(self) -> Optional[str]:
        """Get API-related context if API work is detected"""
        context = []
        
        # Look for API specification files
        api_files = [
            "openapi.yaml", "openapi.yml", "openapi.json",
            "swagger.yaml", "swagger.yml", "swagger.json",
            "api.yaml", "api.yml", "api.json"
        ]
        
        for api_file in api_files:
            api_path = self.project_dir / api_file
            if api_path.exists():
                context.append(f"API specification found: {api_file}")
                break
        
        # Look for API route files
        for pattern in ['**/routes/**/*.{js,ts,py}', '**/api/**/*.{js,ts,py}', '**/controllers/**/*.{js,ts,py}']:
            result = subprocess.run(
                ['find', str(self.project_dir), '-path', pattern.replace('**/', '*/').replace('{js,ts,py}', '*')],
                capture_output=True, text=True
            )
            if result.stdout.strip():
                files = result.stdout.strip().split('\n')[:3]
                context.append(f"API files found: {', '.join([Path(f).name for f in files])}")
                break
        
        return "\n".join(context) if context else None
    
    def get_database_context(self) -> Optional[str]:
        """Get database-related context"""
        context = []
        
        # Look for migration files
        migration_dirs = ['migrations', 'db/migrations', 'database/migrations']
        for mig_dir in migration_dirs:
            mig_path = self.project_dir / mig_dir
            if mig_path.exists():
                recent_migrations = sorted(mig_path.glob('*'))[-3:]
                if recent_migrations:
                    context.append(f"Recent migrations: {', '.join([f.name for f in recent_migrations])}")
                break
        
        # Look for schema files
        schema_files = ['schema.sql', 'schema.prisma', 'models.py', 'db/schema.rb']
        for schema_file in schema_files:
            schema_path = self.project_dir / schema_file
            if schema_path.exists():
                context.append(f"Database schema found: {schema_file}")
                break
        
        return "\n".join(context) if context else None
    
    def enhance_prompt(self, prompt: str) -> str:
        """Main enhancement logic"""
        intent = self.detect_intent(prompt)
        files = self.extract_file_references(prompt)
        
        contexts = []
        
        # Add file-specific contexts
        if files:
            contexts.append(f"Referenced files detected: {', '.join([Path(f).name for f in files[:5]])}")
            
            if intent['testing']:
                coverage_context = self.get_test_coverage_context(files)
                if coverage_context:
                    contexts.append("=== Test Coverage ===")
                    contexts.append(coverage_context)
            
            if intent['debugging']:
                changes_context = self.get_recent_changes_context(files)
                if changes_context:
                    contexts.append("=== Recent Changes ===")
                    contexts.append(changes_context)
            
            dep_context = self.get_dependency_context(files)
            if dep_context:
                contexts.append("=== Dependencies ===")
                contexts.append(dep_context)
        
        # Add intent-specific contexts
        if intent['api']:
            api_context = self.get_api_context()
            if api_context:
                contexts.append("=== API Context ===")
                contexts.append(api_context)
        
        if intent['database']:
            db_context = self.get_database_context()
            if db_context:
                contexts.append("=== Database Context ===")
                contexts.append(db_context)
        
        # Add branch context
        try:
            branch = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True, text=True, cwd=self.project_dir
            ).stdout.strip()
            if branch and branch not in ['main', 'master']:
                contexts.append(f"Current branch: {branch}")
        except:
            pass
        
        if contexts:
            return "\n\n".join(contexts)
        return None


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(1)
    
    prompt = input_data.get('prompt', '')
    project_dir = input_data.get('cwd', '.')
    
    enhancer = PromptEnhancer(project_dir)
    additional_context = enhancer.enhance_prompt(prompt)
    
    if additional_context:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"[Automated Context]\n{additional_context}"
            }
        }
        print(json.dumps(output))
    
    sys.exit(0)


if __name__ == "__main__":
    main()