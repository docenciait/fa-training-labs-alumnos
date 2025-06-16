from typing import Protocol
from app.domain.models.user import User


class AuthServicePort(Protocol):
    def register(self, username: str, password: str, role: str) -> User: ...
    def login(self, username: str, password: str) -> str: ...
