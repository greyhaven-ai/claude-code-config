# LLM Project Case Studies

Real-world examples of successful LLM project methodology from industry leaders.

## 1. Karpathy's HN Time Capsule

**Project**: Analyze 128 historical Hacker News threads to extract insights about technology predictions.

### Methodology

1. **Manual Validation First**
   - Took ONE HN thread
   - Pasted into ChatGPT with analysis prompt
   - Confirmed Opus 4.5 could produce quality analysis
   - THEN started automation

2. **Pipeline Architecture**
   ```
   fetch_threads → prepare_prompt → analyze_with_llm → parse_output → render_markdown
   ```

3. **File System as State**
   - Each thread in own directory: `data/threads/{thread_id}/`
   - Files: `raw.json`, `prompt.txt`, `response.json`, `analysis.md`
   - Resume from any point on restart

4. **Structured Output**
   - Explicit format requirements in prompt
   - Section markers for parsing
   - Model knew output would be parsed programmatically

### Key Takeaways

| Principle | Application |
|-----------|-------------|
| Validate manually first | One thread in ChatGPT before coding |
| Deterministic wrapper | Only LLM call is non-deterministic |
| File-based checkpointing | Never re-process completed threads |
| 3-hour "vibe coding" | Let agent handle implementation details |

### Cost Analysis

- 128 threads × ~2000 input tokens × ~500 output tokens
- Using Opus 4.5: ~$5-10 total
- Cost per thread: ~$0.04-0.08

---

## 2. Vercel d0 (SWE-Bench Performance)

**Project**: Automated code generation and debugging for software engineering tasks.

### The Architectural Reduction Discovery

| Configuration | Tools | Success Rate |
|---------------|-------|--------------|
| Full toolset | 17 tools | 80% |
| **Reduced set** | **2 tools** | **100%** |

### Methodology

1. **Started with maximum tools** (17)
   - File read/write
   - Search/grep
   - Git operations
   - Shell commands
   - Browser tools
   - etc.

2. **Discovered degradation**
   - Model confused by tool abundance
   - Wrong tool selection
   - Inconsistent results

3. **Progressive reduction**
   - Removed tools one at a time
   - Measured success rate
   - Found sweet spot at 2 tools

4. **Final architecture**
   - `read_file` - Get file contents
   - `write_file` - Modify files
   - Everything else handled by deterministic code

### Key Takeaways

| Principle | Application |
|-----------|-------------|
| Fewer tools = better | 17 → 2 tools improved 80% → 100% |
| Combine operations | One tool doing A+B beats separate tools |
| Deterministic wrapper | Handle file operations outside LLM |
| Measure and iterate | Data-driven tool reduction |

### Grey Haven Application

```typescript
// Minimal tool pattern for Grey Haven agents
const MINIMAL_TOOLS = [
  {
    name: "query_database",
    description: "Read tenant data",
    // Replaces: list_tables, query_table, get_schema
  },
  {
    name: "update_record",
    description: "Modify tenant data",
    // Replaces: insert, update, delete, upsert
  },
];
```

---

## 3. Manus Agent (Production Optimization)

**Project**: Production agent system with optimized context management and caching.

### KV-Cache Optimization Patterns

#### Pattern 1: Append-Only Context

```python
# BAD: Modifying context breaks cache
messages = [system_prompt, user_message]
messages[0] = updated_system_prompt  # Invalidates entire cache

# GOOD: Append-only
messages = [system_prompt, user_message]
messages.append(new_context)  # Cache preserved for earlier messages
```

#### Pattern 2: Mask, Don't Remove Tools

```python
# BAD: Removing tools
tools = [tool for tool in tools if tool.name != "disabled_tool"]
# Different tool list = different cache key

# GOOD: Mask tools
for tool in tools:
    if tool.name == "disabled_tool":
        tool.description = "[UNAVAILABLE] " + tool.description
# Same structure = cache preserved
```

#### Pattern 3: File System as External Memory

