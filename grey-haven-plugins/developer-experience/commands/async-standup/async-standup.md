---
name: async-standup
description: Generate automated async standup updates from Git commits, Linear issues, and calendar events for distributed teams working across time zones
---

# Async Standup Automation

Automatically generate comprehensive standup updates by analyzing your work activity across Git, Linear, and calendar events.

## What This Command Does

Generates async standup updates by:
- **Analyzing Git commits** - Extract accomplishments from commit history
- **Reviewing Linear activity** - Track issue progress and completions
- **Identifying blockers** - Surface impediments with context and impact
- **Planning next work** - Generate action items from Linear backlog
- **Tracking metrics** - Calculate productivity and velocity metrics

Perfect for distributed teams working across time zones where synchronous standups are impractical.

## When to Use This

- **Daily standup automation** - Generate update at end of day or start of next day
- **Before team sync** - Prepare status update for weekly team meetings
- **Sprint reviews** - Summarize sprint accomplishments
- **Manager check-ins** - Provide concise progress summary
- **Documentation** - Create work log for retrospectives

## Usage

```bash
/async-standup [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--timeframe` | Time period: `today`, `yesterday`, `this-week`, `last-week`, custom | `today` |
| `--format` | Output format: `slack`, `markdown`, `linear-comment`, `email` | `slack` |
| `--include-metrics` | Include velocity and productivity metrics | `true` |
| `--post-to` | Auto-post to: `slack`, `linear`, `none` | `none` |
| `--channel` | Slack channel for posting | `#standup` |
| `--linear-project` | Linear project ID for comment | auto-detect |
| `--timezone` | Your timezone for time formatting | auto-detect |

### Examples

```bash
# Generate today's standup
/async-standup

# Yesterday's standup with Slack posting
/async-standup --timeframe yesterday --post-to slack --channel "#standup"

# Weekly summary
/async-standup --timeframe this-week --format markdown

# Custom timeframe
/async-standup --timeframe "2025-01-15 to 2025-01-17"
```

## Data Sources

### 1. Git Commit Analysis
Analyzes commit history to extract accomplishments by:
- Parsing conventional commit messages (feat, fix, docs, refactor, chore)
- Extracting linked Linear issues from commit messages
- Calculating impact from file changes and line additions/deletions
- Categorizing by scope (authentication, payments, etc.)

### 2. Linear Integration
Tracks issue activity via Linear API:
- Issues moved to "In Progress"
- Issues completed (with story point totals)
- Issues blocked (with blocker details)
- Comments added and priority changes
- Subtask completion tracking

### 3. Blocker Detection
Automatically identifies blockers from:
- **Linear**: Issues with "blocked" label, no activity for > 48 hours, comments containing "blocked"/"waiting"
- **Git**: WIP commits with no follow-up, reverted commits, multiple failed CI runs
- **Code Analysis**: Failing tests, unresolved review comments, dependency update failures

**See [reference/data-sources.md](reference/data-sources.md)** for detailed extraction algorithms and examples.

## Output Formats

The command generates updates in 4 formats optimized for different platforms:

### Slack Format
Formatted with emojis, sections for Yesterday/Today/Blockers/Metrics, threaded replies for discussions.

### Markdown Format
Comprehensive format with detailed accomplishment descriptions, impact analysis, blocker classification, and metrics tables.

### Linear Comment Format
Concise format optimized for Linear project comments with key metrics and links.

### Email Format
Plain-text format suitable for email with clear sections and minimal formatting.

**See [examples/output-formats.md](examples/output-formats.md)** for complete format specifications and examples.

## Intelligent Features

### 1. Accomplishment Extraction
Automatically transforms commits into meaningful accomplishments:
- Detects commit type from conventional commits
- Extracts scope and description
- Calculates impact from code changes
- Correlates with Linear issues

