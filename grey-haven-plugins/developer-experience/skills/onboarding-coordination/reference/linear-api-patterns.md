# Linear API Patterns for Onboarding

Complete reference for Linear CLI and GraphQL API patterns specific to onboarding automation.

## Quick Reference

| Task | CLI Command | GraphQL Alternative |
|------|-------------|-------------------|
| Create issue | `linear issue create` | `issueCreate` mutation |
| List issues | `linear issue list` | `issues` query |
| Update issue | `linear issue update` | `issueUpdate` mutation |
| Add comment | `linear comment create` | `commentCreate` mutation |
| Create view | `linear view create` | `customViewCreate` mutation |
| Get team info | `linear team info` | `team` query |

## Installation and Authentication

```bash
# Install Linear CLI
npm install -g @linear/cli

# Authenticate
linear login
# Opens browser for OAuth authentication

# Verify authentication
linear whoami
# Output: Authenticated as alex@greyhaven.io

# Get API key (for scripts)
linear api-key
# Output: lin_api_xxxxxxxxxxxxxxxx
# Store in: LINEAR_API_KEY environment variable
```

## Issue Management

### Create Issue

**Basic Issue**:
```bash
linear issue create \
  --title "Alex Chen - Day 1: Environment Setup" \
  --team "Engineering" \
  --assignee "alex@greyhaven.io" \
  --priority 1
```

**With Description (Multiline)**:
```bash
linear issue create \
  --title "Week 1: First PR" \
  --team "Engineering" \
  --description "$(cat <<'EOF'
**Goal**: Ship first feature

Tasks:
- [ ] Complete good-first-issue
- [ ] Shadow buddy on code review
- [ ] Pair program on small feature
- [ ] Write tests
- [ ] Deploy to staging

**Success**: First PR merged by end of Week 1
EOF
)" \
  --assignee "alex@greyhaven.io" \
  --label "onboarding,good-first-issue" \
  --due-date "2024-01-22"
```

**With Parent (Sub-issue)**:
```bash
# Create parent issue
PARENT_ID=$(linear issue create \
  --title "Q1 2024 Onboarding" \
  --team "Engineering" \
  --json | jq -r '.id')

# Create child issue
linear issue create \
  --title "Alex - Week 1" \
  --team "Engineering" \
  --parent "$PARENT_ID"
```

**Capture Issue ID**:
```bash
ISSUE_ID=$(linear issue create \
  --title "30-Day Check-in" \
  --team "Engineering" \
  --json | jq -r '.id')

echo "Created issue: $ISSUE_ID"
# Output: Created issue: GH-123
```

### List Issues

**By Assignee**:
```bash
# List all issues assigned to new hire
linear issue list \
  --assignee "alex@greyhaven.io" \
  --label "onboarding"
```

**By Status**:
```bash
# List pending onboarding tasks
linear issue list \
  --label "onboarding" \
  --filter "state.type != 'completed'" \
  --sort "dueDate"
```

**By Due Date**:
```bash
# Upcoming milestones (next 7 days)
linear issue list \
  --label "milestone" \
  --filter "dueDate <= $(date -d '+7 days' +%Y-%m-%d)"
```

**JSON Output**:
```bash
# Get JSON for scripting
linear issue list \
  --assignee "alex@greyhaven.io" \
  --json | jq -r '.[] | "\(.title) (\(.state.name))"'

# Output:
# Day 1: Environment Setup (In Progress)
# Week 1: First PR (Todo)
# 30-Day Check-in (Todo)
```

### Update Issue

**Change Status**:
```bash
# Move to "In Progress"
linear issue update GH-123 \
  --state "In Progress"

# Mark complete
linear issue update GH-123 \
  --state "Done"
```

**Update Assignee**:
```bash
# Reassign to buddy
linear issue update GH-123 \
  --assignee "sarah@greyhaven.io"
```

**Update Due Date**:
```bash
# Extend due date
linear issue update GH-123 \
  --due-date "2024-02-15"
```

**Update Priority**:
```bash
# Increase priority (1 = Urgent, 2 = High, 3 = Normal, 4 = Low)
linear issue update GH-123 \
  --priority 1
```

## Comments

### Add Comment

**Basic Comment**:
```bash
linear comment create \
  --issue GH-123 \
  --body "Great progress on your first week!"
```

**Mention User**:
```bash
linear comment create \
  --issue GH-123 \
  --body "@sarah Can you pair with Alex on this issue?"
```

**Multiline Comment**:
```bash
linear comment create \
  --issue GH-123 \
  --body "$(cat <<'EOF'
## Week 1 Feedback

**What went well**:
- Environment setup smooth
- First PR merged successfully

**Areas for growth**:
- Ask more questions
- Review others' PRs

**Next week goals**:
- Ship 2 small features
- Lead daily standup once
EOF
)"
```

### List Comments

