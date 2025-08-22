---
url: "https://docs.anthropic.com/en/docs/claude-code/llm-gateway"
title: "LLM gateway configuration - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Deployment

LLM gateway configuration

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

LLM gateways provide a centralized proxy layer between Claude Code and model providers, offering:

- **Centralized authentication** \- Single point for API key management
- **Usage tracking** \- Monitor usage across teams and projects
- **Cost controls** \- Implement budgets and rate limits
- **Audit logging** \- Track all model interactions for compliance
- **Model routing** \- Switch between providers without code changes

## [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#litellm-configuration)  LiteLLM configuration

LiteLLM is a third-party proxy service. Anthropic doesn’t endorse, maintain, or audit LiteLLM’s security or functionality. This guide is provided for informational purposes and may become outdated. Use at your own discretion.

### [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#prerequisites)  Prerequisites

- Claude Code updated to the latest version
- LiteLLM Proxy Server deployed and accessible
- Access to Claude models through your chosen provider

### [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#basic-litellm-setup)  Basic LiteLLM setup

**Configure Claude Code**:

#### [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#authentication-methods)  Authentication methods

##### Static API key

Simplest method using a fixed API key:

Copy

```bash
# Set in environment
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Or in Claude Code settings
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}

```

This value will be sent as the `Authorization` header.

##### Dynamic API key with helper

For rotating keys or per-user authentication:

1. Create an API key helper script:

Copy

```bash
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Example: Fetch key from vault
vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'

```

2. Configure Claude Code settings to use the helper:

Copy

```json
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}

```

3. Set token refresh interval:

Copy

```bash
# Refresh every hour (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000

```

This value will be sent as `Authorization` and `X-Api-Key` headers. The `apiKeyHelper` has lower precedence than `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY`.

#### [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#unified-endpoint-recommended)  Unified endpoint (recommended)

Using LiteLLM’s [Anthropic format endpoint](https://docs.litellm.ai/docs/anthropic_unified):

Copy

```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000

```

**Benefits of the unified endpoint over pass-through endpoints:**

- Load balancing
- Fallbacks
- Consistent support for cost tracking and end-user tracking

#### [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#provider-specific-pass-through-endpoints-alternative)  Provider-specific pass-through endpoints (alternative)

##### Anthropic API through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

Copy

```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic

```

##### Amazon Bedrock through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/bedrock):

Copy

```bash
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1

```

##### Google Vertex AI through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/vertex_ai):

Copy

```bash
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5

```

### [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#model-selection)  Model selection

By default, the models will use those specified in [Model configuration](https://docs.anthropic.com/en/docs/claude-code/bedrock-vertex-proxies#model-configuration).

If you have configured custom model names in LiteLLM, set the aforementioned environment variables to those custom names.

For more detailed information, refer to the [LiteLLM documentation](https://docs.litellm.ai/).

## [​](https://docs.anthropic.com/en/docs/claude-code/llm-gateway\#additional-resources)  Additional resources

- [LiteLLM documentation](https://docs.litellm.ai/)
- [Claude Code settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Corporate proxy setup](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy)
- [Third-party integrations overview](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations)

Was this page helpful?

YesNo

[Corporate proxy](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy) [Development containers](https://docs.anthropic.com/en/docs/claude-code/devcontainer)

On this page

- [LiteLLM configuration](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#litellm-configuration)
- [Prerequisites](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#prerequisites)
- [Basic LiteLLM setup](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#basic-litellm-setup)
- [Authentication methods](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#authentication-methods)
- [Unified endpoint (recommended)](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#unified-endpoint-recommended)
- [Provider-specific pass-through endpoints (alternative)](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#provider-specific-pass-through-endpoints-alternative)
- [Model selection](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#model-selection)
- [Additional resources](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#additional-resources)