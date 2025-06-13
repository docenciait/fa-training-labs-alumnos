# Securizando los Websockets con OAuth2

!!! Warning Totalmente Inseguro!!!

```python
@app.websocket("/secured-ws")
async def secured_websocket(websocket: WebSocket, username: str):
        await websocket.accept()
        await websocket.send_text(f"Welcome {username}!")
        async for data in websocket.iter_text():
            await websocket.send_text(
             f"You wrote: {data}"
            )
```

- El punto de conexión aceptará cualquier conexión con un parámetro para especificar el nombre de usuario. Luego, enviará un mensaje de bienvenida al cliente y devolverá cada mensaje recibido al cliente.

- El punto de conexión es inseguro ya que no tiene ninguna protección y se puede acceder fácilmente a él. 

# **Cómo hacerlo…**

A fecha de hoy, la clase `OAuth2PasswordBearer` no es compatible con WebSocket en FastAPI. Esto significa que verificar el token *bearer* en las cabeceras para una conexión WebSocket no es tan directo como lo es para las llamadas HTTP. Sin embargo, podemos crear una clase específica para WebSocket.

```python
from fastapi import (
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.security import OAuth2PasswordBearer

class OAuth2WebSocketPasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, websocket: WebSocket) -> str:
        authorization: str = websocket.headers.get("authorization")
        if not authorization:
            raise WebSocketException(
                code=status.HTTP_401_UNAUTHORIZED,
                reason="Not authenticated",
            )
        
        scheme, param = authorization.split()
        if scheme.lower() != "bearer":
            raise WebSocketException(
                code=status.HTTP_403_FORBIDDEN,
                reason="Invalid authentication credentials",
            )
            
        return param
```
