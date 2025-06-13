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