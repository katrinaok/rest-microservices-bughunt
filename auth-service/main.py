from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="AuthService")

USERS = {
    "alice@example.com": {"password": "alice123", "id": 1},
    "bob@example.com": {"password": "bob123", "id": 2},
}

# 1. Створюємо Pydantic-схему для валідації вхідних даних
class LoginRequest(BaseModel):
    email: str
    password: str

# 2. Змінюємо @app.get на @app.post
@app.post("/login")
async def login(payload: LoginRequest):
    user = USERS.get(payload.email)
    
    # 3. Виправляємо статус-код з 200 на правильний 401 (Unauthorized)
    if not user or user["password"] != payload.password:
        return JSONResponse({"message": "invalid credentials"}, status_code=401)
    
    token = f"fake-token-for-{payload.email}"
    return {"accessToken": token, "userId": user["id"]}

@app.get("/whoami")
async def whoami(authorization: str | None = None):
    if not authorization or not authorization.startswith("Bearer"):
        return JSONResponse({"error": "missing or invalid token"}, status_code=200)
    
    token = authorization.removeprefix("Bearer").strip()
    email = token.replace("fake-token-for-", "")
    return {"email": email}