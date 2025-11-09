# TDD Workflow Checklist

Step-by-step checklist for Test-Driven Development workflow.

## Before Starting

- [ ] Understand the requirement clearly
- [ ] Break down requirement into small testable behaviors
- [ ] Set up test file (copy from [test-file-template.md](test-file-template.md))
- [ ] Ensure test environment is ready (`bun test --watch`)

---

## ❌ RED Phase: Write Failing Test

### 1. Write Test

- [ ] Write test for **one** specific behavior
- [ ] Use descriptive test name (what it should do)
- [ ] Follow Arrange-Act-Assert pattern
- [ ] Keep test focused and simple

### 2. Run Test

- [ ] Run test: `bun test path/to/test.ts`
- [ ] Verify test **fails** with expected error
- [ ] Test fails for the right reason (not syntax error)

### 3. Review Test

- [ ] Test is readable
- [ ] Test covers single behavior
- [ ] Test uses appropriate assertions
- [ ] Test name clearly describes behavior

**Example**:
```typescript
it('displays user name', () => {
  render(<UserCard user={mockUser} />);
  expect(screen.getByText('Alice')).toBeInTheDocument();
});
// ❌ FAIL: Component doesn't exist
```

---

## ✅ GREEN Phase: Write Minimum Code

### 1. Implement

- [ ] Write **simplest** code to make test pass
- [ ] Don't add extra features
- [ ] Don't worry about code quality yet
- [ ] Hardcoding is OK if it passes the test

### 2. Run Test

- [ ] Run test again
- [ ] Verify test **passes**
- [ ] All previous tests still pass

### 3. Review Implementation

- [ ] Code makes the test pass
- [ ] No unnecessary complexity
- [ ] Ready for refactoring

**Example**:
```typescript
export function UserCard({ user }) {
  return <div>{user.name}</div>;
}
// ✅ PASS: Test now passes
```

---

## 🔄 REFACTOR Phase: Improve Code

### 1. Identify Improvements

- [ ] Code duplication
- [ ] Unclear names
- [ ] Long functions
- [ ] Complex logic
- [ ] Missing types

### 2. Refactor

- [ ] Make one small improvement
- [ ] Run tests after each change
- [ ] Ensure all tests still pass
- [ ] Continue until satisfied

### 3. Final Check

- [ ] All tests pass
- [ ] Code is more readable
- [ ] No duplication
- [ ] Good naming
- [ ] Proper structure

**Example**:
```typescript
interface User {
  name: string;
  email: string;
}

interface UserCardProps {
  user: User;
}

export function UserCard({ user }: UserCardProps) {
  return (
    <div className="user-card">
      <h2>{user.name}</h2>
    </div>
  );
}
// ✅ PASS: Tests still pass, code improved
```

---

## 🔄 REPEAT: Next Feature

- [ ] Write next failing test
- [ ] Make it pass
- [ ] Refactor
- [ ] Continue until feature complete

---

## After Each Cycle

### Code Quality

- [ ] All tests pass
- [ ] Code follows style guide
- [ ] No linting errors
- [ ] Types are correct
- [ ] No console warnings

### Test Quality

- [ ] Tests are fast (< 100ms each)
- [ ] Tests are independent
- [ ] Tests are readable
- [ ] Tests cover edge cases
- [ ] Good test coverage (aim for 80%+)

---

## Before Committing

### Pre-Commit Checklist

- [ ] All tests pass: `bun test`
- [ ] Linting passes: `bun run lint`
- [ ] Type checking passes: `bun run type-check`
- [ ] Coverage meets threshold: `bun test --coverage`
- [ ] No console.log() statements
- [ ] No commented code

### Git Commit

- [ ] Stage files: `git add .`
- [ ] Commit with message: `git commit -m "test: add UserCard component"`
- [ ] Push: `git push`

---

## Common Mistakes to Avoid

❌ **Don't**:
- Skip the RED phase (write code before test)
- Write multiple tests at once
- Write too much production code
- Skip refactoring
- Test implementation details
- Have flaky tests
- Have slow tests

✅ **Do**:
- Follow red-green-refactor strictly
- One test at a time
- Write minimum code to pass
- Refactor regularly
- Test behavior
- Keep tests fast and deterministic
- Run tests frequently

---

## Quick Reference

| Phase | Action | Duration |
|-------|--------|----------|
| ❌ RED | Write failing test | 1-2 min |
| ✅ GREEN | Make test pass | 1-5 min |
| 🔄 REFACTOR | Improve code | 2-10 min |
| 🔄 REPEAT | Next feature | Continue |

**Total per cycle**: 5-15 minutes

---

## Example Full Cycle

```
1. ❌ RED: Write test for "displays user email"
   → Test fails

2. ✅ GREEN: Add {user.email} to component
   → Test passes

3. 🔄 REFACTOR: Extract email display to separate element
   → Tests still pass

4. 🔄 REPEAT: Write test for "displays user role"
   → Continue...
```

---

**Pro Tip**: Print this checklist and keep it visible while coding. Check off items as you go!

**Checklist Version**: 1.0
