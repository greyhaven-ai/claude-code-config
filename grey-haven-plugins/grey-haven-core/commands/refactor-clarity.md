---
allowed-tools: Read, Write, MultiEdit, Bash, Grep, Task, TodoWrite
description: Refactor code for clarity using 10 proven refactoring rules
argument-hint: [file or directory to refactor]
---

Refactor for clarity: $ARGUMENTS

<ultrathink>
Clear code is a gift to future developers. Apply the 10 refactoring rules systematically. Clarity over cleverness.
</ultrathink>

<megaexpertise type="code-clarity-specialist">
The assistant should leverage the code-quality-analyzer subagent in clarity refactoring mode to systematically apply 10 proven refactoring patterns that enhance code comprehension.
</megaexpertise>

<context>
Refactoring target: $ARGUMENTS
Applying 10 clarity-enhancing refactoring rules
Hooks will validate safety of changes
</context>

<requirements>
- Apply 10 refactoring rules systematically
- Preserve all functionality
- Improve readability and maintainability
- Reduce cognitive complexity
- Ensure tests still pass
- Document each refactoring
</requirements>

<actions>
1. **Pre-Refactoring Analysis**:
   ```bash
   # Measure current complexity
   # For Python
   radon cc $ARGUMENTS -s -a 2>/dev/null || echo "Radon not installed"
   
   # For JavaScript
   bunx complexity-report $ARGUMENTS 2>/dev/null || echo "Complexity tool not available"
   
   # Count lines of code
   wc -l $ARGUMENTS
   ```

2. **Create Refactoring Plan with TodoWrite**:
   - List files to refactor
   - Identify which of the 10 rules apply
   - Set priority order

3. **Invoke Code Clarity Refactorer**:
   - Use code-quality-analyzer subagent (clarity refactoring mode)
   - Apply the 10 rules:
     1. Guard Clause - Flatten nested conditionals
     2. Delete Dead Code - Remove never-executed code
     3. Normalize Symmetries - Make similar things look similar
     4. New Interface, Old Implementation - Better APIs
     5. Reading Order - Logical flow for readers
     6. Cohesion Order - Group related code
     7. Move Declaration & Initialization Together
     8. Explaining Variable - Extract expressions
     9. Explaining Constant - Replace magic numbers
     10. Explicit Parameters - No hidden state

4. **Hook Integration Checkpoints**:
   - **complexity-analyzer hook**: Identifies high-complexity functions
   - **dead-code-detector hook**: Finds unused code
   - **test-runner hook**: Validates functionality preserved
   - **post-edit-validator hook**: Ensures standards met

5. **Incremental Refactoring Process**:
   ```
   For each applicable rule:
   
   1. IDENTIFY: Find code matching the pattern
   2. EXPLAIN: Document why this improves clarity
   3. REFACTOR: Apply the transformation
   4. VALIDATE: Run tests to ensure behavior unchanged
   5. MEASURE: Check complexity reduction
   ```

6. **Example Transformations**:
   
   **Guard Clause**:
   ```python
   # Before: Nested conditionals
   if user:
       if user.active:
           if user.has_permission:
               process()
   
   # After: Early returns
   if not user:
       return
   if not user.active:
       return  
   if not user.has_permission:
       return
   process()
   ```
   
   **Explaining Variable**:
   ```javascript
   // Before: Complex expression
   if (user.age > 18 && user.country === 'US' && user.verified) {
   
   // After: Self-documenting
   const isEligibleUSUser = user.age > 18 && 
                            user.country === 'US' && 
                            user.verified;
   if (isEligibleUSUser) {
   ```

7. **Post-Refactoring Validation**:
   ```bash
   # Run tests
   pytest tests/ -v  # Python
   bun test          # JavaScript
   
   # Check style/lint
   ruff check $ARGUMENTS  # Python
   eslint $ARGUMENTS     # JavaScript
   ```

8. **Refactoring Report**:
   ```markdown
   ## Clarity Refactoring Report
   
   ### Metrics Improvement
   - Cyclomatic Complexity: 15 → 8 (-53%)
   - Nesting Depth: 5 → 2 (-60%)
   - Lines of Code: 500 → 420 (-16%)
   - Functions: 10 → 15 (better separation)
   
   ### Rules Applied
   ✅ Guard Clause: 5 instances
   ✅ Dead Code Removal: 50 lines
   ✅ Explaining Variables: 8 created
   ✅ Explicit Parameters: 3 functions
   ✅ Cohesion Ordering: 2 modules reorganized
   
   ### Quality Improvements
   - Readability Score: +35%
   - Test Coverage: Maintained at 95%
   - Code Review Time: -40% (estimated)
   
   ### Files Modified
   - src/auth.py: Guard clauses, explaining variables
   - src/processor.js: Dead code removal, cohesion
   - lib/validator.ts: Explicit parameters
   ```

9. **Commit with Descriptive Message**:
   ```bash
   git add $ARGUMENTS
   git commit -m "refactor: Apply 10 clarity rules to $ARGUMENTS
   
   - Applied guard clauses to reduce nesting
   - Removed dead code (50 lines)
   - Extracted explaining variables for complex conditions
   - Reordered functions for better cohesion
   - All tests passing, functionality preserved"
   ```
</actions>

The assistant should systematically apply each refactoring rule, explaining the benefits and ensuring all changes preserve functionality while improving clarity.