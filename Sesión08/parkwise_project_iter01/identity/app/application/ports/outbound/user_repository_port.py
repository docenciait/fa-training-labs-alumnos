from typing import Protocol, Optional
from app.domain.models.user import User

class UserRepositoryPort(Protocol):
    def get_by_username(self, username: str) -> Optional[User]: ...
    def save(self, user: User) -> User: ...
