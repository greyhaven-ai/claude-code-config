# Pipeline Patterns Reference

Detailed code patterns for building LLM pipelines in Grey Haven projects.

## Pipeline Stage Templates

### TypeScript (TanStack Start)

#### Base Pipeline Class

```typescript
// lib/pipelines/base-pipeline.ts
import { existsSync, mkdirSync, writeFileSync, readFileSync } from "fs";
import { join } from "path";
import Anthropic from "@anthropic-ai/sdk";

export abstract class BasePipeline<TInput, TOutput> {
  protected client: Anthropic;
  protected cacheDir: string;
  protected tenantId: string;

  constructor(tenantId: string, cacheDir?: string) {
    this.tenantId = tenantId;
    this.client = new Anthropic();
    this.cacheDir = cacheDir || join(process.cwd(), ".cache", tenantId);
  }

  // Stage 1: Get input data
  abstract acquire(id: string): Promise<TInput>;

  // Stage 2: Format prompt
  abstract prepare(input: TInput): string;

  // Stage 3: Call LLM (with caching)
  protected async process(prompt: string, cacheKey: string): Promise<string> {
    const cachePath = join(this.cacheDir, `${cacheKey}.response.json`);

    if (existsSync(cachePath)) {
      console.log(`[cache hit] ${cacheKey}`);
      return JSON.parse(readFileSync(cachePath, "utf-8")).response;
    }

    console.log(`[llm call] ${cacheKey}`);
    const response = await this.client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    });

    const text = response.content[0].type === "text"
      ? response.content[0].text
      : "";

    mkdirSync(this.cacheDir, { recursive: true });
    writeFileSync(cachePath, JSON.stringify({
      response: text,
      model: "claude-sonnet-4-20250514",
      timestamp: new Date().toISOString(),
    }));

    return text;
  }

  // Stage 4: Parse response
  abstract parse(response: string): TOutput;

  // Stage 5: Save/render output
  abstract render(id: string, output: TOutput): Promise<TOutput>;

  // Run full pipeline
  async run(id: string): Promise<TOutput> {
    const input = await this.acquire(id);
    const prompt = this.prepare(input);
    const response = await this.process(prompt, id);
    const output = this.parse(response);
    return await this.render(id, output);
  }

  // Run for multiple items
  async runBatch(ids: string[]): Promise<Map<string, TOutput>> {
    const results = new Map<string, TOutput>();

    for (const id of ids) {
      try {
        const output = await this.run(id);
        results.set(id, output);
      } catch (error) {
        console.error(`[error] ${id}:`, error);
      }
    }

    return results;
  }
}
```

#### Implementation Example

```typescript
// lib/pipelines/ticket-classifier.ts
import { z } from "zod";
import { BasePipeline } from "./base-pipeline";
import { db } from "@/db";
import { tickets } from "@/db/schema";
import { eq, and } from "drizzle-orm";

const ClassificationSchema = z.object({
  urgency: z.enum(["critical", "high", "medium", "low"]),
  category: z.string(),
  suggested_response: z.string(),
  confidence: z.number().min(0).max(1),
});

type Classification = z.infer<typeof ClassificationSchema>;

interface Ticket {
  id: string;
  subject: string;
  body: string;
  customer_email: string;
}

export class TicketClassifierPipeline extends BasePipeline<Ticket, Classification> {
  async acquire(ticketId: string): Promise<Ticket> {
    const ticket = await db.query.tickets.findFirst({
      where: and(
        eq(tickets.tenant_id, this.tenantId),
        eq(tickets.id, ticketId)
      ),
    });

    if (!ticket) throw new Error(`Ticket ${ticketId} not found`);
    return ticket;
  }

  prepare(ticket: Ticket): string {
    return `Classify this support ticket.

SUBJECT: ${ticket.subject}
BODY: ${ticket.body}
CUSTOMER: ${ticket.customer_email}

