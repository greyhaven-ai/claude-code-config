#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

"""
Subagent Orchestrator - Coordinate multi-subagent workflows

Orchestrates complex workflows by chaining subagents based on results and context.
Runs on SubagentStop to determine next subagents in workflow chains.
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class SubagentOrchestrator:
    def __init__(self):
        self.project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        self.workflow_state_file = Path(self.project_dir) / '.claude' / 'workflow-state.json'
        
        # Define subagent workflow chains
        self.workflow_chains = {
            'full-development-cycle': [
                'code-synthesis-analyzer',
                'tdd-python-implementer',
                'code-clarity-refactorer',
                'git-diff-documentation-agent',
                'tech-docs-maintainer'
            ],
            'security-audit-workflow': [
                'security-orchestrator',
                'bug-issue-creator',
                'tech-docs-maintainer'
            ],
            'documentation-workflow': [
                'git-diff-documentation-agent',
                'tech-docs-maintainer',
                'web-docs-researcher'
            ],
            'quality-improvement-workflow': [
                'code-synthesis-analyzer',
                'code-clarity-refactorer',
                'tdd-python-implementer'
            ]
        }
        
        # Define conditional chains based on subagent results
        self.conditional_chains = {
            'code-synthesis-analyzer': self.handle_analysis_results,
            'security-orchestrator': self.handle_security_results,
            'tdd-python-implementer': self.handle_tdd_results,
            'git-diff-documentation-agent': self.handle_documentation_results
        }
        
        # Subagent dependencies - which subagents should run after specific subagents
        self.subagent_dependencies = {
            'code-synthesis-analyzer': {
                'on_issues_found': ['code-clarity-refactorer', 'tdd-python-implementer'],
                'on_success': ['git-diff-documentation-agent']
            },
            'security-orchestrator': {
                'on_critical': ['bug-issue-creator'],
                'on_complete': ['tech-docs-maintainer']
            },
            'tdd-python-implementer': {
                'on_tests_added': ['code-clarity-refactorer'],
                'on_complete': ['git-diff-documentation-agent']
            },
            'code-clarity-refactorer': {
                'on_refactored': ['git-diff-documentation-agent', 'tech-docs-maintainer']
            }
        }
    
    def load_workflow_state(self) -> Dict:
        """Load current workflow state"""
        if self.workflow_state_file.exists():
            try:
                with open(self.workflow_state_file) as f:
                    return json.load(f)
            except:
                pass
        return {'active_workflows': [], 'completed_subagents': [], 'pending_subagents': []}
    
    def save_workflow_state(self, state: Dict):
        """Save workflow state"""
        self.workflow_state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.workflow_state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def handle_analysis_results(self, result: Dict) -> List[str]:
        """Determine next subagents based on analysis results"""
        next_subagents = []
        
        if result.get('issues_found'):
            issue_types = result.get('issue_types', [])
            
            if 'quality' in issue_types or 'complexity' in issue_types:
                next_subagents.append('code-clarity-refactorer')
            
            if 'missing_tests' in issue_types:
                next_subagents.append('tdd-python-implementer')
            
            if 'security' in issue_types:
                next_subagents.append('security-orchestrator')
        else:
            # No issues found, proceed to documentation
            next_subagents.append('git-diff-documentation-agent')
        
        return next_subagents
    
    def handle_security_results(self, result: Dict) -> List[str]:
        """Determine next agents based on security results"""
        next_agents = []
        
        findings = result.get('findings', [])
        critical_count = sum(1 for f in findings if f.get('severity') == 'critical')
        high_count = sum(1 for f in findings if f.get('severity') == 'high')
        
        if critical_count > 0:
            next_agents.append('bug-issue-creator')
        
        if critical_count > 0 or high_count > 0:
            next_agents.append('tech-docs-maintainer')
        
        if result.get('code_changes_suggested'):
            next_agents.append('code-clarity-refactorer')
        
        return next_agents
    
    def handle_tdd_results(self, result: Dict) -> List[str]:
        """Determine next agents based on TDD results"""
        next_agents = []
        
        if result.get('tests_written', 0) > 0:
            next_agents.append('code-clarity-refactorer')
        
        if result.get('implementation_complete'):
            next_agents.append('git-diff-documentation-agent')
        
        if result.get('coverage_increased'):
            next_agents.append('tech-docs-maintainer')
        
        return next_agents
    
    def handle_documentation_results(self, result: Dict) -> List[str]:
        """Determine next agents based on documentation results"""
        next_agents = []
        
        if result.get('documentation_gaps'):
            next_agents.append('tech-docs-maintainer')
        
        if result.get('api_changes'):
            next_agents.append('web-docs-researcher')
        
        return next_agents
    
    def detect_workflow_pattern(self, subagent_name: str, user_context: str = "") -> Optional[str]:
        """Detect which workflow pattern is being used"""
        # Check if subagent is part of a known workflow
        for workflow_name, subagents in self.workflow_chains.items():
            if subagent_name in subagents:
                # Check if this looks like the start of a workflow
                if subagent_name == subagents[0]:
                    return workflow_name
        
        # Check based on context keywords
        context_lower = user_context.lower()
        if 'security' in context_lower and 'audit' in context_lower:
            return 'security-audit-workflow'
        if 'document' in context_lower:
            return 'documentation-workflow'
        if 'quality' in context_lower or 'improve' in context_lower:
            return 'quality-improvement-workflow'
        if 'develop' in context_lower or 'implement' in context_lower:
            return 'full-development-cycle'
        
        return None
    
    def get_next_in_workflow(self, workflow: str, completed_subagent: str) -> Optional[str]:
        """Get next subagent in a workflow chain"""
        if workflow not in self.workflow_chains:
            return None
        
        subagents = self.workflow_chains[workflow]
        try:
            current_index = subagents.index(completed_subagent)
            if current_index < len(subagents) - 1:
                return subagents[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def format_suggestion(self, next_subagents: List[str], workflow: Optional[str] = None) -> str:
        """Format suggestion message for next subagents"""
        if not next_subagents:
            return ""
        
        lines = ["\n" + "="*50,
                "🔄 Workflow Orchestration",
                "="*50]
        
        if workflow:
            lines.append(f"📋 Active Workflow: {workflow.replace('-', ' ').title()}")
        
        lines.append("\n🎯 Suggested Next Steps:")
        
        for i, subagent in enumerate(next_subagents, 1):
            subagent_desc = self.get_subagent_description(subagent)
            lines.append(f"  {i}. `{subagent}` subagent - {subagent_desc}")
        
        lines.append("\n💡 Claude may invoke these subagents to continue your workflow.")
        lines.append("="*50)
        
        return "\n".join(lines)
    
    def get_subagent_description(self, subagent: str) -> str:
        """Get a brief description of what a subagent does"""
        descriptions = {
            'code-clarity-refactorer': "Improve code quality and readability",
            'tdd-python-implementer': "Add tests using TDD methodology",
            'git-diff-documentation-agent': "Document recent changes",
            'tech-docs-maintainer': "Update technical documentation",
            'security-orchestrator': "Perform security audit",
            'bug-issue-creator': "Create GitHub issues for bugs",
            'code-synthesis-analyzer': "Analyze implementation quality",
            'web-docs-researcher': "Research documentation and APIs"
        }
        return descriptions.get(subagent, "Specialized task execution")
    
    def process(self, data: Dict) -> Dict:
        """Process the SubagentStop event"""
        subagent_name = data.get('agentName')
        result = data.get('result', {})
        
        if not subagent_name:
            return {"decision": "approve"}
        
        # Load current workflow state
        state = self.load_workflow_state()
        
        # Mark subagent as completed
        if subagent_name not in state['completed_subagents']:
            state['completed_subagents'].append(subagent_name)
        
        # Determine next subagents based on conditional logic
        next_subagents = []
        
        # Check conditional chains
        if subagent_name in self.conditional_chains:
            handler = self.conditional_chains[subagent_name]
            conditional_next = handler(result)
            next_subagents.extend(conditional_next)
        
        # Check if part of an active workflow
        active_workflow = None
        for workflow in state.get('active_workflows', []):
            next_subagent = self.get_next_in_workflow(workflow, subagent_name)
            if next_subagent and next_subagent not in next_subagents:
                next_subagents.append(next_subagent)
                active_workflow = workflow
                break
        
        # If no active workflow, detect if we should start one
        if not active_workflow and not next_subagents:
            workflow = self.detect_workflow_pattern(subagent_name)
            if workflow:
                state['active_workflows'].append(workflow)
                next_subagent = self.get_next_in_workflow(workflow, subagent_name)
                if next_subagent:
                    next_subagents.append(next_subagent)
                    active_workflow = workflow
        
        # Update pending subagents
        for subagent in next_subagents:
            if subagent not in state['pending_subagents']:
                state['pending_subagents'].append(subagent)
        
        # Save state
        self.save_workflow_state(state)
        
        # Format response
        if next_subagents:
            suggestion = self.format_suggestion(next_subagents, active_workflow)
            
            return {
                "decision": "approve",
                "systemMessage": suggestion,
                "hookSpecificOutput": {
                    "completedSubagent": subagent_name,
                    "suggestedSubagents": next_subagents,
                    "activeWorkflow": active_workflow,
                    "workflowState": state
                }
            }
        
        # Check if workflow is complete
        if active_workflow:
            workflow_subagents = self.workflow_chains.get(active_workflow, [])
            if all(subagent in state['completed_subagents'] for subagent in workflow_subagents):
                completion_msg = f"\n✅ Workflow Complete: {active_workflow.replace('-', ' ').title()}\n" + \
                               f"   All {len(workflow_subagents)} subagents have been executed successfully."
                
                # Clear the completed workflow
                if active_workflow in state['active_workflows']:
                    state['active_workflows'].remove(active_workflow)
                self.save_workflow_state(state)
                
                return {
                    "decision": "approve",
                    "systemMessage": completion_msg
                }
        
        return {"decision": "approve"}

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Process the event
        orchestrator = SubagentOrchestrator()
        result = orchestrator.process(input_data)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        error_response = {
            "decision": "approve",
            "error": f"Orchestrator error: {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)

if __name__ == "__main__":
    main()