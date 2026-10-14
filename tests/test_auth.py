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