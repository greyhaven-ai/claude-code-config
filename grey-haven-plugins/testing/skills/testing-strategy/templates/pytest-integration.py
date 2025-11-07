# tests/integration/test_FEATURE_api.py
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.integration
class TestYourAPI:
    """Integration tests for Your API endpoints."""

    async def test_create_endpoint(self, client: AsyncClient, tenant_id):
        """Test POST /api/YOUR_RESOURCE creates resource."""
        response = await client.post(
            "/api/YOUR_RESOURCE",
            json={
                "name": "Test Resource",
                "description": "Test description",
            },
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Resource"
        assert data["tenant_id"] == str(tenant_id)

    async def test_get_endpoint(self, client: AsyncClient, tenant_id, test_resource):
        """Test GET /api/YOUR_RESOURCE/{id} retrieves resource."""
        response = await client.get(
            f"/api/YOUR_RESOURCE/{test_resource.id}",
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_resource.id)
        assert data["name"] == test_resource.name

    async def test_get_enforces_tenant_isolation(
        self, client: AsyncClient, tenant_id, test_resource
    ):
        """Test GET enforces tenant isolation."""
        # Should succeed with correct tenant
        response = await client.get(
            f"/api/YOUR_RESOURCE/{test_resource.id}",
            headers={"X-Tenant-ID": str(tenant_id)},
        )
        assert response.status_code == 200

        # Should fail with different tenant
        different_tenant = str(uuid4())
        response = await client.get(
            f"/api/YOUR_RESOURCE/{test_resource.id}",
            headers={"X-Tenant-ID": different_tenant},
        )
        assert response.status_code == 404

    async def test_list_endpoint(self, client: AsyncClient, tenant_id):
        """Test GET /api/YOUR_RESOURCE lists resources."""
        response = await client.get(
            "/api/YOUR_RESOURCE",
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_update_endpoint(
        self, client: AsyncClient, tenant_id, test_resource
    ):
        """Test PATCH /api/YOUR_RESOURCE/{id} updates resource."""
        response = await client.patch(
            f"/api/YOUR_RESOURCE/{test_resource.id}",
            json={"name": "Updated Name"},
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    async def test_delete_endpoint(
        self, client: AsyncClient, tenant_id, test_resource
    ):
        """Test DELETE /api/YOUR_RESOURCE/{id} deletes resource."""
        response = await client.delete(
            f"/api/YOUR_RESOURCE/{test_resource.id}",
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 204

        # Verify deletion
        response = await client.get(
            f"/api/YOUR_RESOURCE/{test_resource.id}",
            headers={"X-Tenant-ID": str(tenant_id)},
        )
        assert response.status_code == 404

    async def test_validation_errors(self, client: AsyncClient, tenant_id):
        """Test endpoint validates input correctly."""
        response = await client.post(
            "/api/YOUR_RESOURCE",
            json={
                "name": "",  # Invalid: empty name
            },
            headers={"X-Tenant-ID": str(tenant_id)},
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
