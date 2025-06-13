
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SECRET_KEY = "secret"
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # solo para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base ficticia de usuarios
users_db = {
    "user1": "pass1",
    "admin": "adminpass"
}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    if data.username in users_db and users_db[data.username] == data.password:
        token = jwt.encode({"sub": data.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token}
    return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

async def get_current_user_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        await websocket.close(code=1008)
        return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user = await get_current_user_ws(websocket)
    if not user:
        return
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{user} says: {data}")
    except WebSocketDisconnect:
        print(f"{user} disconnected.")
