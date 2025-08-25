# Claude Config Presets

Complete list of available configuration presets for `claude-config` CLI.

## Quick Start

```bash
# Apply a preset
claude-config preset <preset-name>

# List all presets
claude-config list-presets

# Apply to specific location
claude-config preset <preset-name> --location [local|project|user]
```

## Available Presets (23 Total)

### 🎯 Core Presets

#### `minimal`
- **Description**: Essential hooks and basic statusline for lightweight setup
- **Best for**: Quick setup, minimal overhead
- **Key features**: Basic session tracking, file modification alerts

#### `recommended` ⭐
- **Description**: Grey Haven's recommended setup with balanced features
- **Best for**: Most projects, good starting point
- **Key features**: Context loading, code quality, subagent support

#### `complete`
- **Description**: Every available hook, agent, and command - maximum automation
- **Best for**: Power users who want everything
- **Key features**: All hooks, all agents, all commands, full monitoring

#### `full`
- **Description**: All available features (similar to complete but simplified)
- **Best for**: Comprehensive setup
- **Key features**: Security, quality, testing, documentation

### 💻 Language-Specific

#### `python-focused`
- **Description**: Optimized for Python projects with testing and type checking
- **Best for**: Python development
- **Key features**: Import organization, coverage analysis, test generation

#### `python-data-science`
- **Description**: Jupyter notebooks, pandas, numpy, and ML model validation
- **Best for**: Data science and ML projects
- **Key features**: Notebook support, memory profiling, model validation

#### `javascript-focused`
- **Description**: Optimized for JS/TS projects with React support
- **Best for**: JavaScript/TypeScript development
- **Key features**: ESLint, Prettier, type checking, React testing

#### `bun-optimized`
- **Description**: JavaScript/TypeScript development optimized for Bun runtime
- **Best for**: Projects using Bun
- **Key features**: Bun-specific optimizations, fast execution

#### `react`
- **Description**: Optimized for React/Next.js development
- **Best for**: React applications
- **Key features**: Component testing, accessibility, performance monitoring

### 🔧 Workflow-Specific

#### `quality`
- **Description**: Testing, linting, formatting, and code quality automation
- **Best for**: Teams focused on code quality
- **Key features**: Auto-formatting, linting, test running, coverage

#### `code-quality`
- **Description**: Using existing quality-focused hooks and agents
- **Best for**: Quality-first development
- **Key features**: Impact analysis, similar code detection, import organization

#### `security`
- **Description**: Security validation using existing validator
- **Best for**: Security-sensitive projects
- **Key features**: Security validation, dependency analysis, prompt enhancement

#### `tdd`
- **Description**: Test-driven development with coverage tools
- **Best for**: TDD practitioners
- **Key features**: Coverage gaps, test generation, test data creation

#### `testing-focus`
- **Description**: Test generation, coverage analysis, and TDD tools
- **Best for**: Test-heavy projects
- **Key features**: Multiple test generators, coverage analysis

#### `performance`
- **Description**: Memory profiling and performance detection
- **Best for**: Performance-critical applications
- **Key features**: Memory profiling, regression detection, DB query analysis

### 🌐 API & Backend

#### `api-backend`
- **Description**: API contract validation and database performance
- **Best for**: Backend API development
- **Key features**: Contract validation, DB performance, security

#### `api-development`
- **Description**: REST/GraphQL API development (placeholder - hooks don't exist)
- **Best for**: API development
- **Key features**: Contract validation, documentation generation

### 📚 Specialized

#### `documentation`
- **Description**: Auto-documentation fetching, generation, and maintenance
- **Best for**: Documentation-heavy projects
- **Key features**: Auto-fetching docs, code narration, tech docs maintenance

#### `migration`
- **Description**: Helps with migrating and updating legacy code
- **Best for**: Code modernization projects
- **Key features**: Migration assistant, impact analysis, similar code finding

#### `linear-workflow`
- **Description**: Integration with Linear for issue tracking
- **Best for**: Teams using Linear
- **Key features**: Work completion, issue tracking, git integration

#### `subagent-orchestration`
- **Description**: Advanced multi-agent workflow coordination
- **Best for**: Complex workflows requiring multiple agents
- **Key features**: Agent routing, orchestration, result processing

#### `mcp-integration`
- **Description**: Commands for Chrome, Cloudflare, Context7, and Playwright MCP servers
- **Best for**: Projects using MCP servers
- **Key features**: Frontend debugging, deployment, documentation, visual testing

#### `integrated-workflow`
- **Description**: Advanced integration with workflow orchestration and quality gates
- **Best for**: Complex projects requiring workflow automation
- **Key features**: Workflow orchestration, quality gates, comprehensive monitoring

## Preset Categories

### By Complexity
- **Simple**: `minimal`
- **Balanced**: `recommended`, `quality`, `documentation`
- **Comprehensive**: `complete`, `full`

### By Language
- **Python**: `python-focused`, `python-data-science`, `tdd` (Python agent)
- **JavaScript/TypeScript**: `javascript-focused`, `bun-optimized`, `react`
- **Language Agnostic**: `minimal`, `recommended`, `quality`

### By Team Size
- **Solo Developer**: `minimal`, `recommended`
- **Small Team**: `quality`, `tdd`, `documentation`
- **Large Team**: `linear-workflow`, `security`, `complete`

### By Project Type
- **Web Frontend**: `react`, `javascript-focused`, `mcp-integration`
- **Backend API**: `api-backend`, `api-development`
- **Data Science**: `python-data-science`
- **Library/Package**: `documentation`, `testing-focus`
- **Enterprise**: `security`, `complete`, `linear-workflow`

## Combining Presets

You can layer presets by applying them in sequence:

```bash
# Start with language-specific
claude-config preset python-focused

# Add security on top
claude-config preset security

# Add specific workflow
claude-config preset linear-workflow
```

## Custom Presets

Create your own preset in `setup-claude-code/presets/my-preset.json`:

```json
{
  "name": "My Custom Preset",
  "description": "Description here",
  "hooks": {
    "SessionStart": [...],
    "PostToolUse": [...]
  },
  "agents": ["agent-name"],
  "commands": ["/command-name"],
  "statusLine": {...}
}
```

Then apply it:
```bash
claude-config preset my-preset
```

## Recommendations

### For New Users
Start with `recommended` - it's our balanced, battle-tested configuration.

### For Specific Languages
- Python → `python-focused`
- JavaScript → `javascript-focused`
- TypeScript → `bun-optimized` (if using Bun) or `javascript-focused`
- React → `react`

### For Specific Workflows
- Quality Focus → `quality` or `code-quality`
- Security Focus → `security`
- Test-Driven → `tdd` or `testing-focus`
- Documentation → `documentation`

### For Maximum Features
Use `complete` - it includes every hook, agent, and command available.