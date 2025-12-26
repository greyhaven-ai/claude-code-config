# TanStack Start Pipeline Example

Complete example of an LLM pipeline in a Grey Haven TanStack Start application.

## Use Case: Content Summarization Pipeline

Summarize long-form content for tenant dashboards with caching and database storage.

## Directory Structure

```
app/
├── lib/
│   └── pipelines/
│       ├── base-pipeline.ts          # Base class
│       ├── content-summarizer.ts     # Implementation
│       └── types.ts                  # Shared types
├── routes/
│   └── api/
│       └── summarize.$contentId.ts   # API route
└── db/
    └── schema.ts                     # Drizzle schema
```

## Implementation

### 1. Database Schema

```typescript
// db/schema.ts
import { pgTable, uuid, text, timestamp, jsonb } from "drizzle-orm/pg-core";

export const contents = pgTable("contents", {
  id: uuid("id").primaryKey().defaultRandom(),
  tenant_id: uuid("tenant_id").notNull(),
  title: text("title").notNull(),
  body: text("body").notNull(),
  // LLM-generated fields
  summary: text("summary"),
  key_points: jsonb("key_points").$type<string[]>(),
  summary_generated_at: timestamp("summary_generated_at"),
  // Standard fields
  created_at: timestamp("created_at").defaultNow().notNull(),
  updated_at: timestamp("updated_at").defaultNow().notNull(),
});
```

### 2. Base Pipeline

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
    this.cacheDir = cacheDir || join(process.cwd(), ".cache", "pipelines", tenantId);
  }

  abstract acquire(id: string): Promise<TInput>;
  abstract prepare(input: TInput): string;
  abstract parse(response: string): TOutput;
  abstract render(id: string, output: TOutput): Promise<TOutput>;

  protected async process(prompt: string, cacheKey: string): Promise<string> {
    const cachePath = join(this.cacheDir, `${cacheKey}.json`);

    if (existsSync(cachePath)) {
      const cached = JSON.parse(readFileSync(cachePath, "utf-8"));
      console.log(`[cache hit] ${cacheKey}`);
      return cached.response;
    }

    console.log(`[llm call] ${cacheKey}`);
    const response = await this.client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    });

    const text = response.content[0].type === "text" ? response.content[0].text : "";

    mkdirSync(this.cacheDir, { recursive: true });
    writeFileSync(cachePath, JSON.stringify({
      response: text,
      input_tokens: response.usage.input_tokens,
      output_tokens: response.usage.output_tokens,
      timestamp: new Date().toISOString(),
    }));

    return text;
  }

  async run(id: string): Promise<TOutput> {
    const input = await this.acquire(id);
    const prompt = this.prepare(input);
    const response = await this.process(prompt, id);
    const output = this.parse(response);
    return await this.render(id, output);
  }
}
```

### 3. Content Summarizer Implementation

```typescript
// lib/pipelines/content-summarizer.ts
import { z } from "zod";
import { BasePipeline } from "./base-pipeline";
import { db } from "@/db";
import { contents } from "@/db/schema";
import { eq, and } from "drizzle-orm";

// Schema for parsed output
const SummarySchema = z.object({
  summary: z.string().min(50).max(500),
  key_points: z.array(z.string()).min(1).max(5),
  tone: z.enum(["formal", "casual", "technical", "persuasive"]),
  word_count: z.number(),
});

type Summary = z.infer<typeof SummarySchema>;

interface Content {
  id: string;
  tenant_id: string;
  title: string;
  body: string;
}

export class ContentSummarizerPipeline extends BasePipeline<Content, Summary> {
  async acquire(contentId: string): Promise<Content> {
    const content = await db.query.contents.findFirst({
      where: and(
        eq(contents.tenant_id, this.tenantId),
        eq(contents.id, contentId)
      ),
    });

    if (!content) {
      throw new Error(`Content ${contentId} not found for tenant ${this.tenantId}`);
    }

    return content;
  }

  prepare(content: Content): string {
    return `Summarize this content for a business dashboard.

TITLE: ${content.title}

CONTENT:
${content.body}

I will parse this programmatically. Respond with valid JSON:
{
  "summary": "2-3 sentence executive summary (50-500 chars)",
  "key_points": ["point 1", "point 2", "point 3"] (1-5 items),
  "tone": "formal" | "casual" | "technical" | "persuasive",
  "word_count": number (original content word count)
}

Ensure JSON is complete and parseable.`;
  }

