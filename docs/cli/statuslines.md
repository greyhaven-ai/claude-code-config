# Claude Config Statuslines

Complete catalog of available statusline configurations for Claude Code.

## Quick Start

```bash
# Apply a statusline
claude-config statusline <name>

# List all available statuslines
claude-config list-statuslines

# Apply to specific location
claude-config statusline <name> --location [local|project|user]
```

## Available Statuslines (20 Total)

### Simple & Clean

#### `minimal`
- **Description**: Minimal statusline with just model and directory
- **Tags**: simple, clean
- **Shows**: Model name, current directory

#### `git-aware`
- **Description**: Shows model, directory, and git branch
- **Tags**: git, branch, simple
- **Shows**: Model, directory, current git branch

#### `compact`
- **Description**: Compact view with all key information
- **Tags**: compact, condensed, efficient
- **Shows**: Abbreviated model, branch, directory, lines added, cost

### Comprehensive

#### `grey-haven-default`
- **Description**: Comprehensive statusline with git, cost, and productivity metrics
- **Tags**: comprehensive, recommended, git, cost
- **Shows**: Full metrics dashboard

#### `productivity-dashboard`
- **Description**: Detailed productivity metrics and scoring
- **Tags**: metrics, productivity, detailed
- **Shows**: Comprehensive productivity analysis

#### `context-aware`
- **Description**: Adapts based on language, git workflow, and activity
- **Tags**: smart, adaptive, context
- **Shows**: Context-sensitive information

### Fun & Interactive

#### `tamagotchi`
- **Description**: Fun virtual pet that evolves with your coding activity
- **Tags**: fun, interactive, gamification
- **Shows**: Virtual pet status based on activity

#### `emoji-status`
- **Description**: Uses emojis to convey status at a glance
- **Tags**: emoji, visual, status
- **Shows**: Status through emoji indicators

#### `time-based`
- **Description**: Shows different emoji based on time of day
- **Tags**: time, emoji, dynamic
- **Shows**: Time-aware emoji and current time

### Technical & Metrics

#### `performance`
- **Description**: Shows API performance metrics
- **Tags**: performance, api, metrics
- **Shows**: API timing and performance percentage

#### `productivity-metrics`
- **Description**: Shows lines of code changed and productivity metrics
- **Tags**: productivity, metrics, cost-per-line
- **Shows**: Lines added/removed, cost per line

#### `progress-bar`
- **Description**: Shows context usage as a progress bar
- **Tags**: progress, visual, context
- **Shows**: Visual progress bar for context usage

### Cost & Resource Tracking

#### `cost-tracker`
- **Description**: Shows model, cost, and session duration
- **Tags**: cost, time, tracking
- **Shows**: Current cost and session time

### Development Focused

#### `development`
- **Description**: Shows model, git status, lines changed, and directory
- **Tags**: development, git, changes
- **Shows**: Branch, directory, lines added/removed

#### `git-dirty`
- **Description**: Shows git status with dirty/clean indicators
- **Tags**: git, status, clean
- **Shows**: Git clean/dirty status, branch, directory

### Visual & Colorful

#### `colorful`
- **Description**: Colorful statusline with ANSI codes
- **Tags**: colorful, ansi, visual
- **Shows**: Colored model, directory, and cost

#### `model-colors`
- **Description**: Different colors for different models
- **Tags**: model, colorful, visual
- **Shows**: Model-specific colors and emoji

### Environment & Context

#### `environment`
- **Description**: Shows different colors/emojis based on directory context
- **Tags**: environment, context, safety
- **Shows**: Environment indicator (PROD/STAGE/TEST/DEV)

### Branded

#### `grey-haven-branded`
- **Description**: Custom Grey Haven Studio branded statusline
- **Tags**: branded, grey-haven, custom
- **Shows**: Grey Haven branding with standard metrics

#### `bun-development`
- **Description**: Statusline optimized for Bun runtime
- **Tags**: bun, javascript, typescript
- **Shows**: Bun-specific branding

## Categories

### By Complexity
- **Simple**: minimal, git-aware, compact
- **Comprehensive**: grey-haven-default, productivity-dashboard, context-aware
- **Technical**: performance, productivity-metrics, progress-bar

### By Focus
- **Git Integration**: git-aware, git-dirty, development
- **Cost Tracking**: cost-tracker, productivity-metrics
- **Visual Appeal**: colorful, model-colors, emoji-status
- **Fun & Gamification**: tamagotchi, emoji-status, time-based

### By Use Case
- **Quick Setup**: minimal
- **Team Projects**: grey-haven-default, git-aware
- **Solo Development**: productivity-dashboard, development
- **Cost-Conscious**: cost-tracker, productivity-metrics
- **Fun Coding**: tamagotchi, time-based

## Creating Custom Statuslines

Add your custom statusline to `setup-claude-code/statuslines/statusline-catalog.json`:

```json
{
  "my-custom": {
    "description": "Description here",
    "command": "bash -c 'your command here'",
    "tags": ["custom", "personal"]
  }
}
```

Then apply it:
```bash
claude-config statusline my-custom
```

## Statusline Scripts

For complex statuslines, create a script in `.claude/statuslines/`:

```bash
# .claude/statuslines/my-statusline.sh
#!/usr/bin/env bash
input=$(cat)
MODEL=$(echo "$input" | jq -r ".model.display_name")
# Your custom logic here
echo "[$MODEL] Your custom output"
```

Then reference it in the catalog:
```json
{
  "my-script": {
    "description": "Custom script statusline",
    "command": "~/.claude/statuslines/my-statusline.sh",
    "tags": ["script", "custom"]
  }
}
```

## Recommendations

### For New Users
Start with `minimal` or `git-aware` for simplicity.

### For Teams
Use `grey-haven-default` for comprehensive metrics.

### For Fun
Try `tamagotchi` for a gamified experience.

### For Cost Management
Use `cost-tracker` or `productivity-metrics`.

### For Visual Appeal
Try `colorful`, `model-colors`, or `emoji-status`.