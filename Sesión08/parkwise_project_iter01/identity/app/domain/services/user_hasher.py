from app.domain.models.user import User
import hashlib

class UserHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        return UserHasher.hash_password(raw_password) == hashed_password
