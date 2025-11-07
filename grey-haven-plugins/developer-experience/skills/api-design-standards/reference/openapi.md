# OpenAPI Customization

**Custom OpenAPI schema with security.**

```python
def custom_openapi(app):
    openapi_schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    return openapi_schema

app.openapi = lambda: custom_openapi(app)
```

Access docs at `/docs` (Swagger UI) or `/redoc` (ReDoc).
