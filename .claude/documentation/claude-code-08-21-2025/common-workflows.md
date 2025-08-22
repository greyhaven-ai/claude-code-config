# Common Workflows

Each task in this document includes clear instructions, example commands, and best practices to help you get the most from Claude Code.

## Understand new codebases

### Get a quick codebase overview

1. Navigate to the project root directory: `cd /path/to/project`
2. Start Claude Code: `claude`
3. Ask for a high-level overview: `> give me an overview of this codebase`
4. Dive deeper into specific components:
   - `> explain the main architecture patterns used here`
   - `> what are the key data models?`
   - `> how is authentication handled?`

### Find relevant code

1. Ask Claude to find relevant files: `> find the files that handle user authentication`
2. Get context on how components interact: `> how do these authentication files work together?`
3. Understand the execution flow: `> trace the login process from front-end to database`

## Fix bugs efficiently

1. Share the error with Claude: `> I'm seeing an error when I run npm test`
2. Ask for fix recommendations: `> suggest a few ways to fix the @ts-ignore in user.ts`
3. Apply the fix: `> update user.ts to add the null check you suggested`

## Refactor code

1. Identify legacy code: `> find deprecated API usage in our codebase`
2. Get refactoring recommendations: `> suggest how to refactor utils.js to use modern JavaScript features`
3. Apply changes safely: `> refactor utils.js to use ES2024 features while maintaining the same behavior`
4. Verify the refactoring: `> run tests for the refactored code`

## Work with tests

1. Identify untested code: `> find functions in NotificationsService.swift that are not covered by tests`
2. Generate test scaffolding: `> add tests for the notification service`
3. Add meaningful test cases: `> add test cases for edge conditions in the notification service`
4. Run and verify tests: `> run the new tests and fix any failures`

## Create pull requests

1. Summarize your changes: `> summarize the changes I've made to the authentication module`
2. Generate a PR: `> create a pr`
3. Review and refine: `> enhance the PR description with more context about the security improvements`
4. Add testing details: `> add information about how these changes were tested`

## Work with images

You can work with images in three ways:
1. Drag and drop an image into the Claude Code window
2. Copy an image and paste it into the CLI with Ctrl+V (not Cmd+V)
3. Provide an image path: "Analyze this image: /path/to/your/image.png"

Ask Claude to:
- Analyze images: `> What does this image show?`
- Generate code from designs: `> Generate CSS to match this design mockup`
- Debug with screenshots: `> Here's a screenshot of the error. What's causing it?`

## Reference files and directories

Use @ to quickly include files or directories:
- Reference a single file: `> Explain the logic in @src/utils/auth.js`
- Reference a directory: `> What's the structure of @src/components?`
- Reference MCP resources: `> Show me the data from @github:repos/owner/repo/issues`

## Use extended thinking

For complex tasks requiring deep reasoning:

1. Provide context and ask Claude to think:
   ```
   > I need to implement a new authentication system using OAuth2 for our API. 
   > Think deeply about the best approach for implementing this in our codebase.
   ```

2. Refine with follow-up prompts:
   - `> think about potential security vulnerabilities in this approach`
   - `> think harder about edge cases we should handle`

Extended thinking is most valuable for:
- Planning complex architectural changes
- Debugging intricate issues
- Creating implementation plans for new features
- Understanding complex codebases
- Evaluating tradeoffs between different approaches

## Resume previous conversations

Claude Code provides two options for resuming conversations:

- **Continue most recent**: `claude --continue`
- **Show conversation picker**: `claude --resume`

Examples:
```bash
# Continue most recent conversation
claude --continue

# Continue with specific prompt
claude --continue --print "Show me our progress"

# Show conversation picker
claude --resume
```

## Run parallel sessions with Git worktrees

Work on multiple tasks simultaneously with complete code isolation:

1. Create a new worktree:
   ```bash
   git worktree add ../project-feature-a -b feature-a
   ```

2. Run Claude Code in each worktree:
   ```bash
   cd ../project-feature-a
   claude
   ```

3. Manage worktrees:
   ```bash
   # List all worktrees
   git worktree list
   
   # Remove a worktree when done
   git worktree remove ../project-feature-a
   ```

## Use Claude as a Unix-style utility

### Add Claude to your verification process

```json
// package.json
{
    "scripts": {
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos.'"
    }
}
```

### Pipe in, pipe out

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

### Control output format

- Text format (default): `claude -p 'summarize this data' --output-format text`
- JSON format: `claude -p 'analyze this code' --output-format json`
- Streaming JSON: `claude -p 'parse this log' --output-format stream-json`

## Create custom slash commands

### Project-specific commands

1. Create commands directory: `mkdir -p .claude/commands`
2. Create command file: `echo "Analyze performance:" > .claude/commands/optimize.md`
3. Use in Claude Code: `> /optimize`

### Commands with arguments

Create flexible commands with `$ARGUMENTS`:
```bash
echo 'Find and fix issue #$ARGUMENTS' > .claude/commands/fix-issue.md
```

Use with: `> /fix-issue 123`

### Personal slash commands

1. Create personal commands: `mkdir -p ~/.claude/commands`
2. Add command: `echo "Review for security:" > ~/.claude/commands/security-review.md`
3. Use across all projects: `> /security-review`

## Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features:

- `> can Claude Code create pull requests?`
- `> how does Claude Code handle permissions?`
- `> what slash commands are available?`
- `> how do I use MCP with Claude Code?`
- `> what are the limitations of Claude Code?`