### 2. Blocker Severity Classification
Classifies blockers by severity (critical, high, medium, low) based on:
- Labels and priority in Linear
- Impact on sprint goals or team members
- Customer-facing feature status
- Deadline proximity

### 3. Smart Work Planning
Generates "Today" section from:
- Current in-progress issues
- Next priority items from backlog
- Capacity calculation (6 hours of focused work)
- Automatic task allocation

### 4. Productivity Metrics
Tracks comprehensive productivity metrics:
- Commits, lines changed, PRs created/merged/reviewed
- Issues completed, story points, code coverage
- Build time, velocity, focus time

**See [reference/intelligent-features.md](reference/intelligent-features.md)** for implementation details and algorithms.

## Automation & Integration

### Slack Integration
Post updates directly to Slack channels with webhook integration and scheduled posting.

### Linear Integration
Add updates as comments on Linear projects with automatic linking.

### GitHub Actions Automation
Schedule daily standup generation at consistent times (e.g., 5 PM daily).

**See [reference/automation-integration.md](reference/automation-integration.md)** for complete integration setup and workflows.

## Configuration

Create `.claude/standup-config.json` to customize:
- User information (name, email, timezone, working hours)
- Integrations (Linear, Slack, GitHub)
- Metrics tracking preferences
- Default format and auto-posting

**See [reference/configuration.md](reference/configuration.md)** for complete configuration schema and examples.

## Best Practices

### 1. Consistent Timing
- Generate standup at same time each day (e.g., end of day)
- Post before next team's working hours start
- Use GitHub Actions for automation

### 2. Meaningful Commit Messages
- Use conventional commits (feat, fix, docs, etc.)
- Reference Linear issues in commits (#GH-123)
- Write descriptive commit messages

### 3. Blocker Documentation
- Add "blocked" label in Linear immediately
- Comment with specific needs and impact
- Suggest workarounds when possible

### 4. Metric Tracking
- Review metrics weekly for trends
- Celebrate improvements
- Address declining metrics proactively

### 5. Team Communication
- Be honest about blockers
- Highlight team collaboration
- Ask for help when needed

## Troubleshooting

Common issues and solutions:

**No commits detected**: Wrong Git author email or time range
**Linear issues not showing**: Linear API authentication or filter issues
**Metrics inaccurate**: Multiple Git repositories or incomplete data

**See [reference/troubleshooting.md](reference/troubleshooting.md)** for detailed troubleshooting steps.

## Related Commands

- `/linear:continue-work` - Get next task recommendation
- `/doc-coverage` - Check documentation progress
- `/quality-pipeline` - Review code quality metrics
- `/monitor-deployment` - Check production health

## Agent Coordination

This command works with:
- **onboarding-coordinator** - Uses standup data for progress tracking
- **tdd-orchestrator** - References test completion metrics
- **docs-architect** - Includes documentation updates
- **observability-engineer** - Incorporates production metrics

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete standup examples
  - [output-formats.md](examples/output-formats.md) - All 4 output format examples
  - [daily-standup-example.md](examples/daily-standup-example.md) - Complete daily standup
  - [weekly-summary-example.md](examples/weekly-summary-example.md) - Weekly summary format
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Technical references
  - [data-sources.md](reference/data-sources.md) - Git, Linear, and blocker detection algorithms
  - [intelligent-features.md](reference/intelligent-features.md) - Extraction and classification logic
  - [automation-integration.md](reference/automation-integration.md) - Slack, Linear, GitHub Actions setup
  - [configuration.md](reference/configuration.md) - Config schema and examples
  - [troubleshooting.md](reference/troubleshooting.md) - Common issues and solutions
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [github-actions-workflow.yaml](templates/github-actions-workflow.yaml) - Daily standup automation
  - [slack-bot-config.js](templates/slack-bot-config.js) - Slack bot configuration

---

**Pro Tip**: Set up GitHub Actions to auto-post your standup at 5 PM daily. Your distributed team can read updates asynchronously in their own timezone, and you never forget to share your progress.
