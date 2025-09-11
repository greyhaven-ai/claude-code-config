#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

"""
Subagent Context Preparer - Prepare optimal context for subagent execution

Detects when a subagent is about to be invoked and prepares relevant context
to enhance subagent performance. Runs on PreToolUse with Task matcher.
"""

import sys
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class SubagentContextPreparer:
    def __init__(self):
        self.project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        self.context_dir = Path(self.project_dir) / '.claude' / 'context'
        self.context_dir.mkdir(parents=True, exist_ok=True)
        
        # Define context requirements for each subagent
        self.subagent_contexts = {
            'tdd-python-implementer': self.prepare_tdd_context,
            'security-orchestrator': self.prepare_security_context,
            'code-synthesis-analyzer': self.prepare_analysis_context,
            'git-diff-documentation-agent': self.prepare_git_context,
            'tech-docs-maintainer': self.prepare_docs_context,
            'code-clarity-refactorer': self.prepare_refactor_context,
            'web-docs-researcher': self.prepare_research_context,
            'bug-issue-creator': self.prepare_issue_context
        }
    
    def run_command(self, cmd: List[str]) -> Optional[str]:
        """Run a command and return output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_dir,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def prepare_tdd_context(self) -> Dict:
        """Prepare context for TDD Python implementer"""
        context = {
            'test_framework': self.detect_test_framework(),
            'test_directory': self.find_test_directory(),
            'coverage_config': self.find_coverage_config(),
            'python_version': self.run_command(['python', '--version']),
            'existing_tests': self.count_existing_tests()
        }
        
        # Write context file for subagent
        context_file = self.context_dir / 'tdd-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_security_context(self) -> Dict:
        """Prepare context for security orchestrator"""
        context = {
            'dependencies': self.get_dependencies(),
            'exposed_ports': self.find_exposed_ports(),
            'auth_files': self.find_auth_files(),
            'sensitive_patterns': self.find_sensitive_patterns(),
            'security_tools': self.detect_security_tools()
        }
        
        context_file = self.context_dir / 'security-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_analysis_context(self) -> Dict:
        """Prepare context for code synthesis analyzer"""
        context = {
            'recent_changes': self.get_recent_changes(),
            'code_metrics': self.calculate_code_metrics(),
            'dependencies': self.get_dependencies(),
            'test_coverage': self.get_test_coverage()
        }
        
        context_file = self.context_dir / 'analysis-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_git_context(self) -> Dict:
        """Prepare context for git diff documentation"""
        context = {
            'branch_name': self.run_command(['git', 'branch', '--show-current']),
            'uncommitted_files': self.run_command(['git', 'status', '--porcelain']),
            'recent_commits': self.run_command(['git', 'log', '--oneline', '-10']),
            'remote_url': self.run_command(['git', 'remote', 'get-url', 'origin'])
        }
        
        context_file = self.context_dir / 'git-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_docs_context(self) -> Dict:
        """Prepare context for documentation maintainer"""
        context = {
            'doc_files': self.find_documentation_files(),
            'readme_exists': os.path.exists(Path(self.project_dir) / 'README.md'),
            'api_endpoints': self.find_api_endpoints(),
            'doc_format': self.detect_doc_format()
        }
        
        context_file = self.context_dir / 'docs-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_refactor_context(self) -> Dict:
        """Prepare context for code clarity refactorer"""
        context = {
            'code_style': self.detect_code_style(),
            'linting_config': self.find_linting_config(),
            'complexity_metrics': self.calculate_complexity(),
            'duplicate_code': self.find_duplicate_patterns()
        }
        
        context_file = self.context_dir / 'refactor-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_research_context(self) -> Dict:
        """Prepare context for web docs researcher"""
        context = {
            'project_type': self.detect_project_type(),
            'main_technologies': self.detect_technologies(),
            'external_apis': self.find_external_apis(),
            'research_history': self.load_research_history()
        }
        
        context_file = self.context_dir / 'research-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    def prepare_issue_context(self) -> Dict:
        """Prepare context for bug issue creator"""
        context = {
            'repo_name': self.get_repo_name(),
            'issue_template': self.find_issue_template(),
            'labels': self.get_available_labels(),
            'recent_issues': self.get_recent_issues()
        }
        
        context_file = self.context_dir / 'issue-context.json'
        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)
        
        return context
    
    # Helper methods
    def detect_test_framework(self) -> str:
        """Detect which test framework is in use"""
        if os.path.exists(Path(self.project_dir) / 'pytest.ini'):
            return 'pytest'
        if os.path.exists(Path(self.project_dir) / 'setup.cfg'):
            with open(Path(self.project_dir) / 'setup.cfg') as f:
                if 'pytest' in f.read():
                    return 'pytest'
        return 'unittest'
    
    def find_test_directory(self) -> str:
        """Find the test directory"""
        for test_dir in ['tests', 'test', 'spec', 'tests_']:
            if os.path.exists(Path(self.project_dir) / test_dir):
                return test_dir
        return 'tests'
    
    def find_coverage_config(self) -> Optional[str]:
        """Find coverage configuration"""
        for config in ['.coveragerc', 'setup.cfg', 'pyproject.toml']:
            if os.path.exists(Path(self.project_dir) / config):
                return config
        return None
    
    def count_existing_tests(self) -> int:
        """Count existing test files"""
        count = 0
        for pattern in ['test_*.py', '*_test.py', '*_spec.py']:
            count += len(list(Path(self.project_dir).rglob(pattern)))
        return count
    
    def get_dependencies(self) -> List[str]:
        """Get project dependencies"""
        deps = []
        if os.path.exists(Path(self.project_dir) / 'requirements.txt'):
            with open(Path(self.project_dir) / 'requirements.txt') as f:
                deps.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
        if os.path.exists(Path(self.project_dir) / 'package.json'):
            deps.append('JavaScript dependencies present')
        return deps[:20]  # Limit to prevent context explosion
    
    def find_exposed_ports(self) -> List[str]:
        """Find potentially exposed ports in configuration"""
        ports = []
        # This is a simplified check - real implementation would be more thorough
        for file in Path(self.project_dir).rglob('*.yml'):
            try:
                with open(file) as f:
                    content = f.read()
                    if 'port' in content.lower():
                        ports.append(str(file))
            except:
                pass
        return ports[:10]
    
    def find_auth_files(self) -> List[str]:
        """Find authentication-related files"""
        auth_patterns = ['*auth*', '*login*', '*session*', '*token*', '*jwt*']
        auth_files = []
        for pattern in auth_patterns:
            auth_files.extend([str(f) for f in Path(self.project_dir).rglob(pattern)])
        return auth_files[:10]
    
    def find_sensitive_patterns(self) -> Dict:
        """Find potentially sensitive patterns"""
        return {
            'has_env_files': len(list(Path(self.project_dir).glob('.env*'))) > 0,
            'has_secrets': len(list(Path(self.project_dir).rglob('*secret*'))) > 0,
            'has_keys': len(list(Path(self.project_dir).rglob('*key*'))) > 0
        }
    
    def detect_security_tools(self) -> List[str]:
        """Detect security tools in use"""
        tools = []
        tool_files = {
            'bandit': '.bandit',
            'safety': '.safety-policy.json',
            'snyk': '.snyk'
        }
        for tool, file in tool_files.items():
            if os.path.exists(Path(self.project_dir) / file):
                tools.append(tool)
        return tools
    
    def get_recent_changes(self) -> List[str]:
        """Get recent file changes"""
        changes = self.run_command(['git', 'diff', '--name-only', 'HEAD~5..HEAD'])
        if changes:
            return changes.split('\n')[:20]
        return []
    
    def calculate_code_metrics(self) -> Dict:
        """Calculate basic code metrics"""
        metrics = {
            'python_files': len(list(Path(self.project_dir).rglob('*.py'))),
            'js_files': len(list(Path(self.project_dir).rglob('*.js'))),
            'total_lines': 0
        }
        return metrics
    
    def get_test_coverage(self) -> Optional[str]:
        """Get test coverage if available"""
        coverage_file = Path(self.project_dir) / '.coverage'
        if coverage_file.exists():
            return "Coverage data available"
        return None
    
    def find_documentation_files(self) -> List[str]:
        """Find documentation files"""
        doc_files = []
        for pattern in ['*.md', '*.rst', '*.txt']:
            doc_files.extend([str(f) for f in Path(self.project_dir).rglob(pattern)])
        return doc_files[:20]
    
    def find_api_endpoints(self) -> List[str]:
        """Find API endpoint definitions"""
        # Simplified - real implementation would parse actual routes
        endpoints = []
        for file in Path(self.project_dir).rglob('*.py'):
            try:
                with open(file) as f:
                    content = f.read()
                    if '@app.route' in content or '@router' in content:
                        endpoints.append(str(file))
            except:
                pass
        return endpoints[:10]
    
    def detect_doc_format(self) -> str:
        """Detect documentation format"""
        if len(list(Path(self.project_dir).rglob('*.rst'))) > 0:
            return 'reStructuredText'
        return 'Markdown'
    
    def detect_code_style(self) -> str:
        """Detect code style configuration"""
        if os.path.exists(Path(self.project_dir) / '.black'):
            return 'black'
        if os.path.exists(Path(self.project_dir) / '.flake8'):
            return 'flake8'
        if os.path.exists(Path(self.project_dir) / 'ruff.toml'):
            return 'ruff'
        return 'none'
    
    def find_linting_config(self) -> List[str]:
        """Find linting configuration files"""
        configs = []
        for config in ['.flake8', '.pylintrc', 'ruff.toml', '.eslintrc', '.prettierrc']:
            if os.path.exists(Path(self.project_dir) / config):
                configs.append(config)
        return configs
    
    def calculate_complexity(self) -> Dict:
        """Calculate code complexity metrics"""
        # Simplified version
        return {
            'needs_analysis': True,
            'files_to_check': len(list(Path(self.project_dir).rglob('*.py')))
        }
    
    def find_duplicate_patterns(self) -> Dict:
        """Find potential duplicate code patterns"""
        return {
            'analysis_needed': True,
            'common_patterns': []
        }
    
    def detect_project_type(self) -> str:
        """Detect project type"""
        if os.path.exists(Path(self.project_dir) / 'package.json'):
            return 'JavaScript/Node.js'
        if os.path.exists(Path(self.project_dir) / 'pyproject.toml'):
            return 'Python'
        if os.path.exists(Path(self.project_dir) / 'Cargo.toml'):
            return 'Rust'
        return 'Unknown'
    
    def detect_technologies(self) -> List[str]:
        """Detect main technologies"""
        tech = []
        file_checks = {
            'React': 'package.json',
            'Django': 'manage.py',
            'Flask': 'app.py',
            'FastAPI': 'main.py'
        }
        for name, file in file_checks.items():
            if os.path.exists(Path(self.project_dir) / file):
                tech.append(name)
        return tech
    
    def find_external_apis(self) -> List[str]:
        """Find references to external APIs"""
        # Simplified version
        return []
    
    def load_research_history(self) -> List[str]:
        """Load previous research topics"""
        history_file = self.context_dir / 'research-history.json'
        if history_file.exists():
            try:
                with open(history_file) as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def get_repo_name(self) -> Optional[str]:
        """Get repository name from git remote"""
        remote = self.run_command(['git', 'remote', 'get-url', 'origin'])
        if remote:
            # Extract repo name from URL
            if '/' in remote:
                return remote.rstrip('.git').split('/')[-1]
        return None
    
    def find_issue_template(self) -> Optional[str]:
        """Find issue template"""
        template_paths = [
            '.github/ISSUE_TEMPLATE',
            '.github/issue_template.md',
            'ISSUE_TEMPLATE.md'
        ]
        for path in template_paths:
            if os.path.exists(Path(self.project_dir) / path):
                return path
        return None
    
    def get_available_labels(self) -> List[str]:
        """Get available GitHub labels (simplified)"""
        return ['bug', 'enhancement', 'documentation', 'help wanted', 'question']
    
    def get_recent_issues(self) -> List[str]:
        """Get recent issues (would need GitHub API in real implementation)"""
        return []
    
    def process(self, data: Dict) -> Dict:
        """Process the PreToolUse event for Task tool"""
        tool = data.get('tool')
        if tool != 'Task':
            return {"decision": "approve"}
        
        params = data.get('params', {})
        subagent_type = params.get('subagent_type')
        
        if not subagent_type:
            return {"decision": "approve"}
        
        # Prepare context for the specific subagent
        preparer = self.subagent_contexts.get(subagent_type)
        if preparer:
            context = preparer()
            
            return {
                "decision": "approve",
                "systemMessage": f"🎯 Prepared context for {subagent_type} subagent\n" +
                               f"   Context saved to: .claude/context/"
            }
        
        return {"decision": "approve"}

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Process the event
        preparer = SubagentContextPreparer()
        result = preparer.process(input_data)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        error_response = {
            "decision": "approve",
            "error": f"Context preparer error: {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)

if __name__ == "__main__":
    main()