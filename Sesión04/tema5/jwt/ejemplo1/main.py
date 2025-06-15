from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
from auth import (
    create_access_token, create_refresh_token,
    get_current_user, verify_password, get_password_hash,
    refresh_tokens_db, verify_refresh_token
)

app = FastAPI()

# --- Base de datos simulada ---
fake_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": get_password_hash("password123"),
        "roles": ["user"]
    },
    "admin1": {
        "username": "admin1",
        "hashed_password": get_password_hash("adminpass456"),
        "roles": ["admin", "user"]
    }
}


# --- Modelos Pydantic ---
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str


# --- Endpoints ---
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Crear tokens
    access_token = create_access_token(data={"sub": user["username"], "roles": user["roles"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    
    # Guardar refresh token válido
    refresh_tokens_db[user["username"]] = refresh_token

    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/refresh", response_model=Token)
async def refresh_token(refresh_request: RefreshTokenRequest):
    payload = verify_refresh_token(refresh_request.refresh_token)
    username = payload.get("sub")

    # Verificar que esté en la "DB"
    stored_refresh_token = refresh_tokens_db.get(username)
    if stored_refresh_token != refresh_request.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token invalid or revoked")
    
    # Crear nuevos tokens
    access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})

    # Actualizar refresh token en "DB"
    refresh_tokens_db[username] = new_refresh_token

    return {"access_token": access_token, "refresh_token": new_refresh_token}


@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Devuelve el usuario actual basado en el access token."""
    return {"user": current_user}


@app.post("/logout")
async def logout(logout_request: LogoutRequest):
    """Invalida el refresh token del usuario."""
    payload = verify_refresh_token(logout_request.refresh_token)
    username = payload.get("sub")

    stored_refresh_token = refresh_tokens_db.get(username)
    if stored_refresh_token == logout_request.refresh_token:
        # Revocar el refresh token
        del refresh_tokens_db[username]
        return {"detail": "Logged out successfully"}
    
    raise HTTPException(status_code=401, detail="Invalid refresh token")

if __name__ == "__main__":


    uvicorn.run(app, host="0.0.0.0", port=8000)