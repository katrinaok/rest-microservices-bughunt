import os
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

app = FastAPI(title="OrderService")

AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8000")
PRODUCT_URL = os.getenv("PRODUCT_URL", "http://product-service:8000")

ORDERS: list[dict] = []

# 1. Pydantic-схема для узгодженого контракту
class OrderRequest(BaseModel):
    productId: int
    qty: int

@app.post("/orders")
async def create_order(payload: OrderRequest, authorization: str | None = Header(default=None)):
    
    # 2. ВИПРАВЛЕНО: Перевіряємо статус авторизації
    async with httpx.AsyncClient() as client:
        auth_resp = await client.get(f"{AUTH_URL}/whoami", headers={"Authorization": authorization or ""})
        if auth_resp.status_code != 200:
            return JSONResponse({"error": "unauthorized"}, status_code=401)
            
    # 3. ВИПРАВЛЕНО: Запитуємо інформацію про товар
    async with httpx.AsyncClient() as client:
        prod_resp = await client.get(f"{PRODUCT_URL}/products/{payload.productId}")
        
        # Якщо товару не існує
        if prod_resp.status_code == 404:
            return JSONResponse({"error": "product not found"}, status_code=404)
            
        product_data = prod_resp.json()
        
        # Якщо товару недостатньо на складі
        if product_data.get("inStock", 0) < payload.qty:
            return JSONResponse({"error": "not enough stock"}, status_code=400)

    # 4. Тільки якщо всі перевірки пройдено — створюємо замовлення
    order = {  
        "order_id": len(ORDERS) + 1,  
        "product_id": payload.productId,  
        "quantity": payload.qty,  
        "status": "created",  
    }  
    ORDERS.append(order)  
    
    return JSONResponse(order, status_code=201)

@app.get("/orders")
async def list_orders():
    return {"orders": ORDERS}