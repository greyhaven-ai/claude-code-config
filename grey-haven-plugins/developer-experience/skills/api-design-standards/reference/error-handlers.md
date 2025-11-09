# Error Handlers

**Complete exception handler configuration.**

See [../templates/error-handler.py](../templates/error-handler.py) for full implementation.

```python
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail, "status_code": exc.status_code})

async def validation_exception_handler(request, exc):
    errors = [{"field": ".".join(str(loc) for loc in e["loc"]), "message": e["msg"], "code": e["type"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": "Validation error", "detail": errors, "status_code": 422})

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
```
