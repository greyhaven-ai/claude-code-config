# FastAPI Setup

**Complete main application configuration.**

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Grey Haven API",
    description="RESTful API for multi-tenant SaaS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True)

# Exception handlers (see error-handlers.md)
# app.add_exception_handler(...)

# Include routers
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Doppler config:** `doppler run --config dev -- uvicorn app.main:app --reload`