I will parse this programmatically. Respond with JSON:
{
  "urgency": "critical" | "high" | "medium" | "low",
  "category": "billing" | "technical" | "feature_request" | "other",
  "suggested_response": "Template response text",
  "confidence": 0.0 to 1.0
}`;
  }

  parse(response: string): Classification {
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error("No JSON in response");
    return ClassificationSchema.parse(JSON.parse(jsonMatch[0]));
  }

  async render(ticketId: string, classification: Classification): Promise<Classification> {
    await db.update(tickets)
      .set({
        urgency: classification.urgency,
        category: classification.category,
        suggested_response: classification.suggested_response,
        classification_confidence: classification.confidence,
        updated_at: new Date(),
      })
      .where(and(
        eq(tickets.tenant_id, this.tenantId),
        eq(tickets.id, ticketId)
      ));

    return classification;
  }
}

// Usage
const pipeline = new TicketClassifierPipeline("tenant-123");
const result = await pipeline.run("ticket-456");
```

### Python (FastAPI)

#### Base Pipeline Class

```python
# app/pipelines/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
import json
from typing import TypeVar, Generic
from anthropic import Anthropic

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")

class BasePipeline(ABC, Generic[TInput, TOutput]):
    def __init__(self, tenant_id: str, cache_dir: Path | None = None):
        self.tenant_id = tenant_id
        self.client = Anthropic()
        self.cache_dir = cache_dir or Path(".cache") / tenant_id

    @abstractmethod
    async def acquire(self, item_id: str) -> TInput:
        """Stage 1: Get input data."""
        pass

    @abstractmethod
    def prepare(self, input_data: TInput) -> str:
        """Stage 2: Format prompt."""
        pass

    async def process(self, prompt: str, cache_key: str) -> str:
        """Stage 3: Call LLM with caching."""
        cache_path = self.cache_dir / f"{cache_key}.response.json"

        if cache_path.exists():
            print(f"[cache hit] {cache_key}")
            return json.loads(cache_path.read_text())["response"]

        print(f"[llm call] {cache_key}")
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({
            "response": text,
            "model": "claude-sonnet-4-20250514",
            "timestamp": datetime.utcnow().isoformat(),
        }))

        return text

    @abstractmethod
    def parse(self, response: str) -> TOutput:
        """Stage 4: Parse response."""
        pass

    @abstractmethod
    async def render(self, item_id: str, output: TOutput) -> TOutput:
        """Stage 5: Save/render output."""
        pass

    async def run(self, item_id: str) -> TOutput:
        """Execute full pipeline."""
        input_data = await self.acquire(item_id)
        prompt = self.prepare(input_data)
        response = await self.process(prompt, item_id)
        output = self.parse(response)
        return await self.render(item_id, output)

    async def run_batch(self, item_ids: list[str]) -> dict[str, TOutput]:
        """Run for multiple items."""
        results = {}
        for item_id in item_ids:
            try:
                output = await self.run(item_id)
                results[item_id] = output
            except Exception as e:
                print(f"[error] {item_id}: {e}")
        return results
```

#### Implementation Example

```python
# app/pipelines/ticket_classifier.py
import re
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.pipelines.base import BasePipeline

class Classification(BaseModel):
    urgency: str = Field(pattern="^(critical|high|medium|low)$")
    category: str
    suggested_response: str
    confidence: float = Field(ge=0.0, le=1.0)

class TicketClassifierPipeline(BasePipeline[Ticket, Classification]):
    def __init__(self, tenant_id: str, db: AsyncSession):
        super().__init__(tenant_id)
        self.db = db

    async def acquire(self, ticket_id: str) -> Ticket:
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.id == ticket_id
            )
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found")
        return ticket

    def prepare(self, ticket: Ticket) -> str:
        return f"""Classify this support ticket.

SUBJECT: {ticket.subject}
BODY: {ticket.body}
CUSTOMER: {ticket.customer_email}

I will parse this programmatically. Respond with JSON:
{{
  "urgency": "critical" | "high" | "medium" | "low",
  "category": "billing" | "technical" | "feature_request" | "other",
  "suggested_response": "Template response text",
  "confidence": 0.0 to 1.0
}}"""

    def parse(self, response: str) -> Classification:
        match = re.search(r'\{[\s\S]*\}', response)
        if not match:
            raise ValueError("No JSON in response")
        return Classification.model_validate_json(match.group())

    async def render(self, ticket_id: str, classification: Classification) -> Classification:
        await self.db.execute(
            update(Ticket)
            .where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.id == ticket_id
            )
            .values(
                urgency=classification.urgency,
                category=classification.category,
                suggested_response=classification.suggested_response,
                classification_confidence=classification.confidence,
                updated_at=datetime.utcnow()
            )
        )
        await self.db.commit()
        return classification

# Usage
async def classify_ticket(tenant_id: str, ticket_id: str, db: AsyncSession):
    pipeline = TicketClassifierPipeline(tenant_id, db)
    return await pipeline.run(ticket_id)
```