```bash
# Get all comments on issue
linear comment list \
  --issue GH-123 \
  --json | jq -r '.[] | "\(.user.name): \(.body)"'
```

## Labels

### Create Labels

```bash
# Onboarding label
linear label create \
  --name "onboarding" \
  --color "#FF6B6B" \
  --description "Onboarding tasks for new hires"

# Milestone label
linear label create \
  --name "milestone" \
  --color "#4ECDC4" \
  --description "30/60/90 day milestones"

# Good-first-issue label
linear label create \
  --name "good-first-issue" \
  --color "#7CB342" \
  --description "Good for new team members"
```

### List Labels

```bash
# List all labels in workspace
linear label list

# Filter by name
linear label list --filter "name ~ 'onboarding'"
```

## Custom Views

### Create Dashboard View

**Manager Dashboard** (All onboarding issues):
```bash
linear view create \
  --name "Onboarding Progress" \
  --team "Engineering" \
  --filter "label:onboarding" \
  --group-by "assignee" \
  --sort-by "dueDate"
```

**Buddy Dashboard** (Assigned to me):
```bash
linear view create \
  --name "My Buddy Assignments" \
  --filter "label:onboarding AND mentions:@me" \
  --group-by "created"
```

**Milestones View** (Upcoming check-ins):
```bash
linear view create \
  --name "Upcoming Milestones" \
  --filter "label:milestone AND dueDate >= today" \
  --sort-by "dueDate"
```

## GraphQL API

### Authentication

```typescript
import { LinearClient } from "@linear/sdk";

const linearClient = new LinearClient({
  apiKey: process.env.LINEAR_API_KEY,
});
```

### Create Issue (GraphQL)

```typescript
async function createOnboardingIssue(
  title: string,
  assigneeEmail: string,
  dueDate: string
) {
  const team = await linearClient.teams({ filter: { name: { eq: "Engineering" } } });
  const teamId = team.nodes[0].id;

  const user = await linearClient.users({ filter: { email: { eq: assigneeEmail } } });
  const assigneeId = user.nodes[0].id;

  const issue = await linearClient.createIssue({
    title,
    teamId,
    assigneeId,
    labelIds: ["label-onboarding-id"],
    dueDate,
    priority: 1,
  });

  return issue.id;
}

// Usage
const issueId = await createOnboardingIssue(
  "Alex - Week 1: First PR",
  "alex@greyhaven.io",
  "2024-01-22"
);
```

### Query Issues (GraphQL)

```typescript
async function getOnboardingIssues(assigneeEmail: string) {
  const issues = await linearClient.issues({
    filter: {
      assignee: { email: { eq: assigneeEmail } },
      labels: { name: { eq: "onboarding" } },
    },
    orderBy: "dueDate",
  });

  return issues.nodes.map((issue) => ({
    id: issue.id,
    title: issue.title,
    state: issue.state.name,
    dueDate: issue.dueDate,
  }));
}

// Usage
const issues = await getOnboardingIssues("alex@greyhaven.io");
console.log(issues);
```

### Add Comment (GraphQL)

```typescript
async function addFeedbackComment(issueId: string, feedback: string) {
  const comment = await linearClient.createComment({
    issueId,
    body: feedback,
  });

  return comment.id;
}

// Usage
await addFeedbackComment(
  "issue-id-123",
  "Great work on your first week! Keep up the momentum."
);
```

## Webhooks for Automation

### Webhook Configuration

```bash
# Create webhook (via Linear UI or API)
# Webhook URL: https://your-api.com/webhooks/linear
# Events: Issue created, Issue updated, Issue completed
```

### Webhook Handler (TypeScript)

```typescript
import { createHmac } from "crypto";

export async function handleLinearWebhook(req: Request) {
  // Verify webhook signature
  const signature = req.headers.get("linear-signature");
  const body = await req.text();

  const expectedSignature = createHmac("sha256", process.env.LINEAR_WEBHOOK_SECRET)
    .update(body)
    .digest("hex");

  if (signature !== expectedSignature) {
    return new Response("Invalid signature", { status: 401 });
  }

  const event = JSON.parse(body);

  // Handle milestone completion
  if (event.type === "Issue" && event.action === "update") {
    const issue = event.data;

    if (issue.labels.includes("milestone") && issue.state.type === "completed") {
      // Milestone completed - send Slack notification
      await sendSlackNotification({
        channel: "#engineering",
        text: `🎉 ${issue.assignee.name} completed: ${issue.title}`,
      });
    }
  }

  return new Response("OK", { status: 200 });
}
```

### Automated Reminders

