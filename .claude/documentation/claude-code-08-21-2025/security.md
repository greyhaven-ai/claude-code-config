# Security

## How we approach security

### Security foundation

Your code's security is paramount. Claude Code is built with security at its core, developed according to Anthropic's comprehensive security program. Learn more at [Anthropic Trust Center](https://trust.anthropic.com/).

### Permission-based architecture

Claude Code uses strict read-only permissions by default. When additional actions are needed (editing files, running tests, executing commands), Claude Code requests explicit permission. Users control whether to approve actions once or allow them automatically.

### Built-in protections

- **Write access restriction**: Claude Code can only write to the folder where it was started and its subfolders—it cannot modify files in parent directories
- **Prompt fatigue mitigation**: Support for allowlisting frequently used safe commands per-user, per-codebase, or per-organization
- **Accept Edits mode**: Batch accept multiple edits while maintaining permission prompts for commands with side effects

### User responsibility

Claude Code only has the permissions you grant it. You're responsible for reviewing proposed code and commands for safety before approval.

## Protect against prompt injection

Prompt injection is a technique where an attacker attempts to override or manipulate an AI assistant's instructions by inserting malicious text.

### Core protections

- **Permission system**: Sensitive operations require explicit approval
- **Context-aware analysis**: Detects potentially harmful instructions by analyzing the full request
- **Input sanitization**: Prevents command injection by processing user inputs
- **Command blocklist**: Blocks risky commands that fetch arbitrary content from the web like `curl` and `wget`

### Privacy safeguards

- Limited retention periods for sensitive information
- Restricted access to user session data
- Clear policies against using feedback for model training

### Additional safeguards

- **Network request approval**: Tools that make network requests require user approval by default
- **Isolated context windows**: Web fetch uses a separate context window to avoid injecting potentially malicious prompts
- **Trust verification**: First-time codebase runs and new MCP servers require trust verification
- **Command injection detection**: Suspicious bash commands require manual approval even if previously allowlisted
- **Secure credential storage**: API keys and tokens are encrypted

**Best practices for working with untrusted content**:

1. Review suggested commands before approval
2. Avoid piping untrusted content directly to Claude
3. Verify proposed changes to critical files
4. Use virtual machines (VMs) to run scripts and make tool calls, especially when interacting with external web services
5. Report suspicious behavior with `/bug`

## MCP security

Claude Code allows users to configure Model Context Protocol (MCP) servers. The list of allowed MCP servers is configured in your source code, as part of Claude Code settings engineers check into source control.

We encourage either writing your own MCP servers or using MCP servers from providers that you trust. Anthropic does not manage or audit any MCP servers.

## Security best practices

### Working with sensitive code

- Review all suggested changes before approval
- Use project-specific permission settings for sensitive repositories
- Consider using devcontainers for additional isolation
- Regularly audit your permission settings with `/permissions`

### Team security

- Use enterprise managed policies to enforce organizational standards
- Share approved permission configurations through version control
- Train team members on security best practices
- Monitor Claude Code usage through OpenTelemetry metrics

### Reporting security issues

If you discover a security vulnerability in Claude Code:

1. Do not disclose it publicly
2. Report it through our [HackerOne program](https://hackerone.com/anthropic-vdp/reports/new?type=team&report_type=vulnerability)
3. Include detailed reproduction steps
4. Allow time for us to address the issue before public disclosure

## Related resources

- Identity and Access Management - Configure permissions and access controls
- Monitoring usage - Track and audit Claude Code activity
- Development containers - Secure, isolated environments
- [Anthropic Trust Center](https://trust.anthropic.com/) - Security certifications and compliance