---

## File-Based State Patterns

### State Directory Structure

```
.cache/
└── {tenant_id}/
    └── {pipeline_name}/
        └── {item_id}/
            ├── input.json      # Acquired data
            ├── prompt.txt      # Prepared prompt
            ├── response.json   # LLM response
            └── output.json     # Parsed output
```

### State Manager

```typescript
// lib/pipelines/state-manager.ts
import { existsSync, mkdirSync, writeFileSync, readFileSync } from "fs";
import { join } from "path";

type PipelineStage = "pending" | "acquired" | "prepared" | "processed" | "parsed" | "complete";

export class PipelineStateManager {
  private baseDir: string;

  constructor(tenantId: string, pipelineName: string) {
    this.baseDir = join(process.cwd(), ".cache", tenantId, pipelineName);
  }

  getItemDir(itemId: string): string {
    return join(this.baseDir, itemId);
  }

  getStage(itemId: string): PipelineStage {
    const dir = this.getItemDir(itemId);

    if (!existsSync(dir)) return "pending";
    if (!existsSync(join(dir, "input.json"))) return "acquired";
    if (!existsSync(join(dir, "prompt.txt"))) return "prepared";
    if (!existsSync(join(dir, "response.json"))) return "processed";
    if (!existsSync(join(dir, "output.json"))) return "parsed";
    return "complete";
  }

  saveInput(itemId: string, data: unknown): void {
    const dir = this.getItemDir(itemId);
    mkdirSync(dir, { recursive: true });
    writeFileSync(join(dir, "input.json"), JSON.stringify(data, null, 2));
  }

  loadInput<T>(itemId: string): T {
    return JSON.parse(readFileSync(join(this.getItemDir(itemId), "input.json"), "utf-8"));
  }

  savePrompt(itemId: string, prompt: string): void {
    writeFileSync(join(this.getItemDir(itemId), "prompt.txt"), prompt);
  }

  loadPrompt(itemId: string): string {
    return readFileSync(join(this.getItemDir(itemId), "prompt.txt"), "utf-8");
  }

  saveResponse(itemId: string, response: string): void {
    writeFileSync(
      join(this.getItemDir(itemId), "response.json"),
      JSON.stringify({ response, timestamp: new Date().toISOString() }, null, 2)
    );
  }

  loadResponse(itemId: string): string {
    return JSON.parse(readFileSync(join(this.getItemDir(itemId), "response.json"), "utf-8")).response;
  }

  saveOutput(itemId: string, output: unknown): void {
    writeFileSync(join(this.getItemDir(itemId), "output.json"), JSON.stringify(output, null, 2));
  }

  loadOutput<T>(itemId: string): T {
    return JSON.parse(readFileSync(join(this.getItemDir(itemId), "output.json"), "utf-8"));
  }

  // Get all items and their stages
  getProgress(): Map<string, PipelineStage> {
    const progress = new Map<string, PipelineStage>();
    if (!existsSync(this.baseDir)) return progress;

    const items = readdirSync(this.baseDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);

    for (const itemId of items) {
      progress.set(itemId, this.getStage(itemId));
    }

    return progress;
  }
}
```

---

## Parallel Execution Patterns

### Concurrent with Rate Limiting