```typescript
// Run daily via cron
async function sendMilestoneReminders() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  const upcomingMilestones = await linearClient.issues({
    filter: {
      labels: { name: { eq: "milestone" } },
      dueDate: { eq: tomorrow.toISOString().split("T")[0] },
      state: { type: { neq: "completed" } },
    },
  });

  for (const issue of upcomingMilestones.nodes) {
    await sendSlackNotification({
      channel: "@" + issue.assignee.email.split("@")[0],
      text: `Reminder: ${issue.title} is due tomorrow!`,
    });

    // Also notify manager
    await sendSlackNotification({
      channel: "@manager",
      text: `${issue.assignee.name}'s milestone "${issue.title}" is due tomorrow`,
    });
  }
}
```

## Batch Operations

### Create Multiple Issues

```bash
#!/bin/bash
# create-onboarding-batch.sh

NEW_HIRE="$1"
EMAIL="$2"
START_DATE="$3"

# Array of issues to create
ISSUES=(
  "Pre-boarding:Setup accounts and equipment:$(($(date -d "$START_DATE" +%s) - 259200)):1"
  "Day 1:Environment Setup:$(date -d "$START_DATE" +%s):1"
  "Week 1:First PR:$(($(date -d "$START_DATE" +%s) + 604800)):2"
  "30-Day:Check-in:$(($(date -d "$START_DATE" +%s) + 2592000)):3"
)

for issue_data in "${ISSUES[@]}"; do
  IFS=':' read -r title desc due priority <<< "$issue_data"

  linear issue create \
    --title "$NEW_HIRE - $title" \
    --description "$desc" \
    --team "Engineering" \
    --assignee "$EMAIL" \
    --label "onboarding" \
    --priority "$priority" \
    --due-date "$(date -d "@$due" +%Y-%m-%d)"

  echo "[OK] Created: $title"
done
```

### Bulk Update Issues

```bash
# Mark all onboarding issues as high priority
linear issue list \
  --label "onboarding" \
  --filter "state.type != 'completed'" \
  --json | jq -r '.[].id' | while read -r issue_id; do
    linear issue update "$issue_id" --priority 2
  done
```

## Team Management

### Get Team Information

```bash
# List all teams
linear team list

# Get specific team details
linear team info "Engineering"
# Output:
# Name: Engineering
# ID: TEAM_abc123
# Members: 12
```

### Get Team Members

```bash
# List team members
linear team members "Engineering" \
  --json | jq -r '.[] | "\(.name) <\(.email)>"'

# Output:
# Sarah Martinez <sarah@greyhaven.io>
# Mike Chen <mike@greyhaven.io>
# ...
```

## Troubleshooting

### Issue: Rate Limiting

```bash
# Linear API rate limits: 1000 requests/hour
# Check current rate limit status (GraphQL)
curl https://api.linear.app/graphql \
  -H "Authorization: Bearer $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { rateLimit { remaining limit } }"}'
```

**Solution**: Batch operations, add delays between API calls

### Issue: Invalid Team ID

```bash
# Error: Team not found

# Solution: Get correct team ID
TEAM_ID=$(linear team list --json | jq -r '.[] | select(.name=="Engineering") | .id')
echo "Team ID: $TEAM_ID"
```

### Issue: User Not Found

```bash
# Error: User with email 'alex@greyhaven.io' not found

# Solution: Check user exists
linear user list --filter "email ~ 'alex'"

# If not exists, invite user first
linear user invite --email "alex@greyhaven.io" --role member
```

### Issue: Label Not Found

```bash
# Error: Label 'onboarding' not found

# Solution: Create label first
linear label create \
  --name "onboarding" \
  --color "#FF6B6B"

# Then use in issue creation
```

## Advanced Patterns

### Conditional Issue Creation

```bash
# Only create 30-day milestone if new hire is junior
if [[ "$EXPERIENCE" == "junior" ]]; then
  linear issue create \
    --title "$NAME - 30-Day Check-in" \
    --description "Detailed feedback session for junior engineer"
else
  # Senior engineers: shorter check-in
  linear issue create \
    --title "$NAME - 30-Day Check-in" \
    --description "Quick alignment on impact and next projects"
fi
```

### Link Issues to GitHub PRs

```bash
# In PR description, mention Linear issue
gh pr create \
  --title "Add loading spinner" \
  --body "Fixes GH-123

Adds loading spinner to login button as part of onboarding.

Linear issue: https://linear.app/greyhaven/issue/GH-123"

# Linear automatically links PR to issue
```

### Export Onboarding Progress

```bash
# Generate CSV report of all onboarding issues
linear issue list \
  --label "onboarding" \
  --json | jq -r '
    ["Assignee", "Title", "State", "Due Date", "Priority"],
    (.[] | [.assignee.name, .title, .state.name, .dueDate, .priority])
    | @csv
  ' > onboarding-report.csv
```

---

Related: [Onboarding Best Practices](onboarding-best-practices.md) | [Buddy System Guide](buddy-system-guide.md) | [Milestone Tracking](milestone-tracking.md) | [Return to INDEX](INDEX.md)
