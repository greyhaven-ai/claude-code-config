# Example: OpenAPI 3.1 Generation from FastAPI Codebase

Complete workflow showing automatic OpenAPI specification generation from a FastAPI codebase with Pydantic v2 models.

## Context

**Project**: E-commerce API (FastAPI + Pydantic v2 + SQLModel)
**Problem**: Manual API documentation was 3 months out of date, causing integration failures for 2 partner teams
**Goal**: Generate comprehensive OpenAPI 3.1 spec automatically from code with multi-language examples

**Initial State**:
- 47 API endpoints with no documentation
- 12 integration issues per week from stale documentation
- Manual doc updates taking 4+ hours per release
- Partners blocked waiting for updated contracts

## Step 1: Pydantic v2 Models with Rich Schemas

```python
# app/models/orders.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str = Field(..., description="Product identifier")
    quantity: int = Field(..., gt=0, description="Quantity to order")
    unit_price: float = Field(..., gt=0, description="Price per unit in USD")

class OrderCreate(BaseModel):
    """Create a new order for the authenticated user."""
    items: List[OrderItem] = Field(..., min_length=1, description="Order line items")
    shipping_address_id: str = Field(..., description="ID of shipping address")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "items": [{"product_id": "prod_123", "quantity": 2, "unit_price": 29.99}],
                "shipping_address_id": "addr_456"
            }]
        }
    }

class Order(BaseModel):
    """Order with calculated totals."""
    id: str
    user_id: str
    items: List[OrderItem]
    subtotal: float = Field(..., description="Sum of all item prices")
    tax: float = Field(..., description="Calculated tax amount")
    total: float = Field(..., description="Final order total")
    status: str = Field(..., description="pending, processing, shipped, delivered, cancelled")
    created_at: datetime
```

## Step 2: Enhanced OpenAPI Generation

```python
# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title="Grey Haven E-Commerce API",
        version="1.0.0",
        description="E-commerce API with JWT auth. Rate limit: 1000 req/hour (authenticated).",
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token from /auth/login"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    # Add error response schema
    openapi_schema["components"]["schemas"]["ErrorResponse"] = {
        "type": "object",
        "required": ["error", "message"],
        "properties": {
            "error": {"type": "string", "example": "INSUFFICIENT_STOCK"},
            "message": {"type": "string", "example": "Product has insufficient stock"},
            "details": {"type": "object", "additionalProperties": True}
        }
    }
    
    # Add rate limit headers
    openapi_schema["components"]["headers"] = {
        "X-RateLimit-Limit": {"description": "Request limit per hour", "schema": {"type": "integer"}},
        "X-RateLimit-Remaining": {"description": "Remaining requests", "schema": {"type": "integer"}},
        "X-RateLimit-Reset": {"description": "Reset timestamp", "schema": {"type": "integer"}}
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

## Step 3: FastAPI Route with Complete Documentation

```python
# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.post("/", response_model=Order, status_code=201)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Order:
    """
    Create a new order for the authenticated user.
    
    The order will be created in 'pending' status and total calculated
    including applicable taxes based on shipping address.
    
    **Requires**:
    - Valid JWT authentication token
    - At least one item in the order
    - Valid shipping address ID owned by the user
    
    **Returns**: Created order with calculated totals
    
    **Raises**:
    - **401 Unauthorized**: If user is not authenticated
    - **404 Not Found**: If shipping address not found
    - **400 Bad Request**: If product stock insufficient or validation fails
    - **429 Too Many Requests**: If rate limit exceeded
    """
    # Validate shipping address belongs to user
    address = session.get(ShippingAddress, order_data.shipping_address_id)
    if not address or address.user_id != current_user.id:
        raise HTTPException(404, detail="Shipping address not found")
    
    # Check stock availability
    for item in order_data.items:
        product = session.get(Product, item.product_id)
        if not product or product.stock < item.quantity:
            raise HTTPException(
                400,
                detail={
                    "error": "INSUFFICIENT_STOCK",
                    "message": f"Product {item.product_id} has insufficient stock",
                    "details": {
                        "product_id": item.product_id,
                        "requested": item.quantity,
                        "available": product.stock if product else 0
                    }
                }
            )
    
    # Create order and calculate totals
    order = Order(
        user_id=current_user.id,
        items=order_data.items,
        subtotal=sum(item.quantity * item.unit_price for item in order_data.items)
    )
    order.tax = order.subtotal * 0.08  # 8% tax
    order.total = order.subtotal + order.tax
    order.status = "pending"
    
    session.add(order)
    session.commit()
    return order
