---
url: "https://docs.anthropic.com/en/docs/claude-code/devcontainer"
title: "Development containers - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Deployment

Development containers

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

The reference [devcontainer setup](https://github.com/anthropics/claude-code/tree/main/.devcontainer) and associated [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) offer a preconfigured development container that you can use as is, or customize for your needs. This devcontainer works with the Visual Studio Code [Dev Containers extension](https://code.visualstudio.com/docs/devcontainers/containers) and similar tools.

The container’s enhanced security measures (isolation and firewall rules) allow you to run `claude --dangerously-skip-permissions` to bypass permission prompts for unattended operation.

While the devcontainer provides substantial protections, no system is completely immune to all attacks.
When executed with `--dangerously-skip-permissions`, devcontainers do not prevent a malicious project from exfiltrating anything accessible in the devcontainer including Claude Code credentials.
We recommend only using devcontainers when developing with trusted repositories.
Always maintain good security practices and monitor Claude’s activities.

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#key-features)  Key features

- **Production-ready Node.js**: Built on Node.js 20 with essential development dependencies
- **Security by design**: Custom firewall restricting network access to only necessary services
- **Developer-friendly tools**: Includes git, ZSH with productivity enhancements, fzf, and more
- **Seamless VS Code integration**: Pre-configured extensions and optimized settings
- **Session persistence**: Preserves command history and configurations between container restarts
- **Works everywhere**: Compatible with macOS, Windows, and Linux development environments

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#getting-started-in-4-steps)  Getting started in 4 steps

1. Install VS Code and the Remote - Containers extension
2. Clone the [Claude Code reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer) repository
3. Open the repository in VS Code
4. When prompted, click “Reopen in Container” (or use Command Palette: Cmd+Shift+P → “Remote-Containers: Reopen in Container”)

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#configuration-breakdown)  Configuration breakdown

The devcontainer setup consists of three primary components:

- [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Controls container settings, extensions, and volume mounts
- [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Defines the container image and installed tools
- [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Establishes network security rules

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#security-features)  Security features

The container implements a multi-layered security approach with its firewall configuration:

- **Precise access control**: Restricts outbound connections to whitelisted domains only (npm registry, GitHub, Anthropic API, etc.)
- **Allowed outbound connections**: The firewall permits outbound DNS and SSH connections
- **Default-deny policy**: Blocks all other external network access
- **Startup verification**: Validates firewall rules when the container initializes
- **Isolation**: Creates a secure development environment separated from your main system

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#customization-options)  Customization options

The devcontainer configuration is designed to be adaptable to your needs:

- Add or remove VS Code extensions based on your workflow
- Modify resource allocations for different hardware environments
- Adjust network access permissions
- Customize shell configurations and developer tooling

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#example-use-cases)  Example use cases

### [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#secure-client-work)  Secure client work

Use devcontainers to isolate different client projects, ensuring code and credentials never mix between environments.

### [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#team-onboarding)  Team onboarding

New team members can get a fully configured development environment in minutes, with all necessary tools and settings pre-installed.

### [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#consistent-ci%2Fcd-environments)  Consistent CI/CD environments

Mirror your devcontainer configuration in CI/CD pipelines to ensure development and production environments match.

## [​](https://docs.anthropic.com/en/docs/claude-code/devcontainer\#related-resources)  Related resources

- [VS Code devcontainers documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [Claude Code security best practices](https://docs.anthropic.com/en/docs/claude-code/security)
- [Corporate proxy configuration](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy)

Was this page helpful?

YesNo

[LLM gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway) [Advanced installation](https://docs.anthropic.com/en/docs/claude-code/setup)

On this page

- [Key features](https://docs.anthropic.com/en/docs/claude-code/devcontainer#key-features)
- [Getting started in 4 steps](https://docs.anthropic.com/en/docs/claude-code/devcontainer#getting-started-in-4-steps)
- [Configuration breakdown](https://docs.anthropic.com/en/docs/claude-code/devcontainer#configuration-breakdown)
- [Security features](https://docs.anthropic.com/en/docs/claude-code/devcontainer#security-features)
- [Customization options](https://docs.anthropic.com/en/docs/claude-code/devcontainer#customization-options)
- [Example use cases](https://docs.anthropic.com/en/docs/claude-code/devcontainer#example-use-cases)
- [Secure client work](https://docs.anthropic.com/en/docs/claude-code/devcontainer#secure-client-work)
- [Team onboarding](https://docs.anthropic.com/en/docs/claude-code/devcontainer#team-onboarding)
- [Consistent CI/CD environments](https://docs.anthropic.com/en/docs/claude-code/devcontainer#consistent-ci%2Fcd-environments)
- [Related resources](https://docs.anthropic.com/en/docs/claude-code/devcontainer#related-resources)