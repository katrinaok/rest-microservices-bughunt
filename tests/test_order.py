import httpx
import pytest

BASE_URL = "http://localhost:8003"

@pytest.mark.asyncio
async def test_create_order_with_invalid_token_fails():
    # Перевірка 1: Ігнорування статусу авторизації
    headers = {"Authorization": "Bearer invalid-token-123"}
    payload = {"productId": 100, "qty": 1}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/orders", json=payload, headers=headers)
    
    # Сервіс має повернути 401, але зараз він ігнорує помилку і повертає 201 Created
    assert response.status_code == 401, "Order service must reject invalid tokens"

@pytest.mark.asyncio
async def test_create_order_out_of_stock_fails():
    # Перевірка 2: Ігнорування наявності товару (ID 101 має inStock: 0)
    headers = {"Authorization": "Bearer fake-token-for-alice@example.com"}
    payload = {"productId": 101, "qty": 1}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/orders", json=payload, headers=headers)
    
    # Сервіс має повернути 400 Bad Request, але зараз він продає "повітря" (201)
    assert response.status_code == 400, "Order service must check product stock"