```python
# Instead of growing context with conversation history
# Write to files and reference them

def remember(key: str, value: str):
    Path(f".memory/{key}.json").write_text(
        json.dumps({"value": value, "timestamp": datetime.now().isoformat()})
    )

def recall(key: str) -> str:
    path = Path(f".memory/{key}.json")
    if path.exists():
        return json.loads(path.read_text())["value"]
    return None

# Context stays small, memory is unlimited
```

### Key Takeaways

| Principle | Application |
|-----------|-------------|
| Append-only context | Never modify, only add |
| Mask tools | Change description, not list |
| File system memory | Keep context small, use files |
| Structured directories | Predictable file locations |

### Grey Haven Application

```typescript
// Memory pattern for Grey Haven pipelines
const memoryDir = `.cache/memory/${tenant_id}`;

async function remember(key: string, value: unknown) {
  const filePath = join(memoryDir, `${key}.json`);
  await writeFile(filePath, JSON.stringify({
    value,
    tenant_id,
    timestamp: new Date().toISOString(),
  }));
}

async function recall(key: string): Promise<unknown | null> {
  const filePath = join(memoryDir, `${key}.json`);
  if (existsSync(filePath)) {
    return JSON.parse(await readFile(filePath, 'utf-8')).value;
  }
  return null;
}
```

---

## 4. Anthropic Multi-Agent Research

**Project**: Research into effective multi-agent coordination patterns.

### Key Findings

#### 1. Handoff > Parallel for Complex Tasks

```
Sequential with handoffs:
  Agent A → (context) → Agent B → (context) → Agent C

Better for: Deep analysis, dependent reasoning

Parallel execution:
  Agent A ─┐
  Agent B ─┼→ Aggregator
  Agent C ─┘

Better for: Independent subtasks, speed
```

#### 2. Context Summarization at Handoffs

```python
# Don't pass full conversation
def handoff(from_agent: str, to_agent: str, context: dict):
    summary = summarize_for_handoff(context)
    # Only essential information transfers
    return {
        "from": from_agent,
        "key_findings": summary["findings"],
        "next_action": summary["recommendation"],
        # NOT: full conversation history
    }
```

#### 3. Tool Specialization by Agent

```python
AGENT_TOOLS = {
    "researcher": ["web_search", "read_file"],
    "coder": ["write_file", "run_tests"],
    "reviewer": ["read_file", "add_comment"],
}

# Each agent gets minimal tools for their role
```

### Key Takeaways

| Principle | Application |
|-----------|-------------|
| Handoffs for depth | Sequential when tasks depend |
| Parallel for breadth | Independent subtasks |
| Summarize at handoffs | Don't pass full context |
| Specialize tools | Each agent gets minimal set |

### Grey Haven Application

```typescript
// Multi-agent pattern for Grey Haven
interface AgentHandoff {
  from_agent: string;
  to_agent: string;
  tenant_id: string;
  summary: {
    task_completed: string;
    findings: string[];
    next_action: string;
  };
  // Explicitly NOT: full conversation
}

const AGENT_CONFIGS = {
  analyzer: {
    tools: ["query_database"],
    model: "claude-haiku-3-5-20241022", // Fast for analysis
  },
  writer: {
    tools: ["update_record"],
    model: "claude-sonnet-4-20250514", // Quality for writing
  },
};
```

---

## Summary: Universal Patterns

| Pattern | Karpathy | Vercel d0 | Manus | Anthropic |
|---------|----------|-----------|-------|-----------|
| Manual validation first | ✓ | - | - | - |
| Minimal tools | - | ✓ | ✓ | ✓ |
| File-based state | ✓ | - | ✓ | - |
| Pipeline architecture | ✓ | ✓ | ✓ | ✓ |
| Context optimization | - | - | ✓ | ✓ |
| Structured output | ✓ | ✓ | - | - |

**The common thread**: Deterministic, resumable pipelines wrapping minimal LLM calls.