  parse(response: string): Summary {
    // Extract JSON from response
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error("No JSON found in response");
    }

    try {
      const parsed = JSON.parse(jsonMatch[0]);
      return SummarySchema.parse(parsed);
    } catch (error) {
      throw new Error(`Failed to parse summary: ${error}`);
    }
  }

  async render(contentId: string, summary: Summary): Promise<Summary> {
    await db.update(contents)
      .set({
        summary: summary.summary,
        key_points: summary.key_points,
        summary_generated_at: new Date(),
        updated_at: new Date(),
      })
      .where(and(
        eq(contents.tenant_id, this.tenantId),
        eq(contents.id, contentId)
      ));

    return summary;
  }
}

// Factory function for easy instantiation
export function createContentSummarizer(tenantId: string) {
  return new ContentSummarizerPipeline(tenantId);
}
```

### 4. API Route

```typescript
// routes/api/summarize.$contentId.ts
import { json } from "@tanstack/start";
import { createAPIFileRoute } from "@tanstack/start/api";
import { createContentSummarizer } from "@/lib/pipelines/content-summarizer";
import { getAuthenticatedTenant } from "@/lib/auth";

export const APIRoute = createAPIFileRoute("/api/summarize/$contentId")({
  POST: async ({ request, params }) => {
    const { contentId } = params;

    // Get tenant from auth
    const tenant = await getAuthenticatedTenant(request);
    if (!tenant) {
      return json({ error: "Unauthorized" }, { status: 401 });
    }

    try {
      const pipeline = createContentSummarizer(tenant.id);
      const summary = await pipeline.run(contentId);

      return json({
        success: true,
        summary,
      });
    } catch (error) {
      console.error(`Summarization failed for ${contentId}:`, error);

      return json({
        error: "Summarization failed",
        message: error instanceof Error ? error.message : "Unknown error",
      }, { status: 500 });
    }
  },
});
```

### 5. React Query Integration

```typescript
// lib/queries/use-summarize.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";

export function useSummarize(contentId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const response = await fetch(`/api/summarize/${contentId}`, {
        method: "POST",
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Summarization failed");
      }

      return response.json();
    },
    onSuccess: () => {
      // Invalidate content query to refresh with new summary
      queryClient.invalidateQueries({ queryKey: ["content", contentId] });
    },
  });
}

// Usage in component
function ContentCard({ content }) {
  const summarize = useSummarize(content.id);

  return (
    <div>
      <h2>{content.title}</h2>
      {content.summary ? (
        <p className="text-gray-600">{content.summary}</p>
      ) : (
        <button
          onClick={() => summarize.mutate()}
          disabled={summarize.isPending}
        >
          {summarize.isPending ? "Generating..." : "Generate Summary"}
        </button>
      )}
    </div>
  );
}
```

## Testing the Pipeline

```typescript
// tests/pipelines/content-summarizer.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { ContentSummarizerPipeline } from "@/lib/pipelines/content-summarizer";

describe("ContentSummarizerPipeline", () => {
  let pipeline: ContentSummarizerPipeline;

  beforeEach(() => {
    pipeline = new ContentSummarizerPipeline("test-tenant-id");
  });

  it("should prepare a valid prompt", () => {
    const content = {
      id: "test-id",
      tenant_id: "test-tenant-id",
      title: "Test Article",
      body: "This is the test content body.",
    };

    const prompt = pipeline.prepare(content);

    expect(prompt).toContain("Test Article");
    expect(prompt).toContain("test content body");
    expect(prompt).toContain("I will parse this programmatically");
  });

  it("should parse valid JSON response", () => {
    const response = `Here's the summary:
{
  "summary": "This is a test summary of the content.",
  "key_points": ["Point 1", "Point 2"],
  "tone": "formal",
  "word_count": 100
}`;

    const parsed = pipeline.parse(response);

    expect(parsed.summary).toBe("This is a test summary of the content.");
    expect(parsed.key_points).toHaveLength(2);
    expect(parsed.tone).toBe("formal");
  });

  it("should throw on invalid JSON", () => {
    const response = "No JSON here, just text.";

    expect(() => pipeline.parse(response)).toThrow("No JSON found");
  });
});
```

## Key Patterns Demonstrated

1. **Tenant isolation**: All queries include `tenant_id`
2. **File-based caching**: Responses cached to prevent re-processing
3. **Structured output**: Zod schema validation
4. **Error handling**: Graceful failures with meaningful messages
5. **React Query integration**: Optimistic updates and cache invalidation
