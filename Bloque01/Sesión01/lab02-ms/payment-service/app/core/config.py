from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "payment-db"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "payment_db"

settings = Settings()