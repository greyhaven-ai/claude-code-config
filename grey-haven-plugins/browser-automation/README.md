# Browser Automation Plugin

**Automate web browser interactions using natural language**

This Grey Haven plugin integrates the Browserbase `agent-browse` tool, enabling Claude Code to perform web browsing and automation tasks using Stagehand, an AI-powered browser automation framework.

## Features

- **Natural Language Control**: Browse websites and interact with web pages using plain English commands
- **Web Scraping**: Extract structured data from websites with custom schemas
- **QA Testing**: Automate testing of web applications
- **Form Automation**: Fill forms, click buttons, and navigate complex workflows
- **Screenshot Capture**: Take screenshots for verification and debugging
- **Session Persistence**: Browser stays open between commands to maintain cookies and state

## Installation

### Prerequisites

Before using this plugin, you need to install the `agent-browse` tool:

```bash
# Clone the repository
git clone https://github.com/browserbase/agent-browse.git
cd agent-browse

# Install dependencies
npm install

# Link the browser command globally
npm link

# Set your Anthropic API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Verify installation
browser navigate https://example.com
```

### Requirements

- **Google Chrome**: Must be installed on your system
- **Node.js**: For running the browser automation tool
- **Anthropic API Key**: Required for AI-powered interactions

### Plugin Installation

This plugin is automatically available when you configure the Grey Haven marketplace in your Claude Code settings.

Add to your `~/.claude/settings.json`:

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/path/to/grey-haven-plugins"
    }]
  }
}
```

Then activate the skill when needed by invoking it in your Claude Code session.

## Usage

### Basic Commands

The plugin provides access to the `browser` CLI tool through Claude Code:

```bash
# Navigate to a URL
browser navigate https://example.com

# Perform actions (click, type, scroll)
browser act "Click the sign up button"
browser act "Type 'hello@example.com' into the email field"

# Extract data
browser extract "Get all product names and prices"

# Discover elements
browser observe "Find all buttons on the page"

# Take screenshot
browser screenshot

# Close browser
browser close
```

### Example Workflows

**Data Extraction:**
```bash
browser navigate https://news.ycombinator.com
browser extract "Get the top 5 post titles and URLs" '{"posts": [{"title": "string", "url": "string"}]}'
browser close
```

**Form Automation:**
```bash
browser navigate https://example.com/signup
browser act "Type 'John Doe' into the name field"
browser act "Type 'john@example.com' into the email field"
browser act "Click the submit button"
browser screenshot
browser close
```

**Testing Workflow:**
```bash
browser navigate https://your-app.com
browser observe "Find the login button"
browser act "Click the login button"
browser act "Type 'testuser' into username"
browser act "Type 'password123' into password"
browser act "Click submit"
browser screenshot
browser close
```

## Best Practices

1. **Always Navigate First**: Before interacting with a page, use `browser navigate <url>`
2. **Use Specific Instructions**: More detail = better results (e.g., "Click the blue Submit button in the footer" vs "Click submit")
3. **Verify with Screenshots**: Use `browser screenshot` after actions to confirm success
4. **Strategic Waiting**: Add explicit waits after actions that trigger page changes
5. **Close Sessions**: Always run `browser close` when finished to free resources
6. **Discovery Before Action**: Use `browser observe` when unsure about page elements

## Configuration

The plugin includes a `setup.json` file that tracks setup completion. After installing the prerequisites, you can update this file to mark setup as complete.

## Documentation

For detailed documentation, see the skill files:

- **SKILL.md**: Complete skill definition and overview
- **EXAMPLES.md**: Comprehensive usage examples
- **REFERENCE.md**: Technical reference and API documentation
- **setup.json**: Setup prerequisites and verification

## Integration

This plugin integrates the following open-source tools:

- **Stagehand**: AI-powered browser automation framework
- **agent-browse**: Browserbase's Claude Code skill for browser control

Original repository: [browserbase/agent-browse](https://github.com/browserbase/agent-browse)

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

Original work by Browserbase.

## Support

For issues specific to the Grey Haven integration, please open an issue in the Grey Haven repository.

For issues with the underlying browser automation tool, see the [agent-browse repository](https://github.com/browserbase/agent-browse).

## Version History

- **1.0.0** - Initial integration into Grey Haven marketplace
  - Integrated all skill files from browserbase/agent-browse
  - Added Grey Haven plugin structure
  - Maintained full compatibility with original tool
