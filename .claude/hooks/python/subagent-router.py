#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

"""
Subagent Router Hook - Intelligent subagent suggestion based on user prompts

Analyzes user prompts and suggests appropriate subagents for Claude to invoke.
Runs on UserPromptSubmit to provide proactive subagent recommendations.
Note: Subagents are invoked by Claude via the Task tool, not directly by users.
"""

import sys
import json
import re
from typing import Dict, List, Optional, Tuple

class SubagentRouter:
    def __init__(self):
        self.subagent_patterns = {
            'tdd-python-implementer': {
                'keywords': ['tdd', 'test driven', 'test first', 'red green refactor', 'python test'],
                'patterns': [r'implement.*with tests?', r'write tests? first', r'using tdd']
            },
            'security-orchestrator': {
                'keywords': ['security', 'vulnerability', 'exploit', 'injection', 'xss', 'csrf', 'auth'],
                'patterns': [r'security (review|audit|check)', r'find vulnerabilities?', r'check.*security']
            },
            'code-clarity-refactorer': {
                'keywords': ['refactor', 'cleanup', 'readability', 'clarity', 'simplify', 'clean code'],
                'patterns': [r'refactor.*code', r'improve.*readability', r'clean.*up']
            },
            'git-diff-documentation-agent': {
                'keywords': ['document changes', 'git diff', 'what changed', 'commit docs'],
                'patterns': [r'document.*changes?', r'what.*changed', r'explain.*diff']
            },
            'bug-issue-creator': {
                'keywords': ['bug', 'issue', 'github issue', 'track bug', 'report problem'],
                'patterns': [r'create.*issue', r'file.*bug', r'track.*problem']
            },
            'web-docs-researcher': {
                'keywords': ['research', 'documentation', 'api docs', 'library docs', 'how to'],
                'patterns': [r'research.*(?:api|library|framework)', r'find.*documentation', r'how.*works?']
            },
            'tech-docs-maintainer': {
                'keywords': ['update docs', 'documentation', 'readme', 'api docs', 'maintain docs'],
                'patterns': [r'update.*docs?', r'maintain.*documentation', r'document.*api']
            },
            'prompt-engineer': {
                'keywords': ['prompt', 'improve prompt', 'better prompt', 'optimize prompt'],
                'patterns': [r'improve.*prompt', r'optimize.*prompt', r'better.*prompt']
            },
            'code-synthesis-analyzer': {
                'keywords': ['analyze implementation', 'check code', 'review changes', 'find issues'],
                'patterns': [r'analyze.*implementation', r'check.*code', r'review.*changes']
            },
            'multi-agent-synthesis-orchestrator': {
                'keywords': ['complex research', 'comprehensive analysis', 'multi-faceted', 'deep dive'],
                'patterns': [r'comprehensive.*analysis', r'deep.*dive', r'research.*complex']
            }
        }
        
    def analyze_prompt(self, prompt: str) -> List[Tuple[str, float]]:
        """Analyze prompt and return matching subagents with confidence scores"""
        prompt_lower = prompt.lower()
        matches = []
        
        for subagent, config in self.subagent_patterns.items():
            score = 0.0
            
            # Check keywords
            keyword_matches = sum(1 for kw in config['keywords'] if kw in prompt_lower)
            if keyword_matches:
                score += keyword_matches * 0.3
            
            # Check patterns
            pattern_matches = sum(1 for pattern in config['patterns'] 
                                if re.search(pattern, prompt_lower))
            if pattern_matches:
                score += pattern_matches * 0.5
            
            # Check exact subagent name mention
            if subagent.replace('-', ' ') in prompt_lower:
                score += 1.0
            
            if score > 0:
                matches.append((subagent, min(score, 1.0)))
        
        # Sort by confidence score
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def format_suggestion(self, subagent: str, confidence: float) -> str:
        """Format subagent suggestion for output"""
        confidence_level = "high" if confidence > 0.7 else "medium" if confidence > 0.4 else "low"
        emoji = "🎯" if confidence > 0.7 else "💡" if confidence > 0.4 else "🤔"
        
        return f"{emoji} Consider using the `{subagent}` subagent ({confidence_level} confidence: {confidence:.0%})"
    
    def process(self, data: Dict) -> Dict:
        """Process the hook event"""
        prompt = data.get('prompt', '')
        if not prompt:
            return {"decision": "allow"}
        
        matches = self.analyze_prompt(prompt)
        
        if not matches:
            return {"decision": "allow"}
        
        # Only suggest if confidence is reasonable
        suggestions = []
        for subagent, confidence in matches[:3]:  # Top 3 matches
            if confidence >= 0.3:
                suggestions.append(self.format_suggestion(subagent, confidence))
        
        if suggestions:
            suggestion_text = "\n".join(suggestions)
            enhanced_prompt = f"{prompt}\n\n---\n🤖 Subagent Router Suggestions:\n{suggestion_text}\n---"
            
            return {
                "decision": "allow",
                "output": enhanced_prompt,
                "hookSpecificOutput": {
                    "suggestedSubagents": [{"name": subagent, "confidence": conf} 
                                      for subagent, conf in matches[:3]]
                }
            }
        
        return {"decision": "allow"}

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Process the event
        router = SubagentRouter()
        result = router.process(input_data)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        error_response = {
            "decision": "allow",
            "error": f"Subagent router error: {str(e)}"
        }
        print(json.dumps(error_response))
        sys.exit(0)

if __name__ == "__main__":
    main()