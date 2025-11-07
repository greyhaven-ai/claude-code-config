# Integration Failure Debug Example

Debugging API integration failures and contract violations.

## Error: 422 Unprocessable Entity from Payment API

```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

## Investigation

### Request Sent

```python
# Our code
await payment_api.create_charge({
    "amount": order.total,  # Sending cents: 0 (empty cart!)
    "currency": "usd",
    "customer_id": "cus_123"
})
```

### API Contract (OpenAPI Spec)

```yaml
/charges:
  post:
    requestBody:
      content:
        application/json:
          schema:
            properties:
              amount:
                type: integer
                minimum: 50  # $0.50 minimum!
```

**Issue**: Sending `amount: 0` violates API's minimum amount requirement.

## Root Cause

Order validation allows empty carts ($0 total). Payment API requires minimum $0.50.

## Fix

```python
from pydantic import BaseModel, validator

class CreateChargeRequest(BaseModel):
    amount: int
    currency: str
    customer_id: str

    @validator('amount')
    def amount_must_meet_minimum(cls, v):
        if v < 50:  # Match API's minimum
            raise ValueError('Amount must be at least $0.50 (50 cents)')
        return v

# Service layer
async def create_charge(order: Order):
    # Validate before API call
    request = CreateChargeRequest(
        amount=order.total_cents,
        currency="usd",
        customer_id=order.customer_id
    )
    return await payment_api.create_charge(request.dict())
```

## Prevention

1. **Schema validation**: Validate against OpenAPI spec
2. **Contract tests**: Test API contract compliance
3. **Integration tests**: Test with real API (or mocks matching spec)

---

**Result**: API contract violations caught at service boundary, not production.
