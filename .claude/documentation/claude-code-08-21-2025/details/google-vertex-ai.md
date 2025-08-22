---
url: "https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai"
title: "Claude Code on Google Vertex AI - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Deployment

Claude Code on Google Vertex AI

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

## [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#prerequisites)  Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

- A Google Cloud Platform (GCP) account with billing enabled
- A GCP project with Vertex AI API enabled
- Access to desired Claude models (e.g., Claude Sonnet 4)
- Google Cloud SDK ( `gcloud`) installed and configured
- Quota allocated in desired GCP region

Vertex AI may not support the Claude Code default models on non- `us-east5` regions. Ensure you are using `us-east5` and have quota allocated, or switch to supported models.

## [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#setup)  Setup

### [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#1-enable-vertex-ai-api)  1\. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

Copy

```bash
# Set your project ID
gcloud config set project YOUR-PROJECT-ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

```

### [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#2-request-model-access)  2\. Request model access

Request access to Claude models in Vertex AI:

1. Navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Search for “Claude” models
3. Request access to desired Claude models (e.g., Claude Sonnet 4)
4. Wait for approval (may take 24-48 hours)

### [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#3-configure-gcp-credentials)  3\. Configure GCP credentials

Claude Code uses standard Google Cloud authentication.

For more information, see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).

When authenticating, Claude Code will automatically use the project ID from the `ANTHROPIC_VERTEX_PROJECT_ID` environment variable. To override this, set one of these environment variables: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, or `GOOGLE_APPLICATION_CREDENTIALS`.

### [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#4-configure-claude-code)  4\. Configure Claude Code

Set the following environment variables:

Copy

```bash
# Enable Vertex AI integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Override regions for specific models
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-central1
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west4
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west4

```

[Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) is automatically supported when you specify the `cache_control` ephemeral flag. To disable it, set `DISABLE_PROMPT_CACHING=1`. For heightened rate limits, contact Google Cloud support.

When using Vertex AI, the `/login` and `/logout` commands are disabled since authentication is handled through Google Cloud credentials.

### [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#5-model-configuration)  5\. Model configuration

Claude Code uses these default models for Vertex AI:

| Model type | Default value |
| --- | --- |
| Primary model | `claude-sonnet-4@20250514` |
| Small/fast model | `claude-3-5-haiku@20241022` |

To customize models:

Copy

```bash
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-3-5-haiku@20241022'

```

## [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#iam-configuration)  IAM configuration

Assign the required IAM permissions:

The `roles/aiplatform.user` role includes the required permissions:

- `aiplatform.endpoints.predict` \- Required for model invocation
- `aiplatform.endpoints.computeTokens` \- Required for token counting

For more restrictive permissions, create a custom role with only the permissions above.

For details, see [Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

We recommend creating a dedicated GCP project for Claude Code to simplify cost tracking and access control.

## [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#troubleshooting)  Troubleshooting

If you encounter quota issues:

- Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter “model not found” 404 errors:

- Verify you have access to the specified region
- Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)

If you encounter 429 errors:

- Ensure the primary model and small/fast model are supported in your selected region

## [​](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai\#additional-resources)  Additional resources

- [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
- [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing)
- [Vertex AI quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)

Was this page helpful?

YesNo

[Amazon Bedrock](https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock) [Corporate proxy](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy)

On this page

- [Prerequisites](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#prerequisites)
- [Setup](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#setup)
- [1\. Enable Vertex AI API](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#1-enable-vertex-ai-api)
- [2\. Request model access](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#2-request-model-access)
- [3\. Configure GCP credentials](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#3-configure-gcp-credentials)
- [4\. Configure Claude Code](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#4-configure-claude-code)
- [5\. Model configuration](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#5-model-configuration)
- [IAM configuration](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#iam-configuration)
- [Troubleshooting](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#troubleshooting)
- [Additional resources](https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai#additional-resources)