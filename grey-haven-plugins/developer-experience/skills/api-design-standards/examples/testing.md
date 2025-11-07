# API Testing Examples

**pytest examples for FastAPI endpoints.**

```python
# tests/api/test_users.py
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
def test_create_user(test_token: str):
    response = client.post("/api/v1/users", json={"email": "test@example.com", "full_name": "Test", "password": "Pass123"}, headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 201
    assert "id" in response.json()

@pytest.mark.integration  
def test_tenant_isolation(test_token: str):
    response = client.get(f"/api/v1/users/{other_tenant_user_id}", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 404  # Cannot access other tenant's data
```

Run with: `doppler run --config test -- pytest tests/api/ -v`