```

## Step 4: Multi-Language Code Examples

### Automated Example Generation

```python
# scripts/generate_examples.py
def generate_examples(openapi_spec):
    """Generate TypeScript, Python, and cURL examples for each endpoint."""
    
    examples = {}
    
    for path, methods in openapi_spec["paths"].items():
        for method, details in methods.items():
            operation_id = details.get("operationId", f"{method}_{path}")
            
            # TypeScript example
            examples[f"{operation_id}_typescript"] = f'''
const response = await fetch('https://api.greyhaven.com{path}', {{
  method: '{method.upper()}',
  headers: {{
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
  }},
  body: JSON.stringify({{
    items: [{{ product_id: "prod_123", quantity: 2, unit_price: 29.99 }}],
    shipping_address_id: "addr_456"
  }})
}});
const order = await response.json();
'''
            
            # Python example
            examples[f"{operation_id}_python"] = f'''
import requests

response = requests.{method}(
    'https://api.greyhaven.com{path}',
    headers={{'Authorization': 'Bearer YOUR_API_TOKEN'}},
    json={{
        'items': [{{'product_id': 'prod_123', 'quantity': 2, 'unit_price': 29.99}}],
        'shipping_address_id': 'addr_456'
    }}
)
order = response.json()
'''
            
            # cURL example
            examples[f"{operation_id}_curl"] = f'''
curl -X {method.upper()} https://api.greyhaven.com{path} \\
  -H "Authorization: Bearer YOUR_API_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{{"items": [{{"product_id": "prod_123", "quantity": 2, "unit_price": 29.99}}], "shipping_address_id": "addr_456"}}'
'''
    
    return examples
```

## Step 5: Interactive Swagger UI

```python
# app/main.py (enhanced)
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "persistAuthorization": True,  # Remember auth token
            "displayRequestDuration": True,  # Show request timing
            "filter": True,  # Enable filtering
            "tryItOutEnabled": True  # Enable try-it-out by default
        }
    )
```

## Step 6: CI/CD Auto-Generation

```yaml
# .github/workflows/generate-docs.yml
name: Generate API Documentation

on:
  push:
    branches: [main]
    paths: ['app/**/*.py']

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Generate OpenAPI spec
        run: |
          pip install -r requirements.txt
          python -c "
          from app.main import app
          import json
          with open('docs/openapi.json', 'w') as f:
              json.dump(app.openapi(), f, indent=2)
          "
      
      - name: Generate code examples
        run: python scripts/generate_examples.py
      
      - name: Validate OpenAPI
        run: npx @redocly/cli lint docs/openapi.json
      
      - name: Deploy to Cloudflare Pages
        run: |
          npm install -g wrangler
          wrangler pages deploy docs/ --project-name=api-docs
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

## Generated OpenAPI Specification (Excerpt)

```yaml
openapi: 3.1.0
info:
  title: Grey Haven E-Commerce API
  version: 1.0.0
  description: E-commerce API with JWT auth. Rate limit: 1000 req/hour.

servers:
  - url: https://api.greyhaven.com
    description: Production

paths:
  /api/v1/orders:
    post:
      summary: Create a new order
      description: Create order in 'pending' status with calculated totals
      operationId: createOrder
      tags: [orders]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderCreate'
      responses:
        '201':
          description: Order created successfully
          headers:
            X-RateLimit-Limit:
              $ref: '#/components/headers/X-RateLimit-Limit'
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: Validation error or insufficient stock
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '401':
          description: Unauthorized (invalid token)
        '429':
          description: Rate limit exceeded

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  
  schemas:
    OrderItem:
      type: object
      required: [product_id, quantity, unit_price]
      properties:
        product_id:
          type: string
          example: "prod_123"
        quantity:
          type: integer
          minimum: 1
          example: 2
        unit_price:
          type: number
          minimum: 0.01
          example: 29.99
```

## Results

### Before

- Manual documentation 3 months out of date
- 47 endpoints with no docs
- 12 integration issues per week
- 4+ hours manual doc updates per release
- Partners blocked waiting for updated contracts

### After

- OpenAPI spec auto-generated on every commit
- 100% endpoint coverage with examples
- Interactive Swagger UI with try-it-out
- Multi-language examples (TypeScript, Python, cURL)
- Complete error response documentation

### Improvements

- Integration issues: 12/week → 0.5/week (96% reduction)
- Doc update time: 4 hours → 0 minutes (automated)
- Partner satisfaction: 45% → 98%
- Time-to-integration: 2 weeks → 2 days

### Partner Feedback

- "The interactive docs with try-it-out saved us days of testing"
- "Code examples in our language made integration trivial"
- "Error responses are fully documented - no guesswork"

## Key Lessons

1. **Automation is Critical**: Manual docs will always drift from code
2. **Pydantic v2 Schema**: Excellent OpenAPI generation with field validators
3. **Multi-Language Examples**: Dramatically improved partner integration speed
4. **Interactive Docs**: Try-it-out functionality reduced support tickets
5. **CI/CD Integration**: Documentation stays current automatically
6. **Error Documentation**: Complete error schemas eliminated guesswork

## Prevention Measures

**Implemented**:
- [x] Auto-generation on every commit (GitHub Actions)
- [x] OpenAPI spec validation in CI/CD
- [x] Interactive Swagger UI deployed to Cloudflare Pages
- [x] Multi-language code examples generated
- [x] Complete error response schemas
- [x] Rate limiting documentation

**Ongoing**:
- [ ] SDK auto-generation from OpenAPI spec (TypeScript, Python clients)
- [ ] Contract testing (validate API matches OpenAPI spec)
- [ ] Changelog generation from git commits

---

Related: [architecture-docs.md](architecture-docs.md) | [coverage-validation.md](coverage-validation.md) | [Return to INDEX](INDEX.md)
