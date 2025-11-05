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
**Generate today's standup:**
```bash
/async-standup
```
**Yesterday's standup with Slack posting:**
```bash
/async-standup --timeframe yesterday --post-to slack --channel "#standup"
```
**Weekly summary:**
```bash
/async-standup --timeframe this-week --format markdown
```
**Custom timeframe:**
```bash
/async-standup --timeframe "2025-01-15 to 2025-01-17"
```
## Data Sources
### 1. Git Commit Analysis
Analyzes commit history to extract accomplishments:
```bash
# Get commits for timeframe
git log --since="today 00:00" --until="now" --author="$(git config user.email)"
# Parse commit messages
# - Feature additions
# - Bug fixes
# - Refactoring
# - Documentation updates
```
**Commit Message Parsing:**
```
feat: Add user authentication endpoints
fix: Resolve race condition in order processing
refactor: Simplify payment validation logic
docs: Update API documentation for v2 endpoints
chore: Update dependencies for security patches
```
**Extracted Accomplishments:**
- SUCCESS: Added user authentication endpoints
- Fixed race condition in order processing
- Simplified payment validation logic
-  Updated API documentation for v2
- Updated dependencies for security
### 2. Linear Integration
Tracks issue activity via Linear API:
```typescript
// Query Linear for user's activity
const issues = await linearClient.issues({
 filter: {
 assignee: { email: { eq: userEmail } },
 updatedAt: { gte: startOfDay }
 }
});
// Categorize by status changes
const completed = issues.filter(i => i.completedAt >= startOfDay);
const inProgress = issues.filter(i => i.state.type === 'started');
const blocked = issues.filter(i => labels.includes('blocked'));
```
**Activity Tracked:**
- Issues moved to "In Progress"
- Issues completed
- Issues blocked
- Comments added
- Priority changes
- Subtask completion
### 3. Blocker Detection
Automatically identifies blockers:
**From Linear:**
- Issues with "blocked" label
- Issues with no activity for > 48 hours
- Issues with comments containing "blocked", "waiting", "need"
**From Git:**
- WIP commits with no follow-up
- Reverted commits
- Multiple failed CI runs
**From Code Analysis:**
- Failing tests (from CI status)
- Unresolved code review comments
- Dependency update failures
## Output Formats
### Slack Format
```markdown
:wave: **Async Standup for <date>**
**:trophy: Yesterday**
• SUCCESS: Completed `GH-123`: User authentication API endpoints
• Fixed race condition in order processing affecting checkout
•  Updated API documentation for v2 endpoints
• Refactored payment validation (reduced complexity by 40%)
**:construction: Today**
• `GH-145`: Implement payment webhook integration
• `GH-146`: Add rate limiting to authentication endpoints
• Code review for PR #234
**:rotating_light: Blockers**
• `GH-144`: Waiting on PlanetScale schema approval (needed for webhooks)
 - **Impact**: Blocks webhook implementation
 - **Need**: Database team review by EOD
 - **Alternative**: Can proceed with mock data for testing
**:chart_with_upward_trend: Metrics**
• Commits: 8
• PRs merged: 2
• Issues completed: 2
• Code review: 3 PRs reviewed
• Velocity: 8 story points completed
```
### Markdown Format
```markdown
# Async Standup - January 17, 2025
## Yesterday
### Completed
- SUCCESS: **GH-123**: User authentication API endpoints
 - Added JWT token generation
 - Implemented refresh token rotation
 - Added rate limiting (100 req/min)
- SUCCESS: **GH-135**: Fixed race condition in order processing
 - Root cause: Concurrent updates to order status
 - Solution: Added distributed lock with Redis
 - Impact: Eliminated duplicate charges
### In Progress
-  **GH-140**: Payment integration refactoring
 - Completed: Stripe webhook handler
 - Remaining: PayPal integration, testing
 - ETA: Tomorrow EOD
## Today
### Planned Work
1. **GH-145**: Implement payment webhook integration (4 SP)
 - Design event schema
 - Implement handlers for payment.succeeded, payment.failed
 - Add retry logic for failed webhooks
2. **GH-146**: Add rate limiting to auth endpoints (2 SP)
 - Use Cloudflare Workers rate limiting
 - Configure per-IP and per-user limits
 - Add monitoring and alerts
3. Code review for PR #234 (teammate's work)
### Focus Areas
- Payment system reliability
- Security hardening
- Team collaboration
## Blockers
### Active Blockers
**GH-144: Payment webhook persistence**
- **Status**: Waiting on database team
- **Blocker**: PlanetScale schema migration needs approval
- **Impact**: Blocks webhook implementation (HIGH priority)
- **Needed**: Schema review by database team
- **Timeline**: Needed by EOD to stay on schedule
- **Workaround**: Can develop with mock data, but won't be production-ready
### Potential Blockers
- Dependency update (Hono v4) may require refactoring
- Waiting on design feedback for checkout UI
## Metrics
| Metric | Value | Change |
|--------|-------|--------|
| Commits | 8 | +2 from yesterday |
| Lines Changed | +487 / -123 | |
| PRs Created | 2 | |
| PRs Merged | 2 | |
| PRs Reviewed | 3 | |
| Issues Completed | 2 (8 SP) | ↑ |
| Code Coverage | 87.3% | +1.2% |
| Build Time | 2m 34s | -12s |
## Notes
- Pair programming session with @teammate on payment integration was very productive
- Discovered optimization opportunity in order query (reduced latency from 450ms to 80ms)
- Need to schedule design sync for new checkout flow next week
```
### Linear Comment Format
```markdown
## Daily Update - Jan 17, 2025
**Completed Today**
• Implemented JWT authentication with refresh tokens
• Fixed critical race condition in order processing
• Updated API documentation for v2 endpoints
**Commits**: 8 | **Lines**: +487/-123 | **Coverage**: 87.3%
**Tomorrow**: Payment webhook integration, rate limiting implementation
**Blockers**: Waiting on schema approval for GH-144
```
### Email Format
```html
Subject: Async Standup - John Doe - January 17, 2025
Hi team,
Here's my daily update:
YESTERDAY
========
SUCCESS: Completed GH-123: User authentication API endpoints
SUCCESS: Fixed race condition in order processing
SUCCESS: Updated API documentation
TODAY
=====
→ GH-145: Payment webhook integration (4 SP)
→ GH-146: Rate limiting for auth endpoints (2 SP)
→ Code review for PR #234
BLOCKERS
========
 GH-144: Waiting on database schema approval
 Impact: Blocks webhook implementation
 Need: Review by EOD
METRICS
=======
8 commits | 2 PRs merged | 2 issues completed (8 SP)
Coverage: 87.3% (+1.2%)
Best,
John
```
## Intelligent Features
### 1. Accomplishment Extraction from Commits
```typescript
// Analyze commit message to extract meaningful accomplishment
function extractAccomplishment(commit: Commit): Accomplishment {
 const message = commit.message;
 // Detect type from conventional commits
 const type = detectCommitType(message); // feat, fix, docs, refactor, etc.
 // Extract scope and description
 const { scope, description } = parseCommit(message);
 // Calculate impact
 const impact = calculateImpact(commit);
 // Correlate with Linear issues
 const linkedIssues = extractLinearIssues(message);
 return {
 type,
 scope,
 description,
 impact,
 linkedIssues,
 filesChanged: commit.stats.filesChanged,
 linesAdded: commit.stats.additions,
 linesRemoved: commit.stats.deletions
 };
}
```
**Example Transformation:**
```
Commit: "feat(auth): add JWT refresh token rotation (#234)"
Accomplishment:
SUCCESS: Added JWT refresh token rotation
 - Scope: Authentication
 - Impact: Security improvement
 - Linked: GH-234
 - Changes: 3 files, +124/-45 lines
```
### 2. Blocker Severity Classification
```typescript
interface Blocker {
 issue: LinearIssue;
 severity: 'critical' | 'high' | 'medium' | 'low';
 impact: string;
 waitingOn: string;
 workaround?: string;
 deadline?: Date;
}
function classifyBlocker(issue: LinearIssue): Blocker {
 let severity: Severity = 'medium';
 // Critical: Blocks sprint goal or production deployment
 if (issue.labels.includes('sprint-blocker') || issue.priority === 1) {
 severity = 'critical';
 }
 // High: Blocks other team members or customer-facing feature
 else if (issue.labels.includes('blocks-team') || issue.priority === 2) {
 severity = 'high';
 }
 // Extract what we're waiting on from comments
 const waitingOn = extractWaitingOn(issue.comments);
 // Check for workaround suggestions
 const workaround = extractWorkaround(issue.comments);
 return {
 issue,
 severity,
 impact: calculateImpact(issue),
 waitingOn,
 workaround,
 deadline: issue.dueDate
 };
}
```
### 3. Smart Work Planning
```typescript
// Generate "Today" section from Linear backlog
function planTodayWork(user: User, context: StandupContext): PlannedWork[] {
 // Get in-progress issues
 const inProgress = context.linearIssues.filter(i => i.state.type === 'started');
 // Get next priority issues if capacity available
 const backlog = await linearClient.issues({
 filter: {
 assignee: { id: { eq: user.id } },
 state: { type: { eq: 'triage' } }
 },
 orderBy: { priority: 'desc' }
 });
 // Calculate capacity (assuming 6 hours of focused work)
 const capacity = 6;
 const planned: PlannedWork[] = [];
 let allocated = 0;
 // Add in-progress work
 for (const issue of inProgress) {
 const estimate = issue.estimate ?? 2; // Default 2 hours
 planned.push({
 issue,
 description: issue.title,
 estimate,
 priority: 'continue'
 });
 allocated += estimate;
 }
 // Fill remaining capacity from backlog
 for (const issue of backlog) {
 if (allocated >= capacity) break;
 const estimate = issue.estimate ?? 2;
 if (allocated + estimate <= capacity) {
 planned.push({
 issue,
 description: issue.title,
 estimate,
 priority: 'new'
 });
 allocated += estimate;
 }
 }
 return planned;
}
```
### 4. Productivity Metrics Calculation
```typescript
interface ProductivityMetrics {
 commits: number;
 linesAdded: number;
 linesRemoved: number;
 prsCreated: number;
 prsMerged: number;
 prsReviewed: number;
 issuesCompleted: number;
 storyPointsCompleted: number;
 codeCoverage: number;
 buildTime: number;
 velocity: number; // Story points per day
 focusTime: number; // Hours of uninterrupted work
}
function calculateMetrics(timeframe: Timeframe): ProductivityMetrics {
 const commits = getCommits(timeframe);
 const prs = getPullRequests(timeframe);
 const issues = getLinearIssues(timeframe);
 return {
 commits: commits.length,
 linesAdded: commits.reduce((sum, c) => sum + c.stats.additions, 0),
 linesRemoved: commits.reduce((sum, c) => sum + c.stats.deletions, 0),
 prsCreated: prs.filter(pr => pr.createdAt >= timeframe.start).length,
 prsMerged: prs.filter(pr => pr.mergedAt >= timeframe.start).length,
 prsReviewed: getPRReviews(timeframe).length,
 issuesCompleted: issues.filter(i => i.completedAt).length,
 storyPointsCompleted: issues.reduce((sum, i) => sum + (i.estimate ?? 0), 0),
 codeCoverage: getCoverageMetric(),
 buildTime: getAverageBuildTime(),
 velocity: calculateVelocity(issues),
 focusTime: calculateFocusTime(timeframe)
 };
}
```
## Automation & Integration
### Slack Integration
```bash
# Post to Slack channel automatically
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
/async-standup --post-to slack --channel "#standup"
```
**Slack Bot Configuration:**
```javascript
// .claude/integrations/slack-standup.js
module.exports = {
 channelDefault: '#standup',
 scheduleTime: '17:00', // Post at 5 PM daily
 mentionOnBlockers: true,
 threadReplies: true
};
```
### Linear Integration
```bash
# Post as comment on sprint's Linear project
/async-standup --post-to linear --linear-project "PROJ-123"
```
### GitHub Actions Automation
```yaml
name: Daily Standup Automation
on:
 schedule:
# Run at 5 PM UTC (adjust for your timezone)
 - cron: '0 17 * * 1-5'
 workflow_dispatch: # Manual trigger
jobs:
 generate-standup:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v3
 - name: Generate async standup
 run: |
 claude /async-standup \
 --timeframe today \
 --format slack \
 --post-to slack \
 --channel "#standup"
 env:
 SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
 LINEAR_API_KEY: ${{ secrets.LINEAR_API_KEY }}
 GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
## Configuration
Create `.claude/standup-config.json`:
```json
{
 "user": {
 "name": "John Doe",
 "email": "john@greyhaven.com",
 "timezone": "America/Los_Angeles",
 "workingHours": {
 "start": "09:00",
 "end": "17:00"
 }
 },
 "integrations": {
 "linear": {
 "enabled": true,
 "teamId": "TEAM-123",
 "projectIds": ["PROJ-456"]
 },
 "slack": {
 "enabled": true,
 "channel": "#standup",
 "webhookUrl": "${SLACK_WEBHOOK_URL}"
 },
 "github": {
 "enabled": true,
 "org": "greyhaven-ai",
 "repos": ["api", "frontend", "workers"]
 }
 },
 "metrics": {
 "enabled": true,
 "trackCoverage": true,
 "trackBuildTime": true,
 "trackVelocity": true
 },
 "preferences": {
 "defaultFormat": "slack",
 "includeMetrics": true,
 "autoPost": false,
 "summarizeCommits": true,
 "groupByProject": false
 }
}
```
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
### Issue: No commits detected
**Cause**: Wrong Git author email or time range
**Solution**:
```bash
# Check Git author
git config user.email
# Check commits manually
git log --since="today 00:00" --author="your@email.com"
# Verify timeframe
/async-standup --timeframe yesterday --debug
```
### Issue: Linear issues not showing
**Cause**: Linear API authentication or filter issues
**Solution**:
```bash
# Verify Linear API key
echo $LINEAR_API_KEY
# Test Linear connection
curl -H "Authorization: Bearer $LINEAR_API_KEY" \
 https://api.linear.app/graphql \
 -d '{"query": "{ viewer { name email } }"}'
# Check assigned issues
/async-standup --debug
```
### Issue: Metrics inaccurate
**Cause**: Multiple Git repositories or incomplete data
**Solution**:
```json
// .claude/standup-config.json
{
 "github": {
 "repos": ["api", "frontend", "workers"], // List all repos
 "aggregateMetrics": true
 }
}
```
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
---
**Pro Tip**: Set up GitHub Actions to auto-post your standup at 5 PM daily. Your distributed team can read updates asynchronously in their own timezone, and you never forget to share your progress.
