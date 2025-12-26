# FastAPI Pipeline Example

Complete example of an LLM pipeline in a Grey Haven FastAPI backend.

## Use Case: Support Ticket Classification

Automatically classify incoming support tickets by urgency, category, and suggest responses.

## Directory Structure

```
app/
├── pipelines/
│   ├── __init__.py
│   ├── base.py                    # Base pipeline class
│   └── ticket_classifier.py       # Implementation
├── models/
│   └── ticket.py                  # SQLModel schema
├── api/
│   └── routes/
│       └── tickets.py             # API endpoints
└── services/
    └── ticket_service.py          # Business logic
```

## Implementation

### 1. SQLModel Schema

```python
# app/models/ticket.py
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)

    # Input fields
    subject: str = Field(max_length=255)
    body: str = Field()
    customer_email: str = Field(max_length=255)

    # LLM-classified fields
    urgency: Optional[str] = Field(default=None)  # critical|high|medium|low
    category: Optional[str] = Field(default=None)
    suggested_response: Optional[str] = Field(default=None)
    classification_confidence: Optional[float] = Field(default=None)
    classified_at: Optional[datetime] = Field(default=None)

    # Standard fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. Base Pipeline

```python
# app/pipelines/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import TypeVar, Generic
import json
from anthropic import Anthropic

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
```

### 3. Ticket Classifier Implementation

```python
# app/pipelines/ticket_classifier.py
import re
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.pipelines.base import BasePipeline

class Classification(BaseModel):
    """Parsed classification output."""
    urgency: str = Field(pattern="^(critical|high|medium|low)$")
    category: str
    suggested_response: str
    confidence: float = Field(ge=0.0, le=1.0)

class TicketClassifierPipeline(BasePipeline[Ticket, Classification]):
    """Classify support tickets using LLM."""

    def __init__(self, tenant_id: str, db: AsyncSession):
        super().__init__(tenant_id)
        self.db = db

    async def acquire(self, ticket_id: str) -> Ticket:
        """Get ticket from database with tenant isolation."""
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.id == ticket_id
            )
        )
        ticket = result.scalar_one_or_none()

        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found for tenant {self.tenant_id}")

        return ticket

    def prepare(self, ticket: Ticket) -> str:
        """Format classification prompt."""
        return f"""Classify this support ticket for a SaaS customer support system.

SUBJECT: {ticket.subject}

BODY:
{ticket.body}

CUSTOMER: {ticket.customer_email}

I will parse this programmatically. Respond with valid JSON:
{{
  "urgency": "critical" | "high" | "medium" | "low",
  "category": "billing" | "technical" | "account" | "feature_request" | "bug_report" | "other",
  "suggested_response": "A helpful template response (2-3 sentences)",
  "confidence": 0.0 to 1.0 (your confidence in this classification)
}}

Classification guidelines:
- critical: Service down, data loss, security issues
- high: Major feature broken, billing errors
- medium: Feature questions, minor bugs
- low: General inquiries, feature requests

Ensure JSON is complete and parseable."""

    def parse(self, response: str) -> Classification:
        """Parse and validate LLM response."""
        # Extract JSON from response
        match = re.search(r'\{[\s\S]*\}', response)
        if not match:
            raise ValueError("No JSON found in response")

        try:
            return Classification.model_validate_json(match.group())
        except Exception as e:
            raise ValueError(f"Failed to parse classification: {e}")

    async def render(self, ticket_id: str, classification: Classification) -> Classification:
        """Save classification to database."""
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
                classified_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        )
        await self.db.commit()

        return classification

# Factory function
def create_ticket_classifier(tenant_id: str, db: AsyncSession) -> TicketClassifierPipeline:
    return TicketClassifierPipeline(tenant_id, db)
