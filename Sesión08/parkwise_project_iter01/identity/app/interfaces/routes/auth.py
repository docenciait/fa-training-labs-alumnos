from fastapi import APIRouter, Depends, HTTPException
from app.application.services.auth_service import AuthService
from app.infrastructure.repositories.user_repository import InMemoryUserRepository
from app.interfaces.schemas.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.interfaces.dependencies.jwt_auth import get_current_user, require_role
from fastapi import Depends



router = APIRouter()
auth_service = AuthService(user_repo=InMemoryUserRepository())

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest):
    user = auth_service.register(data.username, data.password, data.role)
    token = auth_service.login(user.username, data.password)
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    try:
        token = auth_service.login(data.username, data.password)
        return TokenResponse(access_token=token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return {"username": user["sub"], "role": user["role"]}

@router.get("/admin-only")
def admin_endpoint(user: dict = Depends(require_role("admin"))):
    return {"message": f"Hello admin {user['sub']}!"}