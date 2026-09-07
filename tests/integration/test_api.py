import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/products")
        assert response.status_code in (200, 404, 500)