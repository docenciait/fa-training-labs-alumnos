from app.application.ports.outbound.user_repository_port import UserRepositoryPort
from app.domain.models.user import User
from typing import Optional

db_fake = {}

class InMemoryUserRepository(UserRepositoryPort):
    def get_by_username(self, username: str) -> Optional[User]:
        return db_fake.get(username)

    def save(self, user: User) -> User:
        user.id = len(db_fake) + 1
        db_fake[user.username] = user
        return user
