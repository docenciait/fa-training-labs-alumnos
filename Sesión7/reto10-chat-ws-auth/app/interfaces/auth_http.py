
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"

router = APIRouter()

users_db = {
    "user1": {"password": "pass1", "role": "user"},
    "admin": {"password": "adminpass", "role": "admin"},
}

class LoginData(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginData):
    user = users_db.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": data.username, "role": user["role"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}
