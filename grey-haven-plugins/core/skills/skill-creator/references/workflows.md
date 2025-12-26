# Workflow Patterns

Patterns for structuring multi-step workflows in skills.

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. Give Claude an overview at the start:

```markdown
## Workflow Overview

Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

### Grey Haven Example: TDD Workflow

```markdown
## TDD Workflow

Implementing a feature with TDD:

1. **Write failing test** - Create test for expected behavior
2. **Verify test fails** - Run test, confirm red
3. **Write minimal code** - Implement just enough to pass
4. **Verify test passes** - Run test, confirm green
5. **Refactor** - Improve code while tests stay green
6. **Repeat** - Next test case
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
## Workflow Decision

1. Determine the modification type:

   **Creating new content?** → Follow "Creation Workflow" below
   **Editing existing content?** → Follow "Editing Workflow" below

2. **Creation Workflow:**
   - Step A
   - Step B
   - Step C

3. **Editing Workflow:**
   - Step X
   - Step Y
   - Step Z
```

### Grey Haven Example: Code Review Decision Tree

```markdown
## Code Review Workflow

1. Analyze the change type:

   **New feature?** → Focus on architecture, tests, documentation
   **Bug fix?** → Focus on root cause, regression tests, minimal change
   **Refactor?** → Focus on behavior preservation, test coverage
   **Performance?** → Focus on benchmarks, complexity analysis

2. For each type, apply specific checklist...
```

## Parallel Workflows

When multiple independent tasks can run simultaneously:

```markdown
## Parallel Execution

These tasks can run in parallel:

**Track 1: Frontend**
- Component implementation
- Styling
- Client-side tests

**Track 2: Backend**
- API endpoint
- Database queries
- Server-side tests

**Track 3: Integration**
- E2E tests
- Documentation

Merge results after all tracks complete.
```

## Checkpoint Patterns

For long-running or resumable workflows:

```markdown
## Checkpointed Workflow

### Checkpoint 1: Analysis Complete
- [ ] Requirements gathered
- [ ] Existing code reviewed
- [ ] Approach documented

### Checkpoint 2: Implementation Complete
- [ ] Core functionality implemented
- [ ] Unit tests passing
- [ ] Code reviewed

### Checkpoint 3: Integration Complete
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Ready for deployment
```

## Error Recovery Patterns

Handle failures gracefully:

```markdown
## Error Handling

If step fails:

1. **Transient error** (network, timeout):
   - Retry with exponential backoff
   - Max 3 retries

2. **Validation error** (bad input):
   - Log specific error
   - Request corrected input
   - Resume from failed step

3. **Fatal error** (unrecoverable):
   - Save progress to checkpoint
   - Report error with context
   - Exit gracefully
```

---

*Use these patterns to structure complex, multi-step processes in skills*
