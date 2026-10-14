from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="ProductService")

# 1. Додаємо Pydantic-схему для узгодженого контракту
class Product(BaseModel):
    product_id: int
    name: str
    price: float  # ВИПРАВЛЕНО: ціна тепер число, а не рядок
    inStock: int

# Оновлюємо каталог згідно зі схемою
PRODUCTS = [
    Product(product_id=100, name="Keyboard", price=59.99, inStock=5),
    Product(product_id=101, name="Mouse", price=29.99, inStock=0),
]

@app.get("/products")
async def list_products():
    return {"items": PRODUCTS}

@app.get("/products/{pid}")
async def get_product(pid: int):
    for p in PRODUCTS:
        if p.product_id == pid:
            return p
    # 2. ВИПРАВЛЕНО: статус-код 404 замість 200
    return JSONResponse({"message": "not found"}, status_code=404)