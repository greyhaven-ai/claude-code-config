---
allowed-tools: Read, Write, Task, Bash(git diff:*), Bash(git log:*), Grep, Glob, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape, mcp__context7__get-library-docs, mcp__context7__resolve-library-id
description: Check and verify alignment between implementation and documentation
argument-hint: [target: function/file/component or leave empty for full scan]
---
Check documentation alignment for: $ARGUMENTS
<ultrathink>
Documentation is the promise we make; implementation is how we keep it. When they diverge, confusion reigns. Alignment brings clarity, trust, and maintainability.
</ultrathink>
<megaexpertise type="documentation-alignment-specialist">
The assistant should meticulously compare implementation against all available documentation sources, identifying discrepancies, missing documentation, and outdated information while suggesting concrete fixes.
</megaexpertise>
<context>
Target scope: $ARGUMENTS
Project directory: !`pwd`
Recent changes: !`git log --oneline -5`
Modified files: !`git diff --name-only HEAD~3..HEAD`
Documentation files: !`find . -name "*.md" -o -name "*.rst" | head -20`
</context>
<requirements>
- Verify implementation matches documented behavior
- Check function signatures against documentation
- Validate API contracts and interfaces
- Identify undocumented features
- Find outdated documentation
- Suggest documentation improvements
- Use specialized agents for deep analysis
</requirements>
<actions>
1. Scope Identification:
 ```bash
 # Determine what we're checking
 if [ -z "$ARGUMENTS" ]; then
 echo "Full codebase scan"
 elif [ -f "$ARGUMENTS" ]; then
 echo "File: $ARGUMENTS"
 elif [ -d "$ARGUMENTS" ]; then
 echo "Component: $ARGUMENTS"
 else
 echo "Function/Class: $ARGUMENTS"
 fi
 ```
2. Documentation Discovery:
 - Search for inline documentation (docstrings, comments)
 - Find README files and markdown docs
 - Check for API documentation
 - Look for external documentation references
 - Search library documentation if using frameworks
 For external libraries:
 ```
 # Use Context7 for library docs
 - Resolve library ID for any frameworks/libraries
 - Fetch relevant documentation sections
 ```
3. Implementation Analysis:
 - Extract function signatures
 - Identify public APIs
 - Map dependencies and imports
 - Catalog parameters and return types
 - Note error handling patterns
 - Record configuration options
4. Documentation Extraction:
 ```python
 # Parse documentation from various sources
 - README.md sections
 - Inline docstrings
 - Type hints
 - JSDoc/PyDoc comments
 - External wiki/docs
 - OpenAPI/Swagger specs
 ```
5. Alignment Verification Matrix:
 | Aspect | Documentation | Implementation | Status |
 |--------|--------------|----------------|--------|
 | Function Signature | [OK] | [OK] | SUCCESS: Aligned |
 | Parameters | Listed | Match | SUCCESS: Aligned |
 | Return Type | Specified | Verified | SUCCESS: Aligned |
 | Error Handling | Documented | Implemented | WARNING: Partial |
 | Examples | Provided | Tested | ERROR: Missing |
6. Deep Analysis with Agents:
 - **documentation-alignment-verifier**: Primary agent for alignment checking
 - **web-docs-researcher**: Find latest documentation for libraries/frameworks
 - **code-quality-analyzer**: Analyze implementation patterns
 - **multi-agent-synthesis-orchestrator**: Complex alignment investigations
 Trigger the main agent:
 ```
 Task: documentation-alignment-verifier
 Prompt: "Check documentation alignment for $ARGUMENTS and generate fixes for any misalignments found"
 ```
7. Issue Categorization:
 ### [CRITICAL] Critical Misalignments
 - **Incorrect Signatures**: Function parameters don't match docs
 - **Wrong Behavior**: Implementation differs from specification
 - **Missing Error Handling**: Documented errors not handled
 - **Security Issues**: Security requirements not implemented
 ### [WARNING] Documentation Gaps
 - **Undocumented Functions**: Public APIs without docs
 - **Missing Parameters**: Docs incomplete
 - **No Examples**: Usage unclear
 - **Outdated Information**: Docs reference old behavior
 ### [OK] Enhancement Opportunities
 - **Type Hints**: Could add typing information
 - **Better Examples**: More comprehensive samples
 - **Edge Cases**: Document limitations
 - **Performance Notes**: Add complexity information
8. Automated Fix Generation:
 ```python
 # For each issue found:
 if issue.type == "missing_docstring":
 generate_docstring(function)
 elif issue.type == "parameter_mismatch":
 update_documentation(correct_params)
 elif issue.type == "outdated_example":
 create_updated_example()
 ```
9. Report Generation:
 ```markdown
 # Documentation Alignment Report
 ## Summary
 - Alignment Score: X/100
 - Files Checked: N
 - Issues Found: M
 ## Critical Issues
 ### Function: `process_data()`
 **File**: src/processor.py:45
 **Issue**: Parameter 'timeout' documented but not implemented
 **Fix**:
 \```python
 def process_data(data, timeout=30): # Add timeout parameter
 \```
 ## Documentation Updates Needed
 - [ ] Update README with new API endpoints
 - [ ] Add docstrings to utility functions
 - [ ] Fix examples in tutorial.md
 ## Suggested Improvements
 1. Add type hints to all public functions
 2. Include error handling examples
 3. Document performance characteristics
 ```
10. Fix Implementation:
 - Generate pull request with documentation updates
 - Create docstrings for undocumented code
 - Update examples to match current API
 - Add missing parameter descriptions
 - Correct type information
11. Validation Loop:
 ```bash
 # After fixes, re-run alignment check
 ./check-doc-alignment.py $ARGUMENTS --validate
 ```
12. Continuous Monitoring Setup:
 - Create pre-commit hook for doc checks
 - Set up CI pipeline for alignment validation
 - Generate alignment metrics dashboard
 - Track documentation coverage over time
</actions>
<output-format>
The assistant should provide:
1. Alignment score and summary statistics
2. Detailed issue list with severity levels
3. Specific fixes for each misalignment
4. Generated documentation updates
5. Code snippets for implementation fixes
6. Recommendations for maintaining alignment
</output-format>
Take a deep breath and systematically verify that the implementation fulfills every documented promise.