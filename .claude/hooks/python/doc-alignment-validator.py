#!/usr/bin/env python3
"""
Documentation Alignment Validator Hook
=======================================
Type: PreToolUse (Task, Write, Edit)
Description: Validates that code changes maintain alignment with documentation

This hook intercepts code modifications and verifies they align with existing
documentation. It can fetch external documentation, compare implementations,
and suggest documentation updates when needed.
"""

import json
import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class DocumentationAlignmentValidator:
    def __init__(self):
        self.project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.'))
        self.alignment_cache = self.project_dir / '.claude' / 'cache' / 'doc_alignment.json'
        self.alignment_cache.parent.mkdir(parents=True, exist_ok=True)
        
        # Load cache if exists
        self.cache = self.load_cache()
        
    def load_cache(self) -> Dict:
        """Load alignment cache"""
        if self.alignment_cache.exists():
            try:
                with open(self.alignment_cache) as f:
                    return json.load(f)
            except:
                pass
        return {'functions': {}, 'files': {}, 'last_check': None}
    
    def save_cache(self):
        """Save alignment cache"""
        self.cache['last_check'] = datetime.now().isoformat()
        with open(self.alignment_cache, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def extract_function_from_code(self, code: str, language: str = 'python') -> List[Dict]:
        """Extract function definitions from code"""
        functions = []
        
        if language == 'python':
            # Match function definitions with optional type hints
            pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?:\s*(?:"""([^"]*)""")?'
            matches = re.findall(pattern, code, re.MULTILINE | re.DOTALL)
            
            for match in matches:
                name, params, return_type, docstring = match
                functions.append({
                    'name': name,
                    'params': self.parse_params(params),
                    'return_type': return_type.strip() if return_type else None,
                    'docstring': docstring.strip() if docstring else None
                })
        
        elif language in ['javascript', 'typescript']:
            # Match function declarations and arrow functions
            patterns = [
                r'function\s+(\w+)\s*\(([^)]*)\)',  # function declaration
                r'const\s+(\w+)\s*=\s*\(([^)]*)\)\s*=>'  # arrow function
            ]
            for pattern in patterns:
                matches = re.findall(pattern, code)
                for name, params in matches:
                    functions.append({
                        'name': name,
                        'params': self.parse_params(params),
                        'return_type': None,  # Would need more complex parsing for TS
                        'docstring': None
                    })
        
        return functions
    
    def parse_params(self, params_str: str) -> List[Dict]:
        """Parse parameter string into structured format"""
        if not params_str.strip():
            return []
        
        params = []
        for param in params_str.split(','):
            param = param.strip()
            if not param:
                continue
            
            # Handle Python type hints
            if ':' in param:
                name, type_hint = param.split(':', 1)
                name = name.strip()
                type_hint = type_hint.strip()
                # Remove default value if present
                if '=' in type_hint:
                    type_hint = type_hint.split('=')[0].strip()
            else:
                # Handle default values
                if '=' in param:
                    name = param.split('=')[0].strip()
                else:
                    name = param.strip()
                type_hint = None
            
            params.append({'name': name, 'type': type_hint})
        
        return params
    
    def find_existing_documentation(self, function_name: str, file_path: Optional[str] = None) -> Dict:
        """Find documentation for a function"""
        docs = {
            'inline': None,
            'readme': None,
            'external': None,
            'cached': None
        }
        
        # Check cache first
        cache_key = f"{file_path}:{function_name}" if file_path else function_name
        if cache_key in self.cache['functions']:
            docs['cached'] = self.cache['functions'][cache_key]
        
        # Search for inline documentation
        if file_path and Path(file_path).exists():
            content = Path(file_path).read_text()
            # Look for function with docstring
            pattern = rf'def\s+{re.escape(function_name)}\s*\([^)]*\)[^:]*:\s*"""([^"]*)"""'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                docs['inline'] = match.group(1).strip()
        
        # Search README files
        for readme in self.project_dir.glob('**/README*'):
            try:
                content = readme.read_text()
                if function_name in content:
                    # Extract section about this function
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if function_name in line:
                            # Get surrounding context
                            start = max(0, i - 2)
                            end = min(len(lines), i + 10)
                            docs['readme'] = '\n'.join(lines[start:end])
                            break
            except:
                continue
        
        return docs
    
    def check_alignment(self, function: Dict, docs: Dict) -> List[Dict]:
        """Check if function implementation aligns with documentation"""
        issues = []
        
        # Check if function has any documentation
        has_docs = any(docs.values())
        if not has_docs:
            issues.append({
                'type': 'missing_documentation',
                'severity': 'medium',
                'message': f"Function '{function['name']}' has no documentation",
                'suggestion': 'Add a docstring or update README'
            })
            return issues
        
        # Check parameter alignment
        if docs['inline']:
            doc_params = self.extract_params_from_docstring(docs['inline'])
            impl_params = function['params']
            
            # Check for parameter mismatches
            impl_param_names = {p['name'] for p in impl_params}
            doc_param_names = set(doc_params.keys())
            
            missing_in_docs = impl_param_names - doc_param_names
            missing_in_impl = doc_param_names - impl_param_names
            
            if missing_in_docs:
                issues.append({
                    'type': 'undocumented_parameters',
                    'severity': 'medium',
                    'message': f"Parameters {missing_in_docs} not documented",
                    'suggestion': 'Update docstring with missing parameters'
                })
            
            if missing_in_impl:
                issues.append({
                    'type': 'extra_documented_parameters',
                    'severity': 'high',
                    'message': f"Documented parameters {missing_in_impl} not in implementation",
                    'suggestion': 'Remove outdated parameter documentation or implement missing parameters'
                })
        
        # Check return type alignment
        if function['return_type'] and docs['inline']:
            if 'return' not in docs['inline'].lower() and 'yields' not in docs['inline'].lower():
                issues.append({
                    'type': 'missing_return_documentation',
                    'severity': 'low',
                    'message': 'Return type not documented',
                    'suggestion': 'Add Returns section to docstring'
                })
        
        return issues
    
    def extract_params_from_docstring(self, docstring: str) -> Dict[str, str]:
        """Extract parameters from docstring"""
        params = {}
        
        # Look for various parameter documentation styles
        patterns = [
            r':param\s+(\w+):\s*(.+)',  # Sphinx style
            r'@param\s+(\w+)\s+(.+)',   # JSDoc style  
            r'Args:\s*\n\s*(\w+)[:\s]+(.+)',  # Google style
            r'(\w+)\s*\([\w\s,]+\):\s*(.+)'  # NumPy style
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, docstring, re.MULTILINE)
            for param_name, param_desc in matches:
                params[param_name] = param_desc.strip()
        
        return params
    
    def suggest_documentation_update(self, function: Dict, issues: List[Dict]) -> str:
        """Generate suggested documentation"""
        lines = ['"""']
        
        # Add a basic description
        lines.append(f"{function['name'].replace('_', ' ').title()}")
        lines.append('')
        
        # Add parameters section
        if function['params']:
            lines.append('Args:')
            for param in function['params']:
                type_hint = f" ({param['type']})" if param['type'] else ""
                lines.append(f"    {param['name']}{type_hint}: Description needed")
            lines.append('')
        
        # Add return section if there's a return type
        if function['return_type']:
            lines.append('Returns:')
            lines.append(f"    {function['return_type']}: Description needed")
            lines.append('')
        
        lines.append('"""')
        
        return '\n'.join(lines)
    
    def validate_task_subagent(self, params: Dict) -> Dict:
        """Validate documentation for subagent tasks"""
        subagent_type = params.get('subagent_type', '')
        prompt = params.get('prompt', '')
        
        # Check if subagent has documentation
        subagent_docs = {
            'tdd-python-implementer': 'Test-Driven Development implementation',
            'security-analyzer': 'Security vulnerability analysis',
            'code-quality-analyzer': 'Code quality and clarity analysis',
            'web-docs-researcher': 'Web documentation research',
            'documentation-alignment-verifier': 'Documentation alignment verification'
        }
        
        if subagent_type not in subagent_docs:
            return {
                'has_issues': True,
                'message': f"Unknown subagent type: {subagent_type}",
                'suggestion': f"Available agents: {', '.join(subagent_docs.keys())}"
            }
        
        # Check if prompt aligns with agent purpose
        agent_purpose = subagent_docs[subagent_type]
        if agent_purpose.lower() not in prompt.lower():
            return {
                'has_issues': False,
                'warning': f"Task may not align with {subagent_type} purpose: {agent_purpose}"
            }
        
        return {'has_issues': False}
    
    def process(self, data: Dict) -> Dict:
        """Process hook data"""
        tool_name = data.get('tool_name', '')
        tool_input = data.get('tool_input', {})
        
        # Handle Task tool for subagent documentation
        if tool_name == 'Task':
            validation = self.validate_task_subagent(tool_input)
            if validation.get('has_issues'):
                return {
                    'decision': 'block',
                    'message': validation['message'],
                    'suggestion': validation.get('suggestion', '')
                }
            elif validation.get('warning'):
                print(f"⚠️ {validation['warning']}", file=sys.stderr)
        
        # Handle Write/Edit tools for code changes
        elif tool_name in ['Write', 'Edit', 'MultiEdit']:
            if tool_name == 'Write':
                content = tool_input.get('content', '')
                file_path = tool_input.get('file_path', '')
            elif tool_name == 'Edit':
                content = tool_input.get('new_string', '')
                file_path = tool_input.get('file_path', '')
            else:  # MultiEdit
                # Check all edits
                all_issues = []
                for edit in tool_input.get('edits', []):
                    content = edit.get('new_string', '')
                    if content:
                        functions = self.extract_function_from_code(content)
                        for func in functions:
                            docs = self.find_existing_documentation(func['name'])
                            issues = self.check_alignment(func, docs)
                            all_issues.extend(issues)
                
                if all_issues:
                    self.report_issues(all_issues)
                return {'decision': 'approve'}
            
            # Extract language from file extension
            ext = Path(file_path).suffix if file_path else ''
            language = 'python' if ext == '.py' else 'javascript' if ext in ['.js', '.ts'] else 'unknown'
            
            # Extract functions from new content
            functions = self.extract_function_from_code(content, language)
            
            all_issues = []
            for func in functions:
                # Find existing documentation
                docs = self.find_existing_documentation(func['name'], file_path)
                
                # Check alignment
                issues = self.check_alignment(func, docs)
                all_issues.extend(issues)
                
                # Cache the analysis
                cache_key = f"{file_path}:{func['name']}"
                self.cache['functions'][cache_key] = {
                    'params': func['params'],
                    'return_type': func['return_type'],
                    'has_docs': any(docs.values()),
                    'last_checked': datetime.now().isoformat()
                }
            
            self.save_cache()
            
            if all_issues:
                self.report_issues(all_issues)
                
                # Block if critical issues
                critical = [i for i in all_issues if i['severity'] == 'high']
                if critical:
                    return {
                        'decision': 'warn',
                        'message': 'Documentation alignment issues detected',
                        'issues': critical
                    }
        
        return {'decision': 'approve'}
    
    def report_issues(self, issues: List[Dict]):
        """Report alignment issues"""
        if not issues:
            return
        
        print("=" * 60, file=sys.stderr)
        print("📚 Documentation Alignment Check", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        
        # Group by severity
        by_severity = {'high': [], 'medium': [], 'low': []}
        for issue in issues:
            by_severity[issue['severity']].append(issue)
        
        if by_severity['high']:
            print("\n🔴 Critical Issues:", file=sys.stderr)
            for issue in by_severity['high']:
                print(f"   • {issue['message']}", file=sys.stderr)
                print(f"     → {issue['suggestion']}", file=sys.stderr)
        
        if by_severity['medium']:
            print("\n🟡 Important Issues:", file=sys.stderr)
            for issue in by_severity['medium']:
                print(f"   • {issue['message']}", file=sys.stderr)
                print(f"     → {issue['suggestion']}", file=sys.stderr)
        
        if by_severity['low']:
            print("\n🟢 Minor Issues:", file=sys.stderr)
            for issue in by_severity['low']:
                print(f"   • {issue['message']}", file=sys.stderr)
        
        print("\n💡 Run `/doc-align` to perform full alignment check", file=sys.stderr)
        print("=" * 60, file=sys.stderr)

def main():
    try:
        # Read hook data
        data = json.load(sys.stdin)
        
        # Process with validator
        validator = DocumentationAlignmentValidator()
        result = validator.process(data)
        
        # Return result
        if result['decision'] == 'block':
            print(json.dumps({
                'decision': 'block',
                'message': result.get('message', 'Documentation alignment failed'),
                'suggestion': result.get('suggestion', 'Update documentation first')
            }))
            sys.exit(2)
        elif result['decision'] == 'warn':
            print(json.dumps({
                'decision': 'approve',
                'warning': result.get('message', 'Documentation issues found')
            }))
            sys.exit(0)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"Documentation validator error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()