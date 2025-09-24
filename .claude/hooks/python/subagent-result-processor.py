#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

"""
Subagent Result Processor - Capture and process subagent outputs

Processes results from completed subagents and triggers appropriate follow-up actions.
Runs on SubagentStop to handle subagent completion events.
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

class SubagentResultProcessor:
    def __init__(self):
        self.project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        self.results_dir = Path(self.project_dir) / '.claude' / 'agent-results'
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Define follow-up actions for each subagent
        self.subagent_workflows = {
            'security-orchestrator': self.process_security_results,
            'tdd-python-implementer': self.process_tdd_results,
            'code-synthesis-analyzer': self.process_analysis_results,
            'git-diff-documentation-agent': self.process_documentation_results,
            'bug-issue-creator': self.process_issue_results,
            'code-clarity-refactorer': self.process_refactor_results
        }
    
    def save_subagent_result(self, subagent_name: str, result: Dict) -> Path:
        """Save subagent result for audit and future reference"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{subagent_name}_{timestamp}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'subagent': subagent_name,
                'timestamp': timestamp,
                'result': result
            }, f, indent=2)
        
        return filepath
    
    def process_security_results(self, result: Dict) -> Dict:
        """Process security orchestrator results"""
        suggestions = []
        
        # Check for critical findings
        if 'findings' in result:
            critical_count = sum(1 for f in result.get('findings', []) 
                               if f.get('severity') == 'critical')
            if critical_count > 0:
                suggestions.append(f"⚠️ {critical_count} critical security issues found!")
                suggestions.append("Consider using `/bug-issue-creator` to track these issues")
        
        # Suggest documentation update
        if result.get('success'):
            suggestions.append("📝 Update security documentation with `/tech-docs-maintainer`")
        
        return {
            'follow_up_actions': suggestions,
            'requires_immediate_attention': critical_count > 0 if 'findings' in result else False
        }
    
    def process_tdd_results(self, result: Dict) -> Dict:
        """Process TDD implementer results"""
        suggestions = []
        
        # Check test coverage
        if 'tests_written' in result:
            test_count = result.get('tests_written', 0)
            if test_count > 0:
                suggestions.append(f"✅ {test_count} tests written successfully")
                suggestions.append("Consider running `/code-clarity-refactorer` to improve code quality")
        
        # Check for incomplete implementations
        if result.get('incomplete_features'):
            suggestions.append("📋 Some features remain incomplete - continue with TDD cycle")
        
        return {
            'follow_up_actions': suggestions,
            'test_metrics': {
                'tests_added': result.get('tests_written', 0),
                'coverage_delta': result.get('coverage_change', 'unknown')
            }
        }
    
    def process_analysis_results(self, result: Dict) -> Dict:
        """Process code synthesis analyzer results"""
        suggestions = []
        
        if result.get('issues_found'):
            suggestions.append("🔍 Issues detected in implementation")
            suggestions.append("Run `/code-clarity-refactorer` to address code quality issues")
            
            if result.get('missing_tests'):
                suggestions.append("Use `/tdd-python-implementer` to add missing tests")
        
        return {
            'follow_up_actions': suggestions,
            'quality_metrics': result.get('metrics', {})
        }
    
    def process_documentation_results(self, result: Dict) -> Dict:
        """Process documentation agent results"""
        suggestions = []
        
        if result.get('documentation_created'):
            suggestions.append("📚 Documentation updated successfully")
            suggestions.append("Review with `/tech-docs-maintainer` for consistency")
        
        return {
            'follow_up_actions': suggestions,
            'docs_updated': result.get('files_documented', [])
        }
    
    def process_issue_results(self, result: Dict) -> Dict:
        """Process bug issue creator results"""
        suggestions = []
        
        if result.get('issue_created'):
            issue_url = result.get('issue_url')
            if issue_url:
                suggestions.append(f"🐛 Issue created: {issue_url}")
                suggestions.append("Track progress in your issue tracker")
        
        return {
            'follow_up_actions': suggestions,
            'issue_tracking': {
                'created': result.get('issue_created', False),
                'url': result.get('issue_url')
            }
        }
    
    def process_refactor_results(self, result: Dict) -> Dict:
        """Process refactoring results"""
        suggestions = []
        
        if result.get('refactoring_complete'):
            suggestions.append("♻️ Refactoring completed successfully")
            suggestions.append("Run tests to ensure no regressions")
            suggestions.append("Update documentation with `/git-diff-documentation-agent`")
        
        return {
            'follow_up_actions': suggestions,
            'refactor_metrics': result.get('metrics', {})
        }
    
    def generate_summary(self, subagent_name: str, processing_result: Dict) -> str:
        """Generate a summary message for the user"""
        lines = [f"\n{'='*50}",
                f"🤖 Subagent Completed: {subagent_name}",
                f"{'='*50}\n"]
        
        # Add follow-up actions
        if processing_result.get('follow_up_actions'):
            lines.append("📋 Suggested Follow-up Actions:")
            for action in processing_result['follow_up_actions']:
                lines.append(f"  • {action}")
        
        # Add metrics if available
        for key, value in processing_result.items():
            if key not in ['follow_up_actions'] and isinstance(value, dict):
                lines.append(f"\n📊 {key.replace('_', ' ').title()}:")
                for k, v in value.items():
                    lines.append(f"  • {k}: {v}")
        
        lines.append(f"\n{'='*50}")
        return "\n".join(lines)
    
    def process(self, data: Dict) -> Dict:
        """Process the SubagentStop event"""
        subagent_name = data.get('agentName', 'unknown')
        result = data.get('result', {})
        
        # Save the result
        result_file = self.save_subagent_result(subagent_name, result)
        
        # Process based on subagent type
        processor = self.subagent_workflows.get(subagent_name)
        if processor:
            processing_result = processor(result)
        else:
            processing_result = {
                'follow_up_actions': [
                    f"Subagent {subagent_name} completed",
                    "Results saved for review"
                ]
            }
        
        # Generate summary
        summary = self.generate_summary(subagent_name, processing_result)
        
        # Check if immediate attention needed
        if processing_result.get('requires_immediate_attention'):
            return {
                "decision": "block",
                "reason": summary + "\n\n⚠️ IMMEDIATE ATTENTION REQUIRED"
            }
        
        return {
            "decision": "approve",
            "systemMessage": summary,
            "hookSpecificOutput": {
                "subagent": subagent_name,
                "resultFile": str(result_file),
                "processingResult": processing_result
            }
        }

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Process the event
        processor = SubagentResultProcessor()
        result = processor.process(input_data)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        error_response = {
            "decision": "approve",
            "error": f"Subagent result processor error: {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)

if __name__ == "__main__":
    main()