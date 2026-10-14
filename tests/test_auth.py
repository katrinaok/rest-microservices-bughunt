import httpx
import pytest

BASE_URL = "http://localhost:8001"

@pytest.mark.asyncio
async def test_login_should_be_post():
    payload = {"email": "alice@example.com", "password": "alice123"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/login", json=payload)

    assert response.status_code == 200, "Login endpoint must accept POST requests!"
    assert "accessToken" in response.json()

@pytest.mark.asyncio
async def test_whoami_unauthorized_should_return_401():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/whoami")
    
    assert response.status_code == 401, "Endpoint /whoami must return 401 Unauthorized when token is missing!"