```typescript
// lib/pipelines/concurrent-runner.ts
import pLimit from "p-limit";

export async function runConcurrent<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number = 5
): Promise<Map<T, R>> {
  const limit = pLimit(concurrency);
  const results = new Map<T, R>();

  await Promise.all(
    items.map(item =>
      limit(async () => {
        try {
          const result = await processor(item);
          results.set(item, result);
        } catch (error) {
          console.error(`Error processing ${item}:`, error);
        }
      })
    )
  );

  return results;
}

// Usage
const pipeline = new TicketClassifierPipeline("tenant-123");
const ticketIds = ["t1", "t2", "t3", "t4", "t5"];

const results = await runConcurrent(
  ticketIds,
  id => pipeline.run(id),
  3 // Max 3 concurrent LLM calls
);
```

### Python Async Pattern

```python
# app/pipelines/concurrent.py
import asyncio
from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")
R = TypeVar("R")

async def run_concurrent(
    items: list[T],
    processor: Callable[[T], Awaitable[R]],
    concurrency: int = 5
) -> dict[T, R]:
    """Run processor on items with limited concurrency."""
    semaphore = asyncio.Semaphore(concurrency)
    results = {}

    async def process_with_limit(item: T) -> tuple[T, R | None]:
        async with semaphore:
            try:
                result = await processor(item)
                return (item, result)
            except Exception as e:
                print(f"Error processing {item}: {e}")
                return (item, None)

    tasks = [process_with_limit(item) for item in items]
    completed = await asyncio.gather(*tasks)

    for item, result in completed:
        if result is not None:
            results[item] = result

    return results

# Usage
async def main():
    pipeline = TicketClassifierPipeline("tenant-123", db)
    ticket_ids = ["t1", "t2", "t3", "t4", "t5"]

    results = await run_concurrent(
        ticket_ids,
        pipeline.run,
        concurrency=3
    )
```

---

## Error Handling Patterns

### Retry with Exponential Backoff

```typescript
// lib/pipelines/retry.ts
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
  } = {}
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;

      const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
      console.log(`Retry ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error("Unreachable");
}

// Usage in pipeline
async process(prompt: string, cacheKey: string): Promise<string> {
  return withRetry(async () => {
    const response = await this.client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    });
    return response.content[0].text;
  }, { maxRetries: 3, baseDelay: 2000 });
}
```

### Graceful Degradation

```typescript
// Fallback chain: Sonnet → Haiku → Default response
async function processWithFallback(prompt: string): Promise<string> {
  try {
    return await callModel("claude-sonnet-4-20250514", prompt);
  } catch (e) {
    console.log("Sonnet failed, trying Haiku");
  }

  try {
    return await callModel("claude-haiku-3-5-20241022", prompt);
  } catch (e) {
    console.log("Haiku failed, using default");
  }

  return JSON.stringify({
    urgency: "medium",
    category: "unknown",
    suggested_response: "Thank you for your message. Our team will review and respond shortly.",
    confidence: 0.0,
  });
}
```

---

## Cost Tracking Pattern

```typescript
// lib/pipelines/cost-tracker.ts
interface CostEntry {
  timestamp: Date;
  pipeline: string;
  itemId: string;
  model: string;
  inputTokens: number;
  outputTokens: number;
  cost: number;
}

const PRICING: Record<string, { input: number; output: number }> = {
  "claude-sonnet-4-20250514": { input: 3.0, output: 15.0 },
  "claude-opus-4-5-20251101": { input: 15.0, output: 75.0 },
  "claude-haiku-3-5-20241022": { input: 0.8, output: 4.0 },
};

export function calculateCost(
  model: string,
  inputTokens: number,
  outputTokens: number
): number {
  const rates = PRICING[model] || PRICING["claude-sonnet-4-20250514"];
  return (inputTokens / 1_000_000) * rates.input +
         (outputTokens / 1_000_000) * rates.output;
}

// Track in pipeline
async process(prompt: string, cacheKey: string): Promise<string> {
  const response = await this.client.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });

  const cost = calculateCost(
    "claude-sonnet-4-20250514",
    response.usage.input_tokens,
    response.usage.output_tokens
  );

  console.log(`[cost] ${cacheKey}: $${cost.toFixed(4)}`);

  return response.content[0].text;
}
```
