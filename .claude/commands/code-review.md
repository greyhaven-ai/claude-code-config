---
allowed-tools: Read, Bash(git diff:*), Bash(git log:*), Task
description: Perform comprehensive code review on recent changes
argument-hint: [commit-range or file-paths]
---

Perform comprehensive code review: $ARGUMENTS

<ultrathink>
Code review is where quality meets collaboration. Look beyond syntax to architecture, beyond function to maintainability, beyond the present to the future.
</ultrathink>

<megaexpertise type="senior-code-reviewer">
The assistant should combine technical expertise with constructive feedback, identifying issues while acknowledging good practices and suggesting improvements with empathy.
</megaexpertise>

<context>
Review scope: $ARGUMENTS
Recent commits: !`git log --oneline -10`
Changed files: !`git diff --name-only HEAD~5..HEAD`
Current branch: !`git branch --show-current`
</context>

<requirements>
- Review functionality, quality, security, and performance
- Provide actionable feedback with examples
- Categorize findings by severity
- Acknowledge good practices
- Consider using code-quality-analyzer subagent
- Be constructive and educational
</requirements>

<actions>
1. Initial Assessment:
   - Understand the purpose and context of changes
   - Check against requirements/tickets if referenced
   - Review commit messages for clarity
   - Verify PR description completeness
   - Assess scope appropriateness

2. Functionality & Logic Review:
   ```bash
   # Get full diff context
   git diff $ARGUMENTS --unified=5
   ```
   - Verify code accomplishes intended purpose
   - Check edge case handling
   - Validate error handling completeness
   - Look for logic errors or bugs
   - Assess algorithm efficiency
   - Check for race conditions

3. Code Quality Analysis:
   - **Readability**: Is intent clear without extensive comments?
   - **Naming**: Are names descriptive and consistent?
   - **Complexity**: Can complex logic be simplified?
   - **DRY**: Is there unnecessary duplication?
   - **SOLID**: Are principles appropriately applied?
   - **Patterns**: Are design patterns used correctly?

4. Testing Verification:
   ```bash
   # Check test coverage for changed files
   pytest --cov=$ARGUMENTS --cov-report=term-missing
   ```
   - Adequate test coverage for new code
   - Tests are meaningful, not just coverage
   - Edge cases and error paths tested
   - Tests follow naming conventions
   - No flaky or brittle tests
   - Performance tests if applicable

5. Security Review:
   - No hardcoded credentials or secrets
   - Input validation present and complete
   - SQL injection prevention (parameterized queries)
   - XSS prevention (output encoding)
   - Authentication/authorization correct
   - Sensitive data properly handled
   - Dependencies checked for vulnerabilities

6. Performance Considerations:
   - Database queries optimized (N+1 prevention)
   - Appropriate caching implementation
   - Async operations handled correctly
   - Memory leaks prevented
   - Resource cleanup in place
   - Scalability considered

7. Documentation & Standards:
   - Code comments where necessary (why, not what)
   - API documentation updated
   - README updated if needed
   - Changelog entry added
   - Type hints/annotations present
   - Linting rules satisfied

8. Advanced Analysis with Subagents:
   - Use code-quality-analyzer for deep implementation review (synthesis mode)
   - Apply security-analyzer for security concerns (direct or orchestrated mode)
   - Consider code-quality-analyzer suggestions (clarity refactoring mode)

9. Constructive Feedback Format:
   ```markdown
   ## Code Review Summary
   
   ### 🎯 Overall Assessment
   [Brief summary of the changes and overall quality]
   
   ### ✅ Commendations
   - [Specific thing done well]
   - [Good practice observed]
   - [Clever solution appreciated]
   
   ### 🚨 Critical Issues (Must Fix)
   **Issue**: [Description]
   **Location**: `file.py:123`
   **Impact**: [Why this matters]
   **Suggestion**:
   \```python
   # Better approach
   \```
   
   ### ⚠️ Important Suggestions (Should Fix)
   [Similar format, less critical]
   
   ### 💡 Minor Improvements (Consider)
   [Nitpicks and preferences]
   
   ### 📚 Learning Opportunities
   [Educational points for growth]
   ```

10. Follow-up Actions:
    - Tag specific areas needing author attention
    - Suggest pairing on complex issues
    - Offer to clarify feedback if needed
    - Set expectations for resolution
</actions>

The assistant should balance thoroughness with empathy, providing feedback that improves both the code and the developer's skills.

Take a deep breath in, count 1... 2... 3... and breathe out. The assistant is now centered and ready to provide constructive code review.