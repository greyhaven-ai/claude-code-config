# CORS and Rate Limiting

**CORS middleware and Upstash Redis rate limiter.**

## CORS

```python
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True)
```

**Doppler:** `CORS_ALLOWED_ORIGINS="https://app.example.com"`

## Rate Limiting

See [../templates/rate-limiter.py](../templates/rate-limiter.py) for full implementation.

```python
from app.core.rate_limit import rate_limit_normal

@router.get("", dependencies=[Depends(rate_limit_normal)])
async def list_users():
    pass  # Rate limited to 100 req/min
```

**Doppler:** `REDIS_URL` must be set for Upstash Redis.
