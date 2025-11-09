# CC-Trace Analyze

Analyze captured Claude Code API traffic using cc-trace analysis scripts.

## Instructions

1. First, confirm they have captured flows:
   - Ask if they've run a capture session (`/cc-trace-start`)
   - Default flow file location: `~/claude-flows.mitm`
   - Ask if they want to analyze a different file

2. Offer analysis options:

### Option 1: View Last User Prompt

Shows the most recent prompt sent to Claude:

```bash
~/.config/claude/plugins/debugging/scripts/show-last-prompt.sh
```

Or with custom flow file:
```bash
~/.config/claude/plugins/debugging/scripts/show-last-prompt.sh /path/to/flows.mitm
```

**Use case**: Quick check of what was sent in the last request

### Option 2: Extract All Slash Command Expansions

Shows all user messages (including expanded slash commands):

```bash
mitmdump -r ~/claude-flows.mitm \
  -s ~/.config/claude/plugins/debugging/scripts/extract-slash-commands.py
```

**Use case**: See how slash commands are expanded, review conversation history

### Option 3: Parse Streamed Response

Parse a streamed API response from clipboard:

```bash
pbpaste | npx tsx ~/.config/claude/plugins/debugging/scripts/parse-streamed-response.ts
```

**Use case**: Debug streaming issues, examine tool calls in detail

### Option 4: Manual Inspection (Web UI)

If mitmweb is still running:
- Open http://127.0.0.1:8081
- Browse through captured flows
- Click on any request to see full details

If mitmweb is not running, replay the flows:
```bash
mitmweb --web-port 8081 \
  --set flow_filter='~d api.anthropic.com' \
  --rfile ~/claude-flows.mitm
```

3. Help interpret results based on what they're looking for:

**For debugging context issues**:
- Look at request body → messages array → user messages
- Check what files were included in context
- Examine system prompts and instructions

**For optimizing token usage**:
- Look at response → usage object
- Compare input_tokens vs output_tokens
- Identify unnecessary context

**For understanding tool calls**:
- Look at response → content array
- Find entries with type: "tool_use"
- Examine tool names and parameters

**For performance analysis**:
- Check request timestamps
- Measure time between request and first response chunk
- Look for patterns in slow responses

4. Offer to create custom analysis scripts if they have specific needs

## Advanced Analysis

### Custom Filters

Show only specific types of requests:
```bash
# Only requests with file context
mitmdump -r ~/claude-flows.mitm --flow-filter '~bs 10000'

# Only errors
mitmdump -r ~/claude-flows.mitm --flow-filter '~c 4'
```

### Export Specific Flows

```bash
# From mitmweb UI:
# 1. Right-click on flow
# 2. Select "Export"
# 3. Choose format (JSON, HAR, etc.)
```

### Statistics

Count tool usage:
```bash
mitmdump -r ~/claude-flows.mitm \
  -s ~/.config/claude/plugins/debugging/scripts/extract-slash-commands.py \
  | grep -c "tool_use"
```

## Cleanup

After analysis, offer to clean up:
```bash
# Remove old flows (if no longer needed)
rm ~/claude-flows.mitm

# Or archive for later
mv ~/claude-flows.mitm ~/claude-flows-$(date +%Y%m%d-%H%M%S).mitm
```

Remind about security: Flows contain API keys and sensitive data. Handle carefully.
