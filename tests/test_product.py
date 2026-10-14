import httpx
import pytest

BASE_URL = "http://localhost:8002"

@pytest.mark.asyncio
async def test_get_nonexistent_product_should_return_404():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products/9999")
    
    assert response.status_code == 404, "Endpoint must return 404 Not Found for invalid product ID"