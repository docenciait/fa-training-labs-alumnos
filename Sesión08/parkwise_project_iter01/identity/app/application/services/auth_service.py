from app.application.ports.inbound.auth_service_port import AuthServicePort
from app.application.ports.outbound.user_repository_port import UserRepositoryPort
from app.domain.services.user_hasher import UserHasher
from app.domain.models.user import User

from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")

class AuthService(AuthServicePort):
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def register(self, username: str, password: str, role: str) -> User:
        hashed = UserHasher.hash_password(password)
        user = User(id=None, username=username, password=hashed, role=role)
        return self.user_repo.save(user)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(username)
        if not user or not UserHasher.verify_password(password, user.password):
            raise Exception("Invalid credentials")
        return jwt.encode({"sub": user.username, "role": user.role}, SECRET_KEY, algorithm="HS256")