```

### 4. API Routes

```python
# app/api/routes/tickets.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.auth import get_current_tenant
from app.models.ticket import Ticket
from app.pipelines.ticket_classifier import create_ticket_classifier

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/{ticket_id}/classify")
async def classify_ticket(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
):
    """Classify a single ticket using LLM."""
    pipeline = create_ticket_classifier(str(tenant.id), db)

    try:
        classification = await pipeline.run(str(ticket_id))
        return {
            "success": True,
            "ticket_id": str(ticket_id),
            "classification": classification.model_dump(),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {e}")

@router.post("/classify-batch")
async def classify_tickets_batch(
    ticket_ids: list[UUID],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant),
):
    """Queue multiple tickets for classification."""

    async def process_batch():
        pipeline = create_ticket_classifier(str(tenant.id), db)
        await pipeline.run_batch([str(id) for id in ticket_ids])

    background_tasks.add_task(process_batch)

    return {
        "success": True,
        "message": f"Queued {len(ticket_ids)} tickets for classification",
        "ticket_ids": [str(id) for id in ticket_ids],
    }
```

### 5. Service Layer

```python
# app/services/ticket_service.py
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.pipelines.ticket_classifier import create_ticket_classifier

class TicketService:
    def __init__(self, tenant_id: str, db: AsyncSession):
        self.tenant_id = tenant_id
        self.db = db

    async def get_unclassified_tickets(self) -> list[Ticket]:
        """Get all tickets that haven't been classified yet."""
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.classified_at.is_(None)
            ).order_by(Ticket.created_at.desc())
        )
        return list(result.scalars().all())

    async def classify_pending(self) -> dict[str, int]:
        """Classify all pending tickets."""
        tickets = await self.get_unclassified_tickets()

        if not tickets:
            return {"processed": 0, "failed": 0}

        pipeline = create_ticket_classifier(self.tenant_id, self.db)
        results = await pipeline.run_batch([str(t.id) for t in tickets])

        return {
            "processed": len(results),
            "failed": len(tickets) - len(results),
        }

    async def get_classification_stats(self) -> dict:
        """Get classification statistics for dashboard."""
        from sqlalchemy import func

        result = await self.db.execute(
            select(
                Ticket.urgency,
                func.count(Ticket.id).label("count")
            )
            .where(
                Ticket.tenant_id == self.tenant_id,
                Ticket.classified_at.is_not(None)
            )
            .group_by(Ticket.urgency)
        )

        stats = {row.urgency: row.count for row in result.all()}

        return {
            "by_urgency": stats,
            "total_classified": sum(stats.values()),
        }
```

## Testing

```python
# tests/pipelines/test_ticket_classifier.py
import pytest
from app.pipelines.ticket_classifier import TicketClassifierPipeline, Classification

class TestTicketClassifier:
    def test_prepare_prompt(self):
        """Test prompt formatting."""
        pipeline = TicketClassifierPipeline("test-tenant", None)

        class MockTicket:
            subject = "Can't login to my account"
            body = "I've been trying to login but keep getting an error."
            customer_email = "test@example.com"

        prompt = pipeline.prepare(MockTicket())

        assert "Can't login to my account" in prompt
        assert "test@example.com" in prompt
        assert "I will parse this programmatically" in prompt

    def test_parse_valid_json(self):
        """Test parsing valid LLM response."""
        pipeline = TicketClassifierPipeline("test-tenant", None)

        response = '''Here's the classification:
{
  "urgency": "high",
  "category": "technical",
  "suggested_response": "We apologize for the login issue. Please try clearing your browser cache.",
  "confidence": 0.85
}'''

        result = pipeline.parse(response)

        assert result.urgency == "high"
        assert result.category == "technical"
        assert result.confidence == 0.85

    def test_parse_invalid_json(self):
        """Test handling of invalid response."""
        pipeline = TicketClassifierPipeline("test-tenant", None)

        with pytest.raises(ValueError, match="No JSON found"):
            pipeline.parse("This response has no JSON")

    def test_parse_invalid_urgency(self):
        """Test validation of urgency field."""
        pipeline = TicketClassifierPipeline("test-tenant", None)

        response = '{"urgency": "super-urgent", "category": "tech", "suggested_response": "Hi", "confidence": 0.9}'

        with pytest.raises(ValueError):
            pipeline.parse(response)
```

## Key Patterns Demonstrated

1. **Tenant isolation**: All database queries include `tenant_id` filter
2. **Pydantic validation**: Strong typing for classification output
3. **Background tasks**: Batch processing without blocking requests
4. **File-based caching**: Responses cached to `.cache/pipelines/{tenant_id}/`
5. **Service layer**: Business logic separated from API routes
6. **Error handling**: Graceful failures with meaningful HTTP errors
