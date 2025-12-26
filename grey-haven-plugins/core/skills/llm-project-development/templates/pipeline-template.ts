/**
 * Grey Haven LLM Pipeline Template - TypeScript
 *
 * Copy this template and customize for your use case.
 *
 * Usage:
 * 1. Copy to lib/pipelines/your-pipeline.ts
 * 2. Define your input/output types
 * 3. Implement the abstract methods
 * 4. Create API route or service integration
 */

import { existsSync, mkdirSync, writeFileSync, readFileSync } from "fs";
import { join } from "path";
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { db } from "@/db";
import { eq, and } from "drizzle-orm";

// ============================================================================
// 1. DEFINE YOUR OUTPUT SCHEMA
// ============================================================================

const YourOutputSchema = z.object({
  // Define your expected output structure
  summary: z.string(),
  category: z.enum(["type_a", "type_b", "type_c"]),
  confidence: z.number().min(0).max(1),
  // Add more fields as needed
});

type YourOutput = z.infer<typeof YourOutputSchema>;

// ============================================================================
// 2. DEFINE YOUR INPUT TYPE
// ============================================================================

interface YourInput {
  id: string;
  tenant_id: string;
  // Add your input fields
  title: string;
  content: string;
}

// ============================================================================
// 3. BASE PIPELINE CLASS (Don't modify)
// ============================================================================

abstract class BasePipeline<TInput, TOutput> {
  protected client: Anthropic;
  protected cacheDir: string;
  protected tenantId: string;
  protected model: string;

  constructor(
    tenantId: string,
    options: { cacheDir?: string; model?: string } = {}
  ) {
    this.tenantId = tenantId;
    this.client = new Anthropic();
    this.model = options.model || "claude-sonnet-4-20250514";
    this.cacheDir =
      options.cacheDir ||
      join(process.cwd(), ".cache", "pipelines", tenantId);
  }

  abstract acquire(id: string): Promise<TInput>;
  abstract prepare(input: TInput): string;
  abstract parse(response: string): TOutput;
  abstract render(id: string, output: TOutput): Promise<TOutput>;

  protected async process(prompt: string, cacheKey: string): Promise<string> {
    const cachePath = join(this.cacheDir, `${cacheKey}.json`);

    if (existsSync(cachePath)) {
      console.log(`[cache hit] ${cacheKey}`);
      return JSON.parse(readFileSync(cachePath, "utf-8")).response;
    }

    console.log(`[llm call] ${cacheKey}`);
    const response = await this.client.messages.create({
      model: this.model,
      max_tokens: 1024,
      messages: [{ role: "user", content: prompt }],
    });

    const text =
      response.content[0].type === "text" ? response.content[0].text : "";

    mkdirSync(this.cacheDir, { recursive: true });
    writeFileSync(
      cachePath,
      JSON.stringify({
        response: text,
        model: this.model,
        input_tokens: response.usage.input_tokens,
        output_tokens: response.usage.output_tokens,
        timestamp: new Date().toISOString(),
      })
    );

    return text;
  }

  async run(id: string): Promise<TOutput> {
    const input = await this.acquire(id);
    const prompt = this.prepare(input);
    const response = await this.process(prompt, id);
    const output = this.parse(response);
    return await this.render(id, output);
  }

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

// ============================================================================
// 4. YOUR PIPELINE IMPLEMENTATION
// ============================================================================

export class YourPipeline extends BasePipeline<YourInput, YourOutput> {
  /**
   * Stage 1: Acquire input data from database
   */
  async acquire(itemId: string): Promise<YourInput> {
    // TODO: Replace with your table/query
    const item = await db.query.yourTable.findFirst({
      where: and(
        eq(yourTable.tenant_id, this.tenantId),
        eq(yourTable.id, itemId)
      ),
    });

    if (!item) {
      throw new Error(`Item ${itemId} not found for tenant ${this.tenantId}`);
    }

    return item;
  }

  /**
   * Stage 2: Prepare prompt for LLM
   */
  prepare(input: YourInput): string {
    // TODO: Customize your prompt
    return `Analyze this content.

TITLE: ${input.title}

CONTENT:
${input.content}

I will parse this programmatically. Respond with valid JSON:
{
  "summary": "Brief summary (1-2 sentences)",
  "category": "type_a" | "type_b" | "type_c",
  "confidence": 0.0 to 1.0
}

Ensure JSON is complete and parseable.`;
  }

  /**
   * Stage 4: Parse LLM response
   */
  parse(response: string): YourOutput {
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error("No JSON found in response");
    }

    try {
      const parsed = JSON.parse(jsonMatch[0]);
      return YourOutputSchema.parse(parsed);
    } catch (error) {
      throw new Error(`Failed to parse response: ${error}`);
    }
  }

  /**
   * Stage 5: Render/save output to database
   */
  async render(itemId: string, output: YourOutput): Promise<YourOutput> {
    // TODO: Replace with your update query
    await db
      .update(yourTable)
      .set({
        summary: output.summary,
        category: output.category,
        processed_at: new Date(),
        updated_at: new Date(),
      })
      .where(
        and(eq(yourTable.tenant_id, this.tenantId), eq(yourTable.id, itemId))
      );

    return output;
  }
}

// ============================================================================
// 5. FACTORY FUNCTION
// ============================================================================

export function createYourPipeline(
  tenantId: string,
  options?: { model?: string }
) {
  return new YourPipeline(tenantId, options);
}

// ============================================================================
// 6. USAGE EXAMPLE
// ============================================================================

/*
// In API route or server function:
import { createYourPipeline } from "@/lib/pipelines/your-pipeline";

export async function processItem(tenantId: string, itemId: string) {
  const pipeline = createYourPipeline(tenantId);
  return await pipeline.run(itemId);
}

// Batch processing:
export async function processItems(tenantId: string, itemIds: string[]) {
  const pipeline = createYourPipeline(tenantId);
  return await pipeline.runBatch(itemIds);
}
*/
