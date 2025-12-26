"""
Grey Haven LLM Pipeline Template - Python

Copy this template and customize for your use case.

Usage:
1. Copy to app/pipelines/your_pipeline.py
2. Define your input/output models
3. Implement the abstract methods
4. Create API route or service integration
"""

from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import TypeVar, Generic
from uuid import UUID
import re
import json

from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from anthropic import Anthropic

# ============================================================================
# 1. DEFINE YOUR OUTPUT MODEL
# ============================================================================

class YourOutput(BaseModel):
    """Parsed output from LLM."""
    summary: str
    category: str = Field(pattern="^(type_a|type_b|type_c)$")
    confidence: float = Field(ge=0.0, le=1.0)
    # Add more fields as needed


# ============================================================================
# 2. DEFINE YOUR INPUT MODEL (or use SQLModel)
# ============================================================================

class YourInput(BaseModel):
    """Input data structure."""
    id: UUID
    tenant_id: UUID
    title: str
    content: str
    # Add your input fields


# ============================================================================
# 3. BASE PIPELINE CLASS (Don't modify)
# ============================================================================

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class BasePipeline(ABC, Generic[TInput, TOutput]):
    """Base class for LLM pipelines with file-based caching."""

    def __init__(
        self,
        tenant_id: str,
        cache_dir: Path | None = None,
        model: str = "claude-sonnet-4-20250514"
    ):
        self.tenant_id = tenant_id
        self.model = model
        self.client = Anthropic()
        self.cache_dir = cache_dir or Path(".cache") / "pipelines" / tenant_id

    @abstractmethod
    async def acquire(self, item_id: str) -> TInput:
        """Stage 1: Get input data from database."""
        pass

    @abstractmethod
    def prepare(self, input_data: TInput) -> str:
        """Stage 2: Format prompt for LLM."""
        pass

    @abstractmethod
    def parse(self, response: str) -> TOutput:
        """Stage 4: Parse LLM response."""
        pass

    @abstractmethod
    async def render(self, item_id: str, output: TOutput) -> TOutput:
        """Stage 5: Save output to database."""
        pass

    async def process(self, prompt: str, cache_key: str) -> str:
        """Stage 3: Call LLM with file-based caching."""
        cache_path = self.cache_dir / f"{cache_key}.json"

        # Check cache
        if cache_path.exists():
            cached = json.loads(cache_path.read_text())
            print(f"[cache hit] {cache_key}")
            return cached["response"]

        # Call LLM
        print(f"[llm call] {cache_key} using {self.model}")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text

        # Cache response
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({
            "response": text,
            "model": self.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "timestamp": datetime.utcnow().isoformat(),
        }))

        return text

    async def run(self, item_id: str) -> TOutput:
        """Execute full pipeline."""
        input_data = await self.acquire(item_id)
        prompt = self.prepare(input_data)
        response = await self.process(prompt, item_id)
        output = self.parse(response)
        return await self.render(item_id, output)

    async def run_batch(self, item_ids: list[str]) -> dict[str, TOutput]:
        """Run pipeline for multiple items."""
        results = {}
        for item_id in item_ids:
            try:
                output = await self.run(item_id)
                results[item_id] = output
            except Exception as e:
                print(f"[error] {item_id}: {e}")
        return results


# ============================================================================
# 4. YOUR PIPELINE IMPLEMENTATION
# ============================================================================

# TODO: Import your SQLModel
# from app.models.your_model import YourModel


class YourPipeline(BasePipeline[YourInput, YourOutput]):
    """Your custom pipeline implementation."""

    def __init__(self, tenant_id: str, db: AsyncSession, **kwargs):
        super().__init__(tenant_id, **kwargs)
        self.db = db

    async def acquire(self, item_id: str) -> YourInput:
        """Stage 1: Get input data from database."""
        # TODO: Replace with your model and table
        result = await self.db.execute(
            select(YourModel).where(
                YourModel.tenant_id == self.tenant_id,
                YourModel.id == item_id
            )
        )
        item = result.scalar_one_or_none()

        if not item:
            raise ValueError(
                f"Item {item_id} not found for tenant {self.tenant_id}"
            )

        return item

    def prepare(self, input_data: YourInput) -> str:
        """Stage 2: Format prompt for LLM."""
        # TODO: Customize your prompt
        return f"""Analyze this content.

TITLE: {input_data.title}

CONTENT:
{input_data.content}

I will parse this programmatically. Respond with valid JSON:
{{
  "summary": "Brief summary (1-2 sentences)",
  "category": "type_a" | "type_b" | "type_c",
  "confidence": 0.0 to 1.0
}}

Ensure JSON is complete and parseable."""

    def parse(self, response: str) -> YourOutput:
        """Stage 4: Parse LLM response."""
        match = re.search(r'\{[\s\S]*\}', response)
        if not match:
            raise ValueError("No JSON found in response")

        try:
            return YourOutput.model_validate_json(match.group())
        except Exception as e:
            raise ValueError(f"Failed to parse response: {e}")

    async def render(self, item_id: str, output: YourOutput) -> YourOutput:
        """Stage 5: Save output to database."""
        # TODO: Replace with your update query
        await self.db.execute(
            update(YourModel)
            .where(
                YourModel.tenant_id == self.tenant_id,
                YourModel.id == item_id
            )
            .values(
                summary=output.summary,
                category=output.category,
                processed_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        )
        await self.db.commit()

        return output


# ============================================================================
# 5. FACTORY FUNCTION
# ============================================================================

def create_your_pipeline(
    tenant_id: str,
    db: AsyncSession,
    model: str | None = None
) -> YourPipeline:
    """Create pipeline instance."""
    kwargs = {}
    if model:
        kwargs["model"] = model
    return YourPipeline(tenant_id, db, **kwargs)


# ============================================================================
# 6. USAGE EXAMPLE
# ============================================================================

"""
# In API route:
from app.pipelines.your_pipeline import create_your_pipeline

@router.post("/items/{item_id}/process")
async def process_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
):
    pipeline = create_your_pipeline(str(tenant.id), db)
    result = await pipeline.run(str(item_id))
    return {"success": True, "result": result.model_dump()}


# Batch processing:
@router.post("/items/process-batch")
async def process_items_batch(
    item_ids: list[UUID],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
):
    async def process():
        pipeline = create_your_pipeline(str(tenant.id), db)
        await pipeline.run_batch([str(id) for id in item_ids])

    background_tasks.add_task(process)
    return {"success": True, "queued": len(item_ids)}